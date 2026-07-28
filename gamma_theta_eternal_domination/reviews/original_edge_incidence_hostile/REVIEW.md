# Hostile review: original-edge incidence and virtual-rainbow caps

## Verdict

**PASS.**

Theorem 2.1 and Theorem 2.2 are correct under their stated hypotheses.
The one-guard attack sequences are legal, the response-list conclusions
in (2.5) are exactly what closure proves, and an independent truth-table
enumeration confirms that the exact third-color two-list is the sole
locally unit-free cap list for this three-edge gadget.

The source's opening summary now states the scope exactly: for signatures
\(\{a\}\) and \(\{c\}\), (2.5) determines one inclusion and one
exclusion, while only signature \(\{b\}\) determines the whole list:

\[
\begin{array}{c|c}
\sigma(z)&\text{proved information}\\ \hline
\{a\}&c\in L(z),\ a\notin L(z),\quad b\text{ unresolved},\\
\{b\}&L(z)=\{a,c\},\\
\{c\}&a\in L(z),\ c\notin L(z),\quad b\text{ unresolved}.
\end{array}
\]

The theorem body, table (2.5), scope checklist, later use, and corrected
summary all preserve this distinction.

This package does **not** eliminate an arbitrary 2-SAT bicycle.  It gives a
sound local normal form: every failed physical incidence either creates a
locally derived unit or passes through an exact third-color virtual-rainbow
gate.  The controls prove that the unit-free gate genuinely occurs in
equality graphs.  Chaining or excluding those gates around a global
bicycle remains completely open.

## Frozen source bytes reviewed

| Artifact | SHA-256 |
|---|---|
| `math/working/original_edge_core_incidence/NOTE.md` | `36cb17f88c6a6bba5da710bd15e4ebc0c6145bcc5d464244e388c597154554c5` |
| `math/working/original_edge_core_incidence/verify.py` | `2a1f8ff43c0373a83e271e8ecb0b1c5117bd4e9f6da65f9ff97359eabd079efd` |
| `math/working/original_edge_core_incidence/result.json` | `dd473b421915adf6af5a5eb900a7561ee4efae44ce365233d9f738ae64ad0481` |
| `math/working/original_edge_core_incidence/RESEARCH_LOG.md` | `04c3fdc143078dfffcc04474f3fc659e0029e637d129a2b5224de68e8af4d738` |
| `math/working/original_edge_core_incidence/SCOPE_CHECKLIST.md` | `b95d90320eca5a30cbe6258aa9648acb94c5d3c7c26604801fa043b8469c7847` |
| `reviews/original_edge_incidence_hostile/independent_check.py` | `79791e96d3197e7810291452a29299efce9bc79ae098586c1b1dc71fd45244f4` |
| `reviews/original_edge_incidence_hostile/evidence.json` | `04284750cd582f17d500e7338cca2dccb1fcdcd5f72837f4bd3342218b1ccdc1` |

## Proof audit from the one-guard definition

Let \(S=\{a,b,c\}\) be independent and retained in an eternal
triple-family \(\mathcal F\).  If

\[
i\in L(t)\quad\Longleftrightarrow\quad S-i+t\in\mathcal F,
\]

then \(it\in E(G)\): in the successor, the other two anchors both miss
the omitted anchor \(i\), so only \(t\) can dominate it.  Thus

\[
L(x)=\{a,b\}\Longrightarrow ax,bx\in E(G),\ cx\in E(H),
\]

and cyclically

\[
L(y)=\{b,c\}\Longrightarrow by,cy\in E(G),\ ay\in E(H).
\]

The complement nonedges to the omitted anchors are supplied by accepted
C-094 physical representatives; no missing family response is treated as
a graph nonedge.

If \(xy\in E(G)\), the equality \(\gamma(G)=3\) says that
\(\{x,y\}\) is not dominating.  Hence some vertex \(z\notin\{x,y\}\)
satisfies \(xz,yz\in E(H)\).  The four retained direct states

