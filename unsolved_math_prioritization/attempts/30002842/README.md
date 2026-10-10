# Rational VOA finiteness: five audited partial routes

Problem 30002842 / OWR-13673-012, rank 991. **Unsolved; 5/5 approaches.**

Start with [publication acceptance](PUBLICATION_ACCEPTANCE.md), the [full report](original/REPORT.md), [full independent audit](independent_audit/AUDIT.md), and [independent narrow review](second_review/REPORT.md). The narrow review covers only author Sections 2.3–2.5 and 5.

The packet accepts the partial results and the specific unsupported total-tail limit inference in the inspected Han v5 proof. Its affine witness has nonzero V1 and an inner derivation. Neither Han's theorem nor the target conjecture is disproved, and no prior resolution is accepted.

## Layout and immutable inputs

- original/: unchanged author freeze, manifest SHA-256 a9b478491ffe9f3dd75d177bd863ec8dc2f28ac3ed69f04bce9e35955247e989
- corrected/: separately adopted execution-only patch, manifest SHA-256 937d23a943cda19e23850e7e84842b74c97dd936e280d8d3a1bdea07a58710e3
- independent_audit/: unchanged full audit, manifest SHA-256 686831a2a758fcd663fa5795ae0cbe229adcd636be512cc1999e26f93d89287a
- second_review/: unchanged limited-scope review, manifest SHA-256 56e6978c21452d495b7e8dd534ca70eb7f0848cb10f895b56985534acf16db6d

The corrected copy changes only disposable test-fixture permissions and the matching manifest entry. The wrapper replays that exact two-file patch without fuzz and compares every other author byte.

## Reproduction and trust boundary

Python 3 standard library only; no network or packages. Obtain the publication-manifest, verifier and mutation-runner SHA-256 hashes from the independently recorded PR description or a trusted receipt, and verify the two programs before running them. A manifest authenticates bytes against that external record; it is not a signature.

After verifying the program hashes externally, run:

```sh
python -I -B VERIFY_PUBLICATION.py --expected-manifest "$MANIFEST_SHA256"
python -I -B -O VERIFY_PUBLICATION.py --expected-manifest "$MANIFEST_SHA256"
python -I -B -OO VERIFY_PUBLICATION.py --expected-manifest "$MANIFEST_SHA256"
python -I -B TEST_MUTATIONS.py --expected-manifest "$MANIFEST_SHA256" --expected-verifier "$VERIFIER_SHA256"
```

VERIFY_PUBLICATION.py authenticates the full closed inventory, strict JSON, fixed inner manifests, exact correction and file types before any packet code runs. TEST_MUTATIONS.py uses an externally pinned bootstrap and never executes a substituted target verifier. It also makes only its own disposable fixtures writable, so it can run from a read-only release.

Original and corrected author baseline verification, corrected author mutation tests, and full-audit checks run in ordinary, -O and -OO modes. The immutable narrow review uses assertions and is always launched in a fresh isolated ordinary child with sanitized Python environment and a false-assertion control. Optimized wrapper coverage must not be confused with optimized native narrow-checker coverage. Original author mutation tests are not run as a read-only release suite: that documented defect is precisely what the separate corrected copy fixes.

Finite arithmetic and mutation controls do not certify the general VOA proofs. Source inspections and manuscript status are dated evidence, not fresh literature retrieval during replay. No source PDFs, extracts, dataset contents, private material, or coordination files are included. No external author contact or release is part of this publication.
