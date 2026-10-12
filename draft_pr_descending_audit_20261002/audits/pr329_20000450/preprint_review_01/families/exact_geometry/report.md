# Independent exact-geometry review01

Status: scoped geometric verification completed; this is independent family evidence, not publication clearance. The namespace remains unsealed. The candidate and all prior-review artifacts were not changed.

## Claim, assumptions, and success criteria

The targets are the candidate's whole-curve geometric integrality and exact genus-one range, its explicitly normalized regular-pentagon equation, both rational maps to the cubic, the actual signed quadratic twist to Tate normal form, the origin and infinity subgroup, all excluded fibers, and the allowed cuspidal member. The coefficient field has characteristic zero, contains a fixed element `r` with `r²=5`, and `λ` is finite. Geometric assertions are made after algebraic closure. The real regular-pentagon interpretation uses the embedding `r=+√5`.

Success requires exact identities plus a proof about the entire plane curve, rather than one component selected by rational formulas or numerical samples. In particular, a rational-function-field calculation must be supplemented by a primitive-polynomial check; branch multiplicities and all exceptional parameter values must be accounted for. A quadratic twist must be verified at equation level with a nonzero scaling, not only by comparing `j` invariants.

Inputs read directly:

- `/Users/alec/Documents/Math/AGENTS.md`.
- AIM original PDF at `../../evidence/source/qptsurface2.pdf`, physical page 51, including Question 17 and all four remarks.
- Candidate manuscript at `../../evidence/candidate_stage1/inputs/manuscript.tex`.

No previous reviews, root gates, other project verdicts, candidate ZIP, or candidate routines were read. All computations below are independently written here. The existing SymPy 1.14.0 interpreter was used without installation.

Input SHA-256 values recorded by the exact computation:

```
manuscript.tex d29598eca6bcee12d498dfe6bed5a91112bc89acc217ead458e91c655a170dd4
qptsurface2.pdf 8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6
```

## Concrete discrepancy

The sentence immediately after the main theorem attributes “local conditions” to Question 17's remarks. That phrase/topic is absent from the four Question 17 remarks on physical page 51. They concern (i) infinity torsion, (ii) principal homogeneous spaces/Sha motivation and a universal `X₁(5)` twist, (iii) relation to conference talks, and (iv) nonregular/star variants. Earlier material on that same page concerns Hasse/local solubility. Remove “local conditions” from this attribution, or supply a different precise source. This is a minor source-context error and does not affect the checked geometric identities.

No mathematical discrepancy was found in the scoped geometry after the independent checks and proofs below.

## Independent derivation and global proof

### The side product and its scaling

Let `e` be a primitive fifth root with positive real embedding of `φ=1+e+e⁻¹`. In the exact cyclotomic ring `Q[e]/(e⁴+e³+e²+e+1)`, multiply

```
L_j = Z + e^(2j+1) W - (1+e)e^j T,   j=0,...,4.
```

Each factor vanishes at successive vertices `(Z,W,T)=(e^j,e⁻ʲ,1)` and `(e^(j+1),e^(-j-1),1)`. The exact product is

```
Z⁵+W⁵+5φZ²W²T-5φ³ZWT³+φ⁵T⁵.
```

Here `(2φ-1)²=5` and `φ>1`, hence `φ=(1+√5)/2`. Substituting `Z=X+iY`, `W=X-iY` gives exactly the candidate's `P`. This proves its side-product normalization, including the constant and sign. Rotation `Z→eZ`, `W→e⁻¹W` sends `L_j→e L_(j-1)` and preserves the product and `Q`. Its real matrix has

```
cos(72°)=(r-1)/4,  sin(72°)=δ/(2φ),  δ²=5+2r.
```

The independently expanded real substitution also preserves `P` exactly.

### The two quadratic extensions

Expanding the affine equation in `Y` gives the stated `A Y⁴+B Y²+C`. Direct exact expansion proves

