#include <cstdlib>
#include <new>

static std::new_handler the_new_handler = 0;

void * operator new (std::size_t size) {
	// Should not return null pointer
	if (size == 0) {
		size = 1;
	}
	while (true) {
		void *ret = malloc(size);
		if (ret) {
			return ret;
		}
		if (the_new_handler) {
			the_new_handler();
		} else {
			// Should throw std::bad_alloc(), but we have no exception... 
			return NULL;
		}
	}
}

void * operator new[] (std::size_t size) {
	// Try it best not to return null pointer
	if (size == 0) {
		size = 1;
	}
	void *ret = malloc(size);
	return ret;
}

void operator delete (void *p) {
	free(p);
}

void operator delete[] (void *p) {
	free(p);
}

namespace std {
	// Make it a page fault :)
	extern "C" void __throw_bad_alloc() {
		*(int *) 0 = 0;
	}
	
	new_handler set_new_handler(new_handler new_p) {
		new_handler ret = the_new_handler;
		the_new_handler = new_p;
		return ret;
	}
	
	extern "C" new_handler get_new_handler() {
		return the_new_handler;
	}
}
