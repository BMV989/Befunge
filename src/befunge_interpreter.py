import argparse


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
        nonlocal ip_direction
        if string_mode == True and instruction != "\"":
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

        elif  instruction == "/":
            a = stack.pop()
            b = stack.pop()
            stack.append(b // a)

        elif instruction == "%":
            a = stack.pop()
            b = stack.pop()
            stack.append(b % a)

        elif instruction == "!":
            # LOGICAL NOT
            value = stack.pop()
            if value == 0:
                stack.append(1)
            else:
                stack.append(0)
        elif instruction == "`":
            # GREATER THAN (b>a)
            a = stack.pop()
            b = stack.pop()
            if b > a:
                stack.append(1)
            else:
                stack.append(0)
        # TODO: implement the rest instructions
        pass
    def step() -> None:
        while grid[ip_y][ip_x] != end_program:
            interpret(grid[ip_y][ip_x])
            move_ip()

    return step()




def main() -> None:
    parser = argparse.ArgumentParser(prog="Befunge interpreter")
    parser.add_argument("filename", type=str, help="Befunge file to interpret")
    parser.add_argument("-g","--grid", action="store_false", help="show interpreted gird")
    args = parser.parse_args()
    if args.grid: print(parse_befunge_file(args.filename))
    befunge_interpreter(parse_befunge_file(args.filename))

if __name__ == "__main__":
    main()