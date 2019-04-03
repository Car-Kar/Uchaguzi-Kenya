#include <database.hpp>
#include <iostream>

Database &Database::get_instance() {
    static Database instance;
    return instance;
}

void Database::create_instance(mongocxx::uri uri) {
    class noop_logger : public mongocxx::logger {
       public:
        virtual void operator()(mongocxx::log_level,
                                bsoncxx::stdx::string_view,
                                bsoncxx::stdx::string_view) noexcept {}
    };
    auto inst = bsoncxx::stdx::make_unique<mongocxx::instance>(instance);
    configure(inst, bsoncxx::stdx::make_unique<mongocxx::pool>(std::move(uri)));
}

bool Database::connect(const std::string uri, std::vector<std::string> *options)  {

    location = mongocxx::uri{uri};
    /* create_instance(location); */
/*     if (pool.acquire()) {
        std::cout << "Successfully connected to remote db\n" << std::endl;
    }
    else
    {
        std::cout << "Could not connected to remote db\n" << std::endl;
    } */
    
    return true;

}

void Database::configure(std::unique_ptr<mongocxx::instance> instance, std::unique_ptr<mongocxx::pool> p) {
    shared = std::move(instance);
    pool = std::move(p);
}

void Database::sanity() {
    std::cout << "You're not insane!" << std::endl;
}