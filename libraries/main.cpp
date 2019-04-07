#include <database.hpp>
#include <iostream>

int main() {
    const char *path = std::getenv("MONGO_DB");
    auto location = mongocxx::uri{path};
    std::string db_name = "articles";
    std::string coll_name = "submitted";

    Database &inst = Database::get_instance();

    inst.create_instance(std::move(location));
    auto client = inst.create_new_collection(&db_name, &coll_name);
    return 0;
}