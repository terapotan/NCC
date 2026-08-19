; ============================================================
; このファイルは NC16C コンパイラによって自動生成されました。
; 手で編集する場合は再生成時に上書きされる点に注意してください。
; ============================================================
#include "nc16_assemble_USERPROGRAM.asm"

program_start:
    call main
    userret

; ---- 関数 ----
main:
    push bp
    mov bp,sp
    sub sp,19
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
    push bp
    mov e,7
    syscall
    pop bp
    push a
    mov a,0x0014
    mov b,a
    pop a
    push bp
    mov e,6
    syscall
    pop bp
    mov a,d
    push a
    mov a,0x0014
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,__str_0
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_1
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,19
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
_while_2:
    mov a,1
    cmp a,0
    je _while_end_3
    mov a,__str_2
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,19
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,19
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
_while_4:
    mov a,1
    cmp a,0
    je _while_end_5
    mov a,__str_4
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,19
    push a
    pop a
    push bp
    mov e,0
    syscall
    pop bp
    mov a,b
    mov a,bp
    sub a,2
    push a
    mov a,bp
    sub a,19
    push bp
    mov e,4
    syscall
    pop bp
    pop d
    mov memaddr,d
    mov memval,b
    mov [memaddr+0],memval
    mov a,c
    mov a,0x0001
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jle _rel_true_8
    mov a,0
    jmp _rel_end_9
_rel_true_8:
    mov a,1
_rel_end_9:
    cmp a,0
    je _and_false_6
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0003
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jle _rel_true_10
    mov a,0
    jmp _rel_end_11
_rel_true_10:
    mov a,1
_rel_end_11:
    cmp a,0
    je _and_false_6
    mov a,1
    jmp _and_end_7
_and_false_6:
    mov a,0
_and_end_7:
    cmp a,0
    jne _not_false_12
    mov a,1
    jmp _not_end_13
_not_false_12:
    mov a,0
_not_end_13:
    cmp a,0
    je _else_14
    mov a,__str_5
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    jmp _while_4
    jmp _if_end_15
_else_14:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_16
    mov a,0
    jmp _rel_end_17
_rel_true_16:
    mov a,1
_rel_end_17:
    cmp a,0
    je _if_end_18
    mov a,__str_6
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    jmp _while_4
_if_end_18:
_if_end_15:
    jmp _while_end_5
    jmp _while_4
_while_end_5:
    mov a,bp
    sub a,1
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    sub a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0000
    mov b,a
    pop a
    cmp a,b
    je _rel_true_19
    mov a,0
    jmp _rel_end_20
_rel_true_19:
    mov a,1
_rel_end_20:
    cmp a,0
    je _if_end_21
    mov a,__str_7
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,0x0000
    jmp _main_end_1
_if_end_21:
    mov a,bp
    sub a,3
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    sub a,b
    push a
    mov a,0x0004
    mov b,a
    pop a
    push bp
    mov e,6
    syscall
    pop bp
    mov a,d
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,3
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0000
    mov b,a
    pop a
    cmp a,b
    je _rel_true_22
    mov a,0
    jmp _rel_end_23
_rel_true_22:
    mov a,1
_rel_end_23:
    cmp a,0
    je _if_end_24
    mov a,bp
    sub a,3
    push a
    push bp
    mov e,7
    syscall
    pop bp
    push a
    mov a,0x0002
    mov b,a
    pop a
    push bp
    mov e,6
    syscall
    pop bp
    mov a,d
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
_if_end_24:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,3
    mov memaddr,a
    mov a,[memaddr+0]
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
    je _if_end_27
    mov a,bp
    sub a,3
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_if_end_27:
    mov a,bp
    sub a,1
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,3
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    sub a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,__str_8
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,3
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,19
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,19
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_9
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0000
    mov b,a
    pop a
    cmp a,b
    je _rel_true_28
    mov a,0
    jmp _rel_end_29
_rel_true_28:
    mov a,1
_rel_end_29:
    cmp a,0
    je _if_end_30
    mov a,__str_10
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,0x0000
    jmp _main_end_1
_if_end_30:
    jmp _while_2
_while_end_3:
_main_end_1:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----

; ---- 文字列リテラル ----
__str_0:
    #d "picking-stone game\n\0"
    #align 16
__str_1:
    #d "The player and the computer take turns taking 1 to 3 stones each, and the player who takes the last stone loses.\n\0"
    #align 16
__str_2:
    #d "Number of stones:\0"
    #align 16
__str_3:
    #d "\n\0"
    #align 16
__str_4:
    #d "How many stones would you like to take? Please enter a number between 1 and 3.\0"
    #align 16
__str_5:
    #d "Please enter a value between 1 and 3.\n\0"
    #align 16
__str_6:
    #d "You cannot take more stones than the current number of stones.\n\0"
    #align 16
__str_7:
    #d "The CPU wins!\n\0"
    #align 16
__str_8:
    #d "The CPU takes \0"
    #align 16
__str_9:
    #d " stones.\n\0"
    #align 16
__str_10:
    #d "The Player wins!\n\0"
    #align 16
