# Fresh v1.2.6 code, certificate, and reproducibility audit

Timestamp: 2026-08-27T08:55:45-07:00  
Auditor lane: independent code/certificate/reproducibility review  
Packet: `k2p-k3p-theta-ai-referee-v1.2.6`

## Outcome

I found no operative code, certificate, schema, integrity, provenance, or
reproducibility defect. The v1.2.6 assurance claims are accurate within their
expressly stated limits. My recommendation from this audit lane is **accept**.

I first read the entire 20-page main manuscript and visually inspected every
rendered page. Only afterward did I open the supporting notes, certificates,
verifiers, stored transcripts, packet prompts, or coverage inventory. I then
read and visually inspected both pages of each supporting PDF. All 24 supplied
pages were clean, legible, and free of clipping, overlap, missing glyphs, or
broken figures/tables.

## Provenance and integrity

- ZIP SHA-256:
  `f35d5b8ef06870444b20c6572c9676155aacc9d2df214889706f48c9bb07c150`.
- The ZIP has 48 entries: 44 regular files and 4 directories. I found no
  symbolic-link or unsafe-path archive entry.
- `PACKET_SHA256SUMS` verified all 43 listed files before the replay, after the
  replay, and after my independent tests. The driver also enforces the exact
  directory set and rejects nonregular entries.
- The declared annotated tag `k2p-k3p-theta-v1.2.6` peels locally to the
  declared commit `672d96a08be174cd6b67762a6907dfbdcd926b9b`.
- A fresh `git archive` of the tagged canonical subtree was compared to the
  packet. Every one of the 38 common `materials/` files was byte-identical.
  The only tagged-subtree-only paths were the package's deliberately excluded
  repository/release/log/submission files.
- The annotated tag has no cryptographic signature. The internal manifest and
  tag therefore establish reproducible internal identity, not externally
  authenticated authorship. The packet states this limitation accurately.
- No verifier performs network access. Mathematical code uses only Python's
  standard library. Subprocess use is confined to the local replay and hostile
  test orchestration.

## Full replay

On Python 3.14.6, the following clean packet replay passed:

`bash ./RUN_REFEREE_REPLAY.sh --with-pdf`

This established all of the following in disposable working copies:

- complete exact suite, normal mode;
- complete exact suite with Python optimization enabled;
- focused strict-JSON/closed-schema suite, normal and optimized;
- focused compact K2P, graph-derived displayed-tree, source-convention, and
  four-leaf graft checks, including the optimized four-leaf check;
- all individual K2P/K3P supporting entry points;
- byte-identical regeneration of the compact K2P certificate;
- rebuild of all three PDFs and exact equality of their extracted text;
- manifest/path-set verification both before and after execution.

The run ended with `ALL REFEREE REPLAY CHECKS PASSED`. The supplied suite has
25 distinct negative mutations (14 raw/schema, 1 compact-K2P semantic, and 10
K3P semantic). Because the packet driver repeats them through complete normal
and optimized runs, focused schema runs, and individual entry points, it
executed 89 negative-test cases in total; every one failed for its expected
reason. There are no operative Python `assert` statements whose removal under
optimization could bypass verification.

## Computational-claim map

| Manuscript claim family | Executable reconstruction | Audit assessment |
|---|---|---|
| Compact K2P field, topology, admissibility, all stored transition rows, core factorization, all 64 Fourier coordinates, all 64 positive patterns, normalization, minimum, and `Q=0` | `verify_k2p_simple.py` | Fully consumed and checked with exact arithmetic in `Q(sqrt(71))`. |
| Literal four retained K2P graphs, descendant labels, source convention, direct ordinary-state pruning, and comparison with Fourier inversion/tree | `verify_k2p_displayed_trees.py`; `src/verify_source_conventions.py` | The retained graphs, not supplied monomials, generate the Fourier terms. Direct pruning separately reaches all 64 probabilities. |
| Continuous-time K2P number field, isolating intervals, topology, admissibility, factorization, collision, 64 patterns, direct pruning, fixed-order sign failure, and six-order negative point | `src/verify_k2p_extended.py` | Exact six-dimensional field arithmetic and Sturm/root-isolation checks are operative; all finite claims replay. |
| K2P rank-9 minors, tree rank 6, dimensions/fibers, and six-dimensional symmetric collision family | `src/verify_k2p_rank_family.py` | Selected derivatives and determinants are reconstructed, not merely read. The dimension arithmetic is consistent with the proved submersion facts. |
| One four-leaf graft instance in all 256 Fourier and ordinary-state coordinates | `src/verify_k2p_four_leaf_graft.py` | Exact literal-network, tree, Fourier, pruning, and kernel-extension calculations agree. The code correctly labels this a regression, not a proof for arbitrary `n`. |
| K3P quartic field, canonical rooted/suppressed topology, vectors and rows, ansatz, four displayed graphs, collision, 64 coordinates/patterns, direct pruning, K2P-symmetry distinction | `src/verify_k3p.py` | Reconstructed exactly and cross-bound to canonical graph semantics. |
| K3P rank-15 determinant, tree rank 9, dimensions/fibers, and dominance input | `src/verify_k3p.py` | The 225 Jacobian entries are differentiated from the executable map and the determinant is recomputed in `Q(h)`. |
| K3P IFT fixed-output tangent and the two formerly saturated continuous-time margins | `src/verify_k3p.py` | Free and pivot descriptors are canonical, `J p' + F_UC + F_VG = 0` is checked row by row, and margin derivatives are independently differentiated and proved positive. |
| Closed JSON parsing, mutation guards, orchestration, regeneration, integrity, and PDF reproducibility | `strict_json.py`; `src/test_*mutations.py`; `verify.py`; `RUN_REFEREE_REPLAY.sh` | Fail-closed for the present packet schemas; all advertised modes and boundaries passed. |

