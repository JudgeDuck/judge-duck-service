#include <stdlib.h>

// If there are multiple elements that match the key, the element returned is unspecified.
// Implementation: lower bound

void * bsearch(const void *key, const void *base, size_t n, size_t size, int (*cmp)(const void *, const void *)) {
	while (n) {
		size_t m = n >> 1;
		const void *mid = (const char *) base + size * m;
		int tmp = cmp(key, mid);
		if (tmp == 0) {
			return (void *) mid;
		} else if (tmp < 0) {
			base = (const char *) mid + size;
			n -= m;
		} else {
			n = m;
		}
	}
	return NULL;
}
