# Hostile review: the full-list singleton-terminal gate

## Verdict

Date: 2026-07-28 (PDT)

\[
\boxed{\texttt{PASS\_STRICT\_SCOPE}}
\]

The singleton-terminal exclusion in
`math/working/full_list_terminal_gate/NOTE.md`, frozen at commit
`34c80b36dc03b6fbab846c27a71d90db3301cb45`, is correct.

The exact conclusion is:

> Assume
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), fix an independent root
> \(S=\{a,b,c\}\) and one full target \(x\), and suppose all three
> color-restricted C-149 kernels are empty.  Choose one C-149
> rank-decreasing terminal trace for each color, with retained terminal
> states \(S-u+r_u\), \(r_u\in N_{\overline G}(x)\).  The three
> greatest-family root palettes cannot simultaneously be
> \(P(r_a)=\{a\}\), \(P(r_b)=\{b\}\), and \(P(r_c)=\{c\}\).
> Equivalently, every such triple of chosen traces has at least one
> terminal palette of size at least two.  More strongly, at least one
> color has no own-color-singleton terminal trace at all.

This does **not** prove that any color-restricted kernel is nonempty.  It
does not produce a safe color, a proper complement coloring, the complete
\(k=3\) theorem, or the universal gamma--theta conjecture.

The frozen source has SHA-256

```text
0d6eb44fa2807cd34e441c31364149577cccf39f28b426a5d81b7cc78c9d1253
```

and is byte-identical to the file at the reviewed commit.

## Two nonfatal wording cautions

The theorem bytes are sound, but two sentences should not be promoted as
stronger frontier claims.

1. Section 4 says that the nonsingleton conclusion is “sharp at the
   two-color boundary.”  The equality control proves only that two colors
   can be annihilated simultaneously and can have exclusively
   nonsingleton nonroot-corridor terminals.  It does not establish
   sharpness of inequality (3.2), since its third kernel survives and it
   does not realize an all-three-empty instance with exactly one
   nonsingleton terminal.
2. Section 6's all-three-nonsingleton corridor-only case is a legitimate
   next subproblem, not an exhaustive description of everything left by
   Theorem 3.1.  Mixed singleton/nonsingleton palettes and terminal triples
   containing direct-root or anchor-restoration gates also remain open.

These cautions do not alter Theorem 3.1 or Corollary 3.2.  A claims-ledger
entry should use the strict conclusion quoted above.

## 1. Dependency audit

The only substantive imported implication in the new universal theorem is
C-149's retained descent.

- The literal unrestricted greatest family is
  \(\mathcal F^\star\).
- For color \(u\), the restricted kernel bans every state
  \(S-u+z\) with \(z\in B=N_{\overline G}(x)\).
- If this restricted kernel is empty, C-149 Proposition 5.1 starts from
  the retained full-target response \(S-u+x\) and supplies a finite
  trace.  Every preterminal state lies in
  \(\mathcal F^\star\) outside the ban, restricted deletion rank strictly
  decreases, and the last successor is a retained banned state
  \(S-u+r_u\), \(r_u\in B\).

The quantifier is per color: each empty kernel supplies at least one trace,
and the three traces may be selected independently.  Their endpoints all
belong to the same unrestricted family \(\mathcal F^\star\), which is the
only simultaneity needed by the attack proof.  No synchronization of ranks,
attacks, or predecessors across the three traces is assumed.

C-149 Proposition 5.2 classifies the final transition, not the terminal
state:

- a corridor attacks \(r_u\);
- it is direct-root when the mover is \(u\);
- it is a nonroot corridor when the mover is another vertex, in which
  case the named four vertices induce the asserted \(G\)-diamond; or
- an anchor-restoration entry attacks one of the two retained root
  anchors.

The candidate proof uses only the common retained terminal state
\(S-u+r_u\).  It therefore does not need to infer a corridor, diamond, or
restoration property in a case where C-149 does not provide one.

C-142 is not a premise of the attack.  Its role is to delimit the claim and
supply the finite equality control: reverse-color membership is not
future safety, and the named graph has two empty restricted kernels despite
all three colors lying in its global reverse set.  The candidate preserves
that distinction.

The reviewed dependency bytes are:

