# Minimal simplicial-cell torus facets: audited partial result

Problem **30001702 / OWR-4798-027**, rank 833, remains **unsolved, 5/5**. Read [SCOPE_CLARIFICATION.md](SCOPE_CLARIFICATION.md) before interpreting the immutable [author proof](author/PROOF.md). The [independent audit](audit/ADVERSARIAL_AUDIT.md), [expanded lemmas](audit/EXPANDED_LEMMAS.md), and [acceptance](audit/ACCEPTANCE.json) certify only the stated partial scope.

- General central-binomial bound and vertex refinement
- Factorial minima in dimensions one and two and in the regular unimodular lattice-quotient subclass
- Necessary five-vertex K_5 obstruction in dimension three, with f-vector (5,27,44,22) or (5,28,46,23); no realizability claim
- Colored 1-dipole reduction only in the properly four-colorable subclass

No universal resolution, novelty, or human peer-review claim is made. The author and audit archives, all 17 extracted members, and both external manifests are unchanged. The original packets' historical status and commands remain as frozen evidence. They are superseded for publication entry by the isolated procedure below.

## Isolated, externally anchored replay

Obtain the bootstrap SHA-256 and publication-manifest SHA-256 from the independently delivered publication receipt or verified draft-PR metadata. First authenticate bootstrap.py itself without executing it. Trusting a replacement bootstrap or obtaining both new pins from an untrusted modified package defeats authentication.

Use a trusted Python 3 interpreter and its standard library. With an absolute ordinary directory ROOT, execute the independently authenticated bootstrap:

    python3 -I -S -B /trusted/bootstrap.py ROOT EXTERNAL_PUBLICATION_MANIFEST_SHA
    python3 -I -S -B -O /trusted/bootstrap.py ROOT EXTERNAL_PUBLICATION_MANIFEST_SHA
    python3 -I -S -B /trusted/bootstrap.py ROOT EXTERNAL_PUBLICATION_MANIFEST_SHA test_publication.py

The gate requires isolation, no site startup, and no bytecode writes before any nonbuiltin import. It rejects extra files or directories, bytecode caches, import shadows, symlinked roots/ancestors/entrypoints, nonregular and hardlinked files, duplicate manifest keys, and unpinned changed bytes. It checks both immutable archives and every archive member before executing verified source bytes in a private snapshot. A temporary interpreter dispatcher forces -I -S -B for every archived subprocess, preserving normal or optimized mode without editing original code.

The trusted interpreter, standard library, operating system, independently supplied pins, trusted bootstrap, and a quiescent input filesystem remain explicit assumptions. This is an integrity/replay gate, not a sandbox against arbitrarily authorized replacement code or a formal proof checker. The original archived control suite intentionally generates its known diagnostic mutations and demonstrates the limits of caller-replaced manifests.

The adversarial publication suite runs full normal/optimized baseline and relocation checks, rejects malformed trees and pins, and verifies import/source sentinels never execute. PUBLICATION_TEST_RESULTS.json records the results. Finite checks support the mathematical prose; neither checksums nor tests establish the universal conjecture.

## Public-safe boundary

Only authored mathematics, verification code, audits, acceptance, and public source/corpus hashes, sizes, titles, URLs, and inspection metadata are included. Source PDFs, extracted third-party text, images, dataset records, and private coordination files are excluded. Historical source inspections are documented in the original audit; publication replay does not claim fresh source retrieval or a new literature search.
