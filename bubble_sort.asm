; ============================================================
; このファイルは NC16C コンパイラによって自動生成されました。
; 手で編集する場合は再生成時に上書きされる点に注意してください。
; ============================================================
#include "nc16_assemble_USERPROGRAM.asm"

program_start:
    call main
    userret

; ---- 関数 ----
sort:
    push bp
    mov bp,sp
    sub sp,3
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,3
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,bp
    sub a,1
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_2:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,3
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    sub a,b
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_5
    mov a,0
    jmp _rel_end_6
_rel_true_5:
    mov a,1
_rel_end_6:
    cmp a,0
    je _for_end_4
    mov a,bp
    sub a,2
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_7:
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,3
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    sub a,b
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_10
    mov a,0
    jmp _rel_end_11
_rel_true_10:
    mov a,1
_rel_end_11:
    cmp a,0
    je _for_end_9
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov b,a
    pop a
    add a,b
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_12
    mov a,0
    jmp _rel_end_13
_rel_true_12:
    mov a,1
_rel_end_13:
    cmp a,0
    je _if_end_14
    mov a,bp
    sub a,3
    push a
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov b,a
    pop a
    add a,b
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    sub a,3
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_if_end_14:
_for_cont_8:
    mov a,bp
    sub a,2
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _for_7
_for_end_9:
_for_cont_3:
    mov a,bp
    sub a,1
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _for_2
_for_end_4:
_sort_end_1:
    mov sp,bp
    pop bp
    ret

printArray:
    push bp
    mov bp,sp
    sub sp,17
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,17
    mov memaddr,a
    mov [memaddr+0],memval
_for_16:
    mov a,bp
    sub a,17
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,3
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_19
    mov a,0
    jmp _rel_end_20
_rel_true_19:
    mov a,1
_rel_end_20:
    cmp a,0
    je _for_end_18
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,17
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,16
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,16
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_0
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
_for_cont_17:
    mov a,bp
    sub a,17
    push a
    mov a,bp
    sub a,17
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _for_16
_for_end_18:
    mov a,__str_1
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
_printArray_end_15:
    mov sp,bp
    pop bp
    ret

main:
    push bp
    mov bp,sp
    sub sp,26
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,25
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,__str_2
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_3
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,26
    mov memaddr,a
    mov [memaddr+0],memval
_for_22:
    mov a,bp
    sub a,26
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0008
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_25
    mov a,0
    jmp _rel_end_26
_rel_true_25:
    mov a,1
_rel_end_26:
    cmp a,0
    je _for_end_24
    mov a,__str_4
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,24
    push a
    pop a
    push bp
    mov e,0
    syscall
    pop bp
    mov a,b
    mov a,bp
    sub a,25
    push a
    mov a,bp
    sub a,24
    push bp
    mov e,4
    syscall
    pop bp
    pop d
    mov memaddr,d
    mov memval,b
    mov [memaddr+0],memval
    mov a,c
    mov a,bp
    sub a,8
    push a
    mov a,bp
    sub a,26
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    sub a,25
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_cont_23:
    mov a,bp
    sub a,26
    push a
    mov a,bp
    sub a,26
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _for_22
_for_end_24:
    mov a,__str_5
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,0x0008
    push a
    mov a,bp
    sub a,8
    push a
    call printArray
    add sp,2
    mov a,0x0008
    push a
    mov a,bp
    sub a,8
    push a
    call sort
    add sp,2
    mov a,__str_6
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,0x0008
    push a
    mov a,bp
    sub a,8
    push a
    call printArray
    add sp,2
    mov a,0x0000
    jmp _main_end_21
_main_end_21:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----

; ---- 文字列リテラル ----
__str_0:
    #d " \0"
    #align 16
__str_1:
    #d "\n\0"
    #align 16
__str_2:
    #d "Bubble sort\n\0"
    #align 16
__str_3:
    #d "Sort the given numbers in ascending order.\n\0"
    #align 16
__str_4:
    #d "Input a number.\0"
    #align 16
__str_5:
    #d "Before sorting\n\0"
    #align 16
__str_6:
    #d "After sorting \n\0"
    #align 16
