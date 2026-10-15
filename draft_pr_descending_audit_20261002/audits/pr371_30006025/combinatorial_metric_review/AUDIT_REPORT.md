# PR371 independent combinatorial and metric audit

The scoped mathematical claims pass this audit, conditional on the established primary theorems explicitly identified in `MATHEMATICAL_VERDICT.md`. I found no blocking defect in the combinatorial-map/C-decorated-tree, regular-polygon/systole, or intrinsic metric-gluing/sparse-repair arguments. The original Oberwolfach Question 4 remains unanswered by the packet's claimed scope. No historical novelty has been established. Passing finite checks is evidence of implementation consistency and reproducibility, not a proof of the universal assertions or a solution of the source question.

Frozen object: PR371 head `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`, 46 files under `problems/30006025_geometric_chapuy`. All work and outputs for this family are confined to this audit directory. No branch, checkout, commit, push, shared mathematical file edit, or external communication was performed.

## Independence and source fidelity

At 2026-10-03T10:42:07.335115+00:00 I sealed `SOURCE_FIRST_BASELINE.md`, after independently fetching and reading the original OWR printed 2404–2406 contribution and the relevant primary Chapuy, CFF and Janson–Louf definitions. The original printed 2405 Question 4 asks for a “nice geometric adaptation” to construct random surfaces. It does not itself impose exact length preservation, algebraic angles, or a uniquely specified target probability measure. Accordingly, exclusions of those additional conditions cannot exclude every possible answer to the source question. The regular polygon construction is a genuine surface lift but does not supply the claimed controlled random geometry or the WP short-curve law.

The OWR reference to Chapuy is the PTRF 2010 dominant-map paper (arXiv:0804.0546), whose fixed-genus asymptotic must be distinguished from the later exact trisection paper (arXiv:1006.5053). CFF supplies the appropriate all-size exact graph-preserving correspondence; its signs, roots and constant multiplicities matter. Janson–Louf concerns graph cycles and the graph metric at its stated growing-genus scale, not an identified ambient hyperbolic surface metric. These points were established before reading any candidate TURN argument.

I then read every TURN 1–5 argument, independently reconstructed the universal mechanisms, and checked the geometric, probabilistic and transcendence inputs in the primary Izmestiev, Philippe, uniform-dessin, Mirzakhani–Petri, BGL and Delaygue sources. `MATHEMATICAL_VERDICT.md` was sealed at 2026-10-03T10:48:32.357613+00:00, before reading any candidate verifier, check JSON, state, final-result or historical-review file, or any parent/sibling mathematical finding. Both seals remain byte-identical. The source receipts record exact URLs and SHA256 hashes; raw source PDFs, extracted text and renders remain ignored under `private/` and are excluded from publication. The independently downloaded BGL publisher PDF has a dynamic download footer; its byte hash differs from the author's earlier copy, so agreement was checked against the actual mathematical statements rather than assumed from its title.

The detailed sealed verdict is the principal checkable mathematical artifact. Its all-size arguments include the cubic degree counts and CFF weights; an explicit counterexample to arbitrary cyclic splicing; smooth regular-polygon gluing and torsion-free triangle-cover construction; the subgroup systole lower bound and the WP Poisson count discrepancy; the intrinsic cut-disk argument allowing bridges, concave sectors and noninjective development; and the all-E Dirichlet top-k formula and pointwise adaptive-repair bound. It also checks the universal holonomy mechanisms rather than accepting finite matrix computations as their proof.

## Strongest verified result and remaining gap

For a finite cellular embedded one-face graph of total geometric edge length S on a smooth closed curvature −1 genus-g surface, cutting separates boundary occurrences and gives an intrinsic disk with perimeter P=2S and area A=4π(g−1). Izmestiev's inequality gives

    P² ≥ 4πA + A² = 16π²g(g−1).

Thus P=12g is excluded for every integer g≥12, without an angle assumption; genera 2–11 are merely not excluded by this inequality. Necessary relative total length change tends to at least π/3−1. Under the explicitly normalized uniform Dirichlet edge law, every adaptive repair of o(g) edges with uniformly bounded multiplicative stretch has success probability tending to zero, because the changed mass is bounded pointwise by the sum of the k largest coordinates, whose expectation is

    E[T_(E,k)] = (k/E)(1 + H_E − H_k).

These are deductions from credited source theorems and elementary arguments, not empirical rates. They concern the declared embedding/repair class. Unbounded stretch, alterations of curvature/topology, other length normalizations, uncontrolled surface metrics and unrestricted angle choices remain outside the respective exclusions.