```
B²-4AC = (4X²+2X-1)² (20X²-aX+b),
a=40+20r+8λ, b=a+5,
a²-80b=64λ(λ+5r).
```

For `λ≠0,-5r`, the last quadratic has two simple roots and is not a square over the algebraically closed coefficient field's rational function field in `X`. Thus the intermediate extension obtained by adjoining `Y²` has degree two. With `V=(2AY²+B)/h`, `t=V-2rX`, solving the conic gives `X=(b-t²)/(a+4rt)`; substituting this parametrization verifies the conic identity exactly. The conic's function field is therefore the rational field in `t`.

Solving `Y²=(hV-B)/(2A)` on that conic, independently rather than presupposing the cubic, gives exactly

```
Y² = m z² F(z) / [400(z+γλ)²(z+αλ)],
m=5-2r, z=t+5+2r, α=1-r/5, γ=2r/5.
```

The computed identities are the candidate's

```
disc(F)=(24064+10752r)λ(λ+5r)³(λ+c),
F(-αλ)=(-16/5+16r/25)λ²(λ+5r), c=(11+5r)/2.
```

For `λ∉{0,-5r,-c}`, `F` has three distinct roots, none is `s=0` after `s=z+αλ`. The rational square factors `z²` and `(z+γλ)²` do not affect parity of divisor orders. The remaining square root has precisely the three roots of `F` and the pole at `s=0` as its four odd branch points. Its order at infinity is even (degree two). It is therefore nonsquare in the intermediate rational field. The full extension has degree four over the original rational field in `X`; the degree-four polynomial in `Y` is irreducible there. Riemann–Hurwitz for this separable double cover of `P¹` gives `2g-2=-4+4=0`, so `g=1`.

### No component is lost by the chart

The root of the leading coefficient `A` is `X₀=-(5φ+λ)/10`. Direct evaluation gives

```
B(X₀)=λ(λ+5r)(λ+5(φ+1))/25.
```

Outside `0,-5r`, a common zero of `A,B,C` could occur only at `λ=-5(φ+1)`. At that parameter `X₀=1/2` and `C(X₀)=-1`. Thus `A,B,C` have no common root and their gcd is constant. Gauss's lemma promotes rational-function-field irreducibility to irreducibility of the entire affine polynomial. The homogeneous polynomial is not divisible by `T`, because its restriction at infinity is the nonzero form `2X⁵-20X³Y²+10XY⁴`. No extra infinity component exists. This closes the whole-curve gap.

### The cubic and both map directions

Independently expanding `m F(s-αλ)` gives, in descending powers of `s`, precisely the four coefficients `a₀,a₁,a₂,a₃` printed in the candidate. In particular

```
a₃=(-112+48r)λ²(λ+5r)/5 ≠ 0
```

on the allowed range. Writing `w=20Y(z+γλ)/z`, then `ξ=a₃/s`, `η=ξw`, algebraically converts

```
w² = a₀s²+a₁s+a₂+a₃/s
```

to the stated monic cubic `η²=ξ³+a₂ξ²+a₁a₃ξ+a₀a₃²`.

The forward `X` recovery identity expands to `b-t²-X(a+4rt)=-4AG/h²`. For the opposite direction, an independent exact rational function calculation over `Q(√5)(z,λ)` substitutes the inverse into the entire `A Y⁴+B Y²+C` and obtains zero, then recovers the same conic branch `V-2rX=t`, the same `ξ`, and the same `η`. Therefore these are inverse function-field maps. In characteristic zero, the resulting birational map between the smooth projective curves extends uniquely to an isomorphism of their smooth projective models. Fractions failing at the finitely many boundary points do not introduce a new parameter exclusion.

The exact cubic discriminant is

```
Δ_W=2²⁴(161-72r)λ⁵(λ+5r)⁵(λ+c).
```

It is nonzero on every allowed fiber, so the entire normalization is the smooth cubic there.

### All excluded fibers

