# Independent analytic review — Zenodo 22089748

**Disposition: DEFER the present published package for a demonstrated proof defect.** The defect is a false scalar identity in the supplied symmetric-sector phase proof, used to obtain the debt bound in main Appendix A, equation (A.31). This is **not a counterexample to (A.31), Theorem 9, or Theorem 1**. A different all-population-size proof of symmetric-sector curvature is already present in the published source package and supports that conclusion independently. No repair or replacement proof has been created.

Review completed 2026-10-25 UTC. Inventory row 46. Title: *Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating*. Version 1.0.0, DOI https://doi.org/10.5281/zenodo.22089748.

## Source binding and coverage

The fresh public PDF has 30 pages, 235224 bytes, SHA-256 `ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180`. All 30 pages were read, including Appendices A–C and references. Page 25 was also rendered and visually checked to authenticate (A.31), not merely inferred from extracted text.

The five public assets were checked against the acquisition receipt. The source tar has SHA-256 `7220a09d7eb31fdd81c42b35cbeb680f8c1b257df3b3002d37146b00d81e588e`; the referee tar has SHA-256 `d8fc0193da78cd4907ca7a36950111c00c761966538d71a937320b1db23909fb`. Exact public-file pins are in `source_pins.json`; exact hashes of the load-bearing TeX, notes, and verifiers are in `load_bearing_source_hashes.json`. The reader PDFs in the supplied archives are identical copies of the main PDF, not additional independent manuscripts.

Fully read the phase-contraction note and its verifier, and the existing alternative regular-sector proof and its verifier. Read the main manuscript and relevant actual TeX, including the sector decomposition, normalization, and full all-n appendix. The full published referee launcher was inspected for execution behavior and run on an unchanged private copy. After the confirmed defect, further broad source-by-source verification was stopped under the assigned defect policy: **this report does not claim every auxiliary historical/background mathematical note and every one of the 27 Python files has received a separate line-by-line analytic review**. All supplied certified checks nevertheless ran successfully, as recorded below.

## Independence and sequencing

Before examining the supplied mathematical helpers, I constructed exact controls directly from the death–Birth forward transition probabilities. I also constructed the geometric-burst union dual and rectangular marked/active chains independently, then reconstructed the Appendix A finite rank matrices and scalar bounds. These routes do not import supplied helper code. Only after the 30-page read and these independent constructions did the parent communicate another reviewer's suspected Eq. (35) index defect. I authenticated that finding from the original formulas and fresh exact arithmetic; I did not open the sibling's report or code. The targeted verification is consequently independent reproduction of a communicated finding, not an independent discovery of its location.

Necessary published support contains assertions such as “PROVED” and “closes” plus descriptions of prior checks. These were treated as claims to test, not reviewer verdicts. No dedicated historical or sibling review report was consulted.

## Exact mathematical scope

The state is a mutant subset of a finite loopless population of size n. A uniformly chosen target dies; a parent is chosen among its incoming neighbors with probability proportional to its positive fitness times edge weight. After incoming-column normalization, the replacement kernel P has zero diagonal and row sum one. The parent-mutant probability is

`f_r(x) = r*x/(1+(r-1)*x)`, where `x=sum_{u in S}P[v,u]`.

Fixation is averaged over a uniformly random initial singleton. The local theorem is at r=2, at the complete kernel J with off-diagonal entries 1/(n−1). Its tangent consists of all real zero-diagonal row-zero matrices, including directed and nonreversible perturbations. A fixed direction permits a two-sided positive-kernel neighborhood; no n-uniform neighborhood is claimed.

Theorems 1 and 9 concern strict nondegenerate **local** maximality at r=2 for n≥3. They do not establish global maximality at r=2. At n=3 the symmetric-balanced sector is absent. At n=2 the only normalized loopless kernel is J and the fixation probability is 1/2 for every fitness, so the n≥3 restriction is material.

