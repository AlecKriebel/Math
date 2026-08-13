# Independent audit of the hard enabled-181 access-word corollary

**Audit time:** 2026-08-12 01:42 PDT  
**Verdict:** **PASS (strictly local scope).**

This audit concerns only the analytic stopped estimate for the 181 enabled
two-active promotion incidences on the hard 333-pair selector and the finite
identity of that scope.  It does not certify any complete support pair and
does not certify global T3-2.

## 1. Frozen targets and parent dependency

The audited target files have SHA-256 hashes

```text
9be70e2b6c9ce5c4762bf3130246f1ea660bea73f41aa7abdd997853cc0a6b04  research_notes/proof_first_hard_enabled181_access_word.md
7a4397e01c36767474d1040e7937a992f1caa551192e936872e7ed6057243582  src/hard_enabled181_access_word.py
33a8a9337a131bf67b9f562134cec2c418b2ab15b9f5b39381fab5c0ba4260de  tests/test_hard_enabled181_access_word.py
```

The imported all-reaction word lemma and its earlier independent audit were
also replayed at

```text
4764849b05915b9005d68ac885c512a906af439430e8db8a7131f04645224e29  research_notes/two_active_easy_943_common_w_theorem.md
c07f9d9d79574d1c590b03d552de574882c141c84f35fdf452508689e46743f6  research_notes/two_active_easy_416_independent_audit.md
c03e25156ec3718bcf954560a92926b898083fce660018314a7373613ccd4b73  src/two_active_easy_common_w.py
2ff48a23cab8ff449b43058d1a244ff5be453746e51ad2b4cbf0e25705317a91  tests/test_two_active_easy_common_w.py
```

The parent suite passed all ten tests.  The proof below independently
rechecks the part of its Lemma 3.1 used by the hard corollary rather than
inferring the stochastic estimate from table membership.

## 2. Arbitrary-orientation access path

Fix one incidence, one strongly connected orientation of both linkages,
one positive rate vector, and a sequence realizing its exact D-tier
descriptor.  Let $L$ be a proper-top linkage with top intersection
$K=L\cap\mathcal T$ containing the enabled seed $v_0$.  Strong
connectivity gives a directed path from $v_0$ to $L\setminus K$.
Erase loops and stop at the first exit:

\[
 v_0\longrightarrow v_1\longrightarrow\cdots
 \longrightarrow v_{m-1}\longrightarrow v_m,
 \qquad v_0,\ldots,v_{m-1}\in K,
 \quad v_m\notin K .
\]

This is a graph proof for every orientation, not a search over orientations.
The supports have at most five vertices, so $m\le4$.  The first source is
enabled.  After the reaction $v_{j-1}\to v_j$, the physical state contains
the product complex $v_j$, so $v_j$ is an actually enabled source for
the next reaction.  This remains true when the word creates the formerly
inactive species.  Thus no formal support path is substituted for a
physical reaction word.

Let $A_n\to\infty$ be the common propensity scale of the global top
D-tier.  Exact-tier equivalence makes the monomials of every preterminal
source comparable with $A_n$.  A bounded number of preceding reaction
jumps changes these comparisons only by fixed factors: the two active
coordinates diverge, while the newly created inactive population remains
bounded by the word length.  Fixed positive rate constants therefore give

\[
 c_jA_n\le \lambda_{v_j\to v_{j+1}}(X_j)\le C_jA_n
 \quad (j<m).
\]

Every physical source in the network has rate at most $CA_n$ at these
boundedly displaced states.  Since there are finitely many channels, each
desired race has conditional success probability bounded below.  Their
finite product gives a constant $p_0>0$, allowed to depend on the fixed
orientation and rates but not on $n$.  The terminal target is outside
$K=L\cap\mathcal T$, hence below the global top D-tier and has a
diverging factorial gap $g_n\to\infty$.

## 3. All clocks, duration, and actual endpoint moments

At each stage retain every mass-action clock and stop either on the desired
reaction or on the first competing reaction.  The total hazard is at least
$cA_n$, and there are at most four stages.  Standard exponential-race
domination therefore gives, for every fixed $q>0$,

\[
 \mathbb E\tau_n^q=O(A_n^{-q}).
\]

Here is the endpoint calculation with no deleted competitor.  Put

\[
 H_\ell(x)=\sum_i\log(x_i!)+\ell\mathbin\cdot x,
 \qquad G_\ell=K+H_\ell\ge1,
 \qquad W_\ell=G_\ell^4,
\]

