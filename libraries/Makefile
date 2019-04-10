CC:=gcc
LD:=ld

GEN_OUTPUT:=database
SWIG_OUTPUT:=interface
OBJECTS:=database.c
INTERFACE:=database.i

LOCATION:=$(shell pwd)
CFLAGS:=-g -Wall -Wextra -fPIC
LIBRARY_PATH:=-L/usr/local/lib/
INCLUDE:=-I/usr/local/include/libbson-1.0 -I/usr/local/include/libmongoc-1.0 \
		-I$(LOCATION)


PYTHON_INCLUDE:=-I/usr/include/python3.6/
LIBRARIES:=-lmongoc-1.0 -lbson-1.0
LDFLAGS:=-Wl,-rpath,/usr/local/lib/

COMPILE:=$(CC) $(CXXFLAGS) $(INCLUDE)

all: $(GEN_OUTPUT) $(SWIG_OUTPUT)

$(GEN_OUTPUT): $(OBJECTS)
	$(COMPILE) -o $@ $^ $(LIBRARIES) $(LIBRARY_PATH) $(LDFLAGS)

%.o: %.c
	$(COMPILE) -c $< -o $@

$(SWIG_OUTPUT):
	#swig -c++ -python database.i
	swig -python $(INTERFACE)
	$(CC) $(CFLAGS) -c $(INCLUDE) $(OBJECTS) -o database.o
	$(CC) $(CFLAGS) -c $(INCLUDE) $(PYTHON_INCLUDE) database_wrap.c -o database_wrap.o
	$(LD) -shared database.o database_wrap.o -o _interface.so $(LIBRARIES) $(LIBRARY_PATH)

clean:
	rm -f *.o *.so *.out database interface