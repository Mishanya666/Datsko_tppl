%macro save_regs 0
   push rax
   push rbx
   push rcx
   push rdx
%endmacro

%macro restore_regs 0
   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

%macro write_output 2
   save_regs
   mov rax, 1
   mov rdi, 1
   mov rsi, %1
   mov rdx, %2
   syscall
   restore_regs
%endmacro

%macro print_decimal 0
   save_regs
   mov rbx, 0
   mov rcx, 10
   %%divide_loop:
       xor rdx, rdx
       div rcx
       push rdx
       inc rbx
       cmp rax, 0
       jne %%divide_loop

   %%print_digits:
       pop rax
       add rax, '0'
       mov [temp_char], rax
       write_output temp_char, 1
       dec rbx
       cmp rbx, 0
       jg %%print_digits
   restore_regs
%endmacro

section .text
    global _start

_start:
    mov rax, [number_input]
    shr rax, 1
    mov [first_guess], rax

    mov rax, [number_input]
    mov rbx, [first_guess]
    xor rdx, rdx
    div rbx
    add rax, [first_guess]
    shr rax, 1
    mov [second_guess], rax

calc_sqrt_loop:
    mov rax, [first_guess]
    sub rax, [second_guess]
    cmp rax, 1
    jl calc_done

    mov rax, [second_guess]
    mov [first_guess], rax

    mov rax, [number_input]
    mov rbx, [first_guess]
    xor rdx, rdx
    div rbx
    add rax, [first_guess]
    shr rax, 1
    mov [second_guess], rax

    jmp calc_sqrt_loop

calc_done:
    mov rax, [second_guess]

    print_decimal
    write_output newline, nlen
    write_output message_done, msg_len
    write_output newline, nlen

    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    number_input dq 144
    temp_char db 0
    newline db 0xA, 0xD
    nlen equ $ - newline
    message_done db 'Calculation Complete', 0xA, 0xD
    msg_len equ $ - message_done

section .bss
    first_guess resq 1
    second_guess resq 1
