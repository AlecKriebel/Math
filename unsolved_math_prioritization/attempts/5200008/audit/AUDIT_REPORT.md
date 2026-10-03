# Independent mathematical audit: positive reflection-word density

Problem **5200008 / AMR-051-0008**, rank 542. Audit date: **2026-10-03 UTC**.

## Verdict

**PASS AS A SCOPED UNSOLVED ATTEMPT.** Retain `unsolved`, `5/5`, and `full_resolution: false`.

No blocking mathematical error was found in the retained conditional reduction or restricted obstructions. None proves or disproves density for arbitrary allowed small deformations. The essential missing assertion is still approximation of the base inverse by positive words, or a closed obstruction covering every permitted deformation and unbounded word length.

All nine frozen input files were checked, including the manifest itself. Their bytes were not changed. The author verifier was rerun and reproduced the stored JSON byte for byte. A separate implementation reconstructed all **1,682 exact rational controls**, with identical category counts and every check passing. These finite checks do not establish any analytic limit or optical realizability.

This is an independent computational and mathematical review, not a formal proof-assistant certificate or human peer-review claim. It makes no historical novelty or priority claim.

## Frozen scope and reproducibility

- Frozen `SHA256SUMS`: `6606805c3645c25ba166e3d99568ea563205920772d662f5565d015c4984c7ad`.
- Frozen `PROOF.md`: `1022937b6167c1f16879f86545b4c22d0c5b7fea685e90efc2db94273f046a34`.
- `FROZEN_INPUTS.json` records the names, byte lengths, and hashes of all nine input files.
- `author_replay.json` is the reproduced author output.
- `independent_controls.py` uses only Python's standard library and imports no author code. Run `python3 independent_controls.py` and compare with `independent_controls.json`.
- `AUDIT_MANIFEST.json` records this disposition and hashes the other audit deliverables. The audit's own `SHA256SUMS` covers all audit deliverables except itself.

No repository changes or remote writes were made. Full source papers, source extracts, and background records are not redistributed here.

## 1. Target and source gate

The literal target matches Alexey Glutsyuk's Problem 2, PDF pages 6–7 of [Bialy et al., arXiv:2110.10750v2](https://arxiv.org/abs/2110.10750v2). It quantifies over each positive deformation tolerance and each finite smoothness order, and asks for smooth approximation of every Hamiltonian self-map by reflection compositions. The accompanying distinction from inverse-allowed compositions is essential. The audit verified the primary question rather than inferring a theorem from a catalogue status label. Direct catalogue access was not independently established.

