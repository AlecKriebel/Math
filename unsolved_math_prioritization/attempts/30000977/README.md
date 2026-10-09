# Credited degree-12 counterexample to the singular-target degree bound

Problem 30000977 / OWR-1971-010 is resolved negatively by the published Gleissner–Pignatelli–Rito example. Read current/PROOF_AUDIT.md and the complete current/SECOND_AUDIT.md. Both are preserved byte-for-byte from independent acceptance. The example has exactly nine A2 canonical singularities, Cartier ample base-point-free K, K squared 24, pg=4, and complete canonical map of degree 12 onto a singular rank-three quadric cone in P3. Its degree-27 construction cover onto P1 x P1 is a different map.

The inspected arXiv:1807.11854v2 Section 6 is credited; its group-rank and section-divisor typos are explicitly repaired. The contextual patch clarifies function-eigenline duality and completed independent acceptance. The source was published in Communications in Analysis and Geometry 30(8) (2022), 1811–1823, DOI https://doi.org/10.4310/cag.2022.v30.n8.a5. Publisher text was not inspected, so publisher/preprint equivalence and publisher typo status are not asserted. Three of five exploratory routes preceded discovery of the prior example; no new proof-search turn, novelty claim, or broader classification is added.

## External trust and reproduction

Authenticate BOOTSTRAP.py using the SHA-256 in the separately reviewed PR description, then copy the authenticated file outside this packet. Set every packet file to mode 0444 and every directory to 0555. Use actual UID=EUID=1000 and the trusted Python standard library:

    python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet

Omit --controls for the baseline replay. The fixed external bootstrap authenticates the manifest, verifier and control harness before execution. The manifest binds every other delivered file, including every historical/pre-seal receipt and all complete raw references. It excludes only itself and BOOTSTRAP.py: the bootstrap binds the manifest, and its own bytes are fixed by the independent external pin. Final receipts stay outside the bound inventory, avoiding circular hashes. Trust still rests on the reviewed external pin, CPython and its standard library; these are not authenticated by the packet.

Fresh outputs must equal every mode-specific reference byte without normalization. The wrapper replays the unchanged original and independent checker, two positives and seventeen expected mutants per mode, requiring the same historical complete raw output and intended reason. Structured JSON also uses recursive exact types, with duplicate keys and non-finite values rejected. Six positives and fifty-one mutant rejections across the three modes are the audited suite, separate from extra baseline/hostile/control replays. Physical create, append-open and unlink failures are tested at actual UID/EUID1000, with before/after hashes of the entire delivery. Permission modes are an accidental-write barrier, not protection against root or intentional owner chmod.

The original checks cover 27 characters and 25 branch strata. Independent checks derive differentials from the six Kummer equations, test 729 character pairs against 27 group elements (19,683 evaluations), sixteen crossings, 625 invariant-monomial interfaces, all 27 summands, 25 strata, every divisor coefficient, the exact rational differential relation, quadric rank, and degree arithmetic. These finite interfaces do not establish existence, ampleness, duality, singularity classification, completeness, or finiteness without the geometric proofs.

## Historical and excluded evidence

Everything under historical/ records the prior audits, including source retrieval/visual-inspection history, original proof, original runner, acceptance summary and manifests. Statements that retrievals were fresh refer to their recorded audit date, not this publication stage. All historical artifacts are immutable selected inputs. The contextual patch is freshly checked by zero-fuzz application to the historical original proof and comparison with the reviewed proof. The original historical harness itself is NOT_RUN; only its two checkers and seventeen mutations are freshly replayed using the new isolated runner. Historical metadata is not current trust authority.

CHECK_RUNS.json and all reference stdout/stderr files record the pre-seal capture. Full historical harness, source bodies, source classification, publisher text, published/preprint equivalence, new source search, dataset and formal-proof-assistant stages are NOT_RUN. No copied PDF, extracted source text, source image, dataset content, private source or private coordination material is included. No QUEUE or unrelated path changes are included.
