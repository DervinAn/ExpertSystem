from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class Rule:
    name: str
    category: str
    conditions: Dict[str, str]
    reason: str
    specs: Sequence[str]
    priority: int


@dataclass
class Recommendation:
    category: str
    rule_name: str
    reason: str
    confidence: float
    matched_conditions: List[str] = field(default_factory=list)
    trace: List[str] = field(default_factory=list)
    specs: List[str] = field(default_factory=list)


QUESTIONS = {
    "use": ("Main use", ["gaming", "programming", "business", "study", "general use"]),
    "budget": ("Budget", ["low", "medium", "high"]),
    "performance": ("Need high performance", ["yes", "no"]),
    "portability": ("Need portability", ["yes", "no"]),
    "battery": ("Need long battery life", ["yes", "no"]),
    "storage": ("Need large storage", ["yes", "no"]),
}


RULES: List[Rule] = [
    Rule(
        name="Gaming laptop rule",
        category="Gaming laptop",
        conditions={"use": "gaming", "performance": "yes", "storage": "yes"},
        reason="Gaming laptops need a strong processor, a dedicated GPU, and large storage.",
        specs=[
            "Intel Core i7 or AMD Ryzen 7",
            "16 GB RAM or more",
            "Dedicated GPU",
            "512 GB SSD or 1 TB SSD",
        ],
        priority=1,
    ),
    Rule(
        name="Programming laptop rule",
        category="Programming laptop",
        conditions={"use": "programming", "performance": "yes"},
        reason="Programming benefits from fast multitasking, good RAM, and an SSD.",
        specs=[
            "Intel Core i5/i7 or AMD Ryzen 5/7",
            "16 GB RAM",
            "SSD storage",
            "Comfortable keyboard",
        ],
        priority=2,
    ),
    Rule(
        name="Business laptop rule",
        category="Business laptop",
        conditions={"use": "business", "battery": "yes", "portability": "yes"},
        reason="Business users often need battery life and a slim machine for travel.",
        specs=[
            "Intel Core i5 or AMD Ryzen 5",
            "8 GB to 16 GB RAM",
            "SSD storage",
            "Long battery life",
        ],
        priority=3,
    ),
    Rule(
        name="Student laptop rule",
        category="Student laptop",
        conditions={"use": "study", "budget": "low"},
        reason="Students on a low budget usually need an affordable everyday laptop.",
        specs=[
            "Intel Core i3/i5 or AMD Ryzen 3/5",
            "8 GB RAM",
            "256 GB SSD",
            "Lightweight design",
        ],
        priority=4,
    ),
    Rule(
        name="Graphic design laptop rule",
        category="Graphic design laptop",
        conditions={"use": "graphic design", "performance": "yes"},
        reason="Graphic design software needs strong CPU performance and a color-accurate display.",
        specs=[
            "Intel Core i7 or AMD Ryzen 7",
            "16 GB RAM or more",
            "Dedicated GPU",
            "Color-accurate display",
        ],
        priority=5,
    ),
    Rule(
        name="General use rule",
        category="General-purpose laptop",
        conditions={"use": "general use"},
        reason="General use needs a balanced laptop for browsing, school work, and media.",
        specs=[
            "Intel Core i5 or AMD Ryzen 5",
            "8 GB RAM",
            "512 GB SSD",
            "Balanced design",
        ],
        priority=99,
    ),
]


DEMO_CASES = [
    {
        "title": "Test 1: Gaming profile",
        "answers": {
            "use": "gaming",
            "budget": "high",
            "performance": "yes",
            "portability": "no",
            "battery": "no",
            "storage": "yes",
        },
    },
    {
        "title": "Test 2: Business profile",
        "answers": {
            "use": "business",
            "budget": "medium",
            "performance": "no",
            "portability": "yes",
            "battery": "yes",
            "storage": "no",
        },
    },
]
