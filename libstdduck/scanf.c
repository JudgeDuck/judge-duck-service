#include <stdarg.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

#define EOF (-1)
struct FILE;
extern struct FILE *stdin, *stdout;
extern int getchar();
extern int vprintf(const char *fmt, va_list args);

static int my_scanf(int (*getchar)(), int (*peek)(), const char *fmt, va_list args);
static int my_getchar();
static int my_peek();
static const char *my_getchar_source;

extern int _stdduck_peek();

int fprintf(struct FILE *f, const char *fmt, ...) {
	if (f != stdout) {
		return EOF;
	}
	va_list args;
	va_start(args, fmt);
	int ret = vprintf(fmt, args);
	va_end(args);
	return ret;
}

int vfprintf(struct FILE *f, const char *fmt, va_list args) {
	if (f != stdout) {
		return EOF;
	}
	return vprintf(fmt, args);
}

int vscanf(const char *fmt, va_list args) {
	return my_scanf(getchar, _stdduck_peek, fmt, args);
}

int vsscanf(const char *s, const char *fmt, va_list args) {
	my_getchar_source = s;
	return my_scanf(my_getchar, my_peek, fmt, args);
}

int vfscanf(struct FILE *f, const char *fmt, va_list args) {
	if (f != stdin) {
		return EOF;
	}
	return my_scanf(getchar, _stdduck_peek, fmt, args);
}

int scanf(const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	int ret = vscanf(fmt, args);
	va_end(args);
	return ret;
}

int sscanf(const char *s, const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	int ret = vsscanf(s, fmt, args);
	va_end(args);
	return ret;
}

int fscanf(struct FILE *f, const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	int ret = vfscanf(f, fmt, args);
	va_end(args);
	return ret;
}

static int my_getchar() {
	char c = *my_getchar_source;
	if (c != 0) {
		my_getchar_source++;
		return c;
	} else {
		return EOF;
	}
}

static int my_peek() {
	char c = *my_getchar_source;
	if (c != 0) {
		return c;
	} else {
		return EOF;
	}
}

static int my_strtoi(int (*get)(), int (*peek)(), int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	char c;
	while (isspace(peek())) get();
	int is_neg = 0;
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		is_neg = 1;
		get();
	}
	if (base == 16) {
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				get();
			} else {
				return 0;
			}
		}
	} else if (base == 0) {
		base = 10;
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				base = 16;
				get();
			} else if (peek() >= '0' && peek() <= '7') {
				base = 8;
			}
		}
	}
	int ret = 0;
	int lim = is_neg ? INT_MIN / base : INT_MAX / base;
	while (1) {
		c = peek();
		int tmp;
		if (c >= '0' && c <= '9') {
			tmp = c - '0';
		} else if (c >= 'a' && c <= 'z') {
			tmp = c - 'a' + 10;
		} else if (c >= 'A' && c <= 'Z') {
			tmp = c - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		if (is_neg) {
			if (ret < lim || (ret == lim && ret * base < INT_MIN + tmp)) {
				ret = INT_MIN;
			} else {
				ret = ret * base - tmp;
			}
		} else {
			if (ret > lim || (ret == lim && ret * base > INT_MAX - tmp)) {
				ret = INT_MAX;
			} else {
				ret = ret * base + tmp;
			}
		}
		get();
	}
	return ret;
}

static long my_strtol(int (*get)(), int (*peek)(), int base) {
	return my_strtoi(get, peek, base);
}

static long long my_strtoll(int (*get)(), int (*peek)(), int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	char c;
	while (isspace(peek())) get();
	int is_neg = 0;
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		is_neg = 1;
		get();
	}
	if (base == 16) {
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				get();
			} else {
				return 0;
			}
		}
	} else if (base == 0) {
		base = 10;
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				base = 16;
				get();
			} else if (peek() >= '0' && peek() <= '7') {
				base = 8;
			}
		}
	}
	long long ret = 0;
	long long lim = is_neg ? LLONG_MIN / base : LLONG_MAX / base;
	while (1) {
		c = peek();
		int tmp;
		if (c >= '0' && c <= '9') {
			tmp = c - '0';
		} else if (c >= 'a' && c <= 'z') {
			tmp = c - 'a' + 10;
		} else if (c >= 'A' && c <= 'Z') {
			tmp = c - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		if (is_neg) {
			if (ret < lim || (ret == lim && ret * base < LLONG_MIN + tmp)) {
				ret = LLONG_MIN;
			} else {
				ret = ret * base - tmp;
			}
		} else {
			if (ret > lim || (ret == lim && ret * base > LLONG_MAX - tmp)) {
				ret = LLONG_MAX;
			} else {
				ret = ret * base + tmp;
			}
		}
		get();
	}
	return ret;
}