\[
D_a=\{b,c,x\},\quad D_b=\{a,c,x\},\quad
E_b=\{a,c,y\},\quad E_c=\{a,b,y\}
\]

all dominate \(z\).  Because \(x\) and \(y\) miss \(z\), respectively
these states forbid \(z\) from missing both anchors in
\(\{b,c\}\), \(\{a,c\}\), and \(\{a,b\}\).  Therefore

\[
|N_H(z)\cap S|\leq1.
\]

Moreover \(z\notin S\): \(a\) and \(b\) see \(x\) in \(G\), while
\(b\) and \(c\) see \(y\) in \(G\), so each possible anchor conflicts
with one of \(xz,yz\in E(H)\).

The three nonneutral signature cases replay as follows.

- If \(\sigma(z)=\{a\}\), attack \(z\) from
  \(D_b=\{a,c,x\}\).  Only \(c\) can move, so
  \(\{a,x,z\}\in\mathcal F\).  Attack its unoccupied vertex \(b\).
  The anchor \(a\) cannot move.  A move \(z\to b\) would give
  \(S-c+x\notin\mathcal F\), because \(c\notin L(x)\).
  Closure therefore forces \(x\to b\) and
  \(S-c+z\in\mathcal F\).  Hence \(c\in L(z)\), while the actual
  nonedge \(az\in E(H)\) excludes \(a\).

- If \(\sigma(z)=\{c\}\), attack \(z\) from
  \(E_b=\{a,c,y\}\).  Only \(a\) can move, giving
  \(\{c,y,z\}\in\mathcal F\).  Attack \(b\).  A move \(z\to b\)
  would give \(S-a+y\notin\mathcal F\), because \(a\notin L(y)\).
  Closure forces \(y\to b\) and \(S-a+z\in\mathcal F\).  Thus
  \(a\in L(z)\), while \(cz\in E(H)\) excludes \(c\).

- If \(\sigma(z)=\{b\}\), attack \(z\) first from \(D_a\) and then
  attack \(a\) from the forced state \(\{b,x,z\}\).  The same
  exclusion \(S-c+x\notin\mathcal F\) forces
  \(S-c+z\in\mathcal F\), hence \(c\in L(z)\).  Symmetrically,
  attack \(z\) from \(E_c\) and then attack \(c\) from
  \(\{b,y,z\}\); the exclusion \(S-a+y\notin\mathcal F\) forces
  \(S-a+z\in\mathcal F\), hence \(a\in L(z)\).  The actual nonedge
  \(bz\in E(H)\) excludes \(b\), so \(L(z)=\{a,c\}\).

Every attack above is at an unoccupied vertex.  Every retained successor
differs by exactly one guard, and every forced move uses a displayed graph
edge.  The proof never infers a graph nonedge from an absent family state.

## Virtual-rainbow and unit audit

The original edge \(qv\in E(H)\) joins ports with lists
\(\{a,b\}\) and \(\{b,c\}\).  Their only common allowed color is \(b\),
so the original edge forbids precisely the simultaneous \(b\)-events.
C-094 identifies those two events with the \(b\)-events of the same-sign
physical representatives \(x,y\).  Therefore \(X\ne Y\).  The literal
cap edges \(xz,yz\in E(H)\) independently give \(X\ne Z\) and
\(Y\ne Z\).  Thus the three local colors are pairwise distinct.

The independent checker enumerated all nonempty proper cap lists.  In
the numeric notation \(a=0,b=1,c=2\), it obtained:

| \(L(z)\) | Allowed \((X,Y,Z)\) | Fixed colors |
|---|---|---|
| \(\{a\}\) | \((b,c,a)\) | \(X=b,Y=c,Z=a\) |
| \(\{b\}\) | \((a,c,b)\) | \(X=a,Y=c,Z=b\) |
| \(\{c\}\) | \((a,b,c)\) | \(X=a,Y=b,Z=c\) |
| \(\{a,b\}\) | \((a,c,b),(b,c,a)\) | \(Y=c\) |
| \(\{b,c\}\) | \((a,b,c),(a,c,b)\) | \(X=a\) |
| \(\{a,c\}\) | \((a,b,c),(b,c,a)\) | none |

