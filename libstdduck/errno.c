// Non-thread-safe
int * __errno_location (void) {
	static int errno;
	return &errno;
}
