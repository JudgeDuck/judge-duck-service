#include <taskduck.h>
#include <inc/lib.h>

TaskDuck::~TaskDuck() {
	const char *message = "Wrong Answer (Tasklib said nothing ...)";
	if (this->cmp) {
		message = this->cmp_result ? "Correct Answer" : "Wrong Answer";
	} else if (this->message) {
		message = this->message;
	}
	int fd = jd_open("arbiter.in", O_RDWR | O_CREAT | O_TRUNC);
	jd_fprintf(fd, "%s\n", message);
	jd_close(fd);
}
