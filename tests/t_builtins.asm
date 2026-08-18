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
    mov a,g_g_q
    push a
    mov a,g_g_r
    push a
    mov a,g_g_status
    push a
    mov a,0x0064
    push a
    mov a,0x0007
    push a
    pop b
    pop a
    push bp
    mov e,6
    syscall
    pop bp
    pop a
    pop b
    mov memaddr,b
    mov memval,d
    mov [memaddr+0],memval
    mov memaddr,a
    mov memval,e
    mov [memaddr+0],memval
    mov a,c
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,g_g_ascii_status
    push a
    mov a,g_g_ascii_val
    push a
    mov a,__str_0
    push bp
    mov e,4
    syscall
    pop bp
    pop d
    mov memaddr,d
    mov memval,b
    mov [memaddr+0],memval
    mov a,c
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
g_g_q:
    #d 0x0000
g_g_r:
    #d 0x0000
g_g_status:
    #d 0x0000
g_g_ascii_val:
    #d 0x0000
g_g_ascii_status:
    #d 0x0000
g_g_numstr:
    #res 8

; ---- 文字列リテラル ----
__str_0:
    #d "12345\0"
    #align 16
