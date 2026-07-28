# Research log: canonical QQ1 completion dynamics

Date: 2026-07-28 (PDT)

- Reconstructed the accepted C-158 canonical QQ1 core and kept the
  collision \(a=x\) literal.
- Applied C-143 to every independent completion
  \(\{x,r,d\}\), proving that \(d\) must hit the two side witnesses
  \(b,c\) as well as \(p,q\).
- Tested the tempting shortcut that \(\{u,d\}\) must dominate against
  the exact order-15 \(\gamma=2\) control.  It does dominate there, but
  this alone is not an equality proof because \(\gamma=3\) forces a new
  missed vertex.
- Found the cold-witness contradiction.  If \(w\) misses \(u,x,d\), the
  ridge \(\{x,d\}\) transports the exact singleton response at \(u\);
  the retained state \(\{u,b,c\}\) then has no response to the attack
  at \(d\).
- Derived the exact consequence for equality: every witness missed by
  \(\{u,d\}\) hits \(x,r\) and at least one of \(b,c\).  This is the
  first forced external layer beyond the C-159 boundary controls.
- Derived the rank diamond
  \[
  B(1)\leftarrow P_d,Q_d(\le2)\leftarrow R_d(\le3),
  \]
  with equality \(1,2,2,3\) in both fixed controls.
- Compared the result with accepted C-161.  The link separation caps do
  not close the hot layer: the new theorem forces each completion out of
  every outside \(u,x\)-link instead of connecting its two components.
- Identified the exact conditional self-similarity when \(ud\) is a
  nonedge: the hot witness and pivot \(d\) create the opposite asymmetric
  edge \(r\triangleright w\) with the same omitted corner and rank.

