# Authored proofs and hypothesis controls

All varieties and fields below have characteristic zero, and the constant field is C. Equalities of rational differential forms are checked on a dense open set and hence hold as rational forms on the whole irreducible variety. Clearing denominators and saturating a rational rank-one conormal distribution gives its associated singular foliation; no regularity at its polar divisor is asserted.

## 1. A transverse infinitesimal symmetry

Let omega be a nonzero rational 1-form on a smooth irreducible variety, with omega wedge d omega=0. Suppose v is a rational vector field and L_v omega=b omega for a rational function b. Assume a=omega(v) is not identically zero. Then beta=omega/a is closed.

Proof. Lie differentiation shows L_v beta is a rational multiple of beta. Since beta(v)=1, evaluation on v gives (L_v beta)(v)=v(1)-beta([v,v])=0. The multiple is zero. Cartan's identity gives i_v d beta=L_v beta-d(beta(v))=0. Integrability is unchanged by scaling, so beta wedge d beta=0. Contracting this identity by v yields d beta-beta wedge i_v d beta=0. Therefore d beta=0. This is an algebraic proof of the standard infinitesimal-symmetry mechanism (compare LBPRT Proposition 2.2); completeness of v is unnecessary under the displayed rational Lie-derivative hypothesis.

If a connected algebraic group acts on X preserving F and has an orbit direction not tangent to F, differentiating its action supplies such a v. This conditional statement does not assert that an infinite cyclic birational group has such an algebraic closure.

An infinite ambient action can be entirely leafwise: on X=P1_z x Z with F the pullback of a foliation G on Z, (z,p)->(z+1,p) has infinite order and fixes every general F-leaf. The same construction with any G shows why its ambient infinitude imposes no new condition on G.

## 2. First integrals and finite extensions

If F has a nonconstant rational first integral R and has codimension one, then dR is a nonzero closed rational defining form. Indeed dR annihilates the rank dim(X)-1 tangent space of F at a general point, and in characteristic zero dR is nonzero. Their generic kernels therefore coincide. This settles that special case without any hypothesis on f.

The following elementary lemma is useful for testing the much stronger conclusion of algebraic integrability after a cover.

**Constants lemma.** Let K be a characteristic-zero differential field with derivation D and constant field C, algebraically closed. Let L/K be finite. Extend D uniquely to L. If h in L satisfies D(h)=0, then h belongs to C.

Proof. Let p(T)=T^m+a_(m-1)T^(m-1)+...+a_0 be the monic minimal polynomial of h over K. Differentiating p(h)=0 gives sum_(j<m) D(a_j)h^j=0. Minimality forces every D(a_j)=0. Thus p has coefficients in C. Since C is algebraically closed, h belongs to C. The unique extension of D follows by differentiating the minimal polynomial of any algebraic element; its derivative at that element is nonzero by separability.

## 3. An irrational logarithmic model

Put t=(sqrt(5)-1)/2 and lambda=2+t=(3+sqrt(5))/2. Then t^2+t=1 and lambda>1. On Y=P1_x x P1_y use the rational form

beta=dx/x+t dy/y.

It is nonzero and closed. Its foliation is regular on the torus T=(C*)^2 but is considered as a possibly singular foliation on Y. Define

g(x,y)=(x^2 y,xy).

Its inverse on T is (u,v)->(u/v,v^2/u). Thus g is birational on Y. Direct differentiation gives

g*beta=(2+t)dx/x+(1+t)dy/y=lambda beta,

using lambda t=1+t. In particular g preserves the foliation.

### No rational first integral

The derivation D=t x partial_x-y partial_y spans its tangent line on T. We prove that the constants of D on C(x,y) are exactly C. Suppose R=P/Q with Laurent polynomials P,Q is D-constant. Choose (x0,y0) in T with Q(x0,y0) nonzero. Along the local integral curve

x=x0 exp(t z), y=y0 exp(-z),

R is constant, say c. Hence (P-cQ)(x0 exp(t z),y0 exp(-z))=0 near z=0. Expanding the Laurent polynomial yields a finite linear combination of exponentials exp((tm-n)z), for integer pairs (m,n). Distinct pairs give distinct exponents because t is irrational. Such exponentials are linearly independent: their first N derivatives at zero form a Vandermonde matrix with nonzero determinant. Every coefficient of P-cQ is therefore zero. Consequently R=c.

The constants lemma then proves that no finite algebraic extension of C(x,y) contains a nonconstant first integral. A generically finite dominant cover gives just such an extension of function fields, so passing to any such cover does not create a rational first integral of the pulled-back foliation.

### Infinite transverse action

On the universal covering exp:C^2->T, write x=exp(u), y=exp(v). The lifted leaves are the affine lines ell(u,v)=u+t v=constant. Two points of T lie on the same leaf exactly when their ell-values differ by an element of the countable subgroup

Lambda=2 pi i (Z+t Z).

The map g acts on ell by multiplication by lambda. If g^k fixed general leaves for some k>0, then (lambda^k-1)ell would lie in Lambda for all points of a nonempty local transverse open set. A nonconstant affine function cannot map a complex open set into a countable set. Since lambda^k-1 is nonzero, this is impossible. The invariant coordinate boundary of the torus does not merge its leaves: a regular leaf cannot cross an invariant divisor, and singular points are excluded from leaves. Hence this verifies the source's transverse-infinitude condition on the projective foliation.

The powers of the exponent matrix M=[[2,1],[1,1]] are unbounded. This example illustrates discrete birational dynamics and supplies no justification for replacing that cyclic group by a finite-dimensional connected group action. The positive conclusion holds here directly because beta is closed.

## 4. A cover-essential example on a smooth projective surface

Let sigma(x,y)=(1/x,1/y). Then sigma*beta=-beta, and sigma commutes with g. Introduce the birational coordinates

