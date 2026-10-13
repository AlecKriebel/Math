# Research log: independent BFH implication audit

Assigned scope: only this review directory; no external communication, no native
input edits, queue or PR mutation, or publication. Independent task checks the
specific prior-construction implication, rather than a universal historical
firstness claim. Original head: `947442c091ae617804c6a0d07b98ff2c50368798`.

- **2026-10-13 05:15:25 UTC - checkpoint, 35% complete.** Read the original
  packet and relevant BFH sections without reading the priority reviewer's
  conclusions. Verified primary arXiv record and source cover: the inherited
  filename `bfh_v3.pdf` is actually arXiv:2010.00279v2, 25 July 2022. The paper
  supplies a finite-bath, point-evaluation clock, but its stated strong unitary
  continuity alone does not imply point-norm continuity of conjugation on C_b.
- **2026-10-13 05:21:01 UTC - checkpoint, 85% complete.** Reached the initial
  independent conclusion and reported it to the parent. Explicit bit-flip Kraus
  completion W with odd g and finite endpoint limits repairs the continuity
  issue. Forward-generated restriction matches the source. The expectation-GNS
  module is finite dimensional; invariant kernel would yield a derivation
  generator contradicting the channel's diagonal projection derivative. Added
  a full standalone derivation covering both M2 and C^2, plus the explicit
  log(2) kernel witness. No priority verdict was read.
- **2026-10-13 05:22:53 UTC - checkpoint, 100% complete.** All 14 exact
  finite-matrix controls passed using a dependency-free multiquadratic-field
  script. Visually inspected BFH pages 1, 5 and 9-12. Logged source and input
  hashes and explicitly distinguished BFH's stated theorem from this unstated
  short corollary. No mathematical gap remains in the specific implication;
  generic-channel continuity and the conditional extension problem are outside
  scope. Deliverables finalized locally; no commit or push was authorized for
  this subtask.
- **2026-10-13 05:27:10 UTC - final checkpoint, 100% complete.** The same angle identity supplies a selfadjoint
  kernel witness at every s>0 for M2 and C^2. Its shifted expectation has a
  positive coefficient, but the witness is not globally positive in BFH's odd
  extension: at s=log(2), a_s(-s/2)=-(1/4)q. The candidate's clipped extension
  may supply globally positive witnesses as an additional property; this audit
  does not conflate that with the prior short kernel-failure corollary.

Author metadata for the underlying project: Alec Kriebel,
ORCID https://orcid.org/0009-0001-9320-500X.
