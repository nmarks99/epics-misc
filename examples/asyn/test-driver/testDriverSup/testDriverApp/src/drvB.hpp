#pragma once
#include <asynPortDriver.h>

class DriverB : public asynPortDriver {
  public:
    DriverB(const char* name);
    virtual void poll(void);
    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);

  protected:
    int int1Id_;
};
