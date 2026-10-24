# Fresh adversarial audit of the algebraic-cover filter

Completed 2026-10-24 20:32 UTC. Review-task completion estimate: **100%**.
The underlying full Kourovka 21.128 problem remains **unsolved**; the author's
8% estimate is not promoted by this review.

## Verdict and exact scope

**PASS for the bounded theorem as stated. No outstanding substantive
mathematical objection was found.** For the particular projectivized
reflection-arrangement complements

\[
U_T=\mathbb P^3_{\mathbb C}\setminus\bigcup_{H\in\mathcal A_T}\mathbb P(H),
\qquad T=F_4,H_4,
\]

there is no single connected smooth complex algebraic variety with finite
étale surjective algebraic morphisms to both complements. The argument does
**not** prove that their fundamental groups, pure Artin groups, or full Artin
groups are abstractly noncommensurable. There is no claim of originality,
human review, formal verification, or a solution of 21.128 in this verdict.

The seven files in `common_cover/FROZEN_MANIFEST.json` were hash-checked before
and after reproduction. The frozen input receipt, exact independent output,
full author replay, comparison receipt, and primary-source provenance are
preserved alongside this report. No author file was edited.

## 1. Primary theorem and the connectedness hypothesis

I read the actual primary text of Tevelev, *Compactifications of subvarieties
of tori*, arXiv math/0412329v3, Theorems 1.4 and 1.5 and the last paragraph of
§4. I separately obtained the published author-hosted version, *American
Journal of Mathematics* 129 (2007), 1087–1104. The relevant all-flat paragraph
is on published p.1097, after Example 4.1. It identifies the all-intersections
model as the maximal nested-set compactification; its morphism to the visible
contour is log crepant, and its log divisor is globally generated. Theorem
1.5 supplies the ample log divisor on the latter model. The morphism is
birational since it is the identity on the complement, so its pullback is
nef **and big**. Merely citing global generation would not by itself prove
bigness; here that additional step is supplied.

I also read Hacking–Keel–Tevelev, *Compactification of the moduli space of
hyperplane arrangements*, §2, assumption preceding Lemma 2.1 and Theorem
2.2. Its connectedness assumption is explicitly connectedness of the
represented matroid, equivalently finiteness of the projective stabilizer.
This removes possible ambiguity in Tevelev's abbreviated parenthetical
description of projective automorphisms. Nontrivial finite reflection-group
symmetries do not disqualify these arrangements.

Essentiality is immediate from four independent simple normals. Matroid
connectedness was independently certified by fundamental circuits relative
to the simple-root basis: roots supported on consecutive pairs connect all
four basis elements. A nontrivial direct sum of a represented matroid would
partition a basis and forbid any circuit meeting both parts. Thus the
connected support graph is a sufficient certificate. The reproduction checks
this graph for all four tested arrangements.

Primary copies and hashes are in `SOURCE_PROVENANCE.json`. The external
results needed here are the stated compactification theorems and standard
birational/toroidal facts; no group rigidity theorem is being imported.

## 2. Finite étale covers and boundary ramification

This was the main potential hidden assumption. A finite étale map of open
varieties can ramify at the compactification boundary; forgetting the
reduced boundary or applying the ordinary canonical-divisor formula would
invalidate the argument. The frozen proof correctly keeps this boundary.

