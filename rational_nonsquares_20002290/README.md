# Positive-existential definability of rational nonsquares

Problem: [UnsolvedMath 20002290 / AIM-LOGIC-0066](https://www.unsolvedmath.com/problems/20002290), Koenigsmann's Question 6 in the AIM workshop problem list of September 9–13, 2013.

**Outcome: unresolved after five substantive attempts, with restricted negative results and conditional reductions.** This is an AI-assisted, unrefereed research note. No full resolution or historical novelty is claimed.

The structure is M=(Q;0,1,+,P₂), where P₂ is the unary set of rational square values, including zero. Multiplication and the squaring function are not language symbols. The actual question asks whether every existentially definable set is existential-positive definable. The catalogue title, “A positive-existential definition of nonzero rationals,” describes earlier partial progress. The prior positive definition of Q× is credited; the remaining target is Q\P₂.

## Results retained

1. Finite fixed square classes or finitely many local nonsquare tests cannot cover all nonsquares. For any finite prime set S, the positive nonsquare 1+(4∏_{p∈S}p)² is a square in every Q_p with p∈S and in R.
2. Every positive-existential formula has a finite-union normal form of simultaneous fixed-coefficient diagonal-quadratic fibers. A disjunct with at most one square atom whose solution set contains no rational square contributes only O(√H) positive integers up to H, so finitely many such disjuncts cannot define the nonsquares.
3. More generally, the nonsquares are not a finite union of images of rational polynomials of degree at most two. Hasse–Minkowski assigns one fixed local obstruction to each quadratic image avoiding squares. This excludes diagonal normal forms with at most one equation total and no additional witness-only constraints, with any number of square variables.
4. Conditional on a uniform bound B for the number of rational points on genus-two curves, M=(B+1)³+3 affine square tests define the squaring graph. Polarization then defines multiplication and imports Poonen's ring-language nonsquare theorem. The uniformity hypothesis is not proved. The known rational five-test false positive is checked exactly.
5. Every homomorphism M^r→M, for finite r≥1, is a coordinate projection. A full nondefinability certificate would instead require a homomorphism between elementary-equivalent models sending a nonsquare to a square; none was constructed.

The unresolved issue is genuinely simultaneous diagonal-square constraints. The single-quadratic Hasse principle cannot be applied to such systems merely one equation at a time.

## Files and checks

- `turn_01.md` through `turn_05.md`: complete attempts, proofs, and remaining gaps
- `SOURCE_GATE.md`: statement recovery, credited prior baseline, and literature scope
- `RESEARCH_LOG.md`: attempt accounting
- `verify_identities.py` and `verification.json`: eight groups of exact identities and bounded sanity checks

Run `python verify_identities.py` with Python 3 and SymPy. All eight groups pass. These checks do not establish the full conjecture, the uniformity hypothesis, or the general proofs. Fresh independent mathematical review is required before using the deductions as established research.
