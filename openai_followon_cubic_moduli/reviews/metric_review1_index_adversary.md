# Independent adversarial check of Theorem 1

Checked 2026-10-07 06:00 UTC. Scope: `main.tex` lines 92–215, SHA256
`de80fb7f84555b632956f21ed8e6e0d1ae6b32da010ee6a89b69a72eb3cf8193`.
This review sought a falsification, independently of the favorable earlier
reviews. **No blocking error or counterexample found.** Completion of this
scoped check: 100%; this is not a certification of the external theorems or a
novelty assessment.

## Primary evidence actually inspected

- [Druel–Guenancia–Păun, published PDF](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.612.pdf): Theorem A, journal p.94; Definitions 1–2, p.96; Remark 3, p.97; Theorem 6, pp.101–102; Section 5 and Claim 28, pp.115–116. No local DGP source was present in `reproducibility/tmp` at initial inspection, so I read the publisher PDF directly. Its Theorem A supplies exactly the stable-factor quasi-étale product used here, without a Q-factoriality hypothesis. Definition 2 matches the bounded-potential weak KE hypothesis. Remark 3 explicitly ensures pullback KE metrics on finite quasi-étale covers.
- [Hacon, Math 7800 primary notes](https://www.math.utah.edu/~hacon/7800/Math7800-2018.pdf), Theorem 2.22, pp.10–11: the stated vanishing applies to projective klt pairs and a Cartier divisor whose difference from the log canonical divisor is nef and big.
- [Stacks, Lemma 33.45.1 / 0BEM](https://stacks.math.columbia.edu/tag/0BEM): Euler characteristic is polynomial for all integral twists, rather than only large positive twists.
- [Serre, GAGA primary PDF](https://aif.centre-mersenne.org/item/10.5802/aif.59.pdf), Theorem 2, p.19, and its proof, pp.22–23: analytic homomorphisms of coherent algebraic sheaves on a projective variety algebraize uniquely. Smoothness is not imposed.

## Attacks and checkable conclusions

**Actual Cartier root on factors.** Restrict the pulled-back line bundle to
`Z × {b}`, with `b` regular in the complementary product. On `Z_reg` the
product canonical formula gives `ω_Z^{-1} ≅ A^r`, after choosing a nonzero
vector in the fixed complementary determinant line. Both sides extend
reflexively across `Z_sing`, so the identity holds globally. This reasoning
does not restrict a noninvertible canonical sheaf along the singular fiber.
The factor is klt: a product with a smooth neighborhood of `b` has precisely
the factor's discrepancies. It applies to any normal connected algebraic
product cover, not just DGP's isometric product.

**Negative roots and the strict bound.** For each `1 ≤ j ≤ r−1`, the Cartier
divisor `N=−jA` has `N−K_Z=(r−j)A` ample, so higher cohomology vanishes.
Negative ampleness gives no global sections on a positive-dimensional
projective integral variety. Thus `χ(Z,A^{-j})=0`. The Hilbert polynomial
has leading coefficient `A^d/d!>0` and degree `d`; its `r−1` distinct roots
give `d≥r−1`. Two positive-dimensional factors contradict
`m<2(r−1)`. No smooth Riemann–Roch formula or Q-Cartier substitute for `A`
is needed.

**Stability descent without Q-factoriality.** Shrink to a smooth big open
`U⊂X` over which the cover is étale and `F` and `T_X/F` are bundles. Its
inverse image is big because the map is finite. Saturation upstairs agrees
with the bundle pullback there and makes no codimension-one correction.
Choose a general complete-intersection curve of `m−1` divisors in `|kH|`,
`H=−K_X`, disjoint from `X\U`; this is possible by the dimension estimate
for a codimension-two closed set and Bertini. The determinant degree on
this curve computes `k^{m−1} c_1(F)·H^{m−1}` even when its global
determinant is only a Weil divisor. The inverse image curve has class
`(k f^*H)^{m−1}`; degrees on it are multiplied by the cover degree.
Disconnected inverse images pose no problem: sum the degrees on all
components. Cancelling `k^{m−1}` proves the manuscript's slope formulas.
The case `m=1` is ordinary étale pullback on a smooth curve. An independent
subagent separately checked the same lemma and found no Q-factoriality
obstruction.

**Arbitrary normal connected covers.** Such a finite cover is projective;
quasi-étaleness makes it crepant and klt. The Cartier root remains
`f^*L`, and the dimension remains `m`. DGP Remark 3 supplies the weak KE
pullback. Thus the already-proved argument can be rerun there; this is not
an assertion that arbitrary étale pullback of an arbitrary stable sheaf
remains stable. Here the index hypothesis excludes the possible splitting
on each cover. The product prohibition also follows directly from the
factor restriction and polynomial argument. Reading “cover” as a normal
connected variety is the conventional interpretation; explicitly adding
these words would remove an avoidable wording ambiguity.

**Positive Ricci and extension.** Since `I` is orthogonal, `η(u,v)=g(Iu,v)`
is a real two-form. The type decomposition is parallel because `J` is
parallel. On `Λ²T^{*(1,0)}`, mean Chern curvature is `−2λ Id` when
`Ric(g)=λg`, up to a common sign convention. Every parallel section is
annihilated by curvature, so `η^{2,0}=0`. This is a pointwise calculation,
valid on the incomplete regular locus without integration. Consequently
`−JIJ=I`, which is equivalent to commutation. The commuting parallel
endomorphism is holomorphic for the Kähler Chern connection.

`Hom(T_X,T_X)` is reflexive on normal `X`; its analytification is likewise
reflexive. Analytic Hartogs extension across codimension two therefore
extends `I`, and the inspected GAGA theorem algebraizes it. Stable
torsion-free sheaves are simple here by a direct check: a nonzero
intermediate-rank endomorphism has kernel and image of strictly smaller
slope, contradicting degree additivity. Its characteristic polynomial
has constant coefficients by projectivity and normality. Subtracting a
complex eigenvalue gives such a deficient-rank map unless it is zero.
Hence `I=c Id`, and `I²=−1` gives `I=±J`. In rank one the same conclusion
follows from `Hom(T_X,T_X)=O_X`.

**Boundary tests.** For `m=1`, the assumptions force `X=P¹`, `r=2`,
`L=O(1)`; the argument remains valid. The equality family
`P^{r−1}×P^{r−1}` with `L=O(1,1)` has `m=2r−2` and `−K=rL`.
Equally normalized Fubini–Study factors are KE, and the parallel
orthogonal structure `(-J_1,J_2)` differs from both global signs. This
is a valid sharpness example for the uniform strict criterion.

No source edit, Git operation, publication, or external individual
communication was performed. The review's only output file is this note.
