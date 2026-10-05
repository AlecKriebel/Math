# Odd minimal strata: a genus-12 coefficient-test obstruction

Problem 30004618 (OWR-4990375-010), rank 781. Investigation date: 5 October 2026.

**Status: unresolved.** This note proves a limitation of a specified sufficient
positivity test. It does not determine the Kodaira dimension in genus 12, refute
the conjecture, or establish a new general-type theorem. No novelty or priority
claim is made. The arithmetic is independently reproducible; an independent
review of this packet is still required.

## 1. Exact target and literature boundary

For each integer g >= 12, let X_g be the projectivized, non-hyperelliptic odd-spin
component of the stratum of holomorphic Abelian differentials on smooth connected
complex curves of genus g with exactly one zero of order 2g-2. The target is
kappa(X_g) = dim(X_g) = 2g-1, where kappa means the ordinary Kodaira dimension of
a smooth projective birational model of the coarse moduli space. It is not a
log-Kodaira-dimension question, a statement about the unprojectivized stratum,
or a claim that a singular stack's canonical class alone suffices.

Equivalently a point consists of (C,p), with K_C linearly equivalent to (2g-2)p;
the differential is unique up to nonzero scale. Its associated theta
characteristic is O_C((g-1)p). The indicated component has odd h^0 of that line
bundle and is the component conventionally distinguished from the hyperelliptic
one. This qualification matters: for a hyperelliptic curve and a branch point p,
h^0(O_C((g-1)p)) = floor((g-1)/2)+1. Thus the hyperelliptic component also has odd
spin for, for example, g=13. The component name cannot mean all points of odd
parity including a separate hyperelliptic component.

The official report [1], printed p. 349, Conjecture 1, gives the threshold g >= 12.
Its following page explains the need to handle the compactification, coarse-space
ramification, and non-canonical boundary singularities. Theorem 1.4 of [2]
proves general type for g >= 13. Its next paragraph explicitly lists g=12 among
the cases beyond that theorem. The public author manuscript and supplement
retain this threshold. Author publication lists identify the work as Cambridge
Journal of Mathematics 12 (2024), no. 3, 623-752. We inspected the arXiv v1 and
an author-hosted manuscript; we do not claim to have audited the final typeset
journal article or the entire 95-page proof.

The later even-spin paper [3], revised 9 December 2025, has a different component
and large-genus conclusion. It cannot settle the odd genus-12 question by its
stated theorem. Targeted searches and current author lists inspected on the date
above did not reveal a later resolution. That is a bounded search result, not
proof that no such resolution exists.

Consequently the unsettled target addressed here is kappa(X_12)=23. The full
corpus contains 30004619 as a duplicate extraction of the same conjecture; it
provides no separate mathematical target or fresh proof budget.

## 2. A precisely scoped numerical system

We use the fixed class expression of [2, Section 8], with its mid-range
generalized Weierstrass class, the pointed n-fold-point class NF, the Hurwitz
class Hur, and the compensation estimate of Proposition 5.13. The objects below
are **coefficients in that sufficient test**, not intersection numbers proving
that the actual canonical divisor is non-big. A negative coefficient can reflect
an overestimate, an overinclusive collection of numerical graph data, or an
unexploited effective-class relation. None of those possibilities is excluded.

The chosen numerical datum is the rational multi-banana with one top vertex of
genus 5, one bottom vertex of genus 0 carrying the order-22 zero, and eight edges
with prongs (9,1,1,1,1,1,1,1). Its arithmetic genus is 5+(8-2+1)=12. Put

- N=24, k=4g(g-1)/(2g-1)=528/23;
- P=sum p_e=16, Q=sum 1/p_e=64/9, ell=lcm(p_e)=9;
- k_top=P-Q=80/9, k_bottom=k-k_top=2912/207;
- N_bottom=N-P-1=7;
- R=Q/(8+1)=64/81, as in the applicable third case of Proposition 5.13;
- w_lambda=(12+k/2)/k=45/44.

The special 1/ell cases of that proposition do not apply: their first threshold
would require 9 >= 2*8-3=13; the second prong pattern is absent. The top/bottom
pair and this edge count are not a ramified two-edge hyperelliptic banana.
We do not need a new geometric realization or spin-smoothing theorem for the
result below: it is a theorem about the explicitly defined coefficient test.
In particular it is not an assertion that this datum is an unavoidable extremal
ray of the effective cone of X_12.