| artifact | SHA-256 |
|---|---|
| C-141/C-142 source note | `32b6319a0b7b6f226af3c2db4515666ccc6450b1991056e65fd1a38ef85d8967` |
| C-141/C-142 candidate manifest | `8afaeec6e181535ddeaf7925420ef73d7abba444f8ec7e887a6b4fc802d5d467` |
| C-141/C-142 hostile manifest | `cc75898604e02eedda4b0ff7c5fd212af02459839c2b618fbde9eaf91b07388d` |
| C-141/C-142 clean result | `91b554bb820cf6a95e9aad68a930dfaabc21a9be6866dd7c8490c546b61d6412` |
| C-149 source note | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-149 candidate manifest | `8a09e4c9c932caeebea257f7ac8c3e9ece51d1a4dbd444cfa562a55dc86de3f4` |
| C-149 hostile manifest | `129587b63b012058c8b6ac3ccd956455dccc578ecfd60d0c77c7a541e42a2e95` |
| C-149 clean evidence | `dd98027a5e73551e1f5db356f8c2e257bbe5a44bf95de74790e8b872d5fd30af` |

## 2. Palette semantics and the terminal vertices

The palette is the exact family-response palette

\[
 P(z)=
 \{u\in S:uz\in E(G),\ S-u+z\in\mathcal F^\star\}.
\]

It is neither a static dominating-swap list nor an adjacency list.

For a retained terminal \(E_u=S-u+r_u\), the two root anchors in
\(S-u\) are nonadjacent to \(u\).  Since \(E_u\) dominates \(u\), the
outside guard \(r_u\) must be adjacent to \(u\).  Thus

\[
u\in P(r_u).
\]

There is one small implication used repeatedly in the attack proof that is
worth spelling out.  If \(v\in S\) and the state \(S-v+r\) belonged to
\(\mathcal F^\star\), that retained state would have to dominate the
omitted anchor \(v\).  The other two anchors miss \(v\), so \(rv\in E(G)\).
Consequently

\[
S-v+r\in\mathcal F^\star
\quad\Longrightarrow\quad
v\in P(r).
\]

Therefore \(v\notin P(r)\) legitimately excludes the family state
\(S-v+r\).  It does **not** imply \(rv\notin E(G)\), and the candidate
never uses such a graph-nonedge inference.

Fullness gives \(S\cap B=\varnothing\).  The three singleton equalities
also force \(r_a,r_b,r_c\) to be pairwise distinct: one vertex cannot
simultaneously have two different singleton palettes.

## 3. Complete one-guard attack audit

Write

\[
D_a=\{r_a,b,c\},\quad
D_b=\{a,r_b,c\},\quad
D_c=\{a,b,r_c\}.
\]

All three states are retained.  Since each \(r_u\in B\), the state
\(\{r_a,r_b,r_c\}\) misses \(x\) and cannot belong to an eternal family.

Consider \(D_{ab}=\{r_a,r_b,c\}\).

### Case 1: \(D_{ab}\notin\mathcal F^\star\)

Attack the unoccupied vertex \(r_b\) from \(D_a\).

- The guard \(b\) has the move edge \(br_b\), but its successor is the
  assumed-absent \(D_{ab}\).
- If \(r_a\) has a move edge to \(r_b\), its successor is
  \(S-a+r_b\), absent because \(a\notin P(r_b)\).
- Eternal closure therefore either fails immediately or retains the only
  remaining possible response, by \(c\), at
  \(Q=\{r_a,b,r_b\}\).

Attack the unoccupied anchor \(a\) from \(Q\).  Guard \(b\) cannot move
because \(ab\notin E(G)\).  The other two possible successors are
\(S-c+r_b\) and \(S-c+r_a\), both absent because
\(c\notin P(r_b),P(r_a)\).  This contradicts closure.

### Case 2: \(D_{ab}\in\mathcal F^\star\)

Attack the unoccupied vertex \(r_c\).

- Moving \(c\) produces \(\{r_a,r_b,r_c\}\), which does not dominate
  \(x\).
- Thus a retained response, if one exists, moves \(r_a\) or \(r_b\).

If \(r_a\) moves, the successor is
\(Q_a=\{r_b,c,r_c\}\).  Attack the unoccupied anchor \(b\).
Guard \(c\) cannot move because \(bc\notin E(G)\); the other two
successors are \(S-a+r_c\) and \(S-a+r_b\), both absent.

If \(r_b\) moves, the symmetric successor is
\(Q_b=\{r_a,c,r_c\}\).  Attack the unoccupied anchor \(a\).
Again \(c\) cannot move, and the remaining successors
\(S-b+r_c\) and \(S-b+r_a\) are absent.

Both possible retained responses fail.  This closes the second case.

Every attack above is at an unoccupied named vertex.  Every candidate
response replaces exactly one guard, uses an edge of \(G\), and remains
inside the same family when called retained.  The proof never invokes an
all-guards move, an occupied-vertex attack, or a complement edge as a move
edge.

## 4. Quantifier and 27-label audit

For every choice of one terminal trace per color, the preceding attack
rules out the conjunction of the three own-color singleton palettes.
Hence at least one selected endpoint has a second palette color.

