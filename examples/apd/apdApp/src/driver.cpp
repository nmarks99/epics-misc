#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "driver.hpp"

static void poll_thread_C(void *pPvt) {
    SimpleApd *pSimpleApd = (SimpleApd *)pPvt;
    pSimpleApd->poll();
}

SimpleApd::SimpleApd(const char *asyn_port, const char *dev_port)
    : asynPortDriver(asyn_port, MAX_CONTROLLERS,
                     asynInt32Mask | asynFloat64Mask | asynDrvUserMask | asynOctetMask | asynInt32ArrayMask,
                     asynInt32Mask | asynFloat64Mask | asynOctetMask | asynInt32ArrayMask,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK,
                     1, /* ASYN_CANBLOCK=0, ASYN_MULTIDEVICE=1, autoConnect=1 */
                     0, 0),
      poll_time_(DEFAULT_POLL_TIME), count_(0) {

    epicsThreadCreate("SimpleApdPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium), (EPICSTHREADFUNC)poll_thread_C, this);
}

void SimpleApd::poll() {
    while (true) {
        lock();

	std::cout << "Hello World "  << this->count_ << std::endl;
	this->count_ += 1;

        callParamCallbacks();
        unlock();
        epicsThreadSleep(poll_time_);
    }
}


// register function for iocsh
extern "C" int SimpleApdConfig(const char *asyn_port_name, const char *robot_ip) {
    SimpleApd *pSimpleApd = new SimpleApd(asyn_port_name, robot_ip);
    pSimpleApd = NULL;
    return (asynSuccess);
}

static const iocshArg apdArg0 = {"Asyn port name", iocshArgString};
static const iocshArg apdArg1 = {"Device port name", iocshArgString};
static const iocshArg *const apdArgs[2] = {&apdArg0, &apdArg1};
static const iocshFuncDef apdFuncDef = {"SimpleApdConfig", 2, apdArgs};

static void apdCallFunc(const iocshArgBuf *args) { SimpleApdConfig(args[0].sval, args[1].sval); }

void SimpleApdRegister(void) { iocshRegister(&apdFuncDef, apdCallFunc); }

extern "C" {
epicsExportRegistrar(SimpleApdRegister);
}
