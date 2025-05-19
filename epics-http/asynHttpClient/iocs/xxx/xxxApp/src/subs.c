#include <dbAccess.h>
#include <dbDefs.h>
#include <dbFldTypes.h>
#include <epicsExport.h>
#include <registryFunction.h>
#include <stdbool.h>
#include <stdio.h>
#include <subRecord.h>

static long sub_example(struct subRecord *psub) {
    printf("value of INPA = %d\n", (int)psub->a);
    return 0;
}

epicsRegisterFunction(sub_example);
