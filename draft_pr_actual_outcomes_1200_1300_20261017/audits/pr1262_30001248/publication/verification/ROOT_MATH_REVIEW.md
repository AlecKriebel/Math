# Root mathematical review: PR1262 /30001248

2026-10-17T22:13Z. Estimate: mathematical verification 85%; publication packet 15%.

The eight original files were read in full and authenticated against the submitted
Git snapshot and the historical manifest's seven `entries` (`file`, `bytes`,
`sha256`; self excluded). They remain unchanged. This review checks the complete
triangle conclusion as a consequence of an explicitly named published theorem.
It does not claim to reproduce the deep proof of that theorem.

## Claim and scope

For fixed 0<p<1 and ordinary triangles counted once in G(n,p), let mu and sigma
be the true mean and standard deviation. For every sequence of positive integers
q(n), the relative maximum residue discrepancy tends to zero if and only if
q=o(n^2). The original Scott contribution actually uses absolute deviations;
the bars were checked visually rather than inferred from text extraction.
Its Gaussian unit-cell convention is addressed explicitly. Sparse or varying p,
labeled embeddings, arbitrary induced counts, and general disconnected counts
are outside this theorem. The broader source conjecture is not substituted for
the triangle target.

## Independent line-by-line checks

1. Expanding each product of three independent edge indicators gives the stated
   orthogonal edge-set decomposition. Its second and third components have
   variances 3 C(n,3) p^4(1-p)^2 and C(n,3) p^3(1-p)^3. The leading variance is
   C(n,2)(n-2)^2 p^5(1-p). Their sum equals the covariance-counting formula;
   the ordered shared-edge contribution is 12 C(n,4), not 6 C(n,4).
   The exact residual-to-leading variance ratio is
   `[(1-p)/p + (1-p)^2/(3p^2)]/(n-2)`. Thus the binomial CLT and L2 negligible
   remainder establish the required CLT without using the local theorem.
   Triangle span is one for n>=3 by the empty and single-triangle graphs.
2. Sah–Sawhney Theorem1.1 supplies the uniform integer point-probability error
   delta/sigma, delta=O(n^(-1/2+epsilon)). Root checked the theorem's true
   standard deviation and Section5's unlabelled-copy count (the automorphism
   denominator is explicit). K3 meets connectedness and nondegeneracy; fixed p
   admits a fixed lambda separated from both endpoints. This is an imported
   theorem, not a new local limit theorem or an independent audit of its entire
   Fourier/decoupling proof.
3. The bounded-differences martingale has edge range at most n-2 and squared-range
   sum D=C(n,2)(n-2)^2. Since sigma^2>=alpha D, alpha=p^5(1-p), the two-sided
   tail is at most 2 exp(-2 alpha R^2). The stated R^2=16 log(n)/alpha gives
   2 n^-32. The full integer Gaussian tail is bounded by the two inward grid
   intervals and then 2 exp(-R^2/4) for R>=4, sigma>=1. The latter is at most
   2 n^-16 because alpha<=1/4. Event strictness at the window boundary causes
   no missing terms. All these restrictions hold eventually for fixed p.
4. At most 2R sigma/q+1 integers of a residue lie in the central interval.
   Multiplication by q leaves delta(2R+q/sigma), and both full tails retain
   their q factor. With q<=sigma=O(n^2), all errors vanish. The shifted-mesh
   bound follows by integrating f' on every partition interval and absolute
   summation; for phi its total variation is sqrt(2/pi). The Gaussian error
   is O(q/sigma), uniformly in the residue and fractional mean. In particular,
   arbitrarily slowly subcritical q are covered; no fixed-q constant is used.
5. If q is not o(sigma), restrict to q/sigma>=c and then sigma/q converging to
   r>=0. Eventually q>=2. Relative residue uniformity bounds the first modular
   Fourier coefficient by the discrepancy. Its centered modulus tends to
   exp(-2 pi^2 r^2)>0 by the binomial-projection CLT. The varying-frequency
   justification uses E|Z|<=1, so r=0 and oscillating sequences are covered.
   This is an asymptotic subsequence argument, not a purported uniform
   finite-n lower bound.
6. The Gaussian midpoint error is bounded by ||phi''||infinity/(24 sigma^3).
   This converts the density theorem to the original cell theorem with error
   O(n^(-5/2+epsilon))+O(n^-6)=o(n^-2), epsilon<1/2.
7. The credited 2K2 supplement is sound in its asymptotic range n>=4. Its exact
   identity Y=C(M,2)-W gives the conditional wedge variance using A wedges,
   B=A(4n-10) ordered distinct overlapping pairs, and the remaining ordered
   disjoint pairs. The first-order falling-factorial expansion yields
   B-4A^2/N=-2A, eliminating order n^4. Errors are O(n^3). Conditional
   concentration on O(n^(3/2)) integers and a central binomial atom Omega(1/n)
   give an unconditional atom Omega(n^(-5/2)); its true sigma is Theta(n^3).
   This refutes a uniform Gaussian LLT on the correct span-one lattice.
   It reconstructs Sah–Sawhney's known obstruction and is not new here.

## Validation limits and next gate

No mathematical defect has been found. Independent exact computations and the
fresh candidate-aware adversary's sealed result still require root authentication
before the mathematical gate is recorded. A second family is working only from
the original question and primary literature; its derivation remains independent
until sealed. Finite checks authenticate identities, not the imported asymptotic
theorem. Historical reports about earlier computations remain historical.

Only after mathematical acceptance will the priority audit begin. The retained
draft already disclaims firstness; this does not replace checking earlier
statements and mechanisms. Submission and publication remain pending fresh
whole-package review rounds. The work uses AI extensively and has no external
human peer review or formal proof-assistant certification.
