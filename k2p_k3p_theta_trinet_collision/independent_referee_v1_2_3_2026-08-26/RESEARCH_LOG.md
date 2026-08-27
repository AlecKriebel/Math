# Research log

## 2026-08-26 21:23 PDT - Audit initialized

- Created a dedicated audit directory and a disposable byte-for-byte packet
  copy.
- Verified every packet file listed in `PACKET_SHA256SUMS`; all hashes matched.
- Confirmed work remains on `main`. The surrounding repository already has
  unrelated modified and untracked files; they will not be altered or included
  in audit commits.
- Defined the central hypotheses to test:
  1. the theta-trinet network and comparison tree have the asserted exact K2P
     collision with strict stochastic and edgewise continuous-time parameters;
  2. the K3P quartic, local-geometry, continuous-time, and algebraic conclusions
     follow at exactly the stated scope;
  3. arbitrary-taxon grafting preserves equality and the claimed topology and
     genuinely-K3P properties;
  4. the supplied programs and certificates independently establish every
     computational assertion attributed to them.
- Success criteria: paper-first derivations; independent source audit; exact
  replay; substantive mutation tests; page-by-page visual QA; literature checks
  against primary sources; and a severity-ranked, claim-by-claim referee report.
- Boundary cases targeted: parameter boundaries, character relabelings,
  rooting/suppression conventions, rank neighborhoods, and graft-kernel
  injectivity.
- Independent approach families launched: mathematical proof audit, code and
  certificate audit, and reproducibility/layout/literature audit, followed by
  adversarial cross-checking.

Best-guess completion: **5%**.

## 2026-08-26 21:38 PDT - Replay, independent reconstruction, and first reconciliation

- Read the 19-page main manuscript in full before the two support documents;
  checked the displayed-tree formula, K2P/K3P constructions, continuous-time
  arguments, ranks/local geometry, algebraic conclusion, and grafting proof.
- Inspected every program, certificate, manifest entry, and provenance claim.
- Ran the complete normal/optimized/PDF replay successfully in the immutable
  packet copy.  All expected text artifacts, compact-certificate regeneration,
  and pre/post hashes matched.
- Ran four substantive negative controls in disposable copies: collision
  datum, graph assignment, stored rank determinant, and K3P fixed-output
  tangent.  Each failed at the intended mathematical assertion rather than at
  packet integrity.
- Built and ran an audit-local clean-room SymPy checker, importing no packet
  module or certificate.  It independently recovered both central collision
  factorizations, direct ordinary-state pruning for K2P and K3P, all coordinates,
  the selected ranks, and the K3P tangent identity.
- Visually inspected all 23 supplied PDF pages and verified literature/scope
  statements against primary sources.  The one substantive prose issue found
  so far is an over-broad attribution of full level-one identifiability to two
  papers that establish generic results.
- Current strongest conclusion: no counterexample or arithmetic/proof defect
  has emerged in a central theorem.  The most material implementation concern
  is that K3P Jacobian/free-direction names are not mechanically bound to their
  semantic descriptors; an adversarial mutation is being tested directly.

Best-guess completion: **82%**.
