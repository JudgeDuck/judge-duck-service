#ifndef JOS_INC_STDIO_H
#define JOS_INC_STDIO_H

#include <inc/stdarg.h>

#ifndef NULL
#define NULL	((void *) 0)
#endif /* !NULL */

#ifdef __cplusplus
extern "C" {
#endif

// lib/stdio.c
void	jd_cputchar(int c);
int	jd_getchar(void);
int	jd_iscons(int fd);

// lib/printfmt.c
void	jd_printfmt(void (*putch)(int, void*), void *putdat, const char *fmt, ...);
void	jd_vprintfmt(void (*putch)(int, void*), void *putdat, const char *fmt, va_list);
int	jd_snprintf(char *str, int size, const char *fmt, ...);
int	jd_vsnprintf(char *str, int size, const char *fmt, va_list);

// lib/printf.c
int	jd_cprintf(const char *fmt, ...);
int	jd_vcprintf(const char *fmt, va_list);

// lib/fprintf.c
int	jd_printf(const char *fmt, ...);
int	jd_fprintf(int fd, const char *fmt, ...);
int	jd_vfprintf(int fd, const char *fmt, va_list);

// lib/readline.c
char*	jd_readline(const char *prompt);

#ifdef __cplusplus
}
#endif

#endif /* !JOS_INC_STDIO_H */
