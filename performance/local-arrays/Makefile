CXX=mpic++

CFLAGS=-g $(shell adios2-config --cxx-flags)
LDFLAGS=$(shell adios2-config --cxx-libs)

all: writer reader

writer: larray_writer.o
	${CXX} -o writer larray_writer.o ${LDFLAGS}

reader: larray_reader.o
	${CXX} -o reader larray_reader.o ${LDFLAGS}

larray_writer.o: larray_writer.cpp
	${CXX} -c larray_writer.cpp ${CFLAGS}

larray_reader.o: larray_reader.cpp
	${CXX} -c larray_reader.cpp ${CFLAGS}

clean:
	rm -f reader writer *\.o
