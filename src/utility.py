import os


def decide(question: str, answers: list[str] = []) -> str:
    print(question)
    # if this is not a selection question, the user has to give his own input
    if not answers:
        return input()

    for i, answer in enumerate(answers):
        print(f"{i + 1}. {answer}")
    return answers[int(input()) - 1]


def inform(content: str):
    print(content)


def exec_sh(command: str) -> int:
    return os.system(command)


def free_storage():
    for item in ["image", "container"]:
        exec_sh(f"docker {item} prune")
