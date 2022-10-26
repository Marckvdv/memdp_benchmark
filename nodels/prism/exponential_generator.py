from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys

env = Environment(loader=FileSystemLoader("."), trim_blocks=True)
template = env.get_template("exponential.template")

if len(sys.argv) == 1:
    N = 10
else:
    N = int(sys.argv[1])

if N&1 != 0:
    print("error, N must be even", file=sys.stderr)
    exit(1)

print(template.render(n=N))
