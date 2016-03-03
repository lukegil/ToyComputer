import argparse
import time
from src.utils import util_functions


def line_is_valid(line):
    
    try:
        int(line[0:10])
    except ValueError:
        pass
    if line[10] != ":":
        raise ValueError("Line #{} is missing a colon.\n Line: {}".format(line[0:10],line))

    if len(line[12:]) != 12:
        raise ValueError("Line #{} has invalid value. Should be 36 characters long.\n Line: {}".format(line[0:10],line))

    try:
        int(line[12:])
    except ValueError:
        raise ValueError("Line #{} has invalid value. Should be a binary string. \n Line : {}\n".format(line[0:10], line))
    
    return True    

def instruction_to_bin(order):
    
    
    if order == "ADDNEW":
        return "00000001"

    #ADD
    elif order == "ADD":
        return "00000011"

    #SUBNEW
    elif order == "SUBNEW":
        return "00000010"

    #SUBTRACT
    elif order == "SUBTRACT":
        return "00000100"


    ### FLOW CONTROL ###
    #GOTOLEFT
    elif order == "GOTOLEFT":
        return "00000101"

    #GOTORIGHT
    elif order == "GOTORIGHT":
        return "00000111"

    #LEFTIFZERO
    elif order == "LEFTIFZERO":
        return "00001000"
    #RIGHTIFZERO
    elif order == "RIGHTIFZERO":
        return "00001001"

    ### TRANSFERS ###

    #SAVE
    elif order == "SAVE":
        return "00001011"

    #REPLACELEFT
    elif order == "REPLACELEFT":
        return "00001111"
    #REPLACELEFT
    elif order == "REPLACERIGHT":
        return "00010000"

    #PRINT
    elif order == "PRINT":
        return  "00010001"

    #STOP
    elif order == "STOP":
        return "00010111"
    elif order == "NULL":
        return "00000000"
    else:
        raise ValueError("unknown command")


def convert_instructions(line_number, first_instruction, second_instruction):
    if not first_instruction:
        first_instruction = "NULL 0"
    if not second_instruction:
        second_instruction = "NULL 0"


    line_list = []
    line_list.append(util_functions.decimal_to_mem_address(line_number))

    line_list.append(instruction_to_bin(first_instruction.split(" ")[0]))

    try :
        val = first_instruction.split(" ")[1]
    except IndexError:
        val = "0"
    line_list.append(util_functions.decimal_to_mem_address(val))

    line_list.append(instruction_to_bin(second_instruction.split(" ")[0]))
    try :
        val = second_instruction.split(" ")[1]
    except IndexError:
        val = "0"
    line_list.append(util_functions.decimal_to_mem_address(val))

    return line_list[0] + " " + "".join(map(str,line_list[1:]))

def convert_value(line_number, value):
    line_number = util_functions.decimal_to_mem_address(line_number)
    value = util_functions.decimal_to_word(value)
    return line_number + " " + value
    

def compile(input_path, output_path):
    f = open(input_path, 'r')
    compiled_lines = []
    for line in f:
        
        line_number = line.split(":")[0]
        try:
            int(line_number)
        except ValueError:
            raise ValueError("line has a bad numbering. \n Number : {} \n Line : {}\n".format(line_number, line))

        line_value = line.split(":")[1].strip()
        if (line_value[0].isalpha()):
            first_instruction = line_value.split(";")[0].strip()
            try:
                second_instruction = line_value.split(";")[1].strip()
            except IndexError:
                second_instruction = ""
            
            new_line = convert_instructions(line_number, first_instruction, second_instruction)
        else:
            new_line = convert_value(line_number, line_value)
        compiled_lines.append(new_line)
    
    o = open(output_path, 'w')
    for line in compiled_lines:
        o.write(line)
        o.write("\n")
        
    f.close()
    o.close()
    return o

if __name__ == '__main__':
    import logging
    now = time.strftime('%s')
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',
                        help="the file that needs compilation")
    parser.add_argument('-o', '--out', default="./{}".format(now),
                        help="the file to which to write")
    parser.add_argument('-v','--verbose', action="store_true",
                        help='print debug logging')

    args = parser.parse_args()

#    if args.verbose:
#        log_level = logging.DEBUG
#    logging.basicConfig(filename=output_file, level=log_level)

    input_file = args.file
    output_file = args.out

    compile(input_file, output_file)
