CFLAGS=-Wall -O3 -g -Wextra -Wno-unused-parameter
CXXFLAGS=$(CFLAGS)
BINARIES=text-example

# Paths for the rpi-rgb-led-matrix submodule
RGB_LIB_DISTRIBUTION=./rpi-rgb-led-matrix
RGB_INCDIR=$(RGB_LIB_DISTRIBUTION)/include
RGB_LIBDIR=$(RGB_LIB_DISTRIBUTION)/lib
RGB_LIBRARY_NAME=rgbmatrix
RGB_LIBRARY=$(RGB_LIBDIR)/lib$(RGB_LIBRARY_NAME).a

# Linker flags (link against rgbmatrix, pthread, etc.)
LDFLAGS += -L$(RGB_LIBDIR) -l$(RGB_LIBRARY_NAME) -lrt -lm -lpthread -lcurl

# Default target
all: text-example

# Rule to build the binary from text-example.cc
text-example: text-example.cc
	$(CXX) $(CXXFLAGS) -I$(RGB_INCDIR) -o $@ $^ $(LDFLAGS)

# Rule to build object files if needed
%.o: %.cc
	$(CXX) -I$(RGB_INCDIR) $(CXXFLAGS) -c -o $@ $<

# Clean target
clean:
	rm -f *.o $(BINARIES)
