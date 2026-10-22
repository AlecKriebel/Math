# Publication scope notice

This preserves the authored mathematical audit below. Its verification narrative describes the earlier audit run; it is not a claim that absent inputs were rerun by a public checkout. Fresh publication runs and complete output bytes appear in verification/REPRODUCTION.json. Historical VERIFICATION.json and the complete superseded report are not distributed. The corrected current_derivative/REPORT.md is the accepted partial report. The full target remains unresolved after five approaches, with no novelty claim.

# Independent mathematical audit: variational maps

## Verdict

**Corrected partial results only; the full target remains unresolved.** The five-approach budget stays exhausted. There is no proof or counterexample of the conjecture, no novelty claim, and no claim of a complete literature search. The frozen report needs an explicit interpolation-admissibility qualification and a trace clarification. CORRECTION_CONTEXT.md and CORRECTION.patch describe the changes; current_derivative/REPORT.md is the usable derivative. The original remains unchanged.

The quantitative identities in the original verifier are correct. Independent exact checks and semantic negative controls are supplied separately. Neither checker proves analytic existence, compactness, harmonic-map regularity, or the conjecture.

## Source and class normalization

The original OWR formulation assumes finitely many triangles, no boundary edges, connected vertex links, and two complete ideal hyperbolic metrics. Its target compares Y and D. The full paper defines weak closure, constructs the restricted minimizer in D̄, and proves open-face invertibility separately. Its extra edge analyticity statement concerns u. These distinctions are retained. [OWR report, pp. 2520–2522](https://ems.press/content/serial-article-files/46762); [Freidin–Gras Andreu, arXiv:1810.06714v1](https://arxiv.org/abs/1810.06714v1).

I inspected the local supplied PDFs and extracted text, including the 2018 paper's definitions of complexes and admissible maps, weak-closure convention, existence construction, properness/degree results, and boundary system. The closure bars in the relevant pages were checked visually. Definition 1 allows identifications between sides of the same triangle. The corrected report therefore does not exclude self-gluings to make its proof easier. This audit credits the primary results; it does not independently reprove their referenced compactness or elliptic regularity theorems.

The 2021 follow-up and the 2024 cone paper were inspected for their stated scope. Separate existence/regularity results and homogeneous cone models do not establish the equality at issue here. The available response for the 2024 published follow-up is HTML, not the full PDF; its mathematical contents have not been treated as inspected. [2021 preprint](https://arxiv.org/abs/2110.13043v1); [2024 cone paper](https://msp.org/pjm/2024/331-2/pjm-v331-n2-p04-p.pdf); [published follow-up](https://link.springer.com/article/10.1007/s10711-023-00871-2).

## Proof-by-proof assessment

### 1. Conditional strict convexity and uniqueness

The curvature sign and unhalved-energy factor are correct. At a point with rank-two differential A and nonzero variation vector V, the curvature expression is the sum of the squared determinants det(V,Ae_i), hence strictly positive. A compact subpatch and a short interpolation interval turn pointwise positivity into strict convexity of that patch's energy. The complement's energy remains convex. This avoids differentiating an improper integral at a cusp: one uses global integrated convexity, and differentiates only on a compact patch.

The analyticity argument is valid: proper degree one supplies surjectivity; Sard gives a rank-two point; the analytic Jacobian then has dense nonzero set on a connected open face. Equality on those points extends by continuity. Properness here is properness of the open-face restriction. For the source's regular maps, a sequence that approaches a source side cannot map into a compact interior target set when traces map to boundary sides; global cusp properness rules out escape to deleted vertices. This is the needed route from global properness to face properness.

Finite energy is essential throughout: the source supplies a finite-energy comparison map, and the lemma explicitly assumes finite-energy minimizers. No step treats equality of two infinite energies as a uniqueness statement.

The missing condition is that the facewise interpolation is admissible on the quotient. Convexity within an abstract triangle does not imply that if different boundary sides are identified. The exact p=i, q=1+i midpoint example in CORRECTION_CONTEXT.md isolates the failure. The derivative consequently makes admissibility an explicit lemma hypothesis. It does not declare the source theorem false or claim this local observation constructs global minimizing maps.

Once admissibility is available, equality of finite energies implies uniqueness as argued. Weak lower semicontinuity gives only a one-sided inequality; it does not provide an energy-recovery sequence from D approaching the unrestricted infimum. The corrected reduction retains both outstanding obligations rather than treating either as proved.

### 2. Target flows and edge balance

For a proper, facewise harmonic map that is C² up to a compact portion of an edge, a compactly supported cell-preserving target flow affects a compact subset of the source. Integration by parts therefore introduces no ideal-vertex boundary term. Summing outward conormals gives the stated pairing with target-pulled tests. The factor 2 in the first variation of the unhalved energy cancels from the zero stationarity equation.

Postcomposition preserves D when the target flow respects the required cell incidences. For D̄, closure stability uses compactly supported bounded-derivative smooth composition, the Sobolev chain rule, and local strong map convergence together with weak derivative convergence; it does not follow merely from the word “weak.” Outside the compact target support the flow is the identity. This is an analytic justification, not something the finite checker certifies.

If h is an edge C¹ diffeomorphism with positive derivative, pulling an arbitrary compactly supported domain test back by h inverse gives a C¹ target test; uniform smooth approximation with fixed compact support is enough because B is locally integrable. The conditional lemma is sound. No C² boundary regularity of v, nonvanishing h prime, or full edge invertibility is obtained by this argument. A collapsed trace has a nontrivial test kernel: on [0,1], B(s)=2s−1 has zero mass but pairs to 1/30 with s(1−s)(2s−1). Smooth compactly supported approximations preserve a positive pairing. The kernel example is a logical illustration of lost tests, not a conjecture counterexample.

Even full local balance does not automatically supply a global noncompact energy comparison with a competitor of unbounded displacement. An exhaustion or cutoff passage needs its own tail control. The frozen report already declines to take that step.

### 3. Hopf argument and flat book obstruction

In the chosen upper-half-plane chart, B stays bounded away from zero on a compact boundary neighborhood and the drift coefficient is bounded under the assumed smoothness. Nonnegativity of A, nontriviality from degree one, the strong maximum principle, and the Hopf lemma give the claimed positive inward derivative. The determinant on the edge is A_x h prime. Tangential conormal balance imposes no sign on h prime.

The flat map's components are harmonic; its tangential normal derivative vanishes on the edge; its Jacobian is negative and positive at the specified interior points. The source consists of half-disks of radius two; the target pages must be full half-planes, as now explicit. The formula need not land in radius-two target half-disks.

The minimization proof is correct for the stated fixed outer-boundary and page-preserving trace class. The cross term vanishes by harmonicity, zero normal-component competitor trace on the glued edge, zero tangential normal derivative, and zero outer trace. A density argument can be applied to the linear test space before imposing the target-page inequality; thus positivity constraints do not invalidate the identity. This proves a local flat Dirichlet fact only.

### 4. Area calibration and compatible isometries

The frame identity e−2J=(a−d)²+(b+c)² is exact for the no-one-half convention. It is independent of compatible oriented frames. For a smooth proper degree-one open-face map, the degree formula applies first to compactly supported target forms. Pulling back a bounded target exhaustion and using |J|≤e/2 justifies passage to the finite-area ideal triangle. The total is 2π times the number of faces plus the nonnegative anti-conformal defect. There is no unaccounted cusp boundary integral in this argument.

A facewise isometry in D supplies energy 2πq. Comparing with the degree-one regular minimizers proves E(u)=E(v)=2πq, including for equal metrics. The original assertion that these maps must equal that particular isometry also invoked the unqualified uniqueness lemma. The derivative keeps the energy result unconditionally within its stated hypotheses and makes map identification conditional on admissible interpolation. It does not identify energy equality with equality of maps without the additional step.

### 5. Cusp example

The derivative range is exactly [−1,3], the energy-density majorant is 10/y², and the tail estimate is 10w/Y. Properness follows uniformly along the displayed homotopy because q_r≥y, while bounded height bounds the preimage height. The sector map fixes its lower boundary and keeps both vertical sides, so its relative degree is one. At infinitely many heights its derivative is strictly negative, and elsewhere positive; it is not eventually injective.

The identity extension across y=Y is C¹, not C²: its right second derivative is 4 and its left second derivative is zero. This is sufficient for the stated Sobolev example. In metric-valued Sobolev terms the energy is finite, and the logarithmic hyperbolic distance growth is square-integrable against the cusp area density. This is not the assertion that the Euclidean coordinate q itself lies in unweighted L² on an infinite strip.

The nonharmonicity residual is −8/q at y−Y=π/4, so the example cannot be promoted to a minimizing harmonic map. Pasting multiple sectors requires genuinely compatible cusp charts and traces. The already qualified local sector statement suffices for the claimed method obstruction; no global pasting claim is needed to resolve the original problem.

## Verification protocol and limits

The original checker is rerun unchanged. The independent checker never imports it and uses a different method: exact centered differences with Richardson cancellation for cubic derivatives; finite interpolation grids with explicit degree bounds; rational Gram/determinant identities; and the differentiation matrix in the basis 1, sin(2r), cos(2r). It also checks the collapsed-trace moment and the local side-incidence midpoint obstruction. All arithmetic is exact Fraction arithmetic; there are no optimization-sensitive assertions, third-party dependencies, network requests, or checker writes.

Nine semantic mutations change an actual mathematical ingredient: the flat mixed coefficient, flat linear term, area normalization, curvature sign, cusp amplitude, cusp stationarity value, collapsed-trace kernel, lower-semicontinuity direction, or quotient-side identification. Each must fail a named semantic check. The candidate's own deliberately false Jacobian control is retained as a separate test. Each positive and negative case runs in normal Python, -O, and -OO under UID 1000. Full command lines, stdout, stderr, return codes, optimization levels, and actual read-only write-denial probes are retained in VERIFICATION.json.

The harness uses externally supplied hashes for the frozen manifest, independent checker, and derivative. It verifies every original member by byte count and SHA-256 and compares full snapshot inventories before and after. Read-only probes test create, append, mkdir, and unlink on a copy with a disposable canary, never on the frozen original. Permission-based read-only modes are a verified runtime condition, not a claim that an owner could not deliberately chmod the files. Outputs are written outside the tested tree.

PASS of these checks means the recorded finite calculations and negative controls behaved as specified. It does not mean PDE arguments were mechanically verified, source theorems reproved, literature status established, or the full conjecture solved. The corrected partial scope is the acceptance boundary.
