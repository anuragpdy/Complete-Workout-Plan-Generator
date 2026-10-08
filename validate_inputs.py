
from typing import Optional
from input_schema import WorkoutInput, FitnessGoal, ExperienceLevel, EquipmentAccess



def validate_inputs(inputs: WorkoutInput) -> Optional[str]:
    """
    Validate workout form inputs for semantic correctness beyond types.

    Pydantic + Streamlit widgets already enforce types and ranges.
    This function catches semantic edge cases and returns user-friendly
    messages for the UI to display.

    Args:
        inputs: The WorkoutInput to validate.

    Returns:
        None if inputs are valid.
        A user-facing error message (str) describing the first failure.
    """
    if inputs.days_per_week < 1 or inputs.days_per_week > 7:
        return "Please select between 1 and 7 training days per week."

    return None