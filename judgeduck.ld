/* For JudgeDuck */
/* Simple linker script for JOS user-level programs.
   See the GNU ld 'info' manual ("info ld") to learn the syntax. */

OUTPUT_FORMAT("elf32-i386", "elf32-i386", "elf32-i386")
OUTPUT_ARCH(i386)
ENTRY(_start)

SECTIONS
{
	/* Load programs at this address: "." means the current address */
	. = 0x800020;

	.text : {
		*(.text .stub .text.* .gnu.linkonce.t.*)
	}

	PROVIDE(etext = .);	/* Define the 'etext' symbol to this value */

	.rodata : {
		*(.rodata .rodata.* .gnu.linkonce.r.*)
	}
	
	.preinit_array : {
		PROVIDE_HIDDEN(__preinit_array_start = .);
		KEEP (*(SORT(.preinit_array.*)))
		KEEP (*(.preinit_array*))
		PROVIDE_HIDDEN (__preinit_array_end = .);
	}
	
	.init_array : {
		PROVIDE_HIDDEN (__init_array_start = .);
		KEEP (*(SORT(.init_array.*)))
		KEEP (*(.init_array*))
		PROVIDE_HIDDEN (__init_array_end = .);
	}
	
	.fini_array : {
		PROVIDE_HIDDEN (__fini_array_start = .);
		KEEP (*(SORT(.fini_array.*)))
		KEEP (*(.fini_array*))
		PROVIDE_HIDDEN (__fini_array_end = .);
	}

	/* Adjust the address for the data segment to the next page */
	/*. = ALIGN(0x1000);*/
	. = 0x10000000;

	.data : {
		*(.data)
	}

	PROVIDE(edata = .);

	.bss : {
		*(.bss)
	}

	. = ALIGN(0x1000);
	PROVIDE(end = .);
	PROVIDE(ebss = .);


	/* Place debugging symbols so that they can be found by
	 * the kernel debugger.
	 * Specifically, the four words at 0x200000 mark the beginning of
	 * the stabs, the end of the stabs, the beginning of the stabs
	 * string table, and the end of the stabs string table, respectively.
	 */

	.stab_info 0x200000 : {
		LONG(__STAB_BEGIN__);
		LONG(__STAB_END__);
		LONG(__STABSTR_BEGIN__);
		LONG(__STABSTR_END__);
	}

	.stab : {
		__STAB_BEGIN__ = DEFINED(__STAB_BEGIN__) ? __STAB_BEGIN__ : .;
		*(.stab);
		__STAB_END__ = DEFINED(__STAB_END__) ? __STAB_END__ : .;
		BYTE(0)		/* Force the linker to allocate space
				   for this section */
	}

	.stabstr : {
		__STABSTR_BEGIN__ = DEFINED(__STABSTR_BEGIN__) ? __STABSTR_BEGIN__ : .;
		*(.stabstr);
		__STABSTR_END__ = DEFINED(__STABSTR_END__) ? __STABSTR_END__ : .;
		BYTE(0)		/* Force the linker to allocate space
				   for this section */
	}

	/DISCARD/ : {
		*(.eh_frame .note.GNU-stack .comment)
	}
}
