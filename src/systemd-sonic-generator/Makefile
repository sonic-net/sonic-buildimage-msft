CC=gcc
CFLAGS=-std=gnu99 -D_GNU_SOURCE

CXX=g++
CXXFLAGS += -std=c++11 -D_GNU_SOURCE -I ./
LDFLAGS += -l stdc++ -lpthread -lboost_filesystem -lboost_system -lgtest

BINARY = systemd-sonic-generator
MAIN_TARGET = $(BINARY)_1.0.0_$(CONFIGURED_ARCH).deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	dpkg-buildpackage -us -uc -b -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	mv ../$(MAIN_TARGET) $(DEST)/
	rm ../$(BINARY)-* ../$(BINARY)_*

$(BINARY): systemd-sonic-generator.cpp
	rm -f ./systemd-sonic-generator

	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

install: $(BINARY)
	mkdir -p $(DESTDIR)
	mkdir -p $(DESTDIR)/lib
	mkdir -p $(DESTDIR)/lib/systemd
	mkdir -p $(DESTDIR)/lib/systemd/system-generators
	cp ./systemd-sonic-generator $(DESTDIR)/lib/systemd/system-generators

.PHONY: test
test: ssg_test
	./ssg_test

ssg_test: ssg-test.cc systemd-sonic-generator.o
	$(CXX) $(CXXFLAGS) -ggdb -o $@ $^ $(LDFLAGS)

systemd-sonic-generator.o: systemd-sonic-generator.cpp
	$(CXX) $(CXXFLAGS) -ggdb -D_SSG_UNITTEST -o $@ -c $^

all: $(BINARY) test

clean:
	rm -f ./systemd-sonic-generator
	rm -f ./systemd-sonic-generator.o
	rm -f ./ssg_test
