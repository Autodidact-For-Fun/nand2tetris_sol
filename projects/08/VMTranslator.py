from utils import read_vmfile, vm_to_assmble, write_asmfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('vmfile_path', type=str)
args = parser.parse_args()

filename = args.vmfile_path.split('/')[-1].split('.')[0]

# read vm file and return content as a list
vm_codes = read_vmfile(args.vmfile_path)

# translate vm codes to assembly codes
asm_codes = vm_to_assmble(vm_codes, filename)

# write assembly codes to output file
write_asmfile(asm_codes, args.vmfile_path.replace('.vm', '.asm'))
print('Assembly codes written to {}'.format(
    args.vmfile_path.replace('.vm', '.asm')))
