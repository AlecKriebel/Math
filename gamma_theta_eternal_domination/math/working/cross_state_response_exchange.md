# Cross-state response exchange

## Status and exact boundary

Date: 2026-07-26 (PDT)

This note uses the standard one-guard-moves model.  Attacks are made only at
unoccupied vertices, exactly one adjacent guard moves, and every successor
retained in the family is a dominating configuration.

The purpose is to add genuinely cross-state information to the
single-reference response lists of C-058 and C-059.  The universal
\(\gamma\)--\(\theta\) conjecture is **not resolved** here.  No
literature-priority claim is made.  The proved results are:

1. two independent \(k\)-states in the same eternal family determine a
   layered exchange system which accepts every next target position and
   every next restoration position;
2. consequently, every ordering of the target positions has a
   family-supported monotone \(k\)-guard path between the two states;
3. if the two independent states share \(k-1\) vertices, their complete
   family-response incidence systems are canonically isomorphic: the
   transposition of the exchanged vertices transports every response list
   exactly; and
4. around a closed ridge path, the canonical permutation induced on the
   vertex set must be an automorphism of the response-incidence system at
   the initial state.

The fourth item is a new constraint on the global coloring obstruction, not
a proof that the obstruction vanishes.  The second serious iteration stops
there: full eternal closure forces response-incidence equivariance, but it
does not force the resulting holonomy permutation to be trivial.

## 1. Definitions and independent-state forcing

Let \(\mathcal F\) be an eternal family of \(k\)-vertex dominating
configurations.  If \(S\) is an independent \(k\)-set, then

\[
 S\in\mathcal F.
\tag{1.1}
\]

Indeed, begin at any state of \(\mathcal F\) and repeatedly attack
unoccupied vertices of \(S\).  A guard already on a different vertex of
\(S\) cannot respond, so each response increases the number of occupied
vertices of \(S\).  The process ends at \(S\).

For such a reference state \(S\) and \(x\notin S\), use the
**family-response list**

\[
 L^{\mathcal F}_S(x)=
 \{u\in S:ux\in E(G)\text{ and }S-\{u\}+\{x\}\in\mathcal F\}.
\tag{1.2}
\]

This is the list used in C-059.  It can be smaller than the static viable
list in C-058: domination of the successor is not by itself enough for
membership in a specified eternal family.

## 2. First iteration: the two-state exchange system

Let \(S,T\) be independent \(k\)-sets.  By (1.1), both belong to
\(\mathcal F\).  Put

\[
 C=S\cap T,\qquad A=S-T,\qquad B=T-S,
\qquad |A|=|B|=m.
\tag{2.1}
\]

For \(U\subseteq A\) and \(X\subseteq B\) with \(|U|=|X|\), write

\[
 D(U,X)=(S-U)\cup X=C\cup(A-U)\cup X
\tag{2.2}
\]

and define

\[
 \mathcal Q_{\mathcal F}(S,T)=
 \{(U,X):D(U,X)\in\mathcal F\}.
\tag{2.3}
\]

Thus \((\varnothing,\varnothing)\) and \((A,B)\) are in
\(\mathcal Q_{\mathcal F}(S,T)\).

### Theorem 2.1 (adversarial two-state exchange) — PROVED

The exchange system \(\mathcal Q_{\mathcal F}(S,T)\) has both of the
following closure properties.

1. **Target expansion.**  If \((U,X)\in\mathcal Q_{\mathcal F}(S,T)\)
   and \(b\in B-X\), there is an \(a\in A-U\) such that
   \[
   ab\in E(G),\qquad
   (U\cup\{a\},X\cup\{b\})
   \in\mathcal Q_{\mathcal F}(S,T).
   \tag{2.4}
   \]
2. **Source restoration.**  If
   \((U,X)\in\mathcal Q_{\mathcal F}(S,T)\) and \(a\in U\), there is a
   \(b\in X\) such that
   \[
   ab\in E(G),\qquad
   (U-\{a\},X-\{b\})
   \in\mathcal Q_{\mathcal F}(S,T).
   \tag{2.5}
   \]

#### Proof

For target expansion, attack \(b\) from \(D(U,X)\).  The attack is
unoccupied.  Every guard in \(C\cup X\) is nonadjacent to \(b\), because
these vertices all lie in the independent set \(T=C\cup B\).  Therefore
the responding guard must be some \(a\in A-U\).  Eternal closure gives
exactly the state in (2.4).

For source restoration, attack \(a\) from \(D(U,X)\).  Again the attack is
unoccupied.  Every guard in \(C\cup(A-U)\) is nonadjacent to \(a\), because
these vertices all lie in the independent set \(S=C\cup A\).  The
responding guard must therefore be some \(b\in X\), and eternal closure
gives (2.5).  Every move in both directions is along the displayed graph
edge. \(\square\)

### Corollary 2.2 (every target ordering has a monotone path) — PROVED

For every ordering \(b_1,\ldots,b_m\) of \(B\), there are distinct
vertices \(a_1,\ldots,a_m\) of \(A\) such that

