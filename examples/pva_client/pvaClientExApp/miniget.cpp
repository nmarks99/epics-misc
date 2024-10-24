/*
 * Copyright information and license terms for this software can be
 * found in the file LICENSE that is included with the distribution
 */
// The simplest possible PVA get

#include <iostream>

#include <pva/client.h>
#include <pv/caProvider.h>

int main(int argc, char *argv[]) {
    try {
        if(argc<=1) {
            std::cerr<<"Usage: "<<argv[0]<<" <pvname>\n";
            return 1;
        }

        // Get the PV using PV access provider
        pvac::ClientProvider pva_provider("pva");
        pvac::ClientChannel pva_channel(pva_provider.connect(argv[1]));
        std::cout<<pva_channel.name() << " : " << pva_channel.get() << std::endl;
    
        // Get the PV using channel access provider
        epics::pvAccess::ca::CAClientFactory::start();
        pvac::ClientProvider ca_provider("ca");
        pvac::ClientChannel ca_channel(ca_provider.connect(argv[1]));
        std::cout<<ca_channel.name() << " : " << ca_channel.get() << std::endl;



    } catch(std::exception& e){
        std::cerr<<"Error: "<<e.what()<<"\n";
        return 1;
    }
}
