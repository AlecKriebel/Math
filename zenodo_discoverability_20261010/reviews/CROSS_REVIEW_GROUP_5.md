# Independent adversarial content review: group 5

Result: **all 15 proposals pass the metadata-content review; no blocking error found.** No patch or remote metadata was changed by this reviewer. Completion estimate: 100% of assigned cross-review. Timestamp is recorded in `CROSS_REVIEW_GROUP_5_QA.json`.

The review independently compared all proposed fields with the current metadata and the exact deposited main-paper text: author/title lines, abstracts, principal theorem statements, definitions, and scope discussions. For the two NMSC papers, selected full main classification, finite-hierarchy, sampling and demographic-fiber statements were read; for the substitution-model papers, the strong/weak class definitions, regular-germ interpretation, principal-positive versus strict-continuous-time domains, and tree–theta exception were checked. The recurrence supplement was also read completely. This is an adversarial check of metadata fidelity, not a new proof audit of all analytic arguments or imported large certificates.

`CROSS_REVIEW_GROUP_5_QA.json` records independent exact checks that all protected fields are absent from the patches; existing related-identifier objects are preserved; English is added only where missing; keyword lists have no exact duplicates; and every source PDF MD5 matches the assigned deposited artifact. The two creator repairs and both description repairs are tested separately below.

## Checks applying to all records

The proposals preserve all manuscript titles, DOI/prereservation fields, versions, publication dates, access and license fields. No new technical or priority claims are introduced in prose. Thirteen descriptions are unchanged. New keywords describe actual objects, subject areas or methods; they do not certify novelty, external peer review, complete formal verification or practical finite-sample sufficiency. The three numerical MSC tags on the simultaneous-amplification record are already existing keywords and are printed verbatim in that deposited paper; they are not guessed additions.

## Record-by-record adversarial findings

### 22929486 — Kourovka Notebook Problem 16.45

Pass. The deposited paper's abstract and §1 distinguish `b_f`, `b`, and the maximum independent-subset invariant. The example has affine group `F_29² ⋊ H`, `H≅SL_2(5)`, order 100920, and `b_f=b=3<4=μ′`. §§1.1–1.2 explicitly cover nonfaithful/intransitive actions, normal-bottom constraints and Boolean meet-semilattice embeddings. Added affine-group, minimal-base, subgroup-lattice and Boolean-meet terms are directly supported. “Irredundant generating sets” is a standard nearby search term: an independent set is irredundant for the subgroup it generates; the unchanged description expressly says it need not generate the ambient group. No minimum-order or global-priority claim is introduced.

### 22770864 — Odd-order p-group with equal full automorphism order

Pass, including the creator correction. The deposited author line reads Alec Kriebel with ORCID `0009-0001-9320-500X`; changing `Alec, Kriebel` to `Kriebel, Alec` repairs a surname/given-name reversal. Exact comparison confirms affiliation and ORCID are untouched. Abstract and Theorem 1.1 give `p=1009`, `|G|=|Aut(G)|=1009^52359`; §1 limits this to one example and excludes prime/order minimality. The rank-31 Lie ring, Zp lattice, BCH/Lazard interface, derivation matrix and Smith valuations support the added nilpotent/Lie-ring/p-adic tags. The newly cited Omirov–Ruan arXiv DOI corresponds to §1's explicit Theorem 4.8 template attribution. The full automorphism group remains distinguished from a Sylow subgroup.

### 22729545 — Raw strongly tree-child level-2 NMSC graph/parameter quotient

Pass. Main Theorem 1.1 fixes a known surjective sampled-lineage map and a strict, temporally separated, rooted binary strongly tree-child class of level at most two. It asserts a pointwise equivalence of complete normalized metric-genealogy laws and an eight-move quotient. Main Theorem 7.3 states sufficiency of the **indexed collection of all** marginals on subsets of at most three sampled lineages, explicitly excluding one-fixed-triple recovery and minimality of three. Theorems 9.1–9.4 keep the exposure qualifications: unary population rates and clocks are invisible; inheritance remains attached to typed outlets; bi-unary sister direction is the exceptional reversal. Added Kingman, sampling-consistency, inheritance, rooted-network and observational-equivalence tags fit these exact results. The unchanged description retains all those qualifications and the companion-paper dependence of the direct-sequence corollary. No generic qualification is incorrectly substituted for the pointwise result, and no claim to all demographic parameters is added.

### 22729537 — Direct sequence laws under NMSC

