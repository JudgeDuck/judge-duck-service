#include <stdlib.h>
#include <string.h>

namespace judgeduck {
	extern void *malloc_start;
}

static void *malloc_curpos = NULL;

static void * do_malloc(size_t size) {
	if (malloc_curpos == NULL) {
		malloc_curpos = judgeduck::malloc_start;
	}
	if (size > 0x7fffffffu) {
		return NULL;
	}
	void *ret = malloc_curpos;
	malloc_curpos = (char *) malloc_curpos + size;
	return ret;
}

void * malloc(size_t size) {
	if (size == 0) {
		return NULL;
	} else {
		return do_malloc(size);
	}
}

void * calloc(size_t n, size_t size) {
	if (n * size == 0) {
		return NULL;
	} else {
		void *ret = do_malloc(n * size);
		if (ret) {
			memset(ret, 0, n * size);
		}
		return ret;
	}
}

void * realloc(void *p, size_t size) {
	if (p == NULL) {
		return malloc(size);
	} else if (size == 0) {
		free(p);
		return NULL;
	} else {
		return NULL;
	}
}

void free(void *p) {
	return void();
}
