from typing import Optional

from groq import Groq

from input_schema import WorkoutInput, FitnessGoal, ExperienceLevel, EquipmentAccess
from prompts import build_system_prompt, build_user_prompt
from config import MODEL, TEMPERATURE, MAX_TOKENS

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

_client = Groq() 

class WorkoutGenerationError(Exception):
    """
    Raised when the API responds but fails to produce
    a complete workout plan.
    """
    pass


def generate_workout_plan(inputs: WorkoutInput) -> str:
    """
    Generate a workout plan using the Groq API.

    Args:
        inputs: A WorkoutInput instance containing all the necessary parameters.


    Returns:
        The generated workout plan as a string.

    Raises:
        WorkoutGenerationError: If the API call fails or the response is incomplete.
    """

    messages = [
        {
            "role": "system",
            "content": build_system_prompt(),
        },
        {
            "role": "user",
            "content": build_user_prompt(inputs),
        },
    ]

    response = _client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    finish_reason = response.choices[0].finish_reason
    content = response.choices[0].message.content

    # Content-level failure: response was received,
    # but the model did not produce a complete answer.

    if not content or not content.strip():
        raise WorkoutGenerationError(
            f"API returned empty content (finish_reason={finish_reason!r})."
        )

    if finish_reason == "length":
        raise WorkoutGenerationError(
            "Response was truncated at the max_tokens limit."
        )

    if finish_reason == "content_filter":
        raise WorkoutGenerationError(
            "Response was blocked by the content filter."
        )

    if finish_reason != "stop":
        raise WorkoutGenerationError(
            f"Response ended unexpectedly (finish_reason={finish_reason!r})."
        )

    return content.strip()