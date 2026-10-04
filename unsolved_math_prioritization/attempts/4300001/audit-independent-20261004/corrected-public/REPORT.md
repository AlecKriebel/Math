# 4300001 / AMR-042-0001 — Order of mixing

## Result

The original prime-unspecified target remains **unsolved** after five substantive
approach families. The submitted partial theorem is:

- The defining seven-term polynomial is absolutely irreducible for every prime.
- The group F_p^*⟨x,y⟩ is radical-saturated in its function field.
- For every prime p, **5 ≤ M_p ≤ 6**.
- For **p=2, M_2=6**.

`PROOF.md` contains complete arguments for these partial conclusions. It imports
Einsiedler–Ward's geometric bound and Derksen–Masser's minimum nonmixing-relation
lemma, with attribution. Historical novelty has not been established.

## Remaining question

For each odd prime, does a six-term nonzero Laurent multiple of f exist over F_p?
Here that question is equivalent to M_p=5 versus M_p=6. The reduction is justified
by a proved saturation result; it is not assumed for arbitrary algebraic actions.
The report also proves necessary congruences for any such six-term witness.
No finite exponent bound is asserted.

## Source and status check

The exact polynomial and source question were checked in Thomas Ward's December
2006 update, Problem A, p. 1. The catalogue URL returned HTTP 403. The pinned
catalogue record agrees with the primary source. A later published result,
Derksen–Masser (online 2017; print 2018), provides an effective general algorithm;
its two worked examples differ from this polynomial. The bounded literature
search found no exact resolution of Ward's example, which is not evidence that
none exists. The prior catalogue report's general computational pessimism is
therefore not retained as a current theorem.

Live repository checks found this target queued at 0/5 and no exact-ID branch,
PR, indexed code hit, state entry, attempt folder, or related-target group.
The broader mixing-title PR results concerned different problems. This does not
exclude differently named or unindexed duplicates. No remote write was made.

## Reproduction

From this directory, run:

```
python3 check.py --output control-results.replay.json
cmp control-results.json control-results.replay.json
sha256sum -c SHA256SUMS
```

The standard-library-only script passes **62,094 exact assertions**. It verifies
symbolic identities, small characteristic controls, two truncated local series,
finite support-graph cases, necessary odd-prime congruences, and all 59,561
projectively distinct multipliers in four small boxes. Every searched box has
minimum resulting support seven.

These computations supplement the written unbounded proofs. They do not prove
saturation, mixing, or the missing odd-prime six-term exclusion. No large search
or effective general Derksen–Masser algorithm was run.

## Review and publication gate

This is the frozen author submission for fresh independent mathematical and
source review. It has not yet passed that review. Suggested queue disposition:
**unsolved, 5/5**. Only this target's status and turn cells may be changed unless
separate Findings approval is obtained. Source PDFs, corpus files, live repository
snapshots, and private coordination are excluded from this public packet.
No merge, release, DOI, or preprint publication is claimed or requested here.
