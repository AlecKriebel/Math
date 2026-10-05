# PR85 independent dynamics and computational audit

**Verdict within this assigned family: PASS.** No mathematical counterexample to the submitted argument was found. The stationary flow, Gramian, exact two-state ambiguity, local injectivity, curvature scaling, and fixed-atlas bounds are correct. The finite controls are consistent with the proof when interpreted as local algebra and geometry controls. They are not a certificate of the global theorem.

Target: problem 30001203 / OWR-3394-020, submitted PR85 head `7271f51995532791220ac8e6b738a578d5d59143`, claimed_solved, substantive attempt 1/5. Audit completed 2026-10-05 UTC. This is independent verification, not a new construction family. Central proof-search turns: **0**. No priority or novelty assessment was attempted.

## Scope and independence

The assigned family was dynamics/history maps, Gramian derivation, curvature and chart bounds, reproduction, and interpretation of computational evidence. I read the submitted main proof and metadata, then wrote `INDEPENDENT_DERIVATION.md` and the independent exact suite before inspecting submitted `verify.py`. I did not inspect the contents of any submitted prior review or reviewer code. The pinned review file was hashed as bytes only to assess declared pin consistency.

The hyperbolic compact surface, covering classification, Nash embedding, and compact-manifold completeness are standard theorem inputs. Their full theorem proofs are not reproved here. The smooth isometric embedding existence input is not computationally certified in this audit; this report's geometry-to-dynamics verification is conditional on that input, which is explicitly cited rather than concealed in the submission. This is an ordinary external theorem dependency, not a transfer to an unsupported equivalent observability claim.

All new artifacts and intentionally corrupted fixtures are within this audit folder. Submitted files were read only. No Git/index/tracked-file mutations, PR actions, publication changes, tracker edits, or external individual communication occurred.

## Primary statement check