Consequently \(\{a,c\}\), the two-list omitting the shared original
color \(b\), is exactly the sole cap list with no local unit consequence.
This is a statement about this displayed local clause gadget.  It is not
a theorem that every global unit-free response formula has already been
classified or eliminated.

## Independent finite-control audit

`independent_check.py` decodes each graph6 record directly into bit-mask
adjacency.  It imports no target or campaign module.  For every graph it:

- exhaustively computes \(\gamma,i,\alpha\);
- confirms the independent dominating anchor triple and a three-coloring
  of the complement, hence \(\theta=3\);
- confirms that every pair has a common complement neighbor;
- starts from every dominating triple and performs simultaneous
  greatest-fixed-point deletion from the one-guard definition;
- replays every retained unoccupied-attack obligation;
- reconstructs all response lists, complete induced frozen projections,
  component parities, physical representative sets, and cap sets; and
- independently enumerates every response-list coloring and verifies that
  it extends the fixed anchor coloring to a proper coloring of \(H\).

For `MFzJbZYhlrDZdMhd_`, it found 182 dominating triples.  Five are
deleted in the first simultaneous round, leaving the claimed greatest
family of 177 states with family hash

```text
43318de751e7f8f80617bde59f5f16948ef41d38dc3fa13a7201ce3e107955ad
```

and all \(177(14-3)=1947\) obligations.  The exact tuple is

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

At \(S=012\), port \(3\) has unique same-sign physical representative
\(8\).  The specified pairs \(34,39\) lie in \(H\), while \(84,89\)
lie in \(G\).  Their complete common-\(H\)-cap sets are respectively the
singletons \(13\) and \(7\), with the lists and anchor signatures recorded
in the source.  This really refutes simultaneous retention of both
specified original edges by that representative.

For `NFzJbZZhlrDZdMhd|h_`, it found 227 dominating triples.  Eleven are
deleted in the first round, leaving the claimed greatest family of 216
states with family hash

```text
66b8ac6f738dc501ce5f541ecbad4e782fa449b17ffa0cc2ef77e73d3a3e8580
```

and all \(216(15-3)=2592\) obligations.  Its exact tuple is again

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

The original pair \(34\) lies in \(H\).  Its physical representative
sets are exactly \(\{8\}\) and \(\{7\}\), but \(87\in E(G)\).  Their
complete common-\(H\)-cap set is the singleton \(\{13\}\), with

\[
L(13)=\{0,2\},\qquad N_H(13)\cap S=\{1\}.
\]

Thus the exact third-color gate is realized.  This really refutes
unconditional joint physicalization of an original clause.

Both controls have exactly two compatible response-list colorings.  They
are equality controls with \(\theta=3\), not conjecture counterexamples
and not examples satisfying an inclusion-minimal-unsatisfiable premise.

## Effect on the arbitrary-bicycle target

The package makes a legitimate but bounded advance: it replaces a vague
failed-incidence branch by an exact dichotomy and identifies the unique
local no-unit gate.  It does not shorten a gate chain, convert a derived
unit into an independently supported attack tree, force a dominating
pair, or rule out global facet holonomy.  Accordingly:

\[
\boxed{\text{local normal form advanced; arbitrary bicycle not advanced
to an exclusion.}}
\]

The summary correction is incorporated, so promotion is appropriate as a
structural lemma.  It must not be described as a proof of the \(k=3\)
case, an order-frontier increase, or a resolution of the universal
conjecture.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/original_edge_incidence_hostile/independent_check.py \
  --check reviews/original_edge_incidence_hostile/evidence.json

python3 -I -B -W error \
  math/working/original_edge_core_incidence/verify.py \
  --check math/working/original_edge_core_incidence/result.json
```

Both commands return `PASS` on the reviewed bytes.