Pass. Definition 3.1 and Theorem 3.2 require known nonrecombining locus boundaries, contemporaneous labelled sampling, independent loci/routing, strict positive rates/durations, and a shared irreducible stationary reversible finite-state generator. The observation is the complete indexed locus-law hierarchy, not estimated gene trees or one site distribution. Theorems 3.3 and 12.2 restrict finite determination to a fixed finite union of compact semianalytic finite-presentation charts, with no effective universal bound asserted. Theorem 12.4 gives exact arbitrary-order collisions when epoch count grows. Theorem 3.4 and §11 restrict literal graph recovery to the specified tree/one-reticulation/faithful level-1 subclasses; CCR is canonical behavior, not a canonical biological graph. Moment determinacy, minimal realization, demographic epochs, sequence identifiability and statistical consistency all occur in the actual theorem suite. The unchanged metadata retains resonances, unknown-nonreversible exclusion, and the graph/behavior distinction.

### 22729355 — Exact diffusion design and stable Turing patterns

Pass. The main abstract, theorem suite and §§1–2 say that the n-species construction is synthetic, binary-complex, and stoichiometric-codimension one with a **semipositive** conservation law omitting X1. The stationary law is specific to homogeneously stable realizations and positive diagonal diffusion rays; it is not a classification of arbitrary wave instability. Theorems 6.1/7.1 explicitly use Neumann conditions and conservation-compatible local nonlinear stability. Therefore the added principal-subsystem, diffusion-driven-instability, center-manifold, chemical-kinetics and Neumann tags are supported. The unchanged prose retains local/fixed-dimension stability and synthetic-network limits. “Systems biology” is a subject tag, not a claim that the synthetic design models a natural biochemical mechanism.

### 22395326 — Symmetry-stratified JC/K2P/K3P identifiability synthesis

Pass. Main abstract and central universality statement compare networks on the same labelled leaf set in the fixed one-step reticulation-preserving **strong** class. Each same-model theorem concerns source-relative regular full-dimensional physical containment, separately on principal positive and strict continuous-time domains; it does not claim equality of entire stochastic images. The known fixed substitution-model condition and triangle-redirection quotient remain explicit in metadata. The Fourier/rank/S3 calculations support symmetry-stratification and Fourier-coordinate additions. Imported JC/K2P/K3P global classifications remain version-bound dependencies, while new finite calculations are kept separate. No unknown-model, unrestricted level-2, level-3, numerical-parameter or finite-sample extension appears in the patch.

### 22178672 — K3P triangle hypersurfaces and strong-class boundary

Pass. Main abstract states rank 14 on the normalized 15-dimensional triangle Fourier chart, the shared irreducible eight-term quartic H14, and a common **relative** smooth strict-continuous-time germ. It explicitly says the triangle image is not ambient-open. Necessity uses a generic noncut detector and pointwise cut/one-active obstructions; it does not assert a universal pointwise noncut rank theorem. The weak-class sharpness family has dimension `6n−3` for n≥3. Added Fourier, triangle-redirection and quartic-hypersurface tags match the manuscript. Existing complete-factor/coherent-transport and strict-domain qualifications are not weakened.

### 22168797 — K2P principal domain and strict continuous time

Pass, including the typo repair. The main abstract defines `D+` by `0<s<1`, `0<g<1`, `g>2s−1`, and separately the strict continuous-time domain by `s²<g<1`. The strong-class theorem identifies regular-germ containment modulo ordinary triangle redirection, rather than equality of all stochastic images or mixed-sign classification. Strong/weak tree-childness is defined by every/some admissible rooting in the fixed simple one-step convention. Added group-based/Fourier/triangle/strict-continuous-time tags are exact. Independent string comparison verifies the description differs **only** by removal of the final extraneous `r` from `No mixed-sign K2P classification is claimed.r</p>`. Source bindings, AI assistance, licensing, external-review status and all theorem qualifiers are preserved. The accidental leading hyphen in the existing reproducibility keyword is also cleaned.

### 22136869 — Exact tree–theta-trinet collisions

Pass. Abstract and §§1–2 distinguish a genuinely K3P **network parameter** from its explicitly K2P-relabelled shared distribution. They then derive nearby observably genuine K3P collisions separately from submersive Jacobians. The theta trinet admits no tree-child rooting; this is not a counterexample within the strong identifiability class. Strict edgewise continuous time allows generators/rate ratios to vary by edge and does not impose a global clock. The common-subtree extension replaces one internal vertex by one theta blob, not several independently composable replacements. Added observational-equivalence, theta, trinet, site-pattern, Fourier, fiber and exact-counterexample tags are supported without strengthening the claims. All cautions remain in the unchanged description.

### 22089807 — Simultaneous amplifiers beyond 3/2

Pass. The main model definitions and §1 retain the quantifier order: one fitness-independent weighted graph family, each fixed fitness `1<r<R_hyb`, and a family-size threshold allowed to depend on r. `R_hyb≈1.5028569` is a lower bound on the unrestricted threshold, and its optimality is only within the displayed first-order pair–pendant model. The unrestricted threshold and finite universal upper bound remain open. Weak-cut asymptotics, weighted Moran processes, selection amplification and drift are valid search concepts. Existing manuscript-printed MSC values are preserved. The unchanged description carefully separates finite symbolic replay from analytic population/weak-cut asymptotics.

