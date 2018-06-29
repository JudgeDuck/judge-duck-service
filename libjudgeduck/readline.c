#include <inc/stdio.h>
#include <inc/error.h>

#define BUFLEN 1024
static char buf[BUFLEN];

char *
jd_readline(const char *prompt)
{
	int i, c, echoing;

#if JOS_KERNEL
	if (prompt != NULL)
		jd_cprintf("%s", prompt);
#else
	if (prompt != NULL)
		jd_fprintf(1, "%s", prompt);
#endif

	i = 0;
	echoing = jd_iscons(0);
	while (1) {
		c = jd_getchar();
		if (c < 0) {
			if (c != -E_EOF)
				jd_cprintf("read error: %e\n", c);
			return NULL;
		} else if ((c == '\b' || c == '\x7f') && i > 0) {
			if (echoing)
				jd_cputchar('\b');
			i--;
		} else if (c >= ' ' && i < BUFLEN-1) {
			if (echoing)
				jd_cputchar(c);
			buf[i++] = c;
		} else if (c == '\n' || c == '\r') {
			if (echoing)
				jd_cputchar('\n');
			buf[i] = 0;
			return buf;
		}
	}
}

