# Independent adversarial acceptance report

**Target:** row 1793 / ID 20000200, fixed complex special-Euclidean inverse-signature problem, shared pass 1 of 5.

**Verdict:** **ACCEPT — scoped_resolved, 1/5.** No unresolved mathematical gap was found in the accepted proof record. The accepted statement is a necessary-and-sufficient criterion for every reduced integral one-dimensional target in the fixed `(u,v)=(κ²,κ_s)` plane, with effective decision and reconstruction under the explicitly represented exact coefficient-field model. It is not an unqualified resolution of every interpretation of the original AIM question, a novelty finding, a practical complexity guarantee, or a claim that a general-purpose decision program has been implemented.

The accepted-input and public-edition SHA-256 values are recorded in `ACCEPTANCE.json` and `../EDITION_MAP.json`. All three supplied executable test suites and the independently authored suite were rerun after this snapshot; all 158 named checks passed. The independent suite also verifies 108 rational homogeneous slopes inside one aggregate check. These computations support the conventions and examples. The general theorem is accepted on the proof audit below, not on finite testing.

## 1. Statement that passed the audit

For a target whose first coordinate is constant or whose second coordinate vanishes identically, reject. These are the only one-dimensional degenerate strata.

Otherwise let `K=C(D)=C(u,v)` for the smooth projective normalization and set

- `ω=(i du/v−du/u)/2`,
- `ρ=du/(2v)`,
- `σ=du/(2uv)`.

The target is realizable precisely when both of the following conditions hold:

1. `Nω=df/f` for some positive integer `N` and nonzero `f∈K`, tested by the finite residue-divisor/holomorphic-comparison algorithm described below.
2. The two rational equations `dA+ωA=ρ` and `dB−ωB=σ` have solutions in `K`, tested by bounded Riemann–Roch linear systems.

For the least logarithmic exponent `n`, take `a^n=f`, and reconstruct `z=aA`, `w=a^−1B`, `x=(z+w)/2`, `y=(z−w)/(2i)`. Their affine image closure is an actual allowed source, with function field exactly `K(a)`, signature image closure exactly the prescribed target, and signature degree `n`. Every other allowed source with that target is special-Euclidean congruent to this one.

A nonminimal exponent is also a valid positive certificate: factor its Kummer polynomial and use a component. Minimality is needed for the immediate degree statement, not for checking realization.

## 2. Adversarial proof checks

### Factors, signs, and fixed coordinates

I recomputed the invariants from independent Cartesian jet variables, with `z=x+iy,w=x−iy`, rather than assuming the packet's intrinsic formulas. For `g=x'²+y'²` and `Δ=x'y''−y'x''`, the calculation gives

`u=Δ²/g³`, `v=(gΔ'−(3/2)Δg')/g³`.

Writing `h=dlog(dz/dw)` gives `u=−h²/(4 dz dw)` and `v=i du/h`. Thus `η=i du/v`, `q=du²/(4uv²)`, and the stated `ω,ρ,σ` have the correct signs and factors. The full generic identities, including both reconstruction equations, simplify to zero exactly. Reflection reverses `v`; no reflection or target-coordinate change has been silently substituted.

### Multiplicative obstruction and minimal cover

The norm of any algebraic solution `b` of `db/b=ω` supplies a logarithmic multiple over `K`. Conversely, a root of `T^N−f` supplies such a solution. At most simple poles and rational residues are necessary. Clearing residue denominators by `m` gives a degree-zero integral divisor `A`. Its class must have finite order `t`; even then the remaining holomorphic differential `mtω−df/f` must vanish. All possible logarithmic exponents are multiples of `mt`, so a failed holomorphic comparison cannot be corrected by a larger exponent.

The norm argument also proves irreducibility of `T^n−f` at the least exponent: a root of smaller degree would give a smaller exponent. Every algebraic solution differs from that root by a constant after embedding into a common extension, so every realization contains the same preferred cover. This is a genuine elimination of arbitrary-cover search.

### Additive obstruction and absence of cover repair

