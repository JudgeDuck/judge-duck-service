#include <taskduck.h>
#include <inc/lib.h>

extern "C" {
	extern int main(int, const char **);
}

static void main_wrapper() {
	const char *argv[1] = {"judge-duck-program.exe"};
	main(1, argv);
	sys_quit_judge();
}

void TaskDuck::judge() {
	this->judge_using_wrapper(main_wrapper);
}
