# Independent exact reproduction and falsification report

Audit completion: 100% of this assigned finite-reproduction/adversarial family. This is not a percentage proof of the unqualified source conjecture. Original effort remains unknown/5 (interrupted). No original independent_review, sibling report, or root scientific verdict was read. Root coordination messages were received after the protected initial source-only seal. No Git/index/ref/checkout operation, installation, source modification, external communication or remote mutation was performed.

## Verdict and precise scope

The original finite computations reproduce correctly with ordinary Python: the literal 16-face path is a legal vertex-to-first-vertex geodesic at graph distance two, of squared edge-unit length (307+137 sqrt(5))/2. All 15 crossing pairs agree with a materially different exact implementation. Every edge-axis half-turn has vertex-distance histogram {1:4,3:8,4:4,5:4}; there are 30 edge occurrences but 15 distinct axes. The mathematical graph argument excluding distance-two pairs under such a half-turn is sound.

The submitted universal argument is sound **conditional on its expressly stated parity-aware source convention**: non-edge A0 connections have even N and beta-alpha=72 degrees in the transported billiard boundary convention. The local double-pentagon endpoint-germ calculation, rather than the finite scripts, supplies the universal mechanism. The computations do not establish that convention as the unique literal reading of Fuchs. The bare source shorthand beta-alpha=72 degrees admits the two direct face diagonals, at graph distance two, and cannot be promoted as an unqualified affirmative resolution. Figure 9's diagonal types and Definition 2.1's exceptional directions must remain explicit in the source reconciliation.

There are two independent reproducibility defects to repair in the computational/public-certificate presentation:

1. The original scripts use Python assert for load-bearing scientific guards. Their successful optimized runs discard the guards. Actual wrong-science mutants pass under -O; this does not falsify the correctly guarded finite geometry. Audit-owned hardened private copies preserve the baseline output and reject all tested mutants under ordinary and optimized Python.
2. The actual pinned public certificate's displayed endpoint A+B eta is internally inconsistent with its displayed squared norm. This is separate from the valid reconstructed face-word geometry and its angle-convention problem.

## Independence and primary-source provenance

INITIAL_SOURCE_MODEL.md was protected before opening author proof/code or other opinions, at 2026-10-14T05:20:00.287063Z, SHA256 7763719a20d3fbb33c1dd5bbaebed287363006b99cca65cd4c8b5559718d8f60. It fixes the exact source target, graph metric, unbounded meaning of shortness, source endpoint-angle convention, success/failure conditions and independent geometric model. It is an initial assessment, not a final source-semantics verdict.

The Fuchs primary PDF, DOI 10.1007/s40598-020-00170-8, was read through the source PDF, local extracted text and rendered Figure 8. Cached PDF SHA256: 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d. The cited Athreya-Aulicino-Hooper primary PDF was checked at Proposition 4.4, Theorem 4.5 and Section 5. Its cover result and virtual-Weierstrass midpoint mechanism support the submitted ingredients; its all-saddle-connection Proposition 5.3 is restricted to triangles/squares and was not used for pentagons. Cached PDF SHA256: 76e1ec6f9f182fae395c2c6868c2e40071f24d01698ec3ccdfcb0eba975cec7b.

The pinned public PROBLEM_AND_PROOF.md was actually acquired from the HTTPS raw URL at commit 7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9. It is 5,081 bytes, SHA256 84baf6ab43b2c33c7a1b11e50e47fe2b48d891da981f44da9da18f4a5ba60513. An independent GitHub contents API request at that commit decodes to the identical bytes. The Git blob SHA1 was recomputed from the object header and body and equals API SHA1 29d80113dc2c8fe54568e59e8ce7262a3f24a565. The commit API reports tree 90a30f779b522ec140bb0aff1adc9b9a9550f01c. The commit object's hash was not independently reconstructed. PINNED_SOURCE_PROVENANCE.json contains public-safe metadata; all downloaded bodies and API source records remain private. HTTPS/API and hash agreement authenticates byte provenance, not mathematical validity. No downloaded software was executed.

## Independent exact geometric mechanism

independent_exact.py uses rational four-vectors in Q[T]/(T^4+T^3+T^2+T+1), with T=exp(2 pi i/5). Division uses rational Gaussian elimination of multiplication matrices, materially different from the original nested Q(sqrt(5)) complex classes. Real values convert exactly to a+b sqrt(5), with signs decided by rational comparisons, never floating point. Display angles alone use floating point.

The model constructs the 20 standard 3D vertices, derives edges by exact squared distance, and derives all 12 faces by supporting-plane enumeration. It checks face distance regularity, incidence, degree, all graph-distance censuses, the half-turn vertex/edge/face permutations, and the pairing of opposite edges into 15 axes. An independently found graph isomorphism identifies the authenticated public face list with the exact 3D solid.

For the path it reflects the preceding whole polygon across the shared developed edge, reverses physical cyclic incidence to label the new face, and transports original billiard labels by the reflected correspondence. It checks strictly ordered crossing times, strict edge parameters, exact line intersection identities, strict per-face containment and all developed vertex collinearities. The only vertex hits occur at parameters zero and one. It separately checks the two-edge path 0-16-2 and nonadjacency of 0 and 2.

The terminal transported ray is 2 to 16, exactly T^3, while the outward physical face ray 2 to 10 is -T^4. Exact sector signs give 0<alpha<36 degrees, so the source supplement convention gives beta-alpha=144 degrees for this even-N witness. Its display value alpha is about 5.041282 degrees. The public certificate's subtraction of its physical terminal interior angle yields 72 degrees but does not implement the transported boundary ray and Figure 8 supplement used by the candidate theorem.

