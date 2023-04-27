import argparse
from pathlib import Path
from typing import Dict
import re

VARIABLE_OFFSET = 16
PREDEFINED_SYMBOLS = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
    }



C_INSTRUCTION_COMP = {
    "0": int("0b101010", 2),
    "1": int("0b111111", 2),
    "-1": int("0b111010", 2),
    "D": int("0b001100", 2),
    "A": int("0b110000", 2),
    "M": int("0b110000", 2),
    "!D": int("0b001101", 2),
    "!A": int("0b110001", 2),
    "!M": int("0b110001", 2),
    "-D": int("0b001111", 2),
    "-A": int("0b110011", 2),
    "-M": int("0b110011", 2),
    "D+1": int("0b011111", 2),
    "A+1": int("0b110111", 2),
    "M+1": int("0b110111", 2),
    "D-1": int("0b001110", 2),
    "A-1": int("0b110010", 2),
    "M-1": int("0b110010", 2),
    "D+A": int("0b000010", 2),
    "D+M": int("0b000010", 2),
    "D-A": int("0b010011", 2),
    "D-M": int("0b010011", 2),
    "A-D": int("0b000111", 2),
    "M-D": int("0b000111", 2),
    "D&A": int("0b000000", 2),
    "D&M": int("0b000000", 2),
    "D|A": int("0b010101", 2),
    "D|M": int("0b010101", 2),
}


C_INSTRUCTION_DEST = {
    "": int("0b000", 2),
    "M": int("0b001", 2),
    "D": int("0b010", 2),
    "DM": int("0b011", 2),
    "A": int("0b100", 2),
    "AM": int("0b101", 2),
    "AD": int("0b110", 2),
    "ADM": int("0b111", 2),
}

C_INSTRUCTION_JUMP = {
    "": int("0b000", 2),
    "JGT": int("0b001", 2),
    "JEQ": int("0b010", 2),
    "JGE": int("0b011", 2),
    "JLT": int("0b100", 2),
    "JNE": int("0b101", 2),
    "JLE": int("0b110", 2),
    "JMP": int("0b111", 2),
}


C_INSTRUCTION_REGEX = re.compile(r"(?P<dest>[MDA]{0,1})(?:=)?(?P<comp>[01ADM!+&|-]{1,3})(?:;(?P<jump>[JGTMEQLNP]{1,3}))?")


def remove_whitespace_gen(inp):
    for element in inp:
        yield element.strip().replace(" ", "") 


def transform(line_text: str, symbol_table: Dict[str, int], current_variable_loc: int):
    # A instruction
    if line_text[0] == "@": 
        val = line_text[1:]

        # if literal
        if val.isnumeric():
            return f"{int(val):016b}", symbol_table, current_variable_loc

        # if label or variable
        if val in symbol_table:
            dereference = symbol_table[val]
            return f"{dereference:016b}", symbol_table, current_variable_loc
        else:
            # add new variable to symbol table
            symbol_table[val] = current_variable_loc
            current_variable_loc += 1
            return f"{symbol_table[val]:016b}", symbol_table, current_variable_loc

    # We assume C instruction   
    # check that it matches the C instruction else raise exception
    match = re.match(C_INSTRUCTION_REGEX, line_text)
    if not match:
        breakpoint()
        raise Exception("Invalid Assmebly??")

    dest = match.group("dest") 
    comp = match.group("comp") or ""
    jump = match.group("jump") or ""
    a_bit = 1 if "M" in comp else 0 
    try:
        instruction = f"111{a_bit}{C_INSTRUCTION_COMP[comp]:06b}{C_INSTRUCTION_DEST[dest]:03b}{C_INSTRUCTION_JUMP[jump]:03b}"
    except:
        breakpoint()
    return instruction, symbol_table, current_variable_loc


def main(path: Path):
    # not a deep copy
    symbol_table = {**PREDEFINED_SYMBOLS}
    dest = path.with_suffix(".hack")
    current_variable_loc = VARIABLE_OFFSET

    # 3.10 syntax :))
    with (
            open(path, mode="r") as rf,
            open(dest, mode="w") as wf,
    ):
        # First pass get all labels
        for line_no, line in enumerate(remove_whitespace_gen(rf), 1):
            if line == "":
                continue
            # I assume this is faster than regex
            # L instruction
            if line[0] == "(" and line[-1] == ")":
                label = line[1:-1]
                symbol_table[label] = line_no  

        # reset generator/pointer
        rf.seek(0)
        # Second pass
        for line_no, line in enumerate(remove_whitespace_gen(rf), 1):
            # if line empty or a comment continue or label
            if line == "" or line[:2] == "//" or line[0] == "(" and line[-1] == ")":
                print(f"skipping {line_no}")
                continue
            line, symbol_table, current_variable_loc = transform(line, symbol_table, current_variable_loc)
            wf.write(f"{line}\n")
            print(f"writing line {line_no}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hack Assembler")
    parser.add_argument("path", type=Path, 
                        help="Path to input assembly file to input")
    opt = parser.parse_args()
    main(opt.path)

