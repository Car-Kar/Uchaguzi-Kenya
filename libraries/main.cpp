#include <database.hpp>

int main() {
    const std::string path = "mongodb+srv://root:h#1kiJivP1Gd@jumuiya-fq7b8.mongodb.net/test?retryWrites=true";
    Database *db = Database::instance();
    db->connect(path);
    return 0;
}