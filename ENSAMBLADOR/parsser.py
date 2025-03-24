import re
from encoder import InstructionEncoder

class InstructionParser:
    def __init__(self, instructions_file):
        self.encoder = InstructionEncoder(instructions_file)
    
    def process_line(self, line):
        line = line.split("#")[0].strip()
        if not line:
            return ""
        
        parts = [part.strip() for part in line.split(',')]
        instr_and_rd = parts[0].split()
        instr = instr_and_rd[0]

        if instr in ["ecall", "ebreak"]:
            if len(instr_and_rd) != 1:
                raise ValueError(f"❌ ERROR: Formato inválido en la línea '{line}'.")
            return self.encoder.encode_i_type(instr, "x0", "x0", "0" if instr == "ecall" else "1")

        if instr in ["j", "jal"]:
            if len(instr_and_rd) != 2:
                raise ValueError(f"❌ ERROR: Formato inválido en la línea '{line}'.")
            return self.encoder.encode_j_type("jal", "x0", instr_and_rd[1])

        if len(instr_and_rd) != 2:
            raise ValueError(f"❌ ERROR: Formato inválido en la línea '{line}'.")
        
        instr, rd = instr_and_rd

        if instr == "mv":
            return self.encoder.encode_i_type("addi", rd, parts[1], "0")
        
        if instr == "li":
            imm = int(parts[1])
            if -2048 <= imm <= 2047:
                return self.encoder.encode_i_type("addi", rd, "x0", str(imm))
            else:
                imm_high = (imm >> 12) & 0xFFFFF
                imm_low = imm & 0xFFF
                return self.encoder.encode_u_type("lui", rd, str(imm_high)) + "\n" + self.encoder.encode_i_type("addi", rd, rd, str(imm_low))
        
        if instr == "jr":
            return self.encoder.encode_i_type("jalr", "x0", rd, "0")
        
        if instr == "call":
            label = rd
            return self.encoder.encode_u_type("auipc", "x1", label) + "\n" + self.encoder.encode_i_type("jalr", "x1", "x1", "0")
        
        try:
            if instr in self.encoder.instructions['r_type_instructions']:
                if len(parts) < 3:
                    raise ValueError(f"Formato inválido: {line}")
                return self.encoder.encode_r_type(instr, rd, parts[1], parts[2])

            elif instr in self.encoder.instructions['i_type_instructions']:
                if instr == "jalr":
                    match = re.match(r"(-?\d+)\s*\(\s*(\w+)\s*\)", parts[1])
                    if not match:
                        raise ValueError(f"❌ ERROR: Sintaxis inválida en '{line}'.")
                    return self.encoder.encode_i_type(instr, rd, match.group(2), match.group(1))
                elif len(parts) < 3:
                    raise ValueError(f"Formato inválido: {line}")
                return self.encoder.encode_i_type(instr, rd, parts[1], parts[2])

            elif instr in self.encoder.instructions['i_type_load_instructions']:
                match = re.match(r"(-?\d+)\s*\(\s*(\w+)\s*\)", parts[1])
                if not match:
                    raise ValueError(f"Formato inválido para instrucción de carga: {line}")
                return self.encoder.encode_i_type_load(instr, rd, match.group(2), match.group(1))

            elif instr in self.encoder.instructions['s_type_instructions']:
                match = re.match(r"(-?\d+)\s*\(\s*(\w+)\s*\)", parts[1])
                if not match:
                    raise ValueError(f"Formato inválido para instrucción de almacenamiento: {line}")
                return self.encoder.encode_s_type(instr, match.group(2), rd, match.group(1))

            elif instr in self.encoder.instructions['b_type_instructions']:
                if len(parts) != 3:
                    raise ValueError(f"Formato inválido: {line}")
                return self.encoder.encode_b_type(instr, parts[1], rd, parts[2])

            elif instr in self.encoder.instructions['j_type_instructions']:
                if len(parts) != 2:
                    raise ValueError(f"❌ ERROR: Formato inválido en la línea '{line}'.")
                return self.encoder.encode_j_type(instr, rd, parts[1])

            elif instr in self.encoder.instructions['u_type_instructions']:
                if len(parts) < 2:
                    raise ValueError(f"Formato inválido: {line}")
                return self.encoder.encode_u_type(instr, rd, parts[1])

            else:
                raise ValueError(f"Instrucción desconocida: {instr}")
        
        except Exception as e:
            raise ValueError(f"Error al procesar la línea '{line}': {e}")
