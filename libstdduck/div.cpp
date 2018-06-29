#include <stdlib.h>
#include <inttypes.h>

div_t div(int a, int b) {
	return (div_t) {a / b, a % b};
}

ldiv_t ldiv(long a, long b) {
	return (ldiv_t) {a / b, a % b};
}

lldiv_t lldiv(long long a, long long b) {
	return (lldiv_t) {a / b, a % b};
}

imaxdiv_t imaxdiv(intmax_t a, intmax_t b) {
	return (imaxdiv_t) {a / b, a % b};
}
