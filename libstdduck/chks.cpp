#include <stdio.h>

// Why glibc use these functions ??????

size_t __fread_chk(void *p, size_t plen, size_t size, size_t n, FILE *f) {
	return fread(p, size, n, f);
}

size_t __fwrite_chk(const void *p, size_t plen, size_t size, size_t n, FILE *f) {
	return fwrite(p, size, n, f);
}
