#ifndef DATABASE_H
#define DATABASE_H
#include <string>
#include <vector>

class Database {
    public:
        Database();
        ~Database();
        
    private:
        const std::string *path;
        bool connect(std::string path);
    protected:
};

#endif
