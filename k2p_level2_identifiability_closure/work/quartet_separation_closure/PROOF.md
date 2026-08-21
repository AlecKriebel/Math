# Pointwise K2P separation by displayed quartets

This gate binds the topology filters in the four-port raw ledger and the
five-port restoration forest to the pointwise K2P theorem of Englander,
Frohn, Gross, Holtgrefe, van Iersel, Jones, and Sullivant, bioRxiv version 4
(4 July 2026), Propositions 2.9--2.10 and Theorem 2.11.

Let the three quartet topologies be \(A=12|34\), \(B=13|24\), and
\(C=14|23\).  In K2P Fourier coordinates put

\[
 F_A=q_{GGGG}-q_{GGTT}.
\]

On topology \(A\), \(F_A=0\).  On either \(B\) or \(C\), direct tree
substitution gives a product of positive pendant factors times
\(1-a_C\), where the internal-edge K2P eigenvalue satisfies
\(0<a_C<1\).  Hence \(F_A>0\).  Leaf permutations give the analogous
separator for every singleton displayed set.

Also put

\[
 G_B=q_{GGGG}-q_{GGTT}-q_{GTTG}+q_{GTGT}.
\]

This is zero on \(A\) and \(C\), and strictly positive on \(B\).
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
