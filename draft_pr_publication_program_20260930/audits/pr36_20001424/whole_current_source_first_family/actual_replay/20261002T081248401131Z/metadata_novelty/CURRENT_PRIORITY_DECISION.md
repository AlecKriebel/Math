# PR36: full-target negative answer is an earlier source consequence

2026-10-02 07:31 UTC. Disposition: **PRIOR_APPLICATION; already_solved**.
This is a mathematical and priority decision, not a completed current-packet
acceptance gate. Original substantive attempts **1/5**; new substantive
attempts **0**; verification/priority inspection **0**. No paper, new DOI,
tracker row, or GitHub release is appropriate under the user's process.

## Exact question and success criterion

Numeric source 20001424, AIM-DYNAMICAL_SYSTEMS-0082, is the full question:
“Are all PCF maps defined over their field of moduli?” The recovered official
[AIM Problem 2.6](http://aimpl.org/finitedynamics/2/) has no odd-postcritical-set,
rigidity, degree, or critically-fixed restriction. One algebraic rational
map of degree at least two, with finite forward critical orbit and no model
over its absolute field of moduli, answers it negatively.

The exact source and complete upstream prior are pinned separately and in
the unchanged nested original source_record. Their native source-pair hash is
772b051437b7dbf9ab9eddf38e10981f681b99ac4d83f44fbc886600c5c06270;
literal statement hash is
66ebcc5661f95cab8df379cd71155d75a571bcf1fdd05acbfe1294c92e2d3f03.
The official literal page was actually recovered, HTTP200, 33,521 bytes,
SHA256 990076ea9a8b9a23c9a6a34e6686eda087be82cd616c02d743e996a9c1e7d178.
Earlier failed retrievals remain failed observations in their dated receipts.

## Primary prior source and independent verification

Joseph H. Silverman, *The field of definition for dynamical systems on P1*,
Compositio Mathematica **98** (1995), 269–304, printed p.271 equation (1),
already prints the cubic

\[
 f(z)=i\left(\frac{z-1}{z+1}\right)^3.
\]

The same printed source discusses the odd-degree family and obstruction on
pp.296–297. The [official archive metadata](https://www.numdam.org/item/CM_1995__98_3_269_0/)
establishes the 1995 publication. The actual primary PDF is 3,149,856 bytes,
SHA256 0a405ab1fbe4fc04e73439ecc31db4afaae3d8e38ce58bfd49f65442c6e88116.
Root visually checked the formula on printed pp.271 and296, because extracted
text omits mathematical glyphs, and read the operative descent statements.
Two distinct closed priority families and an independent source-first child
verified the implication below. Their exact reading/exposure scopes,
retrieval failures, corrected real-phase controls, and version boundaries
remain in their frozen ledgers. Root reconstructed the argument separately.

The source prints the formula, moduli field and descent obstruction. It does
not label the displayed family PCF or identify AIM Problem2.6. The PCF property
is the exact elementary source consequence proved here; this audit does not
claim earliest worldwide recognition of that consequence.

## Complete elementary certificate for the cubic

In homogeneous coordinates the map is
[i(X−Y)^3:(X+Y)^3]. These cubics have no common zero on P1, so the degree is
exactly3 and coefficients are algebraic over Q. The critical points are
exactly1 and−1, each with local degree3 and ramification multiplicity2.
On finite points away from the pole,
f'(z)=6i(z−1)^2/(z+1)^4. At infinity the local source chart w=1/z gives
f(1/w)=i((1−w)/(1+w))^3 with derivative−6i at w=0, so infinity is not critical.
At−1, the reciprocal target chart has a zero of order3. This accounts for
all ramification, 4=2·3−2, including both exceptional charts.

Direct exact evaluation, with the projective value at infinity, gives

\[
1\longmapsto0\longmapsto-i\longmapsto-1\longmapsto
\infty\longmapsto i\longmapsto1.
\]

Thus the map is PCF. The reduced postcritical set has six elements; the
earlier sufficient descent criterion requiring an odd invariant divisor
does not apply to this portrait. No numerical approximation or generic
hyperbolic-center assumption is involved.

Every holomorphic Möbius map commuting with f permutes its critical pair
{1,−1} and their critical values {0,infinity}, compatibly. If it fixes both
critical points, it also fixes both critical values and is identity. If it
swaps the critical points, it swaps0 and infinity and has the form λ/z.
The image of1 forces λ=−1. This sole candidate T(z)=−1/z fails to commute:
Tf(0)=−i whereas fT(0)=f(infinity)=i. Hence Aut(f) is trivial.

Coefficient conjugation satisfies fbar=T f T^{-1}; this can also be checked
as an exact homogeneous polynomial identity, without choosing sample points.
All absolute Galois automorphisms fixing i fix f, and all others take it to
fbar, which is Qbar-conjugate to f by this rational T. Consequently the
absolute class stabilizer is all Gal(Qbar/Q), and the absolute field of
moduli is exactly Q, not merely a real subfield inferred from a finite test.

Let c(z)=conjugate(z). The antiholomorphic Möbius involution A=T c commutes
with f. It has no fixed point: at finite nonzero z its fixed-point equation
is |z|^2=−1; it exchanges0 and infinity. Any other commuting antiholomorphic
Möbius map, composed with A^{-1}, is a holomorphic automorphism of f and thus
identity. A is therefore the unique antiholomorphic dynamical symmetry.

If any complex Möbius conjugate of f had real coefficients, pulling back
ordinary conjugation would give a commuting antiholomorphic involution with
a nonempty fixed circle. Uniqueness forces that involution to be A, which
has no fixed point, a contradiction. No real model exists, and hence no
model over Q exists. This proves every part of the literal counterexample.

For the printed odd exponents d≥3 the same proof works with ramification
2d−2, derivative2di(z−1)^{d−1}/(z+1)^{d+1}, and infinity derivative−2di.
The residues d mod4 give the six-cycle when d≡3 and two three-cycles when
d≡1. The cubic alone suffices; finite tested degrees are reproducibility
controls and do not replace this general deduction.

## Original PR36 result and bounded priority conclusions

The original degree11 critically-fixed graph construction is mathematically
supported by the independent graph, algebra/descent and source-scope families.
Root checked realization hypotheses, intrinsic symmetry naturality,
equivariant face-arc selection, trivial holomorphic centralizer, algebraicity
of the finite normalized constructible locus, and real-model obstruction.
All sixteen original Git files, their two exact executable receipts, the
original1/5 ledger, and the complete17-path diff are preserved. Its exact
coefficients and exact moduli field were not computed and are unnecessary
for that existence proof. The graph proof is separate supporting evidence.

The universal negative answer already follows from the printed1995 map, so
the original new-resolution framing cannot remain current. Priority of the
particular degree11 graph construction, earliest explicit PCF attribution,
and minimum possible degree are not established by this bounded audit.
Neither a still-listed AIM question nor an unlocated exact earlier graph
proves novelty. The withdrawn arXiv:2405.03612 characterization is excluded;
later-version results are not backdated to earlier deposits. Additional
BBM/Hidalgo–Quispe/Milnor leads are corroboration, not substitutes for the
decisive explicit old cubic.

Acceptable eventual disposition is a credited already_solved partial-findings
merge, after a NEW whole-current-packet adversary and root reproduction pass.
This note does not transfer an older verdict to that gate. Extensive AI use
is unrefereed; no external human peer review or formal proof-assistant
certification is claimed. No outside individual was contacted.
