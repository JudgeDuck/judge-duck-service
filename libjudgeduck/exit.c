
#include <inc/lib.h>

void
jd_exit(void)
{
	jd_close_all();
	sys_env_destroy(0);
}

