# Hirzebruch–Kummer coverings: scoped partial investigation

Problem 30003859 / OWR-16169-001, rank 741. **Unsolved, 5/5 substantive approaches.** Prepared for draft review on 2026-10-05.

## Controlling scope

The literal unrestricted projective-orbit formulation admits the four-line/Fermat counterexample. That configuration lies outside the intended nontrivial-incidence setting discussed in the primary papers. This packet does not settle that intended conjecture.

The retained all-exponent deduction is eventual periodicity of **infinitesimal-rigidity failure** for each fixed nonpencil arrangement. It permits an infinite periodic set of failures. It is neither eventual rigidity nor a statement that local rigidity is eventually periodic. No novelty claim is made, and the published Bauer–Catanese complete-quadrangle theorem is credited rather than re-proved in full.

The independent audit passes the scoped deductions and honest unresolved status, with no mandatory corrections. This is AI-assisted, unrefereed work, not human peer review or proof-assistant certification. The audit's bounded source search is not proof of absence of later work.

## Precision clarifications

1. In Proof 6B, the homogeneous generators are the componentwise-minimal elements of H minus {0}. Minimality is taken among nonzero homogeneous solutions. Subtraction then gives the induction on coordinate sum. This clarification leaves every frozen author byte unchanged.
2. In the fifth approach, “equisingular” means the deformation subspace defined by the kernel of the local singularity-deformation map in Definition 2.1 of the cited configuration paper. It does not merely mean constant incidence or topology. Persistence and compatible contraction for arbitrary abstract deformations of the resolved surface are not established.

## Contents and reading order

- `PUBLICATION_STATUS.json`: machine-readable scope and disposition.
- `hirzebruch_kummer_30003859/REPORT.md` and `PROOFS.md`: source distinctions, five approaches, complete retained arguments and exact remaining gap.
- `hirzebruch_kummer_30003859_independent_audit/AUDIT_REPORT.md`: proof-by-proof independent audit and limits.
- The two ZIP archives reproduce their corresponding frozen directories byte for byte.
- `PUBLICATION_MANIFEST.json` and `verify_publication.py`: closed delivery inventory, freeze pins, exact replays and adversarial integrity controls.

Historical “pending audit” and “no remote publication” statements within the freezes describe their preparation stage. The wrapper records the subsequent scoped audit without rewriting that history.

## Reproduction

Python 3 standard library only, no downloads or external packages. From any working directory:

    python /path/to/30003859/verify_publication.py --selftest
    python -O /path/to/30003859/verify_publication.py --selftest

The wrapper checks archive/directory equality, preserved manifest pins, exact normal/optimized author and independent outputs, and both historical manifest mutation suites. The author enumerates 220,824 characters; the independent verifier enumerates 630,707. These finite checks supplement the written arguments and do not compute general logarithmic-sheaf cohomology or resolve the conjecture. A delivery-manifest hash proves byte integrity only when compared with a trusted external receipt.

## Queue and publication boundary

The queue patch changes only this target's Status from queued to unsolved and Turns from 0/5 to 5/5. Findings, Chat, DOI, all other cells and rows, and the embedded stale header are preserved byte for byte. The actual immutable Git blob is used, not that historical embedded header.

Only original authored analysis, code, audit results, integrity records and public verification metadata are supplied. Source PDFs, extracted source text, page images, dataset contents, private sources and coordination records are excluded. This draft does not authorize a merge, release, DOI, outreach or a solved-status promotion.
