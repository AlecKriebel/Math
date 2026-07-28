# Hostile review: the simultaneous anchor-only bridge ridge

## Verdict

**PASS after two proof-clarifying corrections, with strict scope.**

The corrected candidate proves its two local conclusions from the accepted
C-129 odd--odd first-clause hypotheses.  Every attack is at an unoccupied
vertex, each forced transition moves exactly one adjacent guard, and every
state asserted to be retained follows from eternal closure after every other
possible retained successor has been excluded.

The original manifest supplied for review was

```text
6874f6611930e8abf9e0fad001548f5452822157a86f119544e36b2913239f60
```

Its argument was mathematically recoverable, but two sentences left avoidable
formal ambiguity:

1. it inherited a response-list notation without restating that list
   membership includes the move edge; and
2. it attacked \(t\) from a state containing \(s\) without explicitly
   recording why \(s\ne t\).

The candidate was corrected to define the family-response list as the legal
direct swap list and to note that the exact, unequal lists
\(L(s)=\{v\}\) and \(L(t)=\{u\}\) force \(s\ne t\).  No theorem statement
or mathematical mechanism changed.  The corrected frozen candidate manifest
is

```text
math/working/anchor_only_bridge_ridge/MANIFEST.json
SHA-256 fe0d52a955d3a98ef98454b63ddc8ae129713e574b6063a91d28f25c66f3f005
```

This review accepts exactly:

1. retention of the common terminal state \(\{w,s,t\}\);
2. nonemptiness and externality from \(S\cup\{s,t\}\) of
   \(W=N_{\overline G}(s)\cap N_{\overline G}(t)\);
3. retention of every \(\{s,t,z\}\), \(z\in W\), and the forced inclusion
   \(w\in L(z)\);
4. the fact that \(W\) is a clique of \(G\) with unique ridge exchanges;
5. the exact list trichotomy
   \(\{w\},\{u,w\},\{v,w\}\); and
6. the stated locations in the two frozen supporting components.

It does not accept an exclusion of the first cross clause, a new vertex or
order count, an exclusion of any of the three bridge-list types, complete
\(k=3\), or the universal gamma--theta conjecture.

## Frozen inputs

The two files named by the corrected candidate manifest match:

```text
NOTE.md
6e1d4a866889538324faeef4a0d6713577042a660a72d266bf5c79bf51069fa1

RESEARCH_LOG.md
4600f518cbbf15ec53593c3d3f2385b71994b3a3cff0a87000c8ddf0df9a08cf
```

The accepted C-129 dependency was also pinned:

```text
math/working/first_cross_clause_attack/NOTE.md
d845635c3df454f7809dde5b6dc089e4c9a7076b106cf19c264d62998e311413

math/working/first_cross_clause_attack/MANIFEST.json
2e157de3ce02eda7eee2cff65d2af064eb7b9103a6f2b3d16772ede44d4e86b0
```

The restoration theorem was checked against its original accepted proof in
`math/working/k3_cross_state_attack.md`, SHA-256
`3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68`.
It applies to every state of the specified family, not only to independent
states or direct successors of \(S\).

## Line-by-line mathematical audit

Throughout, \(S=\{u,v,w\}\) is independent,
\(L(s)=\{v\}\), \(L(t)=\{u\}\), and

\[
 Z_s=N_{\overline G}(w)\cap N_{\overline G}(s)=\{u\},
 \qquad
 Z_t=N_{\overline G}(w)\cap N_{\overline G}(t)=\{v\}.
\]

The accepted C-129 geometry supplies the retained direct state
\(D_s=\{u,w,s\}\), makes \(w\) adjacent in \(G\) to both terminals, and
places the terminals in the named frozen free components.

### 1. The attack at \(t\) really forces \(u\to t\)

The attack is unoccupied: \(s,t\notin S\), and the unequal exact response
lists imply \(s\ne t\).  Since \(u\in L(t)\), the corrected legal-list
definition supplies both \(ut\in E(G)\) and the direct retained state
\(S-u+t\).  Thus \(u\to t\) is a physical move edge from \(D_s\).

All three guards of \(D_s\) have been considered:

- a move \(w\to t\) would produce \(\{u,s,t\}\).  Relative to \(S\), this
  state misses \(v,w\), while
  \(L(s)\cup L(t)=\{u,v\}\).  Arbitrary-state restoration excludes it;
- a move \(s\to t\), if \(st\in E(G)\), would produce
  \(\{u,w,t\}\).  It misses \(v\), but its only outside list is
  \(L(t)=\{u\}\), so restoration excludes it.  When \(st\notin E(G)\), the
  move is unavailable already; and
- the remaining legal response is \(u\to t\), producing
  \(\{w,s,t\}\).

Eternal closure therefore retains \(\{w,s,t\}\).  This argument does not
assume either value of \(st\).

### 2. The common missed set is nonempty and genuinely outside

Because \(\gamma(G)=3\), the two-set \(\{s,t\}\) cannot dominate.  Its
missed vertices are exactly

\[
W=N_{\overline G}(s)\cap N_{\overline G}(t),
\]

so \(W\ne\varnothing\).

