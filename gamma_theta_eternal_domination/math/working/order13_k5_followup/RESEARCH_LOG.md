# Research log: order-13, parameter-five follow-up

## 2026-07-26 10:22 PDT

- Opened an independent follow-up to
  `math/working/order13_k5_structural.md` at frozen SHA-256
  `1761c537ce293f1d7e36fd32786ffad0a67f2f7fe9dd4af6aceed346ccec6d37`.
- Rechecked the exact C-051 projection statement at SHA-256
  `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620`
  and the C-048 simplicial reduction at SHA-256
  `87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a`.
- Found that the preceding note records only part of the available
  projection lattice.  Anchors \(a,b\), their independent pairs with kernel
  vertices, and deeper independent anchors give exact mask-dependent
  parameter-four, -three, -two, and -one residuals.
- Derived an exact equivalence between \(\theta(G)=6\) and the failure to
  insert either attachment vertex into any part of any minimum
  four-clique partition of \(Q\).
- Translated absence of a dominating four-set to exactly 707 subset tests.
- Translated nonsimpliciality to the masks.  Since every \(r\in R\) has
  \(N_G[r]=N_Q[r]\), all vertices of \(R\) must be nonsimplicial in \(Q\);
  hence cluster-graph kernels are impossible.
- Derived necessary first-response tests from the forced independent states
  \(\{v\}\cup I\) and \(\{a,b\}\cup J\).
- Used those tests to prove: if both masks have size six, they must be
  equal.  The unequal case has forced independent sets on which an attack at
  \(b\) has no dominating one-guard successor.
- The equal six-mask branch remains open, so no slice exclusion is claimed.
- Best-guess completion toward a rigorous order-13, \(k=5\) exclusion:
  **35%**.  This estimate reflects a substantially tighter finite universe,
  but no completed orbit enumeration or universal attachment contradiction.

## 2026-07-26 10:30 PDT

- Ran the standalone small audit with warnings fatal and bytecode disabled.
- It checked all 1,024 labeled graphs on five vertices and confirmed that
  the ten labeled graphs with \(\gamma=\alpha=\theta=4\) are exactly the
  one-edge graphs used in Lemma 9.
- It independently reproduced the 707 domination obligations, the
  465,157 ordered and 233,002 unordered raw mask counts, and the split of
  two six-masks into 210 equal pairs and 5,040 unequal pairs.
- The exact output is frozen in `evidence.json`.  This audit is explicitly
  not an all-kernel enumeration or slice certificate.
- Final blocker for this sprint: the forced-response argument eliminates
  unequal six-masks but not \(A=B\), and it gives only necessary tests for
  smaller masks.  A further analytic transition lemma or the covered
  canonical enumeration is required.

