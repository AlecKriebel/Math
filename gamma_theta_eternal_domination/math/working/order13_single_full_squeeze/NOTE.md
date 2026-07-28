# The order-13 full-response squeeze at \(k=3\)

## Status and exact boundary

Date: 2026-07-27 (PDT)

This note contains one new human theorem and one exact finite discovery.

1. **PROVED:** the three external witness layers forced by a full response
   are pairwise disjoint.  Consequently a full response forces at least six,
   rather than five, vertices that are not \(G\)-complete to the reference
   independent triple.
2. **PROVED:** the equality case of the earlier five-vertex witness bound is
   impossible.  At order 13, a full response forces
   \(\lvert Q_S\rvert\leq4\).
3. **CERTIFICATE-BACKED DISCOVERY, PENDING CLEAN-ROOM COVERAGE AUDIT:** an
   exact order-13 CNF with a distinguished full response target, but without
   a uniqueness assumption, is UNSAT.  CaDiCaL produced an ASCII DRAT proof
   and `drat-trim` accepted it in RUP-only mode.

The intended finite theorem, once the formula and its symmetry coverage have
been independently reconstructed, is:

> There is no graph \(G\) of order 13, eternal family \(\mathcal F\) of
> triples, maximum independent triple \(S\in\mathcal F\), and vertex
> \(x\notin S\) such that
> \[
> \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)
> \]
> and \(L_S^{\mathcal F}(x)=S\).

Uniqueness of \(x\) in the full-list set is **not** assumed.  Connectivity is
not assumed or encoded.  This is a complete finite exclusion of the
order-13 full-response branch only; it does not exclude order-13
counterexamples whose response lists all have size at most two, and it does
not prove the universal \(k=3\) case.

The finite statement is not promoted here to the campaign ledger.  The DRAT
certificate proves the generated CNF UNSAT, but an independently written
formula reconstructor and hostile coverage review are still required.

## 1. Setup

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,\qquad H=\overline G,
\]

let \(\mathcal F\) be an eternal family of triples, and let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent.  Fix a full response vertex \(x\notin S\):

\[
 L_S^{\mathcal F}(x)=S.
\]

For \(u\in S\), recall

\[
 A_u=N_H(x)\cap N_H(u),
\qquad
 Y_{u,p}=N_H(u)\cap N_H(p)\quad(p\in A_u).
\]

The accepted full-list geometry proves that:

- every \(A_u\) is nonempty and the three spokes are pairwise disjoint;
- every \(Y_{u,p}\) is nonempty;
- \(Y_{u,p}\) lies outside \(S\cup\{x\}\cup N_H(x)\);
- every \(y\in Y_{u,p}\) is adjacent to \(x\) in \(G\); and
- \(\{x,u,p\},\{u,p,y\}\in\mathcal F\).

Put

\[
 Q_S=\{q\in V(G)-S:q\text{ is adjacent in }G\text{ to all of }S\}.
\]

## 2. External witnesses have one anchor only

### Theorem 2.1 (anchor-pure external witnesses) — PROVED

For \(u\in S\), \(p\in A_u\), and \(y\in Y_{u,p}\),

\[
 N_H(y)\cap S=\{u\}.
\]

#### Proof

Membership in \(Y_{u,p}\) gives \(uy\in E(H)\).  Suppose that
\(vy\in E(H)\) for some \(v\in S-\{u\}\), and let \(w\) be the third
anchor.  Fullness of \(x\) puts

\[
 D=S-v+x=\{u,w,x\}
\]

in \(\mathcal F\).  Attack the unoccupied vertex \(y\).

- The guard at \(u\) cannot move because \(uy\in E(H)\).
- If \(w\) moves, the successor \(\{u,x,y\}\) fails to dominate \(p\):
  all three edges \(pu,px,py\) lie in \(H\).
- If \(x\) moves, the successor \(\{u,w,y\}\) fails to dominate \(v\):
  the anchor triangle gives \(vu,vw\in E(H)\), and \(vy\in E(H)\) by
  assumption.

No one-guard response is retained, contradicting eternal closure.
Therefore \(y\) is adjacent in \(G\) to both anchors other than \(u\).
\(\square\)

### Corollary 2.2 (disjoint witness layers) — PROVED

Choose \(p_u\in A_u\) for every \(u\in S\).  Then the three nonempty sets

\[
 Y_{a,p_a},\qquad Y_{b,p_b},\qquad Y_{c,p_c}
\]

are pairwise disjoint.

Indeed, a vertex in two of them would have two anchor neighbors in \(H\),
contrary to Theorem 2.1.

### Corollary 2.3 (six non-neutral vertices) — PROVED

\[
 \left|V(G)-(S\cup Q_S)\right|\geq6,
\qquad
 |V(G)|\geq |Q_S|+9.
\]

#### Proof

