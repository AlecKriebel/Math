# Research log: RAAG and cyclic-fiber counterexample route

Author metadata: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## 2026-10-17 21:14 UTC — scope and initial checkpoint

**Scoped-route completion estimate: 10%. Overall 21.141 discovery estimate: 5%.**

Investigate whether an incoherent right-angled Artin pro-p group, or a topologically finitely generated but not topologically finitely presented kernel of a character onto Z_p, can supply a counterexample to Kourovka 21.141. No conclusion is assumed. All subgroups are closed, maps continuous, and generation/presentation belong to the pro-p category. No outreach, Git operation, or publication is performed by this subagent.

Success would require a proper pro-p amalgam with coherent vertex groups and polycyclic edge, together with an explicitly verified finitely generated non-finitely-presented closed subgroup. An abstract Bestvina–Brady kernel alone does not meet this criterion.

## 2026-10-17 21:15 UTC — primary evidence and obstruction

**Scoped-route completion estimate: 70%. Overall 21.141 discovery estimate: 8%.**

Read Snopce–Zalesskii's primary paper, *Right-angled Artin pro-p groups*, arXiv:2005.01685, especially Theorem 1.6 and Lemma 5.3–Proposition 5.5. Its natural incoherent cycle examples split coherent tree RAAGs over a rank-two free pro-p edge. This edge is not polycyclic. In contrast, a full RAAG subgroup is polycyclic only when its graph is complete; clique-sums preserve chordality. Thus the canonical RAAG amalgam route is blocked.

Derived a stronger obstruction to the cyclic-fiber mechanism: in any proper amalgam of coherent pro-p vertices with every closed edge subgroup finitely generated, every finitely generated kernel of a character onto Z_p is finitely presented. The finite-orbit case uses only low-degree continuous cohomology and the standard-tree chain sequence. The zero-edge-character case gives quotients with an infinitely generated kernel. The exact argument is in `FIBER_OBSTRUCTION.md`.

## 2026-10-17 21:16 UTC — adversarial checkpoint

**Scoped-route completion estimate: 95%. Overall 21.141 discovery estimate: 10%.**

The supervising counterexample agent independently checked the finite-orbit Mayer–Vietoris argument, the finite-p-quotient construction of an index-p subgroup containing any proper closed edge image, and both quotient mechanisms in the zero-edge-character case. A completed lamplighter quotient supplies a direct certificate of infinite generation in the C_p free-product case. Primary supporting sources are cached with SHA-256 hashes in `sources/manifest.json`.

Strongest checked result: the cyclic-fiber obstruction stated in `FIBER_OBSTRUCTION.md`; in particular no cycle RAAG on at least four vertices can be isomorphic to such a coherent/polycyclic proper amalgam. This is a partial obstruction, not a solution of 21.141, and novelty is not claimed.

Exact remaining gap: arbitrary finitely generated subgroups of the proposed amalgam need not be normal kernels with quotient Z_p, and may have infinite orbit spaces on the standard pro-p tree. The argument does not control their stabilizers or finite presentability. A general nonchordal RAAG with a finitely presented global length kernel is likewise not excluded from an arbitrary noncanonical splitting merely by the cyclic-fiber obstruction.

## 2026-10-17 21:18 UTC — falsifiable boundary example

**Scoped-route completion estimate: 98%. Overall 21.141 discovery estimate: 10%.**

Derived an explicit six-vertex incoherent pro-p RAAG with no finitely generated non-finitely-presented global Z_p-fiber: take a cone on a chordless four-cycle, then attach a pendant vertex at the cone apex u. Its decomposition is `(G_C4 × Z_p(u)) amalg_{Z_p(u)} Z_p^2(u,w)`. A character killing u has an infinitely generated kernel by the zero-edge quotient argument. A character nonzero on u has finite quotient graph, a kernel in the first vertex isomorphic to an open subgroup of G_C4, a procyclic second vertex kernel, and trivial edge kernels; its kernel is finitely presented. This establishes a concrete boundary of the mechanism, not just an absence of a proof. The displayed amalgam has an incoherent vertex and therefore does not answer 21.141.

## 2026-10-17 21:18 UTC — abelian-quotient strengthening

**Scoped-route completion estimate: 98%. Overall 21.141 discovery estimate: 10%.**

The supervising counterexample agent suggested the extension to all finitely generated abelian pro-p quotients. Independently verified the reduction: if the edge image has nonopen image in such a quotient Q, the quotient by that edge image has a nonzero Z_p-character; its pullback kernel is finitely generated as an extension of the proposed finitely generated fiber by a closed subgroup of Q, contradicting the zero-edge-character result. Hence the edge image is open and the finite-orbit argument applies. The complete proof is now Section 3 of `FIBER_OBSTRUCTION.md`.

