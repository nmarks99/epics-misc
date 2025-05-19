#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <iostream>

// {
  // "users": [
    // {
      // "id": 1,
      // "name": "Alice"
    // },
    // {
      // "id": 2,
      // "name": "Bob"
    // }
  // ]
// }



const int DUMP_INDENT = 2;

int main() {

    std::string status_url = "http://localhost:8000/users";

    cpr::Response status_resp = cpr::Get(cpr::Url{status_url});
    auto status_data = nlohmann::json::parse(status_resp.text);
    std::cout << "Response: " << status_resp.status_code << std::endl;
    std::cout << status_data.dump(DUMP_INDENT) << std::endl;

    for (const auto &u : status_data["users"]) {
        std::cout << "found user " << u << std::endl;
    }

    return 0;
}
