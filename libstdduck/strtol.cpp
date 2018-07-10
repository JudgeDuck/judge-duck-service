#include <stdlib.h>
#include <limits.h>
#include <ctype.h>
#include <math.h>

// Target: i386
// long == int
extern "C" long strtol(const char *s, char **endptr, int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	while (isspace(s[0])) s++;
	bool is_neg = false;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		is_neg = true;
		s++;
	}
	if (base == 16) {
		if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
			s += 2;
		}
	} else if (base == 0) {
		base = 10;
		if (s[0] == '0') {
			if (s[1] == 'x' || s[1] == 'X') {
				base = 16;
				s += 2;
			} else if (s[1] >= '0' && s[1] <= '7') {
				base = 8;
				s += 1;
			} else {
				// Nothing
			}
		}
	}
	long ret = 0;
	bool ok = false;
	while (1) {
		int tmp;
		if (s[0] >= '0' && s[0] <= '9') {
			tmp = s[0] - '0';
		} else if (s[0] >= 'a' && s[0] <= 'z') {
			tmp = s[0] - 'a' + 10;
		} else if (s[0] >= 'A' && s[0] <= 'Z') {
			tmp = s[0] - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		ok = true;
		if (is_neg) {
			if (1LL * ret * base - tmp < LONG_MIN) {
				ret = LONG_MIN;
			} else {
				ret = ret * base - tmp;
			}
		} else {
			if (1LL * ret * base + tmp > LONG_MAX) {
				ret = LONG_MAX;
			} else {
				ret = ret * base + tmp;
			}
		}
		s++;
	}
	if (ok && endptr != NULL) {
		*endptr = (char *) s;
	}
	return ret;
}

extern "C" long long strtoll(const char *s, char **endptr, int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	while (isspace(s[0])) s++;
	bool is_neg = false;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		is_neg = true;
		s++;
	}
	if (base == 16) {
		if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
			s += 2;
		}
	} else if (base == 0) {
		base = 10;
		if (s[0] == '0') {
			if (s[1] == 'x' || s[1] == 'X') {
				base = 16;
				s += 2;
			} else if (s[1] >= '0' && s[1] <= '7') {
				base = 8;
				s += 1;
			} else {
				// Nothing
			}
		}
	}
	long long ret = 0;
	long long lim = is_neg ? LLONG_MIN / base : LLONG_MAX / base;
	bool ok = false;
	while (1) {
		int tmp;
		if (s[0] >= '0' && s[0] <= '9') {
			tmp = s[0] - '0';
		} else if (s[0] >= 'a' && s[0] <= 'z') {
			tmp = s[0] - 'a' + 10;
		} else if (s[0] >= 'A' && s[0] <= 'Z') {
			tmp = s[0] - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		ok = true;
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
		s++;
	}
	if (ok && endptr != NULL) {
		*endptr = (char *) s;
	}
	return ret;
}

extern "C" unsigned long strtoul(const char *s, char **endptr, int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	while (isspace(s[0])) s++;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		return 0;
	}
	if (base == 16) {
		if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
			s += 2;
		}
	} else if (base == 0) {
		base = 10;
		if (s[0] == '0') {
			if (s[1] == 'x' || s[1] == 'X') {
				base = 16;
				s += 2;
			} else if (s[1] >= '0' && s[1] <= '7') {
				base = 8;
				s += 1;
			} else {
				// Nothing
			}
		}
	}
	unsigned long ret = 0;
	bool ok = false;
	while (1) {
		int tmp;
		if (s[0] >= '0' && s[0] <= '9') {
			tmp = s[0] - '0';
		} else if (s[0] >= 'a' && s[0] <= 'z') {
			tmp = s[0] - 'a' + 10;
		} else if (s[0] >= 'A' && s[0] <= 'Z') {
			tmp = s[0] - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		ok = true;
		if (1ull * ret * base + tmp > ULONG_MAX) {
			ret = ULONG_MAX;
		} else {
			ret = ret * base + tmp;
		}
		s++;
	}
	if (ok && endptr != NULL) {
		*endptr = (char *) s;
	}
	return ret;
}

