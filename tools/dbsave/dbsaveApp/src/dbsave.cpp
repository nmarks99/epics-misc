#include <iocsh.h>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <optional>
#include <fstream>

#include <dbDefs.h>
#include <epicsString.h>
#include <epicsExport.h>
#include <epicsStdio.h>
#include <epicsStdioRedirect.h>
#include <errlog.h>
#include <macLib.h>

#include <dbStaticLib.h>
#include <dbStaticPvt.h>

extern DBBASE *pdbbase;

// mostly copied from dbWriteRecord from dbStaticLib.h
long db_write_record_instance(DBBASE *pdbbase, const char *precordName, int level) {
    DBENTRY dbentry;
    DBENTRY *pdbentry=&dbentry;
    long    status;
    int     dctonly;

    dctonly = ((level>1) ? FALSE : TRUE);
    dbInitEntry(pdbbase,pdbentry);
    if (precordName) {
        if (*precordName == 0 || *precordName == '*') {
            precordName = 0;
	}
    }

    if(!precordName) {
	dbFinishEntry(pdbentry);
	return 0;
    } else {
        status = dbFindRecord(pdbentry, precordName);
        if(status) {
	    printf("db_write_record_instance: No record named %s found\n", precordName);
            dbFinishEntry(pdbentry);
            return status;
        }
    }

    if (!status) {
	if(dbIsVisibleRecord(pdbentry)) {
	    printf("grecord(%s, \"%s\") {\n", dbGetRecordTypeName(pdbentry), dbGetRecordName(pdbentry));
	} else {
	    printf("record(%s, \"%s\") {\n", dbGetRecordTypeName(pdbentry), dbGetRecordName(pdbentry));
	}

	status = dbFirstField(pdbentry, dctonly);
	while (!status) {
	    if (!dbIsDefaultValue(pdbentry) || level>0) {
		char *pvalstring = dbGetString(pdbentry);

		if (!pvalstring) {
		    printf("    field(%s, \"\")\n", dbGetFieldName(pdbentry));
		} else {
		    // don't show UDF field. Are there others we want to ignore?
		    if (strcmp(dbGetFieldName(pdbentry), "UDF") != 0) {
			printf("    field(%s, \"", dbGetFieldName(pdbentry));
			epicsStrPrintEscaped(stdout, pvalstring, strlen(pvalstring));
			printf("\")\n");
		    }
		}
	    } else if (level>0) {
		printf("    field(%s, \"\")\n", dbGetFieldName(pdbentry));
	    }
	    status = dbNextField(pdbentry, dctonly);
	}

	status = dbFirstInfo(pdbentry);
	while (!status) {
	    const char *pinfostr = dbGetInfoString(pdbentry);
	    printf("    info(\"%s\", \"", dbGetInfoName(pdbentry));
	    epicsStrPrintEscaped(stdout, pinfostr, strlen(pinfostr));
	    printf("\")\n");
	    status = dbNextInfo(pdbentry);
	}
	printf("}\n");
    }

    dbFinishEntry(pdbentry);
    return 0;
}

class MacWrapper {
  public:
    MacWrapper(const char *substitutions) {
	if(macCreateHandle(&macHandle, NULL)) {
	    fprintf(stderr, ERL_ERROR ": macCreateHandle failed\n");
	    if(macHandle) {
		macDeleteHandle(macHandle);
	    }
	    macHandle = NULL;
	    return;
	}

	if (substitutions == NULL) {
	    substitutions = "";
	}
	macParseDefns(macHandle, substitutions, &macPairs_);
	if(macPairs_ == NULL) {
	    macDeleteHandle(macHandle);
	    macHandle = NULL;
	} else {
	    macInstallMacros(macHandle, macPairs_);
	    free(macPairs_);
	}
    }

    ~MacWrapper() {
	if(macHandle) {
	    macDeleteHandle(macHandle);
	}
	macHandle = NULL;
    }

    std::optional<std::string> expand(const char *str) {
	long exp = macExpandString(macHandle, str, output_, MAC_SIZE);
	if (exp < 0) {
	    printf("%s has unexpanded macros\n", str);
	    return std::nullopt;
	} else {
	    return output_;
	}

    }

  private:
    MAC_HANDLE *macHandle = NULL;
    char **macPairs_;
    char output_[MAC_SIZE] = {'\0'};
};

void dbsave(const char *filename, const char *substitutions) {
    if (filename == nullptr) {
	printf("Usage: \".db file path\", \"macro substitutions\"\n");
	return;
    }

    std::ifstream fs(filename);
    if (!fs.is_open()) {
	printf("Couldn't open file '%s\n'", filename);
	return;
    }

    MacWrapper mac(substitutions);

    std::string line;
    std::string record_name;
    while (std::getline(fs, line)) {
	if (line[line.find_first_not_of(' ')] == '#') {
	    continue;
	}
	if (line.find("record") != std::string::npos) {
	    auto ind0 = line.find_first_of('"');
	    auto ind1 = line.find_last_of('"');
	    record_name = line.substr(ind0+1, ind1-ind0-1);
	    if (auto expanded = mac.expand(record_name.c_str()); expanded.has_value()) {
		db_write_record_instance(pdbbase, expanded.value().c_str(), 0);
	    }
	}
    }
}

extern "C" void dbsave_cfunc(const char *filename, const char *macros) {
    dbsave(filename, macros);
}

static const iocshArg dbsaveArg0 = {"db file", iocshArgString};
static const iocshArg dbsaveArg1 = {"Macros", iocshArgString};
static const iocshArg *const dbsaveArgs[] = {&dbsaveArg0, &dbsaveArg1};
static const iocshFuncDef dbsaveFuncDef = {"dbsave", 2 ,dbsaveArgs};
static void dbsaveCallFunc(const iocshArgBuf *args) { dbsave_cfunc(args[0].sval, args[1].sval); }
void dbsaveRegister(void) { iocshRegister(&dbsaveFuncDef, dbsaveCallFunc); }

extern "C" {
    epicsExportRegistrar(dbsaveRegister);
}
