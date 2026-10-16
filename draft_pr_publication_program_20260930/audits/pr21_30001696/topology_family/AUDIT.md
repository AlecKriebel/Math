# PR 21 / 30001696 — independent global topology and PL audit

## Verdict and binding

**PASS within this family’s mathematical scope.** The original candidate supplies a
semialgebraic homeomorphism for the **entire** bounded-switch complex to the
sphere–closed-ball product. Its passage to the standard PL product satisfies the
actual primary Hauptvermutung hypotheses. No fatal global-topology or PL gap was
found. The universal argument, not finite test counts, supports this verdict.

Bound head: `096aacd71a1dc6dd3a73bea3c1055877dc8c0451`.
Bound original `PROOF.md` SHA-256:
`58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`.
The immutable independent reconstruction seal and its hash are in
`INDEPENDENCE_SEAL.md` and `input_binding.json`. All 14 snapshot file hashes were
also checked against the supplied snapshot manifest. Historical review prose,
historical scripts, and sibling mathematical outcomes were not used.

This result does not establish worldwide novelty or priority, certify other audit
families, or authorize any PR action. The exact remaining gap **within this family**
is none found. External classical inputs remain explicit cited inputs; this audit
checks their actual statements, relevant proof mechanisms, and applicability.

## Original question and success criterion

The full primary EMS report was acquired; I read Klee’s complete contribution,
printed pp. 370–373. Question 4 is on p. 372. Its object is the whole `B(i,d)`
defined by at most `i` adjacent switches, not only its boundary. The audited claim is

`|B(i,d)| ≅_PL S^i × D^(d-i-1)` for all integers `d≥2`, `0≤i≤d−2`.

Klee–Novik’s primary arXiv version, Theorem 1.2 and Definition 3.1 / Lemma 3.2,
match the definition and range. Their boundary, homology and manifold results are
context. Their `i=0` case is two simplices and their `i=1` construction is already a
sphere–ball product. None is used to infer the unknown full product in higher `i`.
See the full-text source hashes, versions and locators in `primary_references.json`.

## Universal reconstruction and adversarial checks

### 1. Closed cone, zeros and spherical interior

A point on the cross-polytope’s `l1` sphere is in a face of `B(i,d)` exactly when
its nonzero coordinates admit a facet sign completion with at most `i` switches.
Deleting zeros supplies the minimal possible number: between opposite nonzero
blocks put one transition; between equal signs put none; leading and trailing
zeros add none. Hence the complete realization is precisely `s^-≤i`.

Its complement is open: an excluded point has `i+2` nonzero coordinates in
alternating sign order and those signs persist locally. Thus its intersection
`C` with the round sphere is compact. Radial normalization between the `l1` sphere
and round sphere is bijective, continuous in both directions, and semialgebraic.

Near a fixed round-sphere point, all nonzero signs persist. Every sign assignment
to its zero coordinates is realized by arbitrarily small perturbations, followed
by positive normalization. Therefore the spherical interior is exactly `s^+≤i`.
Both conditions are finite Boolean combinations of coordinate sign conditions;
`∂C=C\int(C)` is semialgebraic. This is an ambient spherical interior statement,
not a relative interior of a lower-dimensional face.

Control: `(1,0,1)` has `s^-=0`, `s^+=2`. It belongs to `C_0` but is a boundary
point. Replacing `s^+` by `s^-` in the interior claim fails immediately.

### 2. Strict trapping and linear core separation

The candidate’s additive-compound argument is sound: adjacent occupied-index
moves into a vacant neighboring index have positive wedge sign and connect all
ordered `k`-subsets. Adding a scalar identity makes the compound nonnegative;
a path term in its exponential makes every entry positive. The compound identity
then gives positive minors of `exp(tJ)`; the full determinant is positive too.
No irreducibility claim is needed for the one-dimensional full compound.

Margaliot–Sontag’s published Theorem 3 has exactly the zero-sensitive inequality
`s^+(Ax)≤s^-(x)` for a TP square matrix and every **nonzero** vector. The appendix
proves the stronger strictly-sign-regular equivalence by grouping coefficients
into consecutive sign blocks and using signed minors. Thus the use on all of `C`,
including zero strata, is legitimate. The normalized positive flow sends `C`
strictly into its spherical interior. TN or weak variation alone would not do so.

For `E`, polynomial evaluation of degree at most `i` with positive coordinate
weights has `s^+≤i`. If a completed sign pattern contained `i+2` alternating
positions, the degree-`≤i` interpolation identity on those nodes would have all
nonzero summands of the same sign. At least one summand is nonzero: such a
polynomial cannot vanish on `i+2` distinct nodes. Contradiction. This explicitly
handles roots at nodes and leading/trailing zero coordinates.

For `F`, any nonzero vector with `s^-≤i` has a polynomial of degree `≤i` whose
roots lie between its opposite-sign nonzero blocks and whose signs agree with
all its nonzero entries. Positive weighted evaluations lie in `E` and have
strictly positive dot product with that vector, contradicting `F=E^⊥`.
Consequently `A=S(E)⊂int(C)` and `B=S(F)∩C=∅`. This establishes actual geometric
separation of explicitly linear spheres, without an embedding classification.

