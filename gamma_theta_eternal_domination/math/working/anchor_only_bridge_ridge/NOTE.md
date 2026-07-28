# Anchor-only odd defects force a retained shared-color bridge

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model:
attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained configuration dominates.

This note continues the accepted first-cross-clause theorem C-129.  Let

\[
 S=\{u,v,w\}\in\mathcal F
\]

be independent in an eternal family of dominating triples.  In the odd--odd
first-clause type, let the singleton terminals satisfy

\[
 L(s)=\{v\},\qquad L(t)=\{u\},
\tag{0.1}
\]

where \(L(q)\) is the family-response list: \(a\in L(q)\) means both
\(aq\in E(G)\) and \(S-a+q\in\mathcal F\).  Thus list membership records a
legal one-guard move from the reference state, not merely membership of the
resulting set in the family.

and let their defect ridges be

\[
 Z_s=N_{\overline G}(w)\cap N_{\overline G}(s),\qquad
 Z_t=N_{\overline G}(w)\cap N_{\overline G}(t).
\tag{0.2}
\]

C-129 proves that these are nonempty disjoint \(G\)-cliques.  The exact
escape left there is that both could be anchor-only:

\[
 Z_s=\{u\},\qquad Z_t=\{v\}.
\tag{0.3}
\]

The new conclusion is:

> **PROVED.** Under (0.3), the missed set
> \[
> W=N_{\overline G}(s)\cap N_{\overline G}(t)
> \]
> is a nonempty \(G\)-clique outside \(S\cup\{s,t\}\).  The state
> \(\{w,s,t\}\) is retained, every \(\{s,t,z\}\) with \(z\in W\) is
> retained, and
> \[
> w\in L(z)
> \quad(z\in W).
> \]
> Since response lists are nonempty and proper, every bridge vertex has
> one of the exact lists
> \[
> \{w\},\qquad\{u,w\},\qquad\{v,w\}.
> \]

Moreover, the bridge lies entirely in the two original supporting
components: singleton-\(w\) vertices lie in their intersection,
\(\{u,w\}\)-vertices lie in the frozen-\(v\) component, and
\(\{v,w\}\)-vertices lie in the frozen-\(u\) component.

Thus the simultaneous anchor-only escape is not dynamically empty.  It
forces a retained shared-color bridge ridge.  This does **not** prove that
the first clause is impossible: the bridge vertices may already be support
vertices or ports, and all three displayed list types remain locally
consistent.  Even arms, longer chains, complete \(k=3\), and the universal
gamma--theta conjecture remain open.

No literature-priority claim is made.

## 1. Imported first-clause geometry

Put \(H=\overline G\).  The complete C-129 setup includes:

1. \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\);
2. every outside response list at \(S\) is nonempty and proper;
3. \(s\) lies in a free component \(K\) of the frozen-\(u\) complement
   projection and \(t\) lies in a free component \(M\) of the
   frozen-\(v\) projection;
4. the shared anchor \(w\) is \(G\)-adjacent to every vertex of
   \(K\cup M\); and
5. the direct singleton states
   \[
   D_s=\{u,w,s\},\qquad D_t=\{v,w,t\}
   \tag{1.1}
   \]
   belong to \(\mathcal F\).

We also use the accepted arbitrary-state restoration theorem.  If
\(D\in\mathcal F\) and \(S\) is the independent reference state, then

\[
 S-D\subseteq\bigcup_{q\in D-S}L(q).
\tag{1.2}
\]

No missing family response will be treated as a graph nonedge.

## 2. The two odd terminals have a retained common state

### Lemma 2.1

Under (0.1),

\[
 \boxed{\{w,s,t\}\in\mathcal F.}
\tag{2.1}
\]

#### Proof

Attack the unoccupied vertex \(t\) from the retained state

\[
 D_s=\{u,w,s\}.
\]

The vertices \(s,t\) are distinct because their exact response lists are
different.  The move \(u\to t\) is available because \(u\in L(t)\), and it
produces \(\{w,s,t\}\).

There are at most two other guard choices.

- If \(w\) moved, the proposed successor would be
  \(\{u,s,t\}\).  Relative to \(S\), its missing anchors are \(v,w\),
  while its outside positions have list union
  \[
  L(s)\cup L(t)=\{u,v\}.
  \]
  This misses \(w\), contradicting (1.2).  Hence this state is not in
  \(\mathcal F\).
- If \(s\) is adjacent to \(t\) and moved, the proposed successor would be
  \(\{u,w,t\}\).  Its only outside position is \(t\), while its missing
  anchor is \(v\); but \(v\notin L(t)=\{u\}\).  Again (1.2) excludes the
  state.  If \(st\notin E(G)\), this move is physically unavailable
  anyway.

Eternal closure therefore forces \(u\to t\), proving (2.1). \(\square\)

The proof does not assume whether \(s\) and \(t\) are adjacent.

## 3. The anchor-only bridge ridge

Assume from now on the simultaneous anchor-only hypothesis (0.3), and put

\[
 W=N_H(s)\cap N_H(t).
\tag{3.1}
\]

### Theorem 3.1 (retained shared-color bridge)

The set \(W\) has all of the following properties.

1. \(W\ne\varnothing\).
2. \(W\cap(S\cup\{s,t\})=\varnothing\).
3. Every \(z\in W\) is adjacent to \(w\) in \(G\).
4. For every \(z\in W\),
   \[
   \{s,t,z\}\in\mathcal F
   \quad\text{and}\quad
   w\in L(z).
   \tag{3.2}
   \]
