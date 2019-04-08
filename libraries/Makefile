CXX:=g++

GEN_OUTPUT:=database
SWIG_OUTPUT:=interface
OBJECTS:=database.cpp main.cpp
INTERFACE:=database.i
CXXSRCS:=database.cpp

LOCATION:=$(shell pwd)
CXXFLAGS:=-g -std=c++11  -Wall -Wextra -fPIC
LIBRARY_PATH:=-L/usr/local/lib/
INCLUDE:=-I/usr/local/include/mongocxx/v_noabi \
		-I/usr/local/include/bsoncxx/v_noabi \
		-I$(LOCATION)

PYTHON_INCLUDE:=-I/usr/include/python3.6/
LIBRARIES:=-lmongocxx -lbsoncxx
LDFLAGS:=-Wl,-rpath,/usr/local/lib/

COMPILE:=$(CXX) $(CXXFLAGS) $(INCLUDE)

all: $(GEN_OUTPUT) $(SWIG_OUTPUT)

$(GEN_OUTPUT): $(OBJECTS)
	$(COMPILE) -o $@ $^ $(LIBRARIES) $(LIBRARY_PATH) $(LDFLAGS)

%.o: %.cpp
	$(COMPILE) -c $< -o $@

$(SWIG_OUTPUT):
	g++ -fPIC -c $(INCLUDE) $(PYTHON_INCLUDE) database.cpp -o database.o
	swig -c++ -python -o database.o database.i 

clean:
	rm -f *.o *.out database