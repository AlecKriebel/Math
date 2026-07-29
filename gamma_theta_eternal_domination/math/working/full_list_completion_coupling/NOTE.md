# Supported pair fans in the terminal-completion layer

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It uses
the standard one-guard-moves model: attacks occur only at unoccupied
vertices, exactly one adjacent guard moves, and the successor remains in
the same eternal family.

The first theorem is a general parameter-three fact.  Every pair of guards
co-occupied in a retained triple has its entire non-domination witness fan
retained.  Applied to a C-170 terminal-completion branch, this gives a
uniform fan for every completion, not merely one selected private witness.

The second theorem couples that fan to the full target.  Either the
corresponding cross state dominates, or the target--anchor edge is
family-active in both directions.  Thus, if neither of the two secondary
target edges is reciprocal, every completion in C-170 has a retained
branch with both a complete supported fan and a dominating cross state.

This is a size-independent cover constraint.  It does not force the cross
state to belong to the family, compare deletion ranks, produce a safe
color, complete parameter three, or resolve the gamma--theta conjecture.
No literature-priority claim is made.

## 1. Definitions

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{1.1}
\]

and let \(\mathcal F\) be any eternal family of dominating triples.  For
distinct vertices \(a,b\), put

\[
 W_{ab}=
 \{z\in V(G)-\{a,b\}:az,bz\notin E(G)\}.
\tag{1.2}
\]

Thus \(W_{ab}\) is exactly the set missed by the pair \(\{a,b\}\).  It is
nonempty because \(\gamma(G)=3\).

For an edge \(ab\), write

\[
 a\mathrel{\triangleright_{\mathcal F}}b
\tag{1.3}
\]

when an independent triple in \(\mathcal F\), containing \(a\) and not
\(b\), has the retained response obtained by moving \(a\to b\).  This is
the activity relation used in accepted C-172.

## 2. Every supported pair has a retained central fan

### Theorem 2.1 (supported-pair fan saturation) — PROVED

Let

\[
 D=\{a,b,c\}\in\mathcal F.
\tag{2.1}
\]

Then

\[
 \boxed{\{a,b,z\}\in\mathcal F\quad\text{for every }z\in W_{ab}.}
\tag{2.2}
\]

The set \(W_{ab}\) is a clique in \(G\).  More precisely, if
\(z\ne c\), then

\[
 cz\in E(G)
\tag{2.3}
\]

and the attack at the unoccupied vertex \(z\) from \(D\) has the unique
response

\[
 D\xrightarrow[\text{attack }z]{c\to z}\{a,b,z\}.
\tag{2.4}
\]

If \(z=c\), (2.2) is simply the assumed membership of \(D\); no occupied
attack is asserted.

#### Proof

Fix \(z\in W_{ab}\).  If \(z=c\), there is nothing to prove.  Suppose
\(z\ne c\).  The retained state \(D\) dominates \(z\).  The guards
\(a,b\) both miss \(z\), so \(c\) must hit \(z\).  At the attack on \(z\),
the guards \(a,b\) are ineligible and \(c\) is the unique eligible guard.
Eternal closure proves (2.4).

