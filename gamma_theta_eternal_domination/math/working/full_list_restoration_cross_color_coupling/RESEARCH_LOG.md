# Research log: cross-color coupling after attacked-anchor restoration

## 2026-07-28 (PDT)

- Began from accepted C-176's exact attacked-anchor restoration.
- Split the terminal according to \(e\in B\) versus \(e\notin B\).
- In the trapped branch, promoted the reciprocal \(xy\)-hinge to the full
  retained completion clique \(C_{re}\); all its states have exact
  source-ban distance two.
- In the nondominating branch, found the forced ladder
  \[
  \{r,t,e\}\to\{p,t,e\}\to\{p,t,v\}.
  \]
- Detected and preserved the collision \(p=u\).  The 16-vertex equality
  control realizes it repeatedly, so no argument may infer an edge \(pu\)
  without first excluding this collision.
- For \(p\ne u\), proved the exact singleton palette \(Q(p)=\{u\}\) and a
  genuine cross-color conclusion: the endpoint has positive rank under
  both other color bans.
- Added the completion fan \(C_{pe}\) and proved that, when \(p,e\notin B\),
  no noncolliding completion can have source rank one.  The proof uses only
  the same-ban C-175 tight shell and two escape barriers.
- Audited the tempting alternate derivation from the maximum independent
  state \(\{v,t,p\}\): the response \(v\to e\) is retained but need not be
  physically unique because \(te\) is unconstrained.  The proof uses only
  the genuinely unique attack at \(p\) from \(\{r,t,e\}\).
- Exact equality control census: 12 restoration rows, 19 witnesses, 12
  \(p=u\) collisions, 7 external singleton-palette witnesses, and 19
  noncolliding completions all at source rank three.
- Best-guess completion: 80% toward an independently reviewable local
  theorem package; 45% toward normalizing attacked-anchor restoration; 20%
  toward complete parameter three.  These are workload estimates, not
  probabilities.
