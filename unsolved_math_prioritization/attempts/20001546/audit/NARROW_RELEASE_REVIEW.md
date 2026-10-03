# Narrow independent release review: rank 456 / problem 20001546

Reviewed 2026-10-03 UTC.

## Verdict: PASS

The 14-file release is a faithful clarified projection of the independently audited nine-file original. All three nonblocking recommendations are correctly addressed. The original mathematical verdict and all essential scope limitations are preserved. No further correction is required by this narrow review.

This PASS concerns mathematical accuracy, faithful projection, and the inspected release contents. It does not itself authorize publication or any remote write.

## Integrity and execution

- All 14 release files match their paths, byte counts, and SHA-256 values in RELEASE_MANIFEST.json; there are no extra files or symlinks.
- RELEASE_CHANGE_MAP.json exactly matches the manifest's file entries.
- An independently reconstructed unified diff for the original nine files matches release_changes.diff.
- All nine original files still match FROZEN_MANIFEST.json and remain unchanged.
- The copied frozen manifest and both independent-control files are byte-identical to their originals.
- Both release verifiers run successfully under ordinary Python 3. Each output is structurally identical to its retained JSON; checks_turn2.json also remains byte-identical to the frozen original.

Machine-readable results are recorded in NARROW_RELEASE_CHECKS.json beside this report.

## Three clarifications

### 1. Exact weak-modularity source and graph identification: PASS

The new Attempt 5 paragraph identifies precisely the needed quotient theorem: Haettel–Huang, *Lattices, Garside structures and weakly modular graphs*, Theorem 5.7. It then uses the proof of Corollary 4.5 in *New Garside structures and applications to Artin groups* to identify the quotient's 1-skeleton with this specific Cayley graph Q. These exact source statements were checked during the full audit.

The Garside element (1,1) here means identity in A and generator 1 in the Z coordinate. It is central, and its quotient removes exactly the extra Z factor. The union of lifted intervals is the identity plus the nine positive generators already specified. No graph substitution or additional hypothesis is hidden in this clarification.

### 2. Intrinsic rank-two normalization and source: PASS

For g=a^u z^k, z=p^3, setting v=3k gives the stated expression max(|u|,|3k|,|u+3k|). In the dual B3 structure with Garside element p, powers a^m have infimum 0 and supremum m for m>=0; inversion gives the negative-power case, and multiplication by p^(3k) shifts both invariants by 3k. Hence the displayed infimum/supremum values are consistent for every integer u,k. Substitution into the simple-generator length formula yields the claimed expression.

I independently opened the exact new [Lee–Lee primary PDF](https://arxiv.org/pdf/math/0604061v2). Section 4, printed page 8, first paragraph, states the three-case shortest simple-generator length formula equivalent to max(sup(g),0)-min(inf(g),0). Section 2.1, printed page 2, supplies the normal-form definitions. The bibliographic title, authors, version and section reference agree with the release.

The added paragraph expressly keeps this calculation intrinsic to the rank-two subgroup and does not assert ambient Q metric preservation, control of centers outside that subgroup, or an unbounded coarse-Helly defect. Thus it clarifies the earlier motivational statement without crossing the unresolved bridge.

### 3. Explicit image controls: PASS

The added assertions directly test that the images of a^n and p^n differ and enumerate the complete triple intersection of the radius-n image ball with the two translated image balls. They pass for n=1,2,3. They do not assume faithfulness, do not assert uniqueness of actual A-elements at n=2,3, and do not change the certificate schema or its values.

## Public projection and scope: PASS

The public audit differs from the full audit only by the declared omission of nonpublic bookkeeping and its short disclosure. It preserves every mathematical section, the PASS/HOLD distinction, source caveats, recommendations and limitations. SOURCE_GATE.md retains the bounded nature of repository and literature checks. The declaration that no mathematical finding was removed is accurate.

README.md and RELEASE_CHANGES.md accurately distinguish the original audited package from the clarified release and retain its unresolved status. Their language about awaiting narrow review describes the state before this report; this report supplies that review. The separate publication gate remains unaffected.

Accepted scope remains UNSOLVED, 5/5. In particular:

- Q, Q^2 and Q^3 fail Hellyness; no arbitrary-power or unbounded-defect conclusion is asserted.
- The tree-fiber obstruction remains conditional on its equivariant projection and isometric real-tree-fiber hypotheses.
- The W x Z counterexample remains a torsion-bearing counterexample to unrestricted factor inheritance, not to a torsion-free variant.
- The canonical hull has a proper action, with cocompactness equivalent to the still-undecided coarse Hellyness of Q.
- No proper cocompact Helly action for A, and no obstruction to every such action, has been established.

No sixth attempt or remote mutation was performed in this narrow review. No new mathematical or literature search was undertaken; the sole new source access was the expressly permitted ordinary read of the exact Lee–Lee citation.
