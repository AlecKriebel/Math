# The order-12 frontier for the \(\gamma\)--\(\theta\) conjecture

## Status and evidentiary boundary

This note assembles accepted analytic reductions and one exact LRAT
refutation to prove that the published counterexample frontier advances from
order \(11\) to order \(12\).

The through-order-\(11\) premise is the published exhaustive computation of
MacGillivray, Mynhardt, and Virgile (2022).  The campaign independently
reproduces their complete 56-graph appendix catalog and independently
enumerates all connected graphs only through order \(9\); it has not
reproduced the original all-graph coverage at orders \(10\) and \(11\).
Accordingly, the final frontier theorem is a rigorous consequence of a
published computational premise plus campaign-certified order-12 results,
not a campaign-only proof-certificate enumeration through order \(12\).

Everything concerns the standard one-guard-moves model: attacks occur only
at unoccupied vertices, exactly one adjacent guard moves to the attacked
vertex, and every resulting configuration must dominate.

This finite theorem does not resolve the universal conjecture and makes no
claim about graphs of order \(13\) or larger.

## 1. Exact order-12 parameter-four exclusion

Let

```text
D = instances/order12_k4_connected_doublelex/instance.cnf
```

The exact DIMACS census and binding are

\[
\begin{aligned}
 \lvert D\rvert&=4{,}030{,}657\text{ bytes},\\
 (v,c,\ell)&=(18{,}381,\ 115{,}507,\ 1{,}190{,}774),\\
 \operatorname{SHA256}(D)
 &=\texttt{14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7}.
\end{aligned}
\]

The accepted certificate package is
`certificates/order12_k4_doublelex_seed0_lrat/`.  Its strict normalizer
turns the solver's complete binary DRAT stream into an addition-only RUP
stream with SHA-256
`2741335a5ed9af769f0db4bd0c03a70e414d0568681d5b8261a5667ed30b6686`.
Warning-fatal forward and backward `drat-trim` replays both verify that
stream with zero RAT lemmas.  The resulting 228,381,671-byte LRAT has
SHA-256
`0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263`
and passes a separate `lrat-check`.

The independent hostile review in
`reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/` reconstructed \(D\)
and the normalized proof byte for byte, reran both proof directions,
produced a fresh byte-identical LRAT, checked both retained and fresh LRATs,
and returned

```text
ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY
```

Its review and machine-readable evidence have SHA-256 values
`fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395`
and
`2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63`.
Thus the exact formula \(D\) is UNSAT.

### Theorem 1

There is no connected finite simple graph \(G\) of order \(12\) satisfying

\[
 \gamma(G)=\gamma^\infty(G)=4<\theta(G).
\tag{1.1}
\]

#### Proof

The accepted equality-collapse theorem first turns (1.1) into

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\tag{1.2}
\]

The exact graph-to-CNF theorem in
`math/lemmas/order12_k4_synthesis_target.md` says that every connected graph
satisfying (1.2), after relabeling one maximum independent four-set and
sorting the remaining eight anchor-adjacency signatures, yields a satisfying
assignment of the exact parent CNF
`instances/order12_k4_connected_parent/instance.cnf`.

The accepted DoubleLex theorem in
`math/lemmas/order12_k4_doublelex.md` proves that the parent is satisfiable
if and only if \(D\) is satisfiable.  Since the independently certified
refutation proves \(D\) UNSAT, the parent is UNSAT.  It can therefore have
no graph realization satisfying (1.2). \(\square\)

The implication from exact \(D\)-UNSAT to Theorem 1 was separately audited
before the certificate was promoted.  Its verdict is
`VALID_CONDITIONAL_CONNECTED_EXCLUSION_ONLY` in
`reviews/order12_k4_doublelex_conditional_implication_audit/REVIEW.md`.

## 2. Structural parameter-five exclusion

The simplicial closed-neighborhood reduction proves the following.  If
\(\gamma(G)=\gamma^\infty(G)=k\), \(v\) is simplicial, and
\(Q=G-N[v]\) is nonempty, then

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k-1,\qquad
 \theta(G)=\theta(Q)+1.
\tag{2.1}
\]