5. \(G[W]\) is a clique.  For distinct \(z,z'\in W\), the attack at
   \(z'\) from \(\{s,t,z\}\) uniquely moves \(z\to z'\).

#### Proof

The pair \(\{s,t\}\) does not dominate because \(\gamma(G)=3\).  Its
missed set is exactly \(W\), proving (1).

The anchors \(u,v,w\) do not belong to \(W\):

- \(ut\in E(G)\), because \(u\in L(t)\);
- \(vs\in E(G)\), because \(v\in L(s)\); and
- \(ws,wt\in E(G)\), by the shared-anchor completeness from C-129.

The absence of loops excludes \(s,t\), proving (2).

Take \(z\in W\).  If \(wz\in E(H)\), then

\[
 z\in N_H(w)\cap N_H(s)=Z_s=\{u\},
\]

contrary to (2).  Therefore \(wz\in E(G)\), proving (3).

Now attack the unoccupied vertex \(z\) from the retained state
\(\{w,s,t\}\) of Lemma 2.1.  The guards at \(s,t\) cannot move, because
\(sz,tz\in E(H)\).  The sole possible guard is \(w\), and (3) gives its
move edge.  Eternal closure forces

\[
 w\longrightarrow z,\qquad \{s,t,z\}\in\mathcal F.
\tag{3.3}
\]

Apply restoration (1.2) to this state.  It is disjoint from \(S\), so the
three anchors \(u,v,w\) must lie in

\[
 L(s)\cup L(t)\cup L(z)
 =\{u,v\}\cup L(z).
\]

Consequently \(w\in L(z)\), proving (4).

Finally take distinct \(z,z'\in W\).  The retained state
\(\{s,t,z\}\) must dominate \(z'\).  Both \(s\) and \(t\) miss \(z'\), so
\(zz'\in E(G)\).  At the unoccupied attack \(z'\), the first two guards
again have no move edge; hence \(z\to z'\) is the unique response.  This
proves (5). \(\square\)

This proof uses the anchor-only hypothesis only to force \(wz\in E(G)\).
The bridge itself is then a literal two-attack consequence:

\[
 \{u,w,s\}\xrightarrow[\text{attack }t]{u\to t}
 \{w,s,t\}
 \xrightarrow[\text{attack }z]{w\to z}
 \{s,t,z\}.
\tag{3.4}
\]

## 4. Exact bridge lists and component locations

Because all outside lists are nonempty and proper, Theorem 3.1 gives the
exhaustive list trichotomy

\[
 L(z)\in
 \bigl\{\{w\},\{u,w\},\{v,w\}\bigr\}
 \qquad(z\in W).
\tag{4.1}
\]

Write

\[
\begin{aligned}
 W_w&=\{z\in W:L(z)=\{w\}\},\\
 W_{uw}&=\{z\in W:L(z)=\{u,w\}\},\\
 W_{vw}&=\{z\in W:L(z)=\{v,w\}\}.
\end{aligned}
\tag{4.2}
\]

### Corollary 4.1 (bridge location)

\[
 \boxed{
 W_w\subseteq K\cap M,\qquad
 W_{uw}\subseteq M-K,\qquad
 W_{vw}\subseteq K-M.
 }
\tag{4.3}
\]

#### Proof

If \(z\in W_w\), then \(u,v\notin L(z)\).  Thus \(z\) belongs to both
frozen projections.  The complement edge \(sz\) joins it to
\(s\in K\), so it lies in \(K\); similarly \(tz\) puts it in \(M\).

If \(z\in W_{uw}\), then it omits \(v\), and the edge \(tz\) puts it in
the same frozen-\(v\) component \(M\) as \(t\).  It does not even belong
to the frozen-\(u\) vertex set, because \(u\in L(z)\), so it is not in
\(K\).  The \(W_{vw}\) case is symmetric. \(\square\)

A singleton-\(w\) bridge vertex lies one complement edge beyond each odd
pin.  It therefore has even parity from both original clause ports and can
serve as a common even--even pin.  This is a structural conversion, not a
contradiction.

## 5. Consequence for the odd--odd escape

Combining C-129 with Theorem 3.1 gives the following exact dichotomy.

### Corollary 5.1

Every odd--odd first-clause core satisfies at least one of:

1. \(Z_s-\{u\}\ne\varnothing\);
2. \(Z_t-\{v\}\ne\varnothing\); or
3. both terminal ridges are anchor-only and the nonempty retained bridge
   ridge \(W\) of Theorem 3.1 exists.

Thus the simultaneous anchor-only case cannot end with only the two
anchors.  It creates a family-saturated \(G\)-clique of shared-color
vertices carried by \(K\cup M\).

The third alternative may use vertices already present on the two support
arms.  No order increase follows without an additional separation
argument.  The unresolved next step is to show that one of the bridge list
types shortens the Boolean obstruction, creates an external static defect,
or is incompatible with a second attack outside \(W\).

## 6. Claim boundary

The rigorous result is a local dynamic theorem about the odd--odd
first-clause geometry.  It does not:

- exclude a common singleton-\(w\) bridge;
- exclude either two-list bridge type;
- prove that \(W\) contains a vertex outside \(K\cup M\);
- handle even support arms;
- eliminate longer one-/two-unit chains or residual bicycles;
- prove complete \(k=3\); or
- resolve the universal gamma--theta conjecture.