### 3. Global cross-section and uniformity

Write `r=i+1`, `N=d−1`; the E indices are `0,…,r−1` and F indices `r,…,N`.
For any point with both components nonzero, let `R=||F||/||E||`. For the
integer-power action `ψ_a`, direct differentiation yields

`d log R(ψ_a x) / d log a = mean_F(k) − mean_E(k) ∈ [1,N]`.

The means use positive squared spectral-component weights. The gap is at least
one even when most components vanish. It follows that every such orbit crosses
`Σ={R=1}` exactly once, with the parameter increasing from zero to infinity.
For `s∈Σ`, integration gives

`a^N≤R(ψ_a s)≤a` when `a≤1`, and `a≤R(ψ_a s)≤a^N` when `a≥1`.

`Σ` is the compact product `S(E)×S(F)`, with each component scaled by `1/√2`.
For inverse continuity, choose two parameters straddling the unique crossing of
a given point. The two strict inequalities persist for nearby points, bracketing
their crossings. Arbitrarily tight brackets prove continuity. There is no hidden
proper-map theorem, smooth boundary, implicit isotopy or connectedness premise.
The graph of the inverse is the graph of the bijective semialgebraic `Γ` with
factors exchanged; no logarithm is used to define this inverse.

Uniform distance estimates are explicit:

`dist(x,A)^2=2−2/√(1+R^2)` and
`dist(x,B)^2=2−2R/√(1+R^2)`.

Compactness of `A⊂int(C)` and `B∩C=∅` supplies uniform allowed small `R` and
forbidden large `R`. The spectral bounds make the corresponding orbit parameters
uniform over **all** of `Σ`, including its disconnected components.

### 4. Closed lower intervals and the hitting graph

Fix `s`. Uniform separation makes the orbit membership set nonempty and bounded
above. If `Γ(s,a_2)∈C`, then for every `0<a_1<a_2`,

`Γ(s,a_1)=ψ_(a_1/a_2)(Γ(s,a_2))∈int(C)`.

This is where **strict** trapping is used. Membership is a lower interval; because
`C` is closed, its finite positive supremum belongs to it. The interval is
`(0,β(s)]`. Every lower point is interior. The endpoint cannot be interior, since
orbit continuity would extend membership beyond the supremum. Higher points are
in the open complement. Therefore the endpoint is exactly the unique boundary
point on the orbit.

For continuity of `β`, choose lower and upper parameters arbitrarily close to
`β(s)`. Their interior and exterior memberships persist for nearby `s`, bracketing
the new endpoint. This proves continuity without assuming a differentiable or
transverse boundary. Its graph is `Γ^−1(∂C)`, so it is semialgebraic. Compact `Σ`
then gives `0<min β≤max β<∞`.

A falsification control shows the strict premise is substantive. On `S²` use the
same distinct spectral indices `(0,1,2)`, E the first two coordinates, and

`C_spike={z²≤x²+y²} ∪ {y=0, x≥0, z≥0, z≤4x}`.

It is compact, semialgebraic, contains a neighborhood of the E sphere, misses the
F sphere, and is invariant under `diag(1,b,b²)` for `0<b<1`. On the exceptional
orbit `s=(1,0,1)/√2`, the endpoint parameter is 2; on every other nearby section
point it is 1. Hence `β` jumps. Every spike point with `1<z/x≤4` is a boundary
point, so a single orbit has many boundary points. Non-strict trapping cannot
replace the candidate’s premise.

### 5. Identity cutoff and the actual product

Choose a **rational** `0<ε<min(1,min β)`; density of the rationals suffices.
The candidate’s two pieces of `h_s` agree at `ε`. Each is strictly increasing,
with endpoint values `h_s(ε)=ε`, `h_s(β(s))=1`, and the stated continuous inverse.
Joint continuity and semialgebraicity follow from continuous semialgebraic `β`
and the strictly positive denominator `β(s)−ε`.

The entire ambient open set

`U={x∈S^(d−1): ||F(x)||<ε^N ||E(x)||}`

lies in both `C` and `D_E`, and both `H` and `H^−1` are the identity on `U`.
Indeed, `R<ε^N` forces orbit parameter `<ε` by the uniform spectral bounds;
the inverse parameter also stays unchanged below `ε`. This checks both directions
at every core point. No limiting E direction, bundle-triviality assumption or
boundary isotopy is hidden in the extension.

The cutoff is essential for the specified identity extension. A stronger control
satisfying strict trapping uses

`C_strict={z≥0, z²≤16x²+4y²} ∪ {z≤0, z²≤x²+y²}` on `S²`.

