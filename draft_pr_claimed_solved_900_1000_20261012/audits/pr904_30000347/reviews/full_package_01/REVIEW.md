# Complete publication-package adversarial review 01: PR 904 / problem 30000347

Checkpoint: **2026-10-13 03:40 UTC / 2026-10-12 20:40 PDT**.
Review completion estimate: **100% of this assigned package review**. This is not
an estimate of completion of the wider PR shard, publication workflow, or a
determination of historical novelty.

**Verdict: PASS within the precise stated mathematical and publication scope.
No required repair or counterexample found.** The note proves the historical
undirected triangle BSP classification, including its stated restrictions and
two optional strengthened variants. The frozen PDF, supporting archive,
documented reproduction entrypoint and local Zenodo manifest are consistent.
First priority and continued open status through 2026 remain unestablished;
the manuscript and metadata explicitly avoid asserting them.

## Independence and scope

I am a new reviewer relative to the original proof, computation, source-model
and priority reviewers. However, this review **inherited parent conversation
context, including prior audit summaries**, so it is not a clean-context or
strictly independent review. I reconstructed the two mathematical identities
and the backup argument from the candidate note and wrote fresh executable
checks before reading the archived reviewer conclusions or their mathematical
code. Those later reports were consulted as additional adversarial leads,
not treated as proof. The parent has indicated it will obtain a subsequent
review initialized without conversation history.

Writes were confined to this `full_package_01` directory. Extraction, deliberate
mutations, regenerated manuscript PDF, downloaded primary-source PDFs and page
images are under ignored `tmp/`. No frozen, original, publication, queue,
shared or Git state was changed. No external communication, merge, close,
stage, publication or sheet append was performed. This is an AI-agent review,
not independent human peer review.

## Exact reviewed candidate

The freeze manifest itself has SHA-256
`c8587791749d5f599d034666e932936d378d51c916a58733858bd7241d039ff7`.
It identifies original PR head
`d67d11bcb7d1e730daf9be7555c75950d3484b5d`.
All listed byte counts and hashes were checked initially and again at the final
checkpoint. The candidate remained unchanged.

| Publication-relative file | Bytes | SHA-256 |
| --- | ---: | --- |
| `note.tex` | 12462 | `908e36fec4c1b73088b2ed960877efd703f87d9ef57e5addb00233131953de3e` |
| `output/pdf/note.pdf` | 54431 | `0f6fc15b270e178cec67ff98f09f1f7f7f09d34f4926ea568266bb8dab35b3a2` |
| `three-terminal-bsp-source-verification-v1.0.zip` | 117514 | `3d7abfbf721702550dfdfacaefb57ef3c0eb4ce4e4ec8fcd3e5b8082143632e8` |
| `zenodo-deposit.json` | 3720 | `a5dc16d3e64a78352670d1e52b8ff4b67891da0358e688a9d826a69395c64ce3` |
| `README.md` | 3746 | `142a2d9db0c6c84359d6dac3447ec98906f5746181bcde904b82b2792684a02a` |
| `verify_package.py` | 4223 | `5d015a7d7e75fabc58661c5cb33a77fd4847d2e33a4975c55f847d4e84d506a7` |
| `tmp/bundle/PACKAGE_MANIFEST.json` | 8616 | `01815bd240506cf2eb04ca4dfcddb27482fc166a4aead8131045554cca21ad57` |

The manuscript, README and verifier inside the ZIP are byte-identical to their
publication copies. The separate-PDF manifest points to the reviewed PDF with
the same byte count and digest. The original proof anchor is
`f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7`.

## Reconstructed mathematics and adversarial checks

The decision input is a finite simple undirected graph with unit traversal
lengths, three distinct initially connected terminals, and a nonnegative
binary integer budget. All three unordered pairs are demands. All edges are
eligible for unit-cost deletion. A residual infinite distance satisfies the
at-least-one increase requirement. The positive rational-cost extension changes
deletion costs, not traversal lengths.

### Subdivision identity

