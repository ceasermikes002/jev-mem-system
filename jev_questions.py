
from typesafe_sdk import Choice, Noul, NoulCriteria

QUESTIONS = {
    "intent": Choice(
        instructions="Identify the user's primary intent.",
        criteria={
            "learn": "The user wants to understand a concept or obtain information.",
            "build": "The user wants to create, implement, or debug something.",
            "decide": "The user wants to compare options or make a decision.",
            "create": "The user wants to produce content or a creative artifact.",
            "plan": "The user wants a plan, roadmap, or sequence of actions.",
            "other": "The request does not fit the other categories.",
        },
    ),

    "urgency": Choice(
        instructions="Classify the urgency expressed in the user's request.",
        criteria={
            "urgent": "The user explicitly needs immediate action.",
            "time_sensitive": "The request has a specific deadline or near-term timing.",
            "normal": "The request has no explicit time pressure.",
        },
    ),

    "sentiment": Choice(
        instructions="Classify the user's expressed sentiment toward the subject.",
        criteria={
            "positive": "The user expresses satisfaction, excitement, or approval.",
            "negative": "The user expresses dissatisfaction, frustration, or disappointment.",
            "neutral": "The user expresses neither clearly positive nor negative sentiment.",
            "mixed": "The user expresses both positive and negative sentiment.",
        },
    ),

    "requires_action": Noul(
        instructions="Estimate how strongly the user is requesting an actionable response.",
        criteria=NoulCriteria(
            true="The user asks for steps, implementation, a recommendation, or a concrete deliverable.",
            false="The user primarily expresses an opinion or asks for information without requesting a concrete action.",
        ),
    ),
}
