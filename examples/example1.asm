; ============================================================
; このファイルは NC16C コンパイラによって自動生成されました。
; 手で編集する場合は再生成時に上書きされる点に注意してください。
; ============================================================
#include "nc16_assemble_USERPROGRAM.asm"

program_start:
    call main
    userret

; ---- 関数 ----
add:
    push bp
    mov bp,sp
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,3
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    jmp _add_end_1
_add_end_1:
    mov sp,bp
    pop bp
    ret

sum_array:
    push bp
    mov bp,sp
    sub sp,2
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
_for_3:
    mov a,bp
    sub a,1
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
    jl _rel_true_6
    mov a,0
    jmp _rel_end_7
_rel_true_6:
    mov a,1
_rel_end_7:
    cmp a,0
    je _for_end_5
    mov a,bp
    sub a,2
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    add a,2
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
_for_cont_4:
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
    jmp _for_3
_for_end_5:
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _sum_array_end_2
_sum_array_end_2:
    mov sp,bp
    pop bp
    ret

classify:
    push bp
    mov bp,sp
    sub sp,1
    mov a,bp
    add a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov memaddr,sp
    mov a,[memaddr+0]
    cmp a,0
    je _case_0_10
    mov memaddr,sp
    mov a,[memaddr+0]
    cmp a,1
    je _case_1_11
    jmp _default_12
_case_0_10:
    mov a,bp
    sub a,1
    push a
    mov a,0x0064
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_9
_case_1_11:
    mov a,bp
    sub a,1
    push a
    mov a,0x00c8
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_9
_default_12:
    mov a,bp
    sub a,1
    push a
    mov a,0x03e7
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_9
_switch_end_9:
    add sp,1
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _classify_end_8
_classify_end_8:
    mov sp,bp
    pop bp
    ret

main:
    push bp
    mov bp,sp
    sub sp,12
    mov a,bp
    sub a,6
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_14:
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0005
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_17
    mov a,0
    jmp _rel_end_18
_rel_true_17:
    mov a,1
_rel_end_18:
    cmp a,0
    je _for_end_16
    mov a,bp
    sub a,5
    push a
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    add a,b
    push a
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    mul a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_cont_15:
    mov a,bp
    sub a,6
    push a
    mov a,bp
    sub a,6
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
    jmp _for_14
_for_end_16:
    mov a,bp
    sub a,10
    push a
    mov a,0x0005
    push a
    mov a,bp
    sub a,5
    push a
    call sum_array
    add sp,2
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,8
    push a
    mov a,0x0003
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,8
    add a,1
    push a
    mov a,0x0004
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,9
    push a
    mov a,bp
    sub a,8
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,9
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,9
    mov memaddr,a
    mov a,[memaddr+0]
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
    mov a,bp
    sub a,10
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x000a
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    ja _rel_true_21
    mov a,0
    jmp _rel_end_22
_rel_true_21:
    mov a,1
_rel_end_22:
    cmp a,0
    je _and_false_19
    mov a,bp
    sub a,8
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0004
    mov b,a
    pop a
    cmp a,b
    je _rel_true_23
    mov a,0
    jmp _rel_end_24
_rel_true_23:
    mov a,1
_rel_end_24:
    cmp a,0
    je _and_false_19
    mov a,1
    jmp _and_end_20
_and_false_19:
    mov a,0
_and_end_20:
    cmp a,0
    je _else_25
    mov a,g_g_total
    push a
    mov a,bp
    sub a,8
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,10
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    call add
    add sp,2
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _if_end_26
_else_25:
    mov a,g_g_total
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_if_end_26:
    mov a,bp
    sub a,6
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_while_27:
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0003
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_29
    mov a,0
    jmp _rel_end_30
_rel_true_29:
    mov a,1
_rel_end_30:
    cmp a,0
    je _while_end_28
    mov a,g_g_total
    push a
    mov a,g_g_total
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,6
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    call classify
    add sp,1
    mov b,a
    pop a
    add a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,6
    push a
    mov a,bp
    sub a,6
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
    jmp _while_27
_while_end_28:
    mov a,g_g_total
    push a
    mov a,g_g_total
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0007
    mov b,a
    pop a
    push bp
    mov e,6
    syscall
    pop bp
    mov a,c
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,11
    push a
    mov a,g_g_total
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0003
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
    mov a,g_g_total
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,g_g_msgbuf
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,g_g_msgbuf
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,g_g_total
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _main_end_13
_main_end_13:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_total:
    #d 0x0000
g_g_msgbuf:
    #res 16
