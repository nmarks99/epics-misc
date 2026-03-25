#include <chrono>
#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "drvB.hpp"

static void poll_thread_C(void* pPvt) {
    DriverB* pDriverB = (DriverB*)pPvt;
    pDriverB->poll();
}

constexpr int ASYN_MASK = asynInt32Mask | asynDrvUserMask;
constexpr int ASYN_INTERRUPT = asynInt32Mask;

constexpr int MAX_ADDR = 1;
DriverB::DriverB(const char* name)
    : asynPortDriver(name, MAX_ADDR, ASYN_MASK, ASYN_INTERRUPT,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK, 1, 0, 0) {

    createParam("INT1", asynParamInt32, &int1Id_);

    epicsThreadCreate("DriverBPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium),
                      (EPICSTHREADFUNC)poll_thread_C, this);
}

void DriverB::poll() {
    while (true) {
        lock();

        setIntegerParam(int1Id_, 1999);

        callParamCallbacks();
        unlock();
        epicsThreadSleep(1.0);
    }
}

asynStatus DriverB::writeInt32(asynUser *pasynUser, epicsInt32 value) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == int1Id_) {
        std::cout << "DriverB[writeInt32]: " << value << std::endl;
    }

    return status;
}

// register function for iocsh
extern "C" int DriverBConfig(const char* name) {
    new DriverB(name);
    return asynSuccess;
}

static const iocshArg driverBArg0 = {"Asyn port name", iocshArgString};
static const iocshArg* const driverBArgs[1] = {&driverBArg0};
static const iocshFuncDef driverBFuncDef = {"DriverBConfig", 1, driverBArgs};

static void driverBCallFunc(const iocshArgBuf* args) {
    DriverBConfig(args[0].sval);
}

void driverBRegister(void) { iocshRegister(&driverBFuncDef, driverBCallFunc); }

extern "C" {
epicsExportRegistrar(driverBRegister);
}
