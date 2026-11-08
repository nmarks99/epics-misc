#define SOL_ALL_SAFETIES_ON 1
#include <sol/sol.hpp>
#include <pvxs/client.h>

static pvxs::client::Context ctx;

void ensure_context() {
    if (!ctx) {
        ctx = pvxs::client::Context::fromEnv();
    }
}

static pvxs::Value get(const std::string& pv) {
    ensure_context();
    auto val = ctx.get(pv).exec()->wait();
    // auto ind = val["display.form.index"];
    // std::cout << ind.as<int>() << std::endl;
    return val;
}

extern "C" int luaopen_pvxs_lua(lua_State* L) {
    sol::state_view lua(L);
    sol::table module = lua.create_table();

    lua.new_usertype<pvxs::Value>(
        "Value",
        sol::meta_function::index,
        [](pvxs::Value& value, const std::string& key) {
            return value[key];
        }
    );

    module.set_function("get", get);

    module.push();
    return 1;
}