For any finite extension in characteristic zero, the normalized trace of a primitive is a primitive downstairs. This holds for ramified extensions as well, because derivations extend uniquely through separable extensions and commute with embeddings. It applies independently to each of the two forms. Dividing a primitive by `a` or multiplying it by `a`, then taking trace to `K`, gives the two rational inhomogeneous equations. The character-eigenspace proof in the canonical-cover report is a second valid route.

Consequently neither unknown additional covers nor coordinate functions on larger covers can supply a realization rejected by the stated tests. Nonzero residues and nonzero holomorphic or second-kind classes are not confused with one another.

### Actual plane image, field generation, uniqueness

The reconstructed differentials are nonzero and their product is `q≠0`. The field `E=C(z,w)` has transcendence degree one and defines an integral affine plane image. Computing its intrinsic rational invariants gives exactly `u,v`, hence `K⊂E`. The differential ratio `a=2v dz/du` then lies in `E`, proving `E=K(a)` without assuming birationality. Nonconstant `u` excludes a line; thus the source has degree greater than one.

The map on coordinate fields is the prescribed inclusion of `C(u,v)`, which proves the required image-closure equality. For another realization, trace-descended primitives differ from the original coordinates only by constants and the common root scaling. These give `(z,w)↦(cz+z₀,c^−1w+w₀)`, exactly a complex special-Euclidean transformation. A redundant parametrization does not create an additional source normalization.

### Degenerate strata and point boundary

Generic zero metric forces an isotropic line. With nonzero metric, zero curvature forces a line. Constant nonzero `u` forces `v=0`, and conversely `v=0` forces constant `u`. Therefore no one-dimensional vertical target or target `v=0` is realized. The allowed point-signature boundary consists precisely of `(a,0)` for `a≠0`, realized by circles with squared radius `1/a`; `(0,0)` belongs only to the excluded nonisotropic lines. The proof does not divide by identically zero functions on these strata.

## 3. Finite effectivity and termination

The coefficient model is an explicitly presented finite extension of a rational-function field over `Q`, with a declared algebraically independent transcendence basis, exact input representations, and a chosen embedding in `C`. Number-field coefficients are included. The theorem over `C` is unconditional; the uniform algorithm is asserted only in this exact model. Discovering algebraic relations among arbitrary numerical complex names is not part of the assertion.

The effectivity report correctly replaces unbounded torsion-order search. After a finite coefficient extension, the residue divisor is rational over a finitely generated field `k`. Spread the curve over a normal integral finite-type `Z`-base, shrink to good reduction, and find two closed points of distinct residue characteristics. Such points exist, and enumeration of finite fields and points terminates. A torsion section of order prime to the residue characteristic extends over the normal base through the finite étale torsion scheme and cannot specialize to zero unless it was zero. This proves the required specialization injectivity.

If the reduced Jacobians have orders `M₁,M₂`, their product annihilates `J(k)_tors`. The packet's alternative factorial annihilator is also valid: the prime-to-`p₁` part of any torsion order divides `M₁`, its `p₁`-part divides `M₂`, both are bounded by `H=max((q₁+1)^(2g),(q₂+1)^(2g))`, and their coprimality makes their product divide `H!`. This bounds the torsion of the field of definition, not the unbounded torsion group `J(C)_tors`.

Testing `L(−BA)` has the correct sign: a nonzero member has divisor exactly `BA` because the divisor has degree zero. Extension of constants cannot create a missing section, so this test is valid for geometric principality too. The final differential comparison is exact. No Mordell–Weil rank computation or numerical period recognition is required.

For `dF+θF=ξ`, every pole order `k>0` satisfies the packet's bound

`k≤max(0,b−1,j)`,

where `b` is the pole order of `ξ`, and `j` is the residue of `θ` only when its pole is simple and that residue is a positive integer, otherwise zero. The holomorphic, higher-pole, and simple-pole resonance cases are exhaustive. The resonance term is essential and was tested independently. The resulting finite Riemann–Roch spaces give complete linear systems. An independent fallback after constructing the cover uses the primitive bound `max(poleord(α)−1,0)`.

