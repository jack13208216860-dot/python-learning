import argparse


parser = argparse.ArgumentParser(
    description="简单计算器"
)

subparsers = parser.add_subparsers(
    dest="command",
    required=True
)

add_parser = subparsers.add_parser(
    "add",
    help="计算两个数字的和"
)
add_parser.add_argument("number1", type=float)
add_parser.add_argument("number2", type=float)

multiply_parser = subparsers.add_parser(
    "multiply",
    help="计算两个数字的乘积"
)
multiply_parser.add_argument("number1", type=float)
multiply_parser.add_argument("number2", type=float)

args = parser.parse_args()

if args.command == "add":
    print("结果：", args.number1 + args.number2)

elif args.command == "multiply":
    print("结果：", args.number1 * args.number2)