The three chosen spoke vertices \(p_a,p_b,p_c\) are distinct and lie in
\(N_H(x)\).  Corollary 2.2 supplies three distinct external witnesses.
The external witnesses are adjacent to \(x\) in \(G\), so none is a spoke.
All six vertices miss an anchor and hence lie outside \(Q_S\). \(\square\)

This strictly strengthens the earlier five-vertex full-response bound.
In particular, at order 13,

\[
 |Q_S|\leq4.
\]

The formerly possible tight-five incidence patterns were:

- a \(2+1\) partition of three nonempty witness sets over two vertices; or
- one witness shared by two layers and the other shared by another two.

Both require a vertex to lie in two external witness layers and are now
excluded by Theorem 2.1.  This is a human proof, independent of SAT.

If \(|Q_S|=4\) at order 13, equality holds in Corollary 2.3: each spoke is
a singleton, each external witness layer is a different singleton, and
there are no other vertices outside \(S\cup Q_S\).  The exact SAT probe also
finds this six-vertex layer inconsistent even after the clique-cover gap is
removed, but no human proof of that stronger assertion is claimed here.

## 3. Exact finite encoding

By relabeling, fix

\[
 S=\{0,1,2\},\qquad x=3.
\]

Edge variables encode \(H=\overline G\).  The minimal frozen formula has
9,802 variables:

| variable family | count |
|---|---:|
| complement edges \(e_{uv}\) | 78 |
| common-neighbor choices \(w_{uvt}\) | 858 |
| family states \(f_D\) | 286 |
| one-guard responses \(m_{D,r,u}\) | 8,580 |

It has 85,409 clauses:

| clause family | count | meaning |
|---|---:|---|
| no \(H\)-\(K_4\) | 715 | \(\alpha(G)\leq3\) |
| pair common-neighbor clauses | 1,794 | \(\gamma(G)\geq3\) |
| selected-state domination | 2,860 | every \(D\in\mathcal F\) dominates |
| family nonempty | 1 | redundant because \(S\) is fixed in |
| exact one-guard closure | 20,020 | one adjacent guard, retained successor |
| fixed \(S\) and full target \(x\) | 10 | anchor triangle, \(S\in\mathcal F\), three full successors |
| complete anchored coloring obstruction | 59,049 | all \(3^{10}\) extensions of colors \(0,1,2\) on \(S\) |
| four-bit signature sorting | 960 | sound \(S_9\) orbit representative |

The formula deliberately omits:

- uniqueness of the full target;
- connectedness;
- the five- or six-vertex witness bound;
- the redundant theorem forcing every \(H\)-triangle into the family; and
- every odd-hole or odd-antihole template.

Thus the finite result does not depend on the new human bound.

### Semantic implications

The anchor triangle gives \(\alpha(G)\geq3\), while the no-\(K_4\) clauses
give \(\alpha(G)\leq3\).  Every pair has an external common neighbor in
\(H\), so no pair dominates \(G\).  The selected full successor states
dominate, and the selected states form a nonempty eternal family, giving

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

The 59,049 coloring clauses are complete because every proper
three-coloring of \(H\) assigns three distinct colors to the anchor
triangle; after permuting color names, those colors are \(0,1,2\).  The
remaining ten vertices have exactly \(3^{10}\) assignments.  Each clause
requires at least one monochromatic \(H\)-edge for its assignment.  Hence
all clauses together say \(\theta(G)=\chi(H)>3\).

## 4. Soundness of the signature sorter

The vertices \(4,\ldots,12\) are otherwise unlabeled.  For such a vertex
\(v\), define its four-bit signature

\[
 \sigma(v)=
 \bigl(1_{0v\in E(H)},1_{1v\in E(H)},
       1_{2v\in E(H)},1_{3v\in E(H)}\bigr),
\]

interpreted as an integer from 0 through 15 with the displayed coordinates
as bits 0 through 3.

For each adjacent labeled pair \(v,v+1\) in \(4,\ldots,12\), and every
ordered signature pair \(p>q\), one eight-literal clause forbids

\[
 \sigma(v)=p,\qquad \sigma(v+1)=q.
\]

There are

\[
 8\binom{16}{2}=960
\]

clauses.  A clause is false exactly on its named inversion, so their
conjunction is precisely

\[
 \sigma(4)\leq\sigma(5)\leq\cdots\leq\sigma(12).
\]

This is sound symmetry breaking.  The full symmetric group on
\(\{4,\ldots,12\}\) fixes \(S\cup\{x\}\) and transports every variable
family:

\[
\begin{aligned}
 e_{uv}&\mapsto e_{\pi(u)\pi(v)},\\
 w_{uvt}&\mapsto w_{\pi(u)\pi(v)\pi(t)},\\
 f_D&\mapsto f_{\pi(D)},\\
 m_{D,r,u}&\mapsto m_{\pi(D),\pi(r),\pi(u)}.
\end{aligned}
\]

