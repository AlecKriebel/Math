# Research log

## 2026-07-27 22:15--22:40 PDT

- Pinned the reviewed target to commit
  `21f5042e6a010db53f759177a0f36d90016cc0ba` and verified that the
  working-tree target bytes matched the commit.
- Read the complete target note, verifier, result, and the exact prerequisite
  statements C-079, C-082, C-083, and the full-link no-isolate theorem.
- Reconstructed the positive-tail neighborhood-independence proof and both
  applications of C-079 in the bow-tie classification.
- Checked every edge and distinctness condition in the outside and anchor
  completion branches.
- Reconstructed the full Lemma 4.1 attack tree.  Confirmed that all attacks
  are at unoccupied vertices, every possible one-guard successor is
  enumerated, and each rejection is by a graph nonedge, an accepted
  dead-state fact, or explicit failure to dominate.
- Independently recomputed the old common-neighborhoods for \(rs\), \(sq\),
  and \(x\); checked all pairwise distinctions among \(z,w,y_0,y_1\);
  and verified the exact \(n\ge13\) and \(n\ge14\)-or-\(L(w)=\{b\}\)
  count.
- Audited every use of response-list information.  Found no inference from
  list omission to graph nonadjacency.

## 2026-07-27 22:40--22:48 PDT

- Reran the target verifier with isolated Python and warnings fatal; the
  output matched the pinned result byte for byte.
- Wrote a clean-room standard-library checker using Graph6 decoding and
  integer masks, with no imports from the target or search code.
- Independently reproduced the 109-state restricted family, deletion
  rounds \(20,4,5,5,2\), all 872 legal unoccupied-attack obligations,
  exact lists, and the sorted-family digest.
- Independently computed unrestricted eternal-kernel sizes
  \(0,0,148\) for \(k=1,2,3\), confirming
  \(\gamma^\infty=3\), and reproduced
  \((\gamma,\alpha,\theta)=(2,3,3)\).
- Verified the exact bow-tie, empty second-color cap sets in the control,
  absence of a complement \(K_4\), and absence of C-079 embeddings.
- Wrote `REVIEW.md` and pinned the machine-readable replay in
  `evidence.json`.
- Final verdict: **PASS on the reviewed bytes**, with the conditional scope
  preserved and no global order claim.
