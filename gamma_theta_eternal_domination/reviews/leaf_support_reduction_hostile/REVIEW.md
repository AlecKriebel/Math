# Independent hostile review of the leaf--support reduction

**Review date:** 2026-07-26  
**Target:** `math/lemmas/leaf_support_reduction.md`  
**Target SHA-256:** `802907a01c27043dfa1348a1c8e97e142769238cb62c9064e946573dfba93517`  
**Verdict:** **ACCEPT -- PROVED, WITH AN EXPLICIT PUBLISHED-COMPUTATION
DEPENDENCY FOR THE \(5k/2\) COROLLARY.**

No unresolved critical, high-, medium-, or low-severity mathematical defect
remains in the reviewed bytes.  An earlier draft omitted the reason that a
minimum \(k\)-guard state containing the leaf \(x\) cannot also contain its
support \(y\).  The reviewed version supplies the necessary argument at lines
129--135.  The final eternal-family projection is now valid for an
**arbitrary** eternal \(k\)-family, with attacks only at unoccupied vertices
and exactly one guard moving.

The self-contained leaf deletion, counterexample preservation, and
minimum-degree conclusions are unconditional relative to the already accepted
parameter-chain and component-additivity reductions.  The later
\(\lceil5k/2\rceil\) and order-\(12\), \(k=5\) conclusions additionally rely
on the published MacGillivray--Mynhardt--Virgile computation that there is no
counterexample through order \(11\).  The note states this dependency
accurately and does not represent it as a new certificate.

## 1. Model and quantifiers audited

I used precisely the family formulation

\[
 \forall D\in\mathcal D\ \forall r\in V(G)-D\
 \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal D,
\]

where \(\mathcal D\) is nonempty and every member is a dominating \(k\)-set.
Thus:

1. the attacked vertex is unoccupied;
2. the responding guard is adjacent to it;
3. exactly that one guard moves; and
4. the successor remains in the same family.

No occupied attack, simultaneous movement, guard stacking, or all-guards
variant is used.

## 2. Clean-room proof audit

### 2.1 Static parameters and well-coveredness

The equality collapse gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k,
\]

so every maximal independent set of \(G\) has size \(k\).  If \(I\) is any
maximal independent set of \(Q=G-\{x,y\}\), then \(I\cup\{x\}\) is independent
and dominating in \(G\): \(x\) handles \(x,y\), while maximality makes \(I\)
dominate \(Q\).  Hence \(|I|=k-1\).  This proves simultaneously that \(Q\) is
well-covered and that

\[
 i(Q)=\alpha(Q)=k-1.
\]

The upper bound \(\gamma(Q)\leq k-1\) follows from
\(\gamma(Q)\leq i(Q)\).  If \(A\) dominated \(Q\) with at most \(k-2\)
vertices, then \(A\cup\{x\}\) would dominate \(G\) with at most \(k-1\)
vertices.  Therefore

\[
 \gamma(Q)=\alpha(Q)=k-1.
\]

### 2.2 The arbitrary-family eternal reduction

Let \(\mathcal D\) be any eternal family of \(k\)-sets in \(G\).
Choose a maximum independent set \(I\) of \(Q\).  Then
\(S=I\cup\{x\}\) is an independent \(k\)-set.  Starting from any
\(D\in\mathcal D\), repeatedly attack a vertex of \(S-D\).  Such an attack is
unoccupied.  Since \(S\) is independent, the responding guard cannot be a
guard already on \(S\); each one-guard response increases
\(|D\cap S|\) by one.  Thus \(S\in\mathcal D\), establishing the required
nonemptiness of the \(x\)-slice without choosing a specially constructed
eternal family.

There is one essential minimum-domination observation.  No
\(D\in\mathcal D\) can contain both \(x\) and \(y\).  If it did, deleting the
guard at \(x\) would preserve domination: \(y\) dominates \(x\), and the leaf
\(x\) has no other neighbor.  This would contradict \(\gamma(G)=k\).
Consequently

\[
 \mathcal E=\{D-\{x\}:D\in\mathcal D,\ x\in D\}
\]

is a nonempty family of \((k-1)\)-subsets of \(Q\).

Every \(B\in\mathcal E\) dominates \(Q\), because in
\(D=B\cup\{x\}\) the leaf \(x\) has no neighbor in \(Q\).  Now fix
\(r\in V(Q)-B\).  It is unoccupied in \(D\), so eternal closure supplies

