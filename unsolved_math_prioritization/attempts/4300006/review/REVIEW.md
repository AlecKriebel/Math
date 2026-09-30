# Independent review: the local p-adic entropy normalization

**Verdict: PASS_COMPLETE_SCOPED_CONJUGACY_OBSTRUCTION.** No mandatory correction was found. The proposed logarithmic normalization is incompatible with topological-conjugacy invariance on the stated local multiplication maps, for every prime. Ward's broader entropy/period question remains outside that precise contradiction. Recommended campaign status: **unsolved, 1/5 substantive approaches**, with the complete scoped obstruction recorded. This is an adversarial AI review, not human peer review or a priority finding.

Reviewed artifact: `OBSTRUCTION.md`, SHA-256 `35bdf5f9f59b1b8b573644351c32e01659e1b258fdea06d9e79cef9f35b127bc`. The artifact remained unchanged during review.

## 1. Exact original question

I read Problem F and its update on pp.2–4 of [Ward, Six Problems in Algebraic Dynamics, updated December 2006](https://www.imath.kiev.ua/~skolyada/kevin.pdf), and inspected the rendered p.3. The text first asks about p-adically valued entropy and Mahler measures in a broader motivic program. Its specific local example uses multiplication on Q_p and the logarithm branch normalized by log_p(p)=0. Topological-conjugacy invariance is expressly proposed as an example of a desirable property, rather than as an exhaustive definition of every possible entropy-like notion.

The submitted theorem therefore addresses a genuine and exact conjunction of source requirements. It cannot justify a blanket impossibility statement for all unspecified versions of the broader program. The artifact preserves this distinction and correctly restricts the scalar to Q_p^× when it is to define an automorphism of Q_p.

## 2. The isometric conjugacy is valid for both valuation signs

Let the two multipliers have the same nonzero valuation a, and let u be their ratio, a unit. The exponent floor(v_p(x)/a) is an integer for every nonzero x. Its defining identity after multiplying x by the first scalar is simply floor(r+1)=floor(r)+1. This works for negative a, with no reversal or truncation convention required.

The proposed map preserves valuation and maps each valuation shell bijectively to itself. Its displayed inverse is correct because the output remains on the same shell. For two points on one shell, their difference is multiplied by the same unit. For points on different shells, the ultrametric equality gives the distance as the larger of their two norms before and after the map. The case involving zero follows directly from norm preservation. Thus the map is a surjective isometry of the whole space, including continuity at zero and of the inverse. The intertwining identity follows exactly and proves topological conjugacy.

Haar preservation also follows: each Borel shell piece is transformed by a fixed unit, and the shells plus the zero point partition Q_p countably. Alternatively, a surjective isometry fixing zero carries every ball onto a ball of the same radius, consistent with the normalized additive Haar measure. This assertion concerns the conjugating map; it does not assert that the contracting or expanding multiplication maps preserve Haar measure.

No result about valuation-zero multipliers is needed or asserted. Their dynamics need not share the shell-shift mechanism.

## 3. The logarithmic contradiction includes p=2

For u=1+p², the first logarithmic series term has valuation two. Every later term has valuation 2n−v_p(n)≥n+1≥3, and these valuations tend to infinity. Hence the convergent tail lies in p³Z_p, while the first term does not. The logarithm has valuation exactly two. In particular this proof works unchanged at p=2; replacing p² by p would not justify the same uniform leading-term argument.

Multiplication by p and by p(1+p²) is covered by the conjugacy lemma. Their prescribed normalized logarithms are respectively zero and the nonzero logarithm just computed. Taking inverses preserves the same conjugacy and changes both logarithms' signs, so the expanding-only restriction also remains contradictory. No injectivity assumption on the full p-adic logarithm is used.

The nonadditivity witness is correct, including p=2: both 1 and p−1 lie on the unit shell, while their sum p lies on a different shell. Continuous additive automorphisms of Q_p are precisely nonzero scalar multiplications, by rational linearity and continuity along the dense rational subfield. Consequently the stricter additive-conjugacy category does not identify distinct multipliers. The artifact correctly distinguishes this restriction from an entropy construction with further axioms.

## 4. Periodic entropy and compact systems do not conflict with the obstruction

I checked the full relevant introduction of [Deninger's arXiv:math/0608539v2](https://arxiv.org/abs/math/0608539), equations (1.2)–(1.6), Theorem 1.1, and the finite fixed-point formula in Proposition 2.1. The periodic-entropy definition is explicitly for an action on a set; compactness is not required merely to write this definition. Every positive iterate of either local scalar map has just the fixed point zero, because a nonzero valuation precludes a root of unity. Their finite fixed-point counts are all one, so the periodic logarithmic limit is zero. This remains true for every admissible subgroup sequence.

Deninger's Mahler-measure theorem concerns the different compact algebraic system dual to the integer Laurent-polynomial quotient. For f(t)=pt−(1+p²), the unique root has p-adic norm p and hence lies outside the unit torus. The nonvanishing hypothesis holds. Equation (1.6) gives precisely log_p(1+p²), since log_p(p)=0. The compact example therefore has the stated nonzero periodic entropy, without contradicting the local maps' zero periodic counts.

There is an additional independent check of this concrete comparison. Put u=1+p². The n-periodic configurations in the compact system are the kernel of the integer torus endomorphism pS_n−uI, where S_n is the cyclic shift. Its determinant has absolute value u^n−p^n. Thus its normalized p-adic logarithm is

$$
\frac1n\log_p(u^n-p^n)
 =\log_p u+\frac1n\log_p\bigl(1-(p/u)^n\bigr).
$$
For n≥2, the last logarithm has valuation n, including at p=2; its normalized remainder has valuation n−v_p(n), which tends to infinity. This independently verifies the claimed limit for this particular compact system. The determinant identity and finite leading-term controls are reproduced in the independent checker. This check does not substitute for a re-proof of Deninger's general theorem.

I also read the relevant portions of the full published [Katagiri paper, Kodai Mathematical Journal 44 (2021), 323–333](https://doi.org/10.2996/kmj44207). Definition 1.1 uses coprime-to-p indices, Theorem 2.2 concerns compact Laurent-module duals, Corollary 2.3 incorporates a number-field norm, and Theorem 1.3 imposes a finite set of primes and explicit non-unit eigenvalue hypotheses for the selected solenoids. None identifies local Q_p multiplication with one of these compact systems. The difference between Katagiri's simplified index sequence and Deninger's stronger formulation does not affect either the local zero-count argument or this concrete compact limit.

The full Besser–Deninger 1999 paper and the final typeset Deninger chapter were not independently retrieved for this review. The cited Jensen formula was checked in the complete Deninger preprint actually used. No claim to have audited the full motivic interpretation or every published dependency is made.

## 5. Exact reproduction and disposition

All **122,334 submitted assertions** replayed with a byte-identical receipt. The independent checker passed **4,560 exact assertions**. It constructs orbit representatives by repeated scalar operations rather than by copying the submitted floor implementation, and checks reconstruction, inverse, intertwining, metric preservation, both valuation signs, logarithmic leading valuations, nonadditivity, and compact periodic-point determinants.

From this directory:

```sh
python author_replay/verify.py
python independent_checks.py
```

The submitted checker uses standard-library Python; the independent checker additionally uses SymPy for exact integer determinants. Both regenerate deterministic receipts. Finite checks supplement the universal all-prime proof; they are not used as a proof of continuity, Haar preservation, or convergence of an infinite series.

The exact two-axiom formulation is disproved completely. The broader source leaves its axioms open and already credits a different successful algebraic-periodic framework. Retain the scoped negative conclusion, the broader unresolved classification, and the absence of a novelty claim.