Independently fetched and visually inspected the complete Krener contribution in the [EMS publisher PDF](https://ems.press/content/serial-article-files/46211), printed pp.674-675 (PDF pages 82-83, one-based). The source defines observability by injectivity of the initial-state-to-output-history map, local observability by local injectivity, and the differential Gramian by the submitted integral. It fixes some positive T and uses local coordinates on a manifold. The printed conjecture does not add a simply-connected-state-space hypothesis, constrain output dimension, or exclude a zero field. Its output-scaling/noise-covariance comment does not impose such a restriction. The exact source's uniform coefficient language does not specify a reference atlas; the submission supplies both an arbitrary-fixed-background-metric proof and a bounded hyperbolic atlas.

Source pin: SHA-256 `ef407f7cb1bcf1793d9fb02001b1aa68515342649009e8bdd1c9aecfbf1b7fe9`, 747670 bytes, retrieved 2026-10-05T03:39:23.025034+00:00. It matches the submitted source manifest. The two rendered pages and extraction are preserved under `sources/`.

## Verified mathematical chain

Write the exact flow as phi_t. Because f=0, phi_t=id_M for all real t and d(phi_t)_x=id_(T_xM). In a fixed state chart, F=0 and the initial-value problem Phi'=F Phi, Phi(0)=I has Phi=I. The word "fixed" matters: an externally time-varying frame can display a different matrix even when the intrinsic tangent flow is identity. No such frame occurs in the submitted computation.

Let Y_T(x)(t)=h(phi_t(x)). Here Y_T(x) is the constant function h(x). Its tangent sends v to the constant function dh_x(v). Hence, with the standard Euclidean output inner product and unnormalized L2 time integral,

\[
 P_T(x)(v,w)=\int_0^T\langle dh_x(v),dh_x(w)\rangle\,dt
 =T\langle de_{\pi(x)}d\pi_x(v),de_{\pi(x)}d\pi_x(w)\rangle
 =T(\pi^*g)_x(v,w).
\]

There is no unnoticed 1/T normalization, transition-matrix inverse, or omitted time dependence. The exact h-induced metric equals the metric whose curvature is used. The proof does not select an unrelated metric and then call it the observability Gramian.

For T>0, the squared L2 distance between two histories is

\[
 \|Y_T(x)-Y_T(x')\|_{L^2}^2=T\|h(x)-h(x')\|^2.
\]

Equality of histories is therefore equivalent to h(x)=h(x'). Since e is injective, this is equivalent to pi(x)=pi(x'). The covering degree gives exactly two preimages for every **attainable** history. A history outside Y_T(M) has no preimage. The ordinary reading of "every output history" as a system-generated history is correct, but adding "attainable" would remove any semantic ambiguity. Above an evenly covered base neighborhood, restriction to one sheet makes pi a diffeomorphism. Composing with e proves h and Y_T locally injective. Differential rank two follows separately from invertibility of d pi and injectivity of de.

Because pi^*g is the covering metric, pi is a local isometry and K=-1. Under a constant scaling T, the connection and mixed (1,3) curvature tensor are unchanged, while scalar/sectional curvature scales by 1/T. Thus K(P_T)=-1/T. In dimension two Gaussian and sectional curvatures agree. Compactness ensures geodesic completeness; equivalently, multiplying the metric by a constant positive T leaves the affinely parameterized geodesic equation unchanged. No finite calculation of geodesic trajectories is needed.

For any fixed smooth positive definite background q, the generalized Rayleigh quotient of pi^*g on the compact q-unit tangent bundle has a positive minimum and finite maximum. This proves c q <= P_1 <= C q. It is stronger than selecting q=P_1 and is not a sampled claim.

In sufficiently small centered hyperbolic disk charts, set rho=u^2+v^2. The exact coefficient is lambda_T=4T/(1-rho)^2. On 0<=rho<=1/4,

\[
 \lambda_T-4T=\frac{4T\rho(2-\rho)}{(1-\rho)^2}\ge0,
\]
\[
 \frac{64T}{9}-\lambda_T
 =\frac{4T(1-4\rho)(7-4\rho)}{9(1-\rho)^2}\ge0.
\]

These factorizations establish all-point bounds 4T I<=P_T<=64T/9 I, with the displayed T=1 claim exact. Each chart can have a smaller radius than 1/2; one does not need an embedded full radius-1/2 disk at every point. Restricted open charts retain neighborhoods of their centers and compactness supplies a finite subcover. Arbitrary rescalings or nonorthogonal coordinate changes need not preserve the constants. The submission expressly avoids that impossible demand.

Boundary checks: T=0 makes the Gramian zero, so the positive-definiteness assumption fails. There is no common positive lower bound as T tends to zero, no common metric upper bound as T tends to infinity, and no fixed negative curvature margin as T tends to infinity. The submission only asserts the construction for any **fixed** T>0, as does the source. All-time indistinguishability remains true because each trajectory is stationary.

## Reproduction and genuinely distinct controls

The submitted checker ran unchanged with Python 3.14.6 and pinned SymPy 1.14.0. It reproduced **873 assertions**, PASS, K=-1/T, 197 rational chart points, and 15 nontrivial double-cover characters. The reproduced receipt is **byte-for-byte identical** to submitted `verification.json`, SHA-256 `7fb52cc48729d88ddc24fc29993a24342d71c2b12c8be5b2d88daec0886e1e6a`. The artifact/checker hashes match their declared pins. All six `frozen_artifacts.json` entries match their actual files; the review file was hashed without interpreting its contents.

The independent suite passed **138 exact assertions**. It uses full Riemann/Ricci computations in both disk and upper-half-plane coordinates, checks metric compatibility, checks connection and mixed-curvature scaling, computes curvature in a nonorthogonal chart, checks nonlinear chart pullbacks and a nonlinear chain rule, proves the continuum bounds by symbolic slack factorizations, and checks history-distance/T-boundary identities. It does not merely replace the submitted rational mesh with another mesh. The upper-half-plane and nonorthogonal-chart computations separately confirm curvature -1/T. Its authoring preceded inspection of the submitted checker.

One independent suite run encountered a SymPy limitation solving a rational inequality with a positive symbolic factor T. Dividing by that known-positive factor allowed the same all-positive-T result to be checked. No mathematical claim was weakened. This event and the repair are logged.

The 873 count is a counter of assertions, not 873 independent facts or independent constructions. In particular, 788 assertions are 197 coefficient samples and three positive-T repeats of those same coefficient inequalities; the analytic proof supplies the unsampled domain. The surface-word checks exhaust a finite character space and verify relation closure/transitivity of those monodromy actions, but do not construct a smooth global cover. The chosen-character check and Euler/genus/dimension checks are arithmetic sanity controls. The four selected Jacobians and a generic 3-by-2 H check local algebra; they neither instantiate the 17-dimensional Nash embedding nor numerically evaluate its actual differential.

## Adversarial interpretation probes

Three expected evidence limits were independently demonstrated in local copies, preserved under `controls/intentional_mutation_fixtures/` and summarized in `controls/evidence_limits_receipt.json`:

1. The checker consumes COUNTEREXAMPLE.md only to hash it. Replacing the adjacent proof text with explicit contradictions still gives PASS and 873 controls, with a different hash. Therefore PASS is not a semantic verifier of the proof. Frozen pins and independent proof review supply different parts of the evidence.
2. The submitted ck function uses Python `assert`. In an intentional negative-metric mutation, ordinary Python fails at `symbolic_curvature`; optimized Python `-O` instead reports PASS, 873 controls, and curvature `1/T`. Thus reproduction must use ordinary unoptimized Python. The documented `python verify.py` command does so. This is an informational harness limitation, not a failure of the reproduced default run.
3. A smooth positive conformal coefficient can equal the submitted coefficient at all 197 mesh points and have value 8>64/9 at the unsampled point (1/32,1/32). The construction multiplies the coefficient by 1+C b, where b is the product of squared distances to the grid points and C>0 is chosen exactly. This proves that finite grid checks alone cannot establish a continuum bound. It does not retain the submitted constant-curvature hypothesis and does not challenge the correct submitted analytical bound.

The submission explicitly labels the finite checker modest, states it does not construct a Nash embedding, and attributes covering existence and completeness to mathematical arguments/theorems. No unsupported leap from controls to the global theorem was found in that stated interpretation.

## Remaining gap and promotion boundary

Within this dynamics/computation family, no unresolved mathematical gap remains, subject to the explicitly imported standard existence inputs. Independent authentication of Nash's smooth dimension-17 embedding statement and the global surface/cover construction belongs to the parallel theorem/source audit rather than this control suite. Do not promote this report alone as a machine verification of those inputs or as an assessment of historical novelty. The conjecture's literal manifold formulation is addressed; questions with new hypotheses absent from the source are outside this verdict.

The submitted status, proof, receipt, and explicit limitations are consistent for this family. Claims of a past independent review's 108 controls and workflow/priority searches were not independently certified here because the prior review and research-ledger history were deliberately excluded from the independent proof verification.

Best-guess completion of the assigned independent dynamics and reproduction audit: **100%**. This is a completion estimate for verification, not for historical priority or a claim of novelty.

## Reproduction commands and artifacts

Run from this audit directory:

```sh
.venv/bin/python controls/independent_exact.py
.venv/bin/python controls/adversarial_evidence_limits.py
.venv/bin/python ../source_intake_20261005/submitted/verify.py
```

Pinned runtime packages: SymPy 1.14.0, mpmath 1.3.0. Preserve the submitted files unchanged. `controls/receipt_comparison.json` records exact submitted-receipt equality; `submission_pins.json` records declared pin matches; `sources/owr_source_pin.json` records the primary source pin; `RESEARCH_LOG.md` records timestamps and completion estimates.
