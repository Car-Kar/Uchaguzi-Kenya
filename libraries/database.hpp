#ifndef DATABASE_H
#define DATABASE_H
#include <string>
#include <vector>
/* #include <cstdlib> */
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>

class Database {
    public:
        static Database *instance() {
            static Database *instance;
            return instance;
        }
        bool connect(const std::string, std::vector<std::string> *options = nullptr);
    private:
        Database() = default;
        /* static Database *instance; */
        const std::string *path;
        /* bool connect(std::string path); */
        mongocxx::uri *location;
        mongocxx::pool pool;

    protected:
};

#endif
