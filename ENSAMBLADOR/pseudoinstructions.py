import random

def parse_pseudo_instruction(line):
    """Convierte pseudoinstrucciones RISC-V en sus equivalentes reales."""
    parts = line.strip().split(maxsplit=1)
    instr = parts[0].lower()
    operands = parts[1] if len(parts) > 1 else ""
    operand_list = [op.strip() for op in operands.split(',')] if operands else []

    if instr == "nop":
        return ["addi x0, x0, 0"]

    elif instr == "li" and len(operand_list) == 2:
        rd, imm = operand_list
        try:
            imm = int(imm)
            if -2048 <= imm <= 2047:
                return [f"addi {rd}, x0, {imm}"]
            else:
                upper = (imm >> 12) & 0xFFFFF
                lower = imm & 0xFFF
                return [f"lui {rd}, {upper}", f"addi {rd}, {rd}, {lower}"]
        except ValueError:
            return [f"# Error: Immediate value '{imm}' is not valid"]

    elif instr == "mv" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"addi {rd}, {rs}, 0"]

    elif instr == "not" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"xori {rd}, {rs}, -1"]

    elif instr == "neg" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"sub {rd}, x0, {rs}"]

    elif instr == "negw" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"subw {rd}, x0, {rs}"]

    elif instr == "sext.w" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"addiw {rd}, {rs}, 0"]

    elif instr == "seqz" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"sltiu {rd}, {rs}, 1"]

    elif instr == "snez" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"sltu {rd}, x0, {rs}"]

    elif instr == "sltz" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"slt {rd}, {rs}, x0"]

    elif instr == "sgtz" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"slt {rd}, x0, {rs}"]

    elif instr in ["beqz", "bnez", "blez", "bgez", "bltz", "bgtz"] and len(operand_list) == 2:
        rs, offset = operand_list
        instr_map = {
            "beqz": "beq",
            "bnez": "bne",
            "blez": "bge",
            "bgez": "bge",
            "bltz": "blt",
            "bgtz": "blt"
        }
        
        if instr == "blez":
            return [f"{instr_map[instr]} x0, {rs}, {offset}"]  # bge x0, rs, offset
        elif instr == "bgtz":
            return [f"{instr_map[instr]} x0, {rs}, {offset}"]  # blt x0, rs, offset
        else:
            return [f"{instr_map[instr]} {rs}, x0, {offset}"]  # beq, bne, bge, blt
    
    elif instr in ["bgt", "ble", "bgtu", "bleu"] and len(operand_list) == 3:
        rs, rt, offset = operand_list
        instr_map = {
            "bgt": f"blt {rt}, {rs}, {offset}",   # Si rt < rs, salta (equivalente a rs > rt)
            "ble": f"bge {rt}, {rs}, {offset}",   # Si rt >= rs, salta (equivalente a rs ≤ rt)
            "bgtu": f"bltu {rt}, {rs}, {offset}", # Mismo concepto, pero sin signo
            "bleu": f"bgeu {rt}, {rs}, {offset}"  # Mismo concepto, pero sin signo
        }
        return [instr_map[instr]]
    
    elif instr in ["j", "jal", "jr", "jalr", "ret", "call", "tail"] and len(operand_list) >= 1:
        if instr == "jalr" and len(operand_list) == 3:
            rd, rs1, label = operand_list
            print("LINEAAAA")
            print(f"📌 Procesando instrucción JALR: instr={instr}, rd={rd}, rs1={rs1}, label={label}")
            return [line]  # Devuelve la instrucción tal cual fue escrita

        elif instr == "j":    # Salto incondicional
            offset = operand_list[0]
            return [f"jal x0, {offset}"]  # Permite etiquetas y direcciones
        
        elif instr == "jal":  # Salto y guarda la dirección de retorno
            offset = operand_list[0]
            return [f"jal x1, {offset}"]

        elif instr == "jr":  # Salto a registro (sin guardar retorno)
            rs = operand_list[0]
            return [f"jalr x0, {rs}, 0"]

        elif instr == "jalr":  # Salto a registro (guardando retorno en x1)
            rs = operand_list[0]
            return [f"jalr x1, {rs}, 0"]
        
        elif instr == "ret":  # Retorno de subrutina
            return [
                "auipc x1, offset[31:12]",  # Cargar parte superior del offset
                "jalr x0, x1, 0"  # Return from subroutine
            ]

        elif instr == "call":  # Llamada a subrutina lejana
            offset = operand_list[0]
            return [
                f"auipc x1, %hi({offset})",  # Call far-away subroutine
                f"jalr x1, x1, %lo({offset})"
            ]

        elif instr == "tail":  # Tail call a subrutina lejana
            offset = operand_list[0]
            return [
                f"auipc x6, %hi({offset})",  # Tail call far-away subroutine
                f"jalr x0, x6, %lo({offset})"
            ]

    return [line]
