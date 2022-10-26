import itertools
import sys

colors = 3
guesses = 7
balls = 3

if len(sys.argv) == 4:
    colors, guesses, balls = tuple(map(int, sys.argv[1:]))
elif len(sys.argv) != 1:
    print("Invalid amount of arguments", file=sys.stderr)

INPUT_ENABLED = True

possible_answers = colors**guesses

indent = 0
end_line = True
def write_to_file(text):
    print('\t'*indent + text, end='\n' if end_line else '')

def answer_to_number(ans):
    total = 0
    power = 1
    for a in reversed(ans):
        total += a*power
        power *= colors
    return total

def answer_to_string(ans):
    return "".join(map(str, ans))

write_to_file("// This file was automatically generated.\n")
write_to_file("mdp\n")

write_to_file(f"const int COLORS = {colors};")
write_to_file(f"const int GUESSES = {guesses};")
write_to_file(f"const int BALLS = {balls};")

for i in range(balls):
    write_to_file(f"const int ANSWER{i}; // 0<=ANSWER{i}<={colors-1}")

comment = ",".join([f"0<=ANSWER{i}<={colors-1}" for i in range(balls)])
write_to_file(f"// {comment}")

write_to_file("module mastermind")
indent += 1

write_to_file("// state")
write_to_file("guess : [0 .. GUESSES] init 0;")
write_to_file("correct : [0 .. BALLS] init 0;")

write_to_file("")
write_to_file("// transitions")
for ans in itertools.product(range(colors), repeat=balls):
    end_line = False
    write_to_file(f"[g{answer_to_string(ans)}] (has_guesses & !all_correct) -> ")

    indent -= 1
    write_to_file("(guess'= guess + 1) & ")
    write_to_file("(correct'= (0")
    for i in range(balls):
        write_to_file(f" + ((ANSWER{i}={ans[i]}) ? 1 : 0)")

    end_line = True
    write_to_file("));")
    indent += 1

if INPUT_ENABLED:
    for ans in itertools.product(range(colors), repeat=balls):
        write_to_file(f"[g{answer_to_string(ans)}] (all_correct | (!has_guesses)) -> true;")
else:
    write_to_file("[] all_correct -> true;")
    write_to_file("[] !has_guesses -> true;")

indent -= 1
write_to_file("endmodule\n")

write_to_file("formula has_guesses = guess < GUESSES;")
write_to_file("formula all_correct = correct=BALLS;")

write_to_file('label "target" = all_correct;')