Normalize each auxiliary divisor to lambda coefficient 12. The horizontal and
chosen vertical coefficients contributed by subtracting it are, respectively:

| Class | horizontal | vertical |
|---|---:|---:|
| W_mid | 89/45 | 2912/405 |
| 2 NF | 311/179 | 19472/1611 |
| 2 Hur | 57/35 | 1216/105 |

The normalized compensated canonical coefficients are c_h=-45/23 and
c_b=-15142/1863. These values follow directly from

c_h=-1-k/N,
c_b=(k/N)(N_bottom-R)-k_bottom,
W_h=12(1+k/8)/(12+k/2),
W_b=(12/w_lambda)(k_bottom/k),
NF_h=(2g^2+2g-1)/(g^2+3g-1),
NF_b=2[Q(g^2+g-2)/(g^2+3g-1)-3 k_top/(2g^2+6g-2)],
Hur_h=2(3g^2+12g-6)/[(g+8)(3g-1)], and Hur_b=Q Hur_h.

These are specializations of [2, equations (39), (46), (62), (67)-(69)] and its
public supplementary computation [4]. The verifier computes them from these
formulas with rational arithmetic, rather than executing the supplied program.

### Proposition 1. The W_mid/NF test fails in genus 12

For W_mid weight y and NF weight 1-y, the two coefficients are

h(y)=-902/4117+(1936/8055)y,
b(y)=1320286/333477-(354992/72495)y.

Therefore h(y)>0 requires y>1845/2024, whereas b(y)>0 requires
y<300065/371128. The bounds are approximately 0.91156 and 0.80852,
respectively, and their difference in the latter-minus-former order is
-210325/2041204. Thus no real y makes both coefficients positive, or even
nonnegative. At the horizontal zero the vertical coefficient is -940/1863.
All statements follow by solving these two affine inequalities. This recovers,
with an exact witness, the incompatible decimal bounds already recorded in [4].
It is not claimed as a previously unknown limitation.

### Proposition 2. Adding Hurwitz weight does not repair this fixed test

Let t,u,v be nonnegative real numbers with t+u+v=1, the weights of W_mid,
2 NF, and 2 Hur. Define

h=c_h+t W_h+u NF_h+v Hur_h,
b=c_b+t W_b+u NF_b+v Hur_b.

Exact simplification gives the separating identity

b+(2017/99)h = -940/1863-(286/105)v < 0.

Since the multiplier 2017/99 is positive, h and b cannot both be nonnegative.
This proves infeasibility for every real normalized nonnegative mixture of
these three fixed classes. It does not rule out other effective divisors,
subtracting additional boundary components, another compensation divisor,
non-coefficientwise effectivity, or another proof of general type.

## 3. Exact limits of two proposed local repairs

### Proposition 3. Integer retwisting in the specified family gives no gain

For this datum, the smoothing exponents ell/p_e are one copy of 1 and seven
copies of 9. In the vertical-twisting setup of [2, equation (56)], the top
coefficient is zero and the bottom coefficient is an integer sigma in [0,9].
The bridges have integer increments whose sum on each bridge is sigma.
The correction objective in this case is

Delta = (16 sigma - sum of the squares of all bridge increments)/2.

The length-one bridge contributes sigma^2. For a length-nine bridge, every
integer a satisfies a^2>=a, so the sum of squares is at least sigma. Equality
is possible by choosing sigma increments equal to 1 and the others 0. Ordering
them with the 1s first also respects s_k <= k on these bridges. Hence the
maximum at fixed sigma is sigma(9-sigma)/2. Its maximum over the ten admissible
integers is 10, attained at sigma=4 or 5.

But the mid-range correction already has value
ell(P-Q)/8=9(16-64/9)/8=10. Therefore optimizing these integer twisting parameters
alone does not improve this datum beyond the correction already used in W_mid.
This is confined to this family of vertical twists. It does not exclude additional
vanishing of the degeneracy determinant, a different auxiliary divisor, or
other boundary subtractions. The seven bridge optimizations are elementary
convex integer minimizations, not a numerical approximation.

### Proposition 4. The compensation improvement needed by this pair

