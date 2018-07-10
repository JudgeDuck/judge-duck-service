#include <taskduck.h>
#include <inc/lib.h>

void * TaskDuck::malloc(size_t size, bool alloc) {
	size = ROUNDUP(size, PGSIZE);
	if (!alloc) {
		return this->malloc_end = (char *) this->malloc_end - size;
	}
	char *ret = (char *) this->malloc_end - size;
	for (char *i = ret; i < this->malloc_end; i += PGSIZE) {
		if (sys_page_alloc(0, i, PTE_P | PTE_U | PTE_W) < 0) {
			// panic("malloc failed %p\n", i);
			jd_exit();
		}
	}
	this->malloc_end = ret;
	return ret;
}
