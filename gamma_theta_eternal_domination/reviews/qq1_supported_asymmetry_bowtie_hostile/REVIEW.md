# Hostile review: supported asymmetric-edge bow tie

## Verdict

**UNCONDITIONAL PASS** on the candidate bytes at commit `8fffe1b6`.

The supported one-sided edge theorem, every stated fan status and
activity direction, and the C-166/C-167 QQ1 corollary are correct.  The
proof uses only graph incidences supplied by its hypotheses or accepted
dependencies.  It never converts family omission into a graph nonedge.

The theorem is a size-independent normal form.  It does not eliminate
QQ1, establish activity symmetry, complete \(k=3\), or resolve the
gamma--theta conjecture.

Review date: 2026-07-28 (PDT).

## 1. Hypotheses and dependencies

The universal theorem assumes

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and an arbitrary eternal family \(\mathcal F\) of dominating triples.
It does not require the greatest family.  The imported facts have the
same family quantifier:

- every maximum independent triple belongs to every eternal
  triple-family;
- C-108 transports a retained active response between independent
  triples containing the mover and avoiding the target;
- the supported-pair theorem retains the complete central fan of every
  co-occupied pair and makes its common-nonneighbor set a clique;
- C-172 gives the exact all-retained/all-omitted central-fan dichotomy for
  every adjacent pair.

The canonical QQ1 corollary alone specializes to the greatest family
\(\mathcal K\), exactly as C-166 and C-167 do.

## 2. Bow-tie vertex sets

Let \(ux\) be supported and one-sided active, and fix
\(z\in Z=W_{ux}\).  Since \(\gamma=3\), no pair dominates.  Therefore

\[
 Z,\quad P_z=W_{uz},\quad Q_z=W_{xz}
\]

are all nonempty.  The supported-pair theorem applied to \(ux\) retains
\(R_z=\{u,x,z\}\) and makes \(Z\) a clique.  Each of \(P_z,Q_z\) is a
clique: two nonadjacent members together with the defining independent
pair would form an independent four-set, contradicting \(\alpha=3\).

For \(g\in P_z\), the retained dominating state \(R_z\) covers \(g\).
Its \(u,z\) guards miss \(g\), so \(xg\) is forced.  Similarly
\(uh\) is forced for \(h\in Q_z\).  A vertex in
\(P_z\cap Q_z\) would miss all three guards of \(R_z\), hence the two
sides are disjoint.

The state \(S_g=\{u,z,g\}\) is independent and retained.  Transporting
the assumed \(u\to x\) activity by C-108 retains
\(X_g=\{x,z,g\}\).  Since \(X_g\) dominates every \(h\in Q_z\), while
\(x,z\) miss \(h\), the edge \(gh\) is forced.  Thus every cross edge
exists and \(P_z\cup Q_z\) is a clique.

This proves every nonempty, disjointness, internal-clique, and
complete-join assertion without a freshness assumption.

## 3. Omitted side and mixed-state forcing

For \(h\in Q_z\), the state \(T_h=\{x,z,h\}\) is independent and retained.
If \(O_h=\{u,z,h\}\) were retained, the independent source \(T_h\) would
witness \(x\triangleright_{\mathcal F}u\), contradicting the one-sided
hypothesis.  This is a family-membership implication; no graph nonedge is
inferred.

Now attack the unoccupied vertex \(h\) from
\(S_g=\{u,z,g\}\).  The vertex \(h\) is distinct from every guard:
\(h\ne z,x\) by definition of \(Q_z\), \(h\ne u\) because \(ux\) is an
edge, and \(h\ne g\) because \(P_z,Q_z\) are disjoint.  Exactly two
guards are graph-eligible:

\[
\begin{array}{c|c}
g\to h & \{u,z,h\}=O_h\notin\mathcal F,\\
u\to h & \{z,g,h\}=M_{g,h}.
\end{array}
\]

The \(z\)-guard misses \(h\).  Eternal closure therefore uniquely forces
the retained mixed state \(M_{g,h}\).

The four claimed activities use literal independent sources and retained
one-guard endpoints:

\[
\begin{array}{c|c|c}
\text{move}&\text{source}&\text{endpoint}\\ \hline
u\to h&S_g&M_{g,h}\\
h\to u&T_h&R_z\\
x\to g&T_h&M_{g,h}\\
g\to x&S_g&R_z.
\end{array}
\]

