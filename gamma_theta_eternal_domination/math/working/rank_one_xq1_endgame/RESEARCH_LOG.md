# Research log: rank-one XQ1 endgame

## 2026-07-28 13:05 PDT — lane opened

- Read the final accepted C-145, C-146, and C-150 source notes, the final
  C-150 hostile review, its errata history, manifests, and research logs.
- Fixed the standing hypotheses
  \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), a one-sided active edge
  \(u\triangleright x\), \(x\not\triangleright u\), the independent endpoint
  \(T=\{x,p,q\}\), the rank-one reverse state \(B=\{u,p,q\}\), and an XQ1
  deleting attack \(r\).
- The two rank-zero successors give distinct private witnesses:
  \(y=y_p\) hits \(p\) and misses \(u,r,q\), while \(z=y_u\) hits \(u\)
  and misses \(r,p,q\).  Accepted C-150 further forces
  \(xy,xz,yz\in E(G)\) and the four consecutive independent facets
  \(\{y,r,q\},\{z,r,q\},\{z,p,q\},\{x,p,q\}\).
- New proof target: apply accepted ridge response-covariance along this
  entire facet path, audit every named collision and adjacency, and decide
  whether the resulting exact lists close XQ1 or yield a sharper normal
  form.
- Completion estimate toward this XQ1 subproblem: **30%**.  The accepted
  input is fully reconstructed; the new covariance consequences still need
  a complete proof and hostile self-audit.

## 2026-07-28 13:42 PDT — covariance closes XQ1

- Audited all \(21\) pairs on the seven named vertices.  Nine are forced
  edges, ten are forced nonedges, and only \(up,uq\) remain optional.
  All seven vertices are distinct.
- Avoided covariance at an exchanged target.  In the C-150 ladder, the
  second facet \(J_z=\{z,r,q\}\) has the physical exact list
  \(L_{J_z}(y)=\{z\}\).  C-064 across
  \(J_z\leftrightarrow\{z,p,q\}\) and then
  \(\{z,p,q\}\leftrightarrow T\) gives
  \[
  L_T(y)=\{x\}.
  \]
  Hence \(\{y,p,q\}\) is retained but
  \(M=\{x,y,q\}\) is omitted.
- Extended the independent pair \(\{u,y\}\) to
  \(I=\{u,y,s\}\).  Activity \(u\triangleright x\) retains
  \(\{x,y,s\}\).  If \(s=q\), this is already \(M\).  Otherwise \(q\)
  is unoccupied; domination forces \(sq\), and the unique legal response
  to the attack at \(q\) moves \(s\to q\), again retaining \(M\).
  This contradicts the transported exact list and proves rank-one XQ1
  impossible.
- The completion collision audit is exhaustive: \(s\) cannot equal
  \(x,p,r,z\) because each is adjacent to \(u\) or \(y\), leaving only
  \(s=q\) or an external vertex.
- Wrote `verify_implication.py`, an ordinary-set audit of the complete pair
  partition, collision cases, ridge transpositions, exact list, and retained
  six-state grid.  Its output matches `expected_result.json`.
- Wrote an independent existential-family SAT falsification model.  CaDiCaL
  returned `UNSAT` at the sampled orders \(7\) through \(22\).  These runs
  are frozen as `OBSERVED` only; they have no proof certificates and are not
  used in the symbolic theorem.
- Completion estimate toward this XQ1 subproblem: **90%**.  The proof and
  bookkeeping verifier are complete; final hash freeze, byte audit, commit,
  and push remain.
