# Independent mathematical reconstruction for PR786

Validation of the existing result only; original1/5 is unchanged. INITIAL_POSITION.json was recorded after the complete selected record, paper and metadata, before any PR786 historical/root review conclusions. This is a new problem assignment in an explicitly reused reviewer session, not a freshly initialized session.

The exact claim is: for algebraically closed k of odd prime characteristic p, q=1, r=2p-1 and lambda=(r-1,1), the source-convention FI_N(lambda) is simple of dimensionr-1 at stable N>=r, while I_n(lambda) is nonprojective for every n>=2. This is stronger than exhibiting failure at rank2; the existential rank quantifier in the original problem must be excluded analytically.

## The stable label

The permutation representation k^r splits into constants and augmentation because r=-1 modp is invertible. A nonzero augmentation vector cannot be constant. Subtracting its image under a transposition with unequal coordinates gives a nonzero multiple of e_i-e_j; its conjugates span augmentation. This proves simplicity over k, not just over Fp.

The stable FI label is independently fixed without relying on ordinary Specht conventions. DD's symmetric-power tensor injective multiplicity formula applies to H=Sym^(r-1)(E_N) tensor E_N. Any simple admitting weight alpha=(r-1,1,0,...) has highest weight dominating alpha. Only(r) and alpha do. The alpha highest-weight space in L_N(alpha) has dimension1. The alpha space of L_N(r) also has dimension1: the highest weight line x_1^r lies in the simple socle of Sym^r(E_N), and its unipotent translate has nonzero coefficient r x_1^(r-1)x_2. The ambient weight space has dimension1. This does not assume that the whole stable-rank symmetric power is simple.

Thus H=I_N(r) plus I_N(alpha). Reciprocity at the maximal label identifies I_N(r)=Sym^r(E_N). Multiplication splits by intrinsic polarization delta/r, using Euler's homogeneous identity m delta=r id. Krull-Schmidt cancellation therefore identifies ker(m)=I_N(alpha). Its multilinear weight has r basis vectors, indexed by the distinguished last tensor factor, with permutation action and summation multiplication. Exactness of the stable Schur functor identifies its kernel with augmentation. There is no sign, conjugate-label or rank2-Schur-functor shortcut.

## The algebraic-group rank2 obstruction

The torus has distinct integer character weights on monomials v_i=x^(m-i)y^i. Over algebraically closed k it is diagonalizable and stable subspaces decompose into these lines. Over the infinite field, Vandermonde extraction of unipotent evaluations produces every formal coefficient operator. Restricting to GL2(Fp) would lose this information.

For m=2p-1, (1+t)^m=(1+t^p)(1+t)^(p-1) modulo p has every coefficient nonzero. Every monomial reaches x^m under y -> y+t x, with coefficient1. Translating x^m in the opposite direction then reaches every monomial. The symmetric power is simple.

For m=2p-3, the highest-monomial binomial support is J=[0,p-3] union[p,2p-3]. W on those lines is the injective image of E^(1) tensor Sym^(p-3)E; supports are disjoint. This proves invariance. Every nonzero W-submodule contains a monomial, hence x^m, hence every supported monomial; W is simple of highest weight(m,0), dimension2p-4.

The two missing lines p-2,p-1 give a simple quotient. The opposite root operators connect them with scalarp-1 in both directions. Its highest weight is(p-1,p-2), dimension2. An invariant complement must be the unique torus complement on those two missing lines. But translating v_(p-2) has coefficient x^m in W at t^(p-2). No complement exists. A nonsplit length2 extension of distinct simples has exactly the stated simple socle and head.

After determinant twist, nabla2(lambda) has socle label(2p-2,1) and top label(p,p-1). At p3 these two simple constituents both have dimension2 but their algebraic highest labels differ. No dimension-only inference is used. Among degree-r partitions only(r) strictly dominates lambda, and its rank2 costandard is simple with different label. DD reciprocity forces I2(lambda)=nabla2(lambda). Different head and socle labels exclude contravariant self-duality, hence projectivity.

## All permitted ranks

Suppose I_N(lambda) were projective for any N>=2. Established DD highest-weight/duality theory makes it an indecomposable tilting T_N(mu). Its highest weight dominates the socle label lambda. Therefore mu_1>=r-1, leaving only mu=(r) or lambda; both fit rank2. The actual labelled exact truncation theorem therefore sends the two sides to I2(lambda)=T2(mu). This would be an injective tilting, hence projective, contradicting the rank2 calculation. Arbitrary idempotent preservation of projectivity or heads is never assumed.

Membership in the constructed sufficient DD index family would already give a projective I_n; the all-rank failure excludes membership. No conditional completeness classification or equivalence of the two printed proposals is used.

## Boundaries and old components

p2 is outside the theorem: p-3 would be negative and the nonsplit pattern collapses. Rank1 is outside the original permitted ranks because lambda has two parts. r divisible by p would destroy the permutation splitting. Positive odd characteristic at q1 is essential; a char0 nontrivial-root specialization is not refuted. All modules are rational algebraic-group/polynomial modules, not just finite-group representations.

Actual OWR2009 printed945--946 defines stable FI and says "More strongly" for the index proposal. Its subsequent0.5 characteristic-zero qualification concerns a separate simple-Specht method. Actual DD12Jan2005 printed7--12 supplies reciprocity, symmetric powers, labelled truncation and projective-injective/tilting duality. Cox--Parker accepted printed3 confirms FI. Actual EL2104.05317v1 pp5--6 gives a classical analogue of the nonsplit sequence (n=1,i=p-3), by duality and determinant restoration, and the simple-row criterion for 2p-1. These are old ingredients, properly credited.

No mathematical gap remains identified. The finite programs support the local bookkeeping and small Schur calculation; universal odd-prime and all-rank statements follow from the written argument. Historical originality is a separate unresolved question.
