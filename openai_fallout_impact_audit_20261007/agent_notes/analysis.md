# Impact assessment: published analysis papers, rows 41, 42 and 47

Checkpoint: 2026-10-07. Assigned assessment completion: **100%**. This is an importance/attribution assessment of the actual deposited manuscripts, assuming their stated results and required upstream inputs are correct. It is not a new proof audit or an exhaustive worldwide priority determination. No external individuals were contacted, no Git or spreadsheet mutation was made, and no paper was edited.

The final TeX was read, the deposited PDFs' title/abstract text was checked, and each deposited source archive's candidate `main.tex` was verified byte-for-byte against the local manuscript. The Lane–Emden archive also contains a separate upstream `sources/family370/build/main.tex`; that is not the candidate manuscript. The earlier project reports were used only for comparator context after the final claims and attribution had been read.

## Calibration

**A** rates the importance of the complete mathematical theorem if it were correct and novel as a standalone result. **B** rates the actual incremental contribution of this paper, taking its already available upstream input as given. For a single score describing *the author's published paper*, **use B**. Counting the inherited continuous or one-species breakthrough again would substantially overstate the note's contribution. These scores do not incorporate a separate penalty for being an unrefereed preprint.

| Row | Paper | A: complete theorem | B: actual paper contribution | Short characterization |
|---|---|---:|---:|---|
| 41 | Finite multispecies relativistic Vlasov–Maxwell | **9.0** | **6.5** | Physically significant large-data extension, using the upstream proof's central mechanism |
| 42 | Subcritical Lane–Emden a priori estimates | **8.5** | **4.0** | Useful full-range application package of an inherited Liouville theorem and established reductions |
| 47 | Commuting ergodic Hilbert variation | **8.0** | **5.0** | Important singular ergodic consequence, with explicit but largely established restriction/transference machinery |

The half-point precision is only calibration; plausible neighboring scores do not alter the main distinction. The actual contribution ordering is 41 > 47 > 42. None warrants 9–10 as an independent paper contribution under the assigned rubric.

## Row 41 — Signed impulse estimates and global smooth solutions for finite multispecies relativistic Vlasov–Maxwell

Published DOI: https://doi.org/10.5281/zenodo.23203334. Exact final source: `openai_followon_multispecies_vlasov_maxwell/publication/main.tex`; archive: `publication/upload-kit/source-and-verification.zip`.

**Actual claim.** Theorem 1.1 (source line 66) gives unique global smooth classical solutions of the three-dimensional relativistic Vlasov–Maxwell equations for every fixed finite species list with positive masses and arbitrary real charges. Densities are nonnegative smooth compactly supported functions of position and momentum; Maxwell initial fields have all derivatives bounded and finite L2 energy, and satisfy Gauss constraints. There is no smallness, symmetry or neutrality requirement. Particle phase support remains compact on finite time intervals. The paper also identifies joint bounded momentum as the continuation criterion.

**Lay explanation.** A collisionless relativistic plasma containing several kinds of charged particles can evolve forever under its own electromagnetic field without developing a finite-time mathematical singularity, for the stated smooth initial data. Oppositely charged species, such as an electron–ion type plasma, are covered.

