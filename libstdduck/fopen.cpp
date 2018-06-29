#include <stdio.h>

// Fake implementation

FILE * fopen(const char *path, const char *mode) {
	return NULL;
}

FILE * freopen(const char *path, const char *mode, FILE *f) {
	return NULL;
}
