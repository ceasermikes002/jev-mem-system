import json
import os
from typing import Any

from typesafe_sdk import (
    Noul,
    NoulCriteria,
    SystemOneResponse,
    TypeSafeClient,
)

MODEL = "jev-1.13.0"
REMEMBER_AT = 0.5
MEMORY_KEY = "saved_memories"

client = TypeSafeClient(
    api_key=os.environ["TYPESAFE_API_KEY"],
    base_url=os.environ.get("TYPESAFE_ENDPOINT"),
    timeout=120.0,
)

# Prototype storage: user_id -> list of memories.
MEMORIES: dict[str, list[dict[str, Any]]] = {}


MEMORY_GATE = {
    "remember": Noul(
        instructions=(
            "Does the original user input contain a useful, "
            "lasting fact that should influence future analyses? "
            "Evaluate the original input, not facts inferred "
            "only from the model's answer."
        ),
        criteria=NoulCriteria(
            true=(
                "The input contains a lasting preference, goal, "
                "constraint, profile fact, or recurring context."
            ),
            false=(
                "The input contains only a one-off question, "
                "temporary situation, or information irrelevant "
                "to future requests."
            ),
        ),
    )
}


def ask(state: dict, questions: dict) -> SystemOneResponse:
    """Run Jev using the supplied state and question definitions."""
    serialised_questions = {
        key: question.model_dump(mode="json", exclude_none=True)
        for key, question in questions.items()
    }

    return client.system_one(
        state=state,
        questions=serialised_questions,
        model=MODEL,
    )


def answer_text(question, answer) -> str:
    """Convert a Jev answer into readable memory context."""
    if answer.type == "choice":
        return question.criteria[answer.choice]
    if answer.type == "noul":
        return str(answer.noul)
    return str(answer.score)


def make_memory(
    original_state: dict,
    questions: dict,
    response: SystemOneResponse,
) -> dict:
    """Keep the original request separate from its analysis."""
    return {
        "request": original_state,
        "jev_answered": {
            question.instructions: answer_text(
                question, response.answers[key]
            )
            for key, question in questions.items()
        },
    }


def ask_with_memory(
    state: dict,
    questions: dict,
) -> SystemOneResponse:
    """Run Jev with prior memories, then decide whether to save this request."""

    # A stable user ID is essential for isolating memories.
    user_id = state["user"]["id"]
    saved = MEMORIES.get(user_id, [])

    # Don't modify the caller's original state.
    enriched_state = dict(state)
    if saved:
        enriched_state[MEMORY_KEY] = saved

    # First call: your actual Jev analysis.
    response = ask(enriched_state, questions)

    # Second call: evaluate the original request for memory.
    memory = make_memory(state, questions, response)
    # gate_response = ask(memory, MEMORY_GATE)
    # probability = gate_response.answers["remember"].noul # type: ignore

    # if probability >= REMEMBER_AT:
    #     MEMORIES.setdefault(user_id, []).append(memory)
    gate_response = ask(memory, MEMORY_GATE)

    print("\n=== MEMORY GATE RESPONSE ===")
    print(gate_response.model_dump_json(indent=2))

    probability = gate_response.answers["remember"].noul # type: ignore
    print("\nMemory score:", probability)
    print("Threshold:", REMEMBER_AT)

    if probability >= REMEMBER_AT:
        MEMORIES.setdefault(user_id, []).append(memory)
        print("Memory saved.")
    else:
        print("Memory not saved: score below threshold.")

    # Preserve the normal Jev response interface.
    return response
