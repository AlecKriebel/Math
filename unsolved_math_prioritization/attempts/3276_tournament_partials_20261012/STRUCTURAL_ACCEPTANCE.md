Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Independent acceptance of the recovered structural partial

Date: 12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808.

## Decision and exact bytes

**ACCEPT the structural partial only. The unrestricted conjecture remains unresolved.**

The accepted author packet is `the original source packet`:

- Manifest: [verified original byte count omitted], SHA-256 `[verified undistributed artifact identity]`.
- Mathematical text `STRUCTURAL_PROOFS.md`: [verified original byte count omitted], SHA-256 `[verified undistributed artifact identity]`.
- All 13 manifested payloads were checked against this external pin before and after replay. The author packet is unchanged by this audit.

This is a fresh recovery edition. A workspace rollback removed the earlier local structural packets and unfinished audit. Those historical hashes are not treated as current byte verification. The same mathematical content has been independently reread, checked, and bound to these new bytes. This is not an additional substantive research pass or a claim of historical text preservation.

## Accepted mathematical scope

The precise target is the outgoing formulation for nonempty finite tournaments with at most three arc colors: a directed cyclic rainbow triangle or a vertex reaching every other vertex monochromatically, with the path color allowed to vary by destination.

1. The source-derived forced graph has a predecessor path exactly when it has either a forward monochromatic run of length n-1, or an odd-order backward-two-step run of length (n+1)/2 whose incident pairs use the two other colors. The proof handles cyclic indices, parity, repeated colors, walk-to-path composition, and the overlapping generator descriptions at n=3.
2. Every genuine three-color cycle word survives this relaxation. Even strict two-color alternation also survives, although it is already excluded by a stronger source proposition. These are express limitations, not counterexample constructions.
3. For an odd binary word, avoiding third-color predecessor reachability is equivalent to every gap between nonswitches in step-minus-two cyclic order being at most (n+1)/2. A surviving odd binary obstruction cycle has at least three nonswitches. The full binary criterion also requires at least two occurrences of each used color. Gap equality is allowed; three nonswitches alone are insufficient.
4. The incidence-deletion process has a unique largest stable terminal core, independent of deletion order. Credited source conditions keep every induced-minimal counterexample inside that core. A nonempty rainbow-cycle-free tournament with empty core therefore satisfies the target. More generally, if the target is known for every order at most b, core size at most b suffices.

The core-size-eight application is accepted as this conditional implication. Its finite premise requires the separate accepted computer-assisted tournament bound; this audit does not itself perform that search. The prior finite acceptance was read before the rollback, but its then-local artifact bytes were subsequently unavailable. No fresh finite-certificate verification is inferred from that historical reading, and no general order-nine result is asserted here.

`STRUCTURAL_PROOF_REVIEW.md` supplies the independent mathematical analysis. It explicitly distinguishes direct tournament arcs from forced monochromatic reachability, excludes self-pairs from the auxiliary graph, requires nonempty T for a universal-source conclusion, and says that a retained stable vertex satisfies all retention requirements and cannot be deleted. It does not assume an arbitrary stable superset is stable or that a source of the core extends to the whole tournament.

## Credit and dependencies

The distinguished Hamilton-cycle reduction is Shen's, as reproved in Lemma 2.1 of Georgakopoulos and Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2). Its Lemma 2.7 supplies the switch rule; Proposition 2.8 already excludes even strict binary alternation. Proposition 2.4 and Theorem 3.1 supply the incidence-core conditions. The present audit verifies the deductions and reconstructed reduction/switch proofs; it does not certify the entire source proof of Theorem 3.1. The recovery author's source note reports reinspection of those same public statements. No copied source text, source PDF, dataset content, or private coordination material is included in this audit. No novelty, priority, or exhaustive literature-status certification is made.

## Fresh independent verification

Every check below was run on the new audit code under ordinary Python, -O, and -OO. Results agree after removing their optimization indicator; all guards are explicit exceptions.

- All 29,511 raw words of lengths 3 through 9: independent set/BFS and Boolean-matrix closures agree, and exact start/color predecessor-failure sets agree with the pure-step characterization.
- All 43,688 binary words of odd lengths 3 through 15: third-color reachability agrees with cyclic gap bounds, repetition parity, and one-repetition exclusions.
- Core/lattice tests on 801 deterministic sampled tournaments of orders 1 through 9: three deletion schedules agree with the union of all stable subsets; 102,002 subsets are examined.
- Six graph mutations are detected: forcing repetitions, reversing switch direction, reusing an incident color, omitting the wrap switch, merging colors, and targeting the successor. Two gap-boundary mutations, ten invalid word/gap inputs, two incorrect core predicates, invalid tournament inputs, and the false stable-superset claim are also rejected.
- The final author's two checkers were freshly replayed in all three optimization modes. Their exact outputs match the frozen receipts: 88,560 ternary words through length 10, sharpness families through odd length 101, 111 core fixtures with exhaustive deletion schedules/stable subsets, and the stated malformed-input controls. This entire six-run replay was itself executed in all three auditor optimization modes.
- Five copied-packet integrity mutations are rejected: altered proof, altered result, missing file, added file, and a self-consistently rehashed but externally unpinned manifest.

The independent raw-word scope is through nine; through-ten replay uses inspected author code. The core samples need not be cyclic-rainbow-free and do not certify source existence. No tournament-completion enumeration or proof-assistant certification is claimed by this audit.

## Reproduction and frontier

Run the original normal-mode audit/replay operation, the original optimized-mode audit/replay operation, and the original optimized-mode audit/replay operation. Run `the original checker` in the same modes to pin and replay the recovered author packet. the original externally pinned audit integrity and hostile-control check checks this audit's sealed bytes, receipts, and scope; it does not replay searches.

The unrestricted target, general genuinely three-color obstruction cycles, realization of surviving binary words, and any finite claims beyond the separate accepted bound remain outside this result. No repository, queue, or publication state was changed.
