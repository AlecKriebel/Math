# Target scope and claim limits

Target: UnsolvedMath 2307031 / AMR-022-7031, queue rank 689,
Hayman--Lingham Function Theory Problem 7.31.

The governing primary statement is on printed page 169 of
https://arxiv.org/pdf/1809.07200v2 (PDF page 170). It assumes a_1>0,
0<=a_n<=n, and two successive partial sums b_n and c_n. It asks which
functions f make sum f(c_n/a_n) converge universally, and suggests
comparison with sum f(n^2) under an unspecified smoothness assumption.
The accompanying update reports no progress. This is a historical report,
not a verified assertion that the question is still open today.

The f-class and quantifiers must be explicit. The counterexample proves:

    There exist a single admissible infinite sequence and a single positive,
    strictly completely monotone entire f for which sum f(n^2) converges
    but sum f(c_n/a_n) diverges.

This is not just a finite example or a family with changing f. The sequence
is recursively defined in finite rational blocks. The function is an
infinite positive Laplace mixture adapted to those same blocks. Uniform
complex convergence of every derivative is proved. Ratios at a_n=0 are
interpreted as +infinity with f(+infinity)=0.

The counting theorem proves a uniform O_{a_1}(sqrt(T) log T) upper bound
for the total number of finite ratios <=T. A matching-order construction
has a different admissible sequence for each square T. It does not imply
one sequence realizes all extremal counts simultaneously.

The sufficient condition is stated for nonnegative, locally bounded,
eventually nonincreasing f. It extends the source's power-decay examples,
but is not claimed necessary. The gap between the logarithmic exponents
1 and 2, and the shape condition sqrt(t)f(t) nonincreasing, remain open
within this investigation.

## Status recommendation

Broad classification: unresolved after five substantive approaches.
Recommended broad-target status: exhausted / partial, not solved.

Complete candidate subresults: analytic-completely-monotone comparison
counterexample, matching-order uniform sublevel count, sufficient weighted
integral criterion, and exact controls. Each needs fresh independent audit
before any remote publication. No external communications, remote writes,
release, DOI request, or publication occurred in this investigation.

Novelty and historical priority are not established by negative searches.
The source-linked Borwein article's proof was not inspected and is not
used as a premise of the authored proofs.
