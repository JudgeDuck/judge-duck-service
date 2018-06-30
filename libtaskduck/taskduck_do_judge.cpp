#include <taskduck.h>
#include <inc/lib.h>

#undef NULL
#define NULL 0

static void do_judge(TaskDuck *td, void *eip);

void TaskDuck::judge_using_wrapper(void (*wrapper)()) {
	do_judge(this, (void *) wrapper);
}

namespace judgeduck {
	void *malloc_start;
	
	char *stdin_content;
	int stdin_size;
	
	char *stdout_content;
	int stdout_max_size;
	int stdout_size;
}

static void read_file(TaskDuck *td, const char *filename, char *&content, int &size) {
	if (filename == NULL) {
		content = NULL;
		size = 0;
	} else {
		int fd = jd_open(filename, O_RDONLY | O_CREAT);
		struct Stat stat;
		jd_fstat(fd, &stat);
		// jd_cprintf("[libtaskduck] [%s] size = %d\n", filename, stat.st_size);
		content = (char *) td->malloc(stat.st_size);
		size = jd_read(fd, content, stat.st_size);
	}
}

static void init_judgeduck(TaskDuck *td) {
	extern int ebss;
	
	read_file(td, td->input_filename, td->stdin_content, td->stdin_size);
	judgeduck::stdin_content = td->stdin_content;
	judgeduck::stdin_size = td->stdin_size;
	
	td->pre_alloc_memory();
	
	int n_output_pages = ROUNDUP(td->max_output_size, PGSIZE) / PGSIZE;
	td->stdout_content = (char *) &ebss;
	td->stdout_max_size = td->max_output_size;
	judgeduck::stdout_content = td->stdout_content;
	judgeduck::stdout_max_size = td->stdout_max_size;
	judgeduck::stdout_size = 0;
	
	judgeduck::malloc_start = (char *) &ebss + n_output_pages * PGSIZE;
	
	// jd_cprintf("init done\n");
}

//int arr[550 * (1024 / 4) << 10];

static void finish_judgeduck(TaskDuck *td) {
	// jd_cprintf("finish begin\n");
	int size = judgeduck::stdout_size;
	if (size < 0) {
		size = 0;
	} else if (size > td->stdout_max_size) {
		size = td->stdout_max_size;
	}
	td->stdout_size = size;
	
	read_file(td, td->answer_filename, td->answer_content, td->answer_size);
}

static void *real_eip;

extern "C" {
	extern void exit(int);
}

static void judge_wrapper() {
	extern void libstdduck_init();
	extern void libstdduck_fini();
	
	libstdduck_init();
	((void (*)()) real_eip)();
	exit(0);
}

static void do_judge(TaskDuck *td, void *eip) {
	struct JudgeParams prm;
	memset(&prm, 0, sizeof(prm));
	prm.ns = td->time_ns;
	prm.kb = td->mem_kb;
	#ifndef JD_OLD_MEMORY_LIMIT
		prm.esp = (char *) 0x10000000 + td->mem_kb_hard * 1024;
	#else
		prm.kb = td->mem_kb_hard;
	#endif
	prm.syscall_enabled[SYS_quit_judge] = 1;
	
	init_judgeduck(td);
	
	real_eip = eip;
	sys_enter_judge((void *) judge_wrapper, &prm);
	
	finish_judgeduck(td);
	
	if (td->cmp) {
		td->cmp_result = td->cmp(
			td->stdin_content, td->stdin_size,
			td->stdout_content, td->stdout_size,
			td->answer_content, td->answer_size
		);
	}
}
