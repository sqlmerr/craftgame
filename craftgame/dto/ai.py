from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratedItemDTO:
    name: str
    emoji: str


@dataclass(frozen=True)
class GenerateItemDTO:
    ingredient1_name: str
    ingredient2_name: str
