# Hostile review of C-173: completion fans after a trapped escape

## Verdict

**UNCONDITIONAL PASS** on the candidate bytes at commit `faff3d28`.

The theorem is correctly scoped.  It is a new structural layer in the
full-list \(k=3\) proof lane, not a proof of a safe restricted kernel, not
a complete \(k=3\) theorem, and not a resolution of the gamma--theta
conjecture.  The 13-vertex graph is used only as a sharp
\(\gamma=2\) boundary control.  No conclusion that assumes
\(\gamma=3\) is inferred from that control.

Review date: 2026-07-28 (PDT).

## 1. Independent proof audit

### 1.1 All-\(k\) rank floor

Write \(\Omega_0\) for all dominating \(k\)-sets outside the ban and
\(\Omega_{j+1}=\Phi(\Omega_j)\).  The candidate's deletion-rank
convention is:

\[
 \rho(D)=j
 \quad\Longleftrightarrow\quad
 D\in\Omega_j\setminus\Omega_{j+1}.
\]

For

\[
 \delta(D)=\min_{B'\in\mathcal B}\bigl(k-|D\cap B'|\bigr),
\]

one one-guard move changes the distance to each fixed banned state by at
most one.  The minimum of these one-Lipschitz functions is again
one-Lipschitz.  The exact induction is

\[
 D\in\mathcal F,\quad \delta(D)\ge h+1
 \Longrightarrow D\in\Omega_h.
\]

At the \(h\mapsto h+1\) step the premise is
\(\delta(D)\ge h+2\).  For every unoccupied attack, eternal closure gives
a one-guard successor \(D'\in\mathcal F\), and
\(\delta(D')\ge h+1\).  Hence \(D'\) is unbanned, dominating, and lies in
\(\Omega_h\) by induction.  Therefore \(D\in\Omega_{h+1}\).

If \(D\) has finite rank, taking \(h=\delta(D)-1\) gives
\(\rho(D)\ge\delta(D)-1\).  This indexing agrees with rank zero being
deletion in the first synchronous round.

The quantifiers are sound:

- \(k\ge1\) is arbitrary.
- The ban may be any nonempty collection of \(k\)-configurations; its
  members need not dominate.
- \(\mathcal F\) may be any eternal \(k\)-family, not necessarily the
  greatest one.
- A state "having finite restricted rank" already implies that it is an
  unbanned dominating state in \(\Omega_0\).
- Although an eternal successor can in general be banned, the distance
  inequality keeps every successor used at the induction horizon outside
  the ban.

The clean-room verifier additionally checked the bound for every labeled
graph through order four, every \(k\), every nonempty ban, and every
finite-rank state in the literal greatest eternal family: 75 graphs,
3,677 bans, and 5,477 state incidences.  This covers arbitrary eternal
subfamilies because every state in any eternal family belongs to the
greatest family.

### 1.2 C-168/C-171 hypothesis transfer

The candidate restates every hypothesis used from the accepted results:

- \(\gamma=\alpha=\gamma^\infty=3\);
- the literal greatest eternal triple-family;
- an independent root \(S=\{u,v,t\}\);
- a full target \(x\);
- a rank-zero nonroot corridor \(T=\{v,t,q\}\) with terminal
  \(E=\{v,t,r\}\), \(r\in B\), and selected move \(q\to r\);
- a secondary terminal color \(v\);
- an arbitrary C-168 witness \(w\) missed by \(\{t,q,r\}\);
- the trapped branch \(w\in B\);
- an arbitrary C-171 witness \(y\) missed by \(\{v,q,r\}\).

The imported edge and retention facts are exactly those proved in C-168
and C-171.  In particular, the candidate never turns a missing family
response into a graph nonedge.

### 1.3 Completion cliques and unique exchanges

The pairs \(q,w\) and \(r,y\) are graph-independent.  Since
\(\gamma=3\), neither pair dominates, so both completion sets are
nonempty.  If two vertices in one completion set were nonadjacent, they
and the defining pair would form an independent four-set, contradicting
\(\alpha=3\).  Both sets are therefore \(G\)-cliques.

For \(d\in C_{qw}\setminus\{t\}\), the retained state
\(\{w,t,q\}\) dominates \(d\), while \(q,w\) miss it.  Thus \(t\) is the
unique responder and \(\{q,w,d\}\) is retained.  The collision \(d=t\)
is handled correctly using the closed neighborhood \(N[t]\); the proof
does not attack an occupied vertex.

For the second fan, attacking \(y\) from \(\{v,t,r\}\) uniquely moves
\(t\to y\), retaining \(\{v,r,y\}\).  Every
\(e\in C_{ry}\) is then hit only by \(v\), so \(v\to e\) uniquely
retains \(\{r,y,e\}\).  Here \(e\ne v,t\): membership in \(C_{ry}\)
excludes \(v\) because \(vr\) is an edge and excludes \(t\) because
\(tr,ty\) are edges.

All claimed completion states contain neither fixed ban anchor \(v\) nor
\(t\).  Their Johnson distance from every state
\(\{v,t,b\}\) is at least two, so the all-\(k\) lemma gives exactly the
claimed kernel-or-rank-at-least-one alternative.

### 1.4 Minimum-rank exit

When the restricted kernel is empty, the nonempty second fan has finite
ranks, so a minimum-rank \(K_e\) exists.  An attack at another fan
vertex \(e'\) has the unique endpoint \(K_{e'}\), whose rank is at least
that of \(K_e\); it therefore cannot witness deletion of \(K_e\).
Every remaining unoccupied attack outside \(C_{ry}\) is adjacent to
\(r\) or \(y\).

Because \(K_e\) contains neither \(v\) nor \(t\), one guard move cannot
produce a banned state containing both anchors.  Every retained response
to a deletion-witness attack is consequently dominating, unbanned, and
strictly lower-rank.  The candidate does not claim that this lower-rank
response remains inside a completion fan.

### 1.5 Collision dynamics

If \(wy\) is absent, then \(y\in C_{qw}\) and \(w\in C_{ry}\).
The two hinge states are retained by the completion theorem, and the
only responders to the two displayed attacks are respectively \(q\)
and \(r\).

If \(d\in C_{qw}\cap C_{ry}\), then an absent \(wy\) would make
\(\{q,w,y,d\}\) independent, so \(\alpha=3\) forces \(wy\).  The four
square moves use only the physical edges \(wy,qr\); every other possible
responder is excluded by the four common-nonneighbor incidences.  All
forward and reverse moves are unique, all attacks are unoccupied, and
all four endpoints are retained maximum independent triples.

The separated-fan named-vertex count is also correct when \(wy,qt\) are
edges: the previously forced positive edges exclude all eight named
vertices from the appropriate completion sets, and disjoint nonempty
fans therefore contribute at least two new vertices.

## 2. Independent exact control

`verify_clean.py` is a clean-room bit-mask implementation.  It imports no
candidate or campaign transition code.  It independently:

- decodes and re-encodes `LEhbtnm~D]xln{`;
- checks 13 vertices and 50 edges;
- obtains
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4)\);
- constructs the 200-state literal greatest eternal family directly
  from one-guard synchronous deletion;