Theorem 2 concerns a **fixed**, complete-positive directed weighting as r tends to infinity. It identifies a 1/r deficit given by discrepancies within incoming columns. Corollary 3 additionally uses the earlier strongly connected noncomplete-support obstruction and a source-component argument. It excludes a single fixed finite strict amplifier for all r>1. It does not rule out an n-dependent family that amplifies every fixed beneficial fitness. Proposition 13 only gives a necessary growing-degree condition for such families. The global small-size statements concern positive weighted triangles and the two expressly specified weighted K4 families, not all K4 weightings.

## Demonstrated defect and exact location

Use the source root `sources/published-source/complete_graph_extremality_db_source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/`.

1. `r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md`, lines 53–61, defines

   `omega_k = g^a_k = binom(N-2,k-1)/(2^(N-1)*(N+1))`,

   `q_k = binom(N-3,k-2)/(2^(N-2)*(N+1))`, `2<=k<N`.

2. Lines 283–286 define `Y_k=2(k+1)/(3k(k-1))`.

3. Lines 316–321, Eq. (35), claim

   `D <= Yq = sum_{j=1}^{N-2} [4(j+2)/(3(j+1)(N-2))] omega_j`.

4. Lines 423–431 explicitly use Eq. (35) to obtain `D <= beta_N * ell*f0` and conclude positivity for every N≥40. In the main PDF, the resulting debt bound is (A.31), **page 25**; (A.36), **page 26**, uses it to finish the symmetric-sector argument. The corresponding TeX is `paper_db_extremality/appendices/A_sector_certificates.tex`, lines 513–516 and 591–600. Theorem 9 is on page 11; the subsequent proof of Theorem 1 uses its sector positivity.

The binomial definitions give exactly

`q_k = 2(k-1)/(N-2) * omega_k`.

Thus direct multiplication and reindexing give

`Yq = sum_{j=1}^{N-2} [4(j+2)/(3(j+1)(N-2))] omega_(j+1)`.

This is an audit identity, not a proposed corrected theorem. The printed term uses `omega_j`, which the note explicitly identifies with `g^a_j`; the discrepancy is not a convention for indexing vectors.

At N=40, within the claimed analytic phase range,

`Yq = 11269994184625/25053197072596992`,

`printed sum = 5484149460473/12221071742730240`,

and therefore

`Yq - printed sum = 549755813107/501063941451939840 > 0`.

The smaller checks N=4,5,24 and a tail check N=288 likewise give positive differences. N=3 happens to give equality. Exact values and reproduction code are `targeted_phase_and_alternative_results.json` and `targeted_phase_and_alternative_controls.py`.

**Logical consequence.** The majorization `D<=Yq` alone cannot yield a strictly smaller claimed upper bound. The printed proof of the first inequality in (A.31), and hence this phase proof's deduction of (A.36) for N≥40, has a missing valid comparison. The scalar (A.31) could still be true because the actual debt can be smaller than Yq. No actual-debt counterexample is asserted or sought. The direct finite symmetric solves for N=3,…,39 are unaffected.

## Why the replay does not detect the defect

The published verifier `verify_true_inverse_rank_symmetric_phase.py` has SHA-256 `7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512`, exactly the hash printed in the main paper. Its line 225 correctly checks `q_k=2(k-1)omega_k/(N-2)`. It checks Y as a majorant, independently evaluates the **printed** beta_N and epsilon_N, confirms their finite margins, and verifies the displayed discriminant polynomials. It does not check the equality in Eq. (35), or establish the missing comparison from actual debt to the printed beta bound. Hence a successful run is compatible with this false equality.

My fresh phase code likewise verifies those displayed finite margins and polynomial signs, not their missing logical connection to the true debt. Its 6622 passing checks must be read with that limitation. They do not rescue (A.31).

The full published `run_all_referee_checks.sh` replay returned 0, rejected its prescribed hostile controls, validated 73 source members and 83 payload files, ran the mathematical verifiers, and reproduced the main PDF byte for byte. Start and finish were 2026-10-25T01:36:09Z and 01:38:24Z. See `published_replay_receipt.json`, `published_replay.stdout.txt`, and `published_replay.stderr.txt`. This demonstrates reproducibility of the provided checking process; it is not a complete mathematical correctness certificate.

