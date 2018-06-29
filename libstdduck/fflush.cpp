#include <stdio.h>

// Fake implementation

int fflush(FILE *f) {
	if (f == stdin || f == stdout || f == stderr) {
		return 0;
	} else {
		return EOF;
	}
}
