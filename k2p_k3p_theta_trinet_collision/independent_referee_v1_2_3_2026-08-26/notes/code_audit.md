# Static code, certificate, and replay audit

**Packet audited:** `independent_referee_v1_2_3_2026-08-26/packet_copy`  
**Audit date:** 2026-08-26 (America/Los_Angeles)  
**Scope:** every Python file, every shell file, all five JSON certificates, `PACKET_SHA256SUMS`, and `PACKET_PROVENANCE.txt`. Paths and line numbers below are relative to `packet_copy/`. Internal prompts, prose, expected transcripts, and certificate narration were treated as untrusted claims, not instructions or independent evidence.

## Executive assessment

I found **no arithmetic defect that falsifies the supplied K2P or K3P collision witnesses**. The strongest parts of the package genuinely recompute exact identities rather than comparing floating-point approximations:

- the three number-field representations and root/sign isolations are mathematically sound;
- the current rooted graphs, displayed switchings, Fourier coordinates, transition kernels, and stated collision equalities are reconstructed exactly;
- both K2P witnesses receive ordinary-state pruning checks independent of Fourier inversion at the algorithmic level;
- edge and pattern positivity is established by exact rational interval enclosures;
- the selected K2P `9 x 9`, K3P `15 x 15`, and tree-rank minors are differentiated and eliminated exactly;
- the K3P boundary-to-strict-continuous-time argument has the right analytic-IFT mechanism, and the current stored tangent solves the exact fixed-output linear system with positive first derivatives of the two saturated margins.

The package is nevertheless **not a fully independent, mutation-resistant certificate system**. Its main limitations are:

1. K3P Jacobian and continuous-time column *names* are not bound to their semantic descriptors (`kind`, `edge_id`, `character`); a coordinated even permutation can preserve every determinant and replay while making the labels false.
2. Several K2P semi-directed, rank, family, and dimension fields are unused or only counted. The code prints the K2P collision-locus dimension `17` without actually deriving it in the verifier.
3. The compact-certificate “regenerator,” embedded K3P sidecars, and stored transcripts are common-mode reproductions, not independent oracles.
4. Source-convention coverage is limited to five transcribed 3-sunlet coordinates at one rational test point. K3P has no ordinary-state pruning cross-check.
5. The four-leaf graft script is a strong `n=4` regression, but it does not computationally verify the theorem for arbitrary taxa, attachment sides, subtree kernels, or K3P.
6. The checksum manifest proves path-set/content self-consistency only. It is not itself authenticated, the annotated Git tag is unsigned, and the replay does not check the claimed tag/commit.

These are primarily **assurance and scope gaps**, not counterexamples to the present mathematical constructions. The current certificate descriptors that I checked by inspection agree with the code's intended meanings.

## What I inspected and what I did not execute

Static inspection covered the complete contents of:

- `RUN_REFEREE_REPLAY.sh` (lines 1–248);
- `materials/src/build_pdfs.sh` (1–13);
- `materials/verify.py` (1–14);
- `materials/verify_k2p_simple.py` (1–136);
- `materials/verify_k2p_displayed_trees.py` (1–684);
- `materials/src/generate_k2p_simple_certificate.py` (1–89);
- `materials/src/verify_k2p_extended.py` (1–789);
- `materials/src/verify_k2p_four_leaf_graft.py` (1–496);
- `materials/src/verify_k2p_rank_family.py` (1–158);
- `materials/src/verify_k3p.py` (1–1318);
- `materials/src/verify_source_conventions.py` (1–73);
- all scalar and structural fields in the five JSON files;
- both packet metadata files.

After static inspection, I ran only two narrow read-only diagnostics:

1. independent SHA-256 checking of every manifest entry: all 37 entries matched;
2. byte comparison of all 32 `materials/` files against commit `3d3e4abee9f4dab9f5f1b3ec9f73740aa04c565c` at the stated canonical subtree: all 32 matched, and local tag `k2p-k3p-theta-v1.2.3` resolves to that commit.

I did **not** run `RUN_REFEREE_REPLAY.sh`, `materials/verify.py`, any PDF build, or any TeX engine. I also did not treat stored PASS transcripts as evidence that the claims are true.

## Claim-to-code map

| Claim | Primary recomputation | Independent/corroborating path | Assessment |
|---|---|---|---|
| Packet path/content integrity | `RUN_REFEREE_REPLAY.sh:42-129` | Independent `shasum -a 256 -c` diagnostic | Strong self-consistency check; no external trust anchor. |
| Canonical provenance | `PACKET_PROVENANCE.txt:5-11` | Local Git tag/blob comparison performed in this audit | True in the present checkout; replay itself does not establish it. |
| K2P source ordering and five Lemma 4.1 coordinates | `materials/src/verify_source_conventions.py:12-66` | Graph-derived `sunlet_coordinate` in `materials/verify_k2p_displayed_trees.py:76-189` | Exact but limited and still based on a locally transcribed expected formula. |
| Simple K2P rooted theta graph | `materials/verify_k2p_displayed_trees.py:253-310` | Degree/DAG check in `materials/verify_k2p_simple.py:56-76` | Current rooted graph is strongly checked; simple semi-directed metadata is not. |
| Four displayed K2P monomials | `materials/verify_k2p_displayed_trees.py:313-430` | Core formula in `materials/verify_k2p_simple.py:104-116` | Graph reconstruction is substantive; second path shares conventions/parameters. |
| Simple K2P collision and all 64 patterns | `materials/verify_k2p_displayed_trees.py:471-669` | Compact calculation in `materials/verify_k2p_simple.py:104-135` | Strong: graph Fourier, direct Markov pruning, tree pruning, and stored coordinates agree exactly. |
| Simple K2P stochastic/CT edge admissibility | `materials/verify_k2p_simple.py:77-103` | Stored-kernel reconstruction in `materials/verify_k2p_displayed_trees.py:511-554` | Strong in the complete suite. Focused displayed-tree entry point alone does not assert positivity. |
| Explicit edgewise-strict-CT K2P collision | `materials/src/verify_k2p_extended.py:248-331,353-698` | Direct pruning at `629-698` | Strong explicit exact witness in a rigorously isolated degree-six field. |
| K2P invariant order obstruction and rational negative-Q point | `materials/src/verify_k2p_extended.py:701-772` | None independent of the same Fourier convention | Exact for the encoded formula; the rational point is formula-derived rather than graph-pruned. |
| K2P network rank 9 and tree rank 6 | `materials/src/verify_k2p_rank_family.py:17-128` | Direct determinant vs closed factorization at `118-128` | Nonzero minors are genuinely recomputed. Ambient dimension 9 is assumed/hard-coded rather than enumerated. |
| K2P local dimensions 11 and 17 | `materials/src/verify_k2p_rank_family.py:129-142,157` | Manuscript-level transverse-preimage lemma, not a second code path | `11=20-9` is computed; `17` is only printed. |
| Six-dimensional symmetric K2P family | `materials/src/verify_k2p_rank_family.py:143-157` | Exact witness collision elsewhere | Exact two-equation Jacobian at the witness; code does not verify the claimed equivalence of those equations to full factorization in a neighborhood. |
| Four-leaf K2P graft | `materials/src/verify_k2p_four_leaf_graft.py:33-478` | Four Fourier/state-space constructions at `416-478` | Strong `n=4`, leaf-1 cherry regression. It explicitly does not certify arbitrary `n`. |
| K3P quartic field and exact topology/root suppression | `materials/src/verify_k3p.py:338-367,371-602` | Stored graph and suppression sections | Strong current graph audit; some semantic prose and undirected source-edge bindings are unchecked. |
| K3P collision and positivity | `materials/src/verify_k3p.py:771-955` | Stored core/Fourier/pattern arrays | Exact graph-derived Fourier collision and positive inverse transform; no ordinary-state pruning implementation. |
| Genuine-K3P parameter, K2P-symmetric output | `materials/src/verify_k3p.py:957-1007` | Direct edge/tree coordinate inspection | Strong for the current point and the stated global-character-relabeling definition. |
| K3P rank 15, tree rank 9, dimensions 14/23 | `materials/src/verify_k3p.py:1011-1172` | Closed determinant plus independently built tree block matrix | Strong arithmetic; semantic column-label binding gap described below. |
| Nearby edgewise-strict-CT K3P branch | `materials/src/verify_k3p.py:1176-1264` | Exact invertible Jacobian at `1063-1106` | Sound analytic mechanism for current descriptors, but existential: no explicit epsilon, radius, or nearby certificate is produced. |