Every target is unoccupied, and the relevant mover edge is one of
\(uh,xg,gh,ux\).  At the \(h\to u\) attack, the only competing physical
response is \(x\to u\), whose endpoint is the already omitted \(O_h\);
the \(z\)-guard is ineligible.  Hence the displayed response is also
forced.

## 4. Entire fan statuses

The vertex \(z\) is a common nonneighbor of the edge \(uh\), and its
central state \(O_h\) is omitted.  C-172 therefore places the entire
\(uh\) central fan in the omitted branch.  This also agrees with the
explicit reciprocal activity proved above.

The retained state \(X_g\) co-occupies the edge \(xg\), with
\(z\in W_{xg}\).  The retained state \(M_{g,h}\) co-occupies the edge
\(gh\), with \(z\in W_{gh}\).  The supported-pair theorem therefore
retains both entire central fans and makes both common-nonneighbor sets
cliques.

The proof correctly allows a retained-fan edge to be reciprocal:
\(xg\) has both properties.  It does not claim reciprocity for the cross
edge \(gh\).

## 5. Canonical QQ1 coupling

In canonical QQ1, C-166 supplies \(\{u,x,d\}\in\mathcal K\) for every
\(d\in C_{xr}\).  Since \(\gamma=3\), this completion set is nonempty,
so the edge \(ux\) is supported.  The bow-tie theorem consequently
applies to every \(z\in W_{ux}\).

Fix \(w\in W_{ud}\) and \(z\in W_{ux}\).  C-167 retains
\(\{u,w,z\}\).  C-166 gives \(wx\in E(G)\), while \(z\) misses \(x\);
therefore \(w\ne z\).  The two graph cases are exhaustive:

- If \(wz\) is absent, then \(wu,wz\) are absent, so
  \(w\in P_z=W_{uz}\).  All stated cross edges, mixed states,
  reciprocity of \(xw\), and retention of its central fan are direct
  instances of the bow-tie theorem.
- If \(wz\) is present, the retained bridge supports the edge \(wz\).
  Since \(wu,zu\) are absent, \(u\in W_{wz}\).  The supported-pair
  theorem retains every \(\{w,z,e\}\), makes \(W_{wz}\) a nonempty
  clique, and forces every other member of that clique adjacent to \(u\).

The collision \(w=z\) is explicitly excluded before the split.  In the
edge branch, the possible central-fan collision \(e=u\) is simply the
already retained bridge; the supported-pair theorem makes no occupied
attack in that case.

## 6. Independent computation

`verify_clean.py` shares no transition core or data structure with the
candidate verifier.  It uses immutable neighbor sets and frozenset guard
states.  It independently exhausts all 1,096 labeled graphs on orders
three through five and every eternal subfamily of dominating triples in
the equality-static slice.  The resulting coverage is:

\[
\begin{array}{c|r}
\text{applicable graphs}&107\\
\text{arbitrary eternal families}&197\\
\text{supported asymmetric orientations}&120\\
\text{bow-tie witness/cell obligations}&120/120.
\end{array}
\]

Every obligation passes, including the exact two physical responses at
the mixed-state attack, all four displayed activities, entire retained
and omitted fans, side disjointness, and union-clique status.

The verifier also reconstructs:

1. `D]?`, with
   \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), the specified
   five-state arbitrary eternal family, orientation \(1\to2\) but not
   \(2\to1\), and singleton sides \(P=\{0\},Q=\{3\}\).
2. The labeled order-18 C-169 control
   `QslallyN\~Y^v^|^z~~V|ve~^}G`, with 114 edges,
   \((2,3,3,3,3)\), greatest triple-family size 473,
   \(C_{xr}=\{7\}\), \(W_{ux}=\{9\}\), \(W_{ud}=\{8\}\),
   \(P=\{6\}\), \(Q=\{10\}\), and \(W_{8,9}=\{0\}\).
   It independently counts all 30 dominating pairs.

The order-18 graph is used only as a \(\gamma=2\) boundary control.  It
is not promoted as an instance of the equality theorem or as a
gamma--theta counterexample.

## 7. Scope verdict

No proof step:

- attacks an occupied vertex;
- moves more than one guard;
- uses a complement edge as a guard move;
- infers graph nonadjacency from family omission;
- assumes a fresh witness;
- treats the arbitrary-family theorem as greatest-family-only;
- promotes a boundary control into an equality result.

No mathematical defect, quantifier gap, collision error, activity
direction error, or scope inflation was found.

Best-guess hostile-review completion: **100%**.  Best-guess complete
\(k=3\) proof-lane completion after this normal form: **about 58%**, a
workload estimate rather than a probability.