extern "C" unsigned long long strtoull(const char *s, char **endptr, int base) {
	if ((base < 2 || base > 36) && base != 0) {
		return 0;
	}
	while (isspace(s[0])) s++;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		return 0;
	}
	if (base == 16) {
		if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
			s += 2;
		}
	} else if (base == 0) {
		base = 10;
		if (s[0] == '0') {
			if (s[1] == 'x' || s[1] == 'X') {
				base = 16;
				s += 2;
			} else if (s[1] >= '0' && s[1] <= '7') {
				base = 8;
				s += 1;
			} else {
				// Nothing
			}
		}
	}
	unsigned long long ret = 0;
	unsigned long long lim = ULLONG_MAX / base;
	bool ok = false;
	while (1) {
		int tmp;
		if (s[0] >= '0' && s[0] <= '9') {
			tmp = s[0] - '0';
		} else if (s[0] >= 'a' && s[0] <= 'z') {
			tmp = s[0] - 'a' + 10;
		} else if (s[0] >= 'A' && s[0] <= 'Z') {
			tmp = s[0] - 'A' + 10;
		} else {
			break;
		}
		if (tmp >= base) {
			break;
		}
		ok = true;
		if (ret > lim || (ret == lim && ret * base > ULLONG_MAX - tmp)) {
			ret = ULLONG_MAX;
		} else {
			ret = ret * base + tmp;
		}
		s++;
	}
	if (ok && endptr != NULL) {
		*endptr = (char *) s;
	}
	return ret;
}

