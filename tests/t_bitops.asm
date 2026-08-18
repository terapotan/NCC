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
    sub sp,2
    mov a,bp
    sub a,1
    push a
    mov a,0x00f0
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_and
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x0ff0
    mov b,a
    pop a
    and a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_or
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0x000f
    mov b,a
    pop a
    or a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_xor
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,0xffff
    mov b,a
    pop a
    xor a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_not
    push a
    mov a,bp
    sub a,1
    mov memaddr,a
    mov a,[memaddr+0]
    not a
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_shl
    push a
    mov a,0x0001
    push a
    mov a,0x0008
    mov b,a
    pop a
_shl_2:
    cmp b,0
    je _shl_end_3
    add a,a
    sub b,1
    jmp _shl_2
_shl_end_3:
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_shr
    push a
    mov a,0x8000
    push a
    mov a,0x0004
    mov b,a
    pop a
    shr a,b
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,2
    push a
    mov a,0x0003
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_shl_var
    push a
    mov a,0x0001
    push a
    mov a,bp
    sub a,2
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
_shl_4:
    cmp b,0
    je _shl_end_5
    add a,a
    sub b,1
    jmp _shl_4
_shl_end_5:
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,0x0000
    jmp _main_end_1
_main_end_1:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----
g_g_and:
    #d 0x0000
g_g_or:
    #d 0x0000
g_g_xor:
    #d 0x0000
g_g_not:
    #d 0x0000
g_g_shl:
    #d 0x0000
g_g_shr:
    #d 0x0000
g_g_shl_var:
    #d 0x0000
