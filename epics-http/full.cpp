#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <thread>
#include <chrono>


int main() {
    std::string base_url = "http://localhost:3030/action?action_name=toggle_gripper";

    // Create action_vars
    nlohmann::json action_vars = {
        {"open", false},
        {"close", true}
    };

    // URL-encode the arguments
    auto encoded_args = cpr::util::urlEncode(action_vars.dump());
    std::string full_url = base_url + "&args=" + encoded_args.data();

    std::cout << "Full url: " << full_url << std::endl;

    // Send the POST request
    cpr::Response response = cpr::Post(cpr::Url{full_url});

    if (response.status_code != 200) {
        std::cerr << "Request failed with status code: " << response.status_code << std::endl;
        return 1;
    }

    // Parse the JSON response
    auto data = nlohmann::json::parse(response.text);
    std::cout << data.dump(2) << std::endl;

    std::string action_id = data["action_id"];
    std::string status_url = "http://localhost:3030/action/" + action_id;

    // Poll for result
    for (int i = 0; i < 10; ++i) {
        cpr::Response status_resp = cpr::Get(cpr::Url{status_url});
        auto status_data = nlohmann::json::parse(status_resp.text);
        std::cout << "Response: " << status_resp.status_code << std::endl;
        std::cout << status_data.dump(2) << std::endl;

        if (status_data["status"] == "succeeded") {
            std::cout << "Success: " << status_data["data"] << std::endl;
            break;
        } else if (status_data["status"] == "failed") {
            std::cerr << "Action failed: " << status_data["errors"] << std::endl;
            break;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    return 0;
}

// #include <nlohmann/json.hpp>
// #include <string>
// #include <iostream>
//
// bool is_valid_json(const std::string& input) {
    // try {
        // auto j = nlohmann::json::parse(input);
        // return true;
    // } catch (const nlohmann::json::parse_error& e) {
        // return false;
    // }
// }
//
// int main() {
    // std::string good = R"({"key": "value"})";
    // std::string bad = R"({key: value})";
//
    // std::cout << "Good? " << is_valid_json(good) << "\n";
    // std::cout << "Bad? " << is_valid_json(bad) << "\n";
//
    // return 0;
// }
