# Independent second whole-preprint adversarial review

PR359 / problem30001370 / OWR-4132-003. Review namespace `preprint_review_02`.

**Verdict: PASS for the exact original common-boundary claim in the pinned submission. No mandatory mathematical, scope, metadata or package repair was found.** This is an independent AI adversarial review, not external human peer review. This report was prepared for root's draft read; authoritative final closure status is recorded separately in `CLOSURE.json` after the approved one-shot seal.

The strongest checked result is

\[
 W_0=\overline{\bigcup_{n\ge0}F^{-n}\{1\}}^{L^1(\mathcal D)}
     =\partial_{\mathcal D}W_+=\partial_{\mathcal D}W_-.
\]

It covers every nonnegative integrable probability density on `[-1/2,1/2]`, with the relative `L1` topology, for `0<A<=2/5` and `6<B<=16`. The approximation uses actual self-consistent orbits. No rate of attraction, lower density bound, boundedness, smoothness or membership in the integral-representation class is assumed. There is no assertion about `A=0`, `B=6`, a different feedback family, the separate finite-particle mixture conjecture, or an `L1` differentiable stable manifold.

## Independence and primary-source baseline

The original question was treated as a hypothesis. Before candidate access, I read Keller's entire contribution at printed2713-2715/PDF15-17 in the official OWR49/2009, the entire1944-line author-hosted BKZ extraction including its appendix and references, relevant arXivv1 sections, and selected original PDF layouts. The author and arXiv PDFs each actually have36 pages. They are distinct accessible manuscripts, not the final journal PDF. Source URLs, actual input sizes/SHA and inspection limits are in `SOURCE_INVENTORY.json`. Raw source copies, extracts, comparison output, layouts and receipts are private.

The exact source-first baseline bytes were sealed before candidate release at observed `2026-10-03T23:35:12.429687Z` in `PRIMARY_GATE.json`, SHA `9c199a9b7aa81b3d498943a1b2f3a15e9f36829d60f76f6a700f149d91c4e177`. Its `PRIMARY_BASELINE.md` SHA is `fa67e495327ccf5824c44d8e60599e9319b0f0ae9dda186551c08d72c7fed731`. The initial gate draft had an accidentally future log time; that was corrected before the reported gate and disclosed there. Initial intake records hashes at actual observation and Python's actual `sys.argv=['-']`; it does not pretend to provide a reconstructed full transport receipt or earlier hashes.

After root released the exact four candidate pins, I read the entire current note first, assessed its proof independently, then read the original three author turns and supporting programs. Existing mathematical/priority reports were subsequently read as evidence to audit, not as proof premises. I did not read the first whole-preprint review, its root verdict, or any closed sibling whole-review namespace.

The primary baseline establishes the precise old/new distinction:

- OWR Theorem2 states all-density `L1` three-limit convergence and open stable basins for the prescribed tanh rectangle. Keller then explicitly states the common-boundary conjecture and separately discusses dense stable-basin union.
- BKZ Theorem2 and Proposition3 give the all-density convergence/openness foundations under their Assumptions I/II. Their Example1 discusses tanh up to `B<=18`; the original question and current theorem retain the narrower `B<=16`. S-shape of `G` alone is not the S-shape assumption on the stationary feedback composition. AppendixA's numerical/symbolic evidence is not silently upgraded into a new universal analytic proof. The note invokes the previously stated OWR rectangle theorem as a foundation.
- BKZ Proposition4 proves both-boundary membership on the central part of the canonical mixture class and supplies the seed `1`. That class consists of mixtures of `w_y=(1-y²/4)/(1-xy)²`, `|y|<=2/3`, hence has densities between1/2 and2. It is not `L1` dense in all probability densities. The extracted `D0/G0` glyphs denote PDF primes; I identified the class by its formulas.
- Published finite-time shadowing, regular-space differential calculations and the seed do not by themselves yield the reverse common-boundary inclusion for every rough law. Open image radii may shrink along an orbit. A uniform nonlinear backward lift, together with an actual `L1` comparison, was the source-first falsification target.