For each source edge uv, insert fresh b,c and replace uv by u-b-c-v. The supplied
parts are the original vertices, all b vertices and all c vertices. Every
gadget gives one edge of each cross-part type; distinct gadgets never share
their internal vertices. A source vertex cover extends using one internal
vertex per gadget. If only u is selected, c is the correct choice; if only v
is selected, b is correct. This gives tau(H) <= m+tau(Q).

For an arbitrary H-cover X, put S=X intersect V(Q). Each gadget needs an
internal cover vertex. Each source edge whose two endpoints are outside S
needs both internal vertices. If there are q such edges, then
|X| >= |S|+m+q. Adding one endpoint per such source edge yields an actual
Q-cover of size at most |S|+q <= |X|-m. Duplicate added endpoints only improve
the inequality. Thus tau(H)=m+tau(Q), without assuming S was already a cover,
that X was optimal, or that Q was connected or had no isolates.

### Spoke identity

The three terminal neighborhoods are disjoint, and terminals are nonadjacent.
No terminal path of length 1 or 2 exists. Each cross-part edge uv gives one
terminal geodesic a-u-v-b of length 3. Conversely, any three-edge terminal path
has exactly this form: its two internal vertices must lie in the endpoint
terminals' parts and be joined by an H-edge. No third terminal can occur within
such a path. These are all original geodesics for all three demands.

Deleting the spokes indexed by an H-cover hits every geodesic. For the reverse
direction, any feasible deletion set F contributes the H-endpoint of each
deleted spoke and an arbitrary endpoint of each deleted middle edge. Every
H-edge's geodesic is hit, so its edge is covered by these contributions. The
union has size at most |F|. This handles unrestricted middle-edge deletion,
mixed deletions, repeated endpoint charges and nonoptimal blockers. Therefore
opt(G_H)=tau(H). Longer residual routes do not matter: deleting edges cannot
create a shorter route, and feasibility refers to the original geodesics.

### Reduction, encoding and boundary cases

For m>0, budget B=m+k gives tau(Q)<=k iff opt(G_H)<=B. The exact construction
counts are n+2m+3 vertices and n+5m edges. Its size is independent of the
magnitude of binary k. The three cross-part types exist even for a source
graph consisting of one edge, so initial terminal distances are 3. Isolates
produce harmless spokes. An edgeless source instance with k>=0 is mapped to
the concrete H-triangle/spoke yes-instance with budget 2. Negative source
budgets are outside the specified source language. Zero, insufficient, exact,
oversized and very large budgets do not require extra gadgets.

An edge-list certificate needs only polynomial size. Validate the edge list,
sum its costs, and run three original and three residual BFS computations.
For binary rational costs, a common denominator can have bit length at most
the sum of input denominator bit lengths; exact sums and comparisons are
polynomial in input length. Unit-cost instances provide hardness for this
extension. An exact optimizer would decide the budget language. No weighted
cover identity or P!=NP assumption is used.

### Finite and exact 3-to-4 variants

Each fresh backup chain has four edges and three internal degree-two vertices,
disjoint from all other backup interiors and the original graph. A simple
terminal path using a backup internal vertex must traverse its whole chain.
It has length at least 4, including when it subsequently visits the third
terminal. Thus the length-three geodesic family is unchanged.

Any augmented blocker still hits each old geodesic with an old edge; ignoring
its backup deletions yields the same no-larger H-cover. Conversely, deleting
cover spokes preserves every backup chain and removes every old length-three
path. All terminal distances are both at least and at most 4. Hence the
finite-terminal and exact-distance optima both equal tau(H). The note expressly
avoids claiming that every residual nonterminal vertex remains connected.

### New computational evidence

`independent_full_checks.py` imports no submitted mathematical code. It uses
its own BFS, cover enumeration and deletion masks, with explicit guards that
remain active under optimization. Ordinary and optimized runs both passed:

| Fresh check | Count |
| --- | ---: |
| Every labelled simple source graph of orders 0 through 4; subdivision cover optima | 76 |
| Eligible tripartite graphs of part sizes (1,1,1), (1,1,2), (1,2,2) | 145 |
| Arbitrary original-edge deletion subsets | 165952 |
| Feasible deletion subsets, each checked for no-larger cover extraction | 89975 |
| Arbitrary augmented-edge deletion subsets through the exact optimum for the smaller partitions | 2012 |

