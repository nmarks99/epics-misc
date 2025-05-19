#ifndef _DRIVER_HPP_
#define _DRIVER_HPP_

#include <asynPortDriver.h>
#include <chrono>

#include "nlohmann/json.hpp"
#include "cpr/cpr.h"

static constexpr char DONE_STRING[] = "DONE";
static constexpr char START_PROCESS_STRING[] = "START_PROCESS";

constexpr int MAX_CONTROLLERS = 1;
constexpr double DEFAULT_POLL_TIME = 1.0; // seconds

class AsynHttpClient : public asynPortDriver {
  public:
    AsynHttpClient(const char *asyn_port_name, const char *dev_port_name);
    virtual void poll(void);
    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);
    // virtual asynStatus writeOctet(asynUser *pasynUser, const char *value, size_t maxChars,size_t *nActual);

  private:
    double poll_time_;
    bool running_ = false;
    std::chrono::steady_clock::time_point t0_;

  protected:
    asynUser *pasynUserAsynHttpClient_;
    int doneIndex_;
    int startProcessIndex_;
};

#endif
