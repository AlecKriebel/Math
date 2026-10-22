# Computational and packaging adversarial audit: PR905 / 30000717

Reviewed frozen head: `330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a`.
Reviewed proof SHA256: `a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1`.
Reviewed public manifest SHA256: `1492167c7a7cfeb168976aa4d91b32c0be56c3b58de4090c417785a9d324a765`.

## Verdict and scope

**PASS for the frozen computational claims and elementary universal obstruction, with the boundaries below explicitly preserved.** All submitted exact outputs reproduce. Independent controls rebuilt with Python integers and `fractions.Fraction`, without SymPy or packet imports, find no algebraic discrepancy. The all-epsilon and unbounded-degree conclusions follow from the written argument; none is certified merely by the finite checks. No formal certification, historical priority, or human peer review is claimed.

The strongest mathematical deduction checked here is: for either stated ideal J_R or K_R, for every real constant c, R+c cannot be a finite sum of squares of real polynomials modulo the full real vanishing ideal. In particular this implies the author's theorem for every epsilon≥0 and the failures modulo the original ideal, ordinary radical, and real radical. The negative-c case follows simply by evaluation on a zero line and is a boundary control rather than a new research contribution.

No central mathematical gap was identified in this route. Source accuracy and the exact catalogue-to-publisher formulation are separately assigned; this family verifies source-free packaging rather than authenticating historical retrieval or priority.

## Reproduction evidence

All execution used disposable packet copies. The original thirty-file inventory was recorded before and after and remained identical. SymPy1.14.0 was pinned for submitted replay; own algebra controls use only the Python standard library.

| Control | Result |
|---|---|
| Author verifier | 185 guards; stdout byte-identical to author/checks.json |
| Historical AuditA verifier | Result file byte-identical to its saved exact controls |
| Historical AuditB verifier | 51 guards; stdout byte-identical to its saved output |
| verify_publication.py | PASS normally, under -O, and with PYTHONOPTIMIZE=2 |
| mutation_tests.py | 61 mutations rejected normally and under -O |
| Own independent exact_controls.py | 125 explicit guards pass, identical output normally and under -O |
| Independent changed-packet classes | Listed-file symlink, unlisted-directory symlink, hidden and empty unlisted files, changed manifest rejected |

The replay program records full stdout/stderr, saved-output comparisons, mutation outcomes, original hashes and byte counts in `results/replay_and_attack.json`. The finite computations agree with the frozen assertions and their stated limited scope. Historical AuditA's saved exact-only scope is intentionally preserved; its epsilon supplement and frozen acceptance, not that old JSON scope, supply its later epsilon reasoning.

## Independent arithmetic mechanism

`checks/exact_controls.py` represents a polynomial as an exponent-to-rational-coefficient dictionary and implements addition, multiplication, differentiation, exact substitution, whole-line restriction, Fraction Gaussian elimination and determinant computation. It imports neither the candidate verifier nor its data. The relevant calculations are equality of entire polynomial coefficient dictionaries, rather than point samples or numerical tolerance tests.

It verifies the ordered Schur identity and square specialization, all coordinate and sign symmetries, and the ordered expansion

F(c+w+u,c+w,c)=c u²+c u w+c w²+u³+2u²w.

The signs of these five coefficients prove the ordered case for u,w,c≥0; symmetry then covers squared real coordinates. The identity is an exact algebraic check. The step converting it to global nonnegativity is a mathematical deduction from signs and ordering.

It verifies R and its full gradient vanish identically on each of the ten zero lines; J and K vanish there and on all three axes; on every axis R=t⁶ and the gradient is 6t⁵ in the axis direction. Euler's identity also holds, confirming the distinction from the actual gradient ideal.

The independent homogeneous evaluation ranks in degrees0,1,2,3 are 1,3,6,10 and the cubic determinant in the author's specified order is exactly −128. Degree4 has rank10 with domain dimension15. The nonzero quartic xy(x²−y²) vanishes on all ten directions and evaluates to6 at (2,1,0). Consequently no assertion that all homogeneous degrees are injective has been made or is available: the axis degree argument is essential.