Keep all coefficients except R fixed and replace R by a real parameter r. Then
b_r(y)=b(y)+(22/23)(64/81-r). The horizontal inequality is unchanged and b_r is
strictly decreasing in y. Thus these two strict inequalities, with 0<=y<=1,
are jointly feasible exactly when r<26/99. The originally used value is
64/81; the necessary decrease is strictly greater than 470/891.

Proof: evaluate b_r at y=1845/2024. Its value is positive precisely for
r<26/99. In that case continuity gives a nearby larger y<1 satisfying both
inequalities. If the value is nonpositive, decreasing b_r cannot become positive
for y above that horizontal boundary.

Alternatively, at the horizontal boundary a change delta in the normalized
vertical coefficient w_Gamma of W_mid must exceed 470/9963 to leave a strict
positive margin, since its contribution is (12y/w_lambda)delta. This is a
conditional numerical requirement only. We have not proved that such a change
preserves effectivity, or that r<26/99 preserves extension of pluricanonical
forms at every degeneration. Even satisfying this pair would leave all other
boundary coefficients to check. No extension theorem has been weakened here.

## 4. The spin-space transfer route

The natural map (C,p) -> (C,O_C((g-1)p)) goes to the odd-spin moduli space,
whose dimension is 3g-3. The source has dimension 2g-1. For g=12 these are
23 and 33, so this map is not dominant. The subcanonical-point condition cannot
be erased by treating the minimal stratum as the entire odd-spin moduli space.
Even a general-type theorem for an ambient space would not by itself prove
that an arbitrary proper subvariety is of general type: a blowup of a smooth
projective general-type surface is still of general type and contains its
rational exceptional curve. This route therefore needs a theorem about the
particular codimension-ten image or its canonical/normal data. None is supplied.
This is a dimension obstruction to that proposed shortcut, not a statement
about the actual Kodaira dimension of the image.

## 5. Verification, limits, and stopping point

Run `python3 verify.py` with Python's standard library. It checks the rational
specializations, the exact dual identity, all 5,151 denominator-100 simplex
triples as implementation controls, and all ten integer twist values. The
identity, not the grid, proves infeasibility for real weights. A genus-13
analogue yields the nonempty pair interval
1071/1375 < y < 40409/51625, with boundary value 64/3025. This is a positive
arithmetic control only; it does not reproduce the all-boundary theorem.

Five bounded approach families have been recorded: the two-class test,
three-class mixture, integer twist optimization, compensation refinement, and
spin-space transfer. None settles g=12. Further work would require a genuinely
new effectivity/extension argument, or a different global mechanism, rather
than a fresh search over the same weights. This packet stops without claiming
an independent theorem on X_12 or claiming that the open conjecture is false.

## References

[1] Martin Möller, *Towards the Kodaira dimension of moduli spaces of Abelian
differentials* (joint work with Matteo Costantini and Dawei Chen), in *Moduli
spaces and Modular forms*, Oberwolfach Reports 18 (2021), report 6, printed
pp. 349-350. https://ems.press/content/serial-article-files/46887
Report DOI: https://doi.org/10.4171/OWR/2021/6

[2] Dawei Chen, Matteo Costantini, Martin Möller, *On the Kodaira dimension of
moduli spaces of Abelian differentials*. arXiv:2204.11943v1, 25 April 2022.
https://arxiv.org/abs/2204.11943
Author manuscript: https://esaga.uni-due.de/f/matteo.costantini/papers/KodDim.pdf
Published reference: Cambridge Journal of Mathematics 12 (2024), no. 3,
623-752, DOI https://doi.org/10.4310/CJM.241001000503

[3] Andrei Bud, Dawei Chen, Martin Möller, *The Kodaira dimension of even spin
strata of Abelian differentials*, arXiv:2410.18719v2, 9 December 2025.
https://arxiv.org/abs/2410.18719

[4] Chen–Costantini–Möller supplementary GP/Pari calculation for minimal strata
in small genera, linked from Costantini's publication list.
https://esaga.uni-due.de/f/matteo.costantini/programs/onezerobruteforce.txt
https://esaga.uni-due.de/matteo.costantini/

[5] Dawei Chen's current publication list, checked 5 October 2026.
https://sites.google.com/bc.edu/dawei-chen/home