Original deletion masks are exhaustively tested against the full geodesic family;
BFS independently cross-checks all masks for at most four H-vertices, and all
masks of size at most tau(H)+1 for the five-vertex partition. Backup tests use
BFS on every subset through tau(H), including backup-edge deletions, and find
both strengthened optima. Budgets include a 1001-bit integer. A deliberate
omission of the third demand allows a one-spoke solution for H=K3 while tau=2;
the fresh test detects the resulting invalid extension. This is a meaningful
negative control, not merely a repeated positive example. These finite checks
support the universal argument above; they do not replace it.

## Historical target, attribution and priority language

I independently opened the [publisher's Krause contribution](https://ems.press/content/serial-article-files/46024?nt=1)
and the [institutional dissertation mirror](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf).
The report's printed pp. 2856-2858 use unit traversal lengths, arbitrary edge
deletion costs and precisely all three terminal pairs. The undirected triangle
case is explicitly unclassified there; directed triangle hardness is separate.
The dissertation defines unavailable distance as infinity and regards ordinary
multicut solutions as BSP solutions. Its Section 4.3 leaves the undirected
triangle case unresolved. These sources support the exact historical question
and the paper's disconnection convention, rather than a stronger connectivity
or restricted-graph problem.

I freshly downloaded and visually checked [Karp's printed p. 94](https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf),
where the Main Theorem includes Node Cover. I also visually checked
[Poljak's printed p. 308](https://dml.cz/handle/10338.dmlcz/105554),
which states the two-subdivision stable-set identity. Taking complements gives
exactly the first cover identity in this note. Its attribution is correct.
[Khachiyan and coauthors' Section 6, printed pp. 226-227](https://link.springer.com/content/pdf/10.1007/s00224-007-9025-6.pdf)
was independently inspected, including its figure. It attaches three parts
to three vertices on a terminal path, uses protected vertices, vertex deletion,
one demand and zero/one lengths. The candidate accurately credits this closely
related mechanism while explaining the unit-length, three-demand and
unrestricted edge-deletion change.

My additional current searches used exact BSP/triangle names and three-terminal
shortest-path and bounded-multicut terms. No exact preceding theorem was located
in those results. I then read the archived bounded priority audit, including
its precise comparisons and access gaps. Its older arbitrary-threshold,
directed, vertex-deletion, shielding and full-disconnection results do not by
themselves imply hardness for original distance-three undirected triangle
geodesics. That distinction agrees with the polynomial single-pair original
shortest-path blocker case. No unsupported priority inference is needed in
the proof.

This review does not independently exclude every later theorem or inaccessible
paper. In particular, the archived audit reports inaccessible original
Bienstock-Diaz full text and final Dvorak-Knop journal text, sparse citation
indexes and other access gaps. Those are limitations of a novelty claim. The
note, README and metadata instead state a historical classification and
explicitly disclaim first priority, continued open status through 2026 and
exhaustiveness. That framing is justified. It must be preserved in the final
public record and acceptance language; a claim of a newly solved problem still
open in 2026 would go beyond this review.

## PDF and manuscript readiness

All **four released PDF pages** were rendered at 110 dpi and visually inspected.
The title, author and ORCID are legible; equations, lemmas, proof endings,
section transitions, references and page numbers are intact. No clipped text,
overlap, missing glyph, broken reference, placeholder or visual repair was
found. Splitting the spoke proof across pages does not obscure the argument.
PDF metadata reports the matching title and author, four letter-size pages,
no encryption, no form and no JavaScript.

I compiled the extracted standalone `note.tex` using the documented Tectonic
command in a private output directory. Compilation succeeded without reported
warnings. The rebuilt PDF has 54431 bytes and exactly the same layout-preserving
extracted text as the reviewed release. Its digest differs, consistently with
the README's warning about PDF production timestamps. The frozen release's
identity, not byte-identical recompilation, is the optional PDF integrity gate.

The note expressly discloses extensive AI use for construction, verification,
adversarial review and writing; AI-agent review is distinguished from human
review. The title page says unrefereed, and the body explicitly says there has
been no independent human or journal peer review. Author name, affiliation,
ORCID `0009-0001-9320-500X`, version 1.0 and 12 October 2026 agree across the
PDF, manuscript, README and proposed Zenodo metadata.

## Archive, reproducibility and failure controls

The ZIP contains **48 regular members: the manifest and 47 payload files**.
I rejected duplicate names, absolute/traversal/noncanonical paths, symlinks,
nonregular types, encryption and oversized entries before extracting. Every
member's size and digest matches its package manifest. The nested original
`AUTHOR_FREEZE.tar.gz` contains only the seven authored frozen packet files;
its members are safe regular files and match their frozen counterparts.
`integrity_and_listing.json` records the exact inventory.

The 47 text members were UTF-8-readable; the only binary member is the authored
nested tar archive. The inventory and authored prose were examined for copied
primary PDFs/images, raw catalogue exports, credentials and private account
payloads. None was found. Secret-pattern screening also produced no flags.
The source descriptions are authored paraphrases and retrieval metadata, not
redistributed primary texts. Public hashes do not reveal the private PDFs.

The supported entrypoint was run from a clean private extraction with the
separate frozen PDF, in both ordinary and optimized outer modes. Both exited
zero and verified the PDF, all 47 payload files, five suite entrypoints,
the original three mathematical suites and all 100 original integrity mutations.
Afterward every distributed payload remained byte-identical. Replays use
disposable copies, so the historical results and anchors are preserved.

The verifier and child-code imports were inspected. The supported pipeline
uses only standard-library modules and local processes, with no networking,
credential lookup, shell execution or unsafe archive extraction. Its exact
child command uses `-I` and no `-O`; outer optimization is therefore not
inherited by the mathematical child. Direct optimized historical raw-checker
execution can erase assertions, as the package itself discloses. That command
is not a supported reproduction instruction.

`outer_gate_failure_controls.py` added **18 fresh rejected controls** across
both outer modes with `PYTHONOPTIMIZE=2`: changed manuscript, missing audit,
extra payload, byte-identical symlink, malformed manifest, wrong problem
identity, coordinated proof/outer-manifest rewrite, wrong separate PDF and
injected child mathematical assertion failure. For the last control, I updated
the outer payload digest deliberately so only actual child execution would
detect the failure. Both modes failed with the assertion sentinel, directly
testing the optimization boundary. All mutations occurred only in private
copies.

The archive's consistency protection assumes trusted manifests and verifier
anchors. A fully coordinated replacement of the distributed trust boundary
is outside that guarantee. The README makes this limitation clear, so it does
not claim authenticity or proof-assistant certification from hashes.

## Proposed Zenodo package

The local read-only deposit-tool `check` command passed. It resolved exactly
the reviewed PDF and ZIP to the intended public filenames with the frozen
sizes and hashes. Its manifest matches the note's theorem, optional variants,
unit lengths/costs, author, ORCID, date, version, unrefereed/AI disclosure,
classical credits and priority limitations. It uses publication/preprint,
English, open access and CC BY 4.0, consistent with the README's authored-work
license and exclusion of external reference redistribution. The related
identifiers link the correct PR and historical/methodological references.

No remote staging or schema acceptance was tested by this review. The parent
must verify exact remote metadata, files, submission state and DOI using the
repository tool when it performs the already-authorized publication. That is
a remaining publication operation, not an identified defect in this candidate.

## Required repairs and limits

**Required repairs: none found.** No optional cosmetic change is proposed.
The strongest verified result is the complete deductive restricted
NP-completeness theorem and its finite/exact strengthening, accompanied by
reproducible finite checks and a consistent submission package.

This verdict is hash-bound to the candidate above. It is not a determination
of first priority, an assertion that the problem remained open until 2026,
independent human peer review, formal proof-assistant certification, a complete
privacy/security proof, remote Zenodo acceptance or a completed publication.
Strict review independence is additionally limited by inherited parent
context. A subsequent clean-context reviewer is appropriate before final
promotion, as the parent already plans.
