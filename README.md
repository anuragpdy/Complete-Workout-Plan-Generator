# Workout Plan Generator

A Streamlit app that generates personalized weekly workout plans using an LLM via the Groq API.

Built as Assignment 01 for the Codebasics AI Engineering Cohort.

## Features

- Structured form inputs: fitness goal, experience level, days per week, equipment, optional injuries.
- Generates a markdown-formatted weekly workout plan via Llama / GPT-OSS models hosted on Groq.
- Handles injuries semantically (natural language, not keyword matching).
- Resists prompt injection in free-text fields.
- Graceful error handling for API failures.

## Tech Stack

- **Python 3.11+**
- **Streamlit** for the UI
- **Groq** for the LLM API (currently using `openai/gpt-oss-120b`)
- **Pydantic** for input validation

## Setup

### Prerequisites

- Python 3.11 or higher
- A Groq API key ([get one here](https://console.groq.com))

### Installation

1. Clone the repo:

```bash
   git clone https://github.com/<your-username>/workout-plan-generator.git
   cd workout-plan-generator
```

2. Create and activate a virtual environment:

```bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   # or
   .venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Configure the Groq API key:

```bash
   cp .env.example .env
   # Then edit .env and add your actual key
```
The app opens at `http://localhost:8501`.

### Configuration

Runtime settings are centralized in `config.py`:

| Constant | Default | Purpose |
|---|---|---|
| `MODEL` | `"openai/gpt-oss-120b"` | Groq model identifier |
| `TEMPERATURE` | `0` | Sampling temperature (0 = deterministic) |
| `MAX_TOKENS` | `4000` | Upper bound on response length (sized for 7-day plans) |

To experiment with a different model or increase response variability, edit `config.py` directly. No code changes elsewhere needed.


## Usage

1. Select your fitness goal, experience level, days per week, and equipment access.
2. Optionally describe any injuries or limitations.
3. Click "Generate Plan."
4. The generated workout plan appears below the form.

## Project Structure

```
workout-plan-generator/
├── app.py                # Streamlit UI, entry point
├── config.py             # Runtime config (model, temperature, max_tokens)
├── input_schema.py       # Pydantic schema for form inputs
├── prompts.py            # System and user prompt builders
├── validate_inputs.py    # Explicit semantic validator
├── workout_generator.py  # LLM API call + content validation
├── runner_test.py        # Prompt test battery (used during iteration)
├── requirements.txt
├── .env.example
└── README.md
```

## Architecture

```
                         Streamlit UI
                             │
                             ▼
                         app.py
                             │
                             ▼
                    WorkoutInput
                  (Pydantic validation)
                             │
                             ▼
                    validate_inputs.py
                             │
                             ▼
                   workout_generator.py
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
             prompts.py              config.py
                 │                       │
                 └───────────┬───────────┘
                             ▼
                         Groq API
                             │
                             ▼
                     Generated Plan
```
## Manual Testing

The following scenarios have been verified end-to-end during development:

| Scenario | Expected Behavior | Verified |
|---|---|---|
| Beginner, 2 days, No equipment, General fitness, no injuries | 2-day bodyweight plan, no disclaimer | ✓ |
| Intermediate, 5 days, Full gym, Build muscle, no injuries | 5-day plan with compound lifts, 6-12 reps | ✓ |
| Beginner, 3 days, Home dumbbells, "bad knees" | Plan with physician disclaimer, no deep squats or jumps | ✓ |
| Intermediate, 4 days, Full gym, "no overhead pressing" | Plan with disclaimer, no overhead variants, lateral raises OK | ✓ |
| Beginner, 3 days, No equipment, prompt injection in injuries field | Model ignores injection, generates normal bodyweight plan | ✓ |
| Beginner, 3 days, No equipment, "I only want to use a barbell" | Model uses bodyweight (structured wins), no disclaimer | ✓ |
| Invalid Groq API key | User sees "service unavailable", not technical error | ✓ |
| `max_tokens=5` (force truncation) | User sees "couldn't generate complete plan", not crash | ✓ |

These scenarios form the test battery used during prompt iteration.
See `runner_test.py` for the full automated battery (prompt-level checks).


## Prompt Engineering

The system prompt evolved through 5 iterations and was evaluated against a 9-case test battery.
The test battery covers:
- Normal usage
- Different experience levels
- Different equipment constraints
- Injuries and physical limitations
- Unusual injury phrasing
- Prompt injection
- Multiple simultaneous constraints
- Conflicting structured and free-text inputs

### Key Prompt Engineering Patterns

1. **Explicit output format** The system prompt defines the expected Markdown structure using explicit output templates and placeholders.

2. **Semantic injury handling** The prompt interprets natural-language limitations semantically rather than relying only on keywords.
For example: "No overhead pressing"
is treated as a restriction covering related vertical pressing movements rather than only the exact phrase "overhead pressing".

3. **Input priority.** Conflicting inputs follow an explicit priority order:

```
   System instructions
          ↓
   Structured inputs
          ↓
   Free-text inputs
```

Structured fields therefore take precedence over conflicting instructions contained in free-text fields.

4. **Prompt injection resistance** The injuries/limitations field is treated as untrusted user-provided data.
Instructions embedded within that field cannot modify the system's role, output format, safety rules, or structured inputs.

5. **Instruction/output separation** Instruction sections use:
    `##[Instructions]` while generated output sections use:
    `###` This separation helps prevent instructions from leaking into the generated workout output.

## Error Handling
The application distinguishes between API-level failures and workout-generation failures.
Examples include:
- Authentication errors
- Rate-limit errors
- Invalid API requests
- API timeouts
- API connection failures
- Workout generation failures
- Other API errors
- Unexpected application errors

WorkoutGenerationError is a custom exception used when the API responds but the generated workout cannot be used as a complete response.
For example, the application handles cases such as:
- Empty model responses
- Truncated responses
- Content-filtered responses
- Unexpected completion states
User-facing messages are kept separate from the underlying technical error information.

## Input Validation
The application uses Pydantic to validate structured user inputs.
The WorkoutInput schema defines fields for:
- Fitness goal
- Experience level
- Training days per week
- Equipment access
- Injuries or limitations
Additional semantic validation is handled separately through:
validate_inputs.py

This keeps structured schema validation separate from application-specific validation rules.

## Known Limitations

- The model may prescribe borderline exercises, such as mountain climbers, for users with wrist constraints. Additional category expansion would be required to fully address this.
- The plan does not automatically refresh when inputs change; the user must click Generate Plan again.
- Automated tests are not currently implemented and are deferred to future assignments.

