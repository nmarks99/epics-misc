#include <ncurses.h>
#include <string>
#include <iostream>
#include <cassert>

#include <pva/client.h>
#include <pv/caProvider.h>

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
    pvac::ClientChannel channel_test(provider.connect(prefix + "Receive:ActualTCP_X.VAL"));
    auto value = channel_test.get()->getPVFields().at(0);
    std::cout << "value = " << value << std::endl;
    auto float_array_field = std::dynamic_pointer_cast<epics::pvData::PVScalarArray>(value);
    epics::pvData::shared_vector<const float> float_values;
    float_array_field->getAs(float_values);
    std::vector<float> vec(float_values.begin(), float_values.end());
    std::cout << "value double = " << vec.at(0) << std::endl;
    
    return 0; 
}