At `λ=0`, the polynomial is the verified side product, hence five distinct lines. The identity at `λ=-5r` is exactly the side product with `φ` replaced by its conjugate `(1-r)/2`; cyclotomic conjugation sends the side factors to five distinct factors (the diagonal/star ordering). Again the member is not geometrically integral genus one.

At `λ=-c`, the conic discriminant is `-64`, hence it remains nonsingular. In the shifted coordinate,

```
F(s-αλ)|_(λ=-c) = (s-8r/5)(s-1-3r/5)².
```

The numerator at `s=0` is `-48/5-112r/25`, nonzero. There is one double root and one distinct simple root. Removing the square leaves only the simple root and the pole `s=0` as odd branch points, so the second quadratic extension remains nontrivial but its normalization has genus zero. The same primitive-polynomial argument applies. Thus this fiber is geometrically integral of genus zero, not a missing elliptic component. The infinite pencil member `TQ²=0` is reducible and nonreduced.

### The allowed cusp and every vertex

At the vertex `(X,Y)=(1,0)`, put `u=X-1`, `v=Y`. The quadratic local jet is

```
(4λ+25+10r)u² -25v².
```

Thus it is an ordinary node for every finite parameter except `λ_c=-(25+10r)/4`. At `λ_c` the complete local equation independently expands to

```
2u⁵ +25u⁴/4 -20u³v² +5u³
 -135u²v²/2 +10uv⁴ -75uv² +25v⁴/4 -25v² = 0.
```

Its tangent is the double line `v=0`; the tangent restriction is `u³(5+25u/4+2u²)`. The nonzero leading pair `5u³-25v²`, with coprime exponents 3 and 2, gives a single ordinary cusp of type `A₂`, with delta invariant one. More explicitly, regarding `v²` as an auxiliary variable, the coefficient of `v²` is a unit at the origin, so formal implicit solving gives `v²=u³ H(u)` with `H(0)=1/5`, a unit; extracting its formal square root reduces to `v'²=u³`.

The exact rotation preserves the pencil and cycles the five vertices, so all five have this local type. `λ_c` is distinct from the three excluded values, and the cubic discriminant is nonzero there (the exact value is `26367187500000r-58959960937500`). Hence this is an allowed genus-one normalization. A quintic has arithmetic genus six; its five vertex singularities each have delta invariant one and the normalization has genus one. Their deltas exhaust the genus difference, so there are no other singularities on any allowed fiber.

### The origin, signed Tate twist, and infinity subgroup

At infinity on the cubic, `ord(ξ)=-2`, `ord(η)=-3`. Consequently `s` has order two and `w=η/ξ` a simple pole. At `s=0`, the inverse formulas have finite `X=X₀`, `z=-αλ`, and nonzero factors

```
z+γλ=(γ-α)λ,  a+4rt=4(3-r)λ.
```

Thus `Y` has a simple pole and the plane image is `[0:1:0]`. The plane `X` partial there is exactly ten, so that point is smooth; the stated origins agree.

Completing the square on the Tate equation gives exactly its `T_β(x)/4`. Independent expansion verifies

```
W_rhs(q(x-β)) = q³ T_β(x)/4,
q=(5+2r)k², k=4(λ+5r)/r,
(kδ)⁶=q³.
```

This proves the actual signed twist isomorphism over `K(δ)` with the candidate's coordinates. Its scale is nonzero on every allowed fiber. The discriminants also satisfy exactly `Δ_W=q⁶β⁵(β²-11β-1)`. No exceptional `j` value requires another exclusion.

The horizontal tangent at `(0,0)` has third intersection `(β,0)`, so the Tate group law gives `2P₀=(β,β²)`. The chord joining `P₀` to `2P₀` is `y=βx` and has intersection polynomial `-x(x-β)²`; therefore `3P₀=-2P₀` and `5P₀=O`. Since `β≠0`, these are distinct nonzero points and the order is exactly five.

The inverse's marked-point limits are independently computed as:

| Tate point | plane infinity slope `X/Y` |
|---|---|
| `O` | `0` |
| `(0,0)=P₀` | `r/δ` |
| `(0,β)=-P₀` | `-r/δ` |
| `(β,0)=-2P₀` | `-δ` |
| `(β,β²)=2P₀` | `δ` |