The global convergence/openness and boundary seed are credited prior results. The checked additional argument is density of finite preimages in the entire central basin, followed by the relative-topology deduction.

## Independent analytic audit of every proof step

**Open map and zero fibers.** The factorization `T_r=T_0 o h_r`, `h_r(x)=(x+r/4)/(1+rx)`, is exact. Signed-density pushforward `Q_r` is an `L1` isometry and jointly strongly continuous: first establish the assertion on smooth densities by the explicit inverse/Jacobian, then approximate in `L1` using isometry. To invert `K(u)=Q_{G(phi(u))}u`, solve `r=G(E_v h_{-r})`. The inverse transport decreases in `r`; therefore the residual is strictly increasing by at least its parameter increment. Its signs at `-A,A` bracket a unique root. Joint continuity of the residual and uniqueness give a continuous inverse; the bounded spatial derivative also gives the stated root comparison. Thus `K` is a homeomorphism of the relative probability-density space.

For fixed `w`, the section of `P_0` uses `q_w=w/(P_0w o T_0)` only on positive fibers, and `q_w=1` on zero fibers. Positivity of both branch contributions makes `w=0` almost everywhere on each zero fiber. Consequently `0<=q_w<=2`, `P_0q_w=1`, `R_w z=q_w(z o T_0)` is positive, preserves mass, has exact norm `||R_w z||1=||z||1` for signed `z`, and `R_w(P_0w)=w`. A small perturbation of the output lifts within the same relative `L1` radius. This proves openness everywhere, including boundary points of the positive cone. With the homeomorphism it proves continuity, openness and surjectivity of `F`. For each stable basin `B`, tail invariance gives `F^-1B=B`; continuity and openness then give `F^-1(∂_D B)=∂_D B`. No unsupported globally uniform openness radius is used later.

**Uniform self-consistent inverse.** On any probability space take bounded input `Z` in `J=[-1/2,3/2]` and set `X=b_r(Z)`, with

\[
 b_r(z)=\frac{2z-r-1}{r+4-2rz},\qquad r=G(E b_r(Z)).
\]

Here `∂_r b_r=-(1-4b_r²)/(4-r²)<=0`. The same scalar-residual argument supplies unique feedback for every input, not only densities. Differentiation along the bounded affine input path is legitimate for every fixed `A>0`; denominators stay positive, the scalar implicit derivative denominator is at least1, and all differentiated quantities are bounded. The `L2` norm is on random variables, not on the original density.

Writing `q=1-4X²`, `β=G'(EX)/(4-r²)`, the derivative is `L D^-1`, where `L=I-βq E/(1+βEq)`. If `m=Eq`, `s=Eq²`, then `m²<=s<=m`. On the span of `1,q`, the appropriate orthonormal basis gives the lower triangular matrix with entries `1/(1+βm)`, `-β√(s-m²)/(1+βm)`, and1. On the orthogonal complement `L` is the identity. For `C=1+β/4`, the lower diagonal of `CI-L*L` is `β/4`, and its determinant is

\[
\frac{\beta^2\{(Cm-1/4)^2+C(m-s)\}}{(1+\beta m)^2}\ge0.
\]

Degenerate `β=0` and constant `q` cases are directly harmless. This proves `||L||²<=1+β/4`, a universal moment-constrained operator bound rather than an inference from finite Gram matrices.

For `a=|r|<=2/5`, `G'(EX)<=16-100a²` and the inverse expansion bound give

\[
 \|D V\|^2\le U(a)=\frac{(2+a)(4-13a^2)}{2(2-a)^3}<7/10<(21/25)^2.
\]

The strict inequality follows from the exact identity

\[
7(2-a)^3-5(2+a)(4-13a^2)
=172(a-13/43)^2+12/43+58a^3>0.
\]

Integration along the path proves the claimed global contraction with `κ=21/25`. It includes the upper endpoints `A=2/5,B=16` and the `β=0` norm case. The proof uses no `A`-uniform bound on `G''` as `A` tends to zero.

