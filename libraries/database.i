%module interface
%{
    #include "/usr/local/include/libmongoc-1.0/mongoc.h"
    #include "database.h"
%}

%include "database.h"