For the fixed regular-polygon lift, every output has systole >1 by Philippe's orientation-preserving triangle-group theorem. The short-geodesic count on [1/2,1] is therefore always zero, whereas the normalized WP count converges to a Poisson law with positive mean μ. The resulting limiting one-count total-variation gap is 1−e^(−μ)>3/19, independently of the weighting of the input maps. A different surface lift or suitable deformations remain possible.

The exact unresolved task is a controlled geometric adaptation of the combinatorial correspondence, with an explicit construction and verifiable relationship between the resulting geometry and its intended random-surface law. The original word “nice” is not a formal axiom; this audit does not purport to prove that no such adaptation exists, or to certify that no earlier literature contains one. The packet itself claims obstructions and a limited lift, not a complete answer to Question 4.

## Full code review and replay

All five verifier scripts, both historical review scripts, all 29 input JSON files, and all supporting state/final/history/scope/manifests were read after the mathematical seal. `outputs/INPUT_READ_RECEIPT.json` records every target file's size, SHA256 and Git blob hash and the whole-JSON parse inventory. The full parsed inputs are also retained privately. The replay driver first verifies every snapshot-manifest record against frozen bytes and then works in an ignored private copy; no frozen source file is overwritten.

| Script | What its implementation checks | Limitation |
|---|---|---|
| `verify_turn1.py` | Symbolic trace polynomials through degree 114, powers 1–8, rational Q(√3) matrix arithmetic, all 64 K3,3 rotations, 24 one-face examples and finite genus counts | Rational q examples are not the transcendental algebraic-perimeter barycenter. Hermite–Lindemann and the analytic zero-set argument remain proof inputs. |
| `verify_turn2.py` | 170 rational rotation profiles, full binary expansions on 70 profiles, finite strict maximum-exponent controls and normalization checks | No finite profile palette establishes the all-profile Lindemann–Weierstrass result. |
| `verify_turn3.py` | Genus 2–100 area/index/count controls, 24 clean dessins, rational cosh and Poisson bounds | Reads the TURN1 examples; the driver supplied fresh identical TURN1 output. It neither classifies triangle-group systoles nor simulates a surface distribution. |
| `verify_turn4.py` | Exact Machin-series π bounds, rational threshold certificates, 100 genus controls and 180 rational deformation vectors | The all-embedding intrinsic disk theorem and geometric cutting argument are outside its finite vector checks. |
| `verify_turn5.py` | Exact simplex integrals for E≤32, spacing identities for E≤64, 35 vectors and 1,270 subsets, rational evaluations of probability bounds | Finite identities are supplementary. Adaptation-uniform probability claims require the pointwise proof and all-E formula. |
| Historical `independent_checks.py` | Weighted Laurent expansions, exact rank integrals, tiny exhaustive adaptive budgets and finite geometry constants | Historical checks were read only after the independent seal; they are not a replacement for this family's reconstruction. |
| Historical `verify_review.py` | Review-manifest hashes, final author-manifest hash, stored remote blob records and exact historical independent output | It makes no network request and cannot attest current GitHub/remote state. |

All commands completed with exit code 0 and empty stderr. Every stdout, stderr and complete generated JSON is retained under `outputs/`; no output was sampled or replaced by a summary. The author replay results are:

| Replay | Assertions | Stdout bytes | SHA256, also identical to frozen check JSON |
|---|---:|---:|---|
| TURN1 | 467 | 9,361 | `f392a31ef3ab7e41cf26f754cd1549d4ffecce18fdc03bfbbc2322f84732c283` |
| TURN2 | 1,004 | 913 | `b380b417cb9bcb85b93d6cfe5dc31f24d17eddd1c0f9455648baa3646de0376c` |
| TURN3 | 961 | 1,349 | `73b618495d8c43e0446473e594f475a72065fa89fbd27ad3bfa3ebe39f245b19` |
| TURN4 | 1,136 | 475 | `b72cd36c81ac2936bc6d2e7e1f3d780ae1b5b796c984d571b27229a37eaef4b0` |
| TURN5 | 12,050 | 1,641 | `0c4833d70f58d121d8395b9e8a078f8b0bc265965900f4dab6cb3674b4b39193` |

