# Independent review: the variable-profile acoustic PML multiplier family

**Verdict: PASS_SCOPED_FUNCTIONAL_OBSTRUCTION.** The submitted argument correctly excludes every bounded time-independent choice in the displayed δ,F family for one smooth bounded nonnegative damping profile and the stated class of layer-supported initial pressure data. No mandatory mathematical correction is requested. The broader Lyapunov/stability target remains **unsolved, 2/5**.

This independent adversarial AI review was completed on 2026-09-30 (gpt-6-astra, xhigh). It is not human peer review or a novelty certification.

## 1. Snapshot and exact scope

Reviewed `OBSTRUCTION.md` SHA-256:

`b270af773ded6be5f0c6a1d6c8bfa942ac1fb726b163cb0e7eaa621fa427f8fe`.

Submitted `verify_obstruction.py` SHA-256:

`e55e64815893ca099f906dcdf2b287afcf01a2d696bfc901457ebafff0ded06c`.

All **9,539 submitted assertions** reproduced with byte-identical JSON output in an isolated copy. A separate symbolic verifier passed **21 assertions**, covering identities with arbitrary symbolic jets rather than another finite sample of the author's numerical substitutions. The author directory was not edited.

The claimed conclusion concerns failure of monotonicity of one specified functional family. It does not assert instability, unbounded solutions, or nonexistence of a different local, nonlocal, derivative-dependent, or augmented Lyapunov functional. It also does not address whether the same state can be reached from initial pressure data confined to the physical region.

## 2. Primary-source verification