static unsigned my_strtou(int (*get)(), int (*peek)(), int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	char c;
	while (isspace(peek())) get();
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		return 0;
	}
	if (base == 16) {
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				get();
			} else {
				return 0;
			}
		}
	} else if (base == 0) {
		base = 10;
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				base = 16;
				get();
			} else if (peek() >= '0' && peek() <= '7') {
				base = 8;
			}
		}
	}
	unsigned ret = 0;
	unsigned lim = UINT_MAX / base;
	while (1) {
		c = peek();
		int tmp;
		if (c >= '0' && c <= '9') {
			tmp = c - '0';
		} else if (c >= 'a' && c <= 'z') {
			tmp = c - 'a' + 10;
		} else if (c >= 'A' && c <= 'Z') {
			tmp = c - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		if (ret > lim || (ret == lim && ret * base > UINT_MAX - tmp)) {
			ret = UINT_MAX;
		} else {
			ret = ret * base + tmp;
		}
		get();
	}
	return ret;
}

static unsigned long my_strtoul(int (*get)(), int (*peek)(), int base) {
	return my_strtou(get, peek, base);
}

static unsigned long long my_strtoull(int (*get)(), int (*peek)(), int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	char c;
	while (isspace(peek())) get();
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		return 0;
	}
	if (base == 16) {
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				get();
			} else {
				return 0;
			}
		}
	} else if (base == 0) {
		base = 10;
		if (peek() == '0') {
			get();
			if (tolower(peek()) == 'x') {
				base = 16;
				get();
			} else if (peek() >= '0' && peek() <= '7') {
				base = 8;
			}
		}
	}
	unsigned long long ret = 0;
	unsigned long long lim = ULLONG_MAX / base;
	while (1) {
		c = peek();
		int tmp;
		if (c >= '0' && c <= '9') {
			tmp = c - '0';
		} else if (c >= 'a' && c <= 'z') {
			tmp = c - 'a' + 10;
		} else if (c >= 'A' && c <= 'Z') {
			tmp = c - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		if (ret > lim || (ret == lim && ret * base > ULLONG_MAX - tmp)) {
			ret = ULLONG_MAX;
		} else {
			ret = ret * base + tmp;
		}
		get();
	}
	return ret;
}

