#include <stdlib.h>

extern void (*__preinit_array_start)();
extern void (*__preinit_array_end)();
extern void (*__init_array_start)();
extern void (*__init_array_end)();
extern void (*__fini_array_start)();
extern void (*__fini_array_end)();

namespace stdduck {
	extern void init_fileops();
	extern void fini_fileops();
}

void libstdduck_init() {
	int n;
	
	stdduck::init_fileops();
	
	n = &__preinit_array_end - &__preinit_array_start;
	for (int i = 0; i < n; i++) {
		(*(&__preinit_array_start + i))();
	}
	
	n = &__init_array_end - &__init_array_start;
	for (int i = 0; i < n; i++) {
		(*(&__init_array_start + i))();
	}
}

void libstdduck_fini() {
	int n;
	
	n = &__fini_array_end - &__fini_array_start;
	for (int i = n - 1; i >= 0; i--) {
		(*(&__fini_array_start + i))();
	}
	
	stdduck::fini_fileops();
}
