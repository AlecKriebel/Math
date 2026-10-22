# Turn 2: test the stronger gauge-equivalence conjecture

Timestamp: 2026-10-03T09:31:00Z. Outcome: stronger conjecture refuted; original target unresolved.
Completion estimate toward the general converse: 15% (subjective).

## Attempted negative route and exact control

Could the two sets of 6j-symbols be identified by a relabeling and changes of bases in their trivalent fusion spaces? No: the familiar Vec_G/Rep(G) Morita pair already has different fusion ranks when G is nonabelian. We work out the mechanism rather than treating “equivalent” as an unspecified word.

Let C=Vec_G with trivial associator, and let M=Vec. Make M a C-module category by letting every degree-g simple delta_g act by the identity functor, with trivial module associativity. A finite-dimensional exact endofunctor of Vec is F_W(V)=W tensor V. A C-module structure on F_W is precisely a compatible family of invertible maps rho(g) of W. The module-functor pentagon says

    rho(gh)=rho(g)rho(h),  rho(1)=1.

Module natural transformations are intertwiners. Composition of module endofunctors corresponds to tensor product of representations (an opposite convention makes no difference here because Rep(G) is symmetric). Hence

    Fun_C(M,M) is tensor equivalent to Rep(G).

M is indecomposable because Vec has just one simple object. It therefore supplies the usual categorical Morita equivalence. With the canonical unitary structures, the known Morita-invariance/center theorem gives isomorphic TV TQFTs for Vec_G and Rep(G). This sufficient direction is not a new theorem claimed here.

## Explicit G=S_3 certificate

Vec_(S_3) has six invertible simples and global dimension 6. Rep(S_3) has three simples 1, sgn, V, with dimensions 1,1,2, and rules

    sgn tensor sgn = 1,
    sgn tensor V = V,
    V tensor V = 1 direct_sum sgn direct_sum V.

These rules follow by multiplying the character rows on the conjugacy classes (1), (12), (123):

    class sizes:  1, 3, 2
    1:            1, 1, 1
    sgn:          1,-1, 1
    V:            2, 0,-1.

The weighted character inner products give the displayed decomposition; 1^2+1^2+2^2=6 checks the common global dimension. Changing trivalent bases or relabeling simple objects cannot change their number from six to three. Thus no gauge-equivalence statement about the original F-symbol arrays can follow from ordinary TQFT isomorphism.

## Why this does not solve the source question

The two categories ARE Morita equivalent, witnessed explicitly above. They are therefore a negative control for the stronger gauge claim and a positive control for the Sato/Morita-type relation actually suggested in the source. Calling this a counterexample to Kawahigashi's remark would be a target substitution.

Turn 1 recovered fusion rules of the CENTERS, so there is no contradiction with the different ranks of the INPUT categories here. In both cases the center is the quantum-double category of S_3.

This route is closed as a general counterexample search unless a pair with isomorphic ordinary TQFTs but inequivalent centers is produced. Reusing ordinary Morita pairs cannot accomplish that.
