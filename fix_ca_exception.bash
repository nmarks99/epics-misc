# When you have multiple network interfaces and both EPICS server and client
# programs on the same host, you'll get a CA warning about "multiple identical
# pv names...". Setting the below enviroment variables fixes it

export EPICS_CA_AUTO_ADDR_LIST=NO
export EPICS_CA_ADDR_LIST=164.54.104.7