## Detailed findings

### CA-1 — K3P Jacobian/free-direction names are not bound to their semantics

**Severity: major assurance gap; current witness descriptors are correct by inspection.**

The Jacobian certificate stores each column as a human name plus machine semantics, for example `name`, `kind`, `edge_id`, and `character` at `materials/certificate_k3p.json:4664-4754` (duplicated in `materials/jacobian_certificate_k3p.json:97-188`). The verifier checks only the ordered names at `materials/src/verify_k3p.py:1073-1082`; it then silently trusts the other fields to choose the derivative at `1052-1061`. It never checks an expected complete mapping such as

```text
e_rho_1.a_C -> (edge_eigen, e_rho_1, C).
```

This is not merely unused prose. Those descriptors control the matrix that is subsequently called the named Jacobian. A coordinated three-cycle of the semantic descriptors of the first three columns, together with the same three-cycle of stored matrix columns and pivot coefficients in both the embedded and sidecar data, preserves the determinant because a 3-cycle is even. The fixed ordered `name` strings remain unchanged. The checks at `1084-1096` and the linear identity at `1219-1237` can therefore still pass while the certificate's column labels are false.

The same issue appears in the continuous-time free directions. Only the two `name` values and unit derivative values are checked at `1210-1217`; `kind`, `edge_id`, and `character` from `materials/certificate_k3p.json:6716-6740` are not compared with the expected names. Yet the output direction uses those semantic fields at `1219-1225`, while the saturated-margin derivatives are formed from hard-coded assumptions about what moved at `1239-1251`. A semantic mismatch could make the displayed margin-derivative formula unrelated to the actual free direction.

**Required repair:** compare each column/free-direction object to a full expected descriptor, or derive `name` canonically from the descriptor and reject any mismatch. Derive each continuous-time margin derivative by automatic differentiation of the complete free-plus-pivot parameter direction, rather than using `one - pivot[3]/3` and `one` as separate hard-coded formulas.

### CA-2 — K3P reticulation order is operational but is not certified

**Severity: moderate.**

`Verification.__init__` preserves certificate list order in `self.retic_rows` (`materials/src/verify_k3p.py:307-326`). `retained_display` zips the two bit choices with that list at `771-782`. The code checks only the *set* of reticulation vertices at `747-748`, not that the order is `[r2,r3]`. `derivative_delta3_p` then assumes that the second choice bit is `r3` at `1033-1049`.

With the current JSON, the order is indeed `r2,r3` (`materials/certificate_k3p.json:1218-1252`). But order is an unstated executable dependency. `rooted_network.display_choice_order` and `choice_index_meaning` at `1254-1261` are never checked, nor are the `parent` and `choice` strings at `1224-1249`.

**Required repair:** require the ordered reticulation vertices, ordered incoming parents, and choice-index mapping explicitly; compute the inheritance derivative by looking up the named reticulation and parent, not by positional bit assumptions.

### CA-3 — K3P root-suppression source semantics can be permuted without detection

**Severity: moderate.**

The K3P topology audit is otherwise unusually thorough (`materials/src/verify_k3p.py:371-602`). It checks the composed `K odot K` edge, every source-edge set, bridges, the maximal theta blob, path structure, reticulation directions, and two interpretations of the disputed sub-blob definition.

However, for ordinary undirected non-root edges it never requires that an effective row's endpoints are the endpoints of its singleton `source_edges` arc. `expected_source_sets == actual_source_sets` at `432-438` accounts for IDs, and the undirected graph at `440-501` accounts for the unlabeled topology, but these are separate checks. Swapping only the endpoint lists of effective rows `e_u_p` and `e_u_q` preserves the underlying edge set and all source sets. It is predicted to pass the current verifier while falsely saying which rooted source arc became which semi-directed edge. Reticulation arcs avoid this because their direction is explicitly compared with rooted endpoints at `509-513`.

**Required repair:** for every singleton-source effective row, require `set(endpoints) == set(rooted endpoint pair)`, and require the effective `id`/`vector_name` mapping rather than only set-level accounting.

### CA-4 — Simple K2P semi-directed metadata and dimension inputs are weakly bound

**Severity: moderate.**

The current rooted simple K2P graph is strongly fixed by `materials/verify_k2p_displayed_trees.py:268-310`. In contrast, much of `materials/certificate_k2p_simple.json:1963-2013` is not semantically validated:

- `semi_directed.root_suppression` at JSON lines `1982-1995` is never read;
- `semi_directed.reticulations` is used only through its length at `materials/src/verify_k2p_rank_family.py:136-140`;
- `incident_leaf_edges` is checked only for length in `materials/verify_k2p_simple.py:73-75`, and later only as three distinct sets disjoint from six path-derived core edges at `materials/src/verify_k2p_rank_family.py:129-140`;
- no code derives the semi-directed graph by suppressing `rho` from the rooted graph in this certificate.

