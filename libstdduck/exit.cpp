#include <stdlib.h>

#define ATEXIT_MAX 32

static void (*atexit_funcs[ATEXIT_MAX])();
static int atexit_count = 0;

int atexit(void (*func)()) {
	if (atexit_count < ATEXIT_MAX) {
		atexit_funcs[atexit_count++] = func;
		return 0;
	} else {
		return -1;
	}
}

void exit(int x) {
	extern void libstdduck_fini();
	
	for (int i = atexit_count - 1; i >= 0; i--) {
		atexit_funcs[i]();
	}
	
	libstdduck_fini();
	
	_Exit(x);
}

extern "C" {
	extern void sys_quit_judge();
}

void _Exit(int x) {
	
	sys_quit_judge();
	
	while (1);
}

