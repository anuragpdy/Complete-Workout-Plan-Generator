import streamlit as st
from groq import (
    AuthenticationError,
    RateLimitError,
    BadRequestError,
    APITimeoutError,
    APIConnectionError,
    APIError,
)
from pydantic import ValidationError

from input_schema import WorkoutInput
from validate_inputs import validate_inputs
from workout_generator import generate_workout_plan, WorkoutGenerationError




st.title("Workout Plan Generator")


# -------------------------
# User inputs
# -------------------------

goal = st.selectbox(
    "Fitness Goal",
    [
        "Build muscle",
        "Lose fat",
        "General fitness",
        "Improve endurance",
    ],
)

level = st.selectbox(
    "Experience Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced",
    ],
)

days_per_week = st.slider(
    "Training Days Per Week",
    min_value=1,
    max_value=7,
    value=3,
    step=1,
)

equipment = st.selectbox(
    "Equipment Access",
    [
        "No equipment",
        "Home dumbbells",
        "Full gym",
    ],
)

injuries_or_limitations = st.text_area(
    "Injuries / Limitations",
    placeholder="Enter any injuries, limitations like bad knees, no overhead pressing...",
)


if st.button("Generate Plan"):

    # -------------------------
    # Create validated input object
    # -------------------------

    try:
        inputs = WorkoutInput(
            goal=goal,
            level=level,
            days_per_week=days_per_week,
            equipment=equipment,
            injuries_or_limitations=injuries_or_limitations,
        )

    except ValidationError  as e:
        st.error("Please check your inputs and try again.")
        st.error(f"[ValidationError] {e}")

    else:

        # -------------------------
        # Additional validation
        # -------------------------

        error_message = validate_inputs(inputs)

        if error_message:
            st.error(error_message)

        else:

            # -------------------------
            # Generate workout
            # -------------------------

            with st.spinner("Generating your workout plan..."):

                try:

                    plan = generate_workout_plan(inputs)

                    st.session_state.plan = plan
                    st.session_state.plan_inputs = inputs.model_dump_json()

                except AuthenticationError as e:
                    st.error(
                        "The workout service is unavailable. "
                        "Please try again later or contact support."
                    )
                    print(f"[AuthenticationError] {e}")

                except RateLimitError as e:
                    st.error(
                        "The workout service is busy right now. "
                        "Please try again in a minute."
                    )
                    print(f"[RateLimitError] {e}")

                except BadRequestError as e:
                    st.error(
                        "The workout service encountered an error. "
                        "Please try again later."
                    )
                    print(f"[BadRequestError] {e}")

                except APITimeoutError as e:
                    st.error(
                        "The service took too long to respond. "
                        "Please try again."
                    )
                    print(f"[APITimeoutError] {e}")

                except APIConnectionError as e:
                    st.error(
                        "We can't reach the workout service. "
                        "Please check your connection and try again."
                    )
                    print(f"[APIConnectionError] {e}")

                except WorkoutGenerationError as e:
                    st.error(
                        "We couldn't generate a complete workout plan. "
                        "Please try again."
                    )
                    print(f"[WorkoutGenerationError] {e}")

                except APIError as e:
                    st.error(
                        "The workout service encountered a temporary issue. "
                        "Please try again."
                    )
                    print(f"[APIError] {e}")

                except Exception as e:
                    st.error(
                        "Something unexpected went wrong. "
                        "Please try again."
                    )
                    print(f"[UnexpectedError] {e}")


# -------------------------
# Display generated plan
# -------------------------

if "plan" in st.session_state:

    inputs_obj = WorkoutInput.model_validate_json(st.session_state.plan_inputs)
    st.caption(
        f"Plan for: {inputs_obj.goal} • {inputs_obj.level} • "
        f"{inputs_obj.days_per_week} days • {inputs_obj.equipment}"
    )

    st.markdown(st.session_state.plan)