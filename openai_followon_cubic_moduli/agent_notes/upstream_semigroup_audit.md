# Independent adversarial audit: family 037 large-stabilizer machinery

Audit checkpoint: 2026-10-06 22:13 PDT / 2026-10-07 05:13 UTC.

## Scope, version, and verdict

I independently read the complete source of Sections 04, 05, 06, and 07 of
`The-ordinary-double-point-gap-in-every-dimension-September-24-2026`, together
with the input/output statements in Sections 01–02 and the bibliography.
The source clone is read-only and its HEAD is exactly
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. A diff limited to this preprint was
empty. No source build, branch, commit, push, or external communication was
performed by this audit agent.

**Verdict:** I have found no explicit counterexample or substantive logical
gap in these four sections. Their large-stabilizer upper-bound mechanism is
coherent conditional on the cone reduction, grading approximation,
small-stabilizer theorem, and fourfold base theorem. This verdict is a
human-readable adversarial proof check, not a formal verification of the
all-dimensional theorem and not a substitute for auditing those other inputs.
The bound needed by the cubic application is already obtained in Section 07,
lines 444–484; the equality machinery at lines 486–678 is additional and is
not needed to transfer an upper density bound.

The relevant discovery goal here was to falsify or locate an exact gap in
the assigned machinery. Best-guess completion of this assigned audit: 90%.
Mathematical resolution and publication completion for the parent cubic
project are not estimated by this limited audit.

Source SHA-256 values:

| Source under `build/sections/` | SHA-256 |
| --- | --- |
| `04-jet-interiority.tex` | `0025d703e072514b957be0e8be1bd0f3ed63911f3049e637aea530d6828fca69` |
| `05-adjoint-semigroup.tex` | `1d79ada8f1ccaebdba630c100088e3543097056c19a84139f1cc75f695f3be9b` |
| `06-filtrations.tex` | `d8ea5cb97c715ddb247253503816dd906d3b835ebbf7bb88420260bbfc7fe978` |
| `07-bootstrap.tex` | `5837f6a478e54f735d29ff8cfed5bcc8f821b188bd70f819cf207ccb06d6fcd7` |

All line references below refer to these exact files, not PDF page numbers.

## 1. Jet setup, valuations, and canonical interiority

### Proposition `jet:setup`, Section 04, lines 75–226

The semigroup is additive because total-degree-then-lexicographic leading
monomials multiply. Its leaves are one-dimensional by cancellation of
leading coefficients. Compatible finite jets are realized after sufficient
ample twisting; using every residue class modulo a common stabilizer multiple
is necessary and present at lines 130–141. In particular, constants occur at
all sufficiently large degrees divisible by the chosen stabilizer order
`m`. This gives `(m,0)` in the generated group, not just `(M,0)` for the
auxiliary descent multiple. Linear jets and that constant difference generate
exactly the congruence lattice (lines 143–147).

The fixed affine embedding argument at lines 152–170 gives a uniform order
bound `|gamma| <= C j/r`: generator degrees are uniformly bounded below by
a positive multiple of `r`, and restriction of a homogeneous function to a
transverse slice preserves its local order. A general complete-intersection
curve not contained in its zero divisor then supplies the Bézout bound. This
also justifies the coercivity used in all subsequent differentiated integrals.

The nonsaturated counting proof is not circular. At lines 191–208 the
finitely generated subsemigroup has a conductor, obtained by resolving finitely
many lattice remainders using equality of generated groups. Exhaustion at
lines 210–218 then gives the leading count for the full semigroup; it asserts
only asymptotic density. The lattice covolume after scaling is `Nm/r=1/s`,
so the counting factor is `s`, not `1/s`.

The canonical congruence `r = sum b_i mod m` is consistent with the section
convention `F(epsilon^b z)=epsilon^j F(z)` at lines 40–45 and with the
canonical form in the local extraction. Thus `c_0=(r,1,...,1)` is a lattice
point. No equality-of-volumes hypothesis has entered this proposition.

