# Run 'make V=1' to turn on verbose commands, or 'make V=0' to turn them off.
ifeq ($(V),1)
override V =
endif
ifeq ($(V),0)
override V = @
endif


USER_CFLAGS := -pipe -fno-builtin -O2 -std=gnu99 -MD -fno-omit-frame-pointer -static -Wall -Wno-format -Wno-unused -gstabs -m32 -fno-tree-ch -fno-stack-protector -I../libjudgeduck_include -DJOS_USER -gstabs 
# USER_CFLAGS := $(USER_CFLAGS) -DJD_OLD_MEMORY_LIMIT

USER_CXXFLAGS := -pipe -fno-builtin -O2 -MD -fno-omit-frame-pointer -static -Wall -Wno-format -Wno-unused -gstabs -m32 -fno-tree-ch -fno-stack-protector -I../libjudgeduck_include -DJOS_USER -gstabs 
# USER_CXXFLAGS := $(USER_CXXFLAGS) -DJD_OLD_MEMORY_LIMIT

OBJDIR := .

CC := gcc
CXX := g++
AS := as
AR := ar

LIB_SRCFILES :=	\
			init_fini.cpp \
			exit.cpp \
			malloc.cpp \
			atoi.cpp \
			rand.cpp \
			getenv.cpp \
			system.cpp \
			bsearch.cpp \
			qsort.cpp \
			abs.cpp \
			div.cpp \
			stdin.cpp \
			remove.cpp \
			rename.cpp \
			fclose.cpp \
			fflush.cpp \
			tmpfile.cpp \
			fopen.cpp \
			setbuf.cpp \
			fgetc.cpp \
			fputc.cpp \
			fread.cpp \
			fseek.cpp \
			feof.cpp \
			perror.cpp \
			# [TODO] strtol
			# [TODO] strtod
			# [TODO fake] atoi
			# [TODO] [imp] malloc
			# [TODO] [imp] getenv
			# [fake] system
			# [fake] qsort | O(n^2)
			# [fake] stdin (=1)
			# [fake] remove
			# [fake] rename
			# [fake] fclose
			# [fake] fflush
			# [fake] tmpfile
			# [fake] fopen, freopen
			# [fake] setbuf, setbuffer, setlinebuf, setvbuf
			# [TODO] fprintf
			# [TODO] fscanf
			# [TODO imp] getchar (!)
			# [TODO imp] ungetc
			# [TODO imp] putchar, puts
			# [TODO imp] fread, fwrite
			# [TODO imp] fseek
			# [TODO imp] feof
			# [fake] perror
			# [N] qsort_r
			# [N] abort, atexit
			# [N] mblen
			# [N] tmpnam



LIB_OBJFILES := $(patsubst %.c, $(OBJDIR)/%.o, $(LIB_SRCFILES))
LIB_OBJFILES := $(patsubst %.cpp, $(OBJDIR)/%.o, $(LIB_SRCFILES))
LIB_OBJFILES := $(patsubst %.S, $(OBJDIR)/%.o, $(LIB_OBJFILES))

all: $(OBJDIR)/libstdduck.a

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

$(OBJDIR)/libstdduck.a: $(LIB_OBJFILES)
	@echo + ar $@
	$(V)$(AR) r $@ $(LIB_OBJFILES)

clean:
	rm -rf *.d *.o *.a