\[
 S=D_0,D_1,\ldots,D_m=T
\tag{2.6}
\]

is a path in \(\mathcal F\), where

\[
 D_j=S-\{a_1,\ldots,a_j\}
       +\{b_1,\ldots,b_j\},
\qquad a_jb_j\in E(G).
\tag{2.7}
\]

Thus the guards give an online perfect matching from an adversarial arrival
order of \(B\) into \(A\), and every prefix matching is supported by an
actual family state.  Starting from any intermediate pair \((U,X)\), every
ordering of \(U\) likewise has a family-supported restoration path back to
\((\varnothing,\varnothing)\).

#### Proof

Apply target expansion successively to
\(b_1,\ldots,b_m\).  At level \(m\), all \(m\) members of \(A\) have been
removed, so the endpoint is \(T\).  The restoration assertion follows by
successive applications of (2.5). \(\square\)

This is stronger information than Hall's inequality: it records compatible
intermediate family states for every adversarial target ordering.  It does
**not** assert that one fixed bijection \(A\to B\) works for all subsets,
and it does not turn the family of independent states into the bases of a
matroid.

## 3. Second iteration: exact transport across a ridge

Now suppose

\[
 S=C\cup\{a\},\qquad T=C\cup\{b\},
\qquad |C|=k-1.
\tag{3.1}
\]

The state \(T\) dominates the unoccupied vertex \(a\).  No member of \(C\)
is adjacent to \(a\), because \(S\) is independent.  Hence

\[
 ab\in E(G).
\tag{3.2}
\]

Let \(\rho=(a\ b)\) be the transposition of the graph's vertex set, fixing
every other vertex.  It maps \(S\) to \(T\) and
\(V(G)-S\) to \(V(G)-T\).  No claim is made that \(\rho\) is a graph
automorphism.

### Theorem 3.1 (ridge response-covariance) — PROVED

For every \(x\notin S\),

\[
 \boxed{\quad
 \rho\!\left(L^{\mathcal F}_S(x)\right)
 =
 L^{\mathcal F}_T\!\left(\rho(x)\right).
 \quad}
\tag{3.3}
\]

Equivalently, the bipartite response-incidence systems based at \(S\) and
\(T\) are canonically isomorphic under the same transposition on guard
positions and attack positions.

#### Proof

First take \(x=b\).  The vertex \(b\) is nonadjacent to every member of
\(C\), while (3.2) holds and \(S-a+b=T\in\mathcal F\).  Therefore

\[
 L^{\mathcal F}_S(b)=\{a\}.
\tag{3.4}
\]

Symmetrically,
\(L^{\mathcal F}_T(a)=\{b\}\), proving (3.3) in this case.

It remains to take \(x\notin S\cup T\).

For the exchanged color, suppose
\(a\in L^{\mathcal F}_S(x)\).  Then

\[
 S-a+x=C\cup\{x\}\in\mathcal F.
\tag{3.5}
\]

This state must dominate \(b\).  No member of \(C\) is adjacent to \(b\),
so \(xb\in E(G)\).  Equation (3.5) is also
\(T-b+x\), hence
\(b\in L^{\mathcal F}_T(x)\).  The converse follows by interchanging
\(S,a\) with \(T,b\).

Now fix \(u\in C\) and suppose
\(u\in L^{\mathcal F}_S(x)\).  The family contains

\[
 D=C-\{u\}+\{a,x\}.
\tag{3.6}
\]

Attack the unoccupied vertex \(b\).  No guard in \(C-\{u\}\) can respond,
because \(T\) is independent.  The only possible responding positions are
\(a\) and \(x\).

The response \(x\to b\) would produce

\[
 R=C-\{u\}+\{a,b\}.
\tag{3.7}
\]

But \(R\) does not dominate \(u\): the vertex \(u\) is nonadjacent to
\(C-\{u\}\cup\{a\}\) by independence of \(S\), and it is nonadjacent to
\(b\) by independence of \(T\).  Thus (3.7) cannot be a family state.
Eternal closure forces the other response, \(a\to b\), and therefore puts

\[
 C-\{u\}+\{b,x\}=T-u+x
\tag{3.8}
\]

in \(\mathcal F\).  The edge \(ux\) already follows from
\(u\in L^{\mathcal F}_S(x)\), so
\(u\in L^{\mathcal F}_T(x)\).  Symmetry proves the reverse implication.

The common colors are fixed by \(\rho\), while \(a\) and \(b\) are
exchanged.  Together with (3.4), these equivalences prove (3.3).
\(\square\)

The domination failure in (3.7) is the essential cross-state mechanism.
It uses the one common guard position missing from both paired successor
states.  At distance two or more, other outside guards may dominate all
missing common positions, so the proof does not inductively make the whole
eternal family invariant under \(\rho\).

### Corollary 3.2 (path transport and response holonomy) — PROVED

Let

\[
 S_0,S_1,\ldots,S_\ell
\tag{3.9}
\]

be independent \(k\)-sets such that consecutive states share \(k-1\)
vertices.  For each step let \(\rho_i\) be the transposition of its
departing and entering vertices, and put

