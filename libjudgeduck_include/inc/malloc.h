#ifndef JOS_INC_MALLOC_H
#define JOS_INC_MALLOC_H 1

#ifdef __cplusplus
extern "C" {
#endif

void *jd_malloc(size_t size);
void jd_free(void *addr);

#ifdef __cplusplus
}
#endif

#endif
