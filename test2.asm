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
    sub sp,17
_while_2:
    mov a,1
    cmp a,0
    je _while_end_3
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,17
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,bp
    sub a,17
    push a
    push bp
    mov e,7
    syscall
    pop bp
    mov memval,a
    pop a
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,memval
    mov a,bp
    sub a,17
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
    jmp _while_2
_while_end_3:
    mov a,0x0000
    jmp _main_end_1
_main_end_1:
    mov sp,bp
    pop bp
    ret


; ---- グローバル変数 ----

; ---- 文字列リテラル ----
__str_0:
    #d "\n\0"
    #align 16
