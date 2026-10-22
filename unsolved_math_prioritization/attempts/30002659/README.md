# Shortest billiards in constant-width bodies

Five-attempt partial investigation of problem 30002659 / OWR-13110-001. The all-dimensional statement is **unsolved, 5/5** here. This folder contains source-checked, provisional AI-assisted research by Alec Kriebel; it is not a claimed solution, novelty certificate or human peer-reviewed result.

Read SOURCE_GATE.md for the exact every-shortest-orbit target and primary sources, then the numbered attempts and RESEARCH_LOG.md. Current author budget: 5/5 substantive attempts.

## Results and limits

- Attempt 1: planar trajectories reduce to the credited planar theorem
- Attempt 2: exact finite antipodal-completion test using the classical completion theorem
- Attempt 3: a symmetric skew-family exclusion and a noncertifying 80-start search
- Attempt 4: an orbit-specific balanced-normal moment bound
- Attempt 5: antipodal-normal-measure exclusion and an exact failed-shortcut example

Run `python verify_exact.py` for the exact finite controls. `search_four.py` requires NumPy and SciPy and is explicitly exploratory; its saved output is not a proof or interval certificate. General nonplanar low-turn orbits remain unresolved. Independent review is pending.