### Lemma `jet:test`, Section 04, lines 230–304

The costs are `v(t)=N/r`, `v(z_i)=delta`, on a uniformizing chart with the
finite action `t -> epsilon^-1 t`. Distinct original degrees have distinct
powers of `t`, so the minimum rule does not permit unwanted cross-degree
cancellation. Positive rational costs give a divisorial valuation after
rescaling; `delta=0` is the degree valuation. The canonical form
`t^(r-1) u(z) dt wedge dz` gives exactly `N+N delta` for the log discrepancy.

A Taylor leading-term basis is compatible with total order. Thus the
colength counts indices with `D_0+delta |gamma|<q`. For an `n`-dimensional
cone, the exponential integral is `n!` times the unit cutoff volume, not
`N!`. Integrating first in `D_0` gives the displayed `N`-variable integral
with lattice factor `s`. The factors in the normalized-volume test agree.

### Lemma `jet:moments`, Section 04, lines 313–380

The first inequality follows from the volume lower hypothesis and a valid
test valuation. The second is a near-minimality statement, rather than an
unjustified stationarity assertion for non-minimizing gradings. Homogeneity
gives `E_f f=N` and `E_f f^2=N(N+1)`. Coercivity bounds the first and second
moments of `|x|` uniformly, so the Taylor argument at lines 351–376 yields
`F'(0)/F(0) >= -eta_nu`, with `eta_nu -> 0`. A fixed small rational test is
enough to rule out a uniformly negative derivative. In the exact rational
minimizing case this becomes a one-sided nonnegative derivative.

### Probability lemmas and theorem, Section 04, lines 390–750

I checked the envelope derivative, the log-concavity convolution argument,
the CDF Jensen proof of the barycenter bound, the two likelihood-ratio
single-crossing arguments, the size-bias identity, and the Hessian sign.
In particular, weighting by `X_i X_j` changes the two independent
exponentials to Gamma(2,1) laws, equivalently adding independent exponentials
with their respective coefficients. The conditional identity
`E[(X_i-X_j)^2 | X_i+X_j]=2 E[X_i X_j | X_i+X_j]` supplies the crucial
negative Hessian direction when the higher coefficient occurs twice.

The compactness proof separates escape to infinity for fixed dimension from
the subsequent limit over dimensions. It does not assume bounded maximizers
in every dimension: this is justified only when the supremum exceeds the
escape bound. The exceptional coefficient sequence may tend to infinity
at any rate relative to dimension; almost-sure convergence of the average
of the other exponentials still yields the stated limiting indicator.

The one-variable formulas and derivative signs at lines 699–730 agree by
direct integration. I reproduced the rational numerical certificate using
exact rational arithmetic:

```
sum_{k=0}^8 (4/3)^k/k! + ((4/3)^9/9!)/(1-(4/3)/10)
    = 917330371/241805655 < 1897/500;
sum_{k=0}^6 1/k! = 1957/720 > 1359/500;
(3/4)(1897/500)-(1/3)(1359/500) = 3879/2000 < 2.
```

Numerically `C_* = 1.9391569781927012`; the exact rational certificate,
rather than this decimal, is the reproducible strict gap. There is no need
to rely on Monte Carlo for the probability theorem.

### Theorem `jet:interior`, Section 04, lines 754–798

If `f(1)>=N`, a homogeneous supporting plane gives coefficients with
nonnegative sum. Subtracting their common average gives a sum-zero vector
still below `B_0` on the positive orthant. The envelope plus both moment
inequalities produces `(1-eta/u)H <= C_* <2`, while `H>=2/s>=2`.
This contradiction remains uniform in the chosen grading and point because
`C_*` is dimension-uniform and `eta -> 0`. The proof therefore establishes
strict interiority for sufficiently far terms, including the exact rational
case. It does not require exact saturation in advance.

## 2. Adjoint lifting and exact saturation

### Lemma `adj:vanishing`, Section 05, lines 34–102

