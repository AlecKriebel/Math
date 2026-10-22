# Literal statement, known obstruction, and remaining scope

## Target and conventions

The supplied ID 2193 / EP-584 asks for two subgraphs of an n-vertex graph of density delta=e(G)/n^2: an H1 of size Omega(delta^3 n^2) with pairwise cycles of length at most 6 and adjacent-pair 4-cycles, and an H2 of size Omega(delta^2 n^2) with pairwise cycles of length at most 8. Here a cycle is simple, pairs contain distinct edges, and the implicit positive constants are uniform in n and delta. No sparsity qualifier occurs in the supplied statement field. The complete inherited background nevertheless explicitly distinguishes fixed positive density from a polynomially sparse regime and records the Fox--Sudakov restriction; that context must not be discarded when identifying the intended research question. Distinct H1 and H2 are allowed; a failure of H2 suffices to refute their joint existence claim.

## Credited prior counterexample

Lazebnik, Ustimenko and Woldar, Proposition 2.1(i),(iii), supplies, for each prime q, the simple bipartite graph D(5,q), with n=2q^5 vertices, degree q, and girth at least 10. Consequently m=q^6, delta=1/(4q^4), and delta^2 n^2=q^2/4. If H2 has two edges, its required cycle would be a cycle of length at most 8 in G, impossible. Thus e(H2)<=1, even when witness cycles may leave H2. For any proposed uniform constant c>0, choose a prime q>2/sqrt(c); then c delta^2 n^2>1. This contradicts the required lower bound. Primes are unbounded, so these are arbitrarily large graphs. The mathematical dependency is [LUW], not a finite experiment. No congruence restriction on q is needed for the lower bound on girth in Proposition 2.1(iii); the congruence in part (iv) is only for equality. Adjacent and disjoint pairs are both excluded, since G itself has no qualifying cycle. This family does not refute the H1 assertion on its own: delta^3 n^2=1/(16q^2) tends to zero. The accepted negative conclusion is the unrestricted H2 assertion and hence the joint unrestricted existence assertion.

The same high-girth obstruction is already given in Theorem 1 and Corollary 2 of the April 21, 2026 note [ULAM]. We do not claim discovery. This verification uses the full D family, avoiding any need to determine its connected components. The note's separate Proposition 4 is not used or certified.

## Why this does not settle the intended research question

[FS], Problem 1.1, asks for some positive beta_0 with a conclusion for small beta in m=n^(2-beta). Its Theorem 1.2 proves the H2 bound, with a stronger adjacent-edge condition, for fixed 0<beta<1/5 and sufficiently large n. Our obstruction has delta=2^(-6/5)n^(-4/5), outside that range. The paper's concluding remarks retain the internal strong-C6 density-power question. We do not infer a solution to it from the unqualified statement-field version. The accepted refutation requires a positive lower-bound constant uniform in n and delta, and does not refute a fixed-density assertion whose threshold for n may depend on delta.

[Duke--Erdős 1982], Corollary 1, concerns a fixed positive density and sufficiently large n, and places the witness cycles inside the selected subgraph. Its final discussion already recognizes high-girth obstructions to unrestricted short-cycle conclusions. Fixed-density quantifiers cannot be silently replaced by all density sequences.

## Current manuscript check

[Li 2026], arXiv:2606.06522v1, publicly states an internal weak-C6 and C8 result through density n^(-1/3), an ambient strong-C6 result when k=o(n^(1/2)), and an internal strong-C6 obstruction for fixed beta in [1/3,1/2). These are manuscript claims in this report: the theorem statements and witness definitions were inspected, but the 20-page proofs were not independently audited. Its weak-C6 conclusion omits the adjacent-edge C4 requirement, so it must not be substituted for H1. This packet does not rely on that manuscript for the refutation.

## References

- [LUW] F. Lazebnik, V. A. Ustimenko, A. J. Woldar, A new series of dense graphs of high girth, Bulletin of the AMS 32 (1995), 73-79, Proposition 2.1. https://arxiv.org/pdf/math/9501231
- [ULAM] A note on the formulation of Erdős Problem #584, dated April 21, 2026, Theorem 1 and Corollary 2. https://www.ulam.ai/research/erdos584.pdf
- [FS] J. Fox, B. Sudakov, On a problem of Duke--Erdős--Rödl on cycle-connected subgraphs, JCTB 98 (2008), 1056-1062, DOI 10.1016/j.jctb.2007.12.003. https://people.math.ethz.ch/~sudakovb/cycle-connected.pdf
- [Duke--Erdős 1982] R. Duke, P. Erdős, Subgraphs in which each pair of edges lies in a short common cycle, Congressus Numerantium 35 (1982), 253-260. https://users.renyi.hu/~p_erdos/1982-35.pdf
- [Li 2026] Eric Li, On the Duke--Erdős--Rödl Problem at the One-Third Threshold, arXiv:2606.06522v1, submitted June 2, 2026. https://arxiv.org/abs/2606.06522v1
