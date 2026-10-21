# Independent arithmetic falsification log

## 2026-10-21T02:39:21.277017+00:00 — First independent mechanism/objection checkpoint

Assigned audit completion estimate: **25%**. Only original/PROOF.md, original/SOURCE_AUDIT.md, and SOURCE_SNAPSHOT.json have been read. No prior independent review or earlier audit conclusion has been consulted.

Exact claim under audit: for each fixed x in [1/2,1), full-plane point-weighted normalized periods of L(u,v)=(u,(u^2+1)v) at primes p=3 mod 4 have limsup 1 and liminf at most 23/24, hence no weak limit.

Independent mechanism reconstruction: all nonzero v on a vertical fiber have order ord_p(u^2+1); every proper divisor of p-1 is at most (p-1)/2. Thus at each fixed threshold only primitive multipliers are excluded for p>1/(1-x). A primitive-element character expansion should yield P_p/p=phi(p-1)/(p-1)+o(1), and forced small prime factors yield a totient-ratio subsequence tending to zero. A different subsequence bounded away from zero needs a genuinely unconditional analytic input and residue-class extraction.

Adversarial checks to complete: (1) independently verify the point weighting, p=3 and x=1/2 boundary and strict eventual cutoff; (2) inspect and replay the supplied verifier; (3) independently check the Ramanujan indicator, exceptional quadratic Jacobi sum and total divisor error; (4) recover exact hypotheses and error parameters of the prime-average input, especially no GRH/Artin; (5) ensure the all-prime mean actually implies infinitely many primes in class 3 mod 4 with positive ratio; (6) audit fixed-x quantifiers and weak convergence.

First assessment: no arithmetic contradiction found on paper. The character/Jacobi argument and extraction constants appear internally consistent; source admissibility and the quantifier over the chosen prime set remain a separate interpretive question, not an assumption in the arithmetic theorem. Finite checks alone cannot establish either infinite subsequence.

## 2026-10-21T02:45:49.476124+00:00 — Arithmetic/source checkpoint

Assigned audit completion estimate: **75%**. Independent first checkpoint remains prior to any prior-review reading; prior conclusion documents have still not been consulted. Both supplied standard-library scripts were fully inspected, copied byte-for-byte into this assigned directory, and replayed with Python -E -B. Full finite controls: PASS, 8,347,742 assertions covering 4,148,171 full-plane points at 51 admissible primes through 503. Analytic controls: PASS, 230,780 assertions. Both original snapshot scripts were also attempted and fail at import because SymPy is absent; no installation was attempted. This is a runtime/dependency limitation, not a mathematical counterexample.

Read Menici--Pehlivan equation (1), definition (8), Lemma 2 and complete proof on printed pp.262--263 from the existing full-text reading copy; verified the live institutional PDF and corresponding source text. The relevant lemma is unconditional. Its SW input permits any fixed logarithmic modulus exponent and any fixed error exponent, so K=(log X)^6 and C=4 are compatible. The proof's 1/d weights sum to O(log K); there is no missing log^6 multiplier in the error.

Independently verified original constants 7/24 > 13/48; the residue-class extraction is valid. Boundary probes confirm p=3 has D(3/4)=1 although D(1/2)=5/9, explaining the necessary eventual cutoff. At x=(p-1)/p the CDF equals 1, so no uniform-in-x extension is being assumed.

A distinct continuous-test proof is available: f(t)=max(0,min(1,2t-1)) has integral (1-2/p)(p-1)P_p/p^2 for p=3 mod 4. Its two subsequences contradict weak convergence directly. A separate exact identity T_3(X)=2S_2(X)-S_1(X)+1 (X>=2) plus the same published lemma at m=2 gives conditional class mean A, yielding the optional stronger arithmetic bound liminf D_p(x)<=1-A. This strengthening is recorded separately and is not needed for the original claim.

## 2026-10-21T02:48:42.100744+00:00 — Final arithmetic checkpoint

Assigned audit completion estimate: **100%**. Original arithmetic claim accepted without a mathematical gap. The final added checker passed 2,111 exact controls; supplied replay totals remain 8,347,742 and 230,780, for 8,580,633 final controls. Full derivation, strict-cutoff counterexamples to overstrong variants, independent continuous-test proof, optional class-mean strengthening, source receipts and runtime limitations are recorded in ARITHMETIC_REVIEW.md and VERDICT.json. Reconstructed and hash-checked the initial version of the new checker so its preserved first-run receipt also has a matching source artifact. All 17 immutable original snapshot pins match. No prior review conclusion was consulted, no unrelated agent was contacted, and no Git mutation or external publication was performed. No arithmetic work remains in the assigned audit; historical priority and source interpretation remain outside this verdict.
