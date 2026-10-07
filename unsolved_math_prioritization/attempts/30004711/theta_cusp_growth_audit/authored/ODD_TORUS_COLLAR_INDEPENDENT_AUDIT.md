# Independent audit of the odd elliptic cusp correction

Problem 30004711. Audit date: 7 October 2026.

## Verdict and pinned scope

**Accept the mathematical correction in the frozen Approach 4, with its stated limited scope.** The actual odd-spin once-NS-punctured elliptic family supplies a nonvanishing extending frame whose Petersson squared norm diverges. Both uniform comparison estimates are valid. The harmonic-removability argument correctly excludes a bounded-coefficient extension of the corresponding Chern curvature, including after a finite ramified spin-chart base change.

Frozen target: `AUTHOR_APPROACH_4_ODD_TORUS_COLLAR.md`, 10,912 bytes, SHA-256 `cded43f4a42ce5bbaa8d06c1f6deae2540ba413f60adf9643b199f1a935414b0`.

Precisely, for the period-one frame and curvature-minus-one surface metric used in that file,

\[
\frac{2(T-2)^2}{\pi^2}\leq M(a+iT)\leq C T^2\log T,
\qquad |a|\leq\tfrac12,
\]

for sufficiently large `T`. Consequently the positive metric does not extend continuously and nondegenerately on the specified compactified line, and its Chern curvature does not extend with bounded coefficients in an ordinary holomorphic chart at the cusp.

This rejects the **strong smooth-metric and smooth-form step of the inspected proofs**. It does not disprove a current-level characteristic-class statement, the stated volume/intersection-number identity, or a torsion-volume identity. The audit does not supply the missing finite-flux theorem or torsion-representative comparison. It makes no novelty or comprehensive literature claim.

The target and earlier authored files were read without modification. Nothing was published, committed, or pushed.

## 1. Which bundle and boundary point are being tested

Let `B` be the odd component of the unrigidified compactified spin stack in genus one with one NS marking. Let `ρ:𝒞→C` forget the fiberwise twisted-curve structure, let `π:C→B` be the coarse-fiber universal stable curve, and let `p` be its marked section. The base remains the spin stack. Put

\[
F=R^1(\pi\rho)_*\theta^\vee,\qquad
\lambda=\pi_*\omega_{C/B}.
\]

These are the algebraic bundle convention and twisted-spin construction appearing in Norbury's Definition 2.3, [2005.04378v4, pp.9–10](https://arxiv.org/pdf/2005.04378v4), and in the later paper's definitions. The NS character is nontrivial; a Ramond nodal character is trivial. Duals are tracked explicitly here.

### The odd degeneration is locally free at a Ramond node

The period family `Cτ=ℂ/(ℤ+τℤ)` has the unique odd theta characteristic, the trivial line. Its Tate degeneration has an irreducible nodal genus-one central fiber. The relative dualizing line on this fiber is trivial, generated on its normalization by `du/u`, with opposite residues at the two branches.

There is an especially direct way to identify the relevant extension, without relying only on the smooth-fiber parity label. On a local base chart, choose the extending nonzero invariant differential `α`. The line with generator `e` and square-root map `e²↦α` is a locally free square root of the relative dualizing sheaf throughout this family. Adding the NS root divisor gives the required twisted log-spin structure. At the node it has trivial character, so it is the Ramond extension. On smooth fibers its theta line is trivial, hence odd.

