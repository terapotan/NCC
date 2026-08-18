; ============================================================
; このファイルは NC16C コンパイラによって自動生成されました。
; 手で編集する場合は再生成時に上書きされる点に注意してください。
; ============================================================
#include "nc16_assemble_USERPROGRAM.asm"

program_start:
    call main
    userret

; ---- 関数 ----
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
    je _case_0_3
    mov memaddr,sp
    mov a,[memaddr+0]
    cmp a,1
    je _case_1_4
    jmp _default_5
_case_0_3:
    mov a,bp
    sub a,1
    push a
    mov a,0x0064
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_2
_case_1_4:
    mov a,bp
    sub a,1
    push a
    mov a,0x00c8
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_2
_default_5:
    mov a,bp
    sub a,1
    push a
    mov a,0x03e7
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    jmp _switch_end_2
_switch_end_2:
    add sp,1
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _classify_end_1
_classify_end_1:
    mov sp,bp
    pop bp
    ret

main:
    push bp
    mov bp,sp
    sub sp,1
    mov a,bp
    sub a,1
    push a
    mov a,0x0000
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
_while_7:
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0003
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_9
    mov a,0
    jmp _rel_end_10
_rel_true_9:
    mov a,1
_rel_end_10:
    cmp a,0
    je _while_end_8
    mov a,g_g_result
    push a
    mov a,g_g_result
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,1
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
    jmp _while_7
_while_end_8:
    mov a,g_g_result
    mov memaddr,a
    mov a,[memaddr+0]
    jmp _main_end_6
_main_end_6:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_result:
    #d 0x0000