\[
 u\in D\cap N_G(r),\qquad
 D'=(D-\{u\})\cup\{r\}\in\mathcal D.
\]

The leaf \(x\) is not adjacent to \(r\), hence \(u\ne x\) and \(u\in B\).
The guard at \(x\) stays fixed, and projection gives

\[
 D'-\{x\}=(B-\{u\})\cup\{r\}\in\mathcal E.
\]

This proves closure with the exact
\(\forall B\,\forall r\,\exists u\) order.  Therefore
\(\gamma^\infty(Q)\leq k-1\), while
\(\alpha(Q)\leq\gamma^\infty(Q)\) gives the reverse inequality.

### 2.3 Clique partitions

A clique partition of \(Q\), together with \(\{x,y\}\), proves
\(\theta(G)\leq\theta(Q)+1\).  Conversely, in a minimum clique partition of
\(G\), the part containing \(x\) is either \(\{x,y\}\) or \(\{x\}\).
In the singleton case, the part \(C\) containing \(y\) cannot itself be
\(\{y\}\), since the two singleton parts could be merged.  Replacing
\(\{x\},C\) by \(\{x,y\},C-\{y\}\) and deleting \(\{x,y\}\) leaves
\(\theta(G)-1\) cliques partitioning \(Q\).  Hence

\[
 \theta(G)=\theta(Q)+1.
\]

### 2.4 Counterexample and minimum-degree consequences

If \(\theta(G)>k\), integrality and the deletion identities give

\[
 \theta(Q)=\theta(G)-1\geq k>k-1
 =\gamma(Q)=\gamma^\infty(Q),
\]

so \(Q\) is a strictly smaller counterexample.  Component additivity makes a
minimum-order counterexample connected.  Such a graph is neither \(K_1\) nor
\(K_2\), has no leaf by the deletion theorem, and has no isolated vertex by
connectedness.  Its minimum degree is therefore at least two.

The note correctly isolates the empty-remainder boundary: if \(Q=\varnothing\),
then \(G=K_2\) and \(k=1\).  Extending the displayed identities to that case
requires an explicit convention such as
\(\gamma^\infty(\varnothing)=0\) with the nonempty vacuous family
\(\{\varnothing\}\).  This boundary cannot occur in a counterexample.

## 3. McCuaig--Shepherd source audit

