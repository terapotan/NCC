; ============================================================
; このファイルは NC16C コンパイラによって自動生成されました。
; 手で編集する場合は再生成時に上書きされる点に注意してください。
; ============================================================
#include "nc16_assemble_USERPROGRAM.asm"

program_start:
    call main
    userret

; ---- 関数 ----
factorial:
    push bp
    mov bp,sp
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0000
    mov b,a
    pop a
    cmp a,b
    je _rel_true_2
    mov a,0
    jmp _rel_end_3
_rel_true_2:
    mov a,1
_rel_end_3:
    cmp a,0
    je _if_end_4
    mov a,0x0001
    jmp _factorial_end_1
_if_end_4:
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0001
    mov b,a
    pop a
    sub a,b
    push a
    call factorial
    add sp,1
    mov b,a
    pop a
    mul a,b
    jmp _factorial_end_1
_factorial_end_1:
    mov sp,bp
    pop bp
    ret

sum4:
    push bp
    mov bp,sp
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x03e8
    mov b,a
    pop a
    mul a,b
    push a
    mov a,bp
    add a,3
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0064
    mov b,a
    pop a
    mul a,b
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    add a,4
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x000a
    mov b,a
    pop a
    mul a,b
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    add a,5
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    jmp _sum4_end_5
_sum4_end_5:
    mov sp,bp
    pop bp
    ret

main:
    push bp
    mov bp,sp
    sub sp,2
    mov a,g_g_fact
    push a
    mov a,0x0005
    push a
    call factorial
    add sp,1
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_break
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,1
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_7:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x000a
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
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0004
    mov b,a
    pop a
    cmp a,b
    je _rel_true_12
    mov a,0
    jmp _rel_end_13
_rel_true_12:
    mov a,1
_rel_end_13:
    cmp a,0
    je _if_end_14
    jmp _for_end_9
_if_end_14:
    mov a,g_g_break
    push a
    mov a,g_g_break
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
_for_cont_8:
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
    jmp _for_7
_for_end_9:
    mov a,g_g_cont
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,1
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_15:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0005
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_18
    mov a,0
    jmp _rel_end_19
_rel_true_18:
    mov a,1
_rel_end_19:
    cmp a,0
    je _for_end_17
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0002
    mov b,a
    pop a
    cmp a,b
    je _rel_true_20
    mov a,0
    jmp _rel_end_21
_rel_true_20:
    mov a,1
_rel_end_21:
    cmp a,0
    je _if_end_22
    jmp _for_cont_16
_if_end_22:
    mov a,g_g_cont
    push a
    mov a,g_g_cont
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_cont_16:
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
    jmp _for_15
_for_end_17:
    mov a,g_g_cmp
    push a
    mov a,__str_0
    push a
    mov a,__str_0
    push a
    pop b
    pop a
    push bp
    mov e,1
    syscall
    pop bp
    mov a,c
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_multi
    push a
    mov a,0x0004
    push a
    mov a,0x0003
    push a
    mov a,0x0002
    push a
    mov a,0x0001
    push a
    call sum4
    add sp,4
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,2
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,1
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_do_23:
    mov a,bp
    sub a,2
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
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
_do_cont_24:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0004
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_26
    mov a,0
    jmp _rel_end_27
_rel_true_26:
    mov a,1
_rel_end_27:
    cmp a,0
    jne _do_23
_do_end_25:
    mov a,g_g_dowhile
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,0x0000
    jmp _main_end_6
_main_end_6:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_fact:
    #d 0x0000
g_g_break:
    #d 0x0000
g_g_cont:
    #d 0x0000
g_g_cmp:
    #d 0x0000
g_g_multi:
    #d 0x0000
g_g_dowhile:
    #d 0x0000

; ---- 文字列リテラル ----
__str_0:
    #d "abc\0"
    #align 16
