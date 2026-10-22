# A precise meromorphic-extension bridge and its remaining gap

## Conditional bridge

Let S be an irreducible normal compact complex space of dimension p, and let Σ be an effective Cartier divisor. Suppose h₁,…,h_p are algebraically independent holomorphic functions on S\Σ. Assume each h_i has locally polynomial growth along Σ: if σ is a local equation for Σ, then on each sufficiently small neighbourhood there are C>0 and an integer N≥0 such that

    |h_i| ≤ C |σ|^(−N).

Then a(S)=p.

Proof. The function σ^N h_i is locally bounded and holomorphic off Σ. The Riemann extension theorem on a normal complex space extends it holomorphically across Σ. Hence h_i extends meromorphically. Its extensions remain algebraically independent, since any polynomial relation restricts to one on the dense open set S\Σ. Thus a(S)≥p, while a(S)≤dim S=p. ∎

Now suppose there is an irreducible compact incidence space G, with dominant projections q:G→S and e:G→Z, where Z is a compact connected complex manifold and e is generically finite. Replace G by its normalization if necessary. Pullback injects M(S) into M(G). A proper generically finite holomorphic map induces a finite extension M(G)/M(Z). More explicitly, its Stein factorization is G→T→Z, with T normal, the first map a proper modification and the second finite. Modification invariance gives M(G)=M(T). For a meromorphic function on T, the elementary symmetric functions of its values on a generic finite fibre extend meromorphically on Z, including across branch and pole loci: locally on Z, finite direct image and a common denominator reduce this to the holomorphic symmetric-function construction. The resulting monic polynomial has degree at most the finite covering degree. Every finitely generated intermediate field is simple in characteristic zero and has degree at most that same bound, so the entire field extension is finite. This argument starts with functions meromorphic on the whole compact space; it gives no extension theorem for functions defined only off a divisor. Consequently a(G)=a(Z), so the preceding growth condition implies a(Z)≥p.

This isolates a sufficient bridge in the minimal-parameter incidence setting. The original geometric hypotheses have not been shown here to supply p functions with these growth bounds.

## Why finite traces do not supply the growth bound

For the finite map z=w^d on punctured discs and h(w)=exp(1/w), the trace is

    Tr(h)(z) = d ∑_{k=0}^∞ z^(−k)/(dk)!.

Proof. Sum the expansion ∑_{m≥0} w^(−m)/m! over the d inverse images w, ζw,…,ζ^(d−1)w, where ζ is a primitive d-th root of unity. The root-of-unity sum is zero unless d divides m, in which case it is d. The power series is absolutely convergent on every compact subset of the punctured disc, so the termwise sum is justified. ∎

Every displayed negative-power coefficient is nonzero. The trace has an essential singularity at z=0, so passage through a finite map does not turn holomorphic functions on a complement into meromorphic functions on a compactification. This example is local and is not a counterexample to the original compact geometric problem.

## Remaining mathematical gap

The missing assertion is genuinely global: establish enough meromorphic extensions with controlled boundary growth, or construct global sections that recover the higher-jet parameters missed by initial normal data, or supply another mechanism excluding the residual parameter geometry. These arguments do not prove such an assertion. No general proof, counterexample, or novelty claim is made.