**Importance.** As a theorem independent of the release context, this addresses a famous global regularity problem in mathematical kinetic theory, with a physically natural multispecies scope: A = 9.0. It is broad within this model and substantially stronger than small-data or nearly neutral global results. Current comparator [Mattingly–Pankavich–Ben-Artzi](https://arxiv.org/html/2609.29013v1) explicitly concerns small-data solutions and neutral-plasma decay/scattering; it does not supply arbitrary-data global regularity. This manuscript itself credits earlier mass normalization, multispecies formulation and continuation theory.

**New versus inherited.** Source lines 90–114 explicitly attribute the unrestricted one-species theorem, universal geometric cancellation and angular-selection mechanism to OpenAI family 362. The new work keeps the exact cross-species force coefficient `e_a e_b/m_a`, positive mass-weighted energy and separate species flows, and closes one simultaneous momentum bootstrap for distinct charge-to-mass ratios. The central cancellation is inherited and works for arbitrary timelike curves; the paper's work is proving the upstream analytic chain survives the species-dependent coefficients and shared field. Equal nonzero charge-to-mass ratios reduce immediately to the inherited scalar theorem and are expressly excluded from the genuinely new portion. Opposite charges are the simplest substantive extension. This is a solid specialist follow-on, rather than a second independent solution of the central kinetic problem: B = 6.5.

**Material limits.** Constants can depend on the fixed finite list of masses and charges. There is no massless or infinite-species limit, no momentum tails, no collision term, no curved spacetime and no long-time scattering theorem. Arbitrary smooth finite-energy fields without bounded derivatives are outside scope. The result is an unrefereed preprint, uses extensive AI assistance and claims no reproduced Lean certification. These verification facts matter to confidence but are not the main reason B is lower than A.

## Row 42 — A priori estimates across the subcritical Lane–Emden hyperbola

Published DOI: https://doi.org/10.5281/zenodo.23203323. Exact final source: `openai_followon_lane_emden/publication/main.tex`; archive: `publication/source-and-verification.zip`.

**Actual claim.** Theorem 1 (source line 78) treats classical nonnegative solutions of `-Δu = v^p`, `-Δv = u^q` with `n ≥ 3`, `p,q > 1` and `1/(p+1)+1/(q+1) > (n-2)/n`. It proves universal boundary-distance bounds with scaling exponents `α=2(p+1)/(pq-1)`, `β=2(q+1)/(pq-1)`, the corresponding gradient bounds and exterior decay. It also gives unrestricted zero-Dirichlet half-space nonexistence, uniform Dirichlet bounds on each fixed bounded C2 domain, and strong compactness in W2,r and C1,γ. A C2,θ boundary additionally gives uniform C2,θ bounds and compactness in C2,η for η<θ.

**Lay explanation.** Two functions feeding each other's nonlinear elliptic equations cannot form arbitrarily large interior spikes in the subcritical range. Their size is controlled by distance to the boundary; on a fixed smooth bounded domain the whole family of zero-boundary solutions stays uniformly bounded and compact.

**Importance.** The complete full-range theorem is valuable to nonlinear elliptic systems and provides the estimate package traditionally obtained from the Lane–Emden conjecture. Universal pointwise estimates on all proper domains themselves imply entire nonexistence by applying the estimate on growing balls. Thus the theorem's substantive full-range content is closely tied to the famous underlying conjecture: A = 8.5. The older [Polačik–Quittner–Souplet paper](https://doi.org/10.1215/S0012-7094-07-13935-8) establishes the relevant Liouville-to-estimate framework; [Quittner–Souplet](https://arxiv.org/abs/2407.04154) continues this established program. [Li–Li–Wei](https://arxiv.org/html/2510.06613v1) proves a new higher-dimensional exponent region, rather than the full strictly subcritical hyperbola.

**New versus inherited.** The final abstract and source lines 55–76 expressly state that this is an immediate consequence of OpenAI family 370's entire Liouville theorem and established PQS/QS reductions. The manuscript neither independently resolves the Lane–Emden conjecture nor invents a new transfer mechanism. Its contribution is a checked, explicit full-range formulation, normalizations, boundary blow-up account and exact regularity/compactness spaces. Dimensions three and four and substantial higher-dimensional regions were already accessible. The newly covered exponent range is inherited from the new upstream theorem. This is a useful technical consequence note: B = 4.0.

**Material limits.** Strict subcriticality, p,q>1, unweighted constant-coefficient equations and classical solutions are essential scope restrictions. No critical/supercritical theorem, weak-solution regularity, spatially variable coefficients or parabolic conclusion is supplied. Strong C2,θ boundary estimates are not inferred from a merely C2 boundary. The note has no independent formalization or reproduced full upstream kernel/axiom audit and is unrefereed.

## Row 47 — Bilinear ergodic Hilbert variation for commuting transformations as a consequence of annular triangular variation

Published DOI: https://doi.org/10.5281/zenodo.23204591. Exact final source: `openai_followon_commuting_ergodic_hilbert/main.tex`; archive: `publication/upload-kit/source.zip`.

**Actual claim.** Theorem 1 (source line 49) considers arbitrary commuting invertible probability-preserving transformations S,T and complex f,g in L3. For `H_N = sum_(0<|n|≤N) f(S^n x)g(T^n x)/n`, with H0=0, every r>2 pointwise r-variation has an L3/2 bound uniform in the system. This gives a maximal bound, almost-everywhere convergence, L3/2 convergence and convergence of the maximal tail in that norm.

**Lay explanation.** A signed harmonic-weighted combination of two observables along two commuting dynamics settles to a limit almost everywhere. The quantitative estimate limits its cumulative oscillation, even when one chooses the times of observation separately at each point.

**Importance.** Arbitrary two-generator actions are substantially beyond the opposite powers of a single transformation. The full pointwise variation is also stronger than norm variation and than a maximal bound. This is a major specialized singular-integral/ergodic consequence: A = 8.0. [Becker–Durcik](https://arxiv.org/html/2603.20173v1), Corollary 1.4, gives sharp variation for averages along opposite powers of one transformation and explicitly distinguishes the arbitrary commuting Cesàro problem. The present Hilbert theorem should not be advertised as solving that Cesàro problem.

**New versus inherited.** The source states that the full annular triangular Hilbert variation theorem of OpenAI's October 5 manuscript is the sole new analytic input and is not reproved here. The note supplies fixed positive-area cell restriction, half-integer radial endpoints, a summable signed O(k^-2) kernel error controlling the whole error variation, finite-menu/finite-window transference and a complete measure-theoretic convergence argument. Its actual incremental achievement is making a strong ergodic consequence precise and verifiable. The final source itself credits Demeter–Thiele for continuous-to-lattice/orbit-array reduction, DKST for positive-area phase integration and Calderón for transference. This merits a credible narrow consequence-paper score, B = 5.0, not a separate triangular-Hilbert breakthrough score.

**Material limits.** Symmetric odd Hilbert truncations, L3 inputs, commuting invertible probability-preserving transformations and r>2 are the exact range. No r=2 estimate, noncommuting case, wider input exponent range or one-sided commuting Cesàro convergence is proved. Maximal-tail convergence follows by dominated convergence once variation supplies an integrable maximal function; it is useful scope completion, not a second independent advance. The relevant upstream Lean files concern an older maximal theorem and do not verify full annular variation or this note; no formal certification or conventional human peer review is claimed.

