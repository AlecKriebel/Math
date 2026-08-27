# Independent referee report

## Review environment

- **Reviewer:** OpenAI Codex, GPT-5-based independent reviewer (the exact runtime
  build identifier is not exposed), using separate proof, code, literature/layout,
  and final adversarial audit passes.
- **Date:** 26 August 2026, America/Los_Angeles.
- **Submission reviewed:** `k2p-k3p-theta-ai-referee-v1.2.3`, with the main
  article `materials/combined-paper-clarified.pdf` (19 pages), followed only
  after the paper-first pass by the two supplied support PDFs (2 pages each).
- **Packet integrity:** all 37 entries in `PACKET_SHA256SUMS` matched before and
  after replay.  All 32 files under `materials/` were also byte-identical to the
  stated repository commit `3d3e4abee9f4dab9f5f1b3ec9f73740aa04c565c`.
  The annotated tag `k2p-k3p-theta-v1.2.3` resolves to that commit in the local
  repository, but the tag is unsigned; the packet therefore establishes
  self-consistency, not an external cryptographic trust anchor.
- **System:** macOS 26.5.2, build 25F84; Darwin 25.5.0 arm64; Python 3.14.6;
  Tectonic 0.16.9; Poppler `pdftotext`/`pdftoppm` 26.08.0; SymPy 1.14 for the
  clean-room reconstruction.
