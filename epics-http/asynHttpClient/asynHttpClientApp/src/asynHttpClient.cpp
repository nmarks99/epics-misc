#include <chrono>
#include <cstdio>
#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "asynHttpClient.hpp"

static void poll_thread_C(void *pPvt) {
    AsynHttpClient *pAsynHttpClient = (AsynHttpClient *)pPvt;
    pAsynHttpClient->poll();
}

AsynHttpClient::AsynHttpClient(const char *asyn_port, const char *dev_port)
    : asynPortDriver(asyn_port, MAX_CONTROLLERS,
                     asynInt32Mask | asynFloat64Mask | asynDrvUserMask | asynOctetMask | asynInt32ArrayMask,
                     asynInt32Mask | asynFloat64Mask | asynOctetMask | asynInt32ArrayMask,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK,
                     1, /* ASYN_CANBLOCK=0, ASYN_MULTIDEVICE=1, autoConnect=1 */
                     0, 0),
      poll_time_(DEFAULT_POLL_TIME) {


    epicsThreadCreate("AsynHttpClientPoller", epicsThreadPriorityLow,
                      epicsThreadGetStackSize(epicsThreadStackMedium), (EPICSTHREADFUNC)poll_thread_C, this);
}

void AsynHttpClient::poll() {
    while (true) {
        lock();

        cpr::Response status_resp = cpr::Get(cpr::Url{"http://localhost:8000/users"});
        auto status_data = nlohmann::json::parse(status_resp.text);

        printf("%s\n", status_data.dump(2).c_str());

        callParamCallbacks();
        unlock();
        epicsThreadSleep(poll_time_);
    }
}


asynStatus AsynHttpClient::writeInt32(asynUser *pasynUser, epicsInt32 value) {
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
extern "C" int AsynHttpClientConfig(const char *asyn_port_name, const char *robot_ip) {
    AsynHttpClient *pAsynHttpClient = new AsynHttpClient(asyn_port_name, robot_ip);
    (void)pAsynHttpClient;
    return (asynSuccess);
}

static const iocshArg httpClientArg0 = {"Asyn port name", iocshArgString};
static const iocshArg httpClientArg1 = {"Device port name", iocshArgString};
static const iocshArg *const httpClientArgs[2] = {&httpClientArg0, &httpClientArg1};
static const iocshFuncDef httpClientFuncDef = {"AsynHttpClientConfig", 2, httpClientArgs};

static void httpClientCallFunc(const iocshArgBuf *args) { AsynHttpClientConfig(args[0].sval, args[1].sval); }

void AsynHttpClientRegister(void) { iocshRegister(&httpClientFuncDef, httpClientCallFunc); }

extern "C" {
epicsExportRegistrar(AsynHttpClientRegister);
}
