from .agent import SimpleAgent


def main():
    agent = SimpleAgent()

    print("模块化 Agent 已启动，输入 exit 可以退出。")

    while True:
        user_question = input("\n你：").strip()

        if user_question.lower() in {
            "exit",
            "quit",
            "退出"
        }:
            print("Agent：再见！")
            break

        if not user_question:
            print("请输入问题。")
            continue

        answer = agent.ask(user_question)

        print("Agent：", answer)


if __name__ == "__main__":
    main()