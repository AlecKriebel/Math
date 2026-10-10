# Problem 30003978: credited prior-preprint resolution

**already_solved, 1/5. Every r >= 9, with very general plane centers and one very general evaluation point.** The integral ample examples answer the original conditional question without proving Nagata. This result is credited to two extremely recent preprints, not to this packet:

- Antonio Laface and Luca Ugaglia, [Irrational Seshadri constants from dihedral orbits, arXiv:2609.26521v2](https://arxiv.org/abs/2609.26521v2), Theorem 2: r=9.
- Grzegorz Malara, Łukasz Merta, Justyna Szpond and Marcin Zieliński, [Dihedral reflections and an infinite series of irrational Seshadri constants, arXiv:2610.01783v1](https://arxiv.org/abs/2610.01783v1), Theorem 1.2: every r>=10 through n=2r-13.

The fresh [independent geometric audit](independent_audit/GEOMETRIC_AUDIT.md) gives PASS within this precise scope. It reconstructs the reflection only in globally line-bundle-marked rational blowup families; it does not certify the broader abstract proposition without repairing its base-change shorthand. The audit inspects the needed birational dynamics, Cartier descent, resolution, deformation, evaluation-point quantifiers and ampleness. Both decisive papers remain preprints. No journal acceptance, human peer review, formal verification, originality, first priority, or proof of Nagata is claimed. AI was used extensively.

The all-r argument is universal mathematics and application of the credited theorems. Exact arithmetic tests are supporting controls, not geometric certificates. No result for arbitrary centers, a single asserted Zariski-open locus, or all evaluation points is claimed.

## Preserved evidence

The author and independent-audit directories and their ZIP archives are byte-identical to their supplied freezes. The author's historical pending-audit wording and both packets' no-remote-write statements describe their original checkpoints. This wrapper records the subsequent audit and publication. Public source hashes, sizes, dates, inspection histories and theorem pins remain in their original metadata; no source PDF, extraction, image, raw dataset, selected dataset record or private coordination material is included.

Only this problem's Status, Turns and Findings cells change in the existing queue. Chat, DOI, all other rows and bytes, including the stale embedded SHA/size header, are preserved. PUBLICATION.json records the actual immutable-base queue hashes separately. Queue generation and unrelated state files are outside this narrow publication patch.

## Offline replay

Python 3 and SymPy 1.14.0 are required. From any working directory run:

    python3 /path/to/packet/verify_publication.py --expected-manifest MANIFEST_SHA256 --queue /path/to/QUEUE.md

Supply the publication manifest SHA-256 from the draft PR or private receipt as the external pin. The queue option is optional. The verifier rejects Python optimization, checks every byte, archive member and frozen pin, replays all exact outputs and integrity controls, and runs a synthetic false-assertion execution control. It writes only to temporary directories. Do not put replay output inside the strict packet. Computation can confirm the pinned code's output, not the mathematical truth of the imported geometric theorems. No CI observed must not be described as passing CI.
