from dotenv import load_dotenv

load_dotenv()

from jev_questions import QUESTIONS
from memory import ask_with_memory, MEMORIES


def main():
    user_id = "test-user-001"

    state = {
        "user": {"id": user_id},
        "input": (
            "I’m building Jev, a personal AI assistant. "
            "Please remember that this is an ongoing project and that I "
            "prefer concise, practical guidance with runnable Python "
            "examples. In future conversations, prioritize helping me "
            "improve Jev."
        ),
    }

    response = ask_with_memory(state, QUESTIONS)

    print("\n=== JEV ANALYSIS ===")
    print(response.model_dump_json(indent=2))

    print("\n=== SAVED MEMORIES ===")
    print(MEMORIES.get(user_id, []))


if __name__ == "__main__":
    main()
