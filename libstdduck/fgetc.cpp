#include <stdio.h>

namespace judgeduck {
	extern char *stdin_content;
	extern int stdin_size;
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

static char *stdin_start = NULL, *stdin_end, *stdin_pos;

int getchar() {
	if (stdin_start == NULL) {
		stdin_start = judgeduck::stdin_content;
		stdin_end = stdin_start + judgeduck::stdin_size;
		stdin_pos = stdin_start;
	}
	return stdin_start == stdin_end ? EOF : *(stdin_start++);
}

// TODO: Support ungetc
int ungetc(int c, FILE *f) {
	return EOF;
}
