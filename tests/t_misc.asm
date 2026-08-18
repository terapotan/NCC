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

main:
    push bp
    mov bp,sp
    sub sp,2
    mov a,bp
    sub a,1
    push a
    mov a,0x0535
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,2
    push a
    mov a,0x0004
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_q
    push a
    mov a,bp
    sub a,1
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
    mov a,g_g_r
    push a
    mov a,g_g_q
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
    ja _rel_true_5
    mov a,0
    jmp _rel_end_6
_rel_true_5:
    mov a,1
_rel_end_6:
    cmp a,0
    je _and_false_3
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0004
    mov b,a
    pop a
    cmp a,b
    je _rel_true_7
    mov a,0
    jmp _rel_end_8
_rel_true_7:
    mov a,1
_rel_end_8:
    cmp a,0
    je _and_false_3
    mov a,1
    jmp _and_end_4
_and_false_3:
    mov a,0
_and_end_4:
    cmp a,0
    je _else_9
    mov a,g_g_and
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
    push a
    call add
    add sp,2
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _if_end_10
_else_9:
    mov a,g_g_and
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_if_end_10:
    mov a,g_g_q
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,g_g_buf
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,g_g_buf
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,g_g_q
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _main_end_2
_main_end_2:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_q:
    #d 0x0000
g_g_r:
    #d 0x0000
g_g_and:
    #d 0x0000
g_g_buf:
    #res 16
