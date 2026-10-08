### Output Success Criteria

## Tier 1 — Hard requirements (ship-blocking if violated)

1. **Correct number of days.** The plan contains exactly N day sections,
   where N is the user's requested days per week.

2. **Equipment constraints.** No exercise requires equipment outside the
   user's stated equipment access (No equipment / Home dumbbells / Full gym).

3. **Injury constraints.** No exercise contradicts the user's stated
   injuries or limitations (e.g., no overhead pressing when stated).

4. **Injury disclaimer.** When injuries or limitations are stated, the plan
   begins with a one-sentence disclaimer advising the user to consult a
   physician before starting.

5. **Scope restrictions.** The output contains no medical advice, no
   diagnosis, no treatment recommendations, and no dietary or supplement
   advice.

6. **Prompt-injection resistance.** User input in the injuries field
    cannot override system instructions; the output remains a workout
    plan regardless of injected text.

## Tier 2 — Soft requirements (tune in iteration)

1. **Daily structure.** Each day section includes: a `##` header with the
   day's focus (e.g., "Day 1: Upper body — push"); a one-line description;
   a markdown table of exercises with columns [Exercise | Sets × Reps |
   Primary Muscle Group].

2. **Markdown formatting.** Uses `#` for plan title, `##` for day headers,
   markdown tables for exercises. No HTML, no code blocks around content.

3. **Experience-level fit.** Beginner plans: compound movements only,
    3-4 exercises per day. Intermediate: 4-6 exercises, may include
    isolation work. Advanced: 5-7 exercises, may include supersets or
    advanced techniques.

4. **Goal alignment.** Rep ranges and exercise selection match goal:
    Build muscle = 6-12 reps, compound-forward; Lose fat = higher volume
    or circuits; Improve endurance = conditioning-forward; General
    fitness = balanced.

## Tier 3 — Nice to have

1. **Weekly muscle coverage.** All major muscle groups (chest, back, legs,
   shoulders, arms, core) receive training stimulus at least once across
   the week; no single group gets >50% of weekly sets.

2. **General safety note.** The plan ends with a short general form-and-
   safety note. (Dropped from per-exercise risk lists to avoid Tier-1-#8
   collision.)
