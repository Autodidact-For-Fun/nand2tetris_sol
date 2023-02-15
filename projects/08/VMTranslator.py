from utils import read_vmfile, vm_to_assmble, write_asmfile
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('vmfile_path', type=str)
args = parser.parse_args()

# if args is a file:
if args.vmfile_path[-2:] == "vm":
    print("it's a vm file")
    filename = args.vmfile_path.split('/')[-1].split('.')[0]

    # read vm file and return content as a list
    vm_codes = read_vmfile(args.vmfile_path)

    # translate vm codes to assembly codes
    asm_codes = vm_to_assmble(vm_codes, filename)

    # write assembly codes to output file
    write_asmfile(asm_codes, args.vmfile_path.replace('.vm', '.asm'))
    print('Assembly codes written to {}'.format(
        args.vmfile_path.replace('.vm', '.asm')))

# else if args is a folder:
else:
    print("it's a folder")
    foldername = args.vmfile_path.split('/')[-2]
    vm_codes = ["call Sys.init 0"]
    asm_codes = []
    # the firsr loop is used to create Bootstrap code
    for filename in glob.glob(os.path.join(args.vmfile_path, '*.vm')):
        if "Sys" in filename:
            name = filename.split(".")[0].split("/")[-1]
            print(name)
            vm_codes.extend(read_vmfile(filename))
            asm_codes.extend(vm_to_assmble(vm_codes, name))
    # the second for loop don't need to extent vm_codes
    for filename in glob.glob(os.path.join(args.vmfile_path, '*.vm')):
        if "Sys" not in filename:
            name = filename.split(".")[0].split("/")[-1]
            print(name)
            vm_codes = read_vmfile(filename)
            asm_codes.extend(vm_to_assmble(vm_codes, name))
            
    write_asmfile(asm_codes, '{}/{}.asm'.format(args.vmfile_path, foldername))
    


