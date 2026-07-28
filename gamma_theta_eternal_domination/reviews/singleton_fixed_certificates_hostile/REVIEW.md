# Hostile review: anchor-fixed response certificates

## Verdict

**UNCONDITIONAL PASS**, with the exact scope stated by the candidate.

The arguments in
`math/working/singleton_fixed_certificates/NOTE.md` prove:

1. every retained pair in an eternal two-guard family crosses the two
   sides whenever its vertices lie in one connected component of the
   bipartite complement;
2. every anchor-fixed singleton incidence is aligned, not contradictory;
3. an exact-two vertex is never anchor-fixed in its omitted-color
   projection; and
4. initial fixed-component substitution in the no-full \(k=3\) response
   formula cannot create a false constant, a fixed/free unit, a
   fixed/fixed collision, or a fixed tautology.

This closes only C-119's **immediate fixed-component branch**.  It does not
close contradictions produced later by singleton-unit propagation, the
unit-free bicycle branch, the full-list branch, the whole \(k=3\) case, or
the universal gamma--theta conjecture.

No correction to the candidate statement or proof is required.

## 1. Direct audit of the shortest-even-path attack

Write \(H=\overline J\).  Assume a retained pair \(\{x,y\}\) lies in one
component and on one side of bipartite \(H\).  Among all such retained
pairs, minimize their \(H\)-distance, and let

\[
 x=v_0,v_1,\ldots,v_{2r}=y
\]

be a shortest path.  Its length is positive and even.

- If \(r=1\), then \(v_1\) is unoccupied and is adjacent in \(H\) to both
  guards.  Therefore neither guard dominates \(v_1\) in \(J\), contrary
  to the defining domination requirement on every retained state.
- If \(r\ge2\), then \(v_2\) is unoccupied.  The vertices \(x,v_2,y\)
  lie on the same side of \(H\), so \(xv_2,yv_2\in E(J)\).  With exactly
  two guards, the only one-guard successors are
  \(\{v_2,y\}\) and \(\{x,v_2\}\).  The latter does not dominate \(v_1\),
  since \(xv_1,v_2v_1\in E(H)\).  If the former were retained, its two
  vertices would be a same-side pair joined by the displayed suffix of
  length \(2r-2\); their actual distance is no larger, contradicting
  minimality.  Thus an attack at \(v_2\) has no retained successor.

Every quantifier needed by the one-guard definition is present:
\(v_2\) is unoccupied, each proposed move follows one \(J\)-edge, only one
guard moves, and the surviving response would have to belong to the same
family.  The proof does not assume that the retained pair is independent,
that \(J\) or \(H\) is connected, or that the family is greatest.

## 2. Frozen-projection restoration and family premises

For a frozen anchor \(u\), the relevant vertex set is

\[
 Q_u=(S-\{u\})\cup W_u,\qquad
 W_u=\{x\notin S:u\notin L(x)\},
\]

and the projected family consists exactly of pairs \(A\subseteq Q_u\)
for which \(\{u\}\cup A\in\mathcal F\).

The accepted restoration argument was rechecked rather than treated as a
black box.  If a state \(D\in\mathcal F\) misses \(u\), attack the other
missing anchors of the independent reference state \(S\).  An occupied
anchor cannot answer an attack at another anchor, so those attacks use
outside guards.  This leaves a state \(S-u+x\); attacking \(u\) forces
the outside guard \(x\), proving \(u\in L(x)\).  Hence, while all outside
guards lie in \(W_u\), the frozen guard cannot move in response to an
attack within \(Q_u\).  Removing it preserves domination and every
one-guard obligation in the projected pair family.

The clean-room checker also reconstructed this fact directly for every
state and every projected attack in both controls.  It explicitly checked
that no retained original-family successor moves the frozen guard.

The family-membership premises in the two applications are exact:

- If \(L(s)=\{d\}\) and \(u\ne d\), then
  \(s\in W_u\) and the direct response
  \(S-d+s=\{u,e,s\}\in\mathcal F\) projects to
  \(\{e,s\}\).
- If \(L(x)=S-\{u\}=\{d,e\}\), both direct responses
  \(S-d+x\) and \(S-e+x\) belong to \(\mathcal F\), project respectively
  to \(\{e,x\}\) and \(\{d,x\}\), and \(x\in W_u\).

No static viable list is substituted for a family-response list.

## 3. Anchor components and collision cases

In \(B_u=\overline{Q_u}\), the two unfrozen anchors \(d,e\) are adjacent
because \(S\) is independent in \(G\), so they are in one component and
on opposite sides.

- For a singleton \(L(s)=\{d\}\), if \(s\) is in that component,
  the retained projected pair \(\{e,s\}\) must cross sides.  Since \(d\)
  is opposite \(e\), \(s\) is on the side of \(d\).  Substitution is
  therefore `true`.
- For an exact-two vertex \(L(x)=\{d,e\}\), membership in the anchor
  component would make each of the retained pairs \(\{d,x\}\) and
  \(\{e,x\}\) cross sides.  This would put \(x\) simultaneously on the
  side of \(e\) and on the side of \(d\), impossible.

The complete initial-substitution classification is consequently:

| source | endpoint status after the proved lemmas | simplified form |
|---|---|---|
| anchor-component singleton demand | fixed and aligned | `true` |
| nonanchor singleton demand | free component | unit |
| cross-type exact-two edge | two free components in distinct omitted-color projections | genuine binary clause |

A cross-type edge has endpoints of distinct omitted colors \(u\ne v\).
Its Boolean coordinates are therefore indexed by distinct projections,
so the two free literals cannot collapse to one variable or form a
tautology.  These facts eliminate the immediate false-constant branch
only.  Later propagation of the genuine singleton units can still turn a
binary clause into a unit or contradiction, exactly as the candidate
states.

All uses of adjacency were checked with \(H=\overline G\): complement
edges define bipartite paths and coloring collisions; legal guard moves
and domination use \(G\)-edges.

## 4. Independent finite checks

The independent checker imports no candidate or campaign code and uses
set/frozenset graph states rather than the candidate bitset
implementation.  It obtained:

- `FCpbO`: order \(7\), size \(8\),
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), 12 retained
  triples, 48 original obligations, 8 aligned anchor-fixed singleton
  incidences, and exactly 1 response coloring.
- `LFzJbZYhdrDZdM`: order \(13\), size \(43\), the same five parameters,
  142 retained triples, 1,420 original obligations, 8 exact-two vertices
  in nonanchor components, 10 free/free cross-type collision edges, and
  exactly 2 response colorings.
- The six frozen pair families had sizes
  \(6,6,4,13,13,13\).  Every projected state dominated and all 200
  projected one-guard obligations were replayed.
- Every one of the 33,866 labeled graphs through order 6 was examined;
  5,603 had bipartite complement.  Across their greatest eternal pair
  families, all 54,962 retained pairs satisfied the component-transversal
  conclusion.
- As a direct check not relying on greatest-family containment, all 1,294
  candidate subfamilies through order 4 were tested from the definition;
  all 168 eternal families satisfied the lemma.

The clean-room output has SHA-256

```text
5f4463946704f3429320a6a6991a0746d99fe5adab7f05e0afc82f9ab40c4b31
```

The candidate reproduction output was rerun separately and matched its
declared SHA-256

```text
a06c8a764635a8fed0ec6f5b55a3fc9a95f7f420746f666eee38764647b5a4e5
```

The candidate manifest and all seven listed artifact/dependency hashes
also matched exactly.
