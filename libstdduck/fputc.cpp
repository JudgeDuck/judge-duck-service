#include <stdio.h>

namespace judgeduck {
	extern char *stdout_content;
	extern int stdout_size;
	extern int stdout_max_size;
}

int fputc(int c, FILE *f) {
	if (f != stdout) {
		return EOF;
	} else {
		return putchar(c);
	}
}

int fputs(const char *s, FILE *f) {
	if (f != stdout) {
		return EOF;
	} else {
		return puts(s);
	}
}

int putc(int c, FILE *f) {
	return fputc(c, f);
}

int putchar(int c) {
	if (judgeduck::stdout_size < judgeduck::stdout_max_size) {
		judgeduck::stdout_content[judgeduck::stdout_size++] = c;
		return (int) (char) c;
	} else {
		return EOF;
	}
}

int puts(const char *s) {
	while (*s) {
		if (putchar(*(s++)) == EOF) {
			return EOF;
		}
	}
	return putchar('\n') == EOF ? EOF : 0;
}