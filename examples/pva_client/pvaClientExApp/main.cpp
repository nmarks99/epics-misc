#include "pv/pvData.h"
#include "pv/pvIntrospect.h"
#include <memory>
#include <ncurses.h>
#include <string>
#include <iostream>
#include <cassert>

#include <pva/client.h>
#include <pv/caProvider.h>

namespace pvd = epics::pvData;

int main(int argc, char *argv[]) {
    
    if (argc <= 1) {
        std::cout << "Please provide IOC prefix" << std::endl;
        return 1;
    }

    std::string prefix(argv[1]);

    epics::pvAccess::ca::CAClientFactory::start();
    pvac::ClientProvider provider("ca");
    
    // get the value of a array field as a double...
    // what the hell? why is this so complicated?
    // pvac::ClientChannel channel_test(provider.connect(prefix + "Receive:ActualTCP_X.VAL"));
    // auto value = channel_test.get()->getPVFields().at(0);
    // std::cout << "value = " << value << std::endl;
    // auto float_array_field = std::dynamic_pointer_cast<epics::pvData::PVScalarArray>(value);
    // epics::pvData::shared_vector<const float> float_values;
    // float_array_field->getAs(float_values);
    // std::vector<float> vec(float_values.begin(), float_values.end());
    // std::cout << "value double = " << vec.at(0) << std::endl;
    
    // Get a PV value and convert it to a primitive type (int, double, etc.)
    // the template argument in getSubFieldT must be the correct type
    std::cout << "\n--------------------------------------------------------------" << std::endl;
    std::cout << "double:" << std::endl;
    std::cout << "--------------------------------------------------------------" << std::endl;
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "WaypointJ:1:J1"));
        std::cout << channel_test.get() << std::endl;
        auto value = channel_test.get()->getSubFieldT<pvd::PVDouble>("value");
        std::cout << "value = " << value << std::endl;
        double val_prim = value->getAs<double>();
        std::cout << "val double = " << val_prim << std::endl;
    }

    std::cout << "\n--------------------------------------------------------------" << std::endl;
    std::cout << "string:" << std::endl;
    std::cout << "--------------------------------------------------------------" << std::endl;
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "ENGINEER"));
        std::cout << channel_test.get() << std::endl;
        auto value = channel_test.get()->getSubFieldT<pvd::PVString>("value");
        std::cout << "value = " << value << std::endl;
        std::string val_prim = value->getAs<std::string>();
        std::cout << "val std::string = " << val_prim << std::endl;
    }

    std::cout << "\n--------------------------------------------------------------" << std::endl;
    std::cout << "double array:" << std::endl;
    std::cout << "--------------------------------------------------------------" << std::endl;
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "Receive:ActualTCPPose"));
        std::cout << channel_test.get() << std::endl;
        auto value = channel_test.get()->getSubFieldT<pvd::PVValueArray<double>>("value");
        std::cout << "value = " << value << std::endl;
        epics::pvData::shared_vector<const double> epics_vec;
        value->getAs(epics_vec);
        std::cout << "value std::vector<double> = ";
        std::vector<double> vec(epics_vec.begin(), epics_vec.end());
        for (const auto &i : vec) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
    
    return 0; 
}
