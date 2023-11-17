import argparse
from itertools import repeat

def main():
    parser = argparse.ArgumentParser(description='This program prints to standard output text \
                                     representing an hspice test for use in VLSI .sp test files, given a number of parameters.',
                                     epilog=None)
    
    parser.add_argument('dut', 
                        type=str,
                        help='the name of the device under test (DUT)')  
    
    parser.add_argument('inputs', 
                        type=str,
                        nargs='+',
                        help='the names of the inputs to the logic function')  
    
    args = parser.parse_args()

    print("* HSPICE testbench file (test.sp)")
    print("* transistor model")
    print(r'.INCLUDE "/cae/apps/data/asap7PDK-2022/asap7PDK_r1p7/models/hspice/7nm_TT_160803.pm')
    print("* Design Under Test (DUT)")
    print(f'.INCLUDE "{args.dut}.sp" * Enable this line for schematic netlist')
    print(f'*.INCLUDE "{args.dut}.pex.netlist" * Enable this line for layout netlist')
    print('* Simulation Parameters')
    print('.TEMP 25.0')
    print('.options artist=2 ingold=2 parhier=local psf=2 hier_delim=0 accurate=1 NUMDGT=8 measdgt=5 GMINDC=1e-18 DELMAX=1n method=gear INGOLD=2 POST=1')
    print('')
    print("v1 vdd 0 0.9v")
    print("v2 vss 0 0v")

    pattern = []
    count_0 = (2 ** len(args.inputs))
    count_1 = (2 ** len(args.inputs))
    slope = 0
    for c in range(len(args.inputs)):
        sub_pattern = (list(repeat(0, count_0)) + list(repeat(1, count_1)))
        sub_pattern = sub_pattern * (2*(2 ** len(args.inputs)) // len(sub_pattern))
        pattern.append(sub_pattern)
        count_0 = count_0 // 2
        count_1 = count_1 // 2
    
    p_c = 0
    for n, s in enumerate(args.inputs):
        print(f"v{n+3} {s} 0 pwl    ", end='')

        slope = 0
        for i, c in enumerate(pattern[n]):
            if c == 0:
                if slope == 2:
                    print(f"{i}ns {p_c}v", end=' ')
                    print(f"{i}.02ns 0v", end=' ')
                    slope = 0
                else:
                    print(f"{i}ns 0v", end=' ')
            else:
                if slope == 2:
                    print(f"{i}ns {p_c}v", end=' ')
                    print(f"{i}.02ns 0.9v", end=' ')
                    slope = 0
                else:
                    print(f"{i}ns 0.9v", end=' ')
            slope += 1
            p_c = 0 if c == 0 else 0.9
        
        print("")

    print('.OP')
    print(f'.tr 10p {(2**(len(args.inputs))*2)-1}ns')

if __name__ == "__main__":
    main()