extern "C" double strtod(const char *s, char **endptr) {
	while (isspace(s[0])) s++;
	bool is_neg = false;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		is_neg = true;
		s++;
	}
	double ret = 0;
	if (tolower(s[0]) == 'i') {
		if (tolower(s[1]) != 'n') return 0;
		if (tolower(s[2]) != 'f') return 0;
		if (endptr) *endptr = (char *) s + 3;
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(s[3]) != 'i') return ret;
		if (tolower(s[4]) != 'n') return ret;
		if (tolower(s[5]) != 'i') return ret;
		if (tolower(s[6]) != 't') return ret;
		if (tolower(s[7]) != 'y') return ret;
		if (endptr) *endptr = (char *) s + 8;
		return ret;
	} else if (tolower(s[0]) == 'n') {
		if (tolower(s[1]) != 'a') return 0;
		if (tolower(s[2]) != 'n') return 0;
		ret = is_neg ? -NAN : NAN;
		s += 3;
		while (isalnum(s[0]) || s[0] == '_') s++;
		if (endptr) *endptr = (char *) s;
		return ret;
	} else if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
		s += 2;
		while (1) {
			int tmp;
			if (s[0] >= '0' && s[0] <= '9') {
				tmp = s[0] - '0';
			} else if (s[0] >= 'a' && s[0] <= 'f') {
				tmp = s[0] - 'a' + 10;
			} else if (s[0] >= 'A' && s[0] <= 'F') {
				tmp = s[0] - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			s++;
		}
		if (s[0] == '.') {
			s++;
			double tmp1 = 1.0;
			while (1) {
				int tmp;
				if (s[0] >= '0' && s[0] <= '9') {
					tmp = s[0] - '0';
				} else if (s[0] >= 'a' && s[0] <= 'f') {
					tmp = s[0] - 'a' + 10;
				} else if (s[0] >= 'A' && s[0] <= 'F') {
					tmp = s[0] - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				s++;
			}
		}
		if (s[0] == 'p' || s[0] == 'P') {
			s++;
			int tmp = strtol(s, endptr, 16);
			ret = ret * pow(16, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (s[0] >= '0' && s[0] <= '9') {
				ret = ret * 10.0 + (s[0] - '0');
				s++;
			} else {
				break;
			}
		}
		if (s[0] == '.') {
			s++;
			double tmp = 1.0;
			while (s[0] >= '0' && s[0] <= '9') {
				tmp = tmp * 0.1;
				ret += tmp * (s[0] - '0');
				s++;
			}
		}
		if (s[0] == 'e' || s[0] == 'E') {
			s++;
			int tmp = strtol(s, endptr, 10);
			ret = ret * pow(10, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	}
}

extern "C" float strtof(const char *s, char **endptr) {
	while (isspace(s[0])) s++;
	bool is_neg = false;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		is_neg = true;
		s++;
	}
	float ret = 0;
	if (tolower(s[0]) == 'i') {
		if (tolower(s[1]) != 'n') return 0;
		if (tolower(s[2]) != 'f') return 0;
		if (endptr) *endptr = (char *) s + 3;
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(s[3]) != 'i') return ret;
		if (tolower(s[4]) != 'n') return ret;
		if (tolower(s[5]) != 'i') return ret;
		if (tolower(s[6]) != 't') return ret;
		if (tolower(s[7]) != 'y') return ret;
		if (endptr) *endptr = (char *) s + 8;
		return ret;
	} else if (tolower(s[0]) == 'n') {
		if (tolower(s[1]) != 'a') return 0;
		if (tolower(s[2]) != 'n') return 0;
		ret = is_neg ? -NAN : NAN;
		s += 3;
		while (isalnum(s[0]) || s[0] == '_') s++;
		if (endptr) *endptr = (char *) s;
		return ret;
	} else if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
		s += 2;
		while (1) {
			int tmp;
			if (s[0] >= '0' && s[0] <= '9') {
				tmp = s[0] - '0';
			} else if (s[0] >= 'a' && s[0] <= 'f') {
				tmp = s[0] - 'a' + 10;
			} else if (s[0] >= 'A' && s[0] <= 'F') {
				tmp = s[0] - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			s++;
		}
		if (s[0] == '.') {
			s++;
			float tmp1 = 1.0;
			while (1) {
				int tmp;
				if (s[0] >= '0' && s[0] <= '9') {
					tmp = s[0] - '0';
				} else if (s[0] >= 'a' && s[0] <= 'f') {
					tmp = s[0] - 'a' + 10;
				} else if (s[0] >= 'A' && s[0] <= 'F') {
					tmp = s[0] - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				s++;
			}
		}
		if (s[0] == 'p' || s[0] == 'P') {
			s++;
			int tmp = strtol(s, endptr, 16);
			ret = ret * powf(16, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (s[0] >= '0' && s[0] <= '9') {
				ret = ret * 10.0 + (s[0] - '0');
				s++;
			} else {
				break;
			}
		}
		if (s[0] == '.') {
			s++;
			float tmp = 1.0;
			while (s[0] >= '0' && s[0] <= '9') {
				tmp = tmp * 0.1;
				ret += tmp * (s[0] - '0');
				s++;
			}
		}
		if (s[0] == 'e' || s[0] == 'E') {
			s++;
			int tmp = strtol(s, endptr, 10);
			ret = ret * powf(10, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	}
}

extern "C" long double strtold(const char *s, char **endptr) {
	while (isspace(s[0])) s++;
	bool is_neg = false;
	if (s[0] == '+') {
		s++;
	} else if (s[0] == '-') {
		is_neg = true;
		s++;
	}
	long double ret = 0;
	if (tolower(s[0]) == 'i') {
		if (tolower(s[1]) != 'n') return 0;
		if (tolower(s[2]) != 'f') return 0;
		if (endptr) *endptr = (char *) s + 3;
		ret = is_neg ? -INFINITY : INFINITY;
		if (tolower(s[3]) != 'i') return ret;
		if (tolower(s[4]) != 'n') return ret;
		if (tolower(s[5]) != 'i') return ret;
		if (tolower(s[6]) != 't') return ret;
		if (tolower(s[7]) != 'y') return ret;
		if (endptr) *endptr = (char *) s + 8;
		return ret;
	} else if (tolower(s[0]) == 'n') {
		if (tolower(s[1]) != 'a') return 0;
		if (tolower(s[2]) != 'n') return 0;
		ret = is_neg ? -NAN : NAN;
		s += 3;
		while (isalnum(s[0]) || s[0] == '_') s++;
		if (endptr) *endptr = (char *) s;
		return ret;
	} else if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
		s += 2;
		while (1) {
			int tmp;
			if (s[0] >= '0' && s[0] <= '9') {
				tmp = s[0] - '0';
			} else if (s[0] >= 'a' && s[0] <= 'f') {
				tmp = s[0] - 'a' + 10;
			} else if (s[0] >= 'A' && s[0] <= 'F') {
				tmp = s[0] - 'A' + 10;
			} else {
				break;
			}
			ret = ret * 10.0 + tmp;
			s++;
		}
		if (s[0] == '.') {
			s++;
			long double tmp1 = 1.0;
			while (1) {
				int tmp;
				if (s[0] >= '0' && s[0] <= '9') {
					tmp = s[0] - '0';
				} else if (s[0] >= 'a' && s[0] <= 'f') {
					tmp = s[0] - 'a' + 10;
				} else if (s[0] >= 'A' && s[0] <= 'F') {
					tmp = s[0] - 'A' + 10;
				} else {
					break;
				}
				tmp1 = tmp1 / 16.0;
				ret += tmp1 * tmp;
				s++;
			}
		}
		if (s[0] == 'p' || s[0] == 'P') {
			s++;
			int tmp = strtol(s, endptr, 16);
			ret = ret * powl(16, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	} else {
		while (1) {
			if (s[0] >= '0' && s[0] <= '9') {
				ret = ret * 10.0 + (s[0] - '0');
				s++;
			} else {
				break;
			}
		}
		if (s[0] == '.') {
			s++;
			long double tmp = 1.0;
			while (s[0] >= '0' && s[0] <= '9') {
				tmp = tmp * 0.1;
				ret += tmp * (s[0] - '0');
				s++;
			}
		}
		if (s[0] == 'e' || s[0] == 'E') {
			s++;
			int tmp = strtol(s, endptr, 10);
			ret = ret * powl(10, tmp);
		} else {
			if (endptr) *endptr = (char *) s;
		}
		return is_neg ? -ret : ret;
	}
}

