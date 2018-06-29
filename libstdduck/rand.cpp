#include <stdlib.h>

// RAND_MAX = 2^31 - 1

static unsigned rand_next = 1;

int rand() {
	rand_next = rand_next * 1103515245 + 12345;
	return rand_next / 2;
}

void srand(unsigned int seed) {
	rand_next = seed;
}

int rand_r(unsigned int *seed) {
	*seed = *seed * 1103515245 + 12345;
	return *seed / 2;
}
