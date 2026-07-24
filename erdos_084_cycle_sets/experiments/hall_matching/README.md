# Bounded Hall-matching experiment

Start: 2026-07-24.

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
```

The Python verifier accepts only \(m=6,7\), directly constructs finite sets,
uses FIFO push--relabel rather than Dinic, and verifies each failed flow
against its explicit residual Hall cut.