**Correlated labels and genuine nonlinear preimages.** For fixed `u in W0`, work on `(I,u dx)` with its actual orbit `X_j` and branch labels `a_j`. The terminal cumulative map sends the nonatomic law of `X_n` to uniform law even with flat intervals, and moves points by at most `ε=||u_n-1||1`. Backward recursion `Y_j=V(Y_{j+1}+a_j)` preserves the old joint labels. A branch-event sublaw is dominated by the total absolutely continuous law; its inverse branch image is absolutely continuous. Induction from terminal uniform law proves that every `Y_j` has a density. Null endpoint events cannot select a wrong branch. The parameters are exactly `G(EY_j)`, so the starting law `v_n` satisfies the genuine equation `F^n v_n=1`. Neither independent labels nor unchanged feedback is assumed.

The old variables solve the same inverse equations. Comparing on the same probability space cancels the identical labels and yields `||Y_j-X_j||2<=κ^(n-j)ε` and `sum Δ_j<=84ε`. This is precisely the uniform-in-time mechanism missing from a bare open-map argument.

**Non-strict cumulative maps, absolute continuity and exceptional sets.** The deterministic backward maps glue at the old cut to the new cut because the next map fixes both endpoints and `b_ρ(1/2)=-ρ/4`. They are continuous, nondecreasing, onto and absolutely continuous on the whole interval. The composition reasoning is specific: an inner smooth bi-Lipschitz old branch, then the later absolutely continuous map, then a smooth Lipschitz inverse branch, followed by finite continuous gluing. It does not assert that arbitrary compositions of absolutely continuous maps preserve absolute continuity.

The displacement estimates give `d_0<=183ε/8` and `sum d_j<=181ε/2`. For each fixed finite `n`, every old cylinder map is smooth bi-Lipschitz onto its image. It pulls the derivative exceptional sets back to Lebesgue null sets. Thus the almost-everywhere chain rule gives `H_0'=u_n(X_n)R_n`, with no division by a density. Every quotient in `R_n` is a positive smooth map Jacobian. Spatial/parameter logarithmic sensitivities yield `|log R_n|<=213ε`. There is no assertion that an uncontrolled infinite cylinder intersection transports null sets; each proof is finite before taking the sequence limit.

**Lebesgue comparison and actual `L1` convergence.** The estimates on `(I,u dx)` alone would be inadequate to control `H_0'`. The note explicitly switches to Lebesgue input law: for the old external parameter sequence, `c_n=P_{r_{n-1}}...P_{r_0}1` remains a canonical mixture and satisfies `c_n<=2`. The displayed branch mixture identity, its weights, images and bounds hold on the whole closed parameter rectangle. This uses the canonical class only to control a reference orbit, not to approximate `u` by that class. Transfer duality and nonnegative truncation then give `∫|u_n(X_n)-1|dx<=2ε`. Combined with the logarithmic bound this proves

\[
 \|H_0'-1\|_1\le 2\epsilon e^{213\epsilon}+e^{213\epsilon}-1.
\]

For an absolutely continuous nondecreasing onto `H`, the identity `H_*(H'dx)=dx` follows from antiderivatives of continuous test functions and permits flats. Pushforward contracts the full signed-measure variation norm. For continuous `g`, comparing with `g(H)H'dx` yields exactly the modulus/Jacobian bound printed in equation10. Intermediate `H_*(g dx)` may have atoms; the measure inequality still holds. The actual `H_*(u dx)=v_n dx` is already absolutely continuous by the preceding backward-law induction. Consequently this comparison really gives `||v_n-u||1`, not just weak convergence. Fix a continuous approximation `g` first, let `n` tend to infinity, then let the approximation error tend to zero. Constants multiplying `g` need not be uniform in the approximation. No unproved rate or exchange of these limits is needed.

**Topological completion.** The cited all-density trichotomy and open disjoint stable basins make `W0` closed and imply `∂_D W± subset W0`. Every finite preimage of the seed lies in both boundaries by complete backward invariance. The proved `L1` finite-preimage density and boundary closedness give the reverse inclusions. These are boundaries relative to the probability-density set, not the signed `L1` vector space.