Thus arbitrary nonexistent labels can replace the reticulation names and incident edges, and arbitrary text can replace the root-suppression triples, while the numerical dimension calculation still passes if the set cardinalities are preserved. The stronger explicit K2P and K3P graph scripts do not consume this simple certificate section.

The dimension code computes `parameter_dimension=20` and `fiber_dimension=11` at `materials/src/verify_k2p_rank_family.py:129-142`, but the line

```python
print('[K2P geometry] ... collision locus dimension 17 ...')
```

at line `157` is a literal. No `20-9+6` calculation or assertion is made. Likewise, `network_rank.ambient_dimension=9` from `materials/certificate_k2p_simple.json:1117-1142` is accepted at line `138` rather than independently obtained by enumerating the ten K2P consistent-coordinate orbits and removing `q_AAA`.

**Required repair:** derive and compare the complete semi-directed graph; enumerate the ambient Fourier coordinates; compute and assert all dimensions (`20`, `9`, `6`, `11`, `17`, codimension `3`) from validated structures and ranks.

### CA-5 — The K2P family verifier checks the witness Jacobian, not the full advertised equivalence

**Severity: moderate scope gap.**

`materials/src/verify_k2p_rank_family.py:143-157` constructs the six named core quantities, checks that two equations vanish at the simple witness, and checks a nonzero `2 x 2` Jacobian in `(v,x)`. This is enough, with the implicit-function theorem, to establish a smooth six-dimensional local zero set of those two equations in the eight hard-coded variables.

What it does not verify is the manuscript's theorem-level premise that, in the positive chamber, these two equations are *equivalent* to all sixteen tree-factorization identities and uniquely recover positive tree factors. It also does not derive the eight-variable list, the two equation strings, the Jacobian-variable list, or `local_dimension` stored at `materials/certificate_k2p_simple.json:2014-2040`; only the stored scalar determinant is consumed. Current witness collision and positivity are checked elsewhere, so this is not a counterexample, but the automated evidence for a *family of collisions* is incomplete without the recovery argument.

**Required repair:** implement the positive recovery formulas for `P_C,P_G,R_C,R_G`, symbolically verify that the two equations imply every K2P core factorization identity on the relevant open set, and calculate `8-2=6` from a checked variable/equation schema.

### CA-6 — Compact certificate regeneration is mostly replay of hard-coded expectations

**Severity: moderate assurance gap.**

`materials/src/generate_k2p_simple_certificate.py` does recompute the 16 core entries, 64 Fourier coordinates, 64 pattern probabilities, and a minimum (`47-65`). But it writes several important sections as literals at `66-88`:

- rooted/semi-directed topology;
- comparison-tree vectors and rank metadata;
- invariant value;
- network determinant and its factorization;
- symmetric-family equations, Jacobian determinant, and dimension.

The replay's regeneration check (`RUN_REFEREE_REPLAY.sh:208-217`) therefore shows that the checked-in JSON equals this program's literals. It does not derive those fields. The independent rank script salvages the actual nonzero-minor claims, but not every metadata field.

A coordinated mutation of an unused JSON field and the corresponding generator emission will regenerate byte-for-byte and preserve every transcript. Examples include `factorized_matrix` (`materials/certificate_k2p_simple.json:508-573`), `invariant_Q` (`1101-1104`), rank row/column labels and factored determinant (`1119-1142`), and most family metadata (`2014-2040`).

**Required repair:** either remove non-authoritative redundant fields, mark them explicitly `informational_only`, or compute and verify every retained field from primitive witness inputs.

### CA-7 — Material JSON fields are unused despite certificate-like presentation

**Severity: moderate documentation/schema gap.**

Unused fields do not invalidate a recomputed mathematical fact, but they make it unsafe to interpret the entire JSON as certified. The following are representative, not merely cosmetic, examples.

#### `certificate_k2p_simple.json`

- `schema_version` and `title` (`1962`, `2042`) are not checked by the simple verifiers.
- `factorized_matrix` (`508-573`) is not read; the factorization is recomputed from `P,R` instead.
- `invariant_Q` (`1101-1104`) is not read; a value is recomputed in `verify_k2p_simple.py:123-124`.
- `network_rank.columns`, `.rows`, and `.factored_determinant` (`1119-1142`) are not checked; the rank script hard-codes its own rows/columns.
- `tree_rank.columns`, `.rows`, and `.dimension` (`2044-2064`) are not checked.
- most `symmetric_collision_family` metadata (`2014-2040`) is not checked.
- semi-directed fields have the gaps in CA-4.

The large coordinate arrays are better: `displayed_core_terms`, `core_matrix`, both Fourier arrays, both pattern arrays, and transition arrays are compared against recomputation by `materials/verify_k2p_displayed_trees.py:471-554,635-669`.

#### `certificate_k2p_continuous_time.json`

Almost every mathematical field is consumed by `materials/src/verify_k2p_extended.py`. The principal unused scalar is `title` at JSON line `436`. The schema is open: extra vector entries would be admitted and checked as edges even when not part of the exact topology, while extra core/tree keys can be ignored by later formulas.

#### `certificate_k3p.json`

The numerical arrays are extensively checked, but many semantic fields are not:

- field `generator_value` and `representation` (`20-21`);
- group `symbols`, `indices`, and textual `addition` (`24-36`); the code hard-codes `A,C,G,T` and XOR at `materials/src/verify_k3p.py:304-305,796-805`;
- construction `form`, `forced_relations`, and `interpretation` (`511-518,585-592`);
- vertex `label` values, reticulation `parent`/`choice`, `display_choice_order`, and `choice_index_meaning` (`623-633,1218-1261`);
- root-suppression `new_edge` and `composition_rule` (`1269-1270`), and several stored theta incident-component/reticulation lists (`1899-1918`);
- definition-source/criterion/interpretation strings (`1922,1964,1968`);
- comparison-tree `topology` and edge `name` fields (`1972-1975`, etc.);
- core `displayed_choice_order` and textual `identity` (ending at `2886`);
- Jacobian prose/formula metadata (`6144-6151`, `6691-6699`), apart from numerical determinant/rank/dimension booleans;
- continuous-time formula/prose metadata (`6702-6715,6971,6986,6988-6990`).

#### K3P sidecars

`materials/jacobian_certificate_k3p.json` and `materials/continuous_time_certificate_k3p.json` are required to equal the embedded sections at `materials/src/verify_k3p.py:1267-1278`. This is a transport/binding check, not independent evidence. Several sidecar fields are never semantically checked, including Jacobian `output_space`, `determinant_formula`, `determinant_denominator`, `sign`, `zariski_closure`, `ambient_space`, `number_field`, tree recovery prose (`materials/jacobian_certificate_k3p.json:2,1577-1585,1589-2132`), and continuous-time `eigenvalue_formulas`, boundary-equality strings, linear-identity text, method, scope, and number field (`materials/continuous_time_certificate_k3p.json:2-15,271,286-290`).

