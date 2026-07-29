# Research log: rank-one completion-fan anchor exit

## 2026-07-28 PDT

- Began from the tight-shell conclusion that a minimum second-fan state
  of rank one can be deleted only by an attack at \(v\) or \(t\), and
  every retained response has rank zero.
- Eliminated the \(v\)-attack.  Its forced retained response is
  \(J=\{v,r,y\}\), but \(J\) survives the first restricted round:
  attacks other than \(t\) cannot reach the ban, while the attack at
  \(t\) has the retained unbanned response \(r\to t\) to the C-171
  escape \(Y=\{v,t,y\}\).
- At the \(t\)-attack, ruled out both endpoints that retain \(y\).
  Each would survive its first round because its attack at \(v\) has a
  retained unbanned return to \(Y\).  Thus the only retained response is
  \(y\to t\), reaching \(D_e=\{r,t,e\}\) at rank zero.
- Proved that the next deleting attack is necessarily \(v\).  This is
  exactly the attacked-anchor restoration of accepted C-165.  Its
  second physical response is banned when \(e\in B\) and nondominating
  otherwise; the first case also gives the reciprocal \(xy\) hinge.
- No graph search, solver output, or unreviewed finite computation is
  used.
- Best-guess completion: this rank-one-exit subgate **90%** pending
  independent hostile review; complete parameter three **60%**;
  universal resolution **20%**.  These are workload estimates, not
  probabilities.
