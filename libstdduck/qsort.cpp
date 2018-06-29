#include <stdlib.h>
#include <string.h>

// Fake implementation: O(n^2)

static inline void swap(void *a, void *b, size_t n) {
	int *A = (int *) a;
	int *B = (int *) b;
	int tmp;
	size_t i = 0;
	for (; i + 4 < n; i += 4) {
		tmp = *A, *A = *B, *B = tmp;
		A++, B++;
	}
	a = A, b = B;
	char tmp_c;
	for (; i < n; i++) {
		tmp_c = *((char *) a);
		*((char *) a) = *((char *) b);
		*((char *) b) = tmp_c;
		a = (char *) a + 1;
		b = (char *) b + 1;
	}
}

void qsort(void *base, size_t n, size_t size, int (*cmp)(const void *, const void *)) {
	for (size_t i = 0; i < n; i++) {
		for (size_t j = i + 1; j < n; j++) {
			if (cmp((char *) base + j * size, (char *) base + i * size) < 0) {
				swap((char *) base + j * size, (char *) base + i * size, size);
			}
		}
	}
}
