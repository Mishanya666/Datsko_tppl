%macro save_state 0
   push rax          
   push rbx          
   push rcx          
   push rdx        
%endmacro

%macro restore_state 0
   pop rdx           
   pop rcx          
   pop rbx          
   pop rax         
%endmacro

%macro print_string 2
   save_state
   mov rax, 1       
   mov rdi, 1        
   mov rsi, %1     
   mov rdx, %2   
   syscall
   restore_state
%endmacro

%macro debug_print 0
   save_state
   mov rbx, 0        ; Инициализация счетчика цифр
   mov rcx, 10       

divide_loop:
   xor rdx, rdx      ; Очищаем rdx перед делением
   div rcx           

   print_string result, 1 

   push rdx           ; Кладем следующую цифру на стек
   inc rbx            
   cmp rax, 0        
   jne divide_loop    ; Если частное не равно 0, повторяем цикл

print_digits:
   pop rax           
   add rax, '0'       ; Преобразуем в символ ASCII
   mov [result], rax  
   print_string result, 1  

   dec rbx            
   cmp rbx, 0         
   jg print_digits    
   restore_state
%endmacro

section .text
global _start

_start:
    ;Вычисление суммы массива x с использованием XOR и сложения
    xor eax, eax    
    xor ebx, ebx   
sum_x_loop:
    xor edx, edx      ; Очищаем edx перед добавлением, чтобы избежать переполнения
    mov dl, [x + ebx] 
    add al, dl        
    inc ebx           
    cmp ebx, len_x   
    jl sum_x_loop     

    ;Вычисление суммы массива y также как и x
    xor edx, edx      
    xor ebx, ebx      
sum_y_loop:
    xor ecx, ecx   
    mov cl, [y + ebx] 
    add dl, cl     
    inc ebx           
    cmp ebx, len_y    
    jl sum_y_loop     ; Если индекс меньше длины, повторяем цикл

    ;Вычисление разницы между суммами
    cmp al, dl       
    je no_difference  ; Если они равны, разницы нет
    jg x_greater      ; Если sum_x > sum_y, переходим к x_greater

    ; sum_x < sum_y
    mov byte [minus], '-' 
    print_string minus, 1
    sub dl, al            
    mov [diff], dl
    jmp calculate_mean

x_greater:
    sub al, dl            
    mov [diff], al

no_difference:
    mov byte [diff], 0     ; Если суммы равны, разница равна 0

calculate_mean:
    mov ecx, len_x       
    xor ebx, ebx
    mov bl, len_x         
    xor edx, edx
    mov al, [diff]     
    idiv bl               
    mov [mean], al

    mov rax, [mean]
    debug_print           

    print_string newline, nlen  

    mov eax, 1            
    xor ebx, ebx          
    int 0x80        

section .data
    x db 5, 3, 2, 6, 1, 7, 4   ; Массив x
    y db 0, 10, 1, 9, 2, 8, 5  ; Массив y
    len_x equ 7               ; Длина массива x
    len_y equ 7               ; Длина массива y
    sum_x db 0
    sum_y db 0
    diff db 0
    mean db 0

    result dq 0
    newline db 0xA, 0xD     
    nlen equ $ - newline     

section .bss
    minus resb 1             