Consequently, a minimum-order counterexample is connected and has no
simplicial vertex.  In particular, its minimum degree is at least two.
The complete proof is
`math/lemmas/simplicial_neighborhood_reduction.md`; the independent hostile
review found no mathematical defect and retained the novelty caveat caused
by an unavailable 2018 manuscript.

McCuaig and Shepherd proved that every connected graph \(R\) of order \(n\)
and minimum degree at least two, other than seven exceptional graphs of
orders four and seven, satisfies

\[
 \gamma(R)\leq\frac{2n}{5}.
\tag{2.2}
\]

The exact theorem and exception orders were checked in the version of record
and in Henning, Schiermeyer, and Yeo's official 2011 restatement.  The source
details and audit are recorded in
`math/lemmas/leaf_support_reduction.md` and
`reviews/leaf_support_reduction_hostile/REVIEW.md`.

### Theorem 2

Assume the published absence of a counterexample through order \(11\).
If \(G\) is a minimum-order counterexample of order \(n\) with common
parameter

\[
 k=\gamma(G)=\gamma^\infty(G),
\]

then

\[
 n\geq\left\lceil\frac{5k}{2}\right\rceil.
\tag{2.3}
\]

In particular, there is no order-12 counterexample with \(k=5\).

#### Proof

The published lower-order result gives \(n\geq12\), so \(G\) is not one of
the seven exceptions of orders four and seven.  Minimum order, component
additivity, and the simplicial reduction make \(G\) connected with
\(\delta(G)\geq2\).  Equation (2.2) applies:

\[
 k=\gamma(G)\leq\frac{2n}{5}.
\]

Rearrangement and integrality prove (2.3).  For \(n=12\) and \(k=5\),
(2.3) would require

\[
 12\geq\left\lceil\frac{25}{2}\right\rceil=13,
\]

a contradiction. \(\square\)

## 3. Complete parameter coverage at order 12

The published premise used here is Observation 5.6 of:

> G. MacGillivray, C. M. Mynhardt, and V. Virgile,
> *Eternal Domination and Clique Covering*,
> Electronic Journal of Graph Theory and Applications **10**(2) (2022),
> 603--624, DOI `10.5614/ejgta.2022.10.2.19`.

It reports that there is no counterexample of order at most \(11\).

### Theorem 3 (order-12 frontier)

There is no finite simple graph \(G\) of order at most \(12\) satisfying

\[
 \gamma(G)=\gamma^\infty(G)<\theta(G).
\tag{3.1}
\]

Equivalently, every counterexample to the \(\gamma\)--\(\theta\) conjecture,
if one exists, has order at least \(13\).

#### Proof

Orders at most \(11\) are excluded by the published premise.  Suppose that
an order-12 counterexample \(G\) exists.  It then has minimum possible order.
The accepted component-additivity reduction makes \(G\) connected.

Let

\[
 k=\gamma(G)=\gamma^\infty(G).
\]

The accepted minimum-parameter theorem gives \(k\geq3\).  The accepted
half-order domination characterization gives

\[
 12\geq2k+1,
\]

so \(k\leq5\).  Exactly three integral cases remain:

1. \(k=3\) is excluded by the complete independently reviewed
   \((n,k)=(12,3)\) theorem in
   `math/lemmas/order12_k3_exclusion.md`.
2. \(k=4\) is excluded by Theorem 1.
3. \(k=5\) is excluded by Theorem 2.

No possible common parameter remains.  Hence no order-12 counterexample
exists.  Together with the published premise, this proves (3.1).
\(\square\)

## 4. Exact claim boundary

Theorem 1 is campaign-certificate-backed for connected order-12,
parameter-four graphs.  The complete parameter-three slice is separately
campaign-certified.  Theorem 2 is analytic relative to the classical
McCuaig--Shepherd theorem and the published through-order-11 premise.
Theorem 3 combines those results.

The campaign has not produced an all-graph coverage certificate for orders
10 and 11, and this note does not imply one.  Theorem 3 should therefore be
reported as:

> a certified order-12 extension of the published order-11 frontier,
> explicitly conditional on the published lower-order computation.

It must not be reported as a universal proof, a counterexample, or a
campaign-only exhaustive enumeration through order \(12\).
