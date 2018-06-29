#include <taskduck.h>
#include <inc/lib.h>

#undef NULL
#define NULL 0

// Defaults:
// 1s, 256MB, 400MB, 64MB, input.txt, answer.txt, multiline_cmp
TaskDuck::TaskDuck() {
	this->time_ns = 1000 * 1000 * 1000;
	this->mem_kb = 256 * 1024;
	this->mem_kb_hard = 400 * 1024;
	this->max_output_size = 64 * 1024 * 1024;
	this->input_filename = "input.txt";
	this->answer_filename = "answer.txt";
	this->malloc_end = (void *) 0xd0000000;
	this->cmp = TaskDuck::multiline_cmp;
	this->memory_allocated = false;
	this->message = NULL;
}

void TaskDuck::set_time_limit(long long time_ns) {
	this->time_ns = time_ns;
}

void TaskDuck::set_memory_limit(int mem_kb) {
	this->mem_kb = mem_kb;
}

void TaskDuck::set_memory_hard_limit(int mem_kb) {
	this->mem_kb_hard = mem_kb;
}

void TaskDuck::set_max_output_size(int size) {
	this->max_output_size = size;
}

void TaskDuck::set_input_file(const char *filename) {
	this->input_filename = filename;
}

void TaskDuck::set_answer_file(const char *filename) {
	this->answer_filename = filename;
}

void TaskDuck::set_comparator(bool (*cmp)(const char *, int, const char *, int, const char *, int)) {
	this->cmp = cmp;
}

void quit_judge() {
	sys_quit_judge();
}

void TaskDuck::pre_alloc_memory() {
	if (this->memory_allocated) {
		return;
	}
	this->memory_allocated = true;
	
	char *mem_end = ROUNDUP((char *) 0x10000000 + this->mem_kb_hard * 1024, PGSIZE);
	extern int ebss;
	for (char *i = (char *) &ebss; i < mem_end; i += PGSIZE) {
		if (sys_page_alloc(0, i, PTE_P | PTE_U | PTE_W) < 0) {
			// panic("page alloc failed %p\n", i);
			jd_exit();
		}
	}
}