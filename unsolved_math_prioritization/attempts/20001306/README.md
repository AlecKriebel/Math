# Polar-zonoid intersection bodies: audited partial results

Problem 20001306 / AIM-CONVEX_GEOMETRY-0038. Status: **unsolved, 5/5 attempts**.

The original question asks for Baire-generic non-polar-zonoidality of the intersection body of an origin-symmetric convex body in every fixed dimension n >= 3. This package does not solve that unrestricted question.

The strongest accepted result is open-dense non-polar-zonoidality in the separately specified space of four-dimensional bodies of revolution about a fixed axis. It follows by cap truncation from Alfonseca's flat-top theorem, with a normalized inverse-transform verification. Ancillary results include finite rational dual certificates, quantitative stability, and exact cube witnesses. No first-discovery or absolute novelty claim is made.

- [Frozen proof and package guide](public/README.md)
- [Full independent adversarial audit](audit/AUDIT_REPORT.md)
- [Audit verdict](audit/AUDIT_RESULT.json): PASS for partial results only
- [Author manifest](public/FROZEN_AUTHOR_MANIFEST.json)
- [Audit manifest](audit/FROZEN_AUDIT_MANIFEST.json)

The frozen author files retain their historical attempt-stage language. The audit and this publication record supersede their pending-audit notices and clarify the canonical status: `unsolved`, `5/5`. In particular, “exhausted” in the historical narrative describes the spent attempt budget; it is not the queue status.

Run `python3 public/check_exact.py` for standard-library exact checks. The independent controls require SymPy: `python3 audit/calculation-controls/independent_calculations.py`. Both suites have passed; finite checks do not prove the unrestricted conjecture or worldwide novelty.

This draft contains authored mathematical notes, frozen manifests, and complete sanitized audit/control artifacts only. It excludes downloaded PDFs, complete source transcriptions, catalog/prior-report extracts, and local operational context. The queue change is confined to this problem's status and turn-count cells. No merge or release is requested.