[Glutsyuk, arXiv:2005.02657v5](https://arxiv.org/abs/2005.02657v5), revised September 16, 2025, supplies the invoked Lie-algebra result and the inverse-allowed pseudogroup conclusions. Definition 1.2 permits domains exhausting the target domain; Section 1.6 still asks the positive-word question. Theorem 1.1, Theorem 1.13, Theorem 1.5, Corollary 1.7, and the flow/closure passage in Section 4.1 were inspected. The substantial Lie-algebra theorem remains an explicitly attributed mathematical input, not a result certified by the finite verifier.

The optical-transformation question on pages 19–20 of [Albach et al., arXiv:2602.12896v1](https://arxiv.org/abs/2602.12896v1) concerns characterization and supplies no removal-of-inverses theorem. The source PDF hashes agree with the frozen `SOURCE_HASHES.json`. This is a bounded source and scope check, not an exhaustive certificate that no later resolution exists. Repository-search absence and duplicate-search claims are outside this mathematical audit's independent certification.

## 2. Reflection geometry and circle coordinates

The last-intersection convention was checked against the primary definition. Tangent-hyperplane reflection is an involution at one collision point; the induced billiard map need not use that collision point again. This distinction is correctly preserved.

For a line direction `u` and perpendicular foot `q`, orientation reversal sends `(u,q)` to `(-u,q)`. Therefore the one-form `q·du` and its differential change sign. The identity `T^{-1}=J T J` does not express the inverse as a positive word. A symplectic-map sequence cannot converge in `C^1` to this anti-symplectic `J` on a nonempty positive-dimensional open domain. This does not exclude approximating the entire symplectic composite by some other words.

For a circle, the collision computation gives the claimed rotation

`alpha_R(p) = -2 arccos(p/R)`

and preserves the signed momentum. Its derivative is `2/sqrt(R^2-p^2)`. Differentiating the displayed `H_R` gives exactly `alpha_R`; the chosen Hamiltonian convention therefore yields the asserted time-one map. The inverse Hamiltonian is valid throughout the open cylinder. Cutting it off on a momentum neighborhood preserves the target on the compact band because momentum stays fixed. Neither the proof nor this audit requires regularity at grazing.

The independent controls calculate reflections as Gaussian-rational operations `u'=-x^2 conjugate(u)/R^2`. Outgoing momentum is recomputed from the collision, rather than carried through as an assigned variable. First-endpoint inversion, reversal, and the noninvolution witness all pass.

## 3. Angular lifts and uniform nonrecurrence

### Positive powers

For an exponent `m`, the real angular lift varies by `4m arcsin(a/R)` across the band. Once this reaches a full turn, the image interval necessarily contains an odd multiple of pi. Thus the uniform angular distance from identity is exactly pi at the asserted threshold. A sequence of exponents tending to infinity cannot approximate identity, and a bounded sequence has a constant subsequence. No fixed positive exponent is identity on a momentum interval, because its shear derivative is strictly positive.

The reduction from inverse approximation to identity recurrence is valid because the base map preserves the same compact band. Pointwise recurrence on a fixed momentum circle cannot replace this simultaneous compact-band estimate.

### Concentric words

The word and target have globally defined real displacement lifts on the momentum interval. If their angular distance were smaller than `2 arcsin(a/R_0)`, it would in particular be smaller than pi. The integer selecting the nearest lift is then unique and locally constant, hence constant on the connected interval. It cannot jump by a full turn to defeat the endpoint comparison.

The positive word's lift is nondecreasing and the inverse target's lift decreases by `4 arcsin(a/R_0)`. The claimed uniform lower bound follows. It covers the empty word and all finite lengths. The normal-incidence derivative gap also follows directly. This proof uses genuine continuum uniformity; the finite tests are not being substituted for it.

Neither this invariant momentum nor this triangular derivative form is shared by general nonsymmetric deformations. The frozen note makes that restriction explicit and does not use this result as a negative answer to the original question.

## 4. One-inverse conditional reduction

The hypothesis must hold **inside the positive-word closure for each fixed prescribed deformation neighborhood**. It is not enough to approximate the inverse pointwise, on unrelated isolated rays, or using deformations outside that neighborhood.

Under that hypothesis, the following steps are valid:

1. For a fixed smooth normal deformation and a fixed compact set away from grazing, a sufficiently small parameter makes the reflection branch smooth and places its compact image inside the base phase cylinder. Approximate the base inverse on a compact neighborhood of that image. This proves the required local membership of `E_s=T_gamma^{-1} T_gamma_(s,f)` in the positive-word closure.
2. The exact compositional inverse relation with `D_s=T_gamma_(s,f)^{-1} T_gamma` gives `E_s=Id-s v_f+O(s^2)` at each finite derivative order. Both signs of the deformation are available. No inverse of a deformed mirror has thereby been silently granted as an allowed word.
3. On a compact trajectory neighborhood, Euler iteration gives the thin-film flows of both time signs. For each fixed finite iteration, the approximations of the inverse can be chosen as accurate as needed before taking the iteration limit. Closure idempotence handles this nested approximation. The argument does not assume a word-length bound uniform in the Euler parameter.
4. The stated commutator ordering has leading term `+h^2[X,Y]` with the note's bracket convention. The scaling `h=sqrt(t/N)` is correct: accumulated leading time is `N h^2=t`, and the accumulated cubic remainder is `O(N^(-1/2))`. Reversing the two fields supplies the other sign. Trotter products and time rescaling give sums and real multiples.
5. The attributed Lie-algebra density, smooth dependence of flows on compact trajectory neighborhoods, autonomous time discretization, and a diagonal exhaustion give the target Hamiltonian maps. Approximating domains may vary and eventually contain each compact set. No map is asserted to remain smooth over all grazing directions simultaneously.

The commutator sign was independently tested with homogeneous affine matrices for `X=partial_x` and `Y=x partial_y`; the displacement is exactly `h^2 partial_y`. The analytic square-root scaling was checked separately, rather than inferred from those finite samples or copied uncritically from a displayed source formula.

For moving Hamiltonian domains, the cutoff should be understood as a smooth spacetime cutoff on a neighborhood of `{(F_t(x),t): x in K, 0<=t<=1}`, or equivalently a cutoff pulled forward from the initial domain. Its zero extension is then smooth. A single spatial cutoff supported in every moving domain is not required. This is a clarification of the compact-domain argument, not a blocking defect in the claimed self-map result or its standard local extension.

For a round base circle the inverse is explicitly Hamiltonian, so necessity and sufficiency both hold. For a general hypersurface only sufficiency is asserted. The note does not assume every billiard map is Hamiltonian.

## 5. Bounded words and the linear counter-control

For each fixed maximum length `M`, the implicit-function argument on a slightly wider momentum band gives uniform `C^1` continuity of reflection maps under `C^2` normal perturbations. Finite-composition continuity and finitely many lengths provide a single positive tolerance `delta_M`. The derivative estimate at normal incidence is sufficient for the claimed supremum bound. Angular derivatives are independent of adding an integer multiple of a full turn to a local lift.

The quantifier order is decisive: `for every M there exists delta_M`. There is no tolerance independent of `M`, and no resulting bound for arbitrary lengths at one fixed neighborhood. An approximation along shrinking neighborhoods would have to use diverging lengths, which remains possible.

For the matrix family, determinant one and trace `2 cos(2pi/N)` give the distinct eigenvalues `exp(±2pi i/N)` for every `N>=3`. Thus `A_N^N=I`, its `(N-1)`st positive power is its inverse, and that inverse has negative upper-right entry. The family tends to the positive shear as `N` tends to infinity. The exact rational cases `N=3,4,6` were independently checked by Cayley–Hamilton recurrence, not by the author's repeated-multiplication implementation.

This disproves a matrix inference based solely on proximity to a positive shear. It supplies no billiard mirror realization, no simultaneous derivative field on a compact band, and no global cylinder map. The frozen statement correctly declines all of those stronger conclusions.

## 6. Final disposition and limits

The five recorded approaches are substantive and their failure boundaries are accurately described. The packet has retained valid partial arguments while identifying the exact unresolved step.

- Blocking findings: **0**.
- Required mathematical changes to the frozen packet: **none**.
- Optional clarification: make the spacetime cutoff in the moving-domain extension explicit if the note is later revised.
- Author exact controls reproduced: **1,682 / 1,682**, byte-identical output.
- Independent exact controls: **1,682 / 1,682**, same category counts.
- Full positive-word density: **not established**.
- General nondensity for arbitrary deformations: **not established**.
- Base-inverse approximability and optical realization of the matrix model: **not established**.

The warranted disposition remains **unsolved after five attempts**, with the same frozen mathematical scope.