The analytic local-section, implicit-function, constant-rank, Zariski-density,
and universal grafting conclusions appropriately combine these finite
certificates with proofs in the manuscript. The packet does not misdescribe a
finite regression as a computational proof of those general theorems.

## Independent hostile tests

I wrote `notes/code_mutation_harness.py`; it works only in fresh temporary
copies and never edits packet files. Its final result was:

`OPERATIVE/INTEGRITY MUTATIONS REJECTED: 81`  
`DECLARED-INFORMATIONAL VALUE MUTATIONS ACCEPTED: 3`

The 81 rejected mutations break down as follows.

### Strict loader and closed schemas: 19 rejections

- duplicate top-level raw key in each of all five JSON certificate types: 5;
- duplicate key inside a nested object/array record in each of all five: 5;
- unknown top-level field in each of all five: 5;
- `NaN`, `Infinity`, and `-Infinity`: 3;
- valid-JSON huge exponent `1e999`: 1.

The nonstandard constants are rejected during parsing. `1e999` becomes a
different primitive shape and is rejected by the present closed schema. No
canonical v1.2.6 certificate contains a floating-point JSON value.

### Compact K2P semantics and independence: 12 rejections

- each of the six network/effective transition rows (`K`, `K_odot_K`, `U`,
  `V`, `S`, `T`): 6;
- each of the three comparison-tree rows (`alpha`, `beta`, `gamma`): 3;
- rooted endpoint: 1;
- inheritance probability: 1;
- direct-pruning source changed from Klein XOR to cyclic addition while the
  Fourier calculation remained unchanged: 1.

Thus every stored compact-K2P transition row is demonstrably live. The
ordinary-state check is also capable of falsifying a wrong state-group law.

### K3P semantic binding and independence: 45 rejections

- parent endpoint on each of the ten canonical arcs: 10;
- parent and choice contradiction for each of four reticulation incoming-edge
  descriptors: 8;
- duplicate vertex identifier without changing array length: 1;
- transition rows for all six named parameter vectors: 6;
- all three comparison-tree transition rows: 3;
- all nine effective root-suppressed transition rows: 9;
- stored Jacobian matrix, stored determinant, coordinated
  descriptor/matrix/pivot swap, pivot tangent, and free descriptor: 5;
- stored Fourier coordinate and stored ordinary pattern probability: 2;
- K3P direct-pruning source changed from XOR to cyclic addition: 1.

For the Jacobian/tangent attacks, both embedded sections and their sidecars
were changed together. Those cases therefore reached and failed the semantic
binding rather than merely failing the mirror comparison.

### Packet boundary: 5 rejections

- changed byte;
- added file;
- removed file;
- substituted symbolic link;
- added directory.

Every case failed at the initial integrity boundary, before mathematical code
ran.

### Deliberately informational values: 3 expected passes

I made same-shape changes to the K3P title, one ansatz-form display string, and
the Jacobian number-field display string (synchronizing the sidecar for the
latter). All three still passed, as they should: the coverage inventory labels
them informational, while the underlying field, ansatz, and Jacobian
mathematics are independently reconstructed. This supports rather than weakens
the inventory's distinction between semantic and structural coverage.

## Schema and coverage assessment

`strict_json.py` supplies a unique parse by rejecting duplicate keys at every
depth and nonstandard JSON constants. Its packet-specific shape fingerprint
binds object-key names, nesting, primitive types, list lengths, and the
multiset of element shapes. It intentionally does not hash values or list
order. Operative ordered arrays are separately bound in the mathematical
verifiers: most notably the K3P vertex, ten-arc, reticulation, Jacobian-column,
row, and tangent descriptor orders. Fields whose values are not semantically
used remain structurally closed and are accurately called informational.

I found the coverage inventory accurate for the audited claims. In particular:

- all five certificate inputs use the strict loader;
- the two K3P sidecars use it independently and must exactly equal the
  embedded sections;
- the K3P top-level, vertex, arc, reticulation, Jacobian, and tangent semantics
  are hard-bound;
- every compact-K2P stored transition row is consumed;
- transcript and sidecar comparisons are correctly described as consistency
  checks, not independent mathematics;
- manifest integrity is correctly distinguished from authentication.

## Nonblocking hardening observations

1. The supplied compact-K2P mutation script targets only `K_odot_K`, although
   the verifier consumes all nine rows. Expanding the maintained regression to
   corrupt every row would make the test suite itself document that fact. My
   independent nine-row attack already confirms current behavior.
2. For future schemas that might admit JSON floating-point values, consider a
   finite `parse_float` policy (for example `Decimal` plus an explicit finite
   check). The present schemas contain no floats, so valid `1e999` fails by
   type/shape and this is not a v1.2.6 defect.
3. PDF tagging remains absent. The pages are visually clean and readable, so
   this is an optional accessibility improvement, not a correctness or
   submission blocker.
4. A signed release tag or detached external checksum could add external
   authentication. The current unsigned status is already disclosed and does
   not affect internal reproducibility.

## Final code-lane recommendation

No correction is required by this audit. The repaired strict parser, closed
packet schemas, semantic bindings, direct-pruning checks, determinant/tangent
coupling, integrity boundary, and provenance statements all survived fresh
adversarial testing.

**ACCEPT**
