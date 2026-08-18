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
    sub sp,3
    mov a,bp
    sub a,2
    push a
    mov a,0x0003
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,2
    add a,1
    push a
    mov a,0x0004
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,3
    push a
    mov a,bp
    sub a,2
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
    mov a,bp
    sub a,3
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
    mov a,g_g_result
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0064
    mov b,a
    pop a
    mul a,b
    push a
    mov a,bp
    sub a,2
    add a,1
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
    mov a,g_g_result
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
