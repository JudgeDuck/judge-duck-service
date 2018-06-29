#include <stdio.h>

int fseek(FILE *f, long offset, int origin) {
	return -1;
}

long ftell(FILE *f) {
	return -1;
}

void rewind(FILE *f) {
	return void();
}

int fgetpos(FILE *f, fpos_t *pos) {
	return -1;
}

int fsetpos(FILE *f, const fpos_t *pos) {
	return -1;
}