No named collision was missed:

- \(u\notin W\) because \(ut\in E(G)\);
- \(v\notin W\) because \(vs\in E(G)\);
- \(w\notin W\) because C-129 gives \(ws,wt\in E(G)\); and
- \(s,t\notin W\) because the complement neighborhoods are open.

Thus every \(z\in W\) is outside \(S\cup\{s,t\}\).  The ports \(x,y\) and
internal support vertices are not excluded, and the candidate correctly
makes no claim that a bridge vertex is new.

### 3. The anchor-only hypothesis forces \(wz\in E(G)\)

For \(z\in W\), the edge \(sz\) lies in \(\overline G\).  If \(wz\) also
lay in \(\overline G\), then

\[
z\in N_{\overline G}(w)\cap N_{\overline G}(s)=Z_s=\{u\}.
\]

Section 2 already proves \(z\ne u\), a contradiction.  Hence
\(wz\in E(G)\).  This is a literal graph-edge inference from the
anchor-only set equality; it does not convert absence from a family into a
graph nonedge.

### 4. The second attack has a unique legal guard

Attack \(z\in W\) from the retained state \(\{w,s,t\}\).  It is
unoccupied by Section 2.  The complement incidences \(sz,tz\) prevent the
two terminal guards from moving, while Section 3 supplies the edge \(wz\).
Thus the unique possible guard is \(w\), and closure forces

\[
w\to z,\qquad \{s,t,z\}\in\mathcal F.
\]

The resulting state dominates because every state of \(\mathcal F\) does.

This state is disjoint from \(S\).  Arbitrary-state restoration therefore
requires all of \(u,v,w\) to occur in

\[
L(s)\cup L(t)\cup L(z)=\{u,v\}\cup L(z),
\]

which forces \(w\in L(z)\).  This is a family-response conclusion, not a
static-list conclusion.

### 5. The ridge is a retained \(G\)-clique

Let \(z,z'\in W\) be distinct.  The retained state \(\{s,t,z\}\) must
dominate the unoccupied vertex \(z'\).  Both terminals miss \(z'\), so
necessarily \(zz'\in E(G)\).  At an attack on \(z'\), neither terminal
has a move edge; consequently \(z\to z'\) is the unique response and
\(\{s,t,z'\}\) is retained.  This proves both the \(G\)-clique assertion
and the exchange statement, including the singleton-\(W\) case
vacuously.

### 6. The list trichotomy is exact

Every bridge vertex is outside \(S\).  Under the imported no-full,
no-empty hypothesis, its list is a nonempty proper subset of
\(\{u,v,w\}\).  Section 4 forces \(w\) into it.  The only possibilities
are therefore

\[
\{w\},\qquad \{u,w\},\qquad \{v,w\}.
\]

No fourth list is omitted, and the full list is excluded only by the
explicit proper-list hypothesis.

### 7. Frozen-component locations

The frozen-\(u\) projection contains an outside vertex exactly when its
list omits \(u\); the frozen-\(v\) projection has the symmetric rule.
Moreover \(sz,tz\in E(\overline G)\).

- If \(L(z)=\{w\}\), then \(z\) belongs to both projection vertex sets.
  The edge \(sz\) puts it in \(K\), and \(tz\) puts it in \(M\).
- If \(L(z)=\{u,w\}\), then \(z\) belongs to the frozen-\(v\) projection
  and \(tz\) puts it in \(M\).  Because its list contains \(u\), it is not
  even a vertex of the frozen-\(u\) projection and hence cannot lie in
  \(K\).
- If \(L(z)=\{v,w\}\), the symmetric argument puts it in \(K-M\).

Thus

\[
W_w\subseteq K\cap M,\qquad
W_{uw}\subseteq M-K,\qquad
W_{vw}\subseteq K-M.
\]

The statement means that bridge vertices lie in the union of the two
already present supporting components.  It does not prove that they are
distinct from ports or other support vertices, and the candidate states
that limitation correctly.

## Clean-room symbolic replay

`independent_checker.py` imports no candidate or campaign module.  It
exhausts all six nonempty proper response-list masks, verifies the two
restoration exclusions in the first attack, derives exactly the three
bridge lists, checks all named anchor/terminal collisions, and reconstructs
the frozen-component membership table.

Run from the campaign directory:

```text
python3 -I -B -W error \
  reviews/anchor_only_bridge_hostile/independent_checker.py
```

The generated result must have SHA-256

```text
284a08dca64862d0595874873d899324e2bf13ddf749920f629937a741819303
```

The finite replay is corroborative.  The proof audit above establishes the
quantified theorem for arbitrary graphs and arbitrary specified eternal
families satisfying the hypotheses.

## Scope boundary

The proof uses the simultaneous anchor-only equalities only to obtain
\(wz\in E(G)\).  It then converts the escape into a retained shared-color
ridge.  It supplies no contradiction: a bridge vertex can already be a
port or support vertex, and each of the three exact list types is still
allowed.

Accordingly, longer chains, even arms, the complete singleton branch,
complete \(k=3\), and the universal gamma--theta conjecture all remain
open.
