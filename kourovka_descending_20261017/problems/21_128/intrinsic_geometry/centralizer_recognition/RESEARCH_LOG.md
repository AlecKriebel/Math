# Research log: centralizer recognition for Kourovka 21.128

All timestamps UTC. Work confined to this directory; no git operations or
external communications. Original claim being tested: arbitrary finite-index
isomorphisms between F4/H4 Artin groups can be forced to recognize parabolic
centers or maximal parabolic groups intrinsically. Success requires a theorem
covering **all** possible image elements, not only preidentified parabolics.

* **2026-10-24 20:20** -- Opened distinct centralizer/double-centralizer route.
  Preliminary primary searches found Ajbal--Godelle double centralizers and the
  2025 canonical reduction paper. Completion estimate 5%.
* **20:22** -- Established that the power-stable element centralizer is natural
  under finite-index isomorphism, with exact intersection formula. Its
  stabilization also follows from a finite-dimensional ascending chain of
  factorial-power matrix commutants. This is a routine lemma, no originality
  claim. Double-centralizer statements for known parabolics do not prove a
  converse classification. Completion estimate 8%.
* **20:24** -- Derived the maximal proper parabolic normalizer formula for F4/H4
  from elementary ribbon factorization and the central full Garside element.
  Checked the quotient centralizer issue using the length homomorphism.
  The parent independently derived the same mechanism; no sibling files read.
* **20:26** -- Froze current 2025 v2 of canonical reduction paper (rather than
  stopping at v1). Its Theorem 30 strengthens stabilization to computable
  periodicity, but does not classify arbitrary centralizers. Froze complete
  Davis--Huang and Amend--Hoge--Roehrle primary PDFs. Completion estimate 10%.
* **20:27** -- Identified extra rank-one parabolic-center profile in F4: the
  13-plane restricted arrangement, exponents 1,5,7, nonsupersolvable. This is not
  by itself a virtual-group invariant or a proven counterexample to the desired
  B3-only centralizer classification. Parent is independently computing its
  incidence data, so no duplicate computation is started here.
* **20:28** -- Audited Davis--Huang Definitions 1.11, 1.14, Lemma 1.13,
  Proposition 5.11 and Theorem 5.12. Confirmed that the family of Hopf lines is
  supplied by the arrangement, not intrinsically recognized under arbitrary
  group isomorphisms or finite-index isomorphisms. Wrote precise scope report.
* **20:29** -- Completed self-contained proof of exact pure centralizer formula
  C_(Q_T)(bar(Delta_X^2)^m)=P_X and the double-centralizer/virtual-center formula
  after every finite-index restriction. Recorded A3 capped-puncture swap as an
  independent test refuting preservation of raw parabolic rank. Exact remaining
  gaps: nonparabolic stable-centralizer classification, rank-one restricted-
  arrangement comparison, and intrinsic recognition. Publication gate closed.

Strongest established result: the exact maximal-parabolic stable-centralizer
formula and finite-index naturality, together with a primary-source scope audit
of why they do not settle the problem. No resolution of 21.128 is claimed.

* **2026-10-24T20:30:54.402379+00:00** -- Independently adversarially rechecked the parent's general stable-centralizer spectrum lemma and virtual-center quotient variant: all index, power, and quotient formulas hold in arbitrary groups, without finite generation or linearity. Corrected Proposition 1.31 locator to PDF p19. Final route estimate 10%; no complete solution.

2026-10-24T20:42:01.001420+00:00 — Parent intrinsic-family source delta: directly read Marin2007Theorem3 and SorokoProp3; copied public PDFs into family source cache, with hashes. Added unconditional pure-Q unique-root, all-power centralizer equality and subgroup virtual-center equality lemma. No centralizer classification or complete solution follows. Full-goal estimate remains10%. The completed original author could not be reactivated because all agent slots were occupied; this bounded delta was authored by the parent and submitted to the fresh reviewer.
