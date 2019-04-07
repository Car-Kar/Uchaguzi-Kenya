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
#include <mongocxx/exception/exception.hpp>
#include <mongocxx/logger.hpp>
#include <mongocxx/uri.hpp>

class Logger : public mongocxx::logger {
    public:
        explicit Logger(std::ostream* stream) : _stream(stream) {}

        void operator() (mongocxx::log_level level, bsoncxx::stdx::string_view domain,
                    bsoncxx::stdx::string_view message) noexcept override {
            if (level >= mongocxx::log_level::k_trace)
                return;
            *_stream << '[' << mongocxx::to_string(level) << '@' << domain << "] " << message << '\n';
        }

        void handler(mongocxx::log_level level, bsoncxx::stdx::string_view domain,
                    bsoncxx::stdx::string_view message) noexcept {
            *_stream << '[' << mongocxx::to_string(level) << '@' << domain << "] " << message << '\n';           
        }

    private:
        std::ostream* const _stream;
};
/* enum class messages {
    debug = mongocxx::log_level::k_debug
}; */

class Database {
    public:
        static Database &get_instance();
        void configure(std::unique_ptr<mongocxx::instance> instance, std::unique_ptr<mongocxx::pool> p);
        void sanity();
        void create_instance(mongocxx::uri);
        bool create_new_collection(std::string *, std::string *);

        std::string handle_exception(std::string, const char *);

        Database(Database const&) = delete;             // Copy construct
        Database(Database&&) = delete;                  // Move construct
       /*  Database& operator=(Database const&) = delete;  // Copy assign
        Database& operator=(Database &&) = delete;   */

    private:
        const std::string *path;
        std::unique_ptr<mongocxx::instance> shared = nullptr;
        std::unique_ptr<mongocxx::pool> pool = nullptr;
        mongocxx::uri location;

        Database() = default;
        mongocxx::pool::entry get_connection();

    protected:
        Logger *log;
};

#endif