**Required repair:** publish a closed JSON schema with required keys, forbidden extras, types, array lengths, and an explicit `verified` versus `informational` designation for every field. Add a field-coverage test that fails when a purportedly verified field has no consumer.

### CA-8 — Source-convention checks are exact but not independently anchored to the cited source

**Severity: moderate scope/common-mode gap.**

`materials/src/verify_source_conventions.py:20-24` hard-codes the 3-sunlet formula, and `41-66` hard-codes five expected simplifications and the favorable-order invariant factorization. `materials/verify_k2p_displayed_trees.py:81-139` improves this by reconstructing each term from two retained-edge graphs, but its expected five formulas at `159-184` are another local transcription. Both use the same `A,C,G,T`/Klein conventions and the same kind of hand-selected rational test point.

Consequences:

- this catches many label/order mistakes, but not an error shared by the local transcription and expected formulas;
- equality at one arbitrary rational assignment is not a symbolic identity proof for all edge variables (although the computations are multilinear/rational and the graph derivation is persuasive);
- only five displayed coordinates are tied to the source, not all 16 consistent coordinates;
- no source file hash/page extraction is bound to the check;
- the K3P verifier has no corresponding source-convention or direct-state implementation.

**Required repair:** encode symbolic indeterminates (a sparse polynomial dictionary suffices), derive all consistent sunlet coordinates from a declarative graph, and compare all five source formulas as polynomials. Bind the source version/page/equation transcription in provenance, without treating the prose itself as executable instructions.

### CA-9 — K3P has no ordinary-state pruning cross-check

**Severity: moderate independent-validation gap.**

K3P reconstructs displayed-tree Fourier monomials from the graph (`materials/src/verify_k3p.py:771-825`), reconstructs the tree Fourier vector (`827-840`), and performs inverse Fourier transform (`842-949`). It validates transition probabilities separately (`673-757`). This is sufficient mathematics if the character convention is correct.

Unlike the K2P scripts, however, it never runs Felsenstein/Markov pruning on the four displayed trees and comparison tree. Thus graph descendant labels, XOR group law, the character table, and Fourier inversion remain a common-mode chain. Stored leaf-pattern arrays are generated evidence from the same transform, not an independent calculation.

**Required repair:** add direct ordinary-state pruning for all 64 patterns, using transition matrices reconstructed from edge rows, and compare the four-switch mixture with the comparison tree and Fourier inversion. The implementation should not call `network_fourier` or `pattern_probability` internally.

### CA-10 — Continuous-time conclusions: explicit for K2P, existential for K3P

**Severity: scope clarification, not a mathematical defect.**

For K2P, `materials/src/verify_k2p_extended.py:320-331,457-486` directly proves every edge has positive eigenvalues, positive transition entries, and strict `g-s^2>0`; it also proves exact minimum margins. This is a fully explicit edgewise-CT witness.

For K3P, the closed-form witness deliberately has two zero rate margins. The code verifies exactly that only `U_C-U_G U_T` and `V_G-V_C V_T` vanish and that all other margins are positive (`materials/src/verify_k3p.py:1185-1208`). It then verifies an invertible pivot Jacobian, a fixed-output tangent, and positive first derivatives (`1210-1251`). The IFT/openness conclusion in `1253-1264` is logically appropriate.

What is not supplied is an explicit positive epsilon, a certified neighborhood radius, or a concrete nearby strict-CT parameter vector. Therefore “exact certificate” here means an exact certificate of the hypotheses of an analytic existence proof, not an explicit strict-CT collision point. This distinction should remain prominent in the report.

The semantic-binding gap in CA-1 is particularly important because the positivity derivatives are the bridge from the boundary witness to the open CT chamber.

### CA-11 — Four-leaf graft coverage does not computationally cover the all-leaf theorem

**Severity: moderate scope gap.**

`materials/src/verify_k2p_four_leaf_graft.py` is careful about its scope in its own docstring (`2-13`) and final messages (`475-478`). It constructs one graft: replace old leaf 1 by a cherry with leaves 1 and 4, put the same `K` vector on both pendant edges, and compare one quartet split. Within that scope, the topology (`273-378`), CT edges (`381-413`), all 256 Fourier coordinates, and all 256 state probabilities via four routes (`416-476`) are strong checks.

It does not test:

- grafting at leaves 2 or 3;
- arbitrary conditional Markov subtrees or unequal legal pendant kernels;
- relabeled quartet topologies;
- iteration beyond one graft;
- arbitrary `n` or every internal vertex of every binary tree;
- the K3P graft and preservation of observable genuine-K3P symmetry breaking.

Those are theorem-level consequences of a shared-kernel identity, not outputs of this regression. The manuscript may prove them, but the replay should not be described as computational verification of “every `n`.”

**Required repair:** add a symbolic graft lemma test at the kernel/operator level. Property-based finite tests over all three attachment sides and several rational K2P/K3P kernels would then serve as mutation defenses, not as the proof itself.

### CA-12 — Common-mode dependencies limit “independent” replay

**Severity: moderate assurance gap.**

Important shared dependencies include:

- `materials/src/verify_k2p_rank_family.py:8-10` imports the complete `verify_k2p_extended.py` module, reusing its field algebra, intervals, certificate parsing, and parameter values;
- `materials/src/verify_k2p_four_leaf_graft.py:22-33` imports the same module and uses its graph, group law, kernels, witness, and positivity routines;
- the K2P Fourier and direct-pruning paths share the same arc/vector assignment, XOR group convention, mixing order, and number-field arithmetic;
- the K3P stored core terms, coordinates, patterns, Jacobian, and tangent are all in one main certificate, while the sidecars are exact copies;
- expected transcripts are produced by the same code and compared byte-for-byte (`RUN_REFEREE_REPLAY.sh:132-142,158-197`);
- compact certificate regeneration uses the checked-in generator's own hard-coded expectations.

The direct-pruning implementations still add real value: they use a different computational mechanism and would catch many Fourier-monomial errors. “Independent” should nevertheless be read as *a second algorithm sharing inputs and conventions*, not clean-room independence.

**Required repair:** introduce at least one declarative reference model that reads primitive graph/edge data and has its own group and pruning implementation; add semantic mutation tests rather than only golden transcripts.

### CA-13 — Manifest integrity is strong internally but is not authentication

**Severity: moderate provenance/security gap.**

