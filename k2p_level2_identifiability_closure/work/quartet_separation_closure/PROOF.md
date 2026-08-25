# Pointwise K2P separation by displayed quartets

This gate binds the topology filters in the four-port raw ledger and the
five-port restoration forest to the pointwise K2P theorem of Englander,
Frohn, Gross, Holtgrefe, van Iersel, Jones, and Sullivant, bioRxiv version 4
(4 July 2026), Propositions 2.9--2.10 and Theorem 2.11.

Let the three quartet topologies be \(A=12|34\), \(B=13|24\), and
\(C=14|23\).  In K2P Fourier coordinates put

\[
 F_A=q_{CCCC}-q_{CCTT}.
\]

Put \(P=s_1s_2s_3s_4\), and let \(g_I\) denote the singleton-sector
eigenvalue on the internal edge.  Direct tree substitution gives
\(F_A=0\) on \(A\) and \(F_A=P(1-g_I)>0\) on \(B,C\).  Leaf permutations
give the analogous separator for every singleton displayed set.

Also put

\[
 G_B=q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}.
\]

This is zero on \(A,C\) and equals \(2P(1-g_I)>0\) on \(B\).
Again, leaf permutations give one such separator for any selected missing
topology.

A network distribution is a positive mixture of its displayed-tree
distributions.  Therefore:

* if one displayed set is a singleton and the other contains another
  topology, a permuted \(F\) is zero on the first model and positive on the
  second;
* if two displayed sets both have size at least two and differ, choose a
  topology present in one and absent from the other; the corresponding
  permuted \(G\) is positive on the first model and zero on the second.

Thus two binary semi-directed K2P networks with different displayed quartet
sets on any four-leaf restriction have disjoint strict positive images.  The
statement is pointwise and directional: it rules out both containments,
including a lower-dimensional source inside a higher-dimensional target.

The only analytic hypotheses used are strict positive inheritance weights
and internal K2P Fourier eigenvalues in \((0,1)\).  Every edge in
\(\mathcal D_+\) satisfies them.  This is exactly the relation tested by the
graph compiler's complete displayed-switching sets `quartet_splits`; no
generic-variety inference is substituted for the sign theorem.

Corollary 2.12 of the same source then gives pointwise recovery of the
labelled tree of blobs: nonisomorphic trees of blobs force a four-leaf
restriction with different displayed quartet sets, hence disjoint K2P
images.

## Exact convention and transport replay

`QUARTET_SEMANTICS_SPEC.json` fixes the character order, Klein-four codes,
edge spectrum, two nonzero sectors, principal and continuous-time domains,
canonical coordinate dictionary, and the six literal `F`/`J` bodies.
`verify_quartet_logic.py` derives every tree monomial from those declarations;
it does not assume an abstract zero set. It proves the six canonical pullback
tables and all 288 combinations of a leaf permutation, licensed character
transport, and formula. The only fixed-spectrum character transports are the
identity and the global `C<->T` swap.

## Complete promoted-terminal binding

`verify_quartet_terminal_bindings.py` independently converts each committed
displayed-set mismatch into an actual leaf-labelled sparse Fourier expression.
It streams 4,414,710 terminal references across all six promoted finite
layers, binds all 888 certificate IDs, checks that every registry entry is
used, and reports zero missing or dangling entries. For labels outside the
selected quartet the Fourier character is fixed to zero, so these are exactly
the full-tensor coordinates induced by marginalization.

The terminal binder deliberately does not infer displayed splits from a graph.
That premise is supplied by the independent graph producer/replayer for each
ledger. Conversely, those graph programs do not supply the literal Fourier
pullback. Their composition is the complete certificate. Mutation suites alter
the spectrum, coordinate word, split, sign side, leaf transport, proof key,
row reference, and graph-to-proof assignment; all are rejected.
