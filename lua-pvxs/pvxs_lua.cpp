#define SOL_ALL_SAFETIES_ON 1
#include <iostream>
#include <sol/sol.hpp>

#include <pvxs/client.h>

void get(const std::string& pv) {
    auto ctx = pvxs::client::Context::fromEnv();
    auto val = ctx.get(pv).exec()->wait();
    std::cout << val << std::endl;
}

extern "C" int luaopen_pvxs_lua(lua_State* L) {
    sol::state_view lua(L);
    sol::table module = lua.create_table();

    module.set_function("get", get);

    module.push();
    return 1;
}
