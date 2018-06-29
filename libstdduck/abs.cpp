#include <stdlib.h>
#include <inttypes.h>

int abs(int x) {
	return x < 0 ? -x : x;
}

long int labs(long int x) {
	return x < 0 ? -x : x;
}

long long int llabs(long long int x) {
	return x < 0 ? -x : x;
}

intmax_t imaxabs(intmax_t x) {
	return x < 0 ? -x : x;
}
