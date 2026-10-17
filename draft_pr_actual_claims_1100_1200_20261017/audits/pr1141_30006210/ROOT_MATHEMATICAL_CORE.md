# Root independent mathematical reconstruction — PR #1141

Recorded 2026-10-17T22:42:05.965332+00:00 (core reconstructed before reading the prior AUDIT or the new reviewers' reports). Audit is ongoing; this is a universal argument, not a finite-search inference. Provisional mathematical completion: 70%; priority and publication remain unassessed. The assigned PROOF and reviewers' brief progress messages have been seen; this is not a claim of blind isolation.

## Exact target

The official EMS report, DOI 10.4171/OWR/2025/9, printed page 445 (PDF page 41), asks whether polynomially small relative influences suffice to prevent two nonzero real multilinear degree-at-most-d functions from having disjoint supports on the uniform Boolean cube. The denominator is the FULL squared Fourier norm, including the constant. The formula is undefined for the zero polynomial; explicitly requiring each polynomial to be nonzero is necessary. This audit concerns that two-polynomial question only, not the distribution conjecture, a cryptographic theorem, complex coefficients, other groups, or approximate compatibility.

Fresh source: https://ems.press/content/serial-article-files/51353; 715061 bytes; SHA256 c70dc7acd811ff38fcfdf40f4dcc1d1ded8b185adb93ed2f9ccdeec1082b9dad. Root read the entire target text and visually inspected page 445. Its printed non-strict old exponential threshold has an endpoint issue already at d=1: f=1+x, g=1-x have disjoint nonempty supports and both relative influences 1/2. The proposed new bound is strictly below the necessary lower bound, so this does not affect it.

## Separator, with constants

Use {0,1} coordinates for the separator only; affine coordinate changes preserve degree and disjointness. For a real function R bounded by 1 on the b-cube, with R(0)=1 and R(e_j)<=0, let P(t) be its expectation at independent Bernoulli(t) bits. Multilinear expansion gives deg P<=m=deg R, |P|<=1 on [0,1], and P'(0)=sum_j(R(e_j)-R(0))<=-b. Classical Markov after rescaling [-1,1] gives |P'|<=2m^2, hence b<=2m^2. The absolute derivative is essential; root visually checked the absolute bars in Kothari et al. v3 page 4 (the plain PDF text extraction drops those bars).

At a restricted node with p and q both nonzero and disjoint, D=max(deg p,deg q)>=1. The multilinear representative s of p^2-q^2 has degree <=2D and is nonzero. Choose a cube point z maximizing |s|. If p(z)!=0 then s(z)>0 and q(z)=0. The other case is symmetric. Select an inclusion-maximal disjoint family M_1,...,M_b of maximum-degree monomial supports of q. The degree of q is positive, since a nonzero constant q cannot coexist with nonzero disjoint p. Fixing all variables outside M_j at z preserves its top coefficient: no strictly containing monomial exists. The resulting restriction of q is nonzero; as it vanishes at z, some nonempty flip E_j contained in M_j makes it nonzero. At that point p=0 and s<0.

Encoding flips of the disjoint E_j by b bits gives R of degree <=2D, bounded in absolute value by 1, with R(0)=1 and R(e_j)<0. Thus b<=8D^2. H=union M_j has size <=8D^3 and meets every maximum-degree monomial by maximality. Querying H therefore decreases deg q on every branch, or makes q identically zero. The other polynomial's degree cannot increase. Repeat: deg p+deg q decreases at least once at every nonterminal stage, initially <=2d, and only previously unqueried variables are queried. Thus total depth T<=16d^4, also <=n on each branch. If one side vanishes, label for the other side; if both vanish label arbitrarily. This is a total binary-valued tree h, with h=1 on supp f and h=0 on supp g, including arbitrary common-zero subcubes.

This construction is explicitly credited to Li, Li, Li, Liu, arXiv:2608.03824v1, Lemma 3.5; root checked its statement and full proof on pages 7–8 against the fresh primary PDF SHA256 bbe559c475aed158422dbf64e13526efe86ba5c2666660c016de8e9c9b8db272. Its use here is an application, not a claimed new separator. Root has not independently certified the paper's cryptographic model and full cryptographic theorem.

## Adaptive covariance, including stopping

Run h's deterministic, nonrepeating tree on uniform X. Let Y be an independent cube point. For each step replace the newly queried X coordinate by the corresponding Y coordinate, retaining all previously replaced coordinates, and write Z_t for the hybrid. Conditional on a complete X transcript, unqueried X coordinates remain independent fair bits; queried Y coordinates are independent fair bits independent of the transcript. Therefore Z_L is uniform and independent of the transcript, and h(X) is transcript-measurable. For arbitrary real u on this finite cube,

Cov(h,u)=E[(h(X)-1/2)(u(X)-u(Z_L))].

Telescope along the actual finite branch. Before any queried index i is exposed, the query history fixes only the old X coordinates, all of which have ALREADY been replaced by independent Y bits in the hybrid. All remaining X coordinates, and Y_i, are fresh fair bits. Thus conditional on this prequery history, (Z_{t-1},Z_t) has exactly the unconditional uniform-resampling-i pair law. This conditioning is before the answer to query i; conditioning after it would be incorrect. Taking absolute values uses |h-1/2|=1/2. Summing over histories gives

|Cov(h,u)| <= (1/2) sum_i r_i E|u(X)-u(X^{resample i})|,

where r_i is the probability that i is queried. Variable branch lengths and arbitrary common-zero labels are included. Also sum_i r_i=E L<=T. No boundedness or measurability of u with respect to the tree is needed beyond u being a real function on the finite cube.

## Independent square/Fourier calculation

Write a=b+x_i c with b,c functions of the other coordinates. Orthogonality yields ||a||_2^2=E(b^2+c^2), and rho_i=E c^2/||a||_2^2. The flip difference of a^2 is 4x_i bc; resampling changes the bit with probability 1/2. Hence for u=a^2/||a||_2^2,

A_i(u)=2 E|bc|/||a||_2^2 <= 2 sqrt(rho_i(1-rho_i)) <=2 sqrt(rho_i).

This independently obtains the constants in the supplied Parseval argument; it handles arbitrary signed real coefficients, nonzero constants, zero and unit influence, scaling and highly unbalanced means. It requires real coefficients (squares nonnegative and b,c real), which the target explicitly assumes.

## Final contradiction and boundary cases

Normalize u=f^2/||f||_2^2 and v=g^2/||g||_2^2, so Eu=Ev=1. The separator has hu=u and hv=0. Writing mu=Eh, the two covariances are 1-mu and -mu; their absolute values sum to 1. With delta the maximum influence over both functions,

1 <= sum_i r_i (sqrt(rho_i(f)(1-rho_i(f)))+sqrt(rho_i(g)(1-rho_i(g))))
  <= 2T sqrt(delta) <=32d^4 sqrt(delta).

Therefore disjoint nonzero supports force delta>=1/(1024d^8). The claimed inclusive sufficient threshold delta<=1/(4096d^8) gives a contradiction 1<=1/2. Positive integer d>=1 is stated. If the true degree is zero the nonzero functions cannot be disjoint; if n<d the same bound remains valid; n=0 can be disposed of separately by constants. Degree reductions, common zeros, repeated coefficients and equality in auxiliary estimates do not cause endpoint trouble. The stronger necessary bound is inclusive; compatibility follows for strict delta<1/(1024d^8), and the stated smaller inclusive threshold is safe.

No central mathematical gap found in this reconstruction. A sound source-credited corollary is not by itself a finding of historical novelty; that decision remains for the separate extensive priority audit.