Thus the packet supplies a terminating theoretical decision method and finite positive or negative algebraic checks. The supplied scripts do not implement normalization, general Riemann–Roch, arithmetic spreading, or the complete inverse-signature algorithm; no such implementation is accepted or claimed.

## 4. Additional independent genus-one controls

These controls were derived during this audit and are included in `independent_controls.py`.

Let `E: y²=x³−x`, `P=(0,0)`, and `O` the point at infinity. Then `div(x)=2P−2O`. The class of `P−O` has exact order two: it is killed by two, while principality would give a degree-one function on a genus-one curve.

### Torsion passes but the holomorphic comparison fails

Take

`u=x`, `v=i x y/[2(y+x)]`.

The target field is all of `C(E)`, since `y=2vu/(iu−2v)`. One implicit integral target equation is

`4uv²−(u²−1)(iu−2v)²=0`.

Its canonical form is `ω=dx/(2x)+dx/y`. The residues are integral and the residue divisor is `P−O`, with exact order two. But

`2ω−dlog x=2dx/y≠0`.

The right side is nonzero holomorphic. This actual integral one-dimensional candidate therefore passes the residue and torsion checks but is correctly rejected by the required holomorphic comparison.

### Integral residues do not imply exponent one

Instead take

`u=y`, `v=i y(3x²−1)/(5x²−3)`.

If `r=v/(iu)`, then `x²=(3r−1)/(5r−3)` and `x=u²/(x²−1)`, so the target field again equals `C(E)`. Here `ω=dx/(2x)` has integral residues but least logarithmic exponent two. This explicitly tests the nonprincipal torsion case in the actual signature-input setting. It is only a multiplicative-stage control; no realization claim is made for this target.

The supplied suites independently cover a nonhomogeneous realizable cubic with quadratic canonical cover, a realizable genus-one signature, a rational conic with elliptic canonical cover and nonzero holomorphic reconstruction form, a residue obstruction, an irregular connection whose two rational equations nevertheless have solutions, and repeated parametrizations. All those calculations and their geometric interpretations survived review.

## 5. Source verification and scope boundary

- The retained AIM item 3.5 contains the broad question without the adopted group, pair, field, or image convention. Its item and neighboring boundaries were independently inspected in the retained original HTML. A fresh live request returned a gateway error; this audit does not mislabel that retry as a fresh successful retrieval. Source: http://aimpl.org/algvision/3/ .
- Kogan–Ruddy–Vinzant, *Differential signatures of algebraic curves*, equations (20)–(21), Table 1, Example 2.39 and the symmetry-degree discussion were independently inspected in the retained original paper; the rendered formula pages were also viewed. The live version metadata was checked. These confirm the fixed pair and established signature framework, not an inverse-realizability theorem. Source: https://arxiv.org/abs/1812.11388v2 .
- Risch, *The solution of the problem of integration in finite terms* (1970), pp.605–608, was independently read in full, including the exact coefficient caveat and the two-good-reductions mechanism. The original scanned pp.607–608 were visually inspected. This effectivity mechanism is classical prior art, not a new integration algorithm. Source: https://doi.org/10.1090/S0002-9904-1970-12454-5 ; inspected original-paper mirror: https://www.cs.ru.nl/~freek/courses/mfocs-2012/risch/S0002-9904-1970-12454-5.pdf .
- Milne's *Abelian Varieties*, Theorem 14.1 and the discussion around Theorem 23.5, supply the standard finite-field size and good-reduction context. The packet also provides the needed normal-base section argument directly. Source: https://www.jmilne.org/math/CourseNotes/AV110.pdf .

Acceptance is limited to the adopted complex `SE(2,C)` ordered pair and rational image-closure convention. It excludes real descent, smooth closed traversals, other groups or invariant coordinates, higher-dimensional ambient curves, reducible sources, and positive characteristic. It does not establish priority for the specialized synthesis or exhaust the older literature on natural equations. No further mathematical pass is needed for an identified gap in this frozen target; the appropriate result label is **fixed-pair complex scoped resolution, 1/5**.
