# Independent ball-spectrum and compact-counterexample adversary

Frozen submission: `36d5ef15098163e74bf14c2e696f560ce592affd`; record 30005244 / OWR-11101924-008; author turn 2/5. Audit family: ball Hodge/spherical spectrum, quantitative real-frequency perturbation, fat compact point-sampling counterexample.

## Finding

**The submitted TURN_2.md counterexample is mathematically valid as stated. No proof defect was found in this assigned route.** It establishes, for the explicit positive real frequency κ=1/10000, existence of a compact, positive-volume, empty-interior support Ω and an isolated nonreal eigenvalue of SκΩ=AκΩ−I/3, while the omitted-diagonal DDA matrix on every grid (1/n)Z³ is exactly the nonempty 3×3 zero matrix. The support is chosen existentially as one sufficiently advanced member of the displayed compact sequence; neither an effective member index nor an eigenvalue location is provided or needed by the statement.

**The source interpretation remains qualified.** OWR printed 2580 permits the literal phrase “compact subset” without a boundary hypothesis, so the example meets that literal support description and refutes a universal assertion over all compact point-sampled supports. OWR §4, however, describes numerical observations and asks for an accurate theorem; it does not itself formulate that universal assertion. The example is outside the usual regular-particle interpretation and outside CDN's repeated bounded-domain description. It should not be promoted to a claim that the physical observed DDA behavior is false, or that this counterexample alone completely settles every interpretation of the open question. This audit makes no status, paper, deposit, priority, or novelty decision.

The exact and independent derivation is in `INDEPENDENT_DERIVATION.md`. It was saved at 2026-10-15T07:58:17Z before the inherited continuation review was opened. The later comparison did not alter the derivation's mechanism or conclusion.

## Checks of the ball spectrum

The orthogonal decomposition ∇H₀¹(B) ⊕ ∇H_harm¹(B) ⊕ (∇H¹(B))⊥ is complete. Gradient-space closedness follows from Poincaré, and Dirichlet projection gives the harmonic splitting. The final summand has zero distributional divergence after zero extension. Whole-space longitudinal projection then makes A₀ act as 1 on the first summand and 0 on the last.

For a degree-l solid harmonic, the distributional divergence of its zero-extended gradient is the negative boundary normal derivative. The Newton single-layer derivative jump is also negative; keeping both signs gives the positive multiplier l/(2l+1). Orthogonal spherical harmonics converge in the harmonic Dirichlet norm; the energy weights are l for each normalized boundary harmonic. Thus there are no omitted vector modes or additional harmonic spectrum:

σ(A₀)={0,1,1/2}∪{l/(2l+1):l≥1}.

The harmonic degree-l eigenspace has dimension 2l+1. The accumulation point 1/2 is not a separate eigenvalue in this decomposition. For S₀ the zero eigenspace is exactly the three constant vector fields, while l≥2 has eigenvalue (l−1)/(3(2l+1))≥1/15. The remaining spectral values are −1/3, 2/3 and the accumulation 1/6. Consequently the claimed isolated rank three and gap 1/15 are exact. This calculation is intrinsic to L²(B); using the global zero extension here would indeed destroy the finite-rank zero and invalidate the argument. The submission does not make that mistake.

## Checks of every quantitative constant

| Quantity in TURN_2 | Independent result |
|---|---|
| Quadratic kernel | −(I+eeᵀ)/(8πr), with sign verified directly |
| Cubic kernel | −iI/(6π), with no eeᵀ cubic contribution |
| Frobenius numerator squared for C₂ | 6 |
| Double r⁻² integral bound | 32π²/3 |
| C₂ operator bound | ≤HS norm≤1 |
| J/(6π) operator norm | 2/9 |
| Scalar numerator tail | Σ(n≥4)n²/n!=2e−9/2<1 |
| Remainder Frobenius kernel | ≤3|κ|⁴r/(4π), for |κ|≤1/2 and r≤2 |
| Remainder operator bound | ≤HS norm≤2|κ|⁴ |
| Full dynamic correction | ≤(29/18)|κ|²≤2|κ|² on the stated disk |
| Static contour/resolvent | radius 1/30; norm ≤30 |
| Perturbed contour resolvent | norm ≤60 if ε≤1/60 |
| Riesz projection difference | ≤60ε≤120|κ|² |
| Graph norm | ≤η/(1−η)≤240|κ|² when η≤1/2 |
| Graph operator error | ≤(2+2·240)|κ|⁴=482|κ|⁴ |
| Trace error | ≤3·482|κ|⁴=1446|κ|⁴ |

The scalar tail can be bounded entirely rationally: e≤87/32 follows from a geometric factorial tail, giving 2e−9/2≤15/16<1. On every bounded frequency disk the correction's power series converges in Hilbert–Schmidt norm; the correction is an entire operator family on the fixed ball. The explicit estimates use only |κ|≤1/2 because the difference set has radius 2. No boundedness of a nonzero-frequency infinite-space lattice or of the unrestricted outgoing volume kernel is assumed.

The Riesz projection may be nonorthogonal. Distance less than one to P still proves rank three by two injective restrictions. Projection onto V gives an invertible coordinate map on its range, and the graph formula Hκ=P Sκ(I+Γκ)|V is a similarity representation. Its trace therefore counts algebraic multiplicities, including possible Jordan clusters. Since P S₀=0, the only graph error is P Cκ Γκ.