static double my_strtod(int (*get)(), int (*peek)()) {
	while (isspace(peek())) get();
	int is_neg = 0;
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		is_neg = 1;
		get();
	}
	double ret = 0;
	if (tolower(peek()) == 'i') {
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		if (tolower(peek()) != 'f') return 0;
		get();
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 'n') return ret;
		get();
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 't') return ret;
		get();
		if (tolower(peek()) != 'y') return ret;
		get();
		return ret;
	} else if (tolower(peek()) == 'n') {
		get();
		if (tolower(peek()) != 'a') return 0;
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		ret = is_neg ? -NAN : NAN;
		while (isalnum(peek()) || peek() == '_') get();
		return ret;
	} else if (peek() == '0') {
		get();
		if (tolower(peek()) != 'x') {
			return 0;
		}
		while (1) {
			int tmp;
			char c = peek();
			if (c >= '0' && c <= '9') {
				tmp = c - '0';
			} else if (c >= 'a' && c <= 'f') {
				tmp = c - 'a' + 10;
			} else if (c >= 'A' && c <= 'F') {
				tmp = c - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			get();
		}
		if (peek() == '.') {
			get();
			double tmp1 = 1.0;
			while (1) {
				int tmp;
				char c = peek();
				if (c >= '0' && c <= '9') {
					tmp = c - '0';
				} else if (c >= 'a' && c <= 'f') {
					tmp = c - 'a' + 10;
				} else if (c >= 'A' && c <= 'F') {
					tmp = c - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				get();
			}
		}
		if (tolower(peek()) == 'p') {
			get();
			int tmp = my_strtol(get, peek, 16);
			ret = ret * pow(16, tmp);
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (isdigit(peek())) {
				ret = ret * 10.0 + (peek() - '0');
				get();
			} else {
				break;
			}
		}
		if (peek() == '.') {
			get();
			double tmp = 1.0;
			while (isdigit(peek())) {
				tmp = tmp * 0.1;
				ret += tmp * (peek() - '0');
				get();
			}
		}
		if (tolower(peek()) == 'e') {
			get();
			int tmp = my_strtol(get, peek, 10);
			ret = ret * pow(10, tmp);
		}
		return is_neg ? -ret : ret;
	}
}

static float my_strtof(int (*get)(), int (*peek)()) {
	while (isspace(peek())) get();
	int is_neg = 0;
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		is_neg = 1;
		get();
	}
	float ret = 0;
	if (tolower(peek()) == 'i') {
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		if (tolower(peek()) != 'f') return 0;
		get();
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 'n') return ret;
		get();
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 't') return ret;
		get();
		if (tolower(peek()) != 'y') return ret;
		get();
		return ret;
	} else if (tolower(peek()) == 'n') {
		get();
		if (tolower(peek()) != 'a') return 0;
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		ret = is_neg ? -NAN : NAN;
		while (isalnum(peek()) || peek() == '_') get();
		return ret;
	} else if (peek() == '0') {
		get();
		if (tolower(peek()) != 'x') {
			return 0;
		}
		while (1) {
			int tmp;
			char c = peek();
			if (c >= '0' && c <= '9') {
				tmp = c - '0';
			} else if (c >= 'a' && c <= 'f') {
				tmp = c - 'a' + 10;
			} else if (c >= 'A' && c <= 'F') {
				tmp = c - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			get();
		}
		if (peek() == '.') {
			get();
			double tmp1 = 1.0;
			while (1) {
				int tmp;
				char c = peek();
				if (c >= '0' && c <= '9') {
					tmp = c - '0';
				} else if (c >= 'a' && c <= 'f') {
					tmp = c - 'a' + 10;
				} else if (c >= 'A' && c <= 'F') {
					tmp = c - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				get();
			}
		}
		if (tolower(peek()) == 'p') {
			get();
			int tmp = my_strtol(get, peek, 16);
			ret = ret * powf(16, tmp);
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (isdigit(peek())) {
				ret = ret * 10.0 + (peek() - '0');
				get();
			} else {
				break;
			}
		}
		if (peek() == '.') {
			get();
			double tmp = 1.0;
			while (isdigit(peek())) {
				tmp = tmp * 0.1;
				ret += tmp * (peek() - '0');
				get();
			}
		}
		if (tolower(peek()) == 'e') {
			get();
			int tmp = my_strtol(get, peek, 10);
			ret = ret * powf(10, tmp);
		}
		return is_neg ? -ret : ret;
	}
}

static long double my_strtold(int (*get)(), int (*peek)()) {
	while (isspace(peek())) get();
	int is_neg = 0;
	if (peek() == '+') {
		get();
	} else if (peek() == '-') {
		is_neg = 1;
		get();
	}
	long double ret = 0;
	if (tolower(peek()) == 'i') {
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		if (tolower(peek()) != 'f') return 0;
		get();
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 'n') return ret;
		get();
		if (tolower(peek()) != 'i') return ret;
		get();
		if (tolower(peek()) != 't') return ret;
		get();
		if (tolower(peek()) != 'y') return ret;
		get();
		return ret;
	} else if (tolower(peek()) == 'n') {
		get();
		if (tolower(peek()) != 'a') return 0;
		get();
		if (tolower(peek()) != 'n') return 0;
		get();
		ret = is_neg ? -NAN : NAN;
		while (isalnum(peek()) || peek() == '_') get();
		return ret;
	} else if (peek() == '0') {
		get();
		if (tolower(peek()) != 'x') {
			return 0;
		}
		while (1) {
			int tmp;
			char c = peek();
			if (c >= '0' && c <= '9') {
				tmp = c - '0';
			} else if (c >= 'a' && c <= 'f') {
				tmp = c - 'a' + 10;
			} else if (c >= 'A' && c <= 'F') {
				tmp = c - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			get();
		}
		if (peek() == '.') {
			get();
			double tmp1 = 1.0;
			while (1) {
				int tmp;
				char c = peek();
				if (c >= '0' && c <= '9') {
					tmp = c - '0';
				} else if (c >= 'a' && c <= 'f') {
					tmp = c - 'a' + 10;
				} else if (c >= 'A' && c <= 'F') {
					tmp = c - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				get();
			}
		}
		if (tolower(peek()) == 'p') {
			get();
			int tmp = my_strtol(get, peek, 16);
			ret = ret * powl(16, tmp);
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (isdigit(peek())) {
				ret = ret * 10.0 + (peek() - '0');
				get();
			} else {
				break;
			}
		}
		if (peek() == '.') {
			get();
			double tmp = 1.0;
			while (isdigit(peek())) {
				tmp = tmp * 0.1;
				ret += tmp * (peek() - '0');
				get();
			}
		}
		if (tolower(peek()) == 'e') {
			get();
			int tmp = my_strtol(get, peek, 10);
			ret = ret * powl(10, tmp);
		}
		return is_neg ? -ret : ret;
	}
}

static void my_get_string(int (*get)(), int (*peek)(), char *s) {
	while (isspace(peek())) get();
	while (!isspace(peek())) *(s++) = get();
	*s = 0;
}


static int my_scanf(int (*get)(), int (*peek)(), const char *fmt, va_list args) {
	int ret = 0;
	int has_error = 0;
	while (*fmt) {
		if (isspace(*fmt)) {
			while (isspace(peek())) {
				get();
			}
		} else if (*fmt != '%') {
			if (peek() != *fmt) {
				has_error = 1;
				break;
			} else {
				get();
			}
		} else {
			fmt++;
			// TODO: support '*'
			// TODO: support width
			if (fmt[0] == 'l') {
				if (fmt[1] == 'l') {
					fmt += 2;
					if (fmt[0] == 'd') {
						va_arg(args, long long *)[0] = my_strtoll(get, peek, 10);
					} else if (fmt[0] == 'i') {
						va_arg(args, long long *)[0] = my_strtoll(get, peek, 0);
					} else if (fmt[0] == 'u') {
						va_arg(args, unsigned long long *)[0] = my_strtoull(get, peek, 10);
					} else if (fmt[0] == 'o') {
						va_arg(args, unsigned long long *)[0] = my_strtoull(get, peek, 8);
					} else if (fmt[0] == 'x') {
						va_arg(args, unsigned long long *)[0] = my_strtoull(get, peek, 16);
					} else {
						has_error = 1;
						break;
					}
					fmt++;
				} else {
					fmt += 1;
					if (fmt[0] == 'd') {
						va_arg(args, long *)[0] = my_strtol(get, peek, 10);
					} else if (fmt[0] == 'i') {
						va_arg(args, long *)[0] = my_strtol(get, peek, 0);
					} else if (fmt[0] == 'u') {
						va_arg(args, unsigned long *)[0] = my_strtoul(get, peek, 10);
					} else if (fmt[0] == 'o') {
						va_arg(args, unsigned long *)[0] = my_strtoul(get, peek, 8);
					} else if (fmt[0] == 'x') {
						va_arg(args, unsigned long *)[0] = my_strtoul(get, peek, 16);
					} else if (fmt[0] == 'f') {
						va_arg(args, double *)[0] = my_strtod(get, peek);
					} else {
						has_error = 1;
						break;
					}
					fmt++;
				}
			} else if (fmt[0] == 'L') {
				if (fmt[1] == 'f') {
					fmt += 2;
					va_arg(args, long double *)[0] = my_strtold(get, peek);
					fmt++;
				} else {
					has_error = 1;
					break;
				}
			} else {
				if (fmt[0] == 'd') {
					va_arg(args, int *)[0] = my_strtoi(get, peek, 10);
				} else if (fmt[0] == 'i') {
					va_arg(args, int *)[0] = my_strtoi(get, peek, 0);
				} else if (fmt[0] == 'u') {
					va_arg(args, unsigned *)[0] = my_strtou(get, peek, 10);
				} else if (fmt[0] == 'o') {
					va_arg(args, unsigned *)[0] = my_strtou(get, peek, 8);
				} else if (fmt[0] == 'x') {
					va_arg(args, unsigned *)[0] = my_strtou(get, peek, 16);
				} else if (fmt[0] == 'f') {
					va_arg(args, float *)[0] = my_strtof(get, peek);
				} else if (fmt[0] == 's') {
					my_get_string(get, peek, va_arg(args, char *));
				} else if (fmt[0] == '%') {
					if (peek() != '%') {
						has_error = 1;
						break;
					} else {
						get();
						--ret;
					}
				} else {
					has_error = 1;
					break;
				}
				fmt++;
			}
			ret++;
		}
	}
	return ret;
}
