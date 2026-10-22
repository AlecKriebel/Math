# Independent check of the constant-F3 degree-seven detector

Date: 2026-10-21 UTC. This is an audit derivation, not a new genus theorem or a claim of conventional human review. The mechanism was reconstructed from the primary sources before reading the specifically identified earlier integrated audit. Afterward it was found to agree with that earlier correction; no priority claim is made.

## Exact statement

Let A be the cyclic coordinate permutation and B=diag(1,w,w^2), with w=exp(2 pi i/3). Their images in PU(3) generate K=C3 x C3. Put M=PU(3)/K, and let c:M -> BK classify the principal K-cover PU(3) -> M. Then

    c*:H^7(BK;F3) -> H^7(M;F3)

is identically zero. This contradicts the specific nonzero-map assertion in Proposition 4.2(1) of the inspected [Chen-Wan arXiv v2, pp. 5-7](https://arxiv.org/pdf/2306.17303v2). It does not assert that the genus is less than eight.

## Fundamental group and cup product

Both A and B have determinant one and order three. In SU(3) the group

    H={w^t A^a B^b : a,b,t in F3}

has order 27. The relation BA=w AB gives the normal-form multiplication law

    (a,b,t)(d,e,s)=(a+d,b+e,t+s+bd).

Its center and commutator subgroup are both {(0,0,t)}; its abelianization is K. The exact monomial-matrix program in this folder checks the 27 matrices, all 729 products against this law, and the 729 cochain identities below. It uses integer arithmetic modulo three. Those finite checks corroborate these algebraic inputs; the topological argument remains a mathematical proof.

Since SU(3) is simply connected, SU(3) -> SU(3)/H=M is the universal cover. Thus pi_1(M)=H. The K-cover in question is obtained by quotienting this universal cover by the central subgroup C3. Consequently c factors, up to homotopy, through the classifying map M -> BH and the quotient map BH -> BK. In particular,

    c*:H^1(BK;F3) -> H^1(M;F3)

is an isomorphism, as H_ab=K.

Let y(a,b,t)=a and y'(a,b,t)=b denote the quotient's coordinate one-cocycles. For the normalized group one-cochain f(a,b,t)=t-ab, direct substitution gives

    delta f(g,h)=f(h)-f(gh)+f(g)=a(g)b(h)=(y cup y')(g,h).

Therefore the pullback of yy' to BH, and hence to M, is zero. This explicit identity avoids any convention dependence in identifying the central-extension class.

## Duality

The standard cohomology of the elementary abelian group is

    H*(BK;F3)=exterior(y,y') tensor F3[x,x'],
    |y|=|y'|=1, |x|=|x'|=2.

Every degree-seven class is of the form yP(x,x')+y'Q(x,x'), with P and Q homogeneous of polynomial degree three. Its product with either degree-one generator is zero or a multiple of yy'. Hence its pullback to M pairs to zero with all of H^1(M;F3).

The quotient M is a closed connected orientable manifold of real dimension eight. Indeed, it is the quotient of the compact connected eight-dimensional Lie group SU(3) by a free finite right action, and each right translation is isotopic to the identity and preserves orientation. Poincare duality over F3 makes the pairing

    H^7(M;F3) x H^1(M;F3) -> H^8(M;F3)=F3

nondegenerate. It follows that c*(u)=0 for every u in H^7(BK;F3). In fact dim_F3 H^7(M;F3)=2, by the same duality and the H^1 calculation. QED.

## Scope of the obstruction to repair

Changing the degree-seven representative cannot repair this constant-coefficient route. Correcting the printed x/x-prime inconsistency in the preprint's quoted Leary relation cannot change the argument above, which does not use that relation or a Chern-ideal description of the edge kernel. Information about universal Chern transgressions alone does not justify that complete kernel description.

A lower bound using nontrivial local coefficients, a different test space, or a different mechanism remains logically possible. Merely asserting such a detector leaves the central lower-bound proof unsupported. No statement is made about the proof in the uninspected 2025 journal version, about genus <8, or about failure of the published theorem.
