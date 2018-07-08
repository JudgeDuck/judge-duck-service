#include <cstdlib>

void * operator new (std::size_t size) {
	return malloc(size);
}

void * operator new[] (std::size_t size) {
	return malloc(size);
}

void operator delete (void *p) {
	return free(p);
}

void operator delete[] (void *p) {
	return free(p);
}

// Make it a page fault :)
namespace std {
	extern "C" void __throw_bad_alloc() {
		*(int *) 0 = 0;
	}
}
