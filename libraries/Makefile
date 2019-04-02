CXX:=g++

OUTPUT:=database
OBJECTS:=database.cpp main.cpp

LOCATION:=$(shell pwd)
CXXFLAGS:=-g -std=c++11  -Wall -Wextra
LIBRARY_PATH:=-L/usr/local/lib64/
INCLUDE:=-I/usr/local/include/mongocxx/v_noabi \
		-I/usr/local/include/bsoncxx/v_noabi \
		-I$(LOCATION)

LIBRARIES:=-lmongocxx -lbsoncxx
LDFLAGS:=-Wl,-rpath,/usr/local/lib64/

COMPILE:=$(CXX) $(CXXFLAGS) $(INCLUDE)

all: $(OUTPUT)

$(OUTPUT): $(OBJECTS)
	$(COMPILE) -o $@ $^ $(LIBRARIES) $(LIBRARY_PATH) $(LDFLAGS)

%.o: %.cpp
	$(COMPILE) -c $< -o $@

clean:
	rm -f *.o *.out database