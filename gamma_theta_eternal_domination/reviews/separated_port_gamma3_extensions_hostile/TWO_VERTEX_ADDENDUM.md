# Addendum: exact two-vertex induced extensions

## Verdict

**PASS for the stated bounded computation.**

A clean-room implementation independently enumerated all

\[
2^{9+9+1}=524{,}288
\]

labeled ways to adjoin vertices 9 and 10 to the fixed nine-vertex induced
complement core.  Exactly six extensions satisfy
\(\gamma(G)=\alpha(G)=3\).  In every one, the greatest one-guard eternal
triple kernel is empty; all 45 first-round and 17 second-round deletions
exhaust the 62 dominating triples, and the reference triple
\(\{0,1,2\}\) is deleted in round two.

Thus no graph in this precise finite template has
\(\gamma=\alpha=\gamma^\infty=3\).  The campaign may conservatively retain
the label `OBSERVED` because this is a local diagnostic rather than a
counterexample-order exclusion.  The counts and bounded conclusion
themselves now have an independent exact replay.

## Frozen targets

The revised notes and target computation reviewed here have SHA-256 hashes:

```text
math/working/gamma3_port_identification_proof/NOTE.md
0b852592548e72face4eb8944909c1dd24c4fbedd31e1a468d118ceb9b0d1487

math/working/gamma3_port_identification_proof/two_vertex_extensions.py
866e933fb739c6ce593252eb8a7b25789bcd41d001f4dd818f47de39405bf4e0

math/working/gamma3_port_identification_proof/two_vertex_extensions_result.json
32dd9e6596794f4950468c06682945a907a45c83fe846f5ef2de77e9e7e4de30

math/working/separated_port_gamma3_extensions/NOTE.md
8f4deb09e0290bbcd6317763704d1dba1040aef22bb56b5cba37ac2e7904bc34
```

## 1. Coverage

The induced complement on old vertices \(0,\ldots,8\) is held exactly
fixed.  A labeled extension is determined independently by:

- the nine old neighbors of vertex 9 in \(H\);
- the nine old neighbors of vertex 10 in \(H\); and
- whether \(9\,10\in E(H)\).

These are 19 independent bits.  The clean-room decoder traversed every
integer from 0 through \(2^{19}-1\), reconstructed the three fields, and
asserted that re-encoding them returned the original integer.  This proves
coverage of the full stated labeled Cartesian product.

The scope does not allow any edge among the old nine vertices to change.  It
does not cover three or more added vertices, a different induced
separated-port core, or arbitrary graphs of order 11.

## 2. Static predicate

Let \(H=\overline G\).  The fixed old graph \(H_0\) has exactly one triangle,
\(\{0,1,2\}\), and no \(K_4\).  Consequently every \(K_4\) in an extension
has one of two forms:

1. one new vertex joined to all vertices of an old triangle; or
2. both adjacent new vertices together with an old \(H_0\)-edge contained
   in their common old neighborhood.

The independent generator used this characterization, not the target's
general \(K_4\) routine.  It also ran a generic four-subset check on every
survivor.

The anchor triangle gives \(\omega(H)\geq3\), so absence of a \(K_4\) is
equivalent to

\[
\alpha(G)=\omega(H)=3.
\]

A pair \(\{u,v\}\) fails to dominate \(G\) exactly when some third vertex is
nonadjacent in \(G\) to both, equivalently when

\[
N_H(u)\cap N_H(v)\ne\varnothing.
\]

Thus every pair having a common \(H\)-neighbor is equivalent to the absence
of a dominating pair.  Together with \(\alpha=3\), this gives
\(\gamma=3\).  The clean-room checker also computed \(\gamma\) and
\(\alpha\) directly on every survivor.

Exactly these six labeled codes survive:

```text
260093
260094
261115
261118
261627
261629
```

Their complement neighborhoods and graph6 records match the target result
byte for byte.

## 3. Eternal-kernel replay

For each survivor the independent checker:

1. enumerated all triples;
2. retained only dominating triples;
3. for every retained state considered attacks only at unoccupied vertices;
4. allowed a response only when exactly one guard moves along a \(G\)-edge
   to the attacked vertex; and
5. simultaneously deleted every state with an attack having no successor
   in the current family.

This is literal greatest-fixed-point deletion in the one-guard model.  It
uses ordinary sets and imports no target search code.

Every survivor begins with 62 dominating triples.  The identical deletion
histogram is

\[
\begin{array}{c|rr}
\text{round}&1&2\\ \hline
\text{states deleted}&45&17.
\end{array}
\]

The kernel is therefore empty in every case.  The reference state
\(\{0,1,2\}\) has deletion rank two in all six cases, independently
confirming the target records.

Because the entire triple kernel is empty, no response-list condition needs
to be imposed: none of the six static survivors admits any eternal
triple-family at all.  This is stronger, within the fixed template, than
failure of the six old prescribed response lists.

## 4. Claim boundary

The verified conclusion is only:

> No two-vertex extension of this exact fixed induced nine-vertex
> complement core has
> \(\gamma=\alpha=\gamma^\infty=3\).

It is not an exclusion of all order-11 graphs, a proof of terminal-port
recurrence, a proof of the \(k=3\) slice, or a resolution of the universal
gamma-theta conjecture.
