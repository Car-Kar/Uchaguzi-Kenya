#ifndef DATABASE_H
#define DATABASE_H
#include <string>
#include <vector>
#include <cstdlib>
#include <memory>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <mongocxx/pool.hpp>

#include <bsoncxx/stdx/make_unique.hpp>
#include <bsoncxx/stdx/optional.hpp>
#include <bsoncxx/stdx/string_view.hpp>
#include <mongocxx/logger.hpp>
#include <mongocxx/uri.hpp>

class Database {
    public:
        static Database &get_instance();
        void configure(std::unique_ptr<mongocxx::instance> instance, std::unique_ptr<mongocxx::pool> p);
        void sanity();
        void create_instance(mongocxx::uri);
        bool connect(const std::string, std::vector<std::string> *options = nullptr);
        Database(Database const&) = delete;             // Copy construct
        Database(Database&&) = delete;                  // Move construct
        Database& operator=(Database const&) = delete;  // Copy assign
        Database& operator=(Database &&) = delete;  

    private:
        Database() = default;
        /* static Database *instance; */
        const std::string *path;
        /* bool connect(std::string path); */

        std::unique_ptr<mongocxx::instance> shared = nullptr;
        std::unique_ptr<mongocxx::pool> pool = nullptr;
        mongocxx::uri location;
       /*  mongocxx::pool pool; */

    protected:
};
#endif
