#include <stdlib.h>

// Fake implementation: always fails

int system(const char *command) {
	if (command == NULL) {
		return 0;
	} else {
		return -1;
	}
}
