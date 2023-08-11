from src.compiler import MicroCompiler
from src.runtime import MicroRuntime

# Create an instantce of the compiler
compiler = MicroCompiler()

# Load Micro code
# with open("./sample.mi") as file:
#     micro_code = file.read()

micro_code = """
new x = 2
new y = 3
{
    new z = 4
    new w = 5
    {
        new v = 6
        new u = 7
    }
    new p = 8
}

get x
get y
get z
get w
get v
get u
get p
get p

{
"""

main_block = compiler.compile(micro_code)

if main_block is False:
    print("Compilation Error. MicroCompiler.compile() returned False!")
else:
    main_block.print(0)

MicroRuntime(main_block).run()