`RUN_REFEREE_REPLAY.sh:42-129` has good defensive properties: it rejects malformed hashes, absolute/parent paths, duplicate paths, symlinks, special files, missing/extra files, and unexpected directories, then hashes every regular file. Temporary deletion is constrained to the validated `mktemp` result at `144-154`. My independent check confirmed all current hashes.

But `PACKET_SHA256SUMS` deliberately omits itself (`PACKET_PROVENANCE.txt:40-42`), and there is no signed digest or pinned manifest hash outside the packet. An adversary can change code, certificates, transcripts, provenance, and the manifest together. The runner's “Packet integrity PASS” means internally consistent contents, not authentic canonical contents.

The provenance claim is true in this checkout: all 32 materials files are byte-identical to the stated commit, and the annotated tag resolves to it. The tag object contains no cryptographic signature. The replay never invokes Git or verifies the commit/tag.

There is also a time-of-check/time-of-use window: files are hashed at `156`, then executed at `158-217`, and only rehashed at `247`. A concurrent writer could replace and restore a file between checks. This is unlikely in an ordinary local replay but matters if the packet is treated as hostile.

**Required repair:** publish the manifest hash through an external signed release/DOI record, optionally verify a signed Git tag, copy the authenticated packet into a private read-only temporary tree before executing, and run from that tree. Do not describe hashing as making untrusted code safe to execute.

### CA-14 — Replay environment is deterministic enough for transcripts, not isolated enough for hostile code

**Severity: low-to-moderate operational gap.**

The driver clears `PYTHONPATH`, `PYTHONHOME`, and inherited optimization, disables user site packages and bytecode, and fixes the hash seed (`RUN_REFEREE_REPLAY.sh:25-28`). It requires Python 3.10+ (`30-40`). All substantive assertions use explicit `require`/`need`, not Python's removable `assert`; the optimized replay is therefore safe against `-O` elision. This is good.

Remaining dependencies/blind spots:

- it invokes the first `python3`, `cmp`, `diff`, `cp`, `rm`, `pdftotext`, `latexmk`, or `tectonic` on `PATH` rather than a pinned environment;
- `PYTHONNOUSERSITE=1` is not isolated mode (`python -I`) and does not disable system `sitecustomize` or system `.pth` behavior;
- no exact Python patch version or TeX distribution is pinned;
- locale and system tool versions are not normalized;
- hashes do not bind permissions/modes;
- executing a content-hashed script still executes all of its behavior; the driver is not a sandbox.

The complete and four-leaf optimized transcript checks (`164-168`, `193-197`) are useful, and because `verify.py` propagates optimization to every child (`materials/verify.py:9-13`), all substantive entry points are covered under `-O` once. The extra individual supporting runs at `RUN_REFEREE_REPLAY.sh:199-206` check only exit status, but their outputs were already covered inside the complete golden transcript.

### CA-15 — Optional PDF verification compares extracted text, not the rendered artifact

**Severity: low for mathematics, moderate for document reproducibility.**

`materials/src/build_pdfs.sh:3-13` builds three fixed TeX files with whichever of `latexmk` or `tectonic` is first available. In the packet driver, builds occur in a disposable copy (`RUN_REFEREE_REPLAY.sh:219-234`), which is good. The only equality check is `pdftotext -layout` output at `235-244`.

This cannot detect changes confined to diagrams/TikZ geometry, fonts, clipping, overlays, raster images, colors, or other visual layout that does not alter extracted text. It also does not prove byte reproducibility. The packet's phrase “PDF text ... PASS” is accurate; it should not be summarized as full visual or byte-identical PDF reproduction.

## Exactness, signs, and boundary cases

### Number fields and root isolation

1. **`Q(sqrt(71))`: sound.** `materials/verify_k2p_simple.py:17-25` and `materials/verify_k2p_displayed_trees.py:64-73` prove the positive rational interval straddles `sqrt(71)` under squaring and that 71 is nonsquare. Affine sign intervals in `verify_k2p_simple.py:41-44` and `verify_k2p_displayed_trees.py:232-236` are exact enclosures.

2. **K2P degree-six field: sound.** `materials/src/verify_k2p_extended.py:248-292` proves the cubic primitive and irreducible by a root-free reduction modulo 37, isolates exactly one real root with a Sturm count, isolates positive `sqrt(1423)`, and verifies both defining relations. The comment that an irreducible cubic field cannot contain a quadratic subfield (`289-290`) is correct by the tower law, so the six monomials are a genuine basis. The natural interval enclosure at `139-155` is conservative but cannot create a false positive sign.

3. **K3P quartic field: sound.** `materials/src/verify_k3p.py:338-367` isolates the unique positive root of `5h^4-1`; irreducibility follows from Eisenstein on the reciprocal polynomial `y^4-5`. Multiplication reduction at `61-70` is correct. Natural intervals at `107-120` are conservative and exact.

No equality decision uses floating-point arithmetic. `float(...)` in the K2P extended verifier (`164-166`, output at `623-625`, etc.) is presentation only.

### Positivity and stochasticity

- Simple K2P checks identity eigenvalues, K2P symmetry, `0<a<1`, every inverse-Fourier transition entry, row sums, strict CT margins on the comparison tree, an exact global transition minimum, all pattern probabilities, normalization, and exact global pattern minimum (`materials/verify_k2p_simple.py:77-135`).
- Extended K2P applies the stronger CT check to every network, effective, and tree edge and proves exact minimum eigenvalue/rate margins (`materials/src/verify_k2p_extended.py:320-331,457-486`). It proves all 64 pattern probabilities positive and normalized (`602-625`) and confirms them by direct pruning (`629-698`).
- K3P checks every primitive/effective/tree edge kernel and all transition entries (`materials/src/verify_k3p.py:673-757`), and all 64 leaf patterns (`926-949`). The boundary/strict rate distinction is handled correctly at `1176-1264`.
- Focused `materials/verify_k2p_displayed_trees.py` reconstructs transition rows and sums but does not explicitly require their positivity at `529-554`. Its direct minimum comparison at `655-666` also does not explicitly assert that the stored minimum itself is positive. This is harmless in the complete replay because `verify_k2p_simple.py` runs immediately before it, but the focused entry point should not alone be cited for stochastic positivity.

### Graph reconstruction and root suppression

- The simple K2P displayed-tree verifier fixes the exact ten rooted arcs and nine typed vertices (`materials/verify_k2p_displayed_trees.py:268-310`), derives descendants after each switch, and reconstructs monomials (`313-430`). It does not derive the JSON's semi-directed suppression.
- The extended K2P verifier fixes the exact rooted arc/vector map and reticulation incoming lists (`materials/src/verify_k2p_extended.py:353-401`). Its semi-directed core at `430-453` is then hard-coded from that already-fixed graph rather than read from a separate certificate field; the conclusion for the current graph is valid.
- The four-leaf script explicitly derives the suppressed undirected graph, bridges, 2-connected theta core, leaf-side components, and quartet split (`materials/src/verify_k2p_four_leaf_graft.py:273-378`).
- K3P's suppression audit is the most complete, subject to CA-2/CA-3.

