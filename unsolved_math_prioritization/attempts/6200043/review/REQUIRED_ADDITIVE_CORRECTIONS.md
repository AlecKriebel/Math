# Required additive corrections for the 6200043 packet

Reviewed original head: 9eca3cd5e2c2ae85bfc933e5f0b58758bef748b7.
Preserve all 32 frozen files. Add correction documents and a manifest binding the original head, all original SHA-256 hashes, the new files, and any re-review receipt. Do not relabel this work as a sixth proof attempt or a solved conjecture.

## R1. Explicit source-definition normalization (required attribution correction)

Add an explicit note with the following substance:

Kapovich's problem list, printed/PDF page 11, Definition 2, displays mod_Q(E,F)<=phi(Delta(E,F)) and switches from phi to psi in the following line. This packet interprets that display as an apparent typographical error and uses the standard analytic Loewner **lower** bound: Mod_Q(Gamma(E,F))>=Psi(Delta(E,F)), with Psi positive and decreasing, for disjoint nondegenerate continua. Bonk–Kleiner, Geometry & Topology 9 (2005), printed page 227, equation (2.6), is an explicit primary-source statement of this convention. The packet's analytic deductions additionally use its already stated Ahlfors Q-regular representative and Q>1 hypotheses. They do not deduce anything from a literal upper-bound definition or treat the apparent typo as a counterexample to Heinonen's intended problem. The original general conjecture remains unresolved.

Exact source URLs:
- https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf
- https://arxiv.org/pdf/math/0208135

## R2. Reachable-safe chain and transition compatibility (required statement repair)

The Turn 5 geometric criterion is not accepted literally until its chain-state premise is strengthened. One sufficient corrected formulation is:

1. Fix a finite alphabet Sigma, a nonempty finite safe-state set S, an initial state s0 in S, and a total deterministic transition delta on S union {bottom}, with bottom absorbing. For every existing cell word w, its assigned state is delta-star(s0,w); descendant labels use these same transitions.
2. Every y in Y has an infinite word alpha such that, for every k>=0, its prefix cell C_(alpha|k) exists, contains y, and has state in S. Thus the selected point-containing chain consists entirely of reachable safe cells.
3. Every reachable safe state s can reach bottom. Choose a shortest escape word e_s and let N=max_s |e_s|. The graph argument supplies 1<=N<=|S|.
4. Retain nested cells and diam(C_w)<=A rho^|w|, with A>0 and 0<rho<1. For every safe prefix w belonging to one of the selected chains, the descendant C_(w e_s(w)) exists and has a geometric certificate: an actual ambient ball B(z,c0 rho^(|w|+|e_s(w)|)) contained in that descendant (and therefore in C_w), and disjoint from Y. The same c0>0 works for all such w. It is enough instead to supply another compatible escape-word family with a verified uniform length bound; the bound N<=|S| is claimed only for shortest escapes for which the geometric condition has also been verified.

Then for all sufficiently small r the original proof gives porosity constant c0 rho^(N+1)/(2A), or any smaller positive constant. Explain explicitly that the automaton decides graph reachability/escape lengths, while the safe coding chains and actual-ball certificates are separate geometric hypotheses. It does not prove these hypotheses for arbitrary quasisymmetric images of hyperbolic-group boundaries.

An equivalent complete formulation is acceptable. Merely repeating 'missing codeword' or asserting that the automaton itself makes a metric hole is not a repair. Nor is it enough to add the word 'reachable' while leaving 'safe' or transition compatibility unspecified.

## Minor statement clarifications recommended in the same addendum

- Turn 1: specify a single r0>0 such that the homeomorphism/hole hypotheses hold for every y in Y and every 0<r<=r0. The proof's uniform small-scale conclusion uses this quantifier order. If the original was already read this way, this is only explicit notation.
- Turn 3: write U=B(a,s) inside X minus f(X) in the quantitative and measure arguments; take lambda_n>0 for the inverse-Lipschitz statement. Apply the already mandatory h_n=max{1,eta_n(D/s)} substitution to every quantitative denominator and associated displayed conclusion.
- Preserve the existing page-227 bibliographic correction and the unresolved/five-recovery-turn/unknown-historical-count status.

## Required re-review evidence

Return the additive documents, their SHA-256 hashes, a binding to all 32 original unchanged files, and the new pinned head if later publication is separately authorized. A local correction can be re-reviewed before any remote write. This audit itself authorizes no PR, QUEUE change, or remote write.