### 22089748 — Complete-graph local optimality and strong-selection rigidity

Pass. Abstract and §1 distinguish strict **local** optimality at fitness two for all directed/nonreversible normalized perturbations from fixed-graph strong-selection rigidity. They explicitly leave global complete-graph maximality at fitness two open and allow population-sequence thresholds depending on fitness. The fair-geometric union ancestry/coverage representation, stationary collision observable and Hessian-sector decomposition support all new method keywords. No global result is accidentally promoted by the metadata, and the low-order triangle/K4 global results stay separate from the general local theorem.

### 22089551 — Single-linkage bimolecular weakly reversible recurrence

Pass. Main Theorem 2.1 fixes finite weakly reversible one-linkage bimolecular networks and every positive rate vector; nonabsorbing reachable classes are positive recurrent/nonexplosive, while absorbing singletons carry point-mass laws. Lemma 2.2 gives broader reachability symmetry, not broader positive recurrence. §§1–2 and the supplement expressly keep multiple linkage classes and higher molecularity outside the theorem. The marked-target/log-factorial and random-time drift construction supports the added Foster–Lyapunov and random-time terms. Anderson–Kim conjecture is the relevant named problem, with its full resolution clearly excluded by existing prose. Stationary distributions/nonexplosion are genuine conclusions; no bounded-path, all-moments or finite-atlas universal-proof claim is added.

### 22089373 — Sharp strong tree-childness under JC

Pass. Main Theorems 1.1–1.3 and Definition 2.1 require labelled binary LSA-rootable already-simple semi-directed strong networks and a fixed one-step convention. The result is generic outside a proper algebraic exceptional set, modulo ordinary triangles; local common-germ existence is explicitly not full-image equality. Positive bridge factors recover projective tensors modulo incidence scales, not physical bridge multipliers. Weak-class sharpness includes triangle-free pairs for every n≥4. Added generic-identifiability, directed-containment, semi-directed/Fourier/invariant/bridge-reconstruction tags accurately describe this setting. The unchanged description preserves the class and parameter limits.

### 22013710 — Exceptional four-dimensional Hecke Yang–Baxter operator

Pass, including exact prose preservation. Main Theorems 1.1–1.3 give a 16×16 unitary operator on local dimension four, the faithful Hn(3,6) localization, dimension-four minimality, and the scalar enhancement `2 P_H(L;i,i)`. §§1/8–9 explicitly attribute independent concurrent quaternionic construction and transferred finite-image/Clifford/polynomial-time conclusions to Galindo–Rowell. New Pauli/Clifford/Jones–Wenzl/Markov/HOMFLYPT/Turaev/quaternionic/link/finite-image terms are directly present. Independent HTML removal/entity decoding/whitespace normalization verifies that the proposed description's entire visible text is **identical** to the current text; only eleven nested div wrappers and empty whitespace content are removed. No concurrent-priority or dependency caveat is deleted.

### 21699161 — Minimum Bell-setting complexity for qubit POVM/PVM separation

Pass, including ORCID completion. The deposited Main Theorem and §§1–2 concern local Hilbert dimensions at most two, arbitrary finite input-dependent output alphabets, and shared-randomness **convex hulls**. The two-input equality is not same-state simulation, raw nonconvex image equality, operator-level POVM simulability or an outcome-count threshold. The rational 3×2 witness provides a lower bound strictly above a global analytic PVM upper bound, not a claimed global optimum. Lorentz-cone simulation, incidence geometry and the three-state-discrimination construction support the new tags. Creator patch adds only the human user's supplied ORCID to the existing correctly ordered name, preserving null affiliation. The added structured source-release URL already appears literally in the current description and points to the named release. AI/unreviewed provenance is unchanged.

## Nonblocking discovery opportunities

The two NMSC records use the long model name but do not add the acronym `NMSC` as a keyword; an acronym tag would be a reasonable optional improvement. Likewise `CCR` is a standard internal acronym in the direct-sequence paper and could accompany its spelled-out behavior tag. The tree–theta collision record could optionally carry `K2P` and `K3P` keywords in addition to full model names. These are search-coverage suggestions only; no content correction is required, and this reviewer did not edit any patch.

## Handoff

The proposals are ready for the root agent's separate API-compatibility and same-record publication checks. This review does not authorize or perform a new record/version operation. Same-DOI behavior and record/file identity must be verified through the root's chosen metadata-only update flow.

## Addendum: adopted acronym tags

At 2026-10-10T14:20:13-07:00, verified the root-adopted additions: `NMSC` and `CCR` for 22729537, `NMSC` for 22729545, and `K2P`/`K3P` for 22136869. Each is used explicitly in its deposited main manuscript and accurately abbreviates the existing named model or behavior object. These are search synonyms and introduce no theorem or scope change. The QA JSON now binds all 15 current patch files by SHA-256 and updates keyword counts for the three changed proposals. All content checks remain passing.
