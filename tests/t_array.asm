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
    sub sp,7
    mov a,bp
    sub a,7
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,6
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_2:
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
    jl _rel_true_5
    mov a,0
    jmp _rel_end_6
_rel_true_5:
    mov a,1
_rel_end_6:
    cmp a,0
    je _for_end_4
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
_for_cont_3:
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
    jmp _for_2
_for_end_4:
    mov a,bp
    sub a,6
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_for_7:
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
    jl _rel_true_10
    mov a,0
    jmp _rel_end_11
_rel_true_10:
    mov a,1
_rel_end_11:
    cmp a,0
    je _for_end_9
    mov a,bp
    sub a,7
    push a
    mov a,bp
    sub a,7
    mov memaddr,a
    mov a,[memaddr+0]
    push a
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
_for_cont_8:
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
    jmp _for_7
_for_end_9:
    mov a,g_g_result
    push a
    mov a,bp
    sub a,7
    mov memaddr,a
    mov a,[memaddr+0]
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,7
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _main_end_1
_main_end_1:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_result:
    #d 0x0000
