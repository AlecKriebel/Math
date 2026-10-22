# Kapovich Problem 14: credited positive literature deduction

Target: **6200014 / AMR-061-0014**, catalog rank 808. Disposition: **already_solved**, 2/5 substantive approaches. This is a full positive deduction from published results in the exact source scope, with no claim of a new theorem or priority.

For a closed topological manifold with a finite simplicial **flag and no-induced-square** triangulation, the homeomorphism type of the boundary of the associated right-angled Davis complex depends only on the homeomorphism type of the underlying manifold. Disconnected manifolds and dimensions zero and one are included. No arbitrary CAT(0), equivariant, or quasi-isometry assertion is made.

Read the preserved [proof](author/PROOF.md), [independent AI audit](audit/AUDIT_REPORT.md), and [bibliographic addendum](audit/corrections/BIBLIOGRAPHY_ADDENDUM.md). The audit accepts the deduction without mathematical corrections. The source PDF is dated October 24, 2007; the 2005 date refers to the AIM workshop. Both original frozen ZIPs and every extracted file are preserved byte-for-byte.

## Published sources and credit

- Przytycki and Świątkowski, *Flag-no-square triangulations and Gromov boundaries in dimension 3* (2009), Corollary 5.7(2): dimensions at least five excluded, including non-PL triangulations. https://doi.org/10.4171/GGD/66
- Davis, Fowler and Lafont, *Aspherical manifolds that cannot be triangulated* (2014), p. 797: automatic PL property of four-manifold triangulations. This does not assert uniqueness of PL structure. https://doi.org/10.2140/agt.2014.14.795
- Świątkowski, *Trees of manifolds as boundaries of spaces and groups* (2020), Theorem 2 and topological uniqueness of the trees: the crucial boundary recognition. https://doi.org/10.2140/gt.2020.24.593
- Martin and Świątkowski, *Infinitely-ended hyperbolic groups with homeomorphic Gromov boundaries* (2015), Theorem 4.1: the disconnected free-product case. https://doi.org/10.1515/jgth-2014-0043
- Kapovich, *Problems on boundaries of groups and Kleinian groups*, Problem 14 and its preceding hypotheses, p. 5. https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

The authored note and independent AI audit are unrefereed. The finite checks validate encoded combinatorics, integrity, and replay behavior; they do not certify the imported topological theorems. The historical author freeze's audit-pending language is retained as historical provenance; the separate accepted audit supplies the later status.

## Reproduce

Python 3.9 or newer, standard library only; no network required:

    python3 verify_publication.py --replay --negative-controls
    python3 -O verify_publication.py --replay --negative-controls

For provenance checking, add `--manifest-sha256 SHA256` using the separately obtained publication-manifest digest in the publication receipt. Original ZIP and internal-manifest hashes are hard-coded. The wrapper verifies exact files and directories, rejects symlinks and special files, matches every extracted byte to its authenticated ZIP, and replays both packets normally and under optimization. It reruns the independent author's 30 clean/mutation cases and 1,100-graph controls. The wrapper's negative controls also mutate the audit packet, including rehashed false results.

To verify the precise queue change against full separately retrieved snapshots:

    python3 verify_publication.py --queue-base /path/to/before.md --queue-updated /path/to/after.md

Only rank 808's Status, Turns, and Findings change. Every other queue byte, including its pre-existing header, is retained. Source-corpus identity checks are optional and require separately supplied inputs; see the frozen packet READMEs. Source documents, excerpts, screenshots, datasets, and private coordination files are excluded.