## Existing alternative proof: substantive scope qualification

The published source already contains `r2_regular_sector/LOCAL_COMPLETE_HESSIAN_THEOREM.md` (SHA-256 `bb6ab1d47785132c2f66ccf57f84b0b88f44274319e70e5b1644090bb0c772e7`) and `verify_local_complete_hessian.py` (SHA-256 `442ace50585f4eea46f5e045dfc131e076b3d1f7a032ef5a524367cc94f14967`). This is mathematical supporting material, not a newly constructed remedy.

Its domain is exactly the symmetric row-zero tangent at J, which is the affected symmetric-balanced sector. It works in the **forward** subset chain. The first committor derivative is `-v_k q(S)` for a cut statistic, with v solving a strictly diagonally dominant tridiagonal M-matrix system. Literal subset averages of q² and target sums yield the exact second variation

`Phi''/E = -sum_k D_k + sum_k ell_k v_k`,

where `E=sum_{i<j}delta_ij^2`, `D_k>0`, and `ell_k>0`. A supplied rational supersolution bounds v. A positive-coefficient polynomial proves the supersolution inequality for every admissible rank. The n=4,5 cases are solved exactly; n=6,7,8 use exact total ratios below one; n≥9 uses the displayed H(q) polynomial to establish the termwise comparison `ell_k*bar(v)_k < D_(k-1)`.

I reconstructed the generator differentiation, cut increments, occupation current equations, M-matrix implication, and curvature formula. The n=4,5 curvature values agree with my earlier exact full subset-chain controls. Fresh enumeration of all subsets on distinct symmetric-balanced directions for n=4,…,9 verifies the three cut-square averaging identities. Independently simplifying the stated formulas gives

`D_(k-1)-ell_k*bar(v)_k = rho^2 * 2^(-k) * H(q) * F(n,k)`,

`F(n,k)=4(n-1)/[5n(n-3)(n-2)(2n-k)(n+k-3)^2(n+k-2)^2(n+k-1)^2] > 0`.

This validates the important algebraic linkage from H positivity to the curvature inequality, beyond merely rerunning the supplied polynomial expansion. The polynomial certificates are explicit, use exact coefficients with strictly positive shifted coefficients over their stated domains, and their supplied verifier passed during the certified replay. This existing proof supports the symmetric-sector sign for every n≥4 without the faulty phase-debt step.

Therefore the defect must **not** be reported as proof that Theorem 1 is false, or as absence of all published support for the symmetric-sector conclusion. Nevertheless, the alternative does not prove (A.31), and the false Eq. (35) remains in the present source package while the main proof explicitly relies on its derived bound. The present no-error promotion gate is not met. Documenting this already-present alternative is scope assessment, not repair.

## Other completed analytic reconstruction and controls