## Falsification controls and complete reproductions

The two new programs implement mechanisms chosen from the source-first gap, not copied assertion counts from other reviews.

`independent_controls.py` checks exact inverse endpoint/sensitivity cases, a flat central law with zeros, the lower-bound obstruction to density of the canonical class, and an unbounded symmetric integrable central law. Its discrete correlated-label control reconstructs different second moments from independent versus identical two-bit histories despite identical bit marginals. This last example is explicitly a discrete inverse-law control, not claimed to be a density counterexample. Its1052-byte JSON output has no `status` field; exit0 and its exact assertions are the observed facts.

`independent_transport_controls.py` constructs four full correlated absolutely continuous branch histories at depths1,2,3,7. Every label is determined by the same terminal uniform variable; the rough starting law has central zero regions, but all feedback fields are zero and its actual finite orbit is uniform. It also constructs flat transports collapsing a central interval. `H_*dx` has a point mass and its full variation difference is exactly `4δ=||H'-1||1`, while `H_*(H'dx)=dx`. Polynomial moments through degree7 are genuinely integrated using the affine branch coefficients. Nine finite-cylinder length controls challenge null-set pullback. The123 exact assertions are finite controls supporting, not certifying, the preceding analytic argument.

The first transport implementation's moment assignment was too tautological to be useful. Before editing, I preserved its exact executed3673-byte source SHA `14080e705d84c756ea8a8b535fa46faa6b12918613d7fdd980c939f2eff47daf` in the private code-version directory, recording honestly that this was a post-run copy. I strengthened only that control, then reran it. Both complete attempts are retained; their whole2433-byte outputs happen to be identical. This is an inadequacy corrected, not a fabricated failed execution. Current code SHA is `89ec030cdf761082fa284589ac5fc8b8658da675afc23d1684a8a7f067b8716d`.

All programs were read before execution. Symbolic programs used the already present `/opt/homebrew/bin/python3.11`, actually Python3.11.8/SymPy1.14.0; its resolved runtime and native version output are retained. Stdlib programs also used existing Python. No installation or network fetch occurred. The following entire stdout files were reproduced and compared byte for byte, including whitespace and every field:

| Run | Output bytes | Whole expected comparison |
|---|---:|---|
| Original turn1 |310| Stored turn1 checks identical |
| Original turn2 |294| Stored turn2 checks identical |
| Original turn3 |459| Stored turn3 checks identical |
| Historical independent program |518| Stored independent checks identical |
| Supplement default |616| Current metadata-repair stdout identical |
| Supplement full |616| Current metadata-repair stdout identical |
| Priority public-only verifier |370| Current metadata-repair stdout identical |

The source-enabled original wrapper also passed against all three exact historical PDF payloads. Its510-byte output is retained. Original author assertions total60934; historical independent assertions18678; supplement topology controls10116 and backward exact controls19123. Numerical backward corroboration uses a labeled `1e-12` summary tolerance; exact fields and the universal polynomial proofs are separate. Original turn3's40-row rational certificate and older `24/25` constants are preserved as history; the current paper correctly uses the sharper `21/25` argument. A historical Fourier comment overstates what its code directly checks—the code checks an integer recurrence rather than symbolic trigonometric functions—but the accompanying analytic Fourier argument is valid and the current nonlinear proof does not depend on that coding description.

`REPLAY_BINDINGS.json` indexes all11 retained standalone executions, their actual argv/cwd/start/end UTC/exit, complete private stdout/stderr sizes and SHA, actual native receipt bytes, and observed code versions. Every replay exited0 with empty stderr. There are no hidden failed process attempts in this review. The root independently replayed both final new controls and compared the entire1052/2433-byte outputs; its separate preseal receipt is linked without claiming closure.

## Whole package, schemas, original history and presentation

