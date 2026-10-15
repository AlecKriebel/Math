# Group 5 paper metadata review

Checkpoint: 2026-10-10 21:08:58 UTC (14:08:58 America/Los_Angeles). Content-review and patch-preparation completion: 100% (15/15 records); live publication completion: 0%. No Zenodo mutations, versions, DOI reservations, outreach, or Git commits were performed by this reviewer.

## Review boundary and changes

Reviewed the exact checksum-bound deposited PDF texts listed in `group_5_records.json`: 15 paper records and 23 main/supplement PDFs. Reading covered abstracts, introductions, model definitions and main theorem statements, relevant proof mechanisms and theorem dependencies, scoped limitations, and supplementary proof/certificate interfaces. This is a content-faithfulness and discovery review, not a fresh verification of every theorem, exact certificate or source program.

Prepared one `{"metadata": {...}}` patch per record in `../patches/ID.json`. Every title is preserved. Thirteen descriptions are left byte-for-byte alone; the other two receive only a trailing typo correction or removal of redundant HTML wrappers. All useful existing keywords are retained, with one malformed bullet prefix repaired. Final keyword counts are 14–17. Eleven papers missing language receive `eng`, based on the English deposited manuscript. Existing dates, DOI, generated fields, version, license, access and custom fields are never patched. All deposits remain preprints.

Author improvements: correct the visibly reversed `Alec, Kriebel` name on 22770864, preserving affiliation and ORCID; add Alec's supplied ORCID on 21699161, preserving existing name and null affiliation. Two evidenced related identifiers are added, preserving all existing entries.

Compatibility flags: 21699161 has nonempty `custom` codeRepository metadata, so the audited legacy tool conservatively refuses it; use the native editor and preserve that custom field. 22013710 has an existing `dates` entry of type submitted; inspect its native representation and preserve it rather than clearing it if the legacy guard refuses. The patch files do not attempt to remove either field.

## Record-specific evidence and rationale

### 22929486 — Kourovka Problem 16.45 counterexample

Evidence: `Kourovka_16_45_Counterexample_v1.0.1.txt`, abstract/§1 lines 11–59, subgroup conventions lines 61–125, Propositions 8–10 lines 271–317, Theorem 11 lines 340–348, verification boundary lines 386–416. The object is the explicit affine group of order 100920, with SL2(5) complement and `b_f=b=3<4=mu'`; arbitrary/nonfaithful permutation actions matter. The normal-bottom obstruction separates independent sets from minimal permutation bases. Characteristic 11 is an explicit boundary control; no minimum-order or guaranteed-priority claim is made.

Patch: 14 keywords and `eng`. Added group theory, affine groups, minimal bases, irredundant generating sets, SL(2,5), Boolean meet-semilattices to existing problem/base/subgroup terms. The description already explains the distinctions, computational scope, provenance and priority limits well; retain it verbatim. Existing Cameron DOI and software/documentation links remain.

### 22770864 — odd-order p-group with equal automorphism count

Evidence: `kourovka_16_63_v1.1.0.txt`, title page lines 1–37 and §1 lines 77–114, integral Lie-ring construction lines 154–195, full automorphism classification Proposition 3.2, rigid flag Proposition 4.1, logarithm/exponential full-set bijection Proposition 6.3 lines 464–471, Smith data lines 494–527, BCH conclusion lines 565–571 and verification limits lines 623–630. The paper gives one example at p=1009 with order and **full** automorphism-group order `1009^52359`. It does not merely count a p-Sylow automorphism subgroup, does not enumerate the whole group, and does not assert every odd prime or minimality.

