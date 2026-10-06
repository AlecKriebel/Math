# K-sheet quotients: audited type-A partial answer

**Problem 30001460 / OWR-4332-001, rank 826: unsolved, five substantive approaches recorded.**

The [independent audit](audit/AUDIT.md) accepts a scoped partial result, with a one-line summary clarification. The general nonregular arbitrary-type question is unresolved.

## Accepted result and exact limits

Over an algebraically closed field of characteristic zero, with connected K, every K-sheet for gl_n or sl_n has a geometric quotient in finite-type, possibly nonseparated schemes. More generally the proof gives a sufficient criterion: the K-sheet lies in one ambient G-sheet, and each required nilpotent centralizer in the connected adjoint group G is connected. The quotient is obtained by open gluing of nilpotent transverse slices.

Read the [frozen proof](author/RESULT.md) with the [scheme-level supplement](audit/PROOF_SUPPLEMENT.md) and [clarification patch](audit/CLARIFICATION.patch). The ambient G-section is restricted to one K-saturation at a time, so different K-orbits are not silently merged. The supplement proves faithful-flat comparison of morphisms, invariant functions, inverse transition maps, and full cocycle domains. Open chart gluing constructs a scheme; it does not establish separatedness.

The type-A centralizer statement concerns PGL_n, not SL_n. A regular nilpotent SL_n centralizer has n components. The scalar-center eigenspace and the sl_n reduction are treated explicitly in the supplement. No assertion is made for positive characteristic or disconnected K.

## Mandatory clarification of the separated obstruction

The rank-one claim is: there is no **K-invariant orbit-separating morphism** from the specified sl_2 K-sheet to a separated scheme or separated algebraic space. Invariance is essential. The detailed frozen proof already assumes it, but its opening summary omits the words “K-invariant.” The accompanying actual patch inserts only those words. The author freeze remains unchanged; this wrapper and the supplement supply the current accepted reading.

The affine line with doubled origin is a valid nonseparated quotient and is already documented by García-Prada–Peón-Nieto and Hameister–Morrissey. The Hameister–Morrissey result published in 2025 covers the regular locus. It is not a solution for all arbitrary-type nonregular K-sheets. The type-A deduction is assembled from credited published inputs, and no novelty, priority, exhaustive literature search, human peer-review, or formal proof-assistant certification is claimed.

## Five approaches and the remaining gap

[APPROACHES.md](author/APPROACHES.md) records exactly five mechanisms: affine invariants, one slice, gluing type-A slices, requiring separated targets, and attempted extension beyond connected centralizers. The accepted gluing theorem and separated obstruction do not close the fifth route. Local K-orbit separation and scheme representability in the missing arbitrary-type nonregular cases remain unproved. Publication and replay do not count as a sixth proof attempt.

## Preserved artifacts and public boundary

Both [archives](archives/) and their extracted author/audit members are preserved byte-for-byte. Historical freeze-stage statements about pending review remain historical snapshots; current acceptance is the scoped audit verdict above. The public package contains authored mathematical work, code, audit results and public verification metadata only. It contains no source PDFs, copied source extracts, dataset contents, private sources, private personal data, or private coordination records.

## Replay

Python 3.10 or newer, the standard `patch` command, and SymPy are required for full replay. The tested symbolic dependency is SymPy 1.14.0, pinned in requirements.txt. Dependency installation is outside the integrity boundary.

Retain the SHA-256 of PUBLICATION_MANIFEST.json independently and inspect verify_publication.py before running it. The manifest binds the verifier and all package bytes; a self-replaced manifest is not an independent trust anchor. From this directory:

    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256
    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full
    python -I -O -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full

Full replay checks strict inventory and both ZIP/member correspondences before executing code. It replays 23 author rank-one identities, the independent author harness (four baseline/relocation variants and 24 rejected mutation cases), and 38 independent symbolic identities with five mathematical countercontrols. It compares actual outputs with the frozen JSON results. It also applies the actual clarification patch on a temporary copy and checks that only the intended words change. Relocate the entire directory to check path independence.

These finite controls do not prove descent, the gluing theorem, novelty, or full resolution. The optional identity checker takes three separately supplied source corpora and emits only public hashes/counts/match metadata; keep those corpora outside this package. The tests assume a trusted interpreter and no hostile concurrent filesystem writer.
