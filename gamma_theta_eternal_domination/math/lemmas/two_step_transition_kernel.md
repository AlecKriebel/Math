# Forced maximum-independent states in the two-step transition kernel

## Status

The deductions were proved directly from the one-guard definition on
2026-07-25 and accepted by the independent audit in
`reviews/two_step_transition_hostile_review.md`.

Related finite-horizon work predates this campaign.  Burger, Cockayne,
Gründlingh, Mynhardt, van Vuuren, and Winterbach introduced **smart
\(q\)-secure domination**, requiring safe configurations after each of
\(q\) problems, in
[*Finite Order Domination in Graphs*](https://www.vuuren.co.za/papers/finitedomination.pdf),
J. Combin. Math. Combin. Comput. 49 (2004), 159--175.  The same authors
treated the infinite-order limit in
[*Infinite Order Domination in Graphs*](https://combinatorialpress.com/jcmcc-articles/volume-050/infinite-order-domination-in-graphs/),
J. Combin. Math. Combin. Comput. 50 (2004), 179--194.

There is an important quantifier distinction.  Definition 9 of the finite
paper uses

\[
 \forall(r_1,\ldots,r_q)\ \exists(u_1,\ldots,u_q),
\]

and its conclusion states that the entire problem sequence was known in
advance.  The present one-guard game is online: attacks are revealed one at a
time, so its two-ply truncation has the adaptive order

\[
 \forall r_1\ \exists u_1\ \forall r_2\ \exists u_2.
\]

The offline smart-\(q\) notion is therefore related but is not being imported
as an equivalent theorem.  The online finite-horizon kernel below is the
direct game-theoretic truncation of the exact eternal-family definition.
No categorical novelty claim for that general truncation is made pending a
broader literature search.

The contribution of this note is delimited to the present
\(\gamma\)--\(\theta\) program:

1. combining the forced maximum-independent-state lemma with the online
   two-ply truncation of the exact one-guard game;
2. expanding the two-ply consequence into a compact private-region
   certificate and translating it to the \(k=3\) complement target; and
3. measuring that certificate exactly on the recorded near-miss populations.

No claim is made here that this specialization is absent from all prior
literature; that narrower novelty question remains subject to the literature
audit.  Mathematically, the two-ply consequence is strictly stronger than the
one-step condition used earlier in this campaign, and \(C_7\) separates them.

All attacks below are at unoccupied vertices, and each response moves exactly
one guard along one edge to the attacked vertex.

## 1. Online finite horizons in transition-kernel notation

Fix a graph \(G\) and a guard count \(k\).  Let \(\mathcal C_k\) be the set
of dominating \(k\)-subsets of \(V(G)\).  For
\(\mathcal X\subseteq\mathcal C_k\), define

\[
 \Phi(\mathcal X)=
 \left\{D\in\mathcal C_k:
 \begin{array}{l}
 \text{for every }r\in V(G)-D\text{ there is }u\in D\cap N(r)\\
 \text{such that }(D-\{u\})\cup\{r\}\in\mathcal X
 \end{array}
 \right\}.
\]

Starting with \(\mathcal K_0=\mathcal C_k\), put
\(\mathcal K_{j+1}=\Phi(\mathcal K_j)\).

**Lemma 1 (online transition-kernel reformulation).**  The sets

\[
 \mathcal K_0\supseteq\mathcal K_1\supseteq
 \mathcal K_2\supseteq\cdots
\]

form a descending chain that stabilizes.  Its stable value
\(\mathcal K_\ast\) is the greatest eternal dominating family of size \(k\):
an eternal \(k\)-family exists if and only if
\(\mathcal K_\ast\ne\varnothing\), and every eternal \(k\)-family is
contained in \(\mathcal K_\ast\).

**Proof.**  The operator \(\Phi\) is monotone: if
\(\mathcal X\subseteq\mathcal Y\), every response into \(\mathcal X\) is
also a response into \(\mathcal Y\).  Since
\(\Phi(\mathcal K_0)\subseteq\mathcal K_0\), induction using monotonicity
gives

\[
 \mathcal K_{j+1}=\Phi(\mathcal K_j)
 \subseteq\Phi(\mathcal K_{j-1})=\mathcal K_j.
\]

There are only finitely many \(k\)-subsets, so the chain stabilizes at some
\(\mathcal K_\ast\).  At stabilization
\(\mathcal K_\ast=\Phi(\mathcal K_\ast)\).  If it is nonempty, this equality
says directly that every member dominates and every unoccupied attack has a
one-edge, one-guard response remaining in \(\mathcal K_\ast\); hence it is
an eternal family.

Conversely, let \(\mathcal F\) be any eternal \(k\)-family.  Certainly
\(\mathcal F\subseteq\mathcal K_0\).  If
\(\mathcal F\subseteq\mathcal K_j\), every response supplied by closure of
\(\mathcal F\) lands in \(\mathcal K_j\), so
\(\mathcal F\subseteq\Phi(\mathcal K_j)=\mathcal K_{j+1}\).  Induction gives
\(\mathcal F\subseteq\mathcal K_j\) for every \(j\), and hence
\(\mathcal F\subseteq\mathcal K_\ast\). \(\square\)

Thus \(\mathcal K_1\) is the set of secure dominating \(k\)-configurations.
Membership in \(\mathcal K_2\) says more: every first attack has a response
whose resulting configuration is itself secure.

**Corollary 1.1 (forced-state stopping criterion).**  Suppose
\(\alpha(G)=k\).  The following are equivalent:

1. \(\gamma^\infty(G)=k\);
2. \(\mathcal K_\ast\ne\varnothing\);
3. some maximum independent set belongs to \(\mathcal K_\ast\); and
4. every maximum independent set belongs to \(\mathcal K_\ast\).

In particular, deleting even one maximum independent \(k\)-set at a finite
kernel round certifies \(\gamma^\infty(G)\geq k+1\).

**Proof.**  Lemma 1 gives the equivalence of (1) and (2), using the general
lower bound \(\alpha(G)\leq\gamma^\infty(G)\).  If
\(\mathcal K_\ast\ne\varnothing\), it is itself an eternal \(k\)-family.
Every independent \(k\)-set is forced into every eternal \(k\)-family by the
successive-attack argument used below, so (2) implies (4).  The implication
(4) to (3) is immediate, and (3) implies (2).  The final assertion follows
from the descending chain and integrality. \(\square\)

## 2. The forced two-step condition

For a dominating set \(D\) and \(u\in D\), recall the closed private region

\[
 P_D(u)=\{x\in V(G):N[x]\cap D=\{u\}\}.
\]

The swap criterion from `maximum_independent_states.md` says that, for
\(r\notin D\) and \(u\in D\cap N(r)\), the state
\((D-\{u\})\cup\{r\}\) dominates if and only if
\(P_D(u)\subseteq N[r]\).

**Theorem 2 (two-step private-region condition).**  Suppose
\(\alpha(G)=\gamma^\infty(G)=k\).  For every maximum independent set
\(S\) and every \(r\in V(G)-S\), there is a guard \(u\in S\) such that,
with

\[
 D=(S-\{u\})\cup\{r\},
\]

both of the following hold:

1. \(u\in N(r)\) and \(P_S(u)\subseteq N[r]\); and
2. for every \(t\in V(G)-D\), there is
   \(v\in D\cap N(t)\) such that
   \[
     P_D(v)\subseteq N[t].
   \]

Equivalently, every maximum independent \(k\)-set belongs to
\(\mathcal K_2\): every first attack has a legal dominating response that is
itself a secure dominating set.

**Proof.**  Let \(\mathcal F\) be an eternal family of \(k\)-sets.  A
maximum independent set \(S\) has size \(k\).  It belongs to every such
family: starting from any state in \(\mathcal F\), repeatedly attack an
unoccupied vertex of \(S\).  Independence prevents a response from moving a
guard already on \(S\), so each attack increases the number of guards on
\(S\) by one and eventually reaches \(S\).

Now attack \(r\) from \(S\).  Closure of \(\mathcal F\) supplies a guard
\(u\in S\cap N(r)\) and puts
\(D=(S-\{u\})\cup\{r\}\) in \(\mathcal F\).  In particular, \(D\)
dominates, so the swap criterion gives
\(P_S(u)\subseteq N[r]\).

Because \(D\in\mathcal F\), any unoccupied second attack \(t\notin D\) also
has a response: some \(v\in D\cap N(t)\) moves to \(t\), and the resulting
member of \(\mathcal F\) dominates.  Applying the swap criterion to \(D\)
gives \(P_D(v)\subseteq N[t]\).  This proves both assertions. \(\square\)

The explicit adjacency requirement \(v\in N(t)\) in part 2 is necessary.
The intermediate state \(D\) need not be independent, so \(v\) need not
belong to its own private region \(P_D(v)\).

**Corollary 3 (compact lower-bound certificate).**  Suppose
\(\alpha(G)=k\).  Let \(S\) be a maximum independent set and
\(r\notin S\).  For each \(u\in S\cap N(r)\), put
\(D_u=(S-\{u\})\cup\{r\}\).  If, for every such \(u\), either

1. \(D_u\) is not dominating; or
2. there is \(t_u\notin D_u\) such that every
   \(v\in D_u\cap N(t_u)\) gives a non-dominating state
   \((D_u-\{v\})\cup\{t_u\}\),

then

\[
 \gamma^\infty(G)\geq k+1.
\]

**Proof.**  The hypotheses say exactly that the forced state \(S\) does not
belong to \(\mathcal K_2\), contradicting Theorem 2 if
\(\gamma^\infty(G)=k\).  The general inequality
\(\alpha(G)\leq\gamma^\infty(G)\), integrality, and
\(\alpha(G)=k\) give the displayed lower bound. \(\square\)

The certificate can be checked without any fixed-point search.  In case 1,
name one vertex undominated by \(D_u\).  In case 2, name the second attack
\(t_u\) and, for each possible second guard \(v\), one vertex undominated
after its swap.  This is the certificate format implemented independently
of the eternal evaluator in `src/search/two_step_obstruction.py`.

## 3. Complement form for the \(k=3\) target

Put \(H=\overline G\).  Assume \(\alpha(G)=3\), so
\(\omega(H)=3\).  Maximum independent triples of \(G\) are exactly the
triangles of \(H\), and a triple is dominating in \(G\) exactly when it is
externally uncontained in \(H\).

Consequently, if \(\gamma^\infty(G)=3\), then for every triangle \(T\) of
\(H\) and every \(r\notin T\), there is \(u\in T\) such that

1. \(ur\notin E(H)\);
2. \(D=(T-\{u\})\cup\{r\}\) is externally uncontained; and
3. for every \(t\notin D\), there is \(v\in D\) with
   \(vt\notin E(H)\) such that
   \((D-\{v\})\cup\{t\}\) is externally uncontained.

This is a local two-ply constraint on every forced triangle of the complement
target.  Passing it is necessary, not sufficient, for an eternal family.

## 4. Strictness: the seven-cycle

The two-step condition is strictly stronger than requiring every maximum
independent set to be secure.  Label \(C_7\) cyclically by
\(0,1,\ldots,6\).  Its maximum independent triples are the rotations of
\(S=\{0,2,4\}\).  The state \(S\) is secure:

\[
\begin{array}{c|c}
\text{attack}&\text{one dominating response}\\ \hline
1&2\to1\\
3&2\to3\\
5&4\to5\\
6&0\to6
\end{array}
\]

and rotation proves the same for every maximum independent triple.  Thus
\(C_7\) passes the earlier one-step condition.

However, attack \(1\) from \(S\).  Moving \(0\to1\) leaves vertex \(6\)
undominated.  The only dominating first response is \(2\to1\), producing
\(D=\{0,1,4\}\).  From \(D\), attack \(3\).  The only adjacent guard is at
\(4\), and moving it to \(3\) produces \(\{0,1,3\}\), which leaves vertex
\(5\) undominated.  Hence the first attack has no secure successor, so
\(S\notin\mathcal K_2\).  Corollary 3 proves
\(\gamma^\infty(C_7)\geq4\), while the one-step condition alone does not.

## 5. Measured pruning power

The deterministic probe `src/search/two_step_obstruction.py` records a
separate computational measurement in
`results/two_step_obstruction_measurement.json`.  These counts measure the
filter; they are not used in the proof above and do not constitute an
exhaustive nonexistence result.

On the 8,587 canonical edge-toggle near-misses with
\(\gamma=\alpha=3\) and \(\gamma^\infty=\theta=4\), the measured split was:

| outcome | graphs |
|---|---:|
| rejected already by the one-step condition | 4,169 |
| additional graphs rejected only at the second step | 3,892 |
| total rejected by two steps | 8,061 |
| surviving the two-step condition | 526 |

Thus the second step rejects \(3{,}892\) graphs that the earlier local test
cannot reject, and the combined depth-two filter removes about \(93.9\%\) of
this finite near-miss population.

The same probe streamed the complete connected-unlabeled graph orders from
pinned `geng` and applied the static filter
\(\gamma=\alpha=3<\theta\):

| order | static targets | one-step rejected | additional at step two | survive step two |
|---:|---:|---:|---:|---:|
| 7 | 5 | 2 | 3 | 0 |
| 8 | 78 | 51 | 27 | 0 |
| 9 | 1,569 | 1,134 | 435 | 0 |

The order-nine static-target count agrees with the earlier complete A/B
parameter census.  The theorem is universal, but these pruning counts are
delimited observations about the recorded finite inputs.