I checked the coarse-space rounding rather than assuming a stack vanishing
theorem. At a divisor of inertia order `e`, the fractional coefficient of
`D_c` is at most `(e-1)/e`; therefore
`Delta=R+Theta_c-{D_c}` is effective. Its log pullback is bounded above by
the given SNC boundary `Theta`, so it is klt. Tame invariant pushforward
of the invertible sheaf is reflexive and is prescribed in codimension one
by `floor D_c`; this retains possible codimension-two character information
as a Weil-divisor sheaf. The coarse space is locally Q-factorial because
it has quotient singularities.

I inspected the cited primary statement, Fujino's *Cone and contraction
theorem for projective morphisms between complex analytic spaces*, version
0.00 dated 2023-10-09, Theorem 3.2.4, printed page 31. It explicitly permits
an integral Q-Cartier Weil divisor. Its extra bigness condition on log
canonical centers is vacuous for a klt pair, so the cited statement supports
the use here. URL:
<https://www.math.kyoto-u.ac.jp/~fujino/cone-and-contraction.pdf>.

### Lemma `adj:implication`, Section 05, lines 106–403

The central implication is stronger than a leading asymptotic count and I
checked its five distinct steps:

1. A finite cone surrounds the chosen interior point without assuming finite
   generation of the full semigroup (lines 127–134). Scalar weights can
   realize the finite list of total-degree and lexicographic comparisons;
   high Taylor degrees are excluded by positivity. Rational combinations
   and products give the surrounding monomials in a common actual integral
   section degree (lines 136–181).
2. The weighted Rees construction is local in algebraic étale parameters,
   with coherent finite-jet quotients globalized at the residual gerbe.
   The chart ratios show the smooth stack model, including its exceptional
   inertia (lines 184–244). The weights are primitive, but no unjustified
   effectiveness assumption about the exceptional divisor is made.
3. The canonical shift is exact:
   `P_0-(K_Z+E)-H_0/a = (j+r-j_0) pi^*L` (lines 246–258).
   Its coefficient is strictly positive. On each exceptional chart, dropping
   one coordinate from `u.x=U` is an affine isomorphism. Consequently
   `alpha_rem+1` lies in the interior of the scaled Newton polyhedron.
   The section has the required finite-group character with integral
   exponents (lines 265–315).
4. On the log resolution, the base-free part is nef and the positive ample
   pullback is nef and big, exactly as needed by the previously justified
   vanishing statement (lines 317–353). SNC support ensures round-down
   commutes with restriction. The restricted bundle is the multiplier-ideal
   bundle by adjunction (lines 355–373).
5. The positive discrepancy correction is exceptional and the multiplier
   correction is negative effective. Hence no nonexceptional pole survives;
   normality permits regular pushdown. Exceptional order and restriction
   recover a single scalar initial, and the preselected scalar comparisons
   exclude every original-order predecessor (lines 375–403).

Howald's primary monomial multiplier-ideal theorem was inspected at
<https://arxiv.org/html/math/0003232v1>, Main Theorem. Its interior criterion
with `alpha+1` is exactly the one used on the smooth finite uniformizers.
The proof correctly uses an orbifold stack chart instead of incorrectly
treating the coarse weighted exceptional divisor as smooth.

No step here uses `c_0` itself interior. In particular, the dependency
`interiority -> adjoint lifting -> interiority` is absent.

### Theorem `adj:saturation`, Section 05, lines 412–557

The nonpolyhedral possibility is addressed explicitly rather than ruled out
by assertion. At a differentiability point, an irrational support has dense
values on the full lattice; a primitive integral support of height at least
two has value `-1` on a lattice point. Both yield a forbidden strip point.
Recurrence of the boundary point in the lattice torus puts one sequence
outside the cone, while differentiability makes the canonically shifted
sequence strictly inside. Adjoint lifting contradicts this.

