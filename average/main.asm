section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    y dd 0, 10, 1, 9, 2, 8, 5
    n dd 7

section .bss
    sum resd 1

section .text
    global _start

_start:
    mov esi, x
    mov edi, y
    xor eax, eax
    xor ebx, ebx

calculate_differences:
    mov ecx, [esi + ebx * 4]
    sub ecx, [edi + ebx * 4]
    add eax, ecx
    inc ebx
    cmp ebx, [n]
    jl calculate_differences

    mov ebx, [n]
    cdq
    idiv ebx
    mov [sum], eax

    mov eax, 60
    xor edi, edi
    syscall