Now take distinct \(z,z'\in W_{ab}\).  The retained state
\(\{a,b,z\}\) dominates \(z'\).  Since \(a,b\) miss \(z'\), the guard
at \(z\) must hit \(z'\).  Hence \(W_{ab}\) is a clique. \(\square\)

This is stronger than applying C-172 without the co-occupied state \(D\).
C-172 allows an adjacent pair to have an omitted central fan and
reciprocal activity.  Theorem 2.1 says that a pair occurring together in
any retained triple is forced into the retained-fan branch.

## 3. A completion fan either crosses or creates reciprocity

Fix an independent root

\[
 S=\{u,v,t\}\in\mathcal F
\tag{3.1}
\]

and a vertex \(x\notin S\) that is full at \(S\):

\[
 sx\in E(G)
 \quad\text{and}\quad
 S-s+x\in\mathcal F
 \qquad(s\in S).
\tag{3.2}
\]

In particular, every \(sx\) is a graph edge and

\[
 s\mathrel{\triangleright_{\mathcal F}}x
\qquad(s\in S).
\tag{3.3}
\]

Put

\[
 B=N_{\overline G}(x).
\tag{3.4}
\]

Let \(r\in B\), and let \(d\) be a common nonneighbor of \(x,r\):

\[
 dx,dr,xr\notin E(G).
\tag{3.5}
\]

Thus

\[
 I=\{x,r,d\}
\tag{3.6}
\]

is a maximum independent triple and belongs to every eternal
triple-family.  Suppose that the completion branch

\[
 D_t(d)=\{d,t,r\}
\tag{3.7}
\]

belongs to \(\mathcal F\).  No assumption is made that this state was the
physical response by which the terminal was first entered.

Define the cross state

\[
 X_t(d)=\{x,d,t\}.
\tag{3.8}
\]

### Theorem 3.1 (fan--reciprocity dichotomy) — PROVED

Under (1.1) and (3.1)--(3.7):

1. every state
   \[
     \{d,t,e\}\qquad(e\in W_{dt})
   \tag{3.9}
   \]
   belongs to \(\mathcal F\);
2. the missed set of the cross state is exactly
   \[
     V(G)-N_G[X_t(d)]=W_{dt}\cap B;
   \tag{3.10}
   \]
   hence
   \[
     X_t(d)\text{ dominates}
     \quad\Longleftrightarrow\quad
     W_{dt}\cap B=\varnothing;
   \tag{3.11}
   \]
3. if \(X_t(d)\) does not dominate, then
   \[
     x\mathrel{\triangleright_{\mathcal F}}t
     \quad\text{and}\quad
     t\mathrel{\triangleright_{\mathcal F}}x.
   \tag{3.12}
   \]

Thus the two cases distinguished by domination are exact:

\[
\boxed{
\begin{array}{ll}
W_{dt}\cap B=\varnothing
 &\Longrightarrow X_t(d)\text{ dominates};\\[1mm]
W_{dt}\cap B\ne\varnothing
 &\Longrightarrow X_t(d)\text{ is nondominating and }xt
   \text{ is reciprocal.}
\end{array}}
\tag{3.13}
\]

The edge \(xt\) may also be reciprocal in the first case.

#### Proof

Item 1 is Theorem 2.1 applied to \(D_t(d)\).

A vertex is missed by \(X_t(d)=\{x,d,t\}\) exactly when it misses
\(d,t\) and also misses \(x\).  Because \(xt\in E(G)\), the vertex \(x\)
is not itself in \(W_{dt}\).  Equations (3.4) and (1.2) therefore give
(3.10), and (3.11) follows.

Suppose \(W_{dt}\cap B\ne\varnothing\), and choose
\(e\) in that intersection.  The triple

\[
 J_e=\{x,d,e\}
\tag{3.14}
\]

is independent: \(xd\) is absent by (3.5), while \(de\) is absent by
\(e\in W_{dt}\), and \(xe\) is absent by \(e\in B\).  Hence
\(J_e\in\mathcal F\).

Attack the unoccupied vertex \(t\) from \(J_e\).  The guard at \(x\) is
eligible because \(xt\) is an edge, and its successor is

\[
 J_e-x+t=\{d,t,e\},
\tag{3.15}
\]

which is retained by item 1.  Thus
\(x\triangleright_{\mathcal F}t\).  Conversely, (3.2) says that the
independent root \(S\) retains the response \(t\to x\), so
\(t\triangleright_{\mathcal F}x\).  This proves (3.12).

The proof remains literal if \(e=r\).  Then \(J_e=I\) and the retained
endpoint in (3.15) is the original branch \(D_t(d)\); no attack is made
at an occupied vertex. \(\square\)

No family omission is converted into a graph nonedge.  The theorem
distinguishes domination of \(X_t(d)\), not membership of that state in
\(\mathcal F\).

## 4. Uniform consequence for the C-170 completion clique

Return to accepted C-170's rank-zero nonroot corridor:

\[
 T=\{v,t,q\},\qquad E=\{v,t,r\},
\tag{4.1}
\]

at the full target \(x\).  Suppose the terminal palette is full, so the
two secondary witnesses and C-170's two-witness cover are available.
For every \(d\in C_{xr}\), attacking \(d\) from \(E\) retains at least
one of

\[
 \{d,t,r\},\qquad \{v,d,r\}.
\tag{4.2}
\]

### Corollary 4.1 (completion-fan cover) — PROVED

For every \(d\in C_{xr}\), there is an anchor

\[
 c\in\{v,t\}
\tag{4.3}
\]

whose branch \(\{d,c,r\}\) is retained and for which:

\[
 \{d,c,e\}\in\mathcal F
\qquad(e\in W_{dc}),
\tag{4.4}
\]

and either

\[
 \{x,d,c\}\text{ dominates}
\tag{4.5}
\]

or \(xc\) is family-active in both directions.

In particular, if neither \(xv\) nor \(xt\) is reciprocal, then every
completion \(d\in C_{xr}\) has a retained branch satisfying both the
complete fan (4.4) and the dominating cross-state condition (4.5).

#### Proof

The physical attack at \(d\) from \(E\) has no response by \(r\), since
\(dr\) is absent.  Eternal closure supplies a retained physical response
by \(v\) or \(t\), giving at least one state in (4.2).  Apply Theorem 3.1
with \(c=t\) to the first branch or with \(c=v\) to the second.  The last
assertion is the contrapositive of (3.12). \(\square\)

A branch state can happen to be retained even when its corresponding
terminal-entry move edge is absent.  Corollary 4.1 uses one branch
actually supplied by the attack at \(d\); Theorem 3.1 itself applies to
every retained branch state and never infers how that state was entered.

## 5. Exact controls and sharp boundary

The standalone verifier reconstructs the 16-vertex equality graph

```text
OYifur}UO]}iTij]tpo]v
```

with

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
\qquad |\mathcal F^\star|=304.
\tag{5.1}
\]

It checks three sharp branches.

1. **Nondominating/reciprocal.**
   \[
   S=\{0,1,10\},\ x=6,\ r=5,\ d=7,\ t=1.
   \]
   Here \(W_{dt}=\{5,14\}\),
   \(W_{dt}\cap B=\{5\}\), every central state is retained, the cross
   state \(\{1,6,7\}\) is nondominating and omitted, and \(x,t\) are
   active in both directions.
2. **Dominating and retained.**
   With the same \(S,x,r,d\), take \(t=0\).  Then
   \(W_{dt}=\{12\}\), the trapped intersection is empty, and
   \(\{0,6,7\}\) both dominates and belongs to \(\mathcal F^\star\).
3. **Dominating but omitted.**
   \[
   S=\{1,13,14\},\ x=12,\ r=2,\ d=7,\ t=1.
   \]
   Here \(W_{dt}=\{5,14\}\), the trapped intersection is empty, but
   the dominating cross state \(\{1,7,12\}\) is absent from
   \(\mathcal F^\star\).

The third case is essential: domination in (4.5) cannot be strengthened
to family membership or assigned a restricted deletion rank.

The gamma-two graph

```text
HF~mdfj
```

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\tag{5.2}
\]

Its accepted full-terminal completion branch
\(\{2,5,8\}\) has \(W_{2,8}=\varnothing\).  Thus the nonempty fan in
Theorem 2.1 genuinely uses \(\gamma=3\).

## 6. Exact checkpoint

### PROVED in this candidate

- Every pair co-occupied in a retained triple has its complete
  non-domination witness fan retained.
- Every retained completion branch has a uniform supported pair fan.
- The cross state dominates exactly when the supported fan avoids the
  full-target ban region.
- A trapped member of that fan forces reverse target--anchor activity.
- C-170's whole completion clique is covered by supported fans whose
  anchor edge is reciprocal or whose cross state dominates.

### EXACT finite controls

- Both domination sides of the fan--reciprocity dichotomy occur in one
  equality graph.
- A dominating cross state may be retained or omitted in that same
  equality graph.
- At gamma two the supported pair can dominate, leaving no fan.

### OPEN

- Family membership or a rank bound for a dominating cross state.
- A contradiction from iterating the supported fans across three primary
  colors.
- A surviving safe kernel, the complete \(k=3\) theorem, and the
  universal gamma--theta conjecture.
