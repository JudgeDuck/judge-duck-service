#include <cstdlib>
#include <new>

static std::new_handler the_new_handler = 0;

void * operator new (std::size_t size) {
	void *ret = malloc(size);
	if (!ret) {
		the_new_handler();
	}
	return ret;
}

void * operator new[] (std::size_t size) {
	void *ret = malloc(size);
	if (!ret) {
		the_new_handler();
	}
	return ret;
}

void operator delete (void *p) {
	return free(p);
}

void operator delete[] (void *p) {
	return free(p);
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