- **External sources checked:** the relevant formal statements and source
  conventions in [Brits et al. v2](https://arxiv.org/abs/2607.12919v2) and
  [Brits et al. v3](https://arxiv.org/abs/2607.12919v3), and the primary records
  for [Gross--Long (2018)](https://doi.org/10.1137/17M1134238),
  [Gross et al. (2021)](https://doi.org/10.1007/s00285-021-01653-8),
  [Gross--Krone--Martin (2024)](https://doi.org/10.1007/s11538-024-01314-z),
  [Cox--Gross--Martin (2025)](https://doi.org/10.1007/s11538-025-01506-1), and
  [Englander et al. v4](https://doi.org/10.1101/2025.04.18.649493).  I also
  checked the foundational Fourier references cited by the paper,
  [Evans--Speed](https://doi.org/10.1214/aos/1176349030) and
  [Sturmfels--Sullivant](https://doi.org/10.1089/cmb.2005.12.457).

## Executive assessment

The manuscript gives exact three-taxon distributions lying simultaneously in
a comparison-tree model and a strict level-two theta-network model under K2P
and K3P.  Its strongest contribution is not merely the compact
`Q(sqrt(71))` witness: it also supplies an edgewise strictly continuous-time
K2P witness, a quartic K3P parameter outside every globally character-relabelled
K2P parameter specialization, full ambient-rank calculations, local collision
geometry, an implicit-function continuation into the strict K3P rate cone, and
a one-blob grafting theorem for arbitrary binary trees.

I attempted to falsify these claims at four levels: direct derivation from the
paper, line-by-line inspection of all code and JSON, execution with targeted
mutations, and a clean-room symbolic reconstruction that imports no packet code
and reads no packet certificate.  I found no arithmetic defect, counterexample,
or missing mathematical implication that invalidates a central theorem.  In
particular, the clean-room calculation independently reproduced both exact
factorizations, all 64 Fourier coordinates, all 64 ordinary-state probabilities
using literal retained-graph pruning, the selected rank-9 and rank-15
determinants, and the K3P fixed-output tangent identity.

The proof-level distinction between finite computation and analytic deduction
is handled correctly.  The K3P strict-continuous-time point is existential,
obtained by the analytic implicit-function theorem from exact tangent data; it
is not presented as a closed-form nearby point.  The arbitrary-taxon theorem is
proved by a common-kernel argument; the four-leaf computation is correctly
described as a regression test rather than a finite proof for all taxon counts.

I do, however, find several correctable issues.  The most important is a
semantic-binding gap in the K3P certificate verifier: displayed Jacobian and
tangent names are checked separately from the descriptor fields that choose the
actual derivatives.  The present descriptors are correct by inspection, and
the intended derivative calculation was independently reconstructed, so this
does not overturn the theorem; it does mean the certificate framework can
accept a coordinated relabeling that makes its human-readable column labels
false.  The introduction also attributes “full” level-one identifiability to
two papers that establish generic results.  Finally, the reproducibility prose
should distinguish packet self-consistency from authenticity and distinguish
the K2P direct-pruning checks from the K3P Fourier/inverse-Fourier path.

Subject to these localized corrections, I regard the central mathematical
contribution as valid, novel relative to the checked primary record, and
publishable.

## Findings ordered by severity

### 1. K3P derivative names are not mechanically bound to their semantics

**Severity:** minor correction required, with high priority for certificate
assurance; no error found in the current mathematical witness.

**Locations:** `materials/src/verify_k3p.py:1052-1061,1073-1096,1210-1251`;
the `jacobian.columns` and `continuous_time.free_directions` objects in
`materials/certificate_k3p.json` and their sidecars; manuscript pp. 13--15,
especially TeX lines 426--501.

Each Jacobian column object contains a human-readable `name` and executable
semantics (`kind`, `edge_id`, `character`).  The verifier fixes the ordered
names but uses the other fields to construct the derivative without asserting
the complete expected name-to-semantics map.  The continuous-time free
directions have the same separation.  Consequently, a coordinated even
permutation of semantic descriptors and stored columns can preserve the
determinant, fixed-output equations, and transcript while making the displayed
column labels false.  Reticulation list order and some root-suppression source
labels likewise have executable but incompletely bound semantics.

I confirmed this experimentally in a disposable copy.  I kept the first three
names `e_rho_1.a_C/.a_G/.a_T` fixed, cycled their executable characters from
`(C,G,T)` to `(G,T,C)`, and applied the same even three-cycle to the stored
matrix columns and pivot coefficients.  The focused verifier exited zero and
ended with `ALL K3P CHECKS PASSED`.  The determinant is unchanged because the
cycle is even, and the tangent residual is unchanged because coefficients and
columns are cycled together, while the human-readable names are now false.

This gap does not make the current determinant or tangent wrong.  I manually
matched every current descriptor to the manuscript lists, and the independent
checker differentiated the manuscript's formula using the stated rows and
parameters and recovered

\[
\det J_*={h(10h^2+1)\over 2^{61}3^4 5^{14}}
\]

and `J_* p'(0)+F_{U_C}+F_{V_G}=0`.  The issue is that the shipped verifier does
not itself enforce that semantic match.

**Required correction:** compare every Jacobian and free-direction object with
a complete canonical descriptor, or derive its name from its descriptor and
reject mismatches.  Compute both saturated-margin derivatives from the full
free-plus-pivot direction rather than from separate hard-coded formulas.  Add
a permutation mutation test.  The same principle should be applied to the
ordered reticulation choices and singleton-source root-suppression edges.

### 2. The introduction over-attributes full identifiability

**Severity:** minor scholarly correction required.

**Location:** manuscript p. 2, TeX line 29.

The sentence says that algebraic work “has established generic and, under
additional hypotheses, full identifiability results for level-one models” and
cites only Gross--Long (2018) and Gross et al. (2021).  The former establishes a
generic JC large-cycle result, while the latter establishes generic
identifiability for the stated triangle-free level-one class under JC/K2P/K3P.
Neither is the full pointwise theorem described by that sentence.  The full
restricted-parameter-space level-one result is instead the Brits et al. v3
theorem already cited in the preceding paragraph.

**Required correction:** either change the sentence to “has established
generic identifiability results for level-one models,” or split it into a
generic claim cited to the 2018/2021 papers and a full claim cited to the
appropriate theorem in Brits et al. v3.

### 3. Certificate coverage and packet integrity are described too globally

**Severity:** minor reproducibility correction required.

**Locations:** manuscript p. 18, TeX lines 601--611; JSON certificates;
`RUN_REFEREE_REPLAY.sh`; `PACKET_PROVENANCE.txt`.

The computational core is strong, but not every certificate field is derived
or consumed.  Examples include several simple-K2P semi-directed fields, stored
row/column prose, a hard-coded printed K2P collision-locus dimension `17`, and
various K3P semantic/prose fields.  The compact-certificate generator emits
some determinant/topology/family metadata as literals.  The K3P sidecars are
required to equal embedded sections, which is a useful transport check but not
an independent oracle.  Golden transcripts likewise show deterministic replay,
not independent correctness.

The manifest robustly detects altered paths and bytes within the packet, but
because the manifest is not externally signed or pinned, code, data,
transcripts, provenance, and manifest could be changed together.  Thus
“self-consistent with the listed hashes” is established; “immutable” or
“authenticated” is not established by the packet alone.

**Required correction:** identify certificate fields as either verified or
informational, bind all fields used to support a paper claim, and narrow the
word “immutable” to an integrity/self-consistency claim unless the archive is
pinned by an external signed release or DOI.  A closed schema and field-coverage
test would be a valuable, but not theorem-critical, strengthening.

### 4. The shipped K3P path lacks an ordinary-state pruning implementation

**Severity:** minor wording or software correction required.

**Locations:** abstract p. 1; reproducibility discussion pp. 17--18;
`materials/src/verify_k3p.py:771-955`.

The K2P scripts genuinely compare descendant-set Fourier calculations with a
separate ordinary-state Markov-pruning algorithm, including every pattern.  The
K3P script reconstructs all graph Fourier monomials and then applies inverse
Fourier transform, but it does not include a separate ordinary-state pruning
path.  The claim that the package contains independent Fourier and pruning
checks is true in aggregate, but can be read as applying to every K3P claim.

I filled this evidentiary gap for the review: the clean-room program constructs
the four literal retained-edge K3P graphs, converts each edge vector directly
to a transition kernel, prunes all 64 patterns, mixes the four switchings, and
matches both the comparison tree and the Fourier inversion exactly.  Hence the
K3P collision itself is independently established.

**Required correction:** either add this direct K3P pruning path to the shipped
verifier or state precisely that the built-in direct-pruning cross-checks are
K2P checks.  Do not describe embedded/sidecar equality as an independent
calculation.

### 5. Two source/presentation statements should be made literal

**Severity:** minor clarification.

First, the packet says broadly that Version 3 “removes those K2P statements.”
The formal K2P lemma and K2P part of the global corollary are indeed removed,
and v3 explicitly explains the leaf-permutation obstruction and lists the
high-level K2P/K3P extension as open.  However, v3 retains a stale sentence on
its p. 11 saying that JC and K2P are generalized later.  Prefer: “Version 3
removes the formal arbitrary-level K2P lemma and the K2P part of the global
corollary.”  This is a source-version precision issue, not a flaw in the new
theorem.

Second, `technical-summary-clarified.pdf` p. 1 again uses the compressed arc
notation `u -> p,q; p,q -> r_2; p,q -> r_3`, even though the separate
clarification note exists to eliminate that ambiguity.  Expand the ten arcs or
say explicitly that each of `p,q` has an arc to each reticulation.  The main
paper's equation (2), graph, edge table, and calculations are mutually
consistent.

### 6. Optional presentation and hardening improvements

**Severity:** optional.

Figure 1 is complete and readable, but two labels are close enough to merit a
small spacing adjustment.  The PDFs are untagged, which does not affect print
meaning but limits screen-reader navigation.  Further useful software
hardening would include a declarative closed JSON schema, all-coordinate
symbolic source-convention comparison, property tests for attachment-side
grafting, a pinned execution environment, and an external signed manifest
digest.  None is needed to repair a mathematical conclusion found false in
this review.

## Mathematical claim audit

| Claim or result | Status | Independent basis | Limitations or issue |
|---|---|---|---|
| Definitions, theta topology, and parameter counts | **verified** | Suppressing the degree-two root produces the three internally disjoint paths `p-u-q`, `p-r2-q`, and `p-r3-q`; the sole maximal blob has two reticulations and three leaf-side incidences.  The nine effective edges plus two inheritance weights give dimensions 20 and 29. | A literal “2-sub-blob” definition in the source has an incidence ambiguity, discussed below; it does not change the maximal theta 3-blob or the formal v2 lemma's scope. |
| Displayed-tree parameterization | **verified** | Derived from the ten rooted arcs.  The four retained-parent choices give `S_y S_z U_{y+z}`, `S_y T_z U_y V_z`, `T_y S_z U_z V_y`, and `T_y T_z V_{y+z}`; dangling unlabeled branches contribute the identity and degree-two suppression multiplies Fourier eigenvalues. | Requires the stated uniform-root, symmetric group-based convention, which the paper makes explicit. |
| Exact strict-interior K2P collision | **verified** | Recomputed all 16 identities `M[y,z]=P[y+z]R[y]R[z]`, all 64 Fourier coordinates, all 64 inverse probabilities, exact normalization and minimum `1188799/79626240`; direct retained-graph and star pruning agree. | None affecting the claim. |
| K3P non-disjointness by inclusion | **verified** | K2P is the equality submodel `(1,s,g,s)` of K3P; the root law, inheritance mixture, and likelihood map are unchanged. | This inclusion does not itself give a parameter-level genuinely K3P witness, a distinction the paper observes. |
| Exact K3P parameter-level symmetry breaking | **verified** | Recomputed the quartic factorization modulo `5h^4-1`.  The `U` entries satisfy `h/3 < 1/3 < h`, excluding every global pair-equality parameter stratum, while the tree has `alpha=(1,a,a,t)` and `beta=gamma=(1,t,t,t)` and is non-JC because `a != t`. | The shared output is deliberately relabelled-K2P; “genuine” here initially refers to the network parameter, not the output. |
| Edgewise continuous-time K2P result | **verified** | The exact degree-six field arithmetic, root isolation, all edge kernels, all `g-s^2` margins, all 64 coordinates, and independent direct pruning were checked. | Edgewise heterogeneous generators/times only; no common generator or clock is claimed. |
| K2P rank, local locus, and 11-dimensional fibers | **verified** | Independently differentiated the stated map and recovered the displayed nonzero rank-9 determinant.  The tree recovery formulas give rank 6; the submersion/preimage calculation gives `20-9+6=17` and fixed-output dimension `20-9=11`. | The shipped verifier prints rather than derives one dimension, but the paper's deduction is correct. |
| K3P rank, local locus, and 14-dimensional fibers | **verified** | Independently reconstructed the stated 15-by-15 minor and determinant.  Tree recovery gives rank 9; dimensions are `29-15+9=23` and `29-15=14`. | The verifier semantic-binding issue is Finding 1; current semantics were checked separately. |
| Nearby observably genuine K3P collisions | **verified conditional on stated assumptions** | The restricted collision map is a submersion, so it has a local section after shrinking.  Pairwise distinct `U` entries and the rank minor persist on an open parameter neighborhood.  The union of three relabelled-K2P fixed loci is closed and lower-dimensional in the recovered positive tree germ. | “Observably genuine” means outside the paper's explicitly defined union of three global character-relabeling fixed subspaces; it does not exclude arbitrary internal gauges or edge-dependent relabeling notions. |
| Edgewise continuous-time K3P branch | **verified conditional on stated assumptions** | `J_*` is invertible; the exact tangent solves the fixed-output equation.  The two saturated margins have derivatives `(21-20h^2)/19>0` and `1`; all other inequalities, rank, and `U` distinctness persist by openness. | Analytic/existential IFT conclusion, with no explicit radius or closed-form nearby point.  It is only the paper's edgewise heterogeneous CT notion. |
| Dominance and Zariski-density corollary | **verified** | A nonzero full ambient Jacobian minor makes each complexified polynomial map dominant.  A real full-rank point inside each open stochastic/CT chamber gives an ordinary open image, which is Zariski dense. | Applies only after normalization and removal of forced inconsistent coordinates and K2P global symmetry.  It says nothing about inequalities, simplex filling, or tree invariants. |
| One-blob arbitrary-taxon grafting theorem | **verified conditional on stated assumptions** | Equality is preserved by tensoring the common three-interface law with the same three conditional Markov kernels.  Root splitting uses positive coordinatewise square roots; strict CT inequalities are stable.  Injectivity of each attached JC subtree map follows by marginalizing to one leaf and obtaining an invertible path kernel, so observable K3P asymmetry cannot disappear. | Exactly one theta replacement; not a multi-blob composability theorem and not a genuine four-attachment-blob result. |
| Scope and relationship to prior literature | **verified conditional on stated assumptions** | The formal v2 K2P lemma/corollary, their removal in v3, the v3 obstruction/open question, and the cited generic/dimension/3-sunlet results were checked against primary sources.  Targeted searches found no prior exact tree--theta Kimura collision. | Global novelty priority cannot be proved by a bounded search; the line-29 attribution and v3 wording need Finding 2/5 corrections. |

### Supporting derivations

#### Topology and the source's 2-sub-blob terminology

After root suppression, the cyclic core is the union of the three internally
disjoint `p`--`q` paths through `u`, `r_2`, and `r_3`.  It is one maximal
biconnected component with exactly two reticulations, so its level is exactly
two; the three incident cut edges lead to leaves 1, 2, and 3.  The fixed
reticulation directions also force both `p` and `q` to have only reticulation
children in every compatible binary rooting, so no tree-child rooting exists.

Under a literal reading of the cited source's three-clause “2-sub-blob”
definition, each of six two-vertex single-edge subsets qualifies even though
it has four crossing incidences and is not suppressible as an ordinary
degree-two object.  This is a genuine terminology tension in the source.  It
does not rescue the withdrawn v2 result: the formal v2 K2P lemma is stated for
every trinet with a nontrivial 3-blob and contains no no-2-sub-blob hypothesis.
The theta's unique maximal nontrivial 3-blob is unambiguous, and the manuscript
appropriately says its collision theorem needs no additional exclusion.

#### Displayed-tree formula and exact equality

For a consistent label, `x=y+z`.  The four `K` edges have descendant sets
`{1}`, `{2,3}`, `{2}`, `{3}`, hence contribute

\[
K_x K_{y+z}K_yK_z=K_x^2K_yK_z.
\]

At `(r_2,r_3)=(p,p),(p,q),(q,p),(q,q)`, the descendant sets below `u->p`
and `u->q` are respectively `({2,3},emptyset)`, `({2},{3})`,
`({3},{2})`, and `(emptyset,{2,3})`.  This yields exactly the four core
monomials in equation (3), each with weight `1/4`.  A retained edge with no
sampled descendant has character `A` and factor one, which is the Fourier form
of pruning the dangling branch.  Suppressing a degree-two vertex composes two
symmetric group-based kernels and therefore multiplies their edge eigenvalues;
it cannot introduce an omitted factor.

For the compact K2P point, direct substitution gives, among all sixteen checks,
`M[A,C]=151/1440=P_C R_C` and
`M[C,C]=71/1600=R_C^2`.  The full identity gives

\[
q^{N}_{xyz}=K_x^2K_yK_zM_{y,z}
=(K_x^2P_x)(K_yR_y)(K_zR_z)=q^T_{xyz}.
\]

The remaining 48 coordinates vanish on both sides by group consistency.  The
Fourier transform is invertible, so ordinary distributions agree.  Direct
state-space pruning, separately implemented, confirms the same equality rather
than relying only on inversion.

#### Continuous-time criteria

Solving the K3P exponential parameterization gives, for example,

\[
\lambda_Ct={1\over4}\log {a_C\over a_Ga_T}.
\]

Thus all three substitution-rate classes are positive exactly when the three
cyclic inequalities in equation (5) hold.  Under K2P,
`a_C=a_T=s, a_G=g`, two inequalities reduce to `s>sg`, already true for
`0<g<1`, and the remaining one is `g>s^2`.  Coordinatewise edge composition
multiplies these strict inequalities, so suppression and half-time root
splitting behave as claimed.

At the closed quartic K3P point, exactly two margins are zero.  The IFT changes
`U_C` and `V_G` freely while solving for the 15 pivots.  The independently
reconstructed tangent gives

\[
{d\over d\varepsilon}(U_C-U_GU_T)|_0={21-20h^2\over19}>0,
\qquad
{d\over d\varepsilon}(V_G-V_CV_T)|_0=1.
\]

Because the remaining rate margins, transition entries, inheritance
probabilities, rank determinant, and `U` pairwise differences are strict at
the base point (or remain nonzero there), they persist for sufficiently small
positive `epsilon`.

#### Rank, local geometry, and algebraic scope

There are ten K2P orbits among the 16 consistent coordinates; normalization
leaves ambient dimension 9.  K3P has 16 consistent coordinates and normalization
leaves 15.  Applying the positive tree recovery formulas separately to two
K2P characters or all three K3P characters gives tree dimensions 6 and 9.
The rank minors therefore make the network maps submersions at the witnesses.
For a submersion `F:P^d -> A^m` and an embedded tree germ of dimension `t`,
the transverse preimage has dimension `d-m+t`, and the restricted map has
fiber dimension `d-m`.  Substitution yields `(17,11)` and `(23,14)` exactly.

The same nonzero minors are polynomial certificates of generic rank over the
complexification.  Dominance is therefore justified in the effective affine
spaces; the paper correctly keeps normalization, forced zeros, K2P symmetry,
and stochastic/CT inequalities outside the “no additional equality invariant”
claim.

#### Arbitrary-taxon grafting

If `p=p'` on the three interface states, applying the same product kernel
`K_1 tensor K_2 tensor K_3` gives equal full-leaf distributions by linearity.
This proves every taxon count at once; it does not require enumerating `4^n`
patterns.  For the observable-genuine K3P statement, each attached JC subtree
map has column rank four because its marginal to any chosen descendant leaf is
the invertible product of positive-eigenvalue JC matrices along that path.
The tensor product is injective and equivariant under every global nonidentity-
character transposition.  Hence a symmetry of the full output would imply the
same symmetry of the three-interface law, a contradiction.  The topology
argument inserts one binary theta blob, and contracting it recovers the chosen
tree vertex.

## Code and certificate audit

### Claim-to-code map

| File or entry point | Mathematical claim tested | Method | Independence or blind spot |
|---|---|---|---|
| `materials/verify_k2p_simple.py` | Compact K2P field, admissibility, factorization, patterns, minimum | Exact `Q(sqrt(71))` arithmetic and inverse Fourier transform | Topology/schema coverage is weaker than the graph verifier. |
| `materials/verify_k2p_displayed_trees.py` | Rooted graph, four monomials, all K2P coordinates and probabilities | Declarative retained-edge reconstruction plus direct Markov pruning | Shares primitive vectors and group conventions; focused entry point alone does not assert every positivity condition. |
| `materials/src/verify_k2p_extended.py` | Exact edgewise-CT K2P collision and invariant/order audit | Degree-six number field, Sturm isolation, exact interval signs, Fourier and direct pruning | Strong; imported by later K2P scripts, creating shared infrastructure. |
| `materials/src/verify_k2p_rank_family.py` | Rank-9/rank-6 minors, fiber count, symmetric family | Dual-number differentiation and exact elimination | Some metadata is hard-coded/unused; dimension `17` is printed rather than asserted; family equivalence relies on the manuscript recovery proof. |
| `materials/src/verify_k2p_four_leaf_graft.py` | One four-leaf graft instance | Literal graph/topology audit and all 256 Fourier/state probabilities | A regression only; it correctly does not prove arbitrary `n`. |
| `materials/src/verify_k3p.py` | Quartic field/topology, K3P collision, rank 15, tangent, CT margins | Exact quartic arithmetic, graph Fourier, Bareiss elimination, IFT tangent identity | No direct state-pruning path; descriptor/name and list-order gaps in Finding 1. |
| `materials/src/verify_source_conventions.py` | Five source 3-sunlet coordinates and invariant sign convention | Exact evaluation at a rational assignment | Locally transcribed expectations, five coordinates only, not a source-bound symbolic oracle. |
| `materials/src/generate_k2p_simple_certificate.py` | Compact JSON regeneration | Recomputes core/coordinate/pattern arrays | Emits important topology/rank/family metadata as literals. |
| `materials/verify.py` | Complete suite orchestration | Invokes all substantive Python entry points | Propagates child failures correctly; not an independent mathematical check. |
| `RUN_REFEREE_REPLAY.sh` | Integrity, normal/optimized outputs, focused outputs, regeneration, PDF text | Strict path manifest, deterministic environment controls, transcript comparison | Self-consistency rather than authentication; depends on unpinned tools on `PATH`; executing hashed code is not sandboxing. |
| `materials/src/build_pdfs.sh` | Three document builds | Tectonic or latexmk, then extracted-text comparison | Extracted text cannot detect purely visual changes; separate visual QA was performed. |
| Five JSON certificates/sidecars | Primitive values, arrays, determinants, tangent data | Broad recomputation plus embedded/sidecar equality | Numerical coverage is extensive; semantic/prose field coverage is incomplete, and sidecars are not independent. |

### Exactness and coverage

No equality or sign decision essential to a theorem uses floating-point
arithmetic.  Decimal conversions are display-only.  The `Q(sqrt(71))` check
uses a rational isolating interval.  The continuous-time K2P primitive has an
irreducible cubic certified modulo 37 with a Sturm-isolated real root and an
independent `sqrt(1423)` factor; the six displayed basis monomials are valid by
the tower law.  The K3P field uses the unique positive root of `5h^4-1`, with
irreducibility from Eisenstein applied to the reciprocal polynomial.  Exact
natural interval arithmetic establishes all strict signs in the packet.

All 64 Fourier coordinates and all 64 probabilities are checked for both
three-leaf constructions.  For K2P, the packet itself also directly prunes the
literal retained graphs.  For K3P, my clean-room check supplies that missing
independent algorithm.  Every explicit edge transition row and continuous-time
margin attributed to the witnesses was reconstructed.  The determinants are
computed from differentiated formulae and eliminated exactly; they are not
accepted merely because a stored scalar is nonzero.

The strongest common-mode risks are shared field/group infrastructure,
hard-coded expected transcripts, literal generator fields, and embedded
sidecars.  These limit what “independent replay” means but do not survive the
separate clean-room reconstruction used for this review.  Unused or prose-only
JSON fields should not be represented as machine-certified until they acquire
explicit consumers.

## Execution record

All mutations were performed in disposable copies under `packet_mutations/`.
The authenticated `packet_copy/` was not altered.

| Command actually used | Exit status | Compared artifact | Result or divergence |
|---|---:|---|---|
| `bash ./RUN_REFEREE_REPLAY.sh --with-pdf` | 0 | Complete normal/optimized transcripts; focused transcripts; regenerated compact certificate; three PDF text extracts; pre/post hashes | All comparisons matched; all support entry points passed; final integrity check passed. |
| `tmp/sympy_env/bin/python notes/clean_room_symbolic_checks.py` | 0 | Independent manuscript-derived K2P/K3P equations | Both factorizations, direct pruning, all coordinates, selected determinants, and K3P tangent matched exactly. |
| `python3 materials/verify_k2p_simple.py` in NC-1 copy | 1 | Mutated collision datum | Failed at the first broken factorization entry after admissibility checks passed. |
| `python3 materials/verify_k2p_displayed_trees.py` in NC-2 copy | 1 | Mutated rooted arc assignment | Failed at the graph-derived monomial for switching `(p,p)`. |
| `python3 materials/src/verify_k2p_rank_family.py` in NC-3 copy | 1 | Mutated stored determinant | Exact recomputation rejected the determinant. |
| `python3 materials/src/verify_k3p.py` in NC-4 copy | 1 | Mutated tangent in embedded and sidecar data | Passed collision/rank checks, then failed the intended fixed-output residual at row 1. |
| `python3 materials/src/verify_k3p.py` in NC-5 copy | 0 | Even cycle of first three executable Jacobian characters, stored columns, and pivot values while names stayed fixed | All K3P checks passed despite false name-to-derivative bindings, confirming Finding 1. |

The replay used Tectonic because `latexmk`/`xelatex` were unavailable.  Tectonic
rebuilt all three PDFs; `pdftotext -layout` output matched the supplied PDFs.
The complete normal and `-O` runs agreed with the stored complete output, and
the optimized four-leaf run agreed with its normal counterpart.  No
optimization-sensitive `assert` gap was found in the substantive checks.

## Negative controls

| Mutation | Expected failure | Observed failure | Interpretation |
|---|---|---|---|
| Replace compact K2P `U=(1,4/5,19/30,4/5)` by `(1,79/100,46/75,79/100)`, preserving K2P symmetry and strict stochasticity | Core collision factorization | `factor (0, 1)` after field/topology/edge/root checks passed | The collision is recomputed rather than inferred from admissibility or a PASS string. |
| Reassign literal graph arc `p->r2` from `S` to `T` | Displayed-tree monomial | `wrong graph-derived monomial for switch ('p','p')` | The graph verifier uses arc placement and descendant sets substantively. |
| Change stored rank determinant numerator by one | Rank certificate equality | `simple determinant` | The determinant is independently differentiated/eliminated and compared exactly. |
| Change pivot derivative `e_u_p.a_G` from `-6/19+60h^2/19` to `13/19+60h^2/19` in both embedded and sidecar certificates | Fixed-output tangent | Residual `Alg(0,0,0,1/128)` at row 1 | Sidecar equality still passed; the mathematical tangent equation caused rejection. |
| Keep the first three Jacobian names fixed but apply the coordinated even semantic/column/pivot cycle `C,G,T -> G,T,C` | Should fail a name/descriptor binding check | Survived; exit 0 and `ALL K3P CHECKS PASSED` | The current verifier certifies the executed permuted matrix, not the advertised human-readable parameter labeling. |

The first four are substantive failures from direct verifier invocation, not
checksum failures.  The fifth is an important *surviving* mutation: it
demonstrates directly that passing replay must not be interpreted as certifying
the truth of every human-readable JSON label.

## PDF and presentation audit

I rendered and visually inspected all 23 supplied pages at high detail.  The
19-page manuscript has no missing page or figure, clipped content, missing
glyph, black box, broken display, table overflow, unreadable reference, or
unresolved cross-reference marker.  Figure 1 is dense but complete; the pivot
table on p. 13 is small but readable.  The repository URL on p. 18 wraps within
the text block, and the bibliography is intact.

Both two-page support PDFs also render completely.  The technical summary is
dense but legible; its compressed arc wording is the semantic issue in Finding
5, not a rendering failure.  The displayed-tree clarification has intact
tables, equations, radical expressions, and boxed equality.  All PDFs are US
Letter, unencrypted, and use embedded fonts.  They are not tagged for semantic
accessibility.

The rebuild comparison is text-level rather than byte/visual reproducibility:
Poppler extraction matched, but this would not detect a font, diagram-geometry,
color, or clipping-only change.  The separate page-by-page visual inspection
supplies the missing check for the delivered artifacts.

## Required corrections

Before publication, I recommend the following bounded changes:

1. Bind every K3P Jacobian/free-direction name to a canonical complete semantic
   descriptor and derive the two CT-margin derivatives from the executed total
   direction.  Add a permutation mutation test; bind reticulation order and
   singleton source-edge mappings as well.
2. Correct the p. 2 literature sentence so the 2018/2021 citations support only
   generic identifiability, with any full result attributed to the correct
   Brits et al. theorem.
3. State which certificate fields are machine-verified and which are
   informational; avoid presenting embedded/sidecar equality or golden
   transcript equality as independent evidence.
4. Add direct K3P ordinary-state pruning, or narrow the prose so direct pruning
   is accurately attributed to the K2P implementations.
5. Replace the broad v3-removal wording by the literal formal-result statement,
   expand the technical summary's ten arcs, and replace “immutable” by an
   accurate integrity/self-consistency statement unless an externally pinned
   release is supplied.

Spacing in Figure 1, PDF tagging, a closed JSON schema, a signed release digest,
and broader property-based graft tests are worthwhile optional improvements.

## Unreviewed items, limitations, and confidence

- I did not attempt an exhaustive worldwide or unpublished-priority search;
  the novelty conclusion is bounded to the cited primary literature and
  targeted searches current on the review date.
- I did not formalize the analytic and differential-topological arguments in a
  proof assistant.  I checked their hypotheses and deductions directly and
  found them standard and correctly applied.
- The K3P strict-CT branch has no explicit certified radius or nearby algebraic
  parameter.  This is not needed for the stated existential IFT corollary, but
  it limits numerical reuse of that branch.
- The all-taxon theorem was checked as a universal kernel argument plus a
  four-leaf regression, not by finite enumeration at arbitrary `n`.
- Packet execution used the host Python/TeX/Poppler binaries rather than a
  hermetic container.  Exact mathematical outputs and extracted PDF text were
  deterministic in the recorded environment.
- Confidence in the central mathematics is **high**.  Confidence in the
  numerical/algebraic content actually consumed by the verifiers is **high**.
  Confidence that every prose-like JSON field is certified is **low**, which is
  why Findings 1 and 3 require correction.

## Final recommendation

MINOR REVISION — The central collision, local-geometry, continuous-time, dominance, and one-blob grafting results withstand independent proof and computational checks; the remaining defects are localized certificate-semantic, attribution, and reproducibility-wording issues that should be corrected before publication.
