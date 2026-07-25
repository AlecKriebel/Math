# Bounded Hall-matching experiment

Start: 2026-07-24.

The completed outcome and stop decision are recorded in
[`CONCLUSION.md`](CONCLUSION.md).

This experiment tests one possible proof mechanism for the Boolean down-set
inequality in `proofs/SHADOW_PROGRAM.md`.  It is deliberately restricted to
\(m=6,7\).  The first graph permits at most one downward parameter deletion;
if that graph fails, there is exactly one enlargement, to at most two
deletions.  No larger values of \(m\) are part of this experiment.

For \(P\subseteq[2m]\) with \(1\in P\), retain the notation
\(\mathcal A_P,\mathcal H_P,U=V(P)\) from the safe/unsafe decomposition and
put

\[
\begin{aligned}
d(P)&=|\mathcal A_P|-|\mathcal A_P\vee U|,\\
b_0(P)&=|(\mathcal H_P\vee U)\setminus\mathcal H_P|,\\
b_1(P)&=
 |((\mathcal A_P\vee U)\cup(\mathcal H_P\vee U))
   \setminus\mathcal H_P|,\\
b(P)&=b_0(P)+b_1(P).
\end{aligned}
\]

Thus the exact identity is \(g_m(P)=b(P)-d(P)\).

For a deletion radius \(r\), form an integer transportation graph with a
left vertex \(L_P\) of supply \(d(P)\), a right vertex \(R_Q\) of capacity
\(b(Q)\), and an edge

\[
L_P\longrightarrow R_Q
\quad\Longleftrightarrow\quad
Q\subseteq P,\quad |P\setminus Q|\le r,\quad 1\in Q.
\tag{H_r}
\]

Equivalently, one may expand \(L_P\) into the noncanonical members of the
fibres of \(\mathcal A_P\to\mathcal A_P\vee U\), and expand \(R_Q\) into the
two typed boundary sets counted by \(b_0(Q),b_1(Q)\).  Since adjacency
depends only on the parameter labels, the compressed integral flow is
exactly equivalent to a matching of the expanded units.

If all supply is transported, then for every \(P_0\ni1\),

\[
\begin{aligned}
\sum_{\substack{P\subseteq P_0\\1\in P}}d(P)
&\le
\sum_{\substack{Q\subseteq P_0\\1\in Q}}b(Q),
\end{aligned}
\]

because every destination \(Q\) of a source \(P\subseteq P_0\) is still a
subset of \(P_0\), and no right capacity is used twice.  Hence a full
transport proves the desired down-set inequality at that \(m\).

Finite success at \(m=6,7\) is not itself a research result.  The experiment
counts only if the integral flows and their alternating paths expose one of:

1. a deterministic all-\(m\) transport rule;
2. a uniform bounded-congestion rule that can be proved for every \(m\); or
3. a genuine infinite Hall lemma for these Toeplitz OR-closures.

On failure, the minimum cut must be recorded as an exact Hall obstruction.
The experiment then either uses its sole enlargement from \(r=1\) to \(r=2\)
or stops.  Enumeration beyond \(m=7\) is outside scope.

There are two distinct versions of this graph.

- The **raw** graph uses supply \(d(P)\) and capacity \(b(P)\).  It permits
  local capacity at a parameter to act as a relay: an upper source can use
  boundary capacity at \(P\) while \(P\)'s own collision supply moves to a
  child.
- The **net** graph first cancels \(\min(d(P),b(P))\) locally and uses supply
  \((-g(P))_+\) and capacity \(g(P)_+\).  It forbids such implicit relays.
  A net radius-\(r\) matching gives a particularly simple canonical raw
  matching with at most \(r\) deletions.

The net graph is strictly stronger at a fixed radius.  It is included because
alternating paths in the raw radius-one graph canonically collapse to
multi-deletion net transports.

The parameter-only graph is a capacity baseline, not yet an object-level
injection.  A structurally meaningful refinement labels each collision unit
by a safe signature and each boundary unit by its typed boundary signature,
then permits an edge only when bounded changes to a row representation
actually produce that boundary signature.  Capacity success must not be
confused with success of this representation-aware refinement.

## Relay interpretation

There is an exact finite-DAG reformulation of the raw radius-one graph.  Put

\[
\ell(P)=(d(P)-b(P))_+,\qquad
r(P)=(b(P)-d(P))_+,\qquad
c(P)=\min(d(P),b(P)).
\]

A raw radius-one matching exists if and only if the Boolean deletion DAG has
an integral downward transshipment in which \(\ell(P)\) units originate at
\(P\), at most \(r(P)\) units terminate at \(P\), and at most \(c(P)\) units
relay through \(P\).  A matching gives this flow after maximizing diagonal
matches; conversely, diagonal flow \(c(P)\) minus the relay load reconstructs
the matching.

