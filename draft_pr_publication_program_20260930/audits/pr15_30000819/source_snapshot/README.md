# 30000819: volume bounds for semigroup holes

**Independently AI-reviewed partial result / source-scope hold. No full resolution claimed.**

The original 2007 question asks for a highest-hole height bound by normalized
volume. The dataset weakens this to a bound in terms of volume. The note
proves the coarse bound

\[
h\le 2V^2(V-1)^2-2
\]

when holes are finite and nonempty, including configurations which omit
lattice points of their convex hull. This combines classical toric
regularity bounds with elementary support counting. It does not prove the
sharper possible interpretation h <= V, and no historical-priority claim
is made for the coarse corollary.

## Contents

- [PROOF.md](PROOF.md): exact theorem, dependencies, proof, and unresolved
  sharper formulation
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): original wording, current literature,
  and duplicate/prior-attempt gate
- [RESEARCH_LOG.md](RESEARCH_LOG.md): one substantive attempt and stopping
  condition
- [attempt.json](attempt.json): machine-readable status and provenance
- [source_record.json](source_record.json): selected pinned upstream record
- [verify.py](verify.py), [verification.json](verification.json): exact
  finite consistency and negative controls
- [review/REVIEW.md](review/REVIEW.md): independent mathematical and source
  audit, including a corrected degree-zero wording issue and 165 separate
  exact assertions

Run the modest checks with `python3 verify.py`. They do not replace the
general written proof or independent review.

This is provisional AI-assisted research, using gpt-6-astra at xhigh.
The queue's historical ultra planning budget is not the execution setting.