`CURRENT_BINDINGS.json` binds the current four submission files: TEX18361, PDF94713, ZIP162121, metadata2240 bytes. All supplied SHA pins match. The TEX and metadata copies inside the ZIP are byte-identical to the canonical files. The original38-entry snapshot, including the target queue file, was checked entirely by bytes/SHA; all37 original problem files are unchanged in ZIP `candidate/`. The target queue row says `claimed_solved` and3/5 author turns. I read its relevant row, not the unrelated queue's full mathematical contents.

All74 ZIP members were read in full as bytes and UTF-8 text. The manifest's73 payload records, all nested author/review publication manifests and predecessor SHA links, the priority public inventory, original source manifest, controls' output schemas, and metadata were inspected. `FILE_SCHEMA_INVENTORY.json` gives each member's full recursively enumerated JSON schema, sizes, SHA, ZIP attributes, source imports or CSV columns/row counts. Duplicate JSON keys and nonfinite literals are rejected; ZIP names are unique and safe, all are regular files, and no symlinks or hidden binary payloads occur. I recomputed25 historical Git blob IDs from the supplied candidate bytes. This does not assert a fresh remote API or local Git-object retrieval.

The priority namespace's145 private manifest records have their full schemas, safe paths and closure hash bindings checked. Their private payloads are deliberately absent from the public ZIP and were not freshly reverified here. The public-only replay truthfully reports `private_files_checked=0`. This is a distribution/custody limit, not a missing mathematical premise: I independently read the primary-first foundational sources and proof. Existing report evidence about historical source scans, web queries, failures, dates and remote checks is distinguished from our native observations.

The six-page current PDF was rendered and all six pages visually inspected. Title, definitions, equations, proof transitions, references and AI/review paragraph are legible, without clipping or missing content. The native PDF inspection confirms six unencrypted letter pages, no forms or JavaScript. It was not rebuilt or edited by this review.

Zenodo metadata describes the exact same theorem and finite-preimage strengthening. The corrected plaintext interval wording `A in (0,2/5] and B in (6,16]` has the original mathematical meaning and avoids an HTML ambiguity. ORCID `0009-0001-9320-500X`, author, date2026-10-03, version1.0, preprint type, CC-BY4.0 and the PDF/ZIP filenames are consistent. These are local deposit specifications; no upload, DOI or external publication is claimed.

Priority attribution is adequate: BKZ receive credit for trichotomy, open basins, canonical representation, boundary seed and inverse expansion. The reviewed bounded priority dossier distinguishes later regularity/small-coupling/cone/local-attractor results from this all-density central-boundary result. Its alias/language and own-release metadata searches are weak negative evidence, not universal novelty certification. I read the complete dossier and query ledger after forming the proof assessment; I did not independently fetch all later papers or repeat its literature search. The final BKZ journal proof PDF was not obtained in that dossier, and that limit is explicitly disclosed in the note and metadata. No equivalence between the accessible manuscripts and final journal version is assumed. The result remains an unrefereed AI-developed preprint without independent external human review.

## Closure plan and exact remaining work

At the draft checkpoint the substantive whole-source/proof/package/layout/control review is complete. Completion estimate:95% of this scoped audit. The remaining work is root's full draft read and independent custody/verifier assessment, approval of one local seal, and read-only full/public closed-verifier captures outside this namespace. There is no identified unresolved proof gap in the exact stated claim. Universal novelty and external human peer review remain outside the achieved evidence.

The proposed public whitelist is recorded in `CLOSURE_PLAN.json`. The sealer will include only those named author-produced summaries/programs, with every other regular file confined below `private/`, then create one public manifest, one private manifest and one closure record. It refuses an already closed namespace. The verifier is read-only and rechecks inventory/provenance/output bindings, not an additional broad mathematical suite. Full verification checks private payloads and live external submission/source/output pins; public-only verification checks the public layer and honestly leaves private/external bindings unchecked.

After the single seal no namespace writes are permitted. Root's full native closed-verifier captures can use the external prefixes already proposed in `REPLAY_BINDINGS.json`; their actual final bytes/SHA will be indexed by root's external final gate without modifying this namespace. No canonical submission, Git/ref/index/PR, closed sibling namespace or outside individual was changed or contacted.
