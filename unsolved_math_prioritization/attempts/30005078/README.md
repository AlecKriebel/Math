# Multigraded regularity: audited scoped partial results

Problem **30005078 / OWR-10252925-002**, rank 789. **General finite-presentation module problem: UNSOLVED; five of five approach families used.**

## What is established

- Under the standard ambient lattice Z^2, the diagonal structure sheaf on P^1 x P^1 has regularity a+b >= 0 and infinitely many minimal degrees (t,-t). Therefore an unrestricted finite-frontier or finite-minima-box sheaf formulation fails. This does not exclude algorithms returning symbolic descriptions such as a half-space.
- Its finitely generated Cox module S/(x0*y1-x1*y0) instead has regularity N^2. The H_B^1 obstruction explains the difference.
- For monomial quotients on products of positive-dimensional projective spaces, the finite-cell algorithm is exact and terminating. It returns all actual minimal points and the complete regularity region as generalized orthants allowing negative infinity (encoded as None). Empty minimal-point output need not mean an empty region.
- The explicit box bounds minimal points, not the whole usually unbounded region. The audited `audit/frontier_box.py` interface helper exposes `minimal_element_box` while preserving all original result fields and leaving the frozen author code unchanged.
- Exact rational/prime-field ranks handle genuine characteristic dependence. The RP^2 Stanley-Reisner control has regularity 3 in characteristic 2 and 2 in characteristics 0, 3 and 101.

The missing general step is an effective completeness criterion or global frontier bound for arbitrary finite homogeneous module presentations. Membership tests, outer translates, or Dickson finiteness alone do not supply it. No novelty, priority, formal-proof, human-peer-review or general-solution claim is made.

## Immutable packets and later clarifications

`author/` preserves the exact nine-file original freeze, including historical audit-pending and failed-access statements. `audit/` preserves the exact twelve-file independent AI-assisted audit, including `AUDIT.md`, `CORRECTIONS.md`, the helper, complete review-hash verification and qualified source-inspection history. Read those current addenda together with the author packet.

The EMS report was published **14 April 2023**, in the 2022 volume; the workshop ran **27 March–2 April 2022**. The audit successfully inspected the numeric landing page after the earlier author access failure. The audit also independently recomputed the full-record review hash, which the author had explicitly left unrecomputed.

`frozen_archives/` contains canonical base64 encodings of the original two ZIP byte streams. Both ZIP identities, manifests and every extracted member are checked by the publication verifier. `PUBLICATION_PROVENANCE.json` binds the packet to fresh main and records complete cached corpus/source rehashing without distributing any source content. Historical no-remote-write statements refer to the respective freezes.

Primary source: [Toric Geometry report](https://ems.press/journals/owr/articles/10252925), Question 3.1, printed p. 873 (PDF p. 13). The adjacent general-toric Question 3.2 and neighboring record 30005077 are not solved or changed here. Current characterization/bounds/software claims retain their exact hypotheses and completeness limits in `audit/SOURCE_AUDIT.json`. Macaulay2 was not installed or executed.

## Portable verification

Python 3.10+, standard library only; assertions must remain enabled:

    python3 -B /path/to/packet/verify_publication.py --expected-manifest <manifest SHA-256>
    python3 -B /path/to/packet/test_publication_integrity.py

The verifier checks exact recursive inventory, fixed archive and inner-manifest pins, every byte, and the scoped disposition. It replays the frozen audit in an isolated temporary copy and requires byte-identical author and audit outputs. Rebuilt controls include 36 example/field combinations, 3,600 fixed-region degrees, 2,028 independent fine-degree comparisons, 80 Koszul controls, 144 cell-invariance controls, 1,681 diagonal controls, 3,840 additional memberships, 36 proved-box minima comparisons, 24 helper comparisons, seven invalid inputs, and all four RP^2 field controls. Finite tests support the written mathematical audit; they do not replace proof.

Optional `--queue-before` and `--queue-after` arguments check complete queue bytes and the exact two-field patch. Full corpus/source rehashing requires external inputs via `audit/verify_provenance.py`; ordinary standalone replay does not claim to re-inspect literature or reproduce a network search.

## Repository scope

Only this target's queue Status and Turns change to `unsolved` and `5/5`. Findings and every other queue byte, including its stale literal header, are preserved. Catalog, state, history, other targets and source files are unchanged. This is one draft PR, without merge, release, DOI or outreach.