| Component | Mechanism independently checked | Evidence and boundary |
|---|---|---|
| Forward dynamics and local curvature | Exact original mutant-subset transition matrix; Taylor expansion of `2x/(1+x)` through second order; exact absorbing solves | `fresh_forward_controls.py`: 91 checks. All three sector values at n=3,4,5 where present; vanishing first variation; mixed-sector orthogonality; positive leading principal minors of the full 8-dimensional directed tangent at n=4 |
| Geometric union dual | Inclusion–exclusion for the visited set of a fair-geometric sequence; full nonempty union chain; exact coverage of each starting mutant set | `fresh_dual_controls.py`: 111 checks, complete n=3 and nonreversible rational n=3,4 examples |
| Marked/active stationary identity | Independently assembled rectangular A,R, K=RA and M=AR, including empty-cache states; exact stationary flux and collision normalization | Same fresh dual controls; verifies `rho=m/n`, marked current relations, and `nu(H)=1/m` |
| Perturbative and representation reduction | Stationary resolvent expansion, rank averaging identity `S Delta S=0`; row/column-balanced decomposition and permutation-sector dimensions | Reconstructed on paper; finite full-tangent controls support normalization and cross terms. No claim of independently auditing all background representation-theory literature |
| Standard and antisymmetric positivity | Standard positive Schur operators and barrier residual; antisymmetric positive decreasing rank recurrence and sampling averages | Main Appendix A read in full. Fresh standard exact matrices N=2,…,9, barrier polynomial, and finite rank-Poisson checks. No defect found in these sectors |
| Symmetric finite cases and displayed constants | Exact signed two-channel matrix, direct rational scalar; beta/epsilon as printed; discriminants | `fresh_phase_controls.py`: 6622 checks, including direct N=3,…,39; all 248 printed finite margins N=40,…,287. Logical limitation above is essential |
| Strong selection | Expand original extinction equations in epsilon=1/r; complete positivity makes the limiting transient inverse finite; singleton and pair terms yield the stated incoming-column sum of squares | Fresh rational nonreversible full-chain calculations n=3,4,5 match leading term and 1/r deficit. Equality means J after column normalization, not equal unnormalized edge weights across different columns |
| Noncomplete or reducible support | Imported strongly connected theorem plus source-SCC fixation restriction; more than one source SCC precludes fixation; a proper unique source gives a strict uniform-in-r gap from the limiting complete baseline | Analytic reconstruction; conditions discussed below |
| Weighted triangles | Exact six-state absorption and determinant expression; main homogeneous nonnegative numerator/equality argument read | Four independent rational examples, including equal weights and a deleterious r control, agree exactly; supplied full symbolic/SOS checks pass |
| K4 families, monotonicity, growing-degree consequence | Main low-order proof and Appendix B/C read; monotone threshold coupling; harmonic-degree bound | Supplied exact checks pass. No independent full symbolic rederivation of every K4 coefficient before stopping, so no separate exhaustive certification claimed |

Total fresh checks: **6917** (91 forward + 111 dual + 6622 phase + 93 targeted). This number measures individual finite or symbolic controls, not a mathematical probability of correctness.

## Primary imported theorem interface

The load-bearing external result for the strong-selection corollary is Tkadlec et al., *Limits on amplifiers of natural selection under death–Birth updating* (2020), official primary text: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007494 . I checked its model and Theorem 1: finite loopless strongly connected directed weighted structures, noncomplete support, uniformly placed singleton, death–Birth updating, eventual suppression. Its stated restriction on edge weights can be met by a global rescaling without changing this model's normalized replacement probabilities. It does not supply the complete-positive case, which the reviewed manuscript derives separately. The reviewed source-component argument addresses the absence of strong connectivity. No stronger family-uniform conclusion was inferred.

Svoboda et al. (2024), https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012008 , was consulted as primary context for simultaneous amplification; it is not a substitute for the missing phase-debt comparison. Harris and ancestral-selection references are contextual for the explicitly derived finite dual; I checked the finite mechanism directly rather than assume a general duality theorem supplies unverified hypotheses. Other background bibliography was not exhaustively re-audited after the stopping defect.

## Strongest verified result and remaining gap

The finite chain model, marked collision identity, local expansion/normalizations, tested exact Hessian values, complete-support strong-selection coefficient and rigidity, and the scope of the imported noncomplete-support obstruction have independent analytic and exact computational support. The original package also contains an alternative all-n symmetric-sector curvature proof whose main derivation, certificate linkage, and replay check successfully; thus the main local-optimality conclusion retains substantial, specific published support.

The exact outstanding error is the false Eq. (35) in the supplied phase note. Its claimed implication to main (A.31) is unsupported by the stated Y majorization, leaving the displayed phase proof of (A.36) incomplete. No pointwise falsification of (A.31) or main theorem was established. No repair, alternate majorant search, revised submission, website edit, spreadsheet write, Git operation, publication, or outreach was performed. The bounded defect review is complete; full auxiliary-material validation was deliberately stopped once the disposition was supported.
