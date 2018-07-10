#ifndef TASKDUCK_H
#define TASKDUCK_H

typedef unsigned size_t;

// Defaults:
// 1s, 256MB, 400MB, 64MB, input.txt, answer.txt, multiline_cmp

// [!] At most ONE instance of TaskDuck can be allocated !!
struct TaskDuck {
	TaskDuck();
	~TaskDuck();
	
	void set_time_limit(long long time_ns);
	void set_memory_limit(int mem_kb);
	void set_memory_hard_limit(int mem_kb);
	void set_max_output_size(int size);
	void set_input_file(const char *filename);
	void set_answer_file(const char *filename);
	void set_comparator(bool (*cmp)(const char *, int, const char *, int, const char *, int));
	// TODO: special judge
	
	void pre_alloc_memory();
	
	void judge();
	void judge_using_wrapper(void (*wrapper)());
	
	void * malloc(size_t size, bool alloc = true);
	
	static bool multiline_cmp(const char *, int, const char *, int, const char *, int);
	
	long long time_ns;
	int mem_kb;
	int mem_kb_hard;
	int max_output_size;
	const char *input_filename;
	const char *answer_filename;
	bool (*cmp)(const char *, int, const char *, int, const char *, int);
	void *malloc_end;
	bool memory_allocated;
	
	char *stdin_content;
	int stdin_size;
	char *stdout_content;
	int stdout_max_size;
	int stdout_size;
	char *answer_content;
	int answer_size;
	
	bool cmp_result;
	const char *message;
	
	char *judge_pages;
};

#endif
