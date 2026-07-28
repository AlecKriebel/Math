# Hostile review: bridge-side purity and the turning ridge

Date: 2026-07-28 (PDT)

## Verdict

**PASS WITH ONE REQUIRED LOCAL CORRECTION.**

The bridge-side purity inclusions, the fresh-component propagation gate,
and the turning-ridge theorem are mathematically valid under the displayed
hypotheses and the pinned accepted dependencies.  The two equality controls
also pass a clean-room reconstruction.

One displayed consequence is false as written.  Candidate equation (2.2)
states

\[
 zq\in E(G)
 \qquad(z\in W,\ q\in K_1\cup M_1).
\tag{A}
\]

But candidate equations (1.4)--(1.5) put every bridge vertex \(z\) itself
in \(K_1\cup M_1\).  Substituting \(q=z\) into (A) asserts a loop in the
simple graph \(G\).  The correct statement is

\[
 \boxed{
 zq\in E(G)
 \qquad
 (z\in W,\ q\in (K_1\cup M_1)-\{z\}).
 }
\tag{A'}
\]

The advertised special conclusion

\[
 zx,zy\in E(G)
\tag{B}
\]

is nevertheless true, but the candidate's sentence saying that it follows
from (1.3) alone omits a necessary distinctness argument.  If \(z=x\),
then the literal first-clause edge \(xy\in E(H)\) puts

\[
 y\in N_H(z)\cap M_1,
\]

contradicting \(N_H(z)\cap M\subseteq M_0\).  Thus \(z\ne x\).
Symmetrically, \(z=y\) would put
\(x\in N_H(z)\cap K_1\), contradicting the other side-purity inclusion.
Now (A') applies to \(x\in K_1\) and \(y\in M_1\), proving (B).

Accordingly, the candidate should not be promoted on its frozen bytes
without replacing (2.2) by (A') and inserting this one-paragraph
cross-edge argument before (2.3).  No change is needed to the
turning-ridge theorem.

## Exact status boundary

### REFUTED as written

Candidate equation (2.2), with \(q\) allowed to equal \(z\), is false in
a simple graph.  Its corrected distinct-vertex form (A') is proved.

### PROVED, subject only to the local correction above

1. Under the imported odd--odd simultaneous anchor-only setup, every
   bridge vertex receives the shared color \(w\) in the two selected
   component orientations.
2. For every bridge vertex \(z\),
   \[
   N_H(z)\cap K\subseteq K_0,\qquad
   N_H(z)\cap M\subseteq M_0.
   \]
3. Every bridge vertex is distinct from, and adjacent in \(G\) to, both
   original ports \(x,y\).
4. If a two-list bridge \(z\) sends an active shared-\(w\) clause to a
   compatible exact-two port, that clause cannot create a new unit in the
   original supporting component; a genuinely new Boolean variable lies
   in a different free component.
5. If \(L(z)=\{u,w\}\) and
   \(R_z=N_H(w)\cap N_H(z)\), then either \(R_z=\varnothing\) and
   \(\{w,z\}\) dominates, or \(R_z\) is a retained \(G\)-clique with the
   stated unique ridge exchanges.  Under \(\gamma(G)=3\), only the
   nonempty-ridge alternative occurs.
6. The only anchor that can lie in that ridge is \(v\), and every outside
   ridge vertex has list \(\{v\}\) or \(\{u,v\}\).  The
   \(u\leftrightarrow v\) reflection is valid.

### CERTIFIED-FINITE

The clean-room checker independently verifies:

- `FCXfO` has
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), an
  18-state greatest eternal triple kernel, 72 unoccupied-attack
  obligations, \(L(4)=\{1,2\}\), \(L(3)=\{0\}\), and the full two-vertex
  turning ridge with both directed exchanges;
- `HEhbtjK` has the same parameter vector, a 48-state greatest eternal
  triple kernel, 288 obligations, \(L(5)=\{1,2\}\),
  \(L(3)=\{0,1\}\), and the corresponding full ridge and exchanges.

These controls certify that both outside-list alternatives in the
turning-ridge theorem occur even under equality.  They do not realize the
complete C-129 anchor-only first-clause geometry and are not
counterexamples to the gamma--theta conjecture.

### OBSERVED only

The candidate research log reports that a greatest-family scan through
order nine found no full C-129 anchor-only bridge geometry.  This review
does not promote that observation: the scan is not part of the frozen
candidate manifest, and a proper eternal subfamily may have smaller
response lists than the greatest family.

### OPEN

This review does not establish:

- exclusion of a shared-color clause entering a fresh projection
  component;
- exclusion or contraction of arbitrary unit chains, lollipops, or
  bicycles;
- the complete singleton branch;
- the complete \(k=3\) case; or
- the universal gamma--theta conjecture.

## Frozen candidate and integrity

The audited candidate manifest is

```text
math/working/bridge_chain_propagation/MANIFEST.json
SHA-256 73fd244fef69206a433d51d41b88a528b65be02e0e6dde720fc39873c435b20d
```

All candidate file hashes match that manifest:

| artifact | SHA-256 |
|---|---|
| `NOTE.md` | `8ece21369bbb42cb8e8f9d1286fc72a75d095c144d153f15454fed05d8a7d043` |
| `RESEARCH_LOG.md` | `67ee841890edeb68edd7343e5b5a2a32eff10078a9e252752b77be7bb5bafbd2` |
| `verify.py` | `0ff21c68ac03f90ac3e1dd01bcbe9da6dca2ed51fc020383374d6b8a220e9ec5` |
| `result.json` | `be1dc9b9931a69c37a3b5f91aff90df61793ce066876938185455eeb7bff4d9d` |

Every dependency hash named by the candidate manifest also matches,
including the accepted side-purity, free-component polarization,
first-cross-clause, anchor-only bridge, anchor-fixed certificate, and
arbitrary-state restoration notes.

## Independent definitions and model audit

Throughout this review,

\[
S=\{u,v,w\}\in\mathcal F
\]

is an independent retained state,
\(H=\overline G\), and

\[
L(r)=\{a\in S:S-a+r\in\mathcal F\}.
\]

This abbreviated list definition is safe: if \(S-a+r\) is retained, it
must dominate the omitted anchor \(a\).  The two other members of \(S\)
miss \(a\), so \(ar\in E(G)\).  Thus membership in a family-response list
already implies the required physical move edge.  The converse is never
used.

The proof and independent checker both use the standard one-guard model:

- the attacked vertex is unoccupied;
- exactly one occupied guard moves;
- the move traverses one edge of \(G\), never an edge of \(H\);
- the successor remains in the same eternal family; and
- every retained state dominates \(G\).

No all-guards move, occupied-vertex attack, static-only successor, or
complement-color reversal was found.

## 1. Shared-color orientation

The accepted bridge-location result gives

\[
\begin{aligned}
W_w&\subseteq K\cap M,\\
W_{uw}&\subseteq M-K,\\
W_{vw}&\subseteq K-M.
\end{aligned}
\]

The selected singleton orientations are

\[
\begin{array}{c|cc}
&0\text{-side}&1\text{-side}\\ \hline
K&v&w\\
M&u&w.
\end{array}
\]

Every bridge is adjacent in \(H\) to the marker \(s\in K_0\) or
\(t\in M_0\) in each projection to which it belongs.  Bipartiteness
therefore places a \(W_w\)-vertex on \(K_1\cap M_1\), a
\(W_{uw}\)-vertex on \(M_1\), and a \(W_{vw}\)-vertex on \(K_1\).
The singleton list \(\{w\}\) or the polarized side consequently assigns
the selected local color \(w\) in all three cases.

This is a statement about the two component orientations selected by the
terminal units.  It does not assume that the entire response formula is
globally colorable.

## 2. Side-purity applications

For the \(u\)-omitting component \(K\), use the accepted side-purity
theorem with

\[
a=u,\qquad p=t,\qquad q=z.
\]

The hypotheses are exact:

- \(u\in L(t)\), so \(t\) is \(u\)-positive;
- \(t\ne z\), because the accepted bridge theorem has
  \(W\cap\{s,t\}=\varnothing\); and
- \(tz\in E(H)\) by the definition
  \(W=N_H(s)\cap N_H(t)\).

Side-purity therefore puts \(N_H(z)\cap K\) on one bipartition side.
The literal edge \(sz\in E(H)\), with \(s\in K_0\), identifies that side
as \(K_0\).

The reflected application is

\[
a=v,\qquad p=s,\qquad q=z
\]

in the \(v\)-omitting component \(M\).  Here \(v\in L(s)\),
\(sz\in E(H)\), and \(tz\in E(H)\) identifies the permitted side as
\(M_0\).  This proves both advertised inclusions without interpreting any
missing family response as a graph nonedge.

For a **distinct** vertex on \(K_1\) or \(M_1\), absence from the open
complement neighborhood does imply a \(G\)-edge.  The distinctness
qualification is exactly what is missing from candidate equation (2.2).
The original cross edge then proves the needed port distinctness and
recovers the special port-adjacency claim, as shown in the verdict.

## 3. Fresh-component propagation gate

Let \(z\in W_{uw}\) and suppose

\[
zr\in E(H),\qquad L(r)=\{v,w\}.
\]

The list intersection is exactly \(\{w\}\), so the edge is a
shared-\(w\) collision clause.  The bridge lies on \(M_1\) and receives
\(w\).  If \(r\in K\), side-purity forces \(r\in K_0\), where the
selected orientation gives \(v\).  Hence this occurrence of the clause is
already satisfied and creates no new unit.

If the clause does propagate into \(r\), then \(r\) omits \(u\) and lies
in the frozen-\(u\) projection.  The accepted anchor-fixed certificate
theorem says an exact-two vertex lies in a free, not anchor-fixed,
component.  If \(r\notin K\), its component is therefore a different free
component.  This proves precisely the candidate's fresh-variable
statement.  It does not exclude such a continuation.  The reflected
argument is identical.

## 4. Turning ridge

Assume \(L(z)=\{u,w\}\), and put

\[
R_z=N_H(w)\cap N_H(z).
\]

The set \(R_z\) is exactly the set missed by the pair \(\{w,z\}\).
Consequently,

\[
R_z=\varnothing
\quad\Longleftrightarrow\quad
\{w,z\}\text{ dominates }G.
\]

When \(\gamma(G)=3\), no pair dominates, so \(R_z\ne\varnothing\).

The response \(u\in L(z)\) supplies the retained state

\[
D=\{v,w,z\}.
\]

The anchor \(v\), if it lies in \(R_z\), already gives the required ridge
state.  No other anchor can occur: \(w\) is excluded by the open
neighborhood, while \(uz\in E(G)\) follows from \(u\in L(z)\).

For \(q\in R_z-\{v\}\), the attack at \(q\) from \(D\) is unoccupied.
The guards \(w,z\) cannot move because \(wq,zq\in E(H)\).  Eternal
closure therefore forces the sole remaining guard,

\[
v\to q,\qquad \{w,z,q\}\in\mathcal F.
\]

This is a literal one-guard transition.  Arbitrary-state restoration from
\(\{w,z,q\}\) must recover the two missing anchors \(u,v\) through the two
outside lists.  Since \(L(z)=\{u,w\}\), it forces \(v\in L(q)\).
The literal complement edge \(wq\) forces \(w\notin L(q)\).  Hence

\[
L(q)=\{v\}\quad\text{or}\quad L(q)=\{u,v\}.
\]

The list direction is correct: restoration forces the anchor missing from
\(L(z)\), namely \(v\), into \(L(q)\).

For distinct \(q,q'\in R_z\), the retained state
\(\{w,z,q\}\) must dominate the unoccupied vertex \(q'\).  Since both
\(w,z\) miss \(q'\), this forces \(qq'\in E(G)\).  At an attack on
\(q'\), the same two complement edges leave \(q\to q'\) as the unique
possible response.  Thus \(G[R_z]\) is a clique and every directed ridge
exchange is retained.

The contextual assumptions \(\alpha(G)=\gamma^\infty(G)=3\) are stronger
than this local proof needs, but they do not invalidate it.  The proof
uses \(\gamma(G)=3\), the displayed list, independence of \(S\), eternal
closure, and restoration.

## 5. Turning the collision color

For \(z\in W_{uw}\), the selected orientation gives \(z=w\).

- If \(L(q)=\{v\}\), then \(L(z)\cap L(q)=\varnothing\).
- If \(L(q)=\{u,v\}\), then the complement edge \(zq\) has only the
  collision color \(u\).

In the second case the assigned bridge color \(w\) differs from \(u\), so
the edge cannot continue the active shared-\(w\) implication.  This is a
local gate, not a claim that the overall formula is satisfiable.

## 6. Clean-room finite reconstruction

`independent_checker.py` imports no candidate file as executable code and
no campaign evaluator.  It uses:

- an independently structured graph6 decoder;
- integer-mask configurations;
- exhaustive subset tests for \(\gamma,i,\alpha\);
- a direct dynamic program for minimum clique partition;
- simultaneous greatest-fixed-point deletion over dominating
  configurations; and
- literal one-guard successors for every unoccupied attack.

The independent graph6 edge lists agree with `showg` from the pinned local
nauty build.  For each control, the checker recomputes the exact parameter
vector, all greatest-kernel states, every attack obligation, every
response list, the common-nonneighbor ridge, and both directed ridge
exchanges.

The clean-room output is

```text
reviews/bridge_chain_propagation_hostile/independent_result.json
SHA-256 0653d398df0e7e166772652c502559f5ff96d8e4786143b400173a384dda8436
```

Exact replay from the campaign directory:

```text
python3 -I -B -W error \
  reviews/bridge_chain_propagation_hostile/independent_checker.py
```

The checker prints the JSON followed by its SHA-256 line and writes the
JSON bytes to `independent_result.json`.

## Required candidate edit

The minimum mathematically adequate repair is:

1. replace candidate equation (2.2) by (A');
2. after (2.1), add the argument
   \[
   z=x\Rightarrow zy=xy\in E(H),\ y\in M_1,
   \]
   contradicting \(M\)-side purity, and its reflection ruling out
   \(z=y\); and
3. then invoke (A') with \(q=x,y\) to obtain candidate equation (2.3).

With that repair, this hostile review accepts the note at its stated
narrow propagation-gate scope.

## Revised-byte addendum: final unconditional verdict

Date: 2026-07-28 (PDT)

**UNCONDITIONAL PASS ON THE FINAL REVISED BYTES, WITH THE ORIGINAL NARROW
SCOPE.**

This addendum supersedes the qualification in the opening verdict for the
following exact candidate manifest:

```text
math/working/bridge_chain_propagation/MANIFEST.json
SHA-256 29c526ad5f10b659b936ade59b58a449a4fb440f9fff98bd3474c976fe13cea5
```

The final revised artifacts are:

| artifact | SHA-256 |
|---|---|
| `NOTE.md` | `682b02b7aab2ffd326a421c60193c8df8d1b33404a22153a893d935f16cf4579` |
| `RESEARCH_LOG.md` | `4abdabdcd6edc617232b9224f7f80382d4f703edc9d7ac32ceca43d0de07ab61` |
| `verify.py` | `0ff21c68ac03f90ac3e1dd01bcbe9da6dca2ed51fc020383374d6b8a220e9ec5` |
| `result.json` | `be1dc9b9931a69c37a3b5f91aff90df61793ce066876938185455eeb7bff4d9d` |

The candidate made both required revisions:

1. Equation (2.2) now quantifies
   \[
   q\in(K_1\cup M_1)-\{z\}.
   \]
2. Before applying that equation to \(x,y\), the proof now explicitly
   rules out \(z=x\) through
   \(xy\in E(H)\), \(y\in M_1\), and \(M\)-side purity, and rules out
   \(z=y\) by the reflected \(K\)-side argument.

The downstream audit then found one occurrence of the old self-pair
ambiguity in the informal Section 5 phrase “graph-complete to the two
original sides.”  The final bytes repair it exactly: every bridge vertex
is stated to be adjacent to every **distinct** vertex of those sides and,
separately, to both original ports.

No remaining use loses this distinctness:

- Corollary 2.2 assumes \(zr\in E(H)\), which already forces \(r\ne z\);
- every common-neighborhood ridge excludes its defining endpoints because
  the neighborhoods are open; and
- ridge exchanges explicitly quantify distinct \(q,q'\).

The clean-room checker was rerun against the final manifest.  All final
candidate and dependency hashes match; both equality controls retain the
same exact parameter vectors, kernels, response lists, ridges, and
one-guard obligations.  Its revised output is:

```text
reviews/bridge_chain_propagation_hostile/independent_result.json
SHA-256 22c54839e890e85e8169df66158f8d952615592e69198d641000189d9628ab13
```

### Final promoted status

- `PROVED`: shared-color orientation, bridge-side purity, distinct-side
  adjacency, adjacency to both original ports, the fresh-component
  propagation gate, and the turning-ridge theorem with exact ridge lists
  and unique exchanges.
- `CERTIFIED-FINITE`: the two sharp equality controls `FCXfO` and
  `HEhbtjK`.
- `OBSERVED`: the unpromoted order-nine greatest-family scan reported in
  the candidate log.
- `OPEN`: arbitrary fresh-component continuations, unit chains,
  lollipops, bicycles, the complete singleton branch, complete \(k=3\),
  and the universal gamma--theta conjecture.

The historical `REFUTED as written` label earlier in this review applies
only to candidate NOTE SHA-256
`8ece21369bbb42cb8e8f9d1286fc72a75d095c144d153f15454fed05d8a7d043`.
It does not apply to the final revised note.
