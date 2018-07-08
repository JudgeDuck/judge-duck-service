#include <inc/lib.h>

extern union Fsipc fsipcbuf;

void jd_backup(void *buf) {
	static_assert(sizeof(fsipcbuf) == PGSIZE);
	memcpy(buf, &fsipcbuf, PGSIZE);
	memcpy(buf + PGSIZE, &thisenv, sizeof(thisenv));
	memcpy(buf + PGSIZE + sizeof(thisenv), &binaryname, sizeof(binaryname));
}

void jd_restore(const void *buf) {
	memcpy(&fsipcbuf, buf, PGSIZE);
	memcpy(&thisenv, buf + PGSIZE, sizeof(thisenv));
	memcpy(&binaryname, buf + PGSIZE + sizeof(thisenv), sizeof(binaryname));
}
