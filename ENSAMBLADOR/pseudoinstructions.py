import random

def parse_pseudo_instruction(line):
    """Convierte una pseudoinstrucción RISC-V en su equivalente real."""
    
    parts = line.strip().split(maxsplit=1)  # Separa la instrucción del resto
    instr = parts[0].lower()  # Nombre de la instrucción en minúsculas
    operands = parts[1] if len(parts) > 1 else ""  # Obtiene los operandos si existen
    operand_list = operands.split(',') if operands else []  # Lista de operandos

    if instr == "la" and len(operand_list) == 2:
        rd, symbol = operand_list
        return [f"auipc {rd}, {symbol}[31:12]", f"addi {rd}, {rd}, {symbol}[11:0]"]

    elif instr.startswith("l") and instr[1] in "bhdw" and len(operand_list) == 2:
        rd, symbol = operand_list
        return [f"auipc {rd}, {symbol}[31:12]", f"{instr} {rd}, {symbol}[11:0]({rd})"]

    elif instr.startswith("s") and instr[1] in "bhdw" and len(operand_list) == 3:
        rd, symbol, rt = operand_list
        return [f"auipc {rt}, {symbol}[31:12]", f"{instr} {rd}, {symbol}[11:0]({rt})"]

    elif instr == "nop":
        return ["addi x0, x0, 0"]

    elif instr == "li" and len(operand_list) == 2:
        rd, imm = operand_list
        return [f"addi {rd}, zero, {imm}"]

    elif instr == "mv" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"addi {rd}, {rs}, 0"]

    elif instr == "not" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"xori {rd}, {rs}, -1"]

    elif instr == "neg" and len(operand_list) == 2:
        rd, rs = operand_list
        return [f"sub {rd}, x0, {rs}"]

    elif instr == "beqz" and len(operand_list) == 2:
        rs, offset = operand_list
        return [f"beq {rs}, x0, {offset}"]

    elif instr == "bnez" and len(operand_list) == 2:
        rs, offset = operand_list
        return [f"bne {rs}, x0, {offset}"]

    elif instr == "blez" and len(operand_list) == 2:
        rs, offset = operand_list
        return [f"bge x0, {rs}, {offset}"]

    elif instr == "bgez" and len(operand_list) == 2:
        rs, offset = operand_list
        return [f"bge {rs}, x0, {offset}"]

    elif instr == "j" and len(operand_list) == 1:
        return [f"jal x0, {operand_list[0]}"]

    elif instr == "jal" and len(operand_list) == 1:
        return [f"jal x1, {operand_list[0]}"]

    elif instr == "jr" and len(operand_list) == 1:
        return [f"jalr x0, {operand_list[0]}, 0"]

    elif instr == "ret":
        return ["jalr x0, x1, 0"]

    elif instr == "call" and len(operand_list) == 1:
        label = operand_list[0]
        return [random.choice([
            f"auipc x1, {label}[31:12]\njalr x1, x1, {label}[11:0]",
            f"jal x1, {label}"
        ])]

    return [line]  # Devuelve la instrucción original si no es una pseudoinstrucción
