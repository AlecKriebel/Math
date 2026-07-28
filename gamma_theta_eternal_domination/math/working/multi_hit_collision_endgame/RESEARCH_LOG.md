# Research log: multi-hit collision endgame

## 2026-07-28 PDT

- Reconstructed accepted C-143, C-145, C-146 and all three hostile
  reviews before using their consequences.
- Split the C-146 \(k=3\) collision exactly into the three endpoint
  patterns \(\{x,p\}\), \(\{p,q\}\), and \(\{x,p,q\}\), each with
  \(ur\) absent or present.
- Proved the all-rank six-case response table.  In the
  \(\{x,p\},ur=0\) row, the deleting attack has a unique successor of
  exact rank \(h-1\), the response to \(u\) from \(T\) is forced to use
  \(q\), and the active pair \(q,u\) is reciprocal.
- Proved that a singleton response list at \(r\) is reciprocal in the
  \(\{x,p\}\) and \(\{p,q\}\) rows.  The proof uses the alternate
  endpoint as the C-145 common-nonneighbor ridge and never deletes a
  genuine graph edge.
- Proved the private-witness rule for every rank-one successor.
- Eliminated the rank-one \(\{x,p\},ur=0\) row.  Its witness makes
  \(\{u,r,y\}\) independent; activity \(u\to x\) retains
  \(\{x,r,y\}\), which has no responder at the other endpoint \(q\).
- In the remaining \(ur=0\) rank-one rows, proved a paired-witness ridge
  and two forced three-move paths to \(T\).  C-064 covariance excludes
  each private witness from answering the endpoint it privately covers.
- In the rank-one \(\{x,p\},ur=1\) row, proved a forced four-facet
  independent ridge path through the two private witnesses.
- For the \(\{p,q\}\) collision, proved the completion-clique
  alternative.  Equality makes the common-nonneighbor set of \(x,r\)
  nonempty and a clique.  A member missing \(p\) or \(q\) immediately
  gives the corresponding reciprocal \(r\)-edge.  Thus a collision with
  neither reverse direction forces every completion to hit both
  endpoints.
- Located `GCOedo` as a sharp static warning:
  \((\gamma,i,\alpha,\gamma^\infty)=(3,3,3,4)\), and it realizes the
  rank-one \(\{x,p\},ur=0\) local pattern only because the required
  \(u\to x\) successor is non-dominating.
- Replayed `GEjbug` as the sharp dynamic boundary:
  \((\gamma,i,\alpha,\gamma^\infty)=(2,2,3,3)\); its QQ1 collision takes
  the dominating-pair exit \(\{x,r\}\), so the equality completion set
  is empty.
- No equality-compatible dynamic countermodel was found.  The full-hit
  completion-clique branch, all-three-hit branch, and higher-rank
  successor dynamics remain open.

## 2026-07-28 PDT — hostile-review revision

- The frozen hostile audit found no substantive mathematical defect, but
  required the six-case theorem to state its multi-hit hypothesis
  explicitly.
- Corrected the completion set \(C_{xr}\) to exclude its endpoints and
  added the missing line \(y_g\ne g\) in the private-witness proof.
- Refroze the candidate for byte-specific confirmation review; none of
  these edits enlarges the theorem's scope.
