#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "drvA.hpp"
#include "drvB.hpp"
#include "drvC.hpp"

static void poll_thread_C(void* pPvt) {
    DriverC* pDriverC = (DriverC*)pPvt;
    pDriverC->poll();
}

constexpr int ASYN_MASK = asynInt32Mask | asynDrvUserMask;
constexpr int ASYN_INTERRUPT = asynInt32Mask;

constexpr int MAX_ADDR = 1;
DriverC::DriverC(const char* name, const char* drvA_name, const char* drvB_name)
    : asynPortDriver(name, MAX_ADDR, ASYN_MASK, ASYN_INTERRUPT,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK, 1, 0, 0) {

    std::cout << "Constructing DriverC\n";

    std::cout << "Looking up DriverA: " << drvA_name << "\n";
    DriverA* driverA = findDerivedAsynPortDriver<DriverA>(drvA_name);
    if (driverA) {
        std::cout << "DriverA " << drvA_name << " found\n";
        driverA->lock();

        int idx = 0;
        driverA->findParam("INT1", &idx);

        int drva_int = 0;
        driverA->getIntegerParam(idx, &drva_int);
        std::cout << "DriverA int = " << drva_int << std::endl;

        driverA->unlock();
    } else {
        std::cout << "Couldn't find DriverA\n";
        return;
    }

    std::cout << "Looking up DriverB: " << drvB_name << "\n";
    DriverB* driverB = findDerivedAsynPortDriver<DriverB>(drvB_name);
    if (driverB) {
        std::cout << "DriverB " << drvB_name << " found\n";
        driverB->lock();

        int idx = 0;
        driverB->findParam("INT1", &idx);

        int drvb_int = 0;
        driverB->getIntegerParam(idx, &drvb_int);
        std::cout << "DriverB int = " << drvb_int << std::endl;

        driverB->unlock();
    } else {
        std::cout << "Couldn't find DriverB\n";
        return;
    }


    createParam("INT1", asynParamInt32, &int1Id_);

    epicsThreadCreate("DriverCPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium),
                      (EPICSTHREADFUNC)poll_thread_C, this);
}

void DriverC::poll() {
    while (true) {
        lock();

        // std::cout << "Hello " << count_ << std::endl;
        // count_ += 1;

        callParamCallbacks();
        unlock();
        epicsThreadSleep(0.5);
    }
}

asynStatus DriverC::writeInt32(asynUser *pasynUser, epicsInt32 value) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == int1Id_) {
        std::cout << "DriverC[writeInt32]: " << value << std::endl;
    }

    return status;
}

// register function for iocsh
extern "C" int DriverCConfig(const char* name, const char* drvA_name, const char* drvB_name) {
    new DriverC(name, drvA_name, drvB_name);
    return asynSuccess;
}

static const iocshArg driverCArg0 = {"Asyn port name", iocshArgString};
static const iocshArg driverCArg1 = {"DrvA name", iocshArgString};
static const iocshArg driverCArg2 = {"DrvB name", iocshArgString};
static const iocshArg* const driverCArgs[3] = {&driverCArg0, &driverCArg1, &driverCArg2};
static const iocshFuncDef driverCFuncDef = {"DriverCConfig", 3, driverCArgs};

static void driverCCallFunc(const iocshArgBuf* args) {
    DriverCConfig(args[0].sval, args[1].sval, args[2].sval);
}

void driverCRegister(void) { iocshRegister(&driverCFuncDef, driverCCallFunc); }

extern "C" {
epicsExportRegistrar(driverCRegister);
}
