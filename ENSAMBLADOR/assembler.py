import os
import sys
from parser import InstructionParser
from pseudoinstructions import parse_pseudo_instruction

def remove_comments(line):
    """Elimina comentarios y espacios en blanco de una línea de código."""
    return line.split('#')[0].strip()

def first_pass(input_file):
    """Primer pase: Construcción de la tabla de etiquetas con sus direcciones."""
    labels = {}
    address_counter = 0

    with open(input_file, 'r') as infile:
        for line in infile:
            line = remove_comments(line)
            if not line:
                continue
            if line.endswith(':'):
                label = line[:-1]
                labels[label] = address_counter
            else:
                address_counter += 4

    print("Diccionario de etiquetas:")
    for label, address in labels.items():
        print(f"{label}: {address}")

    return labels


def process_file(input_file, output_file):
    """Procesa el archivo ensamblador, expande pseudoinstrucciones y convierte a binario."""
    labels = first_pass(input_file)
    parser = InstructionParser('instructions.json')

    branch_instructions = {'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'}

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        address_counter = 0
        for line in infile:
            line = remove_comments(line)
            if not line or line.endswith(':'):  # Ignoramos etiquetas en este pase
                continue

            try:
                expanded_lines = parse_pseudo_instruction(line)
                print(expanded_lines)
                for expanded_line in expanded_lines:
                    parts = expanded_line.split()
                    instr = parts[0].lower()

                    # Si la instrucción es de salto y usa una etiqueta, calcular el offset
                    if instr in branch_instructions and len(parts) > 1:
                        label = parts[-1]
                        if label in labels:
                            offset = (labels[label] - address_counter) // 2  # Offset relativo
                            parts[-1] = str(offset)
                            expanded_line = ' '.join(parts)

                    else:  
                        print(expanded_lines)
                        # Reemplazar etiquetas en instrucciones básicas
                        for label, address in labels.items():
                            expanded_line = expanded_line.replace(label, str(address))

                        if isinstance(expanded_line, list) and len(expanded_line) > 1:
                            for single_line in expanded_line:
                                binary = parser.process_line(single_line)
                                if binary:
                                    outfile.write(binary + "\n")
                        else:
                            binary = parser.process_line(expanded_line)
                            if binary:
                                outfile.write(binary + "\n")



            except ValueError as e:
                outfile.write(f"Error en la línea: {line} - {str(e)}\n")

            address_counter += 4  # Incrementar dirección de instrucción

if __name__ == "__main__":
    input_filename = os.path.join(os.getcwd(), "prog1.asm")
    output_filename = os.path.join(os.getcwd(), "prog1.bin")

    process_file(input_filename, output_filename)