Patch: 14 keywords, `eng`, corrected creator name `Kriebel, Alec`, and one `cites` DOI. Added odd-order groups, nilpotent groups, Lie rings, Lie algebra derivations and p-adic Lie theory. The first-page author and repeated headers unambiguously establish that the existing `Alec, Kriebel` surname/given-name serialization is reversed. The manuscript attributes its Lie-algebra template to Omirov–Ruan Theorem 4.8 (reference [4], lines 671–672); the [official arXiv record](https://arxiv.org/abs/2605.04602) confirms title, authors and canonical DOI `10.48550/arXiv.2605.04602`. Add this as `cites`, publication-preprint, doi; preserve both existing links. Description unchanged, including attribution and AI disclosures.

### 22729545 — raw strongly tree-child level-2 NMSC classification

Evidence: `NMSC_Paper_B_Main.txt`, abstract lines 11–36, Theorem 1.1/eight moves lines 70–105, sequence corollary and direction/exposure results lines 107–130, model lines 158–181, numerical fiber statements lines 962–984 and comparison lines 987–1020. `NMSC_Paper_B_Supplement.txt` supplies positive-cell/sampling consistency arguments (§§1–2), observable current-grouping formulas (§3), shortcut completion (§4), detailed two/three-lineage inversion (§5), exact hidden-clock/route-projector obstructions (§6), five-core/twelve-repair graph proof (§7) and evidence boundary (§9).

This is a **pointwise**, strict temporally separated rooted-network quotient with a fixed known surjective sampling map and independent-lineage routing. At most three lineages means the **indexed collection of all pair/triple marginals** of the same sampling design, not one triple. Unexposed unary fans retain typed outlet weights but lose internal clock/rate words. Sister direction is invisible only in the bi-unary situation; physical scaling and other quotient fibers remain.

Patch: 15 keywords only. Added rooted phylogenetic networks, Kingman coalescent, reticulation, sampling consistency, inheritance probabilities, coalescent theory and observational equivalence. Language/ORCID already complete. Keep the detailed description and existing companion-paper `cites` link verbatim.

### 22729537 — direct sequence laws and canonical response

Evidence: `NMSC_Paper_A_Main.txt`, abstract lines 12–45, contributions/limits lines 80–93, model lines 98–180, Theorems 3.2–3.4, moment/determinant/shared-generator theorems §§4–7, canonical residual realization Theorems 8.4 and 8.9, qualified graph content §11, finite-locus Theorems 12.2/12.4, statistical consequences §13 and discussion lines 1795–1831. `NMSC_Paper_A_Supplement.txt` expands typed Hankel/minimality and finite-jet criteria, confluence/Frisch–Siu finite determination, Vandermonde collision proof (§11), qualified gluing (§12), consistency (§13), and exact-input/positive-realization caveats lines 1403–1413.

The principal observation is the indexed ordered nonrecombining-locus laws with known boundaries and one shared irreducible stationary reversible generator. CCR is a canonical finite typed **behavior**, not a canonical biological graph. Finite determining length exists on a fixed compact semianalytic finite-presentation class; unbounded epoch count defeats taxon/reticulation-only uniform bounds even for two-taxon known JC. The level-1 graph theorem has incidence-separation and scalar-faithfulness qualifications; no unconditional level-2 graph theorem is imported.

Patch: 16 keywords only. Added multilocus sequence alignments, Kingman coalescent, reversible substitution models, moment determinacy, statistical identifiability, demographic identifiability, minimal realization and coalescent theory. Description remains unchanged and preserves all these qualifications; existing companion `cites` link remains.

### 22729355 — exact synthetic Turing diffusion design

Evidence: `Exact_Diffusion_Design_Preprint_v1.0.11.txt`, abstract/intro/scope lines 13–97, binary-complex network and complete realization family lines 100–200, Theorems 3.2, 4.1, 5.2–5.3, 6.1 and 7.1, discussion lines 1062–1084. `Exact_Diffusion_Design_Supplement_v1.0.11.txt`, §§S1–S4 gives flux cone, semipositive conservation, exhaustive block cases and principal-minor ray proof; §§S5–S8 give profiles/cubic certificates; §§S10–S11 separate local semilinear stability, robustness and numerical/exact evidence.

For each n>=4 the positive-equilibrium topology has no unstable principal subsystem below n−1 and an unstable n−1 block. The exact inequality is for **stationary** diffusion-ray crossing in a homogeneously stable realization; it does not classify arbitrary wave instability. Positive patterns are locally stable in a fixed integrated-mass class for each fixed dimension. The semipositive conserved functional omits X1, so this is not a global mass-conservation theorem or a natural biochemical mechanism.

Patch: 16 keywords and `eng`. Add diffusion-driven instability, principal subsystems, center-manifold reduction, chemical kinetics, Neumann boundary conditions and reaction network theory. Retain original synthetic/local limitation prose and exact software supplement DOI.

### 22395326 — symmetry-stratified JC/K2P/K3P synthesis

Evidence: `Symmetry-Stratified_Level2_Identifiability.txt`, abstract lines 13–47, same known-model theorem/conventions lines 102–149, Theorems 3.1/3.4, uniform triangle geometry theorem and cross-model §8, scope lines 1957–1993 and imported-input boundary lines 1996 onward. `Symmetry-Stratified_Level2_Identifiability_Supplement.txt`, §§1–3 domains/interface obligations, companion theorem/certificate crosswalk, exact orbit and triangle tangent calculations §§5–6, 144 three-leaf cross-model relations §7, expressly exploratory four-leaf triage §8.

Same-model containment/common regular germ yields the ordinary-triangle quotient only within the stated binary standard semi-directed strongly tree-child level-at-most-two class and strict principal/continuous-time domains. Generic exact complete-tensor reconstruction assumes the substitution model is known. It is neither full stochastic-image equality nor all-level-2/unknown-model recovery. The triangle rank/codimension formulas and cross-model restrictions are synthesis contributions; global JC/K2P/K3P proofs remain imported DOI-bound results.

Patch: 17 keywords only; add symmetry stratification, Fourier coordinates and site-pattern distributions. Existing keywords already include all models, genericity and triangle redirection; keep descriptions, model dependencies and related DOI list unchanged.

### 22178672 — K3P triangle hypersurfaces/classification

Evidence: `K3P_Level2_Identifiability_Article_v1.0.0.txt`, abstract lines 10–34, main Theorems 2.1–2.5 and qualifications lines 157–231, domain/transfer §4, H14 §5, bridge fiber §6, bounded/restoration/probe §§8–9. `K3P_Level2_Identifiability_Reader_Supplement_v1.0.0.txt`, dependency graph lines 16–57, domains lines 181–209, explicit eight-term H14 quartic and strict common point lines 236–263, later witness/certificate crosswalks.

The triangle orientations share a **relative** smooth rank-14 germ on an irreducible quartic in a 15-dimensional normalized ambient space, not an ambient-open 15-dimensional triangle germ. Noncut detection is generic; the paper does not assert universal pointwise K3P rank detection. Generic topology is modulo ordinary-triangle redirection, with strict domain and strong-class restrictions; weak-not-strong examples have full-dimensional continuous-time ambiguities.

Patch: 17 keywords and `eng`; add group-based models, Fourier coordinates, triangle redirection and quartic hypersurfaces. The existing description accurately preserves principal/strict domain, computational and archival distinctions; no changes to it or dependencies.

### 22168797 — K2P principal-domain classification

Evidence: `K2P_SAME_Principal_Domain_Article.txt`, abstract lines 14–36, physical/convention proof layers lines 49–125, exact bridge fiber Theorem 4.2, global Theorem 7.3 lines 941–956, exact reconstruction caveats lines 1073–1079, strict continuous-time transfer lines 1082–1096, weak-class Theorem 11.1. `K2P_SAME_Reader_Supplement.txt`, proof/certificate boundaries lines 78–118, conventions/domain lines 121–140, restoration/probe census and explicit weak-class witness lines 799 onward.

Principal domain is `0<s,g<1, g>2s−1`; strict continuous time is `s²<g<1`. The topology conclusion is generic modulo triangles and regular full-dimensional containment, with no complete-image equality or mixed-sign classification. Pointwise quartet signs and generic polynomial/rank exclusions have distinct quantifiers. The finite certificate residue remains load-bearing.

Patch: 17 keywords and `eng`; repair `- reproducible mathematics` to `reproducible mathematics`, add group-based models, Fourier coordinates, triangle redirection and strict continuous-time models. Description change is exactly the trailing `claimed.r` → `claimed.` typo; every other byte and all archived-version/provenance information are preserved.

### 22136869 — exact tree/theta collisions

Evidence: `Kriebel_2026_Exact_Tree_Theta_Trinet_Collisions_v1.2.7.txt`, abstract lines 10–31, comparison/scope lines 38–100, model lines 126–187, exact K2P Theorems 4/7, K3P parameter-versus-observable symmetry Theorem 12, rank/fiber Proposition 13 and Corollaries 14–16, one-vertex replacement Theorem 19, scope lines 972–996.

The theta topology admits **no tree-child rooting**, so these collisions do not refute strong-class generic classification. Exact tree equivalence is nongeneric on the dominant theta parameter map but robust over nearby tree outputs. The exact quartic K3P witness has genuinely K3P parameters while its output is character-relabelled K2P; nearby outputs are genuinely K3P. Continuous-time embeddability is edgewise with no shared-Q or clock. One theta replacement at a chosen tree vertex is proved; multiple independent replacements are not claimed.

Patch: 15 keywords and `eng`; add theta networks, phylogenetic trinets, site-pattern distributions, Fourier coordinates, parameter fibers and exact counterexamples. Preserve source-version distinction and all description claims as written.

### 22089807 — simultaneous amplification beyond 3/2

Evidence: `simultaneous_amplification_beyond_three_halves.txt`, abstract lines 12–30, exact quantifier order lines 55–80, model/baselines lines 83–138, Theorem 3 lines 218–224, weak-cut/establishment/gain proof §§4–7 and discussion lines 1090–1113.

One fitness-independent connected loopless undirected weighted graph sequence amplifies both pure Bd and dB updating for every **fixed** fitness in `(1,R_hyb)` once sufficiently large; `R_hyb≈1.50285691279` is a lower bound on the unrestricted threshold. Its optimization is only within the displayed dilute pair-pendant response model. The global value and even a finite universal upper bound remain open; exact finite replays do not prove the analytic population asymptotics.

Patch: 17 keywords and `eng`; preserve all existing field/MSC terms, add selection amplification, weak-cut asymptotics and genetic drift. Existing supersession/source links remain unchanged; no claim that a metadata edit creates a new version is added.

### 22089748 — dB local optimality and fixed-graph rigidity

Evidence: `complete_graph_extremality_db.txt`, abstract lines 11–30, author summary/intro lines 37–137, Theorems 1/2 lines 224–277, Corollary 3, low-order Theorem 5, sector positivity Theorem 9, explicit global-gap lines 887–894, symmetric K4 theorem lines 1580–1586 and quantifier ledger Appendix C.

The complete row-normalized kernel is a strict nondegenerate **local** maximizer at fitness two against arbitrary directed/nonreversible perturbations, with dimension-dependent neighborhoods. Strong-selection rigidity excludes one fixed finite all-beneficial-fitness amplifier; it does not exclude fitness-dependent size thresholds of graph sequences. Complete graph global maximality at fitness two is open. Weighted triangle and two symmetric K4 results are restricted global slices.

Patch: 14 keywords and `eng`; add Moran process, directed weighted graphs, replacement kernels, ancestral duality, Markov chains, population genetics, stationary collision probabilities and Hessian sector decomposition. Retain precise existing abstract and source derivation DOI.

### 22089551 — one-linkage bimolecular stochastic recurrence

Evidence: `paper-v1.2.4.txt`, abstract lines 11–26, model lines 130–170, Theorem 2.1 lines 182–186, lifted-return Lemma 2.2 and stationarity Corollary 2.3, carried-target/log-factorial mechanism §§3–7 and scope lines 810–829. Read all of `supplementary-note-v1.2.4.txt`: labelled-channel distinctions, finite Foster set/positive-return balance, nonexplosion, absorbing singletons and exact regression scope.

Weak reversibility alone closes each reachable communicating class. Positive recurrence/nonexplosion and unique stationary law for each class need the finite **one-linkage bimolecular** hypotheses, positive rates, and separate absorbing-singleton treatment. Multiple linkage classes and molecularity above two remain open. The universal theorem is analytic; finite exact regression networks do not prove it.

Patch: 15 keywords and `eng`; add chemical reaction network theory, bimolecular reaction networks, single linkage class, stationary distributions, nonexplosion, Anderson-Kim conjecture and random-time Lyapunov drift. Existing description is already accurate and searchable. No new external links were inferred from project folder names.

### 22089373 — strong-class JC identifiability boundary

Evidence: `Strong_Tree_Childness_Sharp_Level2_JC.txt`, abstract lines 10–29, conventions and related-work distinctions lines 37–175, Theorem 1.1/Corollary 1.2/Theorem 1.3, bridge incidence quotient Theorem 5.1, local/certificate Theorems 6.1/6.3, Omega and pendant-transfer sharpness §9. `Strong_Tree_Childness_Sharp_Level2_JC_supplement.txt`, scope lines 12–26, theorem/proof map lines 29–66, fixed-convention checks and exact finite atlas §§3–4, later sharpness/evidence interfaces.

The open JC strong-class generic conclusion applies to binary LSA-rootable, already-simple, one-step reticulation-preserving semi-directed graphs. It identifies topology modulo ordinary triangles, not all numerical parameters or full stochastic images. Bridge factorization gives projective local tensors modulo incidence scaling, not physical bridge multipliers. Triangle-free weak-class pairs show the strong hypothesis matters independently of triangle ambiguity.

Patch: 15 keywords and `eng`; add generic identifiability, directed containment, semi-directed networks, group-based models, phylogenetic invariants, Fourier coordinates, triangle redirection and bridge tree reconstruction. Existing description and evidence-dataset DOI remain verbatim.

### 22013710 — exceptional unitary Hecke Yang–Baxter operator

Evidence: `exceptional-ybe-d4-v1.2.0.txt`, abstract lines 10–31, priority/concurrent-work note lines 74–80, Theorems 1.1–1.3, sparse Pauli construction §§2–4, all-strand faithful localization §5, dimension obstruction §6, exact quaternionic/local-unitary comparison §8, enhancement/HOMFLYPT/all-strand transfer §9, verification/provenance §10 and novelty limitations lines 1068–1078.

The paper supplies the explicit four-dimensional local/16×16 operator, faithful H_n(3,6) localization, minimum dimension, an exact **opposite-operator** local-unitary comparison and all-strand equivalence. Finite braid images/Clifford frame and polynomial-time link evaluation are transferred from Galindo–Rowell's known Family III results; no new all-n group classification, new HOMFLYPT evaluation theorem, or private discovery priority is claimed. Finite Clifford images are not universal braiding in the density sense.

Patch: 15 keywords; add Yang-Baxter equation, Pauli matrices, Clifford group, Jones-Wenzl representations, Markov trace, HOMFLYPT polynomial, Turaev enhancement, quaternionic algebras, link invariants and finite braid group images. Existing language/ORCID/attribution DOI remain. Description change removes eleven nested div wrappers plus empty trailing div/nbsp scaffolding, retaining the **single original paragraph verbatim**, including all concurrent-work attribution and mathematical qualifiers. This improves usable HTML without rewriting the scientific text.

### 21699161 — minimum Bell settings for qubit POVM/PVM separation

Evidence: `kriebel-2026-minimum-bell-setting-complexity-v1.1.0.txt`, abstract/main theorem lines 11–39, attribution and comparisons lines 42–96, fixed dimension/zero projectors/postprocessing conventions lines 145–175, exact witness Theorem 3.1 lines 258–268, binary-party and residual reductions Theorems 4.2/4.5, physical Lorentz completeness Theorem 6.1, two-input Theorem 9.3 and minimum-architecture Corollary 9.4 lines 1167–1186, limitations lines 1189–1219 and AI disclosure/verification later in the paper.

The central equality is between **shared-randomness convex hulls** at fixed local dimension at most two with arbitrary finite input-dependent output alphabets. It is not same-state simulation, raw-image equality or operator-level POVM simulability. The 3×2 witness has attained POVM lower/global PVM upper bounds, not exact optima. The manuscript explicitly credits Vértesi–Bene for the prior 3×2 existence example.

Patch: 16 specialist keywords, `eng`, supplied ORCID and one source-release `isSupplementedBy` URL. Keywords cover Bell nonlocality/inequalities, fixed-qubit POVMs/PVMs, shared randomness/convex behaviors, dimension constraints, setting complexity, Lorentz geometry and state discrimination. The [existing source release](https://github.com/AlecKriebel/Math/releases/tag/qubit-povm-pvm-minimum-settings-v1.1.0) was verified as a real tag/release and is already explicitly named in the original metadata; add the same exact URL with software resource type, preserving custom codeRepository. Description—including unreviewed status and generative-AI responsibility disclosure—unchanged.

## Verification for root review

Patch schema and keyword counts were checked locally. All patches contain exactly one nonempty metadata object, use only allowed metadata fields, preserve author fields other than the two identified improvements, and avoid every protected/non-discovery field. No array is replaced without carrying useful existing entries forward. Title and publication-type patches are absent. Only IDs 22168797 and 22013710 patch descriptions, with the minimal text-preserving differences described above. These are discovery proposals awaiting root cross-review; live API compatibility and complete native before/after preservation must still be checked by the publishing agent.
