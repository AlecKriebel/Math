# 20000276: graded-family F-pure-threshold limits

**Candidate mathematical result; fresh independent review is required.**
The regular-local theorem is complete. The intended scope of the original
AIM question has not been freshly verified because the primary problem page
was unavailable. No historical novelty or human-peer-review claim is made.

## Results

For an F-finite regular local ring of characteristic `p>0` and any sequence
of nonzero proper ideals with `I_a I_b ⊆ I_(a+b)`,

`lim_n n fpt(I_n) = sup_n n fpt(I_n)`, allowing `+infinity`.

The proof works without decreasingness, monomiality, or Noetherianity of
the Rees algebra. Its central ingredient is the fixed-factor formula
`lim_k k fpt(I^k J)=fpt(I)` for a fixed nonzero ideal `J`.

For descending filtrations, a direct ceiling-index argument already proves
convergence using only monotonicity and power scaling of the threshold.
Thus the imported partial result's Noetherian restriction and factor-p
liminf gap were unnecessary in that setting.

Ring assumptions genuinely matter. In
`R=(F_p[x,y,z]/(xy))_(x,y,z)`, a two-generated Rees algebra gives a graded
family of nonzero proper ideals containing nonzerodivisors for which
`n fpt_R(I_n)` alternates exactly between 2 and 0. This is a counterexample
to the unrestricted F-pure-ring reading, not to the regular-local theorem.

## Files and verification

- `PROOFS.md`: all proofs, precise quantifiers, singular boundary and arithmetic examples
- `REPORT.md`: source scope, literature comparison, actual prior-work checks and stopping decision
- `RESEARCH_LOG.md`: three substantive approaches and completion estimates
- `SOURCE_METADATA.json`: public source identity and inspection metadata only
- `verify_math.py`, `CHECKS.json`: 282,118 exact finite assertions
- `verify_integrity.py`, `AUTHOR_MANIFEST.json`: byte-level snapshot verification

Run `python3 verify_math.py` and `python3 verify_integrity.py` from this directory.
The finite controls supplement the proofs; they do not establish the
arbitrary-ring or unbounded-index statements by computation.

The safe packet contains no copied papers, source extracts, dataset contents,
or private coordination files. No remote writes were performed by its author.
