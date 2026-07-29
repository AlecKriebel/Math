# Research log: full-list escape completion fans

## 2026-07-28 PDT

- Audited MMV-027 at the exact C-171 rank-preserving row.  Its source
  escape has rank zero because the next deleting attack is the old
  trapped witness \(w=3\): the unbanned alternate misses vertex \(4\),
  while the other response is banned.
- Isolated the equality-specific failure of that control.  The pairs
  \(\{q,w\}=\{2,3\}\) and \(\{r,y\}=\{10,1\}\) both dominate MMV-027,
  so both common-nonneighbor completion sets are empty.
- Proved the collision-safe first completion fan
  \(C_{qw}\subseteq N[t]\) and its unique \(t\to d\) exchanges away from
  \(d=t\).
- Proved that attacking \(y\) from the retained terminal uniquely
  retains \(\{v,r,y\}\).  This gives the second completion fan and its
  unique \(v\to e\) exchanges.
- Proved the all-\(k\) Johnson-distance rank floor
  \(\rho(D)\ge\delta_{\mathcal B}(D)-1\).  The one-step ban barrier is
  its distance-two specialization: a retained state containing neither
  fixed ban anchor cannot be deleted at restricted rank zero.
- Minimized rank over the second fan.  Its internal unique exchanges
  exclude the entire completion clique from the next deletion-witness
  attack, which must instead hit \(r\) or \(y\) and lead to a strictly
  lower-rank unbanned response.
- Classified the clean collision dynamics.  A \(wy\)-nonedge gives a
  reciprocal two-state hinge.  A common vertex of the two completion
  cliques forces \(wy\) and gives a reciprocal four-state square.
- Constructed and froze the exact 13-vertex separated-fan control
  `LEhbtnm~D]xln{`.  A standalone verifier recomputes
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4)\), greatest-family
  size \(200\), all three empty restricted kernels, source/escape ranks
  \(0/0\), singleton completion fans, completion ranks \(2/2\), and the
  four remaining dominating pairs.
- No unlogged bounded UNSAT result is used in the theorem or control.
- Best-guess completion: completion-fan/rank-rebound subgate **100%**;
  full cross-ban rank gate **60%**; complete \(k=3\) proof **50%**;
  universal conjecture resolution **18%**.  These are workload
  estimates, not probabilities that the conjecture is true.
