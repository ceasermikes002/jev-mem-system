# Jev Playaround

A small project for exploring TypeSafe's Jev model and Python SDK. It asks Jev to
classify a sample request and checks whether the request is worth remembering.

## How it works

- `jev_questions.py` defines questions about intent, urgency, sentiment, and action.
- `memory.py` sends the request to Jev, then scores whether it contains a lasting
  fact or preference. Scores of `0.5` or higher are saved.
- `main.py` runs the example and prints Jev's answers and saved memories.

Memories are kept in memory while the program runs; they are not saved between
runs.

## Run it

Install the packages and provide a TypeSafe API key:

```bash
pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`, then run:

```bash
python main.py
```
