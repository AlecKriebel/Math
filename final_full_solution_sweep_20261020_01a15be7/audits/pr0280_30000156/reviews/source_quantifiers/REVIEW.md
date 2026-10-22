# PR 280: independent source and quantifier adversary

Head reviewed: `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`.
Proof SHA-256: `ba5fc8850a665da5130e3791fb49015c998ed0eee317576712ad3b66bc228c05`.
Assigned audit completion: **100%**. No candidate file was edited.

**Verdict: the candidate covers the exact imported question and the literal universal statement in the original contribution. No source-scope repair is required.** I found no counterexample to its finite dynamics, interval of CDF failures, or weak-limit conclusion. A direct continuous test function supplies an independent proof of the latter. Historical novelty, publication status, and the final promotion decision are separate from this assigned audit.

## Primary source, read before prior verdicts

I read `original/PROOF.md` first, then the complete two-page primary contribution, and saved an independent checkpoint before comparing old reviews. Both printed pages were visually inspected. The institutional PDF and author PDF hashes agree with the previously recorded primary-source hashes; their contents were read directly, rather than inferred from those receipts. The exact imported statement was then read and independently hashed.

The source is Vivaldi, joint work with Roberts, *Maps over finite fields: integrability and reversibility*, OWR 54/2004, printed pp.2944-2945, [institutional report](https://publications.mfo.de/bitstream/handle/mfo/2873/OWR_2004_54.pdf?isAllowed=y&sequence=1); also [author version](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf). Its displayed statistic weights affine points by `p^-2`, uses threshold `px`, and takes an ordinary limit. Its universal sentence is: “The limit (1) exists for any bi-rational map L.” Algebraic integrability is defined using rational map, inverse, and invariant. The exposition permits genus at most one; genus one appears in the later heuristic. Coefficient reduction uses a fixed extension degree and suitable positive-density primes, before specializing to `q=p`. The single-reversing-family condition belongs to a separate refinement. A later conjecture changes both scale and prime averaging. None of these passages adds polynomial inverse, constant Jacobian, elliptic-only fibers, genericity, or a density-one exception to the universal sentence.

The imported question's SHA-256 is `d35548befccb38900fe4d2c6574ef4e42574050421b200153694adfc4f47d587`. It asks the same unrestricted birational-map existence question.

## Adversarial source-fit checks

**Birationality.** With `a(u)=u^2+1`, the two rational formulas `(u,a(u)v)` and `(u,v/a(u))` compose to the identity on the dense open set `a(u) != 0`. Thus the proposed fixed map is birational over Q. Its forward map is polynomial. Over C it contracts the two lines `u=+i,-i`, and its inverse is not polynomial. That last fact is real but does not violate the class being audited. A polynomial-automorphism restriction would pose a different question.

**Integrability and order.** `I=u` is a nonconstant rational invariant. The generic fiber is an affine line with genus-zero projective completion. The mth iterate is `(u,a(u)^m v)`, which is never the identity rational map for positive m. These are checkable algebraic facts and satisfy the stated integrability definition. The descriptive discussion of bounded level sets does not constrain these unbounded fibers. If desired, even an implicit rational area-preservation concern has a direct check: on `v != 0`, the map preserves `du wedge dv/v`. No unmentioned regular symplectic form is assumed.

**Good reduction and all points.** For every `p=3 mod 4`, `-1` is nonsquare. Consequently `a(u)` is nonzero for every field parameter, so both displayed directions are defined on all `p^2` affine points and are mutually inverse permutations. The invariant remains nonconstant, and the map's degrees remain unchanged. No point, exceptional line, or transient is removed from the probability space. The polynomial forward map requires no appeal to projective points. Adding or removing the `p+1` points at infinity in a separately defined completion would change bounded statistics by `O(1/p)` and could not repair the exhibited fixed gap, but no such completion is used here.

**Prime quantifier.** The class `S={p:p=3 mod 4}` is fixed in advance, has prime density 1/2, and is a Frobenius class for Q(i). It is selected by the denominator's algebraic nonvanishing, before any period is observed. Both incompatible prime sequences are contained in this same class. For Q coefficients the natural reduction set is all primes up to harmless finite exclusions; convergence on that set would imply convergence on S. Therefore the candidate's nonconvergence on S disproves the exact imported all-prime limit regardless of how the other primes' exceptional points are treated. Alternatively, S itself supplies a clean positive-density reduction family with an everywhere-defined finite inverse.

The informal reduction paragraph does not formalize every conceivable choice of prime subcollection. This audit does **not** attribute the following stronger assertion to the candidate: failure of convergence on every arbitrary or dynamics-tailored positive-density subset. Such an existential-refinement question is different from the audited ordinary-limit question. The counterexample does, however, survive deleting a density-zero set: the independent positive-density strengthening in `DERIVATIONS.md` proves this explicitly.

**Fixed extension degree.** The construction uses the fixed permitted degree `n=1`, hence `q=p`. A universal claim allowing this degree is refuted by one example at this degree. Nothing here purports to establish the same full-permutation theorem for every extension degree; for example, even extension degrees over these odd primes make `-1` a square.

## Independent mathematical checks relevant to coverage

For `v=0` the period is one. For `v!=0` the period is exactly the multiplicative order of `a(u)`, which divides `N=p-1`. Every proper divisor of N is at most `N/2 < p/2`. For fixed `1/2<=x<1`, the inequality `N>px` holds once `p>1/(1-x)`. Precisely the primitive-parameter fibers are then excluded. Each such parameter contributes exactly `p-1` excluded points, giving

`D_p(x) = 1 - (p-1) P_p / p^2`.

This is the required point count. The horizontal fixed line and vertical fixed line at `u=0` give exactly `2p-1` fixed points, which is an independent geometric check on the boundary accounting. Full divisor fixed-point counts and their Mobius inversions supply another independent diagnostic in `DERIVATIONS.md`.

I checked the character argument algebraically: the primitive-element indicator has the correct factor `phi(N)/N`, all `u^2+1` values are nonzero on S, the quadratic change of variables gives the stated Jacobi sum, and its exceptional quadratic-character case has modulus one. The square-root estimate and `2^omega(N)<=64 N^(1/4)` imply the claimed vanishing error. The truncation of the prime-totient mean is valid assuming the stated standard Siegel-Walfisz theorem: the tail is `O(X/(log X)^6)`, the small-modulus error is `o(X/log X)`, and the Euler product converges absolutely. The subsequent mod-4 average split and CRT/Dirichlet sequence give the two claimed incompatible ranges. I did not independently reread the complete Menici-Pehlivan paper in this role; full published dependency custody belongs to the separate analytic audit.

The finite formula is eventually uniform in the sense needed for every **fixed** x in the interval; no moving-threshold interchange is made. At `x=1/2` the proper divisors are already included. At `x=1`, every point is included. At the moving boundary `x=(p-1)/p`, the maximal periods are included as well, so the primitive-fiber exclusion formula is not asserted there. `D_p(0)=0`. A small-prime failure of the eventual condition, such as p=3 at x=3/4, is harmless and was tested rather than suppressed.

**Weak convergence.** The candidate's countability-of-discontinuities argument is correct because failure occurs throughout an interval. An even more direct check uses the bounded continuous function

`h(t)=0` for `t<=1/2`, `h(t)=2t-1` for `1/2<t<1`, and `h(t)=1` for `t>=1`.

All proper-divisor periods contribute zero, whereas maximal periods contribute `1-2/p`. Hence its expectation is exactly

`(1-2/p)(p-1)P_p/p^2 = phi(p-1)/(p-1)+o(1)`.

The two proven arithmetic subsequences force this bounded continuous expectation to approach zero along one sequence and stay at least `1/24-o(1)` along another. Weak convergence is therefore impossible, without any choice of CDF convention or disputed jump point.

## Reproducibility, later scope comparisons, and exact gap

`independent_diagnostics.py` passed with exact rational arithmetic for all **87** primes `p<=1000` in S. It checked eight full affine orbit graphs, six `p=1 mod 4` nonpermutation controls, divisor/geometric identities, Mobius recovery, fixed-point counts, endpoints, the eventual CDF formula, and the continuous-test moment. These computations certify finite identities only; the infinite subsequences rest on the written arithmetic deductions.

Only after the independent checkpoint and diagnostics did I compare earlier source reviews. Their conclusions agree, including their express qualification about arbitrary prime refinements. This agreement is not used as evidence for the proof.

I also independently read the available primary author texts for the nearby scope comparisons: Jogia-Roberts-Vivaldi (2006), full finite-field section 4.2, distinguishes a fixed elliptic orbit from sampling periodic points over elliptic foliations; Roberts-Vivaldi (2009), introduction and Theorems A/B, proves ensemble expectations for random pairs of involutions. The latter even gives a rational finite permutation restricted to `p=3 mod 4` by the same type of denominator condition. Neither result substitutes a fixed-map, prime-by-prime theorem for the audited question. Source filenames, hashes, and read scopes are pinned separately; no final publisher-version access or comprehensive historical-priority search is claimed here.

**Strongest verified assigned result:** the written counterexample has the exact point measure, scale, fixed field degree, birational class, and full finite phase space needed to negate the complete literal original existence question; the weak-limit corollary is independently certified. **Exact remaining assigned gap:** none. Final theorem dependency certification and historical novelty remain separate project gates. No Git, candidate PR, Sheets, Zenodo, external messaging, or unrelated-agent action was taken.
