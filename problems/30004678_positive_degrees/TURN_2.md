# Turn 2: exact positive comparisons for generic finite-block codes

This is an embedding theorem inside a truth-table fiber, not a count of the whole fiber. It does not construct a new finite-cardinality example. Finite-poset presentations and genericity are classical ingredients; novelty is not established.

Let D be a finite alphabet with at least two symbols. A sequence Z in D^N is 1-generic if, for every computably enumerable open U, either Z belongs to U or some finite prefix of Z has its entire cylinder disjoint from U. Such sequences exist: for each U, the union of U and the interior of its complement is dense open; equivalently one can choose nested cylinders successively meeting U when possible and otherwise avoiding it.

For an injective code f:D→{0,1}^r, encode Z by concatenating f(Z(0)), f(Z(1)), ... , producing a binary set X_f. All these encodings have the same truth-table degree: a finite block is decoded by a total table that has arbitrary values on invalid codewords. Define a partial order R_f on D by a R_f b iff f(a) is coordinatewise at most f(b).

## Exact comparison theorem

For 1-generic Z and injective finite codes f,g,

    X_f ≤p X_g  if and only if  R_g is a subset of R_f.

Sufficiency. For each output coordinate j, define a monotone Boolean function

    H_j(y) = OR over a with f(a)_j=1 of AND over i with g(a)_i=1 of y_i.

Empty conjunction/disjunction have their usual constant values. At y=g(b), a term is true exactly when g(a)≤g(b). The order hypothesis then implies f(a)_j≤f(b)_j. The term a=b proves the reverse implication when f(b)_j=1. Thus H(g(b))=f(b), and applying H separately on every block gives a total positive truth-table reduction.

Necessity. Suppose a positive functional Φ maps X_g to X_f. Let U be the set of alphabet sequences on which at least one output bit of Φ(X_g) differs from X_f. This is c.e. open because Φ is a total truth-table functional and both encodings are local. Z avoids U, so genericity supplies a prefix σ such that equality holds on every sequence extending σ, for every output bit.

If a R_g b but not a R_f b, choose a coordinate j with f(a)_j=1 and f(b)_j=0. In a block beyond σ, replace a by b, holding every other symbol fixed. The entire source binary oracle increases coordinatewise, but that target bit decreases. This contradicts positivity of Φ. No restriction on how many other blocks Φ queries is used. Therefore R_g⊆R_f.

## Every labelled finite partial order appears in this comparison family

Given any partial order R on D, take its principal-ideal code

    f_R(a)_i = 1 exactly when i R a,  for i in D.

This code is injective: mutual equality would imply both a R b and b R a. Moreover f_R(a)≤f_R(b) iff a R b (one implication is transitivity; the reverse uses coordinate i=a). The positive degrees [X_fR] therefore form a copy of the partial orders on the labelled set D ordered by reverse inclusion.

This copy preserves joins: concatenating codes for R and S induces R∩S, while concatenation is positive equivalent to the ordinary disjoint join after a computable permutation. Complementing a code induces the reversed order R^op, so conjugation is also represented inside the family. The equality relation corresponds to the top positive degree of the entire truth-table fiber: its code is the one-hot code, from which every negated bit can be computed positively by the disjunction of the other positions. Thus its complement is positive equivalent to itself, and Turn 1 identifies it with the top.

For alphabet sizes 2,3,4 this gives respectively 3,19,219 distinct degrees in the same fiber. These numbers are already credited finite-cardinality examples in Stephan's different construction; the present generic coding does not prove that this family exhausts its fiber. That distinction is essential.

## Reproduction

The checker exhausts all labelled partial orders through four symbols, verifies ideal-code injectivity and exact induced orders, and checks every pair of the 219 orders on four symbols using the explicit monotone extension or an explicit order-violation witness. It checks intersection joins and reversed-order complements. These finite calculations verify the coding algebra; genericity and the nonexistence of a positive reduction are established by the written forcing argument, not by bounded enumeration of programs.