\[
 \rho=\rho_{\ell-1}\cdots\rho_1\rho_0.
\tag{3.10}
\]

Then \(\rho(S_0)=S_\ell\) and, for every \(x\notin S_0\),

\[
 \rho\!\left(L^{\mathcal F}_{S_0}(x)\right)
 =
 L^{\mathcal F}_{S_\ell}\!\left(\rho(x)\right).
\tag{3.11}
\]

If \(S_\ell=S_0\), then \(\rho\) stabilizes both sides of the bipartition

\[
 S_0\ \dot\cup\ (V(G)-S_0)
\]

and is an automorphism of the response-incidence relation

\[
 \mathcal R_{S_0}
 =\{(u,x):u\in L^{\mathcal F}_{S_0}(x)\}.
\tag{3.12}
\]

In particular, if \(\rho(x)=x\), then

\[
 \rho\!\left(L^{\mathcal F}_{S_0}(x)\right)
 =L^{\mathcal F}_{S_0}(x).
\tag{3.13}
\]

A fixed outside vertex with singleton response list
\(\{u\}\) therefore forces \(\rho(u)=u\).

#### Proof

Apply Theorem 3.1 at each step.  Each partial product maps the complement
of the current reference state onto the complement of the next one, so all
successive list evaluations are defined.  Composition gives (3.11), and
the closed-path conclusions are immediate. \(\square\)

This makes one limited sense of response holonomy rigorous: the canonical
product of forced ridge transpositions need not be the identity, but full
eternal closure forces it to preserve the complete first-response
incidence system.

## 4. Stress tests and rejected strengthenings

### \(C_4\): exchange paths do not canonically label physical guards

For the two opposite independent states

\[
 S=\{0,2\},\qquad T=\{1,3\},
\]

the symmetric difference has size four, not two.  Theorem 2.1 applies and
allows several monotone paths between them.  The accepted four-move loop
in \(C_4\) swaps the two physical guards while returning to \(S\).
Therefore Theorem 2.1 must not be strengthened to a unique matching,
path-independent physical labels, or a single bijection supporting all
exchange paths.  The graph still satisfies

\[
 \gamma(C_4)=\gamma^\infty(C_4)=\theta(C_4)=2.
\]

### \(C_7\): ridge transport alone does not kill a facet loop

The accepted seven-facet loop in \(C_7\) has a nontrivial three-cycle of
the ridge-transported positions.  There is no eternal three-family on
\(C_7\), so Theorem 3.1 does not apply.  This is precisely why full family
membership in (1.2), rather than static viability of a dominating swap, is
essential.  The theorem does not rehabilitate the false assertion that
forced facet moves alone have trivial holonomy.

### `FCpbO`: the theorem does not imply simple connectivity

This accepted equality graph has

\[
 \gamma=i=\alpha=\gamma^\infty=\theta=3
\]

and nonzero first homology of the complement flag complex.  Its six
maximum-independent facets have ridge graph

\[
 012-123-234-345-356-056,
\tag{4.1}
\]

a path.  Theorem 3.1 transports response incidence along this path but
makes no statement that contracts the separate topological cycle.  Thus it
is consistent with, and does not imply the false strengthening of, simple
connectivity.

### `J@l|bfNuVK_`: finite-horizon survival is not enough

For this accepted near-miss,

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

All maximum independent triples survive several finite kernels and all
single-reference viable lists pass Hall, but there is no eternal
three-family.  The hypotheses of Theorems 2.1 and 3.1 therefore fail.
The proof of Theorem 3.1 uses closure at the paired successor state (3.6);
replacing full eternal closure by local balance, Hall, or a fixed finite
survival horizon is unsupported.

## 5. Second-iteration gate

The natural hoped-for strengthening was:

> response covariance around every ridge loop forces the loop permutation
> to be the identity.

That conclusion does not follow from Theorem 3.1.  What is proved is only

\[
 \rho\in\operatorname{Aut}(\mathcal R_S)
\tag{5.1}
\]

for the particular vertex permutation induced by the loop.  A response
incidence system can have nontrivial automorphisms.  C-058 and C-059 supply
Hall and collision constraints on this system, but neither constraint
proves rigidity.  Asking for path-independent colors without an additional
rigidity mechanism returns to the already blocked global list-coloring
problem.

This lane is therefore **STOPPED AFTER TWO SERIOUS ITERATIONS** at the
following exact boundary:

\[
\boxed{
\begin{array}{c}
\text{full one-guard closure forces canonical cross-state response}\\
\text{covariance, but no proved mechanism forces the allowed}\\
\text{response-holonomy automorphisms to be trivial.}
\end{array}}
\]

A future continuation would have to prove one of the following genuinely
additional statements:

1. the response-incidence system of a minimum counterexample is rigid under
   every ridge-loop permutation;
2. enough singleton private markers are fixed by every loop to force all
   guard positions fixed; or
3. a deeper-state analogue of Theorem 3.1 supplies invariants beyond the
   first response layer.

None of these three statements is claimed here.
