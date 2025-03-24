<<<<<<< Updated upstream
MAIN:                   
    add x1, x2, x3        # Tipo R: Suma x1 = x2 + x3
    sub x4, x5, x6        # Tipo R: Resta x4 = x5 - x6
    and x7, x8, x9        # Tipo R: AND lógico

    addi x10, x1, 10      # Tipo I: Suma inmediata x10 = x1 + 10
    jalr x12, 0(x1)       # Tipo I: Salto a la dirección en x1

    lw x13, 20(x2)        # Tipo I (Load): Carga palabra desde memoria
    sw x14, 24(x3)        # Tipo S: Guarda palabra en memoria

    beq x2, x2, label     # Tipo B: Salto condicional (si x2 == x2, salta a label)
    bne x4, x5, label2    # Tipo B: Salto si x4 != x5

    lui x16, 10000      # Tipo U: Carga inmediato en parte superior
    auipc x17, 20000    # Tipo U: Carga inmediato + PC

    #jal label3              # Tipo J: Salto incondicional (jal sin registrar dirección)
    jal x1, label4        # Tipo J: Salto y guarda retorno en x1

label:                  
                       # No hace nada (para alineación o espera)

label2:
    ecall                 # Llamada al sistema
    ebreak                # Pausa para depuración

label3:
    sb x18, 32(x3)        # Tipo S: Guarda byte en memoria
    sh x19, 36(x4)        # Tipo S: Guarda halfword en memoria

label4:
    slt x20, x21, x22     # Tipo R: x20 = (x21 < x22) ? 1 : 0
=======
square(int):
        addi    sp,sp,-32
        sw      ra,28(sp)
        sw      s0,24(sp)
        addi    s0,sp,32
        sw      a0,-20(s0)
        lw      a5,-20(s0)
        mul     a5,a5,a5
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
        jr      ra
main:
        addi    sp,sp,-32
        sw      ra,28(sp)
        sw      s0,24(sp)
        addi    s0,sp,32
        li      a0,2
        call    square(int)
        sw      a0,-20(s0)
        li      a5,0
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
        jr      ra
>>>>>>> Stashed changes