The literal Q diagnostic is also rebuilt: Q=(1−xy)²+y²−1/2, its products are 2y²(xy−1) and 2x²(xy−1)+2xy, Q(0,0)=1/2, Q(2,1/2)=−1/4, and Q(1/t,t)=t²−1/2. The exact branch checks show y=0 forces x=0, while xy=1 makes the second product equal2. Hence the real product variety is just the origin. The strict lower bound and unattained infimum are logical deductions: Q+1/2 is a sum of two real squares; equality would force y=0 and xy=1 simultaneously; the reciprocal path tends to −1/2.

## Universal logic and boundary cases

Let W be the union of the ten whole real zero lines and one coordinate axis. The computed restrictions prove W is contained in both real varieties. For any h vanishing on the corresponding real variety, h vanishes on W. Ordinary-radical membership suffices because h^N∈L evaluated at a real common zero gives h^N=0. Real-radical membership also suffices directly from its defining even-power-plus-squares equation. The proof does not require radical computation or a real Nullstellensatz.

Suppose R+c=Σ_{j=1}^m q_j²+h with real polynomial q_j and finite m. If c<0, any zero-line point gives a negative sum of real squares and a contradiction. For c≥0, restriction to the complete real line tv gives Σ_j q_j(tv)²=c, so each q_j(tv) is bounded by sqrt(c) for all real t and is constant. Alternatively, in a finite sum of real polynomial squares the largest nonzero degree yields a strictly positive leading coefficient in their sum, so a constant sum forces constant summands.

Write each q_j as its finite homogeneous decomposition. Constancy on each line makes every positive-degree component vanish at the corresponding ten directions. The checked injectivity eliminates precisely degrees1,2,3. For c=0 constants vanish too; for c>0 they may be nonzero and are retained. No component of degree≥4 is declared identically zero.

On the axis the certificate becomes t⁶+c=Σ_j q_j(t,0,0)². The left side is nonzero, so at least one axis restriction is nonzero; an empty sum already contradicts the identity. For any finite number of summands of arbitrary ambient degrees, the largest degree D among nonzero axis restrictions therefore exists. If D>3, the coefficient of t^(2D) in the sum is a nonempty sum of squares of nonzero real leading coefficients and is positive, contradicting the degree-six left side. Thus each axis restriction has degree≤3. Its coefficients of degrees1,2,3 were already eliminated, and its higher-degree axis coefficients vanish by this bound. All axis restrictions are constant, contradicting t⁶+c.

This reasoning covers c=0, every c>0 without a fixed numerical epsilon, negative c, empty/zero summands, arbitrarily many finite summands, and arbitrarily high ambient degrees. It does not use finite sampling in t or an SOS degree cutoff. Coefficients must be real and the sum finite: complex squares t^(2D)+(i t^D)² cancel, and signed sums also destroy positivity. Infinite series, rational functions, denominators or extra inequality multipliers are different certificate cones. Constants do not alter derivatives, so J_(R+c)=J_R and K_(R+c)=K_R.

The tangency-variety equivalence also survives edge checks: if a polynomial is negative at0 then0 is in its tangency variety; otherwise a negative point supplies a nonzero-radius compact sphere. A minimizer on that sphere remains negative, and its gradient is a real scalar multiple of the radius vector by the regular-constraint multiplier rule. Thus all minors vanish. This requires neither boundedness below nor attainment of a global infimum. For n=1, the empty generator list already gives the whole line as variety. The literal Q conclusion is kept separate from this tangency argument.

## Adversarial findings and exact gaps

1. **Standalone supporting scripts can falsely pass under optimization.** Each of author/verify.py, historical AuditA and historical AuditB uses `assert`. In disposable copies, replacing R by R+1 destroys the zero-line and specialization identities: normal execution rejects the fixture, but -O returns PASS. The optimized author and AuditB stdout is even byte-identical to their saved PASS output because the changed constant does not affect their reported derivatives or matrices. The fixture is substantive rather than a syntactic broken-script test. The publication wrapper rejects all these changed packets, uses explicit `require` guards under -O, removes PYTHONOPTIMIZE and launches replay children with -I/-B and no optimization flag. **This is a limitation of direct standalone invocation, not a failure of the documented frozen publication command.**

