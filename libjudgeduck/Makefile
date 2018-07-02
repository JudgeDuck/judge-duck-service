# Run 'make V=1' to turn on verbose commands, or 'make V=0' to turn them off.
ifeq ($(V),1)
override V =
endif
ifeq ($(V),0)
override V = @
endif

USER_CFLAGS := -pipe -fno-builtin -O2 -std=gnu99 -MD -fno-omit-frame-pointer -static -Wall -Wno-format -Wno-unused -gstabs -m32 -fno-tree-ch -fno-stack-protector -I../libjudgeduck_include -DJOS_USER -gstabs 
# USER_CFLAGS := $(USER_CFLAGS) -DJD_OLD_MEMORY_LIMIT

OBJDIR := .

CC := gcc
AS := as
AR := ar

LIB_SRCFILES :=		console.c \
			libmain.c \
			exit.c \
			panic.c \
			printf.c \
			printfmt.c \
			readline.c \
			string.c \
			syscall.c \
			ipc.c

LIB_SRCFILES :=		$(LIB_SRCFILES) \
			pgfault.c \
			pfentry.S \
			entry.S \

LIB_SRCFILES :=		$(LIB_SRCFILES) \
			args.c \
			fd.c \
			file.c \
			fprintf.c



LIB_OBJFILES := $(patsubst %.c, $(OBJDIR)/%.o, $(LIB_SRCFILES))
LIB_OBJFILES := $(patsubst %.S, $(OBJDIR)/%.o, $(LIB_OBJFILES))

all: $(OBJDIR)/libjudgeduck.a

.SUFFIXES:

.DELETE_ON_ERROR:

.PRECIOUS: %.o


.PHONY: FORCE



$(OBJDIR)/%.o: %.c
	@echo + cc[USER] $<
	$(V)$(CC) -nostdinc $(USER_CFLAGS) -c -o $@ $<

$(OBJDIR)/%.o: %.S
	@echo + as[USER] $<
	$(V)$(CC) -nostdinc $(USER_CFLAGS) -c -o $@ $<

$(OBJDIR)/libjudgeduck.a: $(LIB_OBJFILES)
	@echo + ar $@
	$(V)$(AR) r $@ $(LIB_OBJFILES)

clean:
	rm -rf *.d *.o *.a
