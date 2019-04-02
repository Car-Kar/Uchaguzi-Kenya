#include <database.hpp>
#include <iostream>

bool Database::connect(const std::string uri, std::vector<std::string> options)  {
    location = mongocxx::uri{uri};
    pool = mongocxx::pool{uri};
    if (pool->acquire()) {
        std::cout << "Successfully connected to remote db\n" << std::endl;
    }
    else
    {
        std::cout << "Could not connected to remote db\n" << std::endl;
    }
    
    return true;

}