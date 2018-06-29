#include <stdio.h>
#include <stdlib.h>

double atof(const char *s) {
	double ret = 0;
	sscanf(s, "%lf", &ret);
	return ret;
}

int atoi(const char *s) {
	int ret = 0;
	sscanf(s, "%d", &ret);
	return ret;
}

long atol(const char *s) {
	long ret = 0;
	sscanf(s, "%ld", &ret);
	return ret;
}

long long atoll(const char *s) {
	long long ret = 0;
	sscanf(s, "%lld", &ret);
	return ret;
}
