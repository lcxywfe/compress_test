all: gdal_translate.so

gdal_translate.so: gdal_translate.o
	gcc -shared -o libgdal_translate.so gdal_translate.o

gdal_translate.o: gdal_translate.cpp
	gcc -c gdal_translate.cpp -o gdal_translate.o -O3

.PHONY: clean
clean:
	rm -f *.o *.so
