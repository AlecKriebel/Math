# Turn 4: a compact-order criterion for positive reductions on a generic cone

This turn goes beyond finite-block encodings. It gives an exact semantic criterion for arbitrary total truth-table functionals at a 1-generic oracle. It does not decide that criterion effectively, count an entire finite fiber, or remove genericity. No novelty certification is claimed.

Let F,G:2^N→2^N be computable total truth-table functionals, and let [σ] be a binary cylinder. Consider the condition

    for all X,Y in [σ], G(X)⊆G(Y) implies F(X)⊆F(Y).             (Mσ)

Here inclusion concerns all infinitely many output coordinates. The condition includes the requirement that F be constant on each G-fiber within the cylinder.

## Effective monotone extension theorem

There exists a total positive truth-table functional H with

    H(G(X))=F(X) for every X in [σ]

if and only if (Mσ) holds.

Necessity is immediate from monotonicity. For sufficiency, fix output coordinate n. Let K_n consist of pairs (X,Y) in [σ]^2 satisfying F(X)(n)=1 and F(Y)(n)=0. This is a computably clopen compact set because F is a total truth-table functional. For N≥0 let K_n,N be its closed subset on which G(X)(i)≤G(Y)(i) for every i<N. The sets are nested compact sets. By (Mσ), their intersection is empty. Compactness implies K_n,N is empty for some finite N.

Such an N can be found effectively. For each trial N, use the computable finite query bounds for F's n-th bit and G's first N bits, together with |σ|, to obtain an input prefix length L determining all these values. Exhaust all pairs of binary strings of length L extending σ and test the displayed finite conditions. The first N with no violating pair terminates, for every n. This is a total computable search under the theorem's hypothesis; the hypothesis itself is not asserted decidable.

Enumerate the finite set P of length-N strings G(X) restricted to N for X in [σ] with F(X)(n)=1, using the same finite prefix search. Define

    H(B)(n)= OR over p in P of AND over i<N with p(i)=1 of B(i).

It is a total monotone truth table. If F(X)(n)=1, the actual p supplies a true term. If F(Y)(n)=0, a true term would produce a positive X whose G-prefix lies below G(Y)'s prefix, contradicting emptiness of K_n,N. Therefore H(G(X))(n)=F(X)(n) throughout the cylinder. Performing this search for each n gives a total positive truth-table functional with a computable use bound. Constant-bit and N=0 cases are included by the empty conjunction/disjunction conventions.

No infinite oracle or undecidable compact-set test is used by the extension algorithm: each finite stage is explicitly exhaustive over a computably bounded number of strings. Compactness proves its termination.

## Exact generic-point criterion

For a 1-generic A,

    F(A)≤pG(A) iff there is a prefix σ of A satisfying (Mσ).

The reverse implication is the extension theorem. For the forward implication, choose a positive functional H realizing the reduction at A. The set of X on which H(G(X)) and F(X) differ at some coordinate is c.e. open. Genericity yields a prefix σ of A avoiding it, so equality holds throughout [σ], and hence (Mσ).

This criterion does not require F or G to be invertible, injective, or block-local. If both outputs happen to be truth-table equivalent to A, it becomes an exact criterion for their positive-degree comparison inside that fiber. A single pair of globally comparable images is not sufficient to refute a pointwise reduction: for nonreducibility the order violation must occur in every cylinder around A. This quantifier is why genericity entered the earlier proofs.

## Controls and limitation

The standard-library checker enumerates every support and binary labeling on the three-bit cube, verifies that monotone compatibility is equivalent to a monotone extension, finds the first finite prefix separating all positive/negative pairs, and checks the explicit DNF on every support point. It also enumerates all maps from a four-element domain into a two-bit cube, including noninjective maps, with all Boolean target maps. These finite checks cover degeneracies in the extension construction; the compactness argument addresses infinite Cantor space.

The unresolved source asks which finite fibers can actually occur without genericity. The criterion is useful for showing why candidate generic codings cannot yield them, but supplies no new finite realized cardinality.