- checks the full root, all named retained states, all C-168/C-171 missed
  sets, and all unique physical responses;
- reconstructs the three empty restricted kernels and deletion-round
  profiles;
- obtains source/escape rank \(0/0\), singleton completion sets
  \(\{11\},\{12\}\), and completion ranks \(2/2\);
- reconstructs exactly the four dominating pairs
  \(\{0,8\},\{5,12\},\{6,10\},\{11,12\}\);
- independently proves \(\theta=4\) by exact complement coloring search.

The reported graph6 hash and edge-list hash are reproduced.  The latter
uses the candidate verifier's explicit graph6-triangular edge order and
`low-high\n` serialization.

## 3. Scope and adversarial exclusions

- Attacks are only at unoccupied vertices.
- Exactly one occupied guard moves along one \(G\)-edge.
- Every retained endpoint dominates and remains in the same family.
- All ranks belong to the single source-color ban; no cross-color rank
  comparison is made.
- Family retention is never confused with graph adjacency.
- The \(\gamma=2\) control is not promoted under the theorem's
  \(\gamma=3\) hypothesis.
- No safe kernel, complete \(k=3\) result, universal theorem, or
  conjecture resolution is claimed.

No mathematical defect, quantifier gap, collision error, or scope
inflation was found.

Best-guess review completion: **100%**.  Best-guess contribution of
C-173 toward the still-open complete \(k=3\) proof lane: **about 57%**
overall for that lane, as a workload estimate rather than a probability.
