# Stable log surfaces: accepted degree-five partials

Problem 30002343 / OWR-12490-003; rank 984. **Unsolved, 5/5 substantive approaches.** No universal 5I theorem or novelty claim. Read [acceptance](ACCEPTANCE.md), [unchanged proof](public/PROOF.md), and the [complete independent audit](independent_audit/INDEPENDENT_AUDIT.md).

The literal ordinary-canonical pair formulation fails for P2 with a smooth quartic boundary. The logarithmic question remains unresolved. For L=I(K+Delta), I>=2, degree five separates every length-two scheme contracted by degree three and every such scheme avoiding the degree-two base locus. Thus generation of 2L implies very ampleness of 5L. The remaining branch is explicitly retained. All original author and audit files are byte-preserved; no correction patch was required.

## Source-free portable verification

Use Python 3.10 or newer, standard library only. Copy this entire directory. Obtain the PUBLIC_MANIFEST.json SHA-256 and the verifier and mutation-suite SHA-256 values from the independently authenticated PR description or publication receipt. Check both executable hashes with a trusted external hash tool before running them. A digest calculated only from the same unauthenticated packet is not an external trust anchor.

From any working directory, replace PIN and PACKET with that manifest hash and the package directory:

    python3 -I -S -B PACKET/verify_publication.py PIN PACKET
    python3 -I -S -B -O PACKET/verify_publication.py PIN PACKET
    python3 -I -S -B -OO PACKET/verify_publication.py PIN PACKET
    python3 -I -S -B PACKET/mutation_tests.py PIN PACKET

The verifier checks exact inventories, bytes, nested frozen manifests, historical metadata, and actual child runtime flags before accepting deterministic replay. It stages execution in a temporary directory and checks that the packet stays unchanged. The corruption suite tests original and relocated copies with 0/1/2 optimization and rejects 19 mutation types at each setting, including laundering attempts against both frozen packets. These are finite controls, not security against hostile executable code.

The frozen programs use assert statements; these are disabled by -O/-OO. The outer verifier uses explicit exceptions and compares the resulting output in every mode. It does not pretend those disabled assertions ran. The independent frozen program's internal nested author commands omit optimization and isolation flags and are not separately probed. The publication harness removes inherited PYTHON environment variables, separately runs author and audit programs with each stated optimization level, and records the runtime flags from inside each direct child.

Source PDFs, source text/extracts and datasets are absent. Source citations, sizes, hashes and inspection history remain public. No network access is used by replay. Historical PDF checks are metadata-checked, not rerun on missing documents. Finite replay does not verify geometric dependencies, universal surface claims, current literature completeness, or novelty. This is AI-assisted, unrefereed research, not conventional human peer review.