Suppose, more strongly, that every color admitted at least one
own-color-singleton terminal trace.  Choose one such trace for each of
the three colors.  This produces the forbidden conjunction, so at least
one color admits no such trace.  This is the strongest correct conclusion.
It still says nothing about whether that color's restricted kernel
survives.

C-149's two terminal forms split into three disjoint labels:

\[
\mathsf D=\text{direct-root corridor},\quad
\mathsf C=\text{nonroot corridor},\quad
\mathsf A=\text{anchor restoration}.
\]

For the ordered colors \(a,b,c\), the Cartesian cube
\(\{\mathsf D,\mathsf C,\mathsf A\}^3\) has \(3^3=27\) label triples and
is exhaustive.  The candidate attack depends only on the retained
terminal states, so it covers the singleton-palette subclass of every one
of those 27 labels.  It neither asserts that all 27 labels are realizable
nor eliminates a label without the singleton-palette hypothesis.

## 5. Clean-room local exhaustion

`independent_checker.py` imports no candidate or campaign code.  On the
seven named vertices

\[
x,a,b,c,r_a,r_b,r_c
\]

it fixes exactly:

- the three root nonedges;
- the three nonedges \(xr_a,xr_b,xr_c\);
- the three full-target edges \(xa,xb,xc\); and
- the three forced terminal edges \(ar_a,br_b,cr_c\).

There are nine remaining pairs and therefore \(2^9=512\) graph
completions.  For each completion, the checker:

1. takes every locally dominating triple except the six root swaps
   excluded by the three singleton palettes;
2. computes the greatest one-guard fixed point from the definition; and
3. tests whether all three required terminal states survive together.

The result is zero countermodels in all 512 completions.  This is a sound
local overapproximation of any ambient graph: an attack at one of the
seven named vertices from a named triple has only named-triple successors.
External vertices can make additional named triples fail domination or
impose additional attacks, but they cannot add a response to one of these
named attacks.  Thus an ambient eternal family would restrict to a subset
of the local universe tested here.

As a mutation control, removing the two singleton bans for any one color
produces 35 local models containing all three terminal states.  The
all-three singleton quantifier is therefore doing real work; the checker
is not merely rejecting the fixed adjacency skeleton.

## 6. Independent equality-control reconstruction

The same clean-room checker independently decodes

```text
Ksv`f\knJVis
```

and obtains

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
\]

39 edges, 127 dominating triples, and a 127-state unrestricted greatest
triple-family.

For root \(S=\{1,2,3\}\) and target \(x=0\), it reconstructs

\[
B=\{6,8,10,11\},\qquad
E(\overline G[B])=\{68,10\,11\}.
\]

The target is full.  The three restricted kernels have sizes

\[
0,\quad0,\quad64
\]

with deletion-round sizes

\[
(16,40,56,12),\quad
(16,40,56,12),\quad
(16,32,13).
\]

The complete rank-decreasing terminal rows reachable from the selected
starts for the two empty kernels are exactly:

| color | predecessor | attack/mover | terminal | palette |
|---|---|---|---|---|
| 1 | \(\{2,3,4\}\) | \(10/4\) | \(\{2,3,10\}\) | \(\{1,2\}\) |
| 1 | \(\{2,3,5\}\) | \(11/5\) | \(\{2,3,11\}\) | \(\{1,3\}\) |
| 2 | \(\{1,3,7\}\) | \(6/7\) | \(\{1,3,6\}\) | \(\{2,3\}\) |
| 2 | \(\{1,3,9\}\) | \(8/9\) | \(\{1,3,8\}\) | \(\{1,2\}\) |

All four are nonroot corridors.  For each, the induced quartet has exactly
the missing edge between \(x\) and its terminal vertex, independently
confirming the C-149 diamond assertion.  This output agrees with the
candidate checker.

The control confirms only that one- and two-color corridor annihilation
can occur under equality.  Since its third kernel has 64 states, it does
not test the theorem's all-three-empty premise.

## 7. Reproduction

Run the clean-room hostile checker:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/full_list_terminal_gate_hostile/independent_checker.py
```

Run the frozen candidate control:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/math/working/full_list_terminal_gate/verify_equality_control.py
```

The clean result has SHA-256

```text
1dba2a568b7bf51b8a7d7d96155c4bd183721992293531f53b5e4f8709de247d
```

The candidate replay's canonical stdout has SHA-256

```text
c079a18479923c9e04475c31285f4ea5a00118bed702fa47cb17257f1458bfb2
```

Subject to the strict conclusion and two wording cautions above, the
singleton-terminal theorem is ready for promotion.
