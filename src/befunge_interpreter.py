import argparse
from random import randint


def parse_befunge_file(filename: str) -> list[list[str]]:
    with open(filename) as f:
        return [[char for char in line.rstrip()] for line in f]


def befunge_interpreter(grid: list[list[str]]) -> None:
    ip_x = 0
    ip_y = 0
    ip_direction = "right"
    stack = []
    string_mode = False
    ip_directions = ["right", "left", "up", "down"]
    end_program = "@"

    def safe_pop():
        try:
            return stack.pop()
        except IndexError:
            return 0

    def move_ip() -> None:
        nonlocal ip_x, ip_y
        if ip_direction == ip_directions[0]:
            ip_x = (ip_x + 1) % len(grid[ip_y])
        elif ip_direction == ip_directions[1]:
            ip_x = (ip_x - 1) % len(grid[ip_y])
        elif ip_direction == ip_directions[2]:
            ip_y = (ip_y - 1) % len(grid)
        elif ip_direction == ip_directions[3]:
            ip_y = (ip_y + 1) % len(grid)

    def interpret(instruction: str) -> None:
        nonlocal ip_direction, string_mode, stack

        if string_mode and instruction != "\"":
            stack.append(ord(instruction))
            return

        if instruction == " ":
            pass

        elif instruction == ">":
            ip_direction = ip_directions[0]

        elif instruction == "<":
            ip_direction = ip_directions[1]

        elif instruction == "^":
            ip_direction = ip_directions[2]

        elif instruction == "v":
            ip_direction = ip_directions[3]

        elif instruction.isdigit():
            stack.append(int(instruction))

        elif instruction == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)

        elif instruction == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)

        elif instruction == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(a * b)

        elif instruction == "/":
            a = stack.pop()
            b = stack.pop()
            stack.append(b // a)

        elif instruction == "%":
            a = stack.pop()
            b = stack.pop()
            stack.append(b % a)

        elif instruction == "!":
            # LOGICAL NOT
            stack.append(int(not stack.pop()))
        elif instruction == "`":
            # GREATER THAN (b>a)
            a = stack.pop()
            b = stack.pop()
            if b > a:
                stack.append(1)
            else:
                stack.append(0)

        elif instruction == "?":
            # PICK ANY DIRECTION
            ip_direction = ip_directions[randint(0, 3)]

        elif instruction == "_":
            # POP; RIGHT IF 0, LEFT OTHERWISE
            value = safe_pop()
            if value == 0:
                ip_direction = ip_directions[0]
            else:
                ip_direction = ip_directions[1]

        elif instruction == "|":
            # POP; DOWN IF 0, UP OTHERWISE
            value = stack.pop()
            if value == 0:
                ip_direction = ip_directions[3]
            else:
                ip_direction = ip_directions[3]

        elif instruction == "\"":
            # STRING MODE
            string_mode = not string_mode

        elif instruction == ":":
            # DUPLICATE VALUE ON TOP OF STACK
            try:
                value = stack[-1]
            except IndexError:
                value = 0
            stack.append(value)

        elif instruction == "\\":
            # SWAP TWO VALUES ON TOP OF STACK
            a = stack.pop()
            b = safe_pop()
            stack.append(a)
            stack.append(b)

        elif instruction == "$":
            # POP TOP AND DISCARD
            stack.pop()

        elif instruction == ".":
            # POP AND OUTPUT AS INTEGER FOLLOWED BY SPACE
            print(stack.pop(), end=" ")

        elif instruction == ",":
            # POP AND OUTPUT AS ASCII CHARACTER
            print(chr(stack.pop()), end="")

        elif instruction == "#":
            # BRIDGE -- SKIP NEXT CELL
            move_ip()

        elif instruction == "p":
            # PUT -- POP Y, X, AND V, THEN SET (X,Y) TO V
            y = stack.pop()
            x = stack.pop()
            v = stack.pop()
            grid[y][x] = chr(v)

        elif instruction == "g":
            # GET -- POP Y AND X, THEN PUSH ASCII VALUE AT (X,Y)
            y = stack.pop()
            x = stack.pop()
            stack.append(ord(grid[y][x]))

        elif instruction == "&":
            # PUSH USER-GIVEN NUMBER
            stack.append(int(input("Enter a number(0-9): ")))

        elif instruction == "~":
            # PUSH ASCII VALUE OF USER-GIVEN CHARACTER
            stack.append(ord(input("Enter a character: ")))

    def step() -> None:
        if grid[ip_y][ip_x] == end_program: return
        interpret(grid[ip_y][ip_x])
        move_ip()
        step()

    step()


def main() -> None:
    parser = argparse.ArgumentParser(prog="Befunge interpreter")
    parser.add_argument("filename", type=str, help="Befunge file to interpret")
    parser.add_argument("-g", "--grid", action="store_true", help="show interpreted gird")
    args = parser.parse_args()
    grid = parse_befunge_file(args.filename)
    if args.grid: print(grid)
    befunge_interpreter(grid)


if __name__ == "__main__":
    main()