I read the complete relevant contribution, printed pp.196–200, in [OWR 03/2013](https://ems.press/journals/owr/articles/12331), including visual inspection of pp.197–198. The equations, signs of B and C, displayed functional, range `0≤δ≤c²α`, nonnegative diagonal F, and algebraic inequalities agree with the submitted transcription. The final paragraph on p.198 already identifies an uncontrolled spatial-variation term and leaves the issue open; the package appropriately credits that prior observation.

The full system and the reduced system with C deleted are different in general. The submitted example has only one nonzero damping coefficient. Every pairwise product then vanishes, so C=0 exactly, as do β and γ. Thus the same local test applies to both systems without making an invalid three-dimensional reduction.

I checked Section 3 and the stated Theorem 1 in the complete publisher-deposited XML of [Kaltenbacher–Kaltenbacher–Sim, JCP 235 (2013)](https://doi.org/10.1016/j.jcp.2012.10.016), available as [PMCID PMC3719215](https://europepmc.org/articles/PMC3719215). The weak formulation imposes Dirichlet conditions on p and v, with no analogous boundary restriction on the vector auxiliary variable. The theorem's initial-data assumption is zero auxiliary vector; it does not require all initial pressure data to be supported in the physical region. The model derivation's zero-initial-data motivation is a narrower setup and must remain separate. The candidate does keep these scopes separate.

I also checked the model, Theorem 2.2, its proof, and Remarks 2.1–2.4 in the full author manuscript of [Baffet–Grote–Imperiale–Kachanovska (2019)](https://doi.org/10.1007/s10915-019-01089-9), [HAL version 2](https://hal.science/hal-01865484v2). The monotone-energy theorem assumes constant damping. The variable-coefficient and interface remainders are already explicit in that work. Its physical initial-data convention is zero data inside the layer. The candidate neither contradicts the constant-coefficient theorem nor supplies a counterexample within that narrower physical initial-data class.

## 3. Initial derivative and the quantified parameter obstruction

At zero auxiliaries, direct differentiation of the source functional gives

`η′(0)=∫[(δ−s)h²−s f_x²+s f_y²+s f_z²+δ f Δf]`.

The cancellation of the terms `sδfh` is exact; the remaining `hΔf+∇f·∇h` is a boundary divergence. Compact support removes it. All F-dependent derivatives contain the initial vector auxiliary u and therefore vanish. This remains valid for bounded measurable δ and F: differentiation is in time, and no spatial derivative of either parameter is needed.

Suppose `δ≤s` and the inequality is strict on a set of positive measure in the face patch. A compactly supported real smooth cutoff χ can have `∫(s−δ)χ²>0`: nonnegativity and an exhaustion by interior compact sets provide such a test. With `h=0` and `f_N=χ cos(Ny)`, the leading term divided by N² is the stated difference of weighted sine and cosine squares. All other terms are O(N) on the fixed compact support, even for merely bounded δ. The oscillatory integrals tend to zero by the Riemann–Lebesgue lemma applied to integrable coefficients. The limit is therefore half the positive integral. This proves that monotonicity for every allowed test solution forces `δ=s` almost everywhere. The argument allows arbitrary spatial dependence of δ, not merely dependence on x.

The quantifiers are important and are handled correctly: one damping profile is fixed; for any allowed δ,F, either the high-frequency test violates monotonicity or δ=s almost everywhere and the following fixed positive-form test does. The same δ,F must serve all initial states. Dropping the prior upper bound on δ does not help: setting f=0 would first force `δ≤s` through arbitrary h.

## 4. Positive derivative with smooth compact support

For the forced choice δ=s, the transverse gradients cancel, leaving

`η′(0)=−2∫s f_x²−∫s′f f_x`.

Where s=x², integration by parts converts the last term to `∫f²`. The displayed witness aε has zero endpoint traces and belongs to H₀¹(ε,1) for each fixed positive ε; no singular endpoint x=0 is included. I independently verified the exact rational-plus-logarithmic integral in equation (8). At ε=2⁻¹⁶, the elementary lower bound `log 2>2/3` gives the claimed strictly positive margin, indeed greater than 11/6.

The weighted quadratic form is continuous in H¹ on the fixed interval. Density of compactly supported smooth functions in H₀¹ therefore preserves strict positivity for some genuine smooth compactly supported a. Multiplying by any nonzero smooth compact transverse b, normalized in L², produces the desired three-dimensional test. No singular state, limiting solution, or numerically inferred sign is used.

An independent change of variables confirms the mechanism: put x=eᵗ and a(x)=x⁻¹ᐟ²v(t). For a zero-trace v, the quadratic form becomes `∫(v²/2−2(v′)²)dt`, since the mixed term is a boundary derivative. A Dirichlet sine has positive form when the logarithmic interval length exceeds 2π. Here that length is `16 log 2>32/3>44/7>2π`. This control is consistent with the submitted explicit witness; it is not needed to replace its proof.

The proposed damping is admissible. A smooth nondecreasing cutoff, flat on x≤0 and equal to one by ε/2, times x² gives a smooth nonnegative nondecreasing profile that equals x² throughout the witness interval and vanishes in the adjoining physical region. It can be continued to a bounded smooth profile with bounded derivatives beyond the computational box. Distant transverse layers can be added outside the finite-propagation neighborhood without changing this local test.

## 5. Local solutions and prior augmentation

The transformation `(q,r,w)=(p_t+sp,∇p+u,u₁)` gives precisely equation (10). Its constant principal matrices couple q to the corresponding component of r symmetrically; their characteristic speeds are 0 and ±1. The p,w equations have no spatial principal part. Smooth bounded lower-order coefficients yield the usual Sobolev solutions by the free-wave propagator and a bounded-perturbation construction, with regularity propagated at every finite order for smooth data. Finite propagation follows from the symmetric principal block and local multiplication terms.

The inverse reconstruction is also correct. With u=r−∇p, the discrepancy `w−u₁` obeys the scalar ODE `(w−u₁)_t=−s(w−u₁)` and is initially zero. The transverse auxiliary equations and the pressure equation then follow, and v is the time integral of p. Choosing time below the positive distance from the initial support to the face edge and outer boundary gives an actual smooth solution of the full extended system, with p=v=0 near the boundary. No contested energy inequality is used to establish its existence.

For δ=s and F=diag(2,1,1), the source functional equals `½∫(q²+|r|²+w²)` identically. Its balance has the negative term `−2∫s r₁²` and the uncontrolled term `−∫s′p r₁`, with the signs and factor two correct. The pointwise matrix inequalities are saturated. Their validity cannot remove the gradient term.

The 2019 integrated-auxiliary energy reduces to this same face energy under the stated zero-auxiliary initialization: its relation gives `s(v_x+Φ₁)=−u₁`, so the additional squared term is exactly w². Its variable-coefficient remainder therefore reduces to the same profile-gradient term. This establishes the attribution without importing an inapplicable monotonicity theorem.

## 6. Reproduction and disposition

From this review directory:

```sh
python independent_checks.py
python author_replay/verify_obstruction.py > author_replay/replayed_verification.json
cmp author_replay/verification.json author_replay/replayed_verification.json
```

The independent script requires SymPy; the submitted script uses only the standard library. Exact algebraic tests do not by themselves certify the high-frequency limit, density step, or local PDE existence; those have been audited separately above.

Retain **unsolved, 2/5**, the explicit layer-supported-data qualification, the credited earlier remainder and constant-damping theorem, and the absence of an instability or general-Lyapunov nonexistence claim. No mandatory correction is needed for the frozen artifact.