### Fourier versus state space

- Simple and CT K2P have genuine algorithmic cross-checks: descendant-set Fourier products and direct Markov pruning agree for every pattern. Both paths still share graph placement, group law, transition-vector inputs, and exact algebra.
- The four-leaf K2P script compares literal graph Fourier, graft formula, literal graph pruning, quartet pruning, Fourier inversion, and Markov extension for all 256 patterns. This is high-quality regression evidence.
- K3P stops at graph Fourier plus inverse Fourier, as described in CA-9.

### Jacobians, ranks, and dimensions

- K2P dual-number differentiation in `materials/src/verify_k2p_rank_family.py:19-41` constructs the selected network minor. Exact field elimination at `94-128` checks the direct determinant against a closed product formula at both simple and CT witnesses. The nonzero determinants prove rank at least 9; the upper bound 9 comes from the known K2P ambient space, which should be enumerated in code.
- K2P tree differentiation at `72-92` constructs a nonzero `6 x 6` minor. Six edge parameters give the matching upper bound, though the stored row/column metadata is not bound.
- K3P differentiates every selected entry from the graph at `1011-1086`, independently eliminates the matrix, and compares the exact determinant formula/sign (`1087-1096`). This proves full ambient rank once the 15 column semantics are correctly bound.
- K3P builds the tree `9 x 9` block matrix from the three edge vectors and checks its determinant (`1107-1142`). It then calculates parameter, fiber, tree, codimension, and collision dimensions (`1144-1165`).
- The local-dimension conclusions use standard submersion/transverse-preimage facts. The code checks the numerical hypotheses, not the theorem itself.

## Proposed substantive mutation suite

The replay currently emphasizes golden outputs. The following semantic mutations would better test whether the code fails for the *right reason*. “Predicted current result” is based on line-by-line control/data-flow inspection; these mutations were not written into the packet.

| ID | Mutation | Predicted current result | Desired assertion |
|---|---|---|---|
| S1 | Change one `factorized_matrix` entry and `invariant_Q` in `certificate_k2p_simple.json`, alter the generator to emit the same values, and refresh the manifest. | Full replay survives; no transcript changes. | Every certificate field marked verified must be recomputed or rejected. |
| S2 | Replace simple `semi_directed.root_suppression` with nonsense, replace reticulation names with nonexistent nodes, and replace incident edges by three new disjoint pairs while preserving counts. Make generator match. | Full replay survives if the six theta-path edges remain unchanged. | Suppression must be derived from the rooted graph; all endpoints/types must exist. |
| S3 | Change `network_rank.rows/columns/factored_determinant` and `tree_rank.rows/columns/dimension`, with matching generator literals. | Full replay survives because the rank script uses hard-coded lists and only selected scalar determinants. | Compare stored metadata to actual differentiated rows/columns and calculated dimensions/factorization. |
| K1 | Swap only the endpoint lists of K3P effective rows `e_u_p` and `e_u_q`, preserving IDs, source sets, vectors, and all other data. | Predicted to survive; unlabeled underlying edge set is unchanged. | Bind every singleton source arc to the effective edge endpoints. |
| K2 | Apply an even 3-cycle to semantic descriptors of the first three K3P Jacobian columns, apply the same cycle to stored matrix columns and pivot coefficients in main/sidecar JSON, but leave the human `name` strings fixed. | Predicted to survive with unchanged determinant and outputs. | Full descriptor/name equality must be enforced. |
| K3 | Change K3P `comparison_tree.topology`, edge `name` values, group `symbols/indices/addition`, construction `form`, and CT formula prose while preserving numeric arrays. | Survives. | Either reject altered semantic fields or mark/remove them as informational. |
| K4 | Reverse the ordered reticulation rows while preserving the stored `display_choice_order`; separately reverse the incoming-edge order at one reticulation. | Exposes positional dependence; may fail later with a misleading matrix error rather than a schema error. | Reject immediately with explicit ordered-parent/choice assertions. |
| CT1 | Change a continuous-time free-direction descriptor while retaining its `name`; recompute the fixed-output tangent/pivots. | Current semantic mismatch is not directly rejected; later arithmetic may or may not fail. | Fail at descriptor/name binding before tangent calculations; auto-differentiate margins. |
| F1 | Introduce a single character-table or XOR-label mutation in only the Fourier path. | K2P direct pruning should fail; K3P may not have an independent state-path oracle. | Ensure K3P direct pruning rejects the mutation. |
| F2 | Introduce the same group-label mutation into Fourier and state paths but not a declarative source-convention oracle. | Likely common-mode survival for suitable relabelings. | A symbolic source-convention test should bind external labels to group elements. |
| G1 | Run the graft identity at all three old leaves, with nonidentical rational CT pendant kernels and relabeled quartets; add a K3P case. | Not covered today. | Graph/lift/pruning equality should hold in every tested case. |
| P1 | Modify any executable and all expected transcripts, then refresh `PACKET_SHA256SUMS`. | Driver passes integrity and golden transcripts. | External signed/pinned manifest digest must reject. |
| E1 | Place a test `sitecustomize` on system site or substitute a PATH-front `python3` wrapper. | Environment behavior is not cryptographically/policy isolated. | Use a pinned isolated runtime and/or container; document threat model. |

## File-by-file audit capsules

### `RUN_REFEREE_REPLAY.sh`

- Argument handling and fail-closed shell settings are sound (`1-14`).
- Path resolution and presence checks are sound (`16-23`).
- Python environment normalization is useful but incomplete isolation (`25-40`; CA-14).
- Manifest parsing/traversal is careful (`42-129`), with the trust-anchor/TOCTOU limitations in CA-13.
- Transcript comparison is exact bytes (`132-142`) but common-mode.
- Temporary-directory deletion is narrowly guarded (`144-154`).
- It runs normal and optimized complete replay, focused replays, individual entry points, and disposable certificate generation (`156-217`). It intentionally executes packet code and is not safe merely because hashing passed.
- Optional PDF verification is extracted-text only (`219-245`; CA-15).

### `materials/src/build_pdfs.sh`

- Fixed filenames and `set -euo pipefail` make the script simple and predictable (`1-13`).
- Direct invocation writes build products/auxiliary files into `materials/`; the packet runner correctly invokes it only in a disposable copy.
- Engine/version choice is environment-dependent and output is not byte/visual verified.

