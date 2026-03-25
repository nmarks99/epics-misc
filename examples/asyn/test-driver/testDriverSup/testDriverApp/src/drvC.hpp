#pragma once
#include <asynPortDriver.h>

class DriverC : public asynPortDriver {
  public:
    DriverC(const char* name, const char* drvA_name, const char* drvB_name);
    virtual void poll(void);
    virtual asynStatus writeInt32(asynUser *pasynUser, epicsInt32 value);
  private:
    int count_ = 0;

  protected:
    int int1Id_;
};
