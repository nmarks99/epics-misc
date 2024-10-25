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

std::string get_value_type(pvac::ClientChannel &channel) {
    return epics::pvData::ScalarTypeFunc::name(
        std::dynamic_pointer_cast<const epics::pvData::Scalar>(
            channel.get()->getStructure()->getField("value"))->getScalarType()
    );
}

int main(int argc, char *argv[]) {
    
    if (argc <= 1) {
        std::cout << "Please provide IOC prefix" << std::endl;
        return 1;
    }

    std::string prefix(argv[1]);

    epics::pvAccess::ca::CAClientFactory::start();
    pvac::ClientProvider provider("ca");
    
    // Get a PV value and convert it to a primitive type (int, double, etc.)
    // the template argument in getSubFieldT must be the correct type
    std::cout << "\n--------------------------------------------------------------" << std::endl;
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "WaypointJ:1:J1"));
        std::cout << channel_test.get() << std::endl;
        auto value = channel_test.get()->getSubFieldT<pvd::PVDouble>("value");
        std::cout << "value = " << value << std::endl;
        double val_prim = value->getAs<double>();
        std::cout << "val double = " << val_prim << std::endl;
    }

    std::cout << "\n--------------------------------------------------------------" << std::endl;
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "ENGINEER"));
        std::cout << channel_test.get() << std::endl;
        auto value = channel_test.get()->getSubFieldT<pvd::PVString>("value");
        std::cout << "value = " << value << std::endl;
        std::string val_prim = value->getAs<std::string>();
        std::cout << "val std::string = " << val_prim << std::endl;
    }

    std::cout << "\n--------------------------------------------------------------" << std::endl;
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

    // get the type of a pv
    {
        pvac::ClientChannel channel_test(provider.connect(prefix + "m1.VAL"));
        std::cout << get_value_type(channel_test) << std::endl;
    }
    
    return 0; 
}
