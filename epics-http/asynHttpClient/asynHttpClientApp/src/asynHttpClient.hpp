#ifndef _DRIVER_HPP_
#define _DRIVER_HPP_

#include <asynPortDriver.h>

#include "nlohmann/json.hpp"
#include "cpr/cpr.h"

static constexpr char BASE_URL_STRING[] = "BASE_URL";
static constexpr char ENDPOINT_STRING[] = "ENDPOINT";
static constexpr char HTTP_GET_STRING[] = "HTTP_GET";
static constexpr char RESPONSE_STRING[] = "RESPONSE";

constexpr int MAX_CONTROLLERS = 1;
constexpr double DEFAULT_POLL_TIME = 1.0; // seconds

class AsynHttpClient : public asynPortDriver {
  public:
    AsynHttpClient(const char *asyn_port_name, const char *dev_port_name);
    // virtual void poll(void);
    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);
    virtual asynStatus writeOctet(asynUser *pasynUser, const char *value, size_t maxChars,size_t *nActual);

  private:
    double poll_time_;

    std::string base_url_;
    std::string endpoint_;
    std::string response_;

  protected:
    asynUser *pasynUserAsynHttpClient_;
    int baseUrlIndex_;
    int endpointIndex_;
    int httpGetIndex_;
    int responseIndex_;
};

#endif
