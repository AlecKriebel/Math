# Independent reconstruction, frozen before consulting prior correction

Timestamp: 2026-10-21T19:18:13.745937+00:00

## Exact target and dependency

The frozen author proof states ordinary, unnormalized section Schwarz genus g(Y/X)=8, where X is the complement of the cubic discriminant in CP^9 and Y chooses one of nine flexes. Its only lower-bound input is Chen–Wan arXiv:2306.17303v2, Theorems 1.2/4.1; its own geometric construction supplies the upper bound.

Chen–Wan pulls back Y/X along the Fermat orbit map M=PU(3)/K -> X, where K=<[A],[B]>=C3^2. The pullback is the regular nine-sheet cover PU(3)->M because K acts regularly on the flexes. Their Proposition 4.2 asserts cl*:H^7(BK;F3)->H^7(M;F3) is nonzero. The genus lower bound8 then follows from the standard classifying-map detector. This is the exact dependency, with no mismatch of the coefficient-space base.

## Independent exact contradiction to the stated detector

Let omega^3=1, A cycle the three standard coordinate vectors, B=diag(1,omega,omega^2). They lie in SU(3), satisfy BA=omega AB, and each has order3. The inverse image of K under SU(3)->PU(3) is

P={omega^c A^a B^b : a,b,c in F3},

with multiplication

(a,b,c)(a',b',c')=(a+a', b+b', c+c'+b a').

Thus P has order27, center and commutator C3, exponent3, and abelianization K. Since SU(3) is simply connected, pi1(M)=P. The cover classifying map induces P->K on fundamental groups. Consequently cl*:H^1(BK;F3)->H^1(M;F3) is an isomorphism.

Let u(a,b)=a and v(a,b)=b be the degree1 generators of H*(BK;F3)=Lambda(u,v) tensor F3[x,y], with x=beta u, y=beta v in degree2. On P, the cochain f(a,b,c)=c-ab obeys

(delta f)(g,h)=f(h)-f(gh)+f(g)=a b'=u(g)v(h).

Therefore inflation of uv is zero in H^2(BP;F3), and hence cl*(uv)=0 on M. This also follows by transgressing the central C3 extension class, but the cochain identity is a direct finite check.

Every degree7 class of BK is u p(x,y)+v q(x,y), for homogeneous cubic p,q. Multiplying it by either u or v yields a multiple of uv, so on M the pullback of every degree7 class pairs trivially with both generators of H^1(M;F3). As those span H1, and M is a connected closed orientable real8-manifold, Poincare duality over F3 forces

cl*:H^7(BK;F3)->H^7(M;F3) = 0.

This contradicts precisely Proposition 4.2(1), not the statement that genus8 might nevertheless be true. It is independent of Leary's ring presentation, possible typographic errors in that presentation, and spectral-sequence kernel assertions.

## Controls and limitations

The projective group is K of order9; the actual fundamental group is its nonabelian order27 lift P, not K. Replacing M by a nonexistent quotient with fundamental group K loses the central-extension relation and is not a valid repair. The pairing is on the compact quotient M, not on the noncompact coefficient space X. Coefficients are the constant trivial F3 system used by Proposition4.2; the argument makes no assertion about other local systems. The Fermat orbit pullback is legitimate; the detector of its claimed genus lower bound is what fails. A different nonzero degree7 detector with another coefficient module, another subspace of X, or a direct obstruction proof could still establish g(Y/X)>=8, but none is established here. Merely assuming such a detector transfers the central difficulty and is blocked.

No prior integrated, other-auditor, root, or correction findings were consulted before this reconstruction was saved.
