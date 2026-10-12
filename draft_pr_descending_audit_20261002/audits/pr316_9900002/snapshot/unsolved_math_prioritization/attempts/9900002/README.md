# No deterministic nondegenerate scale for a null-recurrent total-life process

**9900002 / AMR-098-0002: claimed solved, 1/5 substantive author turns. Complete negative answer; independent mathematical review PASS.**

Thorisson Problem 1.2 asks whether every strictly positive, non-lattice infinite-mean renewal law admits a nondecreasing deterministic scale under which the current total life has a proper nondegenerate limiting distribution. It also proposes the truncated-mean scale. The explicit law in [TURN_1.md](TURN_1.md) answers both questions negatively.

## Result

Give the interarrival law atoms of mass `p_n = 2^(-2^n)` at `a_n = 2^(4^n)`, and place the remaining positive mass uniformly on [1,2]. It is non-lattice and has infinite mean. At deterministic times `t_n = a_n/2`, the current interval has length exactly `a_n` with probability tending to one. Consequently any deterministically scaled subsequence is asymptotically concentrated at one deterministic value. Tightness forces every proper full-time distributional limit to be a point mass. This excludes every deterministic positive normalizer, even without monotonicity.

For the proposed `m(t) = E[min(X,t)]`, the same construction gives `m(t_n)/a_n -> 0`, so the normalized total life escapes to infinity along this subsequence. The proof permits zero initial delay, as the source does, and checks the strict-after renewal endpoint convention.

This does not classify which renewal laws admit useful scales. The regularly varying relative-age literature concerns different assumptions/observables and is not contradicted. The adjacent conditional joint-limit problem is not claimed solved; this example rejects its universal affirmative premise. The distinct Thorisson coupling targets are unchanged.

## Review and reproducibility

- [Complete proof](TURN_1.md), [source/prior-work gate](SOURCE_GATE.md), and [research log](RESEARCH_LOG.md)
- [Independent adversarial review](review/ADVERSARIAL_REVIEW.md): complete negative-answer PASS, with no mandatory mathematical correction
- Author checker: `python verify_turn1.py`, 7,852 exact assertions
- Independent checker: `python review/independent_checks.py`, 646 exact assertions
- Both outputs replay byte-identically; finite controls supplement the written infinite-quantifier proof
- All original author and review bytes are preserved, including historical pending-review status. [Current status](CURRENT_STATUS.json) records the reviewed disposition

## Source-access and priority caveat

Both author and reviewer independently retrieved the primary author's indexed Section 1, pp.1–2, including the exact question and definitions: [Thorisson preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf). Direct original and publisher PDF downloads timed out; no full original visual inspection or preprint/published line-by-line comparison is claimed. The publisher verifies *Open problems in renewal, coupling and Palm theory*, Queueing Systems 68 (2011), 313–319, [DOI](https://doi.org/10.1007/s11134-011-9241-2).

The construction uses elementary geometric stopping and weak-limit arguments. No historical novelty or priority claim is made. This is AI-assisted research with independent AI-assisted review, not human peer review or formal verification. Source PDFs and raw imported records are not redistributed.