Total: 15,618 author assertions. The replay ran from 2026-10-03T10:53:26.998700+00:00 through 2026-10-03T10:53:34.478406+00:00. The historical independent output also reproduces exactly: 24,692 assertions, 770 bytes, SHA256 `a9c746845012c73df2c8a92e452a2710af1207a95ce95dd1e6b2f9c51d674ed0`. The historical review verifier produced its complete 78-byte PASS message. `outputs/AUTHOR_REPLAY_RECEIPT.json` supplies each argv, private working directory, UTC interval, exit code, stream lengths and hashes. All private author files remain byte-identical to the frozen inputs after replay.

The initial system and bundled Python probes lacked SymPy. A private SymPy installation then failed for disk space while creating `bin/isympy`; a redirected retry did not execute because its output files could not be allocated. Complete available probe/install streams are preserved, including the installation error. After validating an existing parent-supplied runtime, only this audit's own failed ignored environment was removed. Successful replays used Python 3.14.6 and SymPy 1.14.0 read-only with bytecode writing disabled. `outputs/DEPENDENCY_RESOLUTION.json` records this resolution and `runtime_validation.stdout` records the actual versions. This environmental failure was not a verifier or mathematical failure.

## Independent falsification controls

`independent_controls.py` implements separate finite checks using the standard library. Its whole output and receipt are public. It does not import or invoke an author verifier. The controls passed 931,906 assertions; most are routine cycle-closure validations, so that count is not a measure of mathematical strength.

The complete rooted one-face pairing enumeration through seven edges contains 146,599 pairings. The totals for n=1,…,7 are 1, 3, 15, 105, 945, 10,395 and 135,135. For every pairing, the code verifies the Euler genus, 2g trisections in the independently chosen face-order convention, and exactly two boundary copies of each edge. It independently matches Catalan planar counts and 19 signed odd-cycle CFF cardinality comparisons. These finite cardinalities cannot supply the full graph-preserving CFF bijection; that is a primary credited theorem.

An independently constructed cubic genus-two one-face map has six vertices, nine edges and a separating bridge with darts (12,13). Its complete involution, rotations and face word appear in `outputs/independent_controls.json`. Positive rational lengths sum to 45/7 and its face perimeter is 90/7. The deliberately incorrect one-copy perimeter rule is rejected. This exercises a boundary case absent from the K3,3 examples.

The code also checks the explicit two-loop rotation counterexample from the sealed verdict: the same vertex-identification graph can have one or three faces according to the chosen cyclic splice. This falsifies a naive alternative, not the candidate's reliance on established CFF. Finally, independent exact simplex-volume integrals for E≤40 verify 860 top-k cases including k=0 and k=E, and all 510 subset choices across E≤8 verify adaptive domination, decreases, and the impossibility of a positive increase under cap C=1. These are meaningful controls for hidden convention errors; the universal probability theorem remains justified by the sealed analytic deduction.

## Status and publication records

The final author manifest has 36 entries; publication manifest 45; historical review manifest 6; historical remote-binding record 37; and TURN manifests 7,5,5,5,4. All 150 entries pass their recorded size/hash tests, including the previous-turn manifest chain. `outputs/MANIFEST_CHECKS.json` retains every checked row. Counts overlap and must not be interpreted as 150 distinct files.

The historical state percentages 8,10,12,16,18 and the final 5/5 research-turn budget consumption describe progress/budget, not a completed source problem. Earlier pending-review artifacts are historical inputs; the additive `REVIEWED_RESULT.md` wrapper records the subsequent scoped review. I found no contradiction requiring a status correction. The appropriate conclusion remains scoped claims accepted, original question unresolved, no full-source solution or historical novelty certification. The stored older author-head binding does not replace the present frozen head receipt.

`PUBLIC_MANIFEST.json` is an explicit allowlist of literal paths relative to this audit root, with bytes and SHA256 for every owned public file except itself. It excludes all raw sources, renders, private input copies, temporary environments and bytecode. `verify_public_manifest.py` verifies that allowlist, the two immutable seals, replay stream receipts and the present frozen input hashes. The research log records UTC checkpoints and completion estimates for this audit; 100% audit completion does not assert completion of Question 4.

For reproduction, `run_author_replays.py --python <Python-with-SymPy>` requires a fresh absent `private/author_replay` destination and the frozen sibling snapshot/manifest. `independent_controls.py` requires only Python's standard library. The original replay environment's available working runtime path is recorded in its receipt; no new dependency installation is necessary to inspect the full preserved outputs. No publication action is taken by this subagent; the parent owns any authorized final release decision.
