#include <database.hpp>
#include <iostream>

int main() {
    class noop_logger : public mongocxx::logger {
       public:
        virtual void operator()(mongocxx::log_level,
                                bsoncxx::stdx::string_view,
                                bsoncxx::stdx::string_view) noexcept {}
    };
    const std::string path = "mongodb+srv://root:h#1kiJivP1Gd@jumuiya-fq7b8.mongodb.net/test?retryWrites=true";
    auto location = mongocxx::uri{path};
    auto instance =  bsoncxx::stdx::make_unique<mongocxx::instance>(bsoncxx::stdx::make_unique<noop_logger>());
    Database &inst = Database::get_instance();
    /* inst.configure(std::move(instance), bsoncxx::stdx::make_unique<mongocxx::pool>(std::move(location))); */
    inst.create_instance(std::move(location));
    /* db->connect(path); */
    inst.sanity();
    return 0;
}