2. **Integrity requires a trusted external manifest digest.** A changed README containing an arbitrary false claim, a recomputed manifest, and a self-supplied new digest can pass the integrity/exact-replay wrapper. The unchanged trusted digest rejects that packet. This is the explicitly documented trust model, not mathematical certification. The hard-coded proof and author-manifest anchors reject a vacuous-author script even after nested/public rehashing. A count of checks, a saved PASS file and output identity alone cannot establish proof truth; this audit independently checks the algebra and logic. This family's pin came from ORIGINAL_SNAPSHOT.json; independently agreeing it with the PR description is the parent review's responsibility.

3. **Non-regular filesystem objects are outside the exact-file scan.** An unlisted FIFO passes `validate`, because inventory includes `is_file()` entries and the symlink guard does not classify FIFOs. This is a concrete low-impact filesystem-hardening gap if the tool is advertised for arbitrary extracted filesystem trees. A FIFO is not a regular byte file or Git-trackable blob and carries no redistributed source bytes in this PR. It does not falsify the submitted thirty-file Git packet's integrity. An optional hardening change would reject anything other than ordinary directories and regular files; no original file was changed here.

4. **Current source-free contents, historical provenance limits.** All thirty frozen files are UTF-8 .md/.py/.json/.txt authored artifacts, code, mathematical data and citation/hash metadata. No PDF, source-page render, source corpus, catalogue-record file, full article extract or private coordination file is present. The packet scripts require no network or source assets for reproduction. Historical claims that source hashes were freshly retrieved, the current catalogue's accuracy, novelty and exhaustive coverage cannot be inferred from these byte manifests; this family's result is confined to current contents and reproduction. No outside communication or source retrieval occurred.

## Artifacts and completion

The intentional review files are listed by SHA256 and byte count in `MANIFEST.json`. `RESEARCH_LOG.md` records timestamps and estimated completion checkpoints. The review is complete for this assigned family; strongest verified result and all limitations are above. No Git mutation, commit, push, release, external contact or edit to the original snapshot occurred.

## Portability follow-up before publication freeze

The completed initial review seal (manifest SHA256 `316be9b7734a117f61d2eff0ad1c72569c86e9457ae55b0a26895063a6e126d1`) and predecessor versions of the changed reports/runner are preserved in `history/initial_20261013T043359Z/`. Historical replay results remain unchanged. The current manifest seals that history and the portability update together.

The supplemental replay/attack runner now prefers the archive-root layout `original_packet/` next to `reviews/computation_family/`. If that archive directory is absent it uses the original historical workspace layout. It enforces fixed original public-manifest and proof hashes before any replay. By default children use the running Python interpreter; `--python PATH` instead selects an explicit interpreter with SymPy1.14.0. The runner itself uses only the standard library, so this explicit-interpreter mode works from a Python lacking SymPy. `--result-name NAME.json` preserves existing historical output by writing a separate result file. The portable archive layout was fully replayed in a disposable extraction; its thirty-file original packet remained unchanged. Evidence is in `results/replay_and_attack_portable.json` and `results/PORTABILITY_CHECK.json`.

The parent audit independently confirmed that the live PR905 description displays the frozen public-manifest hash. `PR_DESCRIPTION_ANCHOR.json` records that confirmation and attribution. This closes the review-level anchor-agreement task noted above; this family did not perform an additional network lookup or make outside contact.

The release's supported entrypoint is `verify_package.py`. Its new outer-package validator rejects special filesystem entries, retains immutable original proof/manifest anchors, and launches isolated replay children without optimization. The FIFO and standalone-optimization findings above concern the unchanged historical original validator and raw supporting scripts. They are deliberately retained as adversarial historical evidence; they do not describe acceptance by the new supported outer wrapper. This family inspected the outer-wrapper code, while the parent is responsible for its final package validation.

The full supplemental replay/attack runner is included and portable, but it writes results. Run it in a disposable copy of an extracted archive so accepted release bytes remain available for the outer integrity verifier. The supported wrapper handles its own disposable copies and is the ordinary reproduction command.
