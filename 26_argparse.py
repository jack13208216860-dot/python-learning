import argparse


parser = argparse.ArgumentParser(
    description="一个简单的问候程序"
)

parser.add_argument(
    "name",
    help="要问候的人名"
)

parser.add_argument(
    "--times",
    type=int,
    default=1,
    help="重复问候次数"
)

args = parser.parse_args()

for _ in range(args.times):
    print(f"你好，{args.name}！")