#include <chrono>
#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "apdDriver.hpp"

constexpr int PROCESS_DURATION = 5000; // milliseconds

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
      poll_time_(DEFAULT_POLL_TIME) {

    createParam(DONE_STRING, asynParamInt32, &doneIndex_);
    createParam(START_PROCESS_STRING, asynParamInt32, &startProcessIndex_);

    epicsThreadCreate("SimpleApdPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium), (EPICSTHREADFUNC)poll_thread_C, this);
}

void SimpleApd::poll() {
    while (true) {
        lock();

        if (running_) {
            setIntegerParam(doneIndex_, 0);
            std::chrono::duration<double> dur = std::chrono::steady_clock::now() -  t0_;
            double elap_ms = std::chrono::duration_cast<std::chrono::milliseconds>(dur).count();
            std::cout << "Elapsed: " << elap_ms << " ms" << std::endl;
            if (elap_ms >= PROCESS_DURATION) {
                setIntegerParam(doneIndex_, 1);
                std::cout << "Process Done" << std::endl;
                running_ = false;
            }
        } else {
            setIntegerParam(doneIndex_, 1);
        }
            

        callParamCallbacks();
        unlock();
        epicsThreadSleep(poll_time_);
    }
}


asynStatus SimpleApd::writeInt32(asynUser *pasynUser, epicsInt32 value) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == startProcessIndex_) {
        if (not running_) {
            std::cout << "Starting process [" << value << "]" << std::endl;
            running_ = true;
            this->t0_ = std::chrono::steady_clock::now();
        } else {
            std::cout << "Please wait for previous process to finish" << std::endl;
        }
    }
    
    return status;
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