For the normalization, process parameters from top to bottom.  If diagonal
flow \(z_P\) plus incoming cross-flow \(I_P\) is below \(c(P)\), redirect that
much outgoing cross-flow to the diagonal.  Afterwards set

\[
t_P=c(P)-z_P,\qquad a_P=z_P+I_P-c(P).
\]

Then \(0\le t_P\le c(P)\), \(0\le a_P\le r(P)\), and the outgoing and incoming
cross-flows are respectively \(\ell(P)+t_P\) and \(t_P+a_P\).  These are
exactly the source, relay, and absorption conservation laws.  The equations
reverse to recover the matching.

This explains why raw radius one can succeed when net radius one fails:
local collision/boundary pairs act as relay capacity.  It does not bound
path length in general, and is standard flow structure rather than the
needed Toeplitz-specific lemma.

## Exact all-\(m\) simplification

The typed formulation exposes an identity valid for every \(m\), not merely
for the tested cases.  The bottom generator is always

\[
G_{m,P}(-m)=\{-m,m\}.
\]

For \(A\in\mathcal A_P\), the unsafe trace \(A\cup\{m\}\) belongs to
\(\mathcal H_P\).  Since \(1\in P\) implies \(m\in U\),

\[
(A\cup\{m\})\cup U=A\cup U.
\]

Consequently \(\mathcal A_P\vee U\subseteq\mathcal H_P\vee U\), and the two
underlying boundary families in the decomposition coincide.  If

\[
\mathcal B_P=(\mathcal H_P\vee U)\setminus\mathcal H_P,
\]

then

\[
e_0(P)=|\mathcal A_P\vee U|+|\mathcal B_P|,\qquad
e_1(P)=|\mathcal B_P|,\qquad
g(P)=2|\mathcal B_P|-d(P).
\]

The two channels remain distinct typed copies in a matching.  Thus a
successful typed matching is equivalently a congestion-two charge to the
single underlying boundary family.  This is a genuine infinite structural
lemma, but it does not establish the needed charge.

## Representation-aware result

The object-level graph uses every non-top safe signature in a
\(\pi_P(A)=A\setminus U\) fibre as a left unit.  An edge to a typed boundary
trace at \(Q=P\) or an immediate child \(Q=P\setminus\{p\}\) exists only when
there are labelled row selections \(B,B'\subseteq J_m\) such that
\(\Phi_P(B)=A\), \(\Phi_Q(B')\) produces that endpoint, and the frozen edit
condition holds.

Stage A permits no edit, one add, one remove, or one exchange:

\[
|B\setminus B'|\le1,\qquad |B'\setminus B|\le1.
\]

It fails with exact Hall deficiencies \(20\) and \(268\) at \(m=6,7\).
The experiment's sole enlargement uses \(|B\mathbin\triangle B'|\le2\),
adding only double-add and double-remove cases.  It has full matchings:

\[
\begin{array}{c|r|r|r|r|r}
m&|L|&E_A&\nu_A&E_B&\nu_B\\ \hline
6&11{,}155&722{,}305&11{,}135&851{,}589&11{,}155\\
7&101{,}623&9{,}145{,}839&101{,}355&
  11{,}249{,}586&101{,}623.
\end{array}
\]

Incrementally repairing the Stage-A matchings needs alternating depth at
most two for \(m=6\) and three for \(m=7\).  This is encouraging, but the
\(m=7\) repairs split into 32 coarse templates and include both double
removals and double additions.  No canonical all-\(m\) matching rule or
uniform depth theorem has been proved.

## Reproduction

The discovery implementation and independent verifier use different family
representations and different maximum-flow algorithms:

```sh
c++ -O3 -std=c++17 -pthread hall_transport.cpp -o /tmp/hall_transport
/tmp/hall_transport --m 6 --radius 1 --threads 4
/tmp/hall_transport --m 7 --radius 1 --threads 4
/tmp/hall_transport --m 6 --radius 1 --threads 4 --net
/tmp/hall_transport --m 7 --radius 1 --threads 4 --net
/tmp/hall_transport --m 6 --radius 2 --threads 4 --net
/tmp/hall_transport --m 7 --radius 2 --threads 4 --net
python3 independent_hall_verify.py --m all
c++ -O3 -std=c++17 -pthread representation_hall.cpp \
  -o /tmp/representation_hall
/tmp/representation_hall --m 6 --threads 2 --quiet-progress
/tmp/representation_hall --m 7 --threads 2 --quiet-progress
python3 independent_representation_spotcheck.py
```

The Python verifier accepts only \(m=6,7\), directly constructs finite sets,
uses FIFO push--relabel rather than Dinic, and verifies each failed flow
against its explicit residual Hall cut.

The representation-aware C++ verifier additionally recomputes every edge
certificate.  The independent Python spot-check reconstructs the complete
\(m=6\) typed graph with direct sets and uses an elementary matcher; it
reproduces both edge counts, all isolated vertices, and both maximum
matching cardinalities.