The [Wiley version-of-record page](https://doi.org/10.1002/jgt.3190130610)
for W. McCuaig and F. B. Shepherd, *Domination in graphs with minimum degree
two*, J. Graph Theory 13 (1989), 749--762, states in its abstract that a
connected graph of minimum degree two, other than seven exceptional graphs,
has domination number at most two-fifths its order.

The exact inequality and exception family were cross-checked in the official
paper of M. A. Henning, I. Schiermeyer, and A. Yeo,
[*A New Bound on the Domination Number of Graphs with Minimum Degree
Two*](https://doi.org/10.37236/499), Electron. J. Combin. 18 (2011), P12.
Visual inspection of its pages 3 and 5 confirms:

- \(\mathcal F_4=\{C_4\}\);
- every member of \(\mathcal F_i\) has order \(i\);
- \(\mathcal F_7\) consists of the six displayed graphs; and
- its Theorem 1 restates McCuaig--Shepherd exactly as

\[
  G\text{ connected},\quad \delta(G)\geq2,\quad
  G\notin\mathcal F_4\cup\mathcal F_7
  \quad\Longrightarrow\quad
  \gamma(G)\leq\frac{2|V(G)|}{5}.
\]

Thus the seven exceptions are exactly one graph of order \(4\) and six graphs
of order \(7\); there is no hidden large exception or extra order
hypothesis.

## 4. The \(5k/2\) consequence and its dependency

MacGillivray, Mynhardt, and Virgile's official paper
[*Eternal Domination and Clique Covering*](https://doi.org/10.5614/ejgta.2022.10.2.19),
EJGTA 10(2) (2022), 603--624, states as Observation 5.6 that there is no
counterexample of order \(n\leq11\).  Visual inspection of page 620 also
confirms that this is explicitly the output of their computer search; the
paper reports approximately 85 CPU days.  It is therefore a legitimate
published premise, but not a proof-certificate package reproduced by this
review.

Let \(G\) be a minimum-order counterexample of order \(n\) and common
parameter \(k\).  The published order-\(11\) result gives \(n\geq12\), so
\(G\) is not one of the order-\(4\) or order-\(7\) exceptions.  The leaf and
component reductions give connectedness and \(\delta(G)\geq2\).
McCuaig--Shepherd then yields

\[
 k=\gamma(G)\leq\frac{2n}{5},
\]

and hence

\[
 n\geq\left\lceil\frac{5k}{2}\right\rceil.
\]

If an order-\(12\), parameter-\(5\) counterexample existed, the same
published premise would make that graph itself minimum-order, but the bound
would require \(n\geq\lceil25/2\rceil=13\).  The order-\(12\), \(k=5\)
slice is therefore excluded.

It is possible in principle to remove the MMV dependency by separately
proving that none of the seven McCuaig--Shepherd exceptions is a
\(\gamma\)--\(\theta\) counterexample.  The finite probe below supports that
strengthening.  I do **not** promote it here: three order-\(7\) exceptions
have \(\gamma=\alpha=3<\theta=4\) and require genuine one-guard failure
certificates to establish \(\gamma^\infty=4\).  Until those certificates or
short analytic proofs are packaged and mapped to the published six graphs,
the main note's explicit MMV premise is the more rigorous boundary.

## 5. Independent finite falsification probe

`probe.py` uses nauty 2.9.3 `geng` only to supply unlabeled graph6 instances.
It independently parses graph6 and computes domination, independence, maximal
independent-set sizes, clique partition number, and the greatest one-guard
eternal fixed point using integer bitmasks.

It exhausts all 13,598 nonempty unlabeled graphs through order \(8\).  Among
694 graphs with \(\gamma=\gamma^\infty\), it checks 467 choices of a leaf and
support with nonempty remainder.  Every predicted equality,
well-coveredness assertion, clique-partition identity, and projected-family
closure test passes.

As a separate source sanity check, the connected
\(\delta\geq2\), \(5\gamma>2n\) census through order \(8\) returns exactly:

| graph6 | \(n\) | \(\gamma\) | \(\alpha\) | \(\gamma^\infty\) | \(\theta\) |
|---|---:|---:|---:|---:|---:|
| `C]` | 4 | 2 | 2 | 2 | 2 |
| `F?ov_` | 7 | 3 | 4 | 4 | 4 |
| ``FCp`_`` | 7 | 3 | 3 | 4 | 4 |
| `FCpb_` | 7 | 3 | 3 | 4 | 4 |
| `FCpbo` | 7 | 3 | 3 | 3 | 3 |
| `FCZb_` | 7 | 3 | 3 | 4 | 4 |
| `FCZbg` | 7 | 3 | 3 | 3 | 3 |

This matches one order-\(4\) and six order-\(7\) exceptions.  The finite
experiment is supporting falsification evidence, not a substitute for the
universal proof or the cited theorem.

## 6. Exact artifact hashes

| Artifact | SHA-256 |
|---|---|
| `math/lemmas/leaf_support_reduction.md` | `802907a01c27043dfa1348a1c8e97e142769238cb62c9064e946573dfba93517` |
| `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| `literature/sources/henning_schiermeyer_yeo_2011_p12.pdf` | `418199b3a9f9c92974046a6c92b0b11b24cdec51e034f5aa23168c4bdfbb4285` |
| `literature/sources/mmv2022.pdf` | `e1a5c6bb4fb4767c3d91a5e848872d26d97d3f0df284142a1b885ad720a20edf` |
| `reviews/leaf_support_reduction_hostile/probe.py` | `4d99d45dc78b68436b83fff817c8afd21fea49bb08a5bc761dcfcbbcdc100820` |
| `reviews/leaf_support_reduction_hostile/probe_result.json` | `873c7bbb05b49b1a2124b763e41883a7d4e65eb04940b4ee533ae5e799d7a2a3` |

## 7. Final hostile verdict

**ACCEPT.**  The final reviewed note proves the leaf--support reduction in the
standard one-guard model, constructs the required nonempty
\((k-1)\)-family from every arbitrary eternal \(k\)-family, preserves a
strict counterexample gap, and correctly forces a minimum-order
counterexample to be connected with minimum degree at least two.  The exact
McCuaig--Shepherd theorem then gives
\(n\geq\lceil5k/2\rceil\) once the seven small exceptions are excluded; the
note does so transparently via the published MMV through-order-\(11\)
computation and therefore correctly excludes the order-\(12\), \(k=5\)
slice.
