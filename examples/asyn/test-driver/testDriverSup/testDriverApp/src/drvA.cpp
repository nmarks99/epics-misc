#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "drvA.hpp"

static void poll_thread_C(void* pPvt) {
    DriverA* pDriverA = (DriverA*)pPvt;
    pDriverA->poll();
}

constexpr int ASYN_MASK = asynInt32Mask | asynDrvUserMask;
constexpr int ASYN_INTERRUPT = asynInt32Mask;

constexpr int MAX_ADDR = 1;
DriverA::DriverA(const char* name)
    : asynPortDriver(name, MAX_ADDR, ASYN_MASK, ASYN_INTERRUPT,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK, 1, 0, 0) {

    createParam("INT1", asynParamInt32, &int1Id_);

    epicsThreadCreate("DriverAPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium),
                      (EPICSTHREADFUNC)poll_thread_C, this);
}

void DriverA::poll() {
    while (true) {
        lock();

        setIntegerParam(int1Id_, 42);

        callParamCallbacks();
        unlock();
        epicsThreadSleep(1.0);
    }
}

asynStatus DriverA::writeInt32(asynUser *pasynUser, epicsInt32 value) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == int1Id_) {
        std::cout << "DriverA[writeInt32]: " << value << std::endl;
    }

    return status;
}

// register function for iocsh
extern "C" int DriverAConfig(const char* name) {
    new DriverA(name);
    return asynSuccess;
}

static const iocshArg driverAArg0 = {"Asyn driver name", iocshArgString};
static const iocshArg* const driverAArgs[1] = {&driverAArg0};
static const iocshFuncDef driverAFuncDef = {"DriverAConfig", 1, driverAArgs};

static void driverACallFunc(const iocshArgBuf* args) {
    DriverAConfig(args[0].sval);
}

void driverARegister(void) { iocshRegister(&driverAFuncDef, driverACallFunc); }

extern "C" {
epicsExportRegistrar(driverARegister);
}