The graph, domination, and one-guard clauses are covariant.  The fixed
anchor/full clauses are unchanged.  The coloring bank is also invariant
because it contains **every** assignment extending the fixed anchor colors.
Therefore any satisfying assignment of the unsorted formula can be
transported by a permutation that orders the nine signatures.  Every orbit
has a sorted representative, including ties.  Consequently UNSAT of the
sorted formula implies UNSAT of the unrestricted formula.

The unsorted formula itself timed out after 120 seconds; no solver outcome
is claimed for that run.  Its timeout neither proves nor weakens the
orbit-representative argument.

## 5. Frozen run and independent proof replay

Generator:

```text
math/working/order13_single_full_squeeze/search.py
```

Exact generation/solve command:

```text
python3 -I -B -W error \
  math/working/order13_single_full_squeeze/search.py \
  --solver tools/cadical_3_0_1/build/cadical \
  --timeout 120 \
  --omit-connected \
  --omit-all-independent-states \
  --omit-unique-full \
  --omit-witness-bound \
  --instance math/working/order13_single_full_squeeze/minimal-instance.cnf \
  --proof math/working/order13_single_full_squeeze/minimal-proof.drat \
  --result math/working/order13_single_full_squeeze/minimal-solver.out
```

CaDiCaL 3.0.1 returned UNSAT.  A replay without proof output took 0.71
seconds real time, 0.70 seconds process time, used 81.66 MB maximum RSS, and
reported 6,634 conflicts.

Proof replay:

```text
tools/drat_trim_2023_05_22/drat-trim \
  math/working/order13_single_full_squeeze/minimal-instance.cnf \
  math/working/order13_single_full_squeeze/minimal-proof.drat -U
```

The independent checker reported:

```text
c 11846 of 85409 clauses in core
c 8277 of 123053 lemmas in core using 485709 resolution steps
c 0 RAT lemmas in core; 3558 redundant literals in core lemmas
s VERIFIED
c verification time: 2.364 seconds
```

The same checker generated the retained 11,846-clause core and its
8,277-lemma reduced proof.

Tool identities:

| tool | identity | executable SHA-256 |
|---|---|---|
| CaDiCaL | 3.0.1 | `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6` |
| `drat-trim` | campaign build from 2023-05-22 | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |

Artifacts:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `minimal-instance.cnf` | 4,808,845 | `d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13` |
| `minimal-proof.drat` | 19,874,489 | `653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910` |
| `minimal-core.cnf` | 184,631 | `dcba47ea9d60afc1cc86672498af39681c3acf02606c728f66cb84f47ee557e7` |
| `minimal-core.drat` | 915,086 | `83f73ee2c2a82ab0a228099f0354abf46e23f3e807561a6d665a43b86b1e273f` |
| `minimal-solver.out` | 16 | `bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162` |
| `search.py` | current source | `fe30fa9cfb7cc3c00103d16dbe497e5f79bb7ff3956d7a8620e22f77608648b5` |

A fresh deterministic regeneration produced the same instance hash
`d5a2f17...cb13`.

## 6. Ablations and positive control

| run | clauses | outcome | exact interpretation |
|---|---:|---|---|
| default strengthened formula | 89,925 | UNSAT | includes uniqueness, connectedness, old witness bound, redundant independent-state clauses |
| omit old witness bound | 89,799 | UNSAT | the bound is not needed |
| omit unique-full condition | 89,916 | UNSAT | led to the stronger one-full-target scope |
| minimal frozen formula | 85,409 | UNSAT + checked DRAT | decisive discovery run |
| minimal formula without sorter | 84,449 | TIMEOUT at 120 s | no SAT/UNSAT claim |
| omit eternal closure | 69,905 | SAT | one-guard dynamics are essential |
| default formula without clique-cover gap | 30,876 | SAT | the full-response equality slice is nonempty |
| minimal formula without clique-cover gap | 26,360 | SAT | source of the positive control below |

For the minimal set of structural clauses with the clique-cover obstruction
removed, the retained SAT model decodes to the graph

```text
LF\|ul\XzVsaqJ
```

with

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
\]

Its greatest eternal family consists of all 157 dominating triples, and
the response lists at \(S=\{0,1,2\}\) have the unique full target \(x=3\).
This is a positive equality control, not a counterexample.  It shows that
the UNSAT result is not caused by inconsistent full-response or equality
clauses; the clique-cover gap is the decisive missing property.

## 7. Exact stopping boundary

The human contribution is unconditional and ready for adversarial proof
review: external witness layers are anchor-pure and disjoint.

The order-13 finite exclusion still requires:

1. a clean-room reconstruction of all 85,409 clauses;
2. an independent truth-table audit of the 960 comparator clauses;
3. independent replay of the full and reduced proofs;
4. verification of the exact formula-to-theorem coverage argument; and
5. independent checking of the positive control.

Even after promotion, the conclusion will be only:

\[
 \boxed{\text{an order-13 counterexample, if one exists, has no full
 family-response target.}}
\]

The remaining order-13 \(k=3\) search is exactly the no-full-list
response-2-SAT branch.  No statement here excludes that branch or raises the
global counterexample frontier by itself.
