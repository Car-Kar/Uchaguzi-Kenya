#ifndef DATABASE_H
#define DATABASE_H

#include <mongoc/mongoc.h>


void interface_init();
void interface_cleanup(mongoc_uri_t *, mongoc_client_pool_t *);
void interface_logger(mongoc_log_level_t level, const char *domain, const char *message, void *data);
mongoc_client_pool_t  *get_interface_pool();
void worker_create_collection(void *);
/*void worker_get_document(void *data);
void worker_add_document(void *data); */

#endif