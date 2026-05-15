from __future__ import annotations

import collections
from typing import Callable, Dict, Iterable, List, Optional

from collections.abc import Mapping, MutableMapping, Sequence

if not hasattr(collections, "Mapping"):
    collections.Mapping = Mapping  # type: ignore[attr-defined]
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = MutableMapping  # type: ignore[attr-defined]
if not hasattr(collections, "Sequence"):
    collections.Sequence = Sequence  # type: ignore[attr-defined]

from experta import Fact, KnowledgeEngine

from .domain import QUESTIONS, Recommendation, RULES, Rule


class AnswerFact(Fact):
    """Stored user answer fact."""


class RecommendationFact(Fact):
    """Final category fact."""


class LaptopExpertSystem(KnowledgeEngine):
    """
    A tiny backward-chaining expert system for laptop recommendations.

    Experta is used for the project structure and fact representation, while
    the reasoning controller performs goal-driven backward chaining.
    """

    def __init__(self, input_func: Callable[[str], str] = input) -> None:
        super().__init__()
        self.input_func = input_func
        self.known_answers: Dict[str, str] = {}
        self.trace: List[str] = []
        self.fired_rule: Optional[Rule] = None

    def ask_fact(self, key: str) -> str:
        if key in self.known_answers:
            return self.known_answers[key]

        label, options = QUESTIONS[key]
        options_text = ", ".join(options)
        while True:
            answer = self.input_func(f"{label} ({options_text}): ").strip().lower()
            if answer in options:
                self.known_answers[key] = answer
                self.declare(AnswerFact(key=key, value=answer))
                return answer
            print(f"Invalid input. Please enter one of: {options_text}")

    def prove_condition(self, key: str, expected: str) -> bool:
        value = self.ask_fact(key)
        return value == expected

    def prove_rule(self, rule: Rule) -> bool:
        satisfied = []
        for key, expected in rule.conditions.items():
            if self.prove_condition(key, expected):
                satisfied.append(f"{key}={expected}")
            else:
                self.trace.append(
                    f"{rule.name}: failed because {key} was {self.known_answers.get(key)!r}, expected {expected!r}"
                )
                return False

        self.trace.append(f"{rule.name}: matched {len(satisfied)}/{len(rule.conditions)} conditions")
        self.fired_rule = rule
        self.declare(RecommendationFact(category=rule.category))
        return True

    def infer(self) -> Recommendation:
        self.reset()
        self.trace = []
        self.fired_rule = None

        ordered_rules = sorted(RULES, key=lambda item: item.priority)
        for rule in ordered_rules:
            if self.prove_rule(rule):
                return self._build_recommendation(rule)

        fallback = next(rule for rule in RULES if rule.category == "General-purpose laptop")
        self.trace.append("No specific rule matched; using the general-purpose fallback.")
        return self._build_recommendation(fallback)

    def _build_recommendation(self, rule: Rule) -> Recommendation:
        matched = [f"{key}={self.known_answers.get(key)}" for key in rule.conditions if self.known_answers.get(key) == rule.conditions[key]]
        confidence = len(matched) / len(rule.conditions) if rule.conditions else 0.0
        specs = list(rule.specs)

        if self.known_answers.get("portability") == "yes" and "Lightweight design" not in specs:
            specs.append("Lightweight design")
        if self.known_answers.get("battery") == "yes" and "Long battery life" not in specs:
            specs.append("Long battery life")
        if self.known_answers.get("storage") == "yes" and "1 TB SSD preferred" not in specs:
            specs.append("1 TB SSD preferred")
        if self.known_answers.get("performance") == "yes" and "High-performance CPU" not in specs:
            specs.append("High-performance CPU")

        return Recommendation(
            category=rule.category,
            rule_name=rule.name,
            reason=rule.reason,
            confidence=confidence,
            matched_conditions=matched,
            trace=list(self.trace),
            specs=specs,
        )

    def run_interactive(self) -> None:
        print("Laptop Recommendation Expert System")
        print("Backward chaining with experta facts")
        print()
        result = self.infer()
        self.print_recommendation(result)

    def run_demo(self, cases: Iterable[dict]) -> None:
        for case in cases:
            title = case["title"]
            answers = case["answers"]
            print("=" * 72)
            print(title)
            print("=" * 72)
            demo = LaptopExpertSystem(input_func=lambda prompt, _answers=answers: _answers[self._question_key(prompt)])
            result = demo.infer()
            demo.print_recommendation(result)
            print()

    def print_recommendation(self, result: Recommendation) -> None:
        print(f"Recommended category: {result.category}")
        print(f"Selected rule: {result.rule_name}")
        print(f"Reason: {result.reason}")
        print(f"Confidence: {round(result.confidence * 100):.0f}%")
        print()
        print("Matched conditions:")
        for item in result.matched_conditions:
            print(f"- {item}")
        print()
        print("Recommended specifications:")
        for item in result.specs:
            print(f"- {item}")
        print()
        print("Reasoning trace:")
        for item in result.trace:
            print(f"- {item}")

    @staticmethod
    def _question_key(prompt: str) -> str:
        for key, (label, _) in QUESTIONS.items():
            if prompt.startswith(label):
                return key
        raise KeyError(prompt)
