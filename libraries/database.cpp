#include <database.hpp>
#include <iostream>
#include <sstream>

#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <bsoncxx/stdx/string_view.hpp>
#include <mongocxx/logger.hpp>
#include <mongocxx/exception/exception.hpp>
#include <mongocxx/exception/bulk_write_exception.hpp>
#include <mongocxx/exception/error_code.hpp>
#include <mongocxx/exception/logic_error.hpp>
#include <mongocxx/exception/operation_exception.hpp>
#include <mongocxx/exception/server_error_code.hpp>

using bsoncxx::builder::basic::kvp;
using bsoncxx::builder::basic::make_document;

Database &Database::get_instance() {
    static Database instance;
    return instance;
}

void Database::create_instance(mongocxx::uri uri) {
    log = new Logger(&std::cout);
    auto inst = bsoncxx::stdx::make_unique<mongocxx::instance>(bsoncxx::stdx::make_unique<Logger>(&std::cout));
    auto pool = bsoncxx::stdx::make_unique<mongocxx::pool>(uri);
    configure(std::move(inst), std::move(pool));

    /* configure(inst, bsoncxx::stdx::make_unique<mongocxx::pool>(std::move(uri))); */
}


void Database::configure(std::unique_ptr<mongocxx::instance> instance, std::unique_ptr<mongocxx::pool> p) {
    shared = std::move(instance);
    pool = std::move(p);
}

void Database::sanity() {
    std::cout << "You're not insane!" << std::endl;
}

mongocxx::pool::entry Database::get_connection() {
    return pool->acquire();
}


std::string Database::handle_exception(std::string msg, const char *e) {
    std::stringstream err;
    err << msg << ": " << e;
    return err.str();
}

bool Database::create_new_collection(std::string *db, std::string *name) {
    auto client = get_connection();
    auto database = (*client)[*db];
    auto collection = bsoncxx::stdx::string_view(*name);

    try {
        mongocxx::collection coll = database.create_collection(collection, 
            make_document(kvp("validator", make_document(kvp("user_id", make_document(kvp("$gt", 0)))))));
        if (coll) {
            log->handler(mongocxx::log_level::k_info, __func__, "Created new collection");
        }
    }
    catch(const mongocxx::operation_exception &e) {
        if (e.code().category() != mongocxx::server_error_category()) {
            return false;
        }
        /*if (e.code() != mongocxx::error_code::k_invalid_collection_object) {
            return EXIT_FAILURE;
        }
         if (e.code().value() != 48) {
            return false;
        } */

        log->handler(mongocxx::log_level::k_error, __func__,  handle_exception("Collection already exists", e.what()));

        return true;
    }

    return true;
}