An interior ball about `c_0` bounds all integral height-one normals, hence
only finitely many occur. Differentiability almost everywhere and local
Lipschitz continuity recover the entire epigraph on the open positive
orthant; translation by `c_0` extends this recovery to coordinate faces.
The coordinate support forms are primitive in the actual congruence lattice
and take value one on `c_0`. Exact saturation and the interior translation
then follow from the facet inequalities. This is a valid convex-lattice
argument conditional on the adjoint implication.

As a falsification control, asymptotic counting alone would be insufficient:
the semigroup generated by `(2,0),(3,0),(0,1)` has full lattice Z^2 and full
quadrant leading density but misses `(1,0)`. Likewise saturation alone does
not force a prescribed canonical translation: for the quadrant semigroup
and `c=(2,1)`, the interior lattice points are not `c+Gamma`. The source
avoids both invalid shortcuts by proving the adjoint implication and
height-one support property separately.

## 3. The two filtrations

### Lemma `filt:first-ring`, Section 06, lines 48–204

The finite semigroup generators lift to a finite algebra generating set
because subduction terminates in every original homogeneous degree. A finite
scalar refinement reproduces the monomial algebra: inclusion together with
equality of dimensions in each original/T bidegree rules out extra initials.
Thus the deformation is finite type and flat. Normal/Gorenstein/CM lifting
through the regular parameter, followed by contraction for a positive
combined grading, gives the stated global properties. The scalar parameter
has zero degree in the two degrees being tracked, so it introduces no hidden
canonical bidegree shift.

The exact constant index `(m,0)` is obtained from saturation. After inversion,
eventual jet realization produces every compatible monomial. The actual
congruence lattice has Laurent splitting with `u_i=tau^(b_i)z_i`; hence there
is no leftover cyclic quotient in the nonzero `v` fibers. Each fixed
T-degree piece is a finite free C[v]-module of rank
`binomial(q+N-1,N-1)`. This yields the Hilbert series of `D`, the canonical
shift `(r-m,N)`, and the compatible basis of `S`.

The Gorenstein lifting statement was checked against the exact primary
Stacks Project lemma <https://stacks.math.columbia.edu/tag/0BJJ>. Reducedness
and normality criteria were checked at
<https://stacks.math.columbia.edu/tag/033P>.

### Lemma `filt:discrepancy`, Section 06, lines 222–297

The Rees convention gives action weight `-1` on the parameter. Adjoint
lifting of the canonical generator therefore gives bidegree `(r,Q-1)`.
On parameter-nonzero fibers, the ratio of canonical generators is a unit
`c lambda^a`; the degree/action calculation forces `a=-Q`. Comparing
canonical forms gives `A_product(V)=A_Rees(V)+Q ell`. Retraction on product
log models independently gives `A_product(V)>=A_C(w)+ell`, so the asserted
inequality has the correct `Q-1` coefficient and sign.

### Lemma `filt:reduced`, Section 06, lines 301–368

At a divisor component of `v=0`, the first Rees total space is regular of
local dimension two. If the central multiplicity is `nu`, costs
`V(lambda)=1`, `V(t)=1/nu` give discrepancy `1+1/nu`. The basis domination
gives a centered valuation on `C` of volume at most one, and the first
canonical shift gives discrepancy at most `N+1/nu`. For `nu>=2`,
`(N+1/2)^(N+1)<2N^(N+1)` holds for `N>=4` by the displayed logarithmic
certificate. It is important that this argument is not silently applied
in dimensions below five. Generic reducedness plus CM gives reducedness
of the full quotient, not merely of its generic points.

### Proposition `filt:structure`, Section 06, lines 370–440

The intrinsic description `W_p=sum_{a=0}^p v^a T_{p-a}` proves independence
from compatible basis lifts and multiplicativity. In a basis product the
T-degree cannot decrease. Equality of W-cost occurs precisely for zero
extra powers of `v`, so the product in `gr_W S` is the product in `D`,
with an independent polynomial variable. Thus the ring identity
`gr_W S=D[v]` is stronger than, and justified independently of, its Hilbert
series. Reducedness of `D`, rather than its normality, suffices for the
codimension-one argument making the second Rees total space normal.

### Lemma `filt:free-grading` and Corollary `filt:stabilizer`, Section 06, lines 491–578

Free grading gives genuine Zariski Gm torsor charts and an honest ample
weight-one line bundle on Proj. Its integral degree is one by the Hilbert
series. Reducedness and equidimensionality force a single integral
component. Successive nonzero sections yield pure CM degree-one Cartier
divisors, hence integral ones; the restrictions of the degree-one subspace
drop in dimension exactly by one, since division by a defining section
leaves a constant function on a proper integral scheme. This constructs a
linear regular parameter sequence and gives the polynomial ring. Applied
to `D`, it would make `gr_W S` polynomial; finite terminating lifting would
then make `S` polynomial as well, contradicting singularity. The nontrivial
stabilizer therefore exists without requiring `D` to be normal.

## 4. Same-dimensional slice and bootstrap

### Lemma `boot:slice-tests`, Section 07, lines 49–161

The level slice through a nonzero homogeneous function admits a finite
étale Gm product cover, because its value is invertible and adjoining a
root of it is étale in characteristic zero. This gives a normal
Gorenstein germ of dimension `n`, with a nonzero function of primitive
character `-1`. Away from that function's zero set it is klt. The slice
field is a finite extension of `K(C)` by the equation
`lambda_Y^d=s/c`; its restriction valuation remains quasi-monomial.
Extension trivially along the Gm factor preserves discrepancies in the
restricted-value scaling. Filtration domination gives center at the
vertex, discrepancy at most `N ell+A_Y(u)`, and volume at most `ell^-n`.

### Lemma `boot:slice-klt`, Section 07, lines 163–200

If the slice were not klt, a nonpositive-discrepancy divisor lies over
`lambda_Y=0` because the complement is klt. Approximating it by monomial
valuations centered exactly at the slice point gives discrepancy/parameter
ratios with limit at most zero. The basic test would force the original
normalized volume to be at most `N^n`, contrary to its lower hypothesis
`2N^n`. The source correctly handles an already nonpositive discrepancy
upper bound before taking a positive nth power.

### Lemma `boot:slice-singular`, Section 07, lines 202–265

This is a pivotal step; a smooth slice would invalidate the use of `M_n`.
If the Rees total space were smooth, cutting the equivariant lift of the
polynomial central variable realizes `D` as either a smooth germ or a
minimal hypersurface whose defining character is `-1 mod h`. In its other
flat deformation, the base parameter has character zero. Equivariant
formal generator lifting and flatness lift either the empty relation or
the single relation of character `-1`. A relation of nontrivial character
has no term involving only the fixed base parameter, so setting every
other formal coordinate to zero defines a fixed formal section.

Its generic point carries a nonvanishing positive-T-degree function since
the original point is nonvertex. But the generic fiber is standard affine
N-space with every coordinate character one; for `h>=2` its fixed scheme
is just the origin, where every positive-T-degree function vanishes.
This contradiction is valid. In particular, the proof does not merely
assume that singularity persists under the two different deformations.

### Lemma `boot:character-shares`, Section 07, lines 283–319

Multiplication by powers of `lambda_Y` injects one character quotient
with a shifted valuation cutoff into another. Since its character is
primitive and its value positive, every character can be connected with
a power at most `h-1`. The fixed cutoff shift gives matching leading
coefficients, each `1/h` of the total. This proof does not assume a free
tangent representation or an isolated fixed point. Without a primitive
nonzero character function, such an equal-share assertion would be false
(for example, a trivial cyclic action has only the trivial character).

### Proposition `boot:refined-estimate`, Section 07, lines 321–377

The exact colength split has no overlap. Dividing a restricted filtration
element by `lambda_Y^p` gives a regular slice function of character `p`.
Valuation additivity gives an injection into that one character quotient,
not into an arbitrarily chosen fraction of the full quotient. The Hilbert
cutoff and equal-character leading coefficients yield
`vol(w)<=min_x {x^n/ell^n+(1-x)^n sigma/h}`. There are only finitely many
characters for each fixed slice, so the asymptotic error can be made uniform
as `p mod h` varies.