## Additional pinned-coordinate arithmetic falsification

The authenticated public text defines eta=exp(i pi/5), phi=(1+sqrt(5))/2, A=(31+13 sqrt(5))/2 and B=-17-8 sqrt(5), and claims norm(A+B eta)=(307+137 sqrt(5))/2. Since eta+conjugate(eta)=phi, direct exact expansion gives

    norm(A+B eta) = A^2 + phi A B + B^2
                 = (425+189 sqrt(5))/2.

The difference from the displayed claim is 59+26 sqrt(5), strictly positive. compare_results.py checks the exact expansion and confirms that the authenticated face list, word and crossed edges equal the reconstructed literal inputs. This is a defect in the displayed coordinate certificate; it does not change the independently developed path's correct norm. INDEPENDENT_RESULTS.json preserves both claims separately.

## Actual baseline and adversarial runs

Runtime: /opt/homebrew/opt/python@3.14/bin/python3.14, version 3.14.6, flags -E -S -B -P, with -O added for optimized controls. The immutable original check_certificate.py, check_half_turn.py and five unittest cases each exit zero in both modes. The original JSON stream hashes match across modes: certificate b3863f882190c98bc385e1ef878961967acacca05b4f4d5c18a097881f0af255; half-turn d37e25d8358ea1ed1733f55cc097d8bf98da4d6ad7a4a41dd755994e3161cc26. The independent normal/optimized JSON hash is f1c54cba6071acc45328a4d287c3416821e9751594797c9c7685aadb73050f94.

| Private-copy control | Original ordinary | Original -O | Hardened ordinary / -O |
| --- | --- | --- | --- |
| Deliberate false guard | rejects | falsely succeeds | rejects / rejects |
| Expected squared length changed from 307/2 to 309/2 | rejects | falsely succeeds | rejects / rejects |
| Wrong source ray substituted | rejects | succeeds with wrong angle difference about 97.9174 degrees | rejects / rejects |
| Edge squared length set to zero | rejects | succeeds with zero edges and no rotations | rejects / rejects |
| Wrong cyclotomic coefficient C | rejects | KeyError, no scientific validation | rejects / rejects |
| Deliberately false unittest assertion | rejects | rejects | not needed |

The audit-owned guard repair transforms every ast.Assert node in both canonical scripts into an explicit conditional raise, on private copies only. Source and transformed hashes are saved per run. Hardened baselines have exactly the original baseline stdout hashes. These are engineering repairs, with provenance separate from the immutable originals; they do not repair or decide source semantics. The independent implementation already uses optimization-safe require guards. Its false-guard and wrong-length controls reject in both modes.

Additional exact boundary/arithmetic checks pass 1,048 controls: 160 rational field cases, 80 Pell near-cancellation cases, zero-denominator rejection in all three tested representations, and four direct first-vertex rays. Binary float returns zero in 51 Pell cases whose exact sign is positive; exact original and independent sign functions still agree. This validates the use of exact comparisons and also shows why the original small float-comparison unit test alone was insufficient evidence.

## Universal-proof audit and exact remaining gap

For an even-N connection satisfying the stated A0 angle relation, the terminal Q corner is q1=h(p0) on the double pentagon. Applying h to the reversed connection gives the same initial regular germ, so first-singularity uniqueness makes the midpoint a regular h-fixed point. The only such points are glued edge midpoints. A physical edge-axis half-turn has intrinsic derivative -I there; first-vertex uniqueness exchanges the endpoints even if the image self-intersects. A distance-two vertex pair has a unique common neighbor because the graph has girth five; swapping the pair would fix that neighbor, whereas the rotational vertex stabilizer has odd order three. This gives the conditional universal exclusion without any length bound or finite-search exhaustion. No circular use of all-pentagon saddle-connection symmetry was found.

The exact remaining gate is the relation of this parity-selected theorem to the literal target/source conventions, including the direct-diagonal exceptions. Finite replay cannot fill that gap. The bare 72-degree claim is falsified by direct diagonals, while the parity-aware theorem survives this independent geometric audit. The original solved label must not conflate those two statements. Historical priority and current-literature novelty are outside this family's conclusion.

## Evidence, limitations, and public-safe packaging

Every scientific replay/control command has actual argv, UTC start/end, exit status, raw stdout/stderr and their SHA256 in private/runs, private/control_runs or private/hardened_runs. The initial exploratory source-reading tool calls predate the runner and are described rather than given invented timestamps/receipts. The runner hashes file arguments after execution; script hashes and immutable-original before/after checks provide source-byte provenance. Commands launching original siblings under -P explicitly insert only the intended original directory; that path operation is necessary because safe-path mode omits implicit script-directory imports. No packages were installed and no SymPy was needed.

RUN_INDEX.json contains metadata-only replay records. SOURCE_INTEGRITY.json verifies the original source hashes and the initial seal. PUBLIC_SAFE_ALLOWLIST.json is the exact allowlist for own-authored report/code/derived data/provenance metadata. The entire private directory is excluded: it contains acquired source bodies, original streams and private repaired/mutated source copies. The allowlist is an inclusion declaration, not a publication action. FINAL_SEAL.json seals the final public-safe files and private receipt-tree hashes. No commit or push was performed under this audit's explicit no-Git/no-publication scope.