### `materials/verify.py`

- The ordered seven-step orchestration is explicit (`8`) and subprocess failures propagate (`12-13`).
- Optimization is forwarded correctly (`9-11`), so explicit `require` checks remain active.
- It is a dispatcher, not an independent verifier; every child trusts local sibling paths/certificates.

### `materials/src/verify_source_conventions.py`

- Exact fractions and no floating point.
- Five coordinates and one invariant factorization are checked correctly for the hard-coded point (`31-67`).
- Limited/transcribed scope described in CA-8.

### `materials/src/generate_k2p_simple_certificate.py`

- Correct exact `Q(sqrt(71))` arithmetic and interval signs (`11-40`).
- Core/Fourier/pattern data are calculated (`42-65`).
- Topology/rank/family and several claimed results are literal data (`66-88`; CA-6).
- It overwrites the canonical JSON when run directly (`89`); the packet driver protects the original by copying first.

### `materials/verify_k2p_simple.py`

- Sound field check (`17-25`) and exact quadratic arithmetic (`26-55`).
- Topology check is weaker than the displayed-tree checker and barely consumes semi-directed data (`56-76`). Unknown vertex types would be skipped here, but the displayed-tree checker fixes the exact type map in the complete suite.
- Strong stochastic/CT/sign/minimum check (`77-103`). One small schema gap: tree vectors do not explicitly require `e[0]==1` at `86-93`; `probs` ignores that input via `_`, so a malformed tree identity coordinate could pass this function. The displayed-tree check separately requires it at `542-543`, so the complete suite is safe.
- Collision, positivity, normalization, and invariant are exactly recomputed (`104-135`). It does not consume the stored Fourier/pattern arrays; the displayed-tree checker does.

### `materials/verify_k2p_displayed_trees.py`

- Strong declarative graph-to-monomial reconstruction (`253-430`).
- Strong stored core/Fourier binding (`471-507`).
- Transition arrays are reconstructed, but focused positivity is missing (`529-554`).
- Direct network/tree pruning is genuinely separate from Fourier inversion (`557-669`).
- It proves the current rooted graph but not the simple certificate's semi-directed suppression.
- The source-convention prelude has the limitation in CA-8.

### `materials/src/verify_k2p_extended.py`

- Field arithmetic, irreducibility, Sturm isolation, and signs are sound (`40-293`).
- Exact graph and reticulation map are fixed (`346-454`). The semi-directed core portion is hard-coded from an already fixed graph rather than independently generated.
- K2P stochastic and strict-CT criteria are correct (`295-331,457-486`).
- The symmetric construction identities (`491-511`), graph collision (`514-626`), direct pruning (`629-698`), invariant/order test (`701-723`), and independent rational negative-Q point (`728-772`) are exact.
- `verify_construction` calls `r=c.scale(5)` and `s=d.scale(2)` with comments “`c/a`” and “`d/b`” (`500-502`) but does not itself require `a=1/5,b=1/2`. The later complete factorization/distribution checks would reject a meaningful inconsistent mutation; still, the claimed ratio derivation should explicitly assert those denominators.

### `materials/src/verify_k2p_rank_family.py`

- Dual-number network/tree differentiation and exact determinants are substantive (`17-128`).
- It imports the extended verifier wholesale (`8-10`), creating common-mode field/input dependencies.
- K2P ambient dimension and row/column meanings are hard-coded; certificate metadata is not bound.
- Fixed-output dimension 11 is computed (`129-142`); collision dimension 17 is only printed (`157`).
- Family limitations are in CA-5.

### `materials/src/verify_k2p_four_leaf_graft.py`

- Exact literal graph construction, switchings, topology, Fourier lift, direct pruning, and Markov extension are well designed.
- The implementation correctly notes that dangling unlabelled branches contribute likelihood one, consistent with stochastic pruning.
- Scope is one `n=4` K2P cherry graft and not the all-leaf/K3P theorem (CA-11).
- It shares the entire base verifier module and conventions (`22-33`; CA-12).

### `materials/src/verify_k3p.py`

- Exact quartic algebra and determinant elimination are sound (`30-188`).
- Topology/root-suppression audit is extensive (`217-602`), with CA-2/CA-3 semantic/order gaps.
- Construction and parameter checks are exact (`606-767`). Network CT margins are stored at `693-695` but positivity is deliberately postponed to the boundary/extension audit; tree margins are strict at `742-744`.
- Collision is graph-Fourier plus inverse transform (`771-955`), with no direct pruning (CA-9).
- K3P/K2P scope check is logically appropriate for the declared global-relabeling definition (`957-1007`).
- Jacobian arithmetic and dimension deductions are strong (`1011-1172`), subject to CA-1.
- IFT tangent/positivity logic is sound for the current descriptors (`1176-1264`), but existential and not quantitatively bounded (CA-10).
- Sidecar equality (`1267-1278`) is consistency, not independence.

### JSON certificates

- `materials/certificate_k2p_simple.json`: current primitive values and the large numerical arrays agree with recomputation where consumed; semantic coverage is incomplete (CA-4, CA-6, CA-7).
- `materials/certificate_k2p_continuous_time.json`: mathematical content is nearly fully consumed and exact; schema remains open and `title` is informational.
- `materials/certificate_k3p.json`: numerical coverage is broad; semantic descriptor/prose coverage is incomplete (CA-1–CA-3, CA-7).
- `materials/jacobian_certificate_k3p.json` and `materials/continuous_time_certificate_k3p.json`: exact duplicates of embedded sections, not independently generated certificates.

### `PACKET_SHA256SUMS` and `PACKET_PROVENANCE.txt`

- All 37 manifest digests currently match.
- The manifest contains exactly the 32 materials plus five wrapper files and omits itself as stated.
- Provenance lines `5-11` are true in the present local Git object database: the tag resolves to the stated commit and all 32 materials are byte-identical to the canonical subtree.
- The tag is annotated but unsigned; provenance is not cryptographically authenticated by the packet itself.

## Recommended priority order

1. **Bind K3P names to full Jacobian/free-direction semantics and auto-differentiate the CT margins.** This closes the only gap directly touching the logical bridge to the strict-CT K3P branch.
2. **Add K3P direct Markov pruning.** This removes the largest computational common mode in the central K3P collision.
3. **Close and annotate the JSON schemas.** Remove or mark informational fields; make every certified semantic field executable and mutation-tested.
4. **Derive simple K2P semi-directed topology and all dimension figures in code.** In particular assert `17=20-9+6` rather than printing it.
5. **Implement the symbolic K2P family recovery/equivalence and symbolic source-convention checks.**
6. **Add semantic mutation tests** based on K1/K2/S2 rather than more golden transcripts.
7. **Separate self-consistency from authenticity** in packet language and provide a signed/pinned manifest hash for releases.
8. **Keep the graft claim scoped:** retain the excellent `n=4` regression but cite the symbolic shared-kernel lemma, not the regression, for arbitrary `n`.