Under `diag(1,b,b²)`, each defining boundary inequality becomes strict for `b<1`.
Its hitting function is the continuous semialgebraic function 2 on the positive-F
section component and 1 on the negative-F component. The naive rescaling
`a↦a/β(s)` equals `ψ_(1/2)` on the positive side and the identity on the negative
side. At `u=(1,1,0)/√2`, paths proportional to `(1,1,±1/n)` converge to `u`, but
their rescaled limits are respectively proportional to `(1,1/2,0)` and `(1,1,0)`.
Thus no single continuous core extension exists. The candidate’s uniform cutoff
fixes both paths eventually and removes this obstruction.

Finally, the map `(u,v)↦(u+v)/√(1+||v||²)` from `S(E)×D(F)` onto `D_E` has the
actual inverse `(y+z)↦(y/||y||,z/||y||)`. On `D_E`, `y` is never zero. The inverse
works at `v=0`, at `||v||=1` and everywhere between. This is a full product map,
not identification of a boundary, homology class or possibly twisted disk bundle.

### 6. Semialgebraicity and the precise PL input

The spectral matrices have algebraic coefficients: rational polynomial
eigenvectors are multiplied by positive square roots of binomial coefficients
and normalized by positive algebraic norms. Spectral projectors are algebraic.
All powers in `M_a` are nonnegative integer powers, so its normalized graph is
semialgebraic for `a>0`. The relation to real flow time is used only to deduce
trapping; the logarithm/exponential never becomes part of the constructed graph.

This matters. Algebraic eigenvalues alone would not justify the same argument
for arbitrary spectra. The graph of `a↦a^√2` is not semialgebraic: a semialgebraic
function on an interval must satisfy a nonzero polynomial relation on some
subinterval, while the terms `a^(m+n√2)` have distinct exponents and are linearly
independent (put `a=e^t` and use a Vandermonde derivative system). The candidate
avoids this false variant using its arithmetic spectral progression.

Round spheres and balls are not polyhedra. Use the boundary and the whole ball
of coordinate cross-polytopes in algebraic orthonormal E/F coordinates. The E
boundary maps radially to `S(E)`. For the F ball, the radial map
`q↦(||q||_1/||q||_2)q` for `q≠0`, with `0↦0`, maps the `l1` ball to the round
ball; its inverse is `v↦(||v||_2/||v||_1)v`. Norm comparison proves continuity
at zero in both directions. A product of these finite polyhedra has a standard
finite staircase triangulation. The source is the original finite simplicial
cross-polytope subcomplex. Thus the constructed composition links **compact
polyhedra** by a **semialgebraic homeomorphism** to the standard PL product.

The primary Shiota–Yokoi theorem 4.1 (p.737) converts a locally subanalytic
homeomorphism of polyhedra to a PL homeomorphism; corollary 4.3 gives uniqueness
of such triangulations, including the semialgebraic case. Definition 6.1 (p.746)
uses the graph criterion. In the compact pure-dimensional case, theorem 4.4
(p.738) also applies directly. Its proof (lemmas 4.5–4.8, proof 4.9, pp.738–745)
stratifies the graph, compares smooth cutouts, obtains PL balls/cones, then extends
by induction using the Alexander trick. Smooth cutouts belong to that theorem’s
proof; they are not added hypotheses on the candidate. No manifold classification,
connectivity, orientation or supplied isotopy is required. HLTV’s published theorem
2.6 (p.2485) independently states the exact compact semialgebraic formulation
used in the candidate. An arbitrary topological homeomorphism would not meet it.

### 7. Endpoints and dimensional controls

- `i=0`: `E` is a line and `S(E)=S^0`. The proof preserves both product components;
  compactness does not require connected `Σ`. The original complex is two simplices.
- `i=d−2`: `F` is a line and `S(F)=S^0`. The two section components can have different
  hitting values; the global minimum and identity cutoff still work.
- `d=2,i=0`: both factors of `Σ` are `S^0`, giving four section points. In the E/F
  basis, original signs are `(u+z,u−z)`. Cone membership is exactly
  `(u+z)(u−z)≥0`, or `|z|≤|u|`; the product is two closed intervals with four endpoints.
- `i=d−1`: F is zero and the cross-section construction is deliberately inapplicable.
  The original complex is the entire standard cross-polytope sphere, giving
  `S^(d−1)×D^0` directly. In particular `d=1,i=0` gives `S^0×D^0`.

## Supplementary computations and limitations

`countermodel_controls.py` was written independently after the seal and imports
only Python’s standard library. It confirms the controls above and checks exact
rational cross-section identities, derivative gaps, uniform ratio bounds, inverse
action, cutoff inverses and the smallest disconnected endpoint. It covers
`d=2,…,11`, all nontrivial splits, eight unrelated rational section points per
split and eight rational flow parameters. `countermodel_results.json` records
**17,984 exact assertions**, all passing. This number is bookkeeping, not evidence
of an all-dimensional topological theorem by itself.

No numerical root solver, floating point limiting argument, old verification code,
historical review conclusions or sibling result was used to establish this verdict.
The primary foreign fulltexts remain under ignored `tmp/`; only first-party audit
notes, exact controls and metadata are intended for integration. No external person
was contacted and no Git, PR, publication, installation or source-folder edit was
performed by this family.
