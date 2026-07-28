# The family-list mixed \(P_4\): dominating endpoints and the dynamic-rank boundary

## Status and strict scope

Date: 2026-07-28 (PDT)

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

let \(\mathcal F\) be an arbitrary one-guard eternal family of dominating
triples, let \(S=\{a,b,c\}\in\mathcal F\) be independent, and put
\(H=\overline G\).  Suppose \(x_0x_1x_2x_3\) is an induced path in \(H\)
with exact **family-response** lists

\[
 L^\mathcal F_S(x_0)=\{a\},\qquad
 L^\mathcal F_S(x_1)=\{a,c\},\qquad
 L^\mathcal F_S(x_2)=\{b,c\},\qquad
 L^\mathcal F_S(x_3)=\{b\}.
\tag{0.1}
\]

The proved result is a strict lift of the input boundary of C-148:

> **Theorem 1 (both omitted middle-color endpoint swaps dominate).**
> Under (0.1), both
> \[
> Q_0=\{a,b,x_0\},\qquad Q_3=\{a,b,x_3\}
> \tag{0.2}
> \]
> dominate \(G\).

Thus the exact static hypothesis in C-148 is unnecessary except for
supplying one endpoint domination defect.  No equality realization of the
family-list pattern can have such a defect.

This does **not** exclude (0.1).  In an arbitrary proper family, omission
of \(Q_0,Q_3\) does not imply graph nonadjacency, failed domination, or
finite deletion rank in the unrestricted greatest kernel.  The exact
remaining branch is recorded in Theorem 2 below.

## 1. One endpoint defect is already impossible

Accepted C-070, which applies to the exact family lists (0.1), gives

\[
 cx_0,cx_3\in E(G).
\tag{1.1}
\]

We isolate the part of accepted C-148 that will be used.

### Lemma 1.1 (one-defect local kernel; accepted C-148)

Assume (0.1), (1.1), and suppose one vertex \(d\) is missed by
\(\{a,b,x_0\}\).  Then no such eternal family exists.

#### Complete local coverage

The missed-vertex condition gives

\[
 da,db,dx_0\notin E(G).
\tag{1.2}
\]

The retained independent root \(S\) dominates \(d\), so \(cd\in E(G)\).
The triple \(\{a,b,d\}\) is independent and therefore belongs to every
eternal triple-family.  It is the direct \(c\)-replacement of \(S\), and
(1.2) excludes the other roles, hence

\[
 L^\mathcal F_S(d)=\{c\}.
\tag{1.3}
\]

The positive \(c\)-roles at \(x_1,x_2\) put
\(\{a,b,x_1\},\{a,b,x_2\}\) in \(\mathcal F\).  These states must
dominate \(d\), forcing

\[
 dx_1,dx_2\in E(G).
\tag{1.4}
\]

The vertex \(d\) is distinct from the seven original vertices: it is not
in the failed state; (1.1) excludes \(c\); the positive \(a\)-edge at
\(x_1\) excludes \(x_1\); the positive \(b\)-edge at \(x_2\) excludes
\(x_2\); and the positive \(b\)-edge at \(x_3\) excludes \(x_3\).

On

\[
 C=\{a,b,c,x_0,x_1,x_2,x_3,d\}
\]

the family lists (0.1), (1.3), the induced complement path, and
(1.1)--(1.4) fix 14 graph edges and 9 graph nonedges.  The only undecided
pairs are

\[
 bx_0,\quad bx_1,\quad ax_2,\quad ax_3,\quad dx_3.
\tag{1.5}
\]

Accepted C-148 checks all \(2^5=32\) completions.  For each completion,
start with every core-dominating triple satisfying arbitrary-state
restoration relative to the five exact displayed lists, then repeatedly
delete a state having an unoccupied displayed attack with no retained
one-edge, one-guard successor.  The terminal kernel is empty in all 32
completions.

This local calculation covers arbitrary external vertices.  A response
from a state contained in \(C\) to an attack at a vertex of \(C\) is
again a triple contained in \(C\).  Therefore the intersection of any
putative global eternal family with the core would survive every local
deletion round, contradicting the empty terminal kernel.

Notice that this lemma assumes exact **family** lists.  It uses no
negative static role except the one actual domination defect (1.2).

### Proof of Theorem 1

If \(Q_0\) failed domination, choose a missed vertex \(d\).  Lemma 1.1
would contradict the existence of \(\mathcal F\).  Hence \(Q_0\)
dominates.

Reflecting

\[
 a\leftrightarrow b,\qquad
 x_0\leftrightarrow x_3,\qquad
 x_1\leftrightarrow x_2,\qquad c\mapsto c
\]

gives the same conclusion for \(Q_3\).  This reflection relabels the
argument; it asserts no graph automorphism. \(\square\)

## 2. Exact greatest-kernel normal form

