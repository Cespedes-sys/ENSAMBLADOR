_start:
    # Load constants using basic instructions (no li)
    addi t0, zero, 50    # t0 = S (number to compute sqrt)
    addi t1, zero, 10    # t1 = x (initial guess)
    addi t2, zero, 1     # t2 = tol (tolerance)

newton_raphson:
    # Compute S / x_n using successive subtraction
    add t3, zero, zero   # t3 = quotient (S / x_n)
    add t4, t0, zero     # t4 = copy of S

div_loop:
    blt t4, t1, div_done # If remainder < divisor, stop
    sub t4, t4, t1       # t4 -= x_n
    addi t3, t3, 1       # quotient += 1
    j div_loop
div_done:

    # Compute (x_n + S / x_n)
    add t5, t1, t3       # t5 = x_n + (S / x_n)

    # Compute (x_n + S / x_n) / 2 using shift right
    srli t6, t5, 1       # t6 = (x_n + S / x_n) / 2

    # Compute |x_n+1 - x_n|
    sub t6, t6, t1       # t7 = x_n+1 - x_n
    bge t6, zero, positive_diff
    sub t6, zero, t6     # t7 = -t7 (absolute value)
positive_diff:

    blt t6, t2, done     # If |x_n+1 - x_n| < tol, exit

    # Update x_n = x_n+1 and repeat
    add t1, t6, zero
    j newton_raphson

done:
    # Exit program
    addi a7, zero, 10
    ecall
    