#include <database.h>
#include <stdlib.h>
#include <stdio.h>

void interface_init() {
   mongoc_init();
   mongoc_log_set_handler(interface_logger, NULL);
}

void interface_cleanup(mongoc_uri_t *uri, mongoc_client_pool_t *pool) {
   mongoc_client_pool_destroy(pool);
   mongoc_uri_destroy(uri);
   mongoc_cleanup();
}

void interface_logger(mongoc_log_level_t level, const char *domain, const char *message, void *data) {
   if (level < MONGOC_LOG_LEVEL_INFO) {
      mongoc_log_default_handler(level, domain, message, data);
   }
}

mongoc_client_pool_t *get_interface_pool() {
   mongoc_uri_t *uri;
   bson_error_t err;
   mongoc_client_pool_t *pool = NULL;

   const char *path = getenv("DB_PATH");

   uri = mongoc_uri_new_with_error(path, &err);

   if (!uri) {
      MONGOC_ERROR("Failed to parse URI string %s: %s\n", path, err.message);
      interface_cleanup(uri, pool);
      return NULL;
   }

   pool = mongoc_client_pool_new(uri);

   if (!pool) {
      interface_cleanup(uri, pool);
      return NULL;
   }
   mongoc_client_pool_set_error_api (pool, 2);
   interface_logger(MONGOC_LOG_LEVEL_DEBUG, "pool", "Successfully created interface pool!", NULL);
   
   return pool;
}

void worker_create_collection(void *data) {
   mongoc_client_t *client;

   mongoc_client_pool_t *pool = data;

   client = mongoc_client_pool_pop();

   if (!client) {
      interface_logger
   }

   mongoc_client_pool_push(pool, client);
}