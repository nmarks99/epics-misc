#include <chrono>
#include <cstdio>
#include <epicsExport.h>
#include <epicsThread.h>
#include <iocsh.h>
#include <iostream>

#include "asynHttpClient.hpp"

// static void poll_thread_C(void *pPvt) {
    // AsynHttpClient *pAsynHttpClient = (AsynHttpClient *)pPvt;
    // pAsynHttpClient->poll();
// }

AsynHttpClient::AsynHttpClient(const char *asyn_port, const char *dev_port)
    : asynPortDriver(asyn_port, MAX_CONTROLLERS,
                     asynInt32Mask | asynFloat64Mask | asynDrvUserMask | asynOctetMask | asynInt32ArrayMask,
                     asynInt32Mask | asynFloat64Mask | asynOctetMask | asynInt32ArrayMask,
                     ASYN_MULTIDEVICE | ASYN_CANBLOCK,
                     1, /* ASYN_CANBLOCK=0, ASYN_MULTIDEVICE=1, autoConnect=1 */
                     0, 0),
      poll_time_(DEFAULT_POLL_TIME) {

    createParam(BASE_URL_STRING, asynParamOctet, &baseUrlIndex_);
    createParam(ENDPOINT_STRING, asynParamOctet, &endpointIndex_);
    createParam(HTTP_GET_STRING, asynParamInt32, &httpGetIndex_);
    createParam(RESPONSE_STRING, asynParamOctet, &responseIndex_);

    // epicsThreadCreate("AsynHttpClientPoller", epicsThreadPriorityLow,
                      // epicsThreadGetStackSize(epicsThreadStackMedium), (EPICSTHREADFUNC)poll_thread_C, this);
}

// void AsynHttpClient::poll() {
    // while (true) {
        // lock();
//
        // // if (base_url_.length() > 0 && endpoint_.length() > 0) {
            // // cpr::Response status_resp = cpr::Get(cpr::Url{"http://localhost:8000/users"});
            // // auto status_data = nlohmann::json::parse(status_resp.text);
            // // printf("%s\n", status_data.dump(2).c_str());
        // // }
//
        // callParamCallbacks();
        // unlock();
        // epicsThreadSleep(poll_time_);
    // }
// }

asynStatus AsynHttpClient::writeOctet(asynUser *pasynUser, const char *value, size_t maxChars,size_t *nActual) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == baseUrlIndex_) {
        printf("Setting base URL to %s\n", value);
        base_url_ = value;
    } else if (function == endpointIndex_) {
        printf("Setting endpoint to %s\n", value);
        endpoint_ = value;
    }

    callParamCallbacks();
    return status;
}

asynStatus AsynHttpClient::writeInt32(asynUser *pasynUser, epicsInt32 value) {
    int function = pasynUser->reason;
    asynStatus status = asynSuccess;

    if (function == httpGetIndex_) {
        if (base_url_.length() > 0 && endpoint_.length() > 0) {
            std::cout << "here" << std::endl;
            std::string full_url = base_url_ + endpoint_;
            std::cout << "full url: " << full_url << std::endl;
            cpr::Response response = cpr::Post(cpr::Url{full_url});

            if (response.status_code != 200) {
                std::cerr << "Request failed with status code: " << response.status_code << std::endl;
                return asynError;
            }

            auto data = nlohmann::json::parse(response.text);

            std::string action_id = data["action_id"];
            std::string status_url = base_url_ + "/action/" + action_id;

            // Poll for result
            for (int i = 0; i < 10; ++i) {
                cpr::Response status_resp = cpr::Get(cpr::Url{status_url});
                if (status_resp.text.length() == 0) {
                    continue;
                }
                auto status_data = nlohmann::json::parse(status_resp.text);
                std::cout << "Response: " << status_resp.status_code << std::endl;
                std::cout << "status_data['data']: " << status_data["data"] << std::endl;
                // std::cout << status_data.dump(2) << std::endl;
                if (status_data["status"] == "succeeded") {
                    std::cout << "Success: " << status_data["data"] << std::endl;
                    std::string data = status_data["data"].dump(2);
                    setStringParam(responseIndex_, data);
                    break;
                } else if (status_data["status"] == "failed") {
                    std::cerr << "Action failed: " << status_data["errors"] << std::endl;
                    break;
                }
                epicsThreadSleep(0.2);
                // std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
        }

    }

    callParamCallbacks();
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