where $\ell$ is any fixed correction.  For a firing $y\to z$, from
$x$ to $x'=x-y+z$, the exact factorial identity is

\[
 H_0(x')-H_0(x)
 =\log\frac{(x')_{\underline z}}{x_{\underline y}}. \tag{3.1}
\]

Suppose a competing channel has current rate $b_n>0$.  Its post-firing
target factorial is at most $CA_n$, because the target is a network
complex and the current state differs from the descriptor state by only a
bounded amount.  Equation (3.1) and fixedness of $\ell$ imply

\[
 (\Delta H_\ell)^+
 \le C+\log^+(A_n/b_n).
\]

The desired clock keeps the total hazard at least $cA_n$, so that
competitor's race probability is at most $Cb_n/A_n$.  Consequently its
contribution to any fixed positive endpoint moment is bounded by

\[
 C\,{b_n\over A_n}
 \left\{1+\log^+{A_n\over b_n}\right\}^q\le C_q. \tag{3.2}
\]

The function on the left is bounded also when $b_n/A_n$ stays in a fixed
compact interval above one.  Summing over the fixed channel set and the at
most four word positions proves

\[
 \sup_n\mathbb E[((\Delta H_\ell)^+)^q]<\infty
 \quad\text{for every fixed }q>0. \tag{3.3}
\]

The preceding prescribed top-to-top jumps cost only $O(1)$, so they do
not alter (3.3).  In particular the orders $q>8$ required by the later
common-potential interface are available.  The endpoint is the state after
the actual interrupting or completing reaction, its population displacement
is bounded, and the duration and $W_\ell$-endpoint are integrable.  Any
reflected debt marks can be updated deterministically along these same
physical jumps; the stopping rule is mark-blind.

## 4. Fourth-power decrement and path labels

On successful completion, (3.1), exact top-tier equivalence along the
prefix, and the terminal strict tier drop give

\[
 \Delta G_\ell=-g_n+O(1),
 \qquad g_n\to\infty.
\]

Because all complexes have molecularity at most two,
$g_n=O(\log(2+\lVert x_n\rVert_1))=o(G_\ell(x_n))$.  Hence the exact
binomial expansion gives a successful contribution at most
$-cG_\ell^3g_n$.  On every other branch, only the positive increment can
increase $W_\ell$; (3.3) through order four bounds its expected
contribution by $O(G_\ell^3)$.  With success probability at least $p_0$,

\[
 \mathbb E[W_\ell(X_{\tau_n})-W_\ell(x_n)]
 \le -cp_0G_\ell(x_n)^3g_n+O(G_\ell(x_n)^3).
\]

The negative term dominates because $g_n\to\infty$.  Adding
$\mathbb E\tau_n=O(A_n^{-1})$ preserves the claimed stopped drift.
This proves the estimate for an arbitrary fixed $\ell$, including a
rate-adjusted correction chosen elsewhere for the same support pair.

The strong-Markov handoff has an unambiguous path label:

* $P$ is completion of every prescribed reaction, including the terminal
  top-tier exit;
* $B$ is the first nonprescribed physical reaction at any word stage.

Both labels stop immediately at their causing reaction.  Thus a later
cleanup cannot relabel a $B$-path as $P$, every boundary-causing reaction
is charged, and both actual endpoints are reclassified under the identical
$W_\ell$.

## 5. Finite scope replay and certification boundary

Finite computation was used only to replay the incidence scope and the
analytic premises, not to prove the orientation or probability statements.
It returned

```text
incidences: 181
pairs:      139
rows SHA-256:    5e8c7399b0635d616fba850ea1c6aeccfe6e9ebcad8501c6895b8e2eb7dcd0f6
payload SHA-256: 500469227922b21d38ce135e2af00fe37446773f04e26e5208e97e6a723d442b
```

All 181 rows are members of the previously audited 929 seeded-access
domain.  Direct premise replay additionally found that every row has one
enabled top seed, every global top scale diverges, and every selected
proper-top linkage has three to five vertices.  The frozen four-test target
suite passed.

The local enabled-181 corollary therefore passes strict audit.  The
certificate's audit flag was deliberately left unchanged as required by
the audit assignment.  Its pair-recurrence and global-T3-2 flags correctly
remain false: the other failed descriptors on those 139 pairs still have
to be composed under the common potential and independently audited.