For real κ the quadratic compression is selfadjoint and has real trace. An optional independent Newton-potential check gives PC₂|V=−4I/15. The constant cubic compression is −(2i/9)κ³I. At the explicit κ,

Im tr Hκ ≤ [−2/3+1446/10000]κ³ = −(7831/15000)κ³ < 0.

All smallness conditions hold exactly. For example 120κ²=3/2500000≤1/2 and 2κ²=1/50000000≤1/60. Strict trace negativity is guaranteed for 0<κ<1/2169, well above 1/10000. Hence at least one of the three algebraically counted eigenvalues has negative imaginary part. Its isolation and finite algebraic multiplicity follow either from the rank-three contour cluster or from analytic Fredholm theory for the compact perturbation of the selfadjoint static ball operator. No numerical eigenvalue evidence is used.

## Checks of the compact example

For radii 2^(−j−k−4), the total removed volume divided by |B| is at most 2^(−3j−12)/7; at j=1 this is 1/229376<1. The sets F_j=closed B\U_j are compact and increasing, with positive volume and |B\F_j|→0. Each rational q_k is removed by its own positive-radius ball. Rational density proves empty interior. The added origin is isolated, because the hole centered at the enumerated origin has positive radius, and it leaves the Lebesgue L² continuum operator unchanged.

Since (1/n)Z³⊂Q³, Ω_j∩(1/n)Z³={0} exactly, for every j,n≥1. The only 3×3 self block is omitted, so every matrix is exactly zero. This is an exact statement, not a small-matrix approximation. The voxelized volume is n⁻³, and |Ω_j△Ω_{j,1/n}|→|Ω_j|>0. In particular the example fails (G), as required for compatibility with the positive theorem.

Small volume removal does not imply static operator norm convergence and the proof does not assume it. Strong masks give strong selfadjoint static compressions with common bound [−1/3,2/3]. Nestedness and vanishing removed measure give almost-everywhere mask convergence. Dominated convergence of the squared weakly singular dynamic kernel gives Hilbert–Schmidt convergence. The ball eigenvalue is enclosed by a disk wholly off the real interval; on this contour the zero complement introduced by whole-space embedding is harmless.

For the continuum mask sequence, the factorizations (z−B_j−C_j)=(z−B_j)(I−R_jC_j) are valid. Compact left multiplication follows from strong resolvent convergence, and compact right multiplication follows from the separate strong convergence of adjoints. Integrating the analytic static resolvent contributes zero, while the compact resolvent corrections converge in norm. The finite-rank Riesz projections therefore converge in norm and eventually have equal positive rank. This proves persistence of a nonreal eigenvalue on one fixed finite-index F_j. The support's zero matrices can never approximate that eigenvalue, which is outside the real I_lat regardless of its unknown decimal endpoints.

## Source scope, counterchecks and limits

The rendered primary OWR pages confirm the Sκ=Aκ−I/3 normalization, center-membership rule and diagonal omission. CDN equations (1.6)–(1.8), (3.38)–(3.42), Lemma 3.14 and Proposition 3.15 independently confirm the distributional shift and inclusion [−1/3,2/3]⊂I_lat. The exact decimal interval endpoints are not inputs. The complete original contribution was read, including the preceding real-positive-frequency warning that the infinite dynamic lattice is unbounded.

Potential falsifiers tested: reversed single-layer sign; missing non-gradient vector modes; loss of finite rank from global zero extension; invalid orthogonal-projection assumptions on Pκ; uncaught Jordan multiplicities; imaginary quadratic trace; quartic remainder too large at explicit κ; use of an infinite-frequency lattice bound; failure of positive volume or compactness; a surviving rational lattice point; loss of eigenvalues under only strong convergence; and invalid compact right multiplication. None survives the written derivation.

The strongest verified statement is precisely the submitted unrestricted-compact counterexample together with compatibility with the qualified positive theorem. This review does not prove (G) necessary, give a full necessary-and-sufficient geometric characterization, analyze eigenvalue density on I_lat, certify source-intended irregular geometry, prove an effective j, establish novelty or priority, or validate unrelated parts of the positive proof beyond the abstract argument used here.

## Reproduction and inherited-review comparison

`exact_controls.py` was independently authored in this folder; no submitted script was imported or executed. It passed 1,244 exact integer/rational assertions, including coefficient checks, bound arithmetic, gap identities, the explicit trace margin and geometric volume-series controls. These finite assertions are supporting receipts; harmonic completeness and infinite-dimensional convergence remain analytic proof arguments. Ordinary floating eigenvalue diagnostics: none.

After saving the independent derivation, I read the inherited `scope_continuation/independent_review/INDEPENDENT_REVIEW.md` and later the short author `scope_verification.json` output. Their ball, graph and compact-mask mechanisms agree with the independent reconstruction, and their exact trace bound agrees. I do not inherit the earlier review's broader disposition wording. No sibling family's report was consulted before or during this independent derivation.

All primary copies, rendered pages and raw control outputs are in ignored `private/`. `SOURCE_PINS.json`, `SOURCE_READMAP.md` and `CONTROLS_RECEIPT.json` identify the checked materials. Only the files in `SAFE_AUTHORED_MANIFEST.json` are safe authored audit outputs. No provider state, Git index/ref, shared database, paper, deposit or tracker was changed, and no outreach was initiated.
