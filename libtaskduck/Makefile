# Run 'make V=1' to turn on verbose commands, or 'make V=0' to turn them off.
ifeq ($(V),1)
override V =
endif
ifeq ($(V),0)
override V = @
endif


USER_CFLAGS := -pipe -fno-builtin -O2 -std=gnu99 -MD -fno-omit-frame-pointer -static -Wall -Wno-format -Wno-unused -gstabs -m32 -fno-tree-ch -fno-stack-protector -I../libjudgeduck_include -I../libtaskduck_include -DJOS_USER -gstabs 
# USER_CFLAGS := $(USER_CFLAGS) -DJD_OLD_MEMORY_LIMIT

USER_CXXFLAGS := -pipe -fno-builtin -O2 -MD -fno-omit-frame-pointer -static -Wall -Wno-format -Wno-unused -gstabs -m32 -fno-tree-ch -fno-stack-protector -I../libjudgeduck_include -I../libtaskduck_include -DJOS_USER -gstabs 
# USER_CXXFLAGS := $(USER_CXXFLAGS) -DJD_OLD_MEMORY_LIMIT

OBJDIR := .

CC := gcc
CXX := g++
AS := as
AR := ar

LIB_SRCFILES :=	\
			taskduck_essentials.cpp \
			taskduck_cmp.cpp \
			taskduck_judge.cpp \
			taskduck_do_judge.cpp \
			taskduck_malloc.cpp \
			taskduck_destructor.cpp \



LIB_OBJFILES := $(patsubst %.c, $(OBJDIR)/%.o, $(LIB_SRCFILES))
LIB_OBJFILES := $(patsubst %.cpp, $(OBJDIR)/%.o, $(LIB_SRCFILES))
LIB_OBJFILES := $(patsubst %.S, $(OBJDIR)/%.o, $(LIB_OBJFILES))

all: $(OBJDIR)/libtaskduck.a

.SUFFIXES:

.DELETE_ON_ERROR:

.PRECIOUS: %.o


.PHONY: FORCE



$(OBJDIR)/%.o: %.c
	@echo + cc[USER] $<
	$(V)$(CC)  $(USER_CFLAGS) -c -o $@ $<

$(OBJDIR)/%.o: %.cpp
	@echo + cxx[USER] $<
	$(V)$(CXX)  $(USER_CXXFLAGS) -c -o $@ $<

$(OBJDIR)/%.o: %.S
	@echo + as[USER] $<
	$(V)$(CC)  $(USER_CFLAGS) -c -o $@ $<

$(OBJDIR)/libtaskduck.a: $(LIB_OBJFILES)
	@echo + ar $@
	$(V)$(AR) r $@ $(LIB_OBJFILES)

clean:
	rm -rf *.d *.o *.a