Here is a more explicit justification in the precise setting needed. Let
\((X,D)\) be the smooth all-flat compactification of one complement, and let
\(L=K_X+D\), which is a nef and big Cartier divisor by §1. Let
\(f:V\to U\) be any connected finite étale algebraic cover of degree \(e\).
Normalize \(X\) in \(\mathbb C(V)\), obtaining a finite projective map
\(\bar f:X'\to X\), and put \(E=(\bar f^{-1}D)_{\mathrm{red}}\).
There is no ramification away from \(D\).

Locally near a point where \(r\) boundary components meet, the punctured
complex analytic chart is
\((\Delta^*)^r\times\Delta^{3-r}\). Each component of its finite cover
corresponds to a finite-index sublattice of \(\mathbb Z^r\). Normalization
adds the same positive cone in the enlarged lattice, which is a toroidal
local model. In characteristic zero there is no wild ramification. In these
charts a logarithmic top differential pulls back to a nonzero constant
multiple of a logarithmic top differential, and therefore

\[
K_{X'}+E=\bar f^*(K_X+D)
\]

as logarithmic Cartier divisors. Equivalently, on a boundary prime with
ramification index \(a\), the ordinary ramification contribution \(a-1\)
is exactly cancelled by replacing \(aE\) with the reduced \(E\).
The local toroidal description is the SNC case of Abhyankar's lemma.

Choose a projective toroidal resolution \(g:Z\to X'\), retaining the full
reduced boundary \(D_Z=Z\setminus V\). A toroidal subdivision is log
crepant, so

\[
K_Z+D_Z=g^*\bar f^*L.
\]

The right side is nef and big. Applying the projection formula first to the
birational \(g\), then to the finite degree-\(e\) map \(\bar f\), gives

\[
\operatorname{logvol}(V)=(K_Z+D_Z)^3=eL^3.
\]

No assertion that \(V\) is itself an arrangement complement occurs here.
Both normalization and resolution leave \(V\) unchanged. A variety finite
over the affine complement is automatically quasi-projective, so the
compactification construction applies to every alleged common cover in the
claim.

The log volume is intrinsic to the open smooth variety. One can see the
independence on a common SNC resolution: the difference between a pulled-back
log divisor and the new log divisor is effective exceptional. For a
boundary-adapted blowup in a codimension-\(c\) center lying in \(r\)
components, it is \((c-r)E\), with \(c\ge r\). Adding such an exceptional
divisor does not change section-growth volume. Consequently the two maps
from a single algebraic \(V\) really do compute the same log volume, even
when the two compactifications differ.

Topological Euler characteristic multiplies by \(e\) under this finite
cover. Finite arrangement-complement CW models suffice; equivalently one
can use algebraic Euler characteristic and its agreement with ordinary
Euler characteristic for smooth complex varieties. Connectedness makes
the degrees positive constants, and both base Euler characteristics are
nonzero. Thus the ratio comparison is legitimate.

## 3. Re-derived blowup formula, including the signs

For a point blowup of a smooth threefold, the canonical discrepancy is
\(2E\); the reduced total transform of \(m\) planes adds \((1-m)E\).
The logarithmic change is therefore \((3-m)E\). Pulled-back divisor cross
terms vanish and \(E^3=1\), giving the author's point correction.

After all rank-three flats have been blown up, the strict transforms of
distinct arrangement lines are disjoint. Any meeting point of two original
lines is a rank-three flat and has already been blown up; their tangent
directions at that point are distinct. The log divisor has degree

\[
d_L=(N-4)+\sum_{P\in L}(3-m_P).
\]

The strict transform of a line is still \(\mathbb P^1\). Its anticanonical
degree is \(4-2p_L\), so adjunction gives
\(\deg N_{L/X}=2-2p_L\). Each subsequent line blowup changes the log
divisor by \(a_LE_L\), with \(a_L=2-m_L\).

Using the convention \(E=\mathbb P(N_{L/X})\) for the exceptional divisor,
the pushforward rules are
\(\pi_*E=0\), \(\pi_*E^2=-[L]\),
\(\int E^3=-\deg N_{L/X}\). Hence

\[
(\pi^*B+a_LE)^3-B^3=-3a_L^2d_L-a_L^3\deg N_{L/X}.
\]

The negative sign in \(E^3\) is essential and is correct in the frozen code.
Blowing up a plain line in \(\mathbb P^3\) gives \(E^3=-2\), a simple sign
control. Multiplicity-two lines have \(a_L=0\); rank-three ordinary triple
points have zero point correction. Their inclusion is harmless.

## 4. Distinct exact computational reproduction

`reproduce_cartan.py` does not import the author's code or root list. It
generates entire root orbits from simple-reflection Cartan matrices with
chains 3–4–3, 5–3–3, 3–3–3, and 3–3–4. Arithmetic is in
\(\mathbb Q(\sqrt5)\), represented by integer triples
\((a,b,d)\mapsto(a+b\sqrt5)/d\), normalized by integer gcd. Thus both the
input construction and the field implementation differ from the frozen
coordinate/\(\mathbb Q(\phi)\) program. All simple-reflection pair orders
are checked exactly, including first return, not just a suitable power.

Rank-two and rank-three flats are obtained by reduced Gaussian elimination,
not Plücker wedges or minors. Closure against every normal, completeness
of pair/triple basis accounting, and connectedness are checked. The output
retains every generated root line and every flat. Cubes are calculated both
by transformed-line corrections and by an independently expanded sum over
point-line flags. Euler characteristics follow from Möbius recursion; the
resulting characteristic polynomials also factor as the expected four
linear factors. No approximate rank or equality test occurs.

| Type | Root lines | Rank-two flats | Rank-three flats | Log volume | Euler characteristic |
|---|---:|---:|---:|---:|---:|
| F4 | 24 | 122 | 120 | 2496 | −240 |
| H4 | 60 | 722 | 1320 | 51660 | −5040 |
| A4 | 10 | 25 | 15 | 61 | −6 |
| B4 | 16 | 58 | 40 | 488 | −48 |

In addition to the aggregate totals, `compare_outputs.py` verifies every
point/line incidence profile and every transformed-line cube-term profile
against frozen data for all four types. For H4 the multiplicity-six points
split into 300 points with local line multiplicities \(2^3,3^4\) and 360
with \(2^5,5^1\); both contributions are present. The author program was
also rerun directly: every saved field matched its frozen counterpart
apart from elapsed time.

Useful hand-checkable volume summaries are

\[
\begin{aligned}
F_4:\quad &20^3-5280-224=2496,\\
H_4:\quad &56^3-122100-3800+1944=51660.
\end{aligned}
\]

The two normalized ratios are \(52/5\) and \(41/4\), with difference
\(3/20\). These exact arithmetic conclusions are independently reproduced,
not inferred solely from the author's assertions.

## 5. Positive controls and boundary cases

The map \([x_1:\cdots:x_4]\mapsto[x_1^2:\cdots:x_4^2]\) is a finite
projective morphism. The inverse image of the A4 arrangement in the
coordinates with a fifth configuration point fixed at zero is exactly the
B4 arrangement. Its restriction is therefore finite, and the coordinate
torus derivative is nonsingular. The projective squaring kernel has size
\(2^4/2=8\), so this restriction is a connected degree-eight finite étale
cover. The independently reproduced volumes and Euler characteristics
scale by exactly eight. This is a genuine algebraic cover, rather than
an appeal to abstract commensurability.

The analogous rank-three cover has degree four. The frozen integer
rank-three calculation is consistent with volumes 5 and 20 and Euler
characteristics 2 and 8. In rank two, the divisor degree \(N-2\) is correct;
at \(N=2\) it is zero and is not big. The latter is only a boundary control,
not an application of the connected log-general-type theorem.

## 6. Exact obstruction still remaining for Kourovka 21.128

If the Artin groups were abstractly commensurable, one obtains isomorphic
finite-index subgroups and, for the projective pure quotients, covers with
isomorphic fundamental groups. This supplies no algebraic isomorphism
between those covers and no common algebraic variety covering both bases.
Neither Tevelev's theorem nor the logarithmic calculation provides such
recognition. The gap is a missing rigidity theorem, not an arithmetic error
that this review can remove. Any elevation to a negative answer to the
original group problem would be unsupported.

This review was conducted by a fresh AI subagent that did not author the
candidate argument. Its checks remain proofs and reproducible exact
computations, not a claim of independent human peer review or first priority.

## Reproduction

From the repository root, with Python 3 and its standard library:

```text
python3 kourovka_descending_20261017/problems/21_128/common_cover/compute_log_volume.py --type both --output kourovka_descending_20261017/problems/21_128/algebraic_cover_adversary/author_reproduction.json
python3 kourovka_descending_20261017/problems/21_128/algebraic_cover_adversary/reproduce_cartan.py --types F4,H4,A4,B4 --output kourovka_descending_20261017/problems/21_128/algebraic_cover_adversary/cartan_reproduction.json
python3 kourovka_descending_20261017/problems/21_128/algebraic_cover_adversary/compare_outputs.py
```

The comparison also rechecks the frozen input hashes and fails if any input
has changed. Runtime for the independent four-type calculation was about
nine seconds on the review host; no time limit or incomplete search is used.