The alternative description by normalization gives the same answer. The two locally free square roots at an irreducible nodal genus-one curve have gluing constants `+1` and `−1`; only `+1` has a section. The non-locally-free alternative is even. The explicitly stated odd-to-Ramond degeneration is also confirmed independently in [Norbury, 2608.25237v2, p.40](https://arxiv.org/pdf/2608.25237v2). That page was visually checked; its numerical volume assertions are not needed here.

### Descent and the absence of a hidden boundary twist

Let `P` be the marked divisor on `𝒞`, with `2P=ρ*p`. Since `θ` has the nontrivial character at `P` and the trivial character at the node, `θ(−P)` has trivial stabilizer characters everywhere and descends to a line `ℓ` on `C`. Thus

\[
\theta=\rho^*\ell\otimes\mathcal O(P),\qquad
\ell^2=\omega_{C/B},\qquad
\rho_*\theta^\vee=\ell^\vee(-p).
\]

For the last identity, the invariant pushforward of `O(−P)` is `O(−p)`. At a local NS chart `x=z²`, the nontrivial character forces an invariant section to contain the factor `z`; its product with the corresponding dual generator contains `x`. At the Ramond node the character is trivial, so there is no additional character correction there. Exactness of invariant pushforward is valid in characteristic zero.

On the odd family `ℓ` is trivial on every geometric fiber, including the central nodal fiber. Cohomology and base change make `H=π_*ℓ` a line, and fiberwise evaluation proves `ℓ≅π^*H`. Likewise the evaluation map gives `ω_(C/B)≅π^*λ`: the nonzero nodal dualizing differential has no zero as a section of that dualizing line. Pulling the square relation back along `p` gives `H²≅λ`.

The exact sequence `0→O(−p)→O→Op→0` identifies `R¹π_*O(−p)` with `R¹π_*O`, because `π_*O→π_*Op` is an isomorphism. Relative Serre duality, valid for this nodal Gorenstein family, identifies the latter with `λ⁻¹`. Therefore

\[
F=H^{-1}\otimes\lambda^{-1}=H^{-3},\qquad F^\vee=H^3.
\]

These are boundary-valid line identities, not merely identities after restriction to the open moduli space. In particular the potential objection that the proposed frame differs from an extending frame by a nonzero power of the plumbing parameter is excluded.

### The actual frame

For `q=exp(2πiτ)` and `u=exp(2πiz)`, the normalized invariant differential is

\[
\alpha=dz=\frac{1}{2\pi i}\frac{du}{u}.
\]

It extends to a nonzero dualizing differential at the Tate node. On a local spin chart, its chosen square root gives a frame of `H`, and

\[
s_\tau=(dz)^{3/2}
\]

is the corresponding nonzero extending frame of `F∨=H³`. On the smooth coarse curve, Serre duality also identifies this with the constant-coefficient section of `K^(3/2)(p)`. There is no independent meromorphic function with a single simple pole at `p` on an elliptic curve; the space is one-dimensional.

A stabilizer action on the frame is harmless. Work in an ordinary chart carrying it. If that chart has parameter `b` with `q=bᵏ` times a unit, the logarithmic growth and every contradiction below remain valid. Neither the coarse modular curve nor its Hodge line is being asserted to possess a global ordinary square root.

## 2. The metric being computed

On `Στ=Cτ\{0}`, write the complete curvature-minus-one metric as

\[
h_\tau=\rho_\tau(z)^2|dz|^2.
\]

The Petersson pairing of 3/2 differentials is defined in [2005.04378v4, equation (40), p.36](https://arxiv.org/pdf/2005.04378v4), and [2312.14558v3, Definition 2.3, equation (11), p.8](https://arxiv.org/pdf/2312.14558v3). In the candidate's area convention it gives exactly

\[
M(\tau)=\|s_\tau\|^2=\int_{\Sigma_\tau}\rho_\tau^{-1}\,dx\,dy.
\]

The norm is finite for each fixed `τ`. At the marked cusp the reciprocal density tends to zero, and `sτ` has no pole in the original smooth elliptic coordinate. The question is the behavior as the surface degenerates, not existence of a single-fiber integral.

A different fixed normalization of the area convention would multiply all squared norms and both comparison constants by the same positive constant. It would not change any extension or curvature conclusion. The metric on `F` is the inverse metric, with opposite Chern curvature; no torsion metric has been identified by this calculation.

## 3. Independent verification of the comparison bounds

### Area lower bound

The flat area of a period parallelogram is `T`. Gauss–Bonnet gives hyperbolic area `2π` for a once-punctured torus. Hölder with exponents `3/2` and `3` yields

\[
T=\int(\rho^{-1})^{2/3}(\rho^2)^{1/3}
\leq M^{2/3}(2\pi)^{1/3}.
\]

Thus `M≥T^(3/2)/√(2π)`. This already obstructs a finite positive limit in the verified extending frame.

### Long-cylinder lower bound

The cylinder `A={1<Im z<T−1}/ℤ` embeds in `Στ`. Its imaginary width is less than `T`, so no translate by a nonzero multiple of `τ` identifies two of its points; it contains no lattice puncture. Set `Y=T−2`.

The complete curvature-minus-one density of this cylinder is

\[
\rho_A(z)=\frac\pi Y\csc\!\left(\frac{\pi(\operatorname{Im}z-1)}Y\right).
\]

For example, exponentiating the strip to the upper half-plane gives this formula immediately. Schwarz–Pick for the inclusion gives `ρτ≤ρA`, which is the correct comparison direction. Hence

\[
M\geq\int_0^1\int_0^Y\frac Y\pi\sin(\pi y/Y)\,dy\,dx
=\frac{2Y^2}{\pi^2}.
\]

The embedding, density, comparison direction, and integral are uniform in `|a|≤1/2`.

### Fixed-comparison upper bound

The cover `Uτ=ℂ\(ℤ+τℤ)→Στ` pulls back the complete hyperbolic metric. Since the omitted lattice always contains `0` and `1`, there is an inclusion

\[
U_\tau\subset U=\mathbb C\setminus\{0,1\}.
\]

Schwarz–Pick now gives `ρUτ≥ρU`, so `1/ρτ≤1/ρU` on a fundamental domain. This is again the correct direction. The standard cusp asymptotic at infinity gives the candidate's global bound

\[
\rho_U(z)^{-1}\leq C(1+|z|)\log(2+|z|).
\]

There is also a source-pinned global estimate that avoids any need to leave the unspecified cusp constant implicit. [Kim, Ma and Ma, *Estimates of the hyperbolic metric on the twice punctured plane*, equation (1.3), printed p.876 / PDF p.2](https://www.acadsci.fi/mathematica/Vol40/vol40pp875-887.pdf), gives

\[
\rho_U(z)^{-1}\leq |z|\bigl(|\log|z||+K\bigr),
\quad K=\Gamma(1/4)^4/(4\pi^2).
\]

The authors explicitly use curvature `−1` and the usual domain-monotonicity convention. They attribute this bound to Hempel and Jenkins. For `R=T+2`, the standard parallelogram has area `T` and lies in `|z|≤R`. Since `r|log r|≤1/e` for `0<r≤1`, and `r log r` is increasing for `r≥1`, the displayed bound gives the explicit sufficient estimate

\[
M(\tau)\leq T\{R(\log R+K)+1/e\}=O(T^2\log T).
\]

This independently validates the candidate's upper comparison with a constant independent of `a`. There is no claim of a sharp leading asymptotic or an upper bound of order `T²` alone.

## 4. Logarithmic growth and curvature obstruction

The estimates imply

\[
\log M=2\log T+O(\log\log T)
\]

uniformly around the cusp. For `t=log(1/|q|)=2πT`, put `u(q)=log M`. Then `u→+∞`, while `|u|=O(log t)=o(t)` uniformly in argument.

### Positive continuous extension

A positive continuous Hermitian metric in a nonzero extending holomorphic frame has a finite strictly positive value at the center of the chart. The divergence of `M` contradicts that property. Its inverse tends to zero, so the inverse metric also has no positive nondegenerate continuous extension. Smooth extension in that sense is therefore impossible.

### Bounded curvature coefficients

Assume that `∂bar∂u` has bounded coefficients near the puncture. Equivalently its real Laplacian is represented on the punctured disk by a bounded function `f`. Extend `f` over the point and use a compactly supported logarithmic potential

\[
v(z)=\frac1{2\pi}\int f(\zeta)\log|z-\zeta|\,dA(\zeta).
\]

After restricting to a smaller disk, this is a bounded potential satisfying `Δv=f`. Consequently `w=u−v` is harmonic off zero. The two-sided uniform growth estimate makes `w=o(log(1/|z|))`.

For completeness, removability can be proved without assuming a convergent negative-power expansion. Fix an outer circle of radius `R` and let `H` be the harmonic extension of `w` from that circle to the full disk. For every `ε>0`, the sublogarithmic bound ensures

`|w−H|≤ε log(R/r)`

on sufficiently small inner circles `|z|=r`. The functions `±(w−H)−ε log(R/|z|)` are nonpositive on both boundaries of the corresponding annulus. The maximum principle makes them nonpositive throughout. Let the inner radius tend to zero and then let `ε→0`; this gives `w=H`. Thus `w` is bounded, and so is `u=w+v`, a contradiction.

This proves precisely that the actual Chern curvature has no bounded-coefficient extension. It does not rely on differentiating either comparison inequality. In rank one the ordinary complex-oriented Euler form is a fixed nonzero scalar multiple of that curvature, so the same obstruction applies to that actual form. The sign from passing to the dual does not affect boundedness.

If a finite base change is needed, repeat the same argument for `u(bᵏ)`: it remains unbounded and uniformly sublogarithmic in `log(1/|b|)`. Thus the obstruction is valid on the genuine spin chart, not just on the coarse plumbing disk.

## 5. Direct check at the Ramond branch

There is a local explanation for the discrepancy with the source's pole argument. At the central Ramond node, the coarse spin line is a square root of the **dualizing** line. On a branch with coarse coordinate `u`, the latter is generated by `du/u`. The limiting section therefore has the intrinsic form

\[
s_0=c\,(du/u)^{3/2},\qquad c\ne0.
\]

The notation records the square-root bundle; it does not claim that an ordinary single-valued square root of the scalar `1/u` exists. The normalization is a punctured sphere with its complete hyperbolic density comparable to `1/(r log(1/r))`. Its contribution to the pairing is consequently comparable to

\[
\frac{\log(1/r)}{r^2}\,dA,
\qquad\text{whose radial integral is }
\int_0^\epsilon\frac{\log(1/r)}r\,dr=\infty.
\]

Thus local freeness or a trivial stabilizer character does not make the relevant 3/2-differential norm integrable at this internal node. A half-canonical line on the normalization without the two nodal log terms would be a different line. The collar calculation has already established the obstruction on the smooth family, so this central-fiber observation is corroboration rather than a necessary limiting-interchange assumption.

## 6. What was verified in the two source proofs

Both PDFs were downloaded afresh in this audit. Their bytes match the previously archived versions exactly. Relevant pages were read as extracted text and rendered images, not inferred from abstracts or search snippets.

1. [Norbury, *Enumerative geometry via the moduli space of super Riemann surfaces*, 2005.04378v4](https://arxiv.org/pdf/2005.04378v4): §3.4.1 introduces Theorem 6 by explicitly making smooth metric extension its mechanism. The proof on PDF/printed pp.37–38 treats the Ramond nodal pole as removable and concludes smooth extension of the pairing and its Chern Euler form. Remark 3.21 on pp.38–39 reinforces that claimed contrast with the Weil–Petersson metric. Theorem 6's final formulation is a characteristic-class identification; the stronger regularity step is explicit in its proof.

2. [Norbury, *Super Weil-Petersson measures on the moduli space of curves*, 2312.14558v3](https://arxiv.org/pdf/2312.14558v3): §3.1.1 and Theorem 3.3, PDF/printed p.11, use the same smooth-extension mechanism for the dual bundle's Hermitian pairing, again distinguishing NS and Ramond nodal behavior in that way. This is not merely an assertion that some abstract smooth representative of the class exists.

The verified family contradicts those strong regularity assertions. It does not follow that the final characteristic-class result is false under an appropriate singular/current interpretation. This audit has not checked all possible replacement proofs or all subsequent treatments.

## 7. Residue and integration remain separate questions

Because `u=O(log log(1/|q|))`, it is locally integrable. Therefore its distributional `∂bar∂` defines a current extension of the curvature on this chart. This is compatible with the candidate's explicit limitation. The argument does not prove that this current has locally finite total variation, is positive, or equals an extension by zero of an absolutely integrable ordinary form.

Let `m(t)` be the angular average of `u(e^(−t+iθ))`. It is `O(log t)`. The relative Chern boundary flux is a fixed convention factor times `m′(t)`, plus a term tending to zero from any smooth reference metric. If the flux has a finite limit, then `m′(t)` has a finite limit, and averaging its derivative gives the same limit for `m(t)/t`. The latter tends to zero. Thus any existing finite flux limit is zero, exactly as asserted.

Existence does not follow from the bounds. For example `2 log t+sin(t²)` is uniformly sublogarithmic and differs from `2 log t` by a bounded amount, while its derivative has no limit. This is a logical counterexample to differentiating growth bounds, not a proposed formula for the actual Petersson norm.

Absolute integrability of the actual curvature would make fluxes Cauchy by Stokes on shrinking annuli and would be a sufficient additional hypothesis. A controlled derivative expansion would also suffice. Neither has been proved in Approach 4 or this audit. Comparison with a torsion-induced connection needs a further actual connection/metric/retraction identification and a boundary estimate for the resulting transgression. Divergence of the canonical metric does not establish a nonzero torsion correction.

At an external NS cusp, a permitted simple-pole 3/2 differential has coefficient `O(e^(−πy))` in a cusp coordinate and yields an `O(y e^(−2πy))` norm density. The candidate's exponential-tail integral is correct. That fixed-surface statement does not control an internal Ramond zero mode as the moduli parameter degenerates.

## 8. Acceptance boundaries and effect on the earlier reports

Accepted without a mathematical repair to the candidate's central claims:

- The compactified odd line and nonvanishing Tate frame.
- Both comparison directions and the stated uniform growth bounds.
- Failure of positive continuous, hence positive smooth, metric extension.
- Failure of bounded-coefficient extension of the actual rank-one curvature form.
- The conditional zero-flux assertion and the explicit refusal to infer existence.
- The distinction between fixed external NS cusp integrability and internal Ramond degeneration.
- The attribution of the strong smooth-extension claim to the two precisely pinned source proofs.

Not certified:

- Any sharp leading metric asymptotic or differentiated asymptotic.
- Absolute curvature integrability, existence of the boundary-flux limit, or an evaluated open-locus canonical curvature integral.
- A failure of the source's numerical identity or of an appropriately formulated current/cohomological theorem.
- An actual torsion metric, torsion transgression, normalization map, or resolution of the original OWR statement.

The earlier frozen source report and its corrective addendum remain historical artifacts. Their source attribution of a published theorem can be retained, but their reliance on the inspected smooth-extension proof must now be qualified by this accepted local obstruction. In particular an earlier algebraic value such as an integral of `c1(F∨)` is still an algebraic characteristic number; its identification with a given open-metric integral cannot be recertified by that contradicted smooth-extension shortcut. This audit does not declare the numerical theorem false or claim an independent replacement proof.

The associated acceptance JSON pins this exact candidate and the verified source bytes. The verification script checks the input hash, elementary symbolic identities, and provenance hashes; it is not represented as a computer proof of hyperbolic uniformization or the bundle argument.
