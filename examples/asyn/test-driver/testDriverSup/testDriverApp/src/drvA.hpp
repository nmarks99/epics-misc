#pragma once
#include <asynPortDriver.h>

class DriverA : public asynPortDriver {
  public:
    DriverA(const char* name);
    virtual void poll(void);
    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);

  protected:
    int int1Id_;
};