### Lemma `boot:holder` and Theorem `boot:upper`, Section 07, lines 379–484

Direct minimization gives denominator
`(ell^(n/N)+(h/sigma)^(1/N))^N`. Hölder with exponents `n/N` and `n`
gives the claimed bound
`d(C)<= (N/n)^n+(A_Y(u)/n)^n sigma/h <= p_n/2+M_n/2`.
The slice is singular, klt, zero-boundary, and dimension `n`, so its
minimizing normalized density is legitimately bounded by the definition
of `M_n`; `h>=2` supplies the improvement. The supremum argument uses
densities tending to `M_n` and does not assume that `M_n` is attained.
Approximation is performed separately on each fixed cone. Consequently
there is no same-dimensional induction circularity in this section.

The deduction still depends on the separate small-stabilizer classification
to exclude an infinite subsequence of such gradings for a density strictly
greater than `p_n`, and on the separate lower-dimensional cone reduction.
These are explicit remaining external dependencies of this audit.

### Equality steps, Section 07, lines 493–678

Although not needed for the cubic upper-bound transfer, I checked the
equality arithmetic and the two key further arguments. The endpoints of
the Hölder chain force `h=2`, `A'=N ell`, and after `ell=1`,
`sigma=2`, `A_C(w)=2N`, `vol(w)=2^-N`. The strict count uses only one
power at each cutoff, so its positive leading loss is not double-counted.
The rounding argument controls the changing chosen section using a fixed
finite set of possible generator monomials; absolute grading error
therefore yields `Nm-r<=o(1)`. Integer rounding is then valid. These steps
again use uniqueness of the normalized-volume minimizer as an external
theorem, and the final identification uses the separate small case.

## 5. Explicit quadratic consistency test

I worked through the full construction for
`S=C[a,z_1,...,z_N,b]/(ab-sum z_i^2)`, `N>=4`, standard original degree.
At the chart `a=1`, the first Taylor weights are `(0,1,2)` on `(a,z,b)`.
The lexicographic monomial semigroup is generated by the constant index,
the linear z indices, and `(1,2e_N)`, after ordering the last variable
to be the smallest monomial. It is saturated. Its noncoordinate primitive
facet form is
`eta(j,gamma)=2j-2 sum_{i<N} gamma_i-gamma_N`, and
`eta(N,1,...,1)=1`, exactly matching the canonical shift.

The first quotient is
`D=C[z_1,...,z_N,b]/(sum z_i^2)`, with T-degrees 1 on z and 2 on b.
Its Hilbert series is `(1-z)^-N`, its canonical T-degree is `N`, and
the b-axis has the new stabilizer `h=2`, despite the original `m=1`.
The second Rees equation is `lambda a' b'-sum (z_i')^2=0`. Slicing
`b'=1` produces an n-dimensional ODP. Its minimizing valuation has
`ell=1`, `A'=N`, `sigma=2`. Restriction assigns weight 2 to all original
generators, so `A_C(w)=2N`, `vol(w)=2^-N`, and `w(v)=2`.
Thus the dimensions, both canonical shifts, both stabilizers, the character
factor, optimization equality, and strict-count boundary agree on an
explicit sharp example. This is a consistency check, not a proof for
arbitrary cones.

## Exact limitations and outstanding independent checks

No Lean declarations or builds were used as validation. This audit does
not certify the fourfold companion, stable degeneration and cone reduction,
small-stabilizer classification, metric tensor estimate, or the global
cubic compactification transfer. It also does not establish priority.
The parent should not promote the full all-dimensional gap or a new
cubic-moduli paper solely on this limited no-obstruction verdict.

The standard semigroup Cohen–Macaulay/canonical-module theorems and
functorial log resolution are being used as published mathematical inputs.
Their precise applications were checked from the source's hypotheses and
derivations; this audit has not recreated their original complete proofs.
There is no identified repair to apply to the assigned sections because
no failed claim was found.