Here `(r/δ)²=5-2r`. The homogeneous infinity form factors exactly as `2ρ(ρ²-(5+2r))(ρ²-(5-2r))` in `ρ=X/Y`, and its gcd with its derivative is one. All five infinity points are smooth. Thus the marked subgroup maps to the entire infinity subgroup directly, without relying only on an automorphism classification.

For every nonmarked torsion root, the residual evaluations `R_β(0)=5β⁸` and `R_β(β)=5β¹²` were checked independently from the printed table. They exclude `x=0,β`. The exact identities

```
z+γλ=(γ-α)λ x/(x-β),  a+4rt=4r(z+γλ)
```

then make all inverse-chart denominators nonzero for those points. A possible `z=0` gives a zero numerator in the inverse rather than a pole; at that chart boundary the smooth-normalization extension handles the vertex. This establishes the claimed lack of an additional inverse-chart exclusion.

## Checkable artifacts and failure accounting

The four independent mathematical programs have final successful replays totaling 72 targeted checks, including six deliberate negative controls. They use exact polynomial/rational arithmetic, not floating point or selected parameter sampling.

| Program | Successful replay | Checks |
|---|---|---:|
| `check_geometry.py` | `runs/geometry_first/` | 31 |
| `check_pentagon.py` | `runs/pentagon_corrected/` | 26 |
| `check_inverse_and_marked.py` | `runs/inverse_marked_canonical_difference/` | 8 |
| `check_tate_boundary.py` | `runs/tate_boundary/` | 7 |

The negative controls change the conic constant, remove a numerator square, reverse the twist sign, change the infinity-square product, double the pentagon scaling, and change the residual beta exponent. Each is detected as nonzero.

Every replay has full actual stdout/stderr in binary and text form, actual argv, exit code, and separate native `/bin/date` UTC start/end records in `record.json`. No failure was replaced by a successful-output template:

- `pentagon_first` exited 1 because the reviewer harness tried unreduced transcendental exponential expressions for an exact algebraic identity, and because I incorrectly predicted a fourth-order cusp coefficient `15/4`; the actual exact coefficient is `25/4`. Both harness expectations were corrected in the next run.
- `inverse_marked_first` was terminated after symbolic expression-tree expansion failed to finish promptly; its record retains child exit `-15` and actual empty output. The exact old program is retained as `check_inverse_and_marked_failed_expansion.py`. Canonical rational-function arithmetic replaced this representation strategy.
- `inverse_marked_canonical` exited 1 on a raw comparison of rational-fraction representations. The independently verified conic-branch difference was already zero. The corrected check explicitly subtracts the recovered and target rational functions and obtains exact zero; `inverse_marked_canonical_difference` exits 0. No geometry formula changed.

The replay commands use `native_run.py --name NEW_NAME -- /Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/geometry/.runtime/bin/python SCRIPT.py`, from this directory. Each new run name must be fresh because the recorder refuses to overwrite a run.

## Strongest verified result and exact remaining gap

The candidate's entire geometric bridge is independently verified: the exact regular-pentagon normalization and scaling; the complete finite elliptic range; whole-curve geometric irreducibility; both birational directions; the signed Tate twist; every excluded fiber; the allowed ordinary cusps and absence of additional allowed-fiber singularities; agreement of origins; the exact infinity subgroup; and the claimed inverse-chart coverage of the residual points.

This family has no unresolved central geometric gap. It does not independently certify the residual division-polynomial completeness argument, external modular-source interpretations, specialization of the full division field, global Galois action, bibliography/priority, or package reproducibility. Those are separate verification responsibilities; geometry alone cannot certify them. The only concrete manuscript discrepancy found here is the minor “local conditions” attribution described above.

No git/index/queue/PR/source changes, publication, tracker actions, or communication to individuals occurred. This report is family evidence only and remains unsealed.
