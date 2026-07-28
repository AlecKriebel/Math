# Research log: rank-one \(ur=1\) endgame

Date: 2026-07-28 (PDT)

- Isolated the two remaining accepted C-150 rank-one collision rows:
  QQ1 and AQ1.
- Reconstructed the three private witnesses and the already proved
  private-witness transfer states
  \[
  M_p=\{x,y_p,q\},\qquad M_q=\{x,p,y_q\}.
  \]
- Verified symbolically that attacking \(y_p\) from \(M_q\) forces
  \(U=\{u,y_p,y_q\}\) into the greatest family, after which the unique
  response to \(r\) forces \(R=\{r,y_p,y_q\}\).
- Began a domination-pair CEGAR probe to identify a small set of
  \(\gamma\geq3\) constraints genuinely needed by the exact SAT
  obstruction.  This is discovery guidance only, not a certificate.
- Found a critical collision omitted by the initial discovery encoding:
  in QQ1 the private witness \(y_u\) may equal \(x\), and `GEjbug`
  realizes exactly that collision.  Retracted any interpretation of the
  fresh-label QQ1 SAT runs as covering the full row.  The symbolic proof
  now makes the canonical choice \(a=y_u=x\) in QQ1 and treats it
  explicitly.
- Proved the forced states
  \[
  M_p=\{x,b,q\},\ M_q=\{x,p,c\},\
  U=\{u,b,c\},\ R=\{r,b,c\}.
  \]
  In AQ1, attacking the fresh \(a=y_u\) from \(R\) also forces a path to
  the independent state \(S=\{a,p,q\}\).
- Proved two private-marker ridge arguments.  In AQ1 they force
  \(ab=ac=1\); in the QQ1 collision they force \(xb=xc=1\).
- Proved short named attack trees forcing, in both rows,
  \[
  xb=xc=bc=up=uq=1.
  \]
  The dynamically excluded hub \(W=\{x,b,c\}\) misses \(r\) directly
  in QQ1; in AQ1 an attack at \(a\) sends every possible mover to a
  state missing one of \(r,p,q\).
- Proved \(u\triangleright a\), \(a\not\triangleright u\) in AQ1.
  Consequently the AQ1 row recreates a literal QQ1 collision on
  \(S=\{a,p,q\}\) with the same rank-one reverse state and blocker.
  Thus only the self-similar canonical QQ1 normal form remains.
- Proved the full-hit completion-clique obstruction: every common
  nonneighbor of \(a,r\) is adjacent to both \(p,q\), and all such
  completion vertices form a clique.
- Recorded the exact seven-vertex complement core: a root triangle, a
  bottom 4-cycle, and three matching spokes.  Each of its seven nonroot
  complement edges needs an external triangle completion under
  \(\gamma=\alpha=3\).
- Independently replayed the fixed graph `Hslaghb` with both campaign
  evaluators:
  \[
  (n,m;\gamma,i,\alpha,\gamma^\infty,\theta)
  =(9,17;3,3,3,4,4).
  \]
  A compact ordinary-set checker independently deletes its 45 dominating
  triples in rounds of sizes 24 and 21.  This is a static boundary
  control, not a counterexample and not a minimality claim.
- Wrote the self-contained candidate proof `NOTE.md`,
  `verify_implication.py`, `verify_control.py`, and exact-byte
  `verify_strict.sh`.  The strict replay passes.
