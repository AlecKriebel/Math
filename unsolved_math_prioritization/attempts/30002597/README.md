# 30002597: source correction and classical decision criterion

**Current result: complete existence-decision criterion, independently reviewed PASS.**
Recommended disposition: **already_solved, 1/5 substantive author turns**, as a
credited classical consequence rather than a novel discovery.
For a prescribed curve on a genus-g closed oriented surface, the new candidate
proves that a stable singular-disk extension in some compact bounding
3-manifold exists exactly when

`corank(pi_1(S_g) / <<gamma>>) = g`.

Razborov's published rank algorithm computes this integer. The proof handles
unoriented choices of ambient 3-manifold, exact parametrized boundary, stable
branch points, all genera, and both directions of the criterion. It is a
classical-consequence result, with **no new-algorithm or historical-priority
claim**. The algorithm is theoretical; it is not implemented here.

- [Current result and limits](RESULT.md)
- [Complete reviewed criterion](CORANK_CANDIDATE.md)
- [Independent full review](corank_independent_review/FINAL_REVIEW.md)
- [Candidate freeze receipt](corank_frozen_artifacts.json)
- [Corank-route sources](corank_sources.json)
- [Finite input/witness controls](verify_corank_inputs.py) and [output](corank_input_verification.json)
- [Earlier source/scope audit](SOURCE_AUDIT.md) and [its independent review](source_review/REVIEW.md)
- [Old counterexample application checks](APPLICATION_CHECK.md)
- [Counterexample verifier](verify_example.py), [output](verification.json), and [sources](sources.json)
- [Research log](RESEARCH_LOG.md)

Fresh substantive author attempts: **1/5**, one corank/handlebody mechanism.
The earlier interrupted source investigation consumed zero proof turns; that
historical count has not been used to erase the new author attempt. Review and
packaging are not counted as mathematical attempts. A complete result was reached on turn 1 and passed separate full review,
so the latest five-turn instruction permits stopping without four artificial attempts.

## Scope and provenance

The universal affirmative interpretation was already false by Carter's 1991
counterexample. The initial source-only audit correctly separated that fact
from an unrestricted decision theorem it had not yet found. Subsequent
substantive attempt 1 supplies a full decision criterion using classical
results. Neither stage claims to classify all virtual-string cobordism classes.

The source-only package is frozen at `aeb7bb3b659db44664de13ece41a8b9d639a6cc6`
and received an independent scoped PASS. The later corank argument has now
received its own full independent PASS. The original imported record, null
prior report, historical notes, and source review are preserved.

The frozen proof and freeze receipt retain their original pending-review status
as historical provenance; the current verdict is the linked full review and
RESULT.md. The original imported open-status fields are likewise historical.

Publication is limited to an open draft PR. No merge, release, or external
researcher outreach is authorized. The parent recorded substantive author turn 1
in the campaign recovery-event ledger. Only this problem’s QUEUE.md row is
updated; global queue-machine files are left to the single queue writer.

## Reproduce finite controls

From the repository root:

```sh
python3 unsolved_math_prioritization/attempts/30002597/verify_example.py
python3 unsolved_math_prioritization/attempts/30002597/verify_corank_inputs.py
```

Both scripts use only the standard library. They do not implement Razborov's
rank algorithm or certify the general topological lemmas by computation.

The earlier `assessment_proposed.json` is a superseded historical source-only
assessment and must not be applied. `assessment_final.json` records the current
reviewed recommendation. No global assessment/history regeneration was run
without the verified source cache.
