# Research log: canonical rank-one QQ1 pair core

Date: 2026-07-28 (PDT)

- Rebuilt the collision encoding with \(y_u=x\); the earlier fresh-label
  encoding does not represent this branch.
- Independently audited the forced edges
  \(xb,xc,bc,up,uq\) using C-064 covariance and explicit unoccupied
  attacks.
- Audited the fresh-to-collision normalization: an independent completion
  of \(\{u,b\}\) and a two-step attack prove \(u\triangleright a\), while
  the reverse state remains \(B\).
- Found that requiring only \(\{u,x\}\) to be non-dominating is UNSAT
  through order 14 but SAT at orders 15 and 16.  This killed the proposed
  one-pair exit as an order artifact.
- Independently reproduced the order-15 control
  `NslalntvXzn^{~n||^w`: it has a unique common nonneighbor of
  \(\{u,x\}\), but 23 other dominating pairs.
- Replayed its complete common-nonneighbor repair square.  The opposite
  asymmetry survives and its omitted corner has rank three, so the
  repair raises rather than lowers the local deletion rank.
- Froze standalone exact checkers for that graph and the order-14
  dominating-\(\{u,x\}\) boundary graph.  Both have
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\) and a literal
  rank-one canonical QQ1 collision.
- Full-\(\gamma\) discovery formulas were UNSAT through order 16.  No
  proof logs or all-order coverage exist, so this remains OBSERVED only.