Let \(\mathcal K_\infty\) be the literal greatest one-guard eternal
triple-family of \(G\), obtained by synchronous deletion from all
dominating triples.  Give every dominating state deleted in round \(j\)
rank \(j\), every nondominating triple rank \(0\), and every survivor rank
\(\infty\).

### Theorem 2 (survivor-or-positive-rank endpoint dichotomy)

Under (0.1), each \(Q_i\), \(i\in\{0,3\}\), satisfies exactly one of:

1. \(Q_i\in\mathcal K_\infty\); or
2. \(Q_i\) has positive finite deletion rank.

In the second case, if \(\rho(Q_i)=r\), there is an unoccupied attack
\(t_i\notin Q_i\) such that every legal successor

\[
 Q_i-u+t_i\qquad
 (u\in Q_i,\ ut_i\in E(G))
\tag{2.1}
\]

has rank strictly less than \(r\).

If (0.1) is the list pattern in the **greatest** family itself, both
states fall in case 2.

#### Proof

Theorem 1 says both states are dominating, so rank zero is impossible.
The greatest-kernel construction partitions dominating triples into
survivors and positive finite deletion rounds, proving the dichotomy.
The attack \(t_i\) and strict rank caps in (2.1) are exactly the
synchronous deletion criterion in round \(r\).  If the greatest family
has the exact lists (0.1), the missing \(c\)-roles say
\(Q_0,Q_3\notin\mathcal K_\infty\), so their ranks are finite and
positive. \(\square\)

The rank row (2.1) is the correct dynamic substitute for the static
defect.  It is not the same eight-vertex incidence: because \(Q_i\)
dominates, the deleting attack is adjacent to at least one occupied guard.
Consequently the C-148 local kernel cannot simply be reused by declaring
\(t_i\) to be a missed vertex.

For an arbitrary proper family, either endpoint state may survive the
unrestricted greatest family even though it is absent from
\(\mathcal F\).  In that case there is no unrestricted deletion rank to
descend.  The graph `FDzro` realizes exactly this boundary at
\(\gamma=2\): its proper 21-state family has (0.1), while its greatest
family contains both endpoint \(c\)-swaps.

## 3. Discovery-only bounded synthesis

The script `synthesize.py` encodes, for fixed order \(n\):

- an unknown simple graph with the independent root and induced
  complement path;
- exact inclusion/exclusion of the twelve direct response incidences in
  (0.1);
- an explicit arbitrary, possibly proper, eternal family of triples;
- literal domination of every retained state;
- one-edge, one-guard closure for every unoccupied attack;
- \(\alpha(G)\le3\); and
- no dominating pair.

Since the root is independent and retained, these conditions imply
\(\gamma=\alpha=\gamma^\infty=3\).  CaDiCaL 3.0.1 reported `UNSAT` for
every order

\[
 12\le n\le22.
\tag{3.1}
\]

Exact variable counts, clause counts, times, memory, and the relevant
generator and solver hashes are in `OBSERVED_RESULTS.json`.  The generated
CNF instances are omitted because they are byte-for-byte reconstructible
from the frozen script.

These outputs are **OBSERVED only**.  They have no DRAT/LRAT package,
independent formula reconstruction, symmetry/coverage audit, or
independent solver replay.  They prove neither (3.1) nor a universal
family-list exclusion.

## 4. Exact next recurrence/core

The static-defect lane is closed by Theorem 1.  The remaining family-list
core is:

1. both forbidden endpoint states \(Q_0,Q_3\) dominate;
2. in the greatest-family version, both have positive finite ranks and
   carry the strict three-successor cap row (2.1);
3. in a proper-family-only version, either state may instead survive the
   unrestricted greatest kernel, so one must first separate genuine
   kernel failure from deliberate family thinning; and
4. no omitted family response may be converted into a graph nonedge.

The highest-value next lemma is therefore:

> Starting from the lower-rank successor rows of \(Q_0,Q_3\), either
> produce a strictly lower-rank copy of one endpoint row, force one of the
> 32 C-148 domination-defect cores, or exhibit a dominating pair.

Without that recurrence, the positive rank statement is a normal form,
not an exclusion.  The family-list mixed \(P_4\), complete \(k=3\), and
the universal gamma--theta conjecture remain unresolved.

## 5. Reproduction

From the campaign directory, for example:

```text
python3 -I -B -W error \
  math/working/family_mixed_p4_lift/synthesize.py \
  --order 12 \
  --cnf /tmp/family-mixed-p4-order12.cnf \
  --result /tmp/family-mixed-p4-order12.json \
  --solver tools/cadical_3_0_1/build/cadical
```

The auxiliary scripts `cegar_dominating_pairs.py` and
`minimize_gamma_pairs.py` are proof-discovery tools only.  Their outputs
must not be promoted without an independent encoding and certificate
audit.
