#ifndef _DRIVER_HPP_
#define _DRIVER_HPP_

#include <asynPortDriver.h>

// Dashboard interface
constexpr int MAX_CONTROLLERS = 1;
constexpr double DEFAULT_POLL_TIME = 0.10; // seconds
constexpr double DEFAULT_CONTROLLER_TIMEOUT = 1.0;

class SimpleApd : public asynPortDriver {
  public:
    SimpleApd(const char *asyn_port_name, const char *dev_port_name);
    virtual void poll(void);
    // virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);
    // virtual asynStatus writeOctet(asynUser *pasynUser, const char *value, size_t maxChars,
                                  // size_t *nActual);

  private:
    double poll_time_;
    int count_;

  protected:
    asynUser *pasynUserApd_;
};

#endif
