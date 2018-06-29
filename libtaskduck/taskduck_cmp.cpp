#include <taskduck.h>
#include <inc/lib.h>

static bool multiline_cmp(const char *A, int n_A, const char *B, int n_B) {
	--A, --B;
	while (n_A && (A[n_A] == '\n' || A[n_A] == ' ')) --n_A;
	while (n_B && (B[n_B] == '\n' || B[n_B] == ' ')) --n_B;
	
	while (1) {
		if (!n_A && !n_B) {
			return true;
		}
		if (!n_A || !n_B) {
			return false;
		}
		if (A[n_A] != B[n_B]) {
			return false;
		}
		if (A[n_A] == '\n') {
			--n_A, --n_B;
			while (n_A && A[n_A] == ' ') --n_A;
			while (n_B && B[n_B] == ' ') --n_B;
		} else {
			--n_A, --n_B;
		}
	}
}

bool TaskDuck::multiline_cmp(const char *I, int n_I, const char *O, int n_O, const char *A, int n_A) {
	return ::multiline_cmp(O, n_O, A, n_A);
}