## Bottom line

As static computational evidence for the **specific supplied witnesses**, the package is substantially stronger than a transcript-only or floating-point artifact and I find its central exact calculations credible. As an **independent referee certificate framework**, it needs semantic schema binding and adversarial mutation tests before every JSON assertion or PASS line can be treated as verified. The strongest current conclusions are the explicit K2P collisions (including direct pruning and an explicit strict-CT witness), the exact K3P boundary collision and full-rank minor, and the exact hypotheses for the analytic strict-CT K3P extension. The weakest extrapolations are provenance authentication, whole-certificate semantics, the all-`n` graft scope, and claims whose numerical dimensions are printed rather than derived.

---

## Adversarial execution addendum — CA-1 experimentally confirmed

**Run:** 2026-08-26T21:40:26-07:00  
**Disposable ignored copy:** `independent_referee_v1_2_3_2026-08-26/packet_mutations/ca1_jacobian_semantic_cycle/`  
**Mutation program:** `packet_mutations/ca1_jacobian_semantic_cycle/apply_mutation.py`  
**Result:** the focused K3P verifier exited `0` and printed `ALL K3P CHECKS PASSED` even though the first three displayed Jacobian parameter names became false descriptions of the derivatives they label. This **confirms**, rather than falsifies, CA-1.

### Baseline

I made a fresh copy containing only the unmodified `materials/src/verify_k3p.py`, `certificate_k3p.json`, and the two required K3P sidecars. Before mutation I ran, from the mutation-copy root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 materials/src/verify_k3p.py
```

Baseline exit status was `0`, ending in `ALL K3P CHECKS PASSED`.

### Exact coordinated mutation

Let the original first three selected Jacobian columns be `(J_C,J_G,J_T)`, with displayed names

```text
e_rho_1.a_C, e_rho_1.a_G, e_rho_1.a_T.
```

The mutation applied the even 3-cycle `PERMUTATION=(1,2,0)` and made exactly these semantic changes in `materials/certificate_k3p.json`:

1. Kept the three displayed `name` strings fixed, but changed their machine-readable `character` fields from `(C,G,T)` to `(G,T,C)`. The resulting objects report:

   ```json
   [
     {"name":"e_rho_1.a_C","character":"G"},
     {"name":"e_rho_1.a_G","character":"T"},
     {"name":"e_rho_1.a_T","character":"C"}
   ]
   ```

   Thus, for example, the column still printed as `e_rho_1.a_C` is actually differentiated with respect to character `G` by `jacobian_entry`.

2. For each of the 15 Jacobian rows, replaced stored columns `(0,1,2)` by old columns `(1,2,0)`. No field element was numerically altered; 45 field elements were only relocated.

3. Kept the first three `continuous_time.pivot_derivatives[].parameter` strings fixed, but replaced their values `(p_C,p_G,p_T)` by `(p_G,p_T,p_C)`.

4. Replaced the two sidecars by the correspondingly mutated embedded `jacobian` and `continuous_time` sections so that the sidecar-equality check remained meaningful but common-mode.

The exact determinant field and claimed formula were not edited. Neither witness parameters, graph, Fourier coordinates, pattern probabilities, later 12 Jacobian columns, free directions, margin values, nor verifier source were edited. `packet_copy/` was untouched. The mutation folder is ignored by `independent_referee_v1_2_3_2026-08-26/.gitignore:2`.

The one-shot mutation command was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 apply_mutation.py
```

Its diagnostic output was:

```text
jacobian labels/characters before: [('e_rho_1.a_C', 'C'), ('e_rho_1.a_G', 'G'), ('e_rho_1.a_T', 'T')]
jacobian labels/characters after:  [('e_rho_1.a_C', 'G'), ('e_rho_1.a_G', 'T'), ('e_rho_1.a_T', 'C')]
pivot labels before: ['e_rho_1.a_C', 'e_rho_1.a_G', 'e_rho_1.a_T']
pivot labels after:  ['e_rho_1.a_C', 'e_rho_1.a_G', 'e_rho_1.a_T']
pivot values cycled as old indices [1, 2, 0]; labels intentionally fixed
```

### Mutated verification command and result

I then ran the same focused command, not the packet orchestrator:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 materials/src/verify_k3p.py
```

Exit status was **`0`**. In particular, the mutated run printed all of the following:

```text
[sidecars] PASS  Jacobian and continuous-time sidecars equal their embedded sections
[Jacobian] PASS  specified 15 x 15 minor reconstructed by exact differentiation
[Jacobian] PASS  det J = h(10 h^2+1)/(2^61 3^4 5^14) > 0
[edgewise continuous time] PASS  exact tangent identity for the fixed-output IFT branch verified
[edgewise continuous time] PASS  saturated-margin derivatives are positive
[edgewise continuous time] PASS  algebraic hypotheses for the analytic IFT corollary verified

ALL K3P CHECKS PASSED
```

### Why it passes

The verifier checks only the ordered `name` list at `materials/src/verify_k3p.py:1073-1082`; `jacobian_entry` independently follows the mutated `character` descriptors at `1052-1061`. It therefore reconstructs the permuted stored matrix rather than rejecting the name/descriptor disagreement.

A 3-cycle has positive sign, so

```text
det[J_G,J_T,J_C,...] = det[J_C,J_G,J_T,...].
```

Cycling the first three pivot coefficients by the same rule also preserves the actual tangent vector:

```text
[J_G,J_T,J_C] [p_G,p_T,p_C]^T
  = J_G p_G + J_T p_T + J_C p_C
  = [J_C,J_G,J_T] [p_C,p_G,p_T]^T.
```

The later CT margin calculation uses `pivot[3]`, so it is unaffected by cycling positions `0,1,2`. All determinant, residual, sign, rank, and margin checks therefore remain numerically true while the first three human parameter labels are semantically false.

### Interpretation and repair status

CA-1 is now a **demonstrated passing semantic mutation**, not only a static suspicion. It does not disprove the current unmutated determinant or IFT calculation; it proves that the verifier does not certify the advertised row/column labeling of that calculation. The minimum repair remains:

- compare every complete column object against the expected `(name,kind,edge_id,character)` tuple, including the inheritance column;
- do the same for each free direction;
- preferably derive `name` from semantic fields rather than storing both independently;
- automatically differentiate the saturated margins along the fully assembled free-plus-pivot direction.

After that repair, this mutation should fail immediately with a descriptor/name mismatch before matrix reconstruction.
