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
    sub sp,67
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,33
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,0x0000
    mov memval,a
    mov a,bp
    sub a,67
    mov memaddr,a
    mov [memaddr+0],memval
    mov a,bp
    sub a,33
    push a
    push bp
    mov e,7
    syscall
    pop bp
    push a
    mov a,0x0064
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
    mov a,__str_0
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
_while_2:
    mov a,1
    cmp a,0
    je _while_end_3
    mov a,bp
    sub a,67
    push a
    mov a,bp
    sub a,67
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
    mov a,__str_1
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,32
    push a
    pop a
    push bp
    mov e,0
    syscall
    pop bp
    mov a,b
    mov a,bp
    sub a,66
    push a
    mov a,bp
    sub a,32
    push bp
    mov e,4
    syscall
    pop bp
    pop d
    mov memaddr,d
    mov memval,b
    mov [memaddr+0],memval
    mov a,c
    mov a,bp
    sub a,33
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,66
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    ja _rel_true_4
    mov a,0
    jmp _rel_end_5
_rel_true_4:
    mov a,1
_rel_end_5:
    cmp a,0
    je _else_6
    mov a,__str_2
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    jmp _while_2
    jmp _if_end_7
_else_6:
    mov a,bp
    sub a,33
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,66
    mov memaddr,a
    mov a,[memaddr+0]
    mov b,a
    pop a
    xor a,0x8000
    xor b,0x8000
    cmp a,b
    jl _rel_true_8
    mov a,0
    jmp _rel_end_9
_rel_true_8:
    mov a,1
_rel_end_9:
    cmp a,0
    je _else_10
    mov a,__str_3
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    jmp _while_2
    jmp _if_end_11
_else_10:
    mov a,__str_4
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_5
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,67
    mov memaddr,a
    mov a,[memaddr+0]
    push a
    mov a,bp
    sub a,65
    push a
    pop b
    pop a
    push bp
    mov e,5
    syscall
    pop bp
    mov a,c
    mov a,bp
    sub a,65
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    mov a,__str_6
    push a
    pop b
    push bp
    mov e,3
    syscall
    pop bp
    mov a,c
    jmp _while_end_3
_if_end_11:
_if_end_7:
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
    #d "Number Guessing Game\n\0"
    #align 16
__str_1:
    #d "Please enter a number between 0 and 100.\0"
    #align 16
__str_2:
    #d "The number you entered is smaller than the correct answer.\n\0"
    #align 16
__str_3:
    #d "The number you entered is greater than the correct answer.\n\0"
    #align 16
__str_4:
    #d "That's right!\n\0"
    #align 16
__str_5:
    #d "number of attempts:\0"
    #align 16
__str_6:
    #d "\n\0"
    #align 16
