# Laptop Recommendation Expert System

This project is a small expert system in Python. It uses a backward-chaining style of reasoning to recommend a laptop category from the user's answers.

## Files

- `main.py` - entry point for the terminal app
- `expert_system/domain.py` - rules, questions, and data models
- `expert_system/engine.py` - backward-chaining engine and output formatting
- `requirements.txt` - Python dependencies

## How to Run

```bash
python3 main.py
```

Demo mode for two test cases:

```bash
python3 main.py --demo
```

## What the System Does

- asks about use, budget, performance, portability, battery, and storage
- checks the rules one by one using backward chaining
- prints the best laptop category and the reasoning trace

## Assignment Notes

The PDF report for this project includes:

- project overview
- code structure
- two test screenshots
- explanation of expert systems vs regular programming
- AI usage disclaimer
