# Mission: Debug & fix the Polygence matching take-home

## Why
The user received a take-home exercise: a slimmed-down Django + DRF + React mentor↔student matching app with a state-transition bug. Completing it well is part of a job application, so the real goal is a correct, well-reasoned, tested fix they can defend in an interview. Secondarily, they want to rebuild Django fluency after a long break from it.

## Success looks like
- The project runs locally; the inconsistent state (accepted proposal with decline reasons) is reproduced
- The root cause is articulated in a few sentences, in their own words
- A fix that fits the repo's existing patterns is shipped, with tests that would have caught the bug
- They can walk an interviewer through the state transition, the bug, and their fix

## Constraints
- Timebox: a few focused hours, not a rewrite
- Working style: the agent guides with Socratic questions; the user does the work (running, reproducing, writing the fix and tests)
- Django knowledge is rusty ("some" experience, long gap) — lessons should include targeted refreshers
- React knowledge is comfortable — no React basics needed
- The agent must not hand over the solution; it coaches toward it

## Out of scope
- Rewriting the app, adding auth, deployment, or any feature beyond the exercise
- Broad Django/React curriculum not tied to this repo
