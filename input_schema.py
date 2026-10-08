from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator

from typing import Literal

FitnessGoal = Literal[
    "Build muscle",
    "Lose fat",
    "General fitness",
    "Improve endurance",
]

ExperienceLevel = Literal[
    "Beginner",
    "Intermediate",
    "Advanced",
]

EquipmentAccess = Literal[
    "No equipment",
    "Home dumbbells",
    "Full gym",
]

class WorkoutInput(BaseModel):
    """
    Validated input schema for the workout plan generator.

    Pydantic enforces:
    - All fields present (except injuries_or_limitations which defaults to None).
    - goal, level, equipment restricted to the Literal values above.
    - days_per_week is a strict int in [1, 7].
    - injuries_or_limitations, if provided, is at most 500 characters.
    - Empty or whitespace-only injuries are normalized to None.
    - Unknown fields raise ValidationError.
    """

    model_config = ConfigDict(extra="forbid")

    goal: FitnessGoal = Field(
        description="The user's primary fitness objective."
    )

    level: ExperienceLevel = Field(
        description="The user's training experience level."
    )

    days_per_week: StrictInt = Field(
        ge=1,
        le=7,
        description="Number of training days per week.",
    )

    equipment: EquipmentAccess = Field(
        description="The equipment available to the user."
    )

    injuries_or_limitations: str | None = Field(
        default=None,
        max_length=500,
        description="Optional free-text injuries, limitations, or restrictions.",
    )

    @field_validator("injuries_or_limitations", mode="before")
    @classmethod
    def normalize_injuries(cls, v: str | None) -> str | None:
        """Treat empty or whitespace-only strings as None."""
        if v is None:
            return None
        stripped = v.strip()
        return stripped if stripped else None