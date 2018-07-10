extern int printf(const char *, ...);
struct FILE;
extern int fflush(struct FILE *);
extern struct FILE *stdout;

void __assert_fail(const char * assertion, const char * file, unsigned int line, const char * function) {
	printf("%s:%u: %sAssertion `%s' failed.\n%n", file, line, function, assertion);
	fflush(stdout);
	asm volatile (
		"int    $0x3 \n"
	);
	while (1);
}
