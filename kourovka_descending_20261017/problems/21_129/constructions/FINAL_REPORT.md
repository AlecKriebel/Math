# Construction-family checkpoint

Timestamp: 2026-10-24T20:06:12Z. Full-problem discovery estimate: **7%**.
Bounded construction probe: **100% complete**, including independent audit.
**Kourovka 21.129 remains unresolved.** No quasi-isometric noncommensurable
spherical Artin pair, common finite cover for an unresolved pair, or all-type
positive proof was found. No novelty claim is made.

The strongest verified geometric result of this probe is an elementary proof
that an irreducible spherical Artin group's central quotient is not strongly
relatively hyperbolic with respect to any finite family of proper finitely
generated subgroups when its rank is at least 3. Proper standard parabolics
inject into the central quotient by a positive-word support argument. Local
rank-two centers connect all standard generators by Z² subgroups, meeting the
exact hypotheses of Anderson–Aramayona–Shackleton Theorem 2. This rules out a
direct identification of the quotient with a finite-volume rank-one lattice.
It does not cancel Euclidean factors from arbitrary quasi-isometries.

The natural arrangement-deletion maps have infinite kernel, detected by the
winding number of a deleted-hyperplane meridian. The Coxeter-orbit CHL
monodromy maps in the relevant finite-parameter tables kill powers of every
standard generator. Crisp–Paris Theorem 1 puts an F2 in their kernel, surviving
passage to the central quotient. Finite-index restrictions retain an infinite
kernel, and even a lift through an abelian central extension still kills
[F2,F2]. Consequently neither the given maps nor central-extension repairs
of them are quasi-isometric embeddings. Arbitrary unrelated quasi-isometries
are not excluded.

The independently derived and audited algebraic classification of central
lattice quotients says: if Γ has p components, k nonsingletons, and
C≤Z(A_Γ) has rank r, then A_Γ/C is virtually (∏Q_i)×Z^(p−r), where Q_i are the
pure central quotients of the nonsingleton factors. This is commensurable
with a spherical Artin group exactly when r≤p−k, with the explicit
empty-diagram finite boundary recorded. When eligible, it simply consumes r
existing A1 components. Equal cyclic stabilization cancels for
commensurability. The additional QI exclusion in that report is expressly
dependent on KKL Theorem B and Cumplido–Paris Remark 5.2.

These construction mechanisms are **blocked** unless a materially new
noncentral operation or a coarse model controlling the infinite kernel is
provided. Rank equality, a common holonomy lattice, or a central product
alone does not supply the missing equivalence. F4/H4 and Dn/En (n=6,7,8)
remain candidate comparisons, not certified noncommensurable pairs here.

Checkable artifacts:

- `ARRANGEMENT_AND_LATTICE_PROBE.md`: all proofs, rank boundaries, exact gaps,
  and primary citations.
- `central_product_probe/CENTRAL_QUOTIENTS.md`: central-lattice and
  stabilization theorem, including nonprimitive lattices and empty/full-rank
  cases.
- `central_product_probe/cancellation_audit/audit.txt`: independent algebraic
  verification, plus a counterexample explaining why trivial virtual center
  cannot be replaced by mere centerlessness.
- `arrangement_adversary/AUDIT.md`: independent proof and source-scope audit. It
  required distinguishing CHL's original Coxeter group W from its Schwarz
  symmetry group G. The report now obtains Artin-generator finite-order
  images directly from CHL §3.5, rather than conflating the domains of
  Theorem 7.1; it also excludes κ=1 and corrects table locations to preprint
  §8.
- `SOURCE_MANIFEST.json` and `sources/`: primary PDFs, extracted text, URLs,
  SHA256 checksums, and theorem locators.
- `RESEARCH_LOG.md`: timestamped checkpoints and completion estimates.

All changes are confined to the delegated construction folder. No Git,
publication, external outreach, QUEUE, or PR action occurred.