a=(x+1)/(x-1), b=(y+1)/(y-1).

Then sigma(a,b)=(-a,-b). Set s=a^2 and r=b/a. The invariant field is exactly C(s,r): C(a,b)=C(a,r), a satisfies a^2=s, and sigma is the nontrivial automorphism of this degree-two extension. In particular the quotient has the explicit smooth projective birational model X=P1_s x P1_r. There is a generically finite dominant degree-two rational map pi:Y -->> X, (a,b)->(a^2,b/a).

In a,b coordinates,

beta=2 da/(1-a^2)+2t db/(1-b^2).

The product a beta is sigma-invariant and descends to the rational form

alpha=[1/(1-s)+t r/(1-s r^2)] ds+[2t s/(1-s r^2)] dr

on X. Its pullback is a beta. Thus alpha defines a singular codimension-one foliation F on the smooth projective surface X, and pi*F is the foliation of beta. Explicitly

d alpha=t/(1-s r^2) ds wedge dr=(ds/(2s)) wedge alpha.

Adjoining a=sqrt(s) gives d(alpha/a)=0. This is a ramified degree-two construction; it is not a proposed etale-cover argument.

### Birational symmetry downstairs

Commutation of g with sigma shows that g restricts to an automorphism of the invariant function field C(s,r); hence it induces a birational map f of X. For completeness its formulas are

S=s(rs+r+2)^2/(2rs+s+1)^2,

R=(rs+1)(2rs+s+1)/[s(r+1)(rs+r+2)].

The diagram pi composed with g=f composed with pi follows either from the invariant-field construction or direct substitution. Birationality follows from the same commutation for g inverse; it is not inferred just from the displayed rational formulas. Furthermore f*F=F, and direct pullback gives

f*alpha=lambda (rs+r+2)/(2rs+s+1) alpha.

### Transverse infinitude survives the quotient

First work on the normal projective quotient Q=Y/<sigma>. Over the torus away from the finite fixed set of sigma, the quotient morphism is an unramified double cover. A downstairs leaf lifts into the union of at most the two leaves upstairs with labels ell and -ell modulo Lambda. This follows by continuing local leaf lifts along paths: their possible endpoints differ only by sigma. A general leaf avoids the finitely many fixed-point leaves, and the images of the torus boundary are invariant, so no extra leaf identifications arise there.

The invariant-field model X is birational to Q. Generic leaf equivalence is unchanged by this birational modification of surfaces. Indeed a common resolution factors the birational correspondence into modifications over finitely many points. Away from those points it is an isomorphism. Removing isolated points from a connected complex regular leaf does not disconnect it; exceptional components and leaves contracted to the finitely many centers do not join distinct general leaves, since the centers where the foliation is singular are excluded from leaves. Consequently a map fixing general leaves on X would fix general leaves on Q, and the preceding double-cover test applies. This argument concerns general leaves and does not assert a global isomorphism of the two leaf spaces at exceptional leaves.

If f^k fixed general leaves, the upstairs transverse coordinate on a local disk would satisfy either

(lambda^k-1)ell in Lambda or (lambda^k+1)ell in Lambda.

For fixed k the set of possible ell is countable, since lambda^k is neither 1 nor -1. It cannot contain a nonempty transverse open set. Thus no positive iterate is leaf-fixing. One can also avoid every such exceptional value at once because their union over all k remains countable.

### No closed rational defining form downstairs

Suppose theta were a nonzero closed rational 1-form on X defining F. Its pullback has the form h beta for h in C(x,y)*. Closedness gives dh wedge beta=0, equivalently D(h)=0. Section 3 implies h=c in C*. But pi*theta is sigma-invariant, whereas sigma*(c beta)=-c beta. This is impossible in characteristic zero. Therefore F is not transversely additive on X, despite being virtually transversely additive.

The same statement holds on every birational model of X, since the existence of a closed rational defining form is a property of the function field and its conormal line.

### No rational first integral after any finite cover downstairs

Suppose a generically finite cover X' -->> X had a nonconstant rational first integral h. Form a common finite extension of C(X') and C(Y) over C(X). The pullback of h remains nonconstant and is constant along the extension of D. The constants lemma and Section 3 force h in C, a contradiction.

This example satisfies the conjecture and disproves only the stronger replacement conclusions “additive without a cover” and “rationally integrable after a finite cover.” It is not a counterexample to the original problem and carries no novelty claim.

## 5. What the covariance equation actually says

Let K=C(X), let omega be a nonzero integrable rational 1-form, and suppose f*omega=A omega with A in K*. Integrability implies one can choose a rational 1-form eta with d omega=eta wedge omega: choose v with omega(v)=1 and use eta=-i_v d omega. Differentiating f*omega=A omega gives precisely

(f*eta-eta-dA/A) wedge omega=0.

Also d eta wedge omega=0, by applying d to d omega=eta wedge omega. Neither identity states that d eta=0. For example, for omega=dx on affine three-space, eta=y dx satisfies d omega=eta wedge omega but d eta=dy wedge dx is nonzero. Changing eta by a multiple of omega leaves its defining equation unchanged.

If a closed eta is already available, then eta_f=f*eta-dA/A is another closed rational form satisfying d omega=eta_f wedge omega. If eta_f-eta is nonzero, it is a closed rational form proportional to omega and hence defines F. If eta_f=eta, that argument produces zero and gives no defining form. This does not show that eta has finite monodromy or that an integrating factor is algebraic.

An algebraic integrating factor h in a finite extension must satisfy

(dh/h+eta) wedge omega=0,

because d(h omega)=0. The present approach does not produce such h from infinite transverse action. This is the explicit differential-algebraic gap, not a computationally tested implication.
