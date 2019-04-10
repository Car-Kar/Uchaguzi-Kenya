#ifndef DATABASE_H
#define DATABASE_H

#include <mongoc/mongoc.h>

void interface_init();
mongoc_client_pool_t  *get_interface_pool();
#endif