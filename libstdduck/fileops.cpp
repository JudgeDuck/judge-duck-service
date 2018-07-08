#include <stdio.h>
#include <string.h>

#define static_assert(x)	switch ((int) (x)) case 0: case (x):

namespace judgeduck {
	extern char *stdin_content;
	extern int stdin_size;
	
	extern char *stdout_content;
	extern int stdout_size;
	extern int stdout_max_size;
}

// Implementation

static char *stdin_start, *stdin_end, *stdin_pos;
static char *stdout_start, *stdout_end, *stdout_pos, *stdout_limit;

// You need to account for any result if you modify these variables.
// The libtaskduck will have a complete check before using them.

namespace stdduck {
	void init_fileops() {
		stdin_start = judgeduck::stdin_content;
		stdin_pos = stdin_start;
		stdin_end = stdin_start + judgeduck::stdin_size;
		
		stdout_start = judgeduck::stdout_content;
		stdout_end = stdout_start;
		stdout_pos = stdout_start;
		stdout_limit = stdout_start + judgeduck::stdout_max_size;
	}

	void fini_fileops() {
		judgeduck::stdout_size = stdout_end - stdout_start;
	}
}

// ==============

int fclose(FILE *f) {
	return EOF;
}

void clearerr(FILE *f) {
	return void();
}

int feof(FILE *f) {
	if (f == stdin) {
		return stdin_pos == stdin_end;
	} else {
		return 1;
	}
}

int ferror(FILE *f) {
	// TODO
	return 1;
}

int fflush(FILE *f) {
	if (f == stdin || f == stdout || f == stderr) {
		return 0;
	} else {
		return EOF;
	}
}

FILE * fopen(const char *path, const char *mode) {
	return NULL;
}

FILE * freopen(const char *path, const char *mode, FILE *f) {
	return NULL;
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
	if (stdout_pos < stdout_limit) {
		*(stdout_pos++) = (char) c;
		if (stdout_pos > stdout_end) {
			stdout_end = stdout_pos;
		}
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

size_t fread(void *a, size_t size, size_t n, FILE *f) {
	if (!size || !n) {
		return 0;
	}
	if (f != stdin) {
		return 0;
	}
	if (1ull * size * n > 2147483647u) {
		return 0;
	}
	size_t ret = (stdin_end - stdin_pos) / size;
	if (ret > n) {
		ret = n;
	}
	size_t len = size * ret;
	memcpy(a, stdin_pos, len);
	stdin_pos += len;
	return ret;
}

size_t fwrite(const void *a, size_t size, size_t n, FILE *f) {
	if (!size || !n) {
		return 0;
	}
	if (f != stdout) {
		return 0;
	}
	size_t ret = (stdout_limit - stdout_pos) / size;
	if (ret > n) {
		ret = n;
	}
	size_t len = size * ret;
	memcpy(stdout_pos, a, len);
	stdout_pos += len;
	if (stdout_pos > stdout_end) {
		stdout_end = stdout_pos;
	}
	return ret;
}

int fseek(FILE *f, long offset, int origin) {
	if (f == stdin) {
		char *tmp;
		if (origin == SEEK_SET) {
			tmp = stdin_start;
		} else if (origin == SEEK_CUR) {
			tmp = stdin_pos;
		} else if (origin == SEEK_END) {
			tmp = stdin_end;
		} else {
			return -1;
		}
		tmp += offset;
		if (tmp < stdin_start || tmp > stdin_end) {
			return -1;
		}
		stdin_pos = tmp;
		return 0;
	} else if (f == stdout) {
		char *tmp;
		if (origin == SEEK_SET) {
			tmp = stdout_start;
		} else if (origin == SEEK_CUR) {
			tmp = stdout_pos;
		} else if (origin == SEEK_END) {
			tmp = stdout_end;
		} else {
			return -1;
		}
		tmp += offset;
		if (tmp < stdout_start || tmp > stdout_end) {
			return -1;
		}
		stdout_pos = tmp;
		return 0;
	} else {
		return EOF;
	}
}

long ftell(FILE *f) {
	if (f == stdin) {
		return stdin_pos - stdin_start;
	} else if (f == stdout) {
		return stdout_pos - stdout_start;
	} else {
		return -1l;
	}
}

void rewind(FILE *f) {
	if (f == stdin) {
		stdin_pos = stdin_start;
	} else if (f == stdout) {
		stdout_pos = stdout_start;
	}
}

int fgetpos(FILE *f, fpos_t *pos) {
	static_assert(sizeof(fpos_t) >= sizeof(long));
	if (f == stdin) {
		*(long *) pos = stdin_pos - stdin_start;
		return 0;
	} else if (f == stdout) {
		*(long *) pos = stdout_pos - stdout_start;
		return 0;
	} else {
		return -1;
	}
}

int fsetpos(FILE *f, const fpos_t *pos) {
	return fseek(f, *(const long *) pos, SEEK_SET);
}

int fgetc(FILE *f) {
	if (f != stdin) {
		return EOF;
	} else {
		return getchar();
	}
}

char * fgets(char *s, int size, FILE *f) {
	if (f != stdin || size <= 0) {
		return NULL;
	}
	
	int n_read = 0;
	--size;
	char *ret = s;
	while (n_read < size) {
		char c = getchar();
		if (c == EOF) {
			break;
		}
		++n_read;
		*(s++) = c;
		if (c == '\n') {
			break;
		}
	}
	*s = '\0';
	return ret;
}

int getc(FILE *f) {
	return fgetc(f);
}

int getchar() {
	return stdin_pos == stdin_end ? EOF : *(stdin_pos++);
}

// TODO: Support ungetc
int ungetc(int c, FILE *f) {
	return EOF;
}

