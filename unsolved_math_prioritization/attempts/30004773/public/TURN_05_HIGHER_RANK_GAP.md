# Attempt 5: higher-rank elimination and the rectangular-matrix route

## Exact reduction for bipartite graphs

Let Gamma have bipartition of sizes a and b. After ordering the parts, every graph-supported alternating matrix has the form

B = [ 0  M ; -M^T  0 ],

where M is an arbitrary a by b matrix supported on the edge board. Its kernel is ker(M^T) direct-sum ker(M), so rank B=2rank M. Consequently, if r_i(S;q) counts rank-i matrices on that rectangular support board S, then

N_i(Gamma;q)=r_i(S;q),
ch(Gamma,i;q)=q^(a+b-2i) r_i(S;q).                           (9)

This puts every rectangular zero-pattern rank-count problem inside the source problem, even for bipartite graphs. It does not impose equality of distinct entries of M: each graph edge still supplies one independent variable.

The familiar Fano-plane example from matrix-counting literature is not a counterexample for the source's odd-prime domain. Lewis and Morales, Rook theory of the finite general linear group, Example 6.4, describe its normalized invertible-matrix count using two polynomials distinguished by even versus odd q. On odd primes that distinction selects just one polynomial. This observation rejects that proposed counterexample; the detailed Fano enumeration is not a theorem used in this packet, nor is any unverified assertion of a stronger nonpolynomial example substituted for it.

Likewise, a wild rank-count theorem for SYMMETRIC matrices cannot be applied directly: symmetric repeated entries and free diagonals differ from independent graph-edge variables in an alternating matrix. A rank-preserving family construction with exact fibre counts would be needed. No such construction is supplied here.

## Exact elimination identity and why it fails to close recursively

An alternating matrix with a nonzero pivot entry a can be written

B=[ A  D ; -D^T C ],  A=[0 a;-a 0],  D=[r;s].

Invertible row and column operations give

rank B=2+rank(C+D^T A^(-1)D).

The residual (j,k) entry is

C_jk+(s_j r_k-r_j s_k)/a.                                  (10)

For a leaf pivot one of r,s is zero; this is precisely why Attempt 3 closes within the same graph family. For a general pivot, formerly forbidden entries acquire products of variables, and those products occur in correlated positions. Treating these new entries as independent variables would change the counting problem and its fibres. The C4 example in Attempt 3 already detects cancellation that the support-only rule misses.

One can condition on all pivot-row data and use (10) as a finite-field algorithm. But the resulting residual families have coupled algebraic constraints. Their symbolic counts have not been proved polynomial, PORC, or non-PORC in this investigation. A per-field enumerator is not the missing uniform theorem.

## Final mathematical disposition

The complete original question remains unsolved by this work. What is proved here is:

1. An explicit complete character construction and the standard exact rank-count factor.
2. A polynomial formula for degree-q characters for every graph.
3. All degree counts for forests by the matching numbers of edge supports.
4. Polynomiality and an effective recovery formula for all degree counts when nu(Gamma)<=3.
5. The exact bipartite reduction and elimination identity, with the failures of the proposed generalisations identified.

For arbitrary graphs with matching number at least four, the precise unresolved issue is the field-size dependence of the independent-edge alternating rank strata N_i(Gamma;q) beyond the counts recovered above. Neither an all-graph symbolic classification nor an odd-prime counterexample to polynomiality has been established here. No assertion is made that the question is a yes/no polynomiality conjecture; the primary source asks the broader descriptive question. No historical priority claim is made.
