# Independent analytic proof — the full unrestricted category

Let k=F4, G=(k,+), N=F2 and Q=G/N. The category is the stated unframed Artinian W(k)-category, with identified residue field and coordinate conjugators reducing to the identity. In particular, coordinates may have nilpotent constant terms. Throughout, a basepoint over the equal-characteristic rings used below means the constant residual action obtained through their specified k-algebra structures. No global choice of basepoint over all mixed-characteristic rings is being assumed.

## A. A structural obstruction to every prorepresentable recipient

Suppose three actual deformation functors have restriction and induction maps D_G->D_N^Q and D_G->D_Q, with unique points over k. Assume two properties:

1. Restriction D_G(k[e]/e²)->D_N(k[e]/e²) has zero tangent kernel.
2. A nonzero v in D_Q(k[e]/e²) maps to the residue point under every natural transformation D_Q->h_R, for every prorepresentable Hom functor h_R.

For any proposed natural maps f:D_N^Q->h_R and g:D_Q->h_R, naturality along k->A=k[e]/e² sends the basepoint 0_N to the residue point. Property 2 gives the same image for v. Thus (0_N,v) belongs to the actual fiber product over A. It reduces to the image of the unique D_G(k)-point. The surjection A->k has kernel annihilated by the maximal ideal, so is small. Formal smoothness would produce w in D_G(A) with res(w)=0_N and ind(w)=v. Property 1 forces w=0_G, whose induction is 0_Q by naturality along k->A. This contradicts v!=0.

This argument uses neither tangent-linearity of f or g, a prescribed tangent dimension of R, nor an extension of f to D_N. It cannot be obtained by replacing one component with a versal hull: the target is the actual set-valued fiber product.

## B. The concrete action and its quotient

The fractional-linear substitutions rho(a)(t)=t/(1+at) compose additively. The coefficient of t² distinguishes a, so the action is faithful. Every nonidentity element has first ramification term at degree two, hence conductor one.

Set y=t²/(1+t). The leading terms of y^m and t y^m have distinct even and odd t-valuations. Successive leading-term subtraction, converging in the t-adic topology, gives a unique expansion A(y)+tB(y) for every formal series. This is also consistent with t²+yt+y=0. Since rho(1)(t)=t+y and y is fixed, invariance is equivalent to yB(y)=0. The domain k[[y]] has no zero divisors, so the fixed ring is k[[y]]. The Laurent-field argument similarly gives k((t))^N=k((y)).

For u²+u+1=0, u(u+1)=1. Direct substitution gives

    rho(u)(y) = t² / [(1+ut)(1+(u+1)t)]
               = t² / (1+t+t²) = y/(1+y).

The quotient action is therefore the known weakly ramified involution sigma(y)=y/(1+y). These computations do not assume any universal deformation ring for G.

## C. A nonzero tangent killed by every natural map to h_R

Use B=k[e]/e³, A=k[e]/e², and j:B->B with j(e)=e+e² and j fixing k. All structures are W(k)-linear through the reduction W(k)->k. The matrix

    M_e = [[1,e],[1,1]]

defines sigma_e(y)=(y+e)/(1+y). Its constant coefficient is nilpotent and its linear coefficient is a unit, exactly the automorphism criterion in the actual BC primary. Its square is (1+e)I, so it defines an involution. Let x be its actual deformation class over B, and v its reduction to A.

The identity-reducing coordinate represented by C=[[1+e,e],[0,1]] is invertible, and exact multiplication modulo e³ gives

    M_(e+e²) C = (1+e) C M_e
                = [[1+e,e²],[1+e,1+e]].

The scalar is a unit, so the two fractional-linear transformations are conjugate. Whether ring-substitution order is written as a right action or ordinary function composition only reverses the conjugating direction; equivalence holds. Hence D_Q(j)(x)=x.

For arbitrary eta:D_Q->h_R, put psi=eta_B(x):R->B. Naturality makes j psi=psi, so psi(R) lies in B^j. In the unique expression c0+c1e+c2e², the automorphism j changes c2 to c2+c1. Thus B^j=k+k e². Reducing this subring to A lands in the coefficient field k. Therefore eta_A(v) is the residue map R->k followed by k->A. This is the basepoint. The argument is valid for mixed-characteristic R and every possible tangent dimension because it is an equality of actual local W(k)-algebra maps, not a calculation with an assumed linear tangent transformation.

To prove v!=0, allow every first-order coordinate change y+e h(y), with arbitrary h in k[[y]], including arbitrary h(0). Its first-order conjugacy perturbation of sigma is h(sigma(y))-sigma'(y)h(y), up to the choice of conjugation sign. Its constant is h(0)-h(0)=0. The perturbation in sigma_e is e/(1+y), whose coefficient of e has constant 1. No such coordinate trivializes v. This is a universal formal-series argument, not just a search over matrices.

The actual BC Proposition 4.1 contains the same cubic conjugacy; its Proposition 6.1 also gives the alternate known route through the injection k[e]/e²->k[w]/w³, e->w², under which v and 0 become equal. Every Hom functor h_R preserves injections of target rings, so naturality immediately gives the same all-recipient collapse. The collapse phenomenon and involution pathology are credited antecedents, not new claims of this review or of the current note.

## D. The exact invariant derivation module

There are no extra discontinuous algebraic derivations to account for in this example. Perfectness and characteristic two give h=a(t)²+t b(t)² for every h in k[[t]]. Any algebraic k-derivation satisfies d(h)=d(t)b(t)²=d(t)h'(t) by the Leibniz rule, without assuming continuity. Conversely each coefficient times partial_t is a continuous derivation. Hence Theta=k[[t]]partial_t is the complete module needed by the first-order calculation.

The field equation X²+yX+y is separable because its derivative is y!=0 in k((y)). Any derivation b(y)partial_y therefore extends uniquely to k((t)). Its coefficient is

    a(t) = b(y)/y'(t) = b(y)(1+t)²/t²,
    y'(t) = t²/(1+t)².

The extension preserves k[[t]] iff b=0 or 2 ord_y(b)-2>=0. Equivalently b belongs to y k[[y]]. Its uniqueness makes it N-invariant. Conversely every invariant derivation restricts to the fixed ring and is recovered this way. Thus, under restriction,

    Theta^N = M = y k[[y]]partial_y.

The coefficient operator induced by the quotient involution is

    T f(y) = (1+y)² f(y/(1+y)).

This follows directly by conjugating a coefficient derivation and using sigma'(sigma(y))=(1+y)². Every group element is an involution, so using inverse conjugation gives the same operator.

## E. A distinct complete-module normal form

Put z=y²/(1+y) and K=k[[z]]. Repeating the exact leading-term basis argument gives k[[y]]=K direct_sum yK, with z fixed by sigma. Multiplication by the nonzero y then gives the **complete** free K-module decomposition

    M = yK direct_sum y²K.

This basis is valid for arbitrary convergent formal series, not just finite polynomials. Since T is K-linear,

    T(y)=y+y²,       T(y²)=y².

In the ordered basis (y,y²), T has matrix [[1,0],[1,1]], and T-1 has matrix [[0,0],[1,0]]. For f=y A(z)+y²B(z),

    (T-1)f = y² A(z).

Therefore ker(T-1)=y²K=im(T-1). In characteristic two, 1+T=T-1, and the standard cyclic-group cocycle formula gives H1(Q,M)=0. More concretely, every invariant f=y²B(z) is the coboundary of yB(z). This supplies an explicit formal-series preimage, closing the arbitrary-series question without relying on an unproved limit of finite calculations.

As an additional consistency calculation, in the basis (1,y) of Theta^sharp=k[[y]] the relation y²=z(1+y) gives

    T = [[1+z,z],[z,1+z]],
    T-1 = z [[1,1],[1,1]].

Its H1 is generated by the class of 1+y modulo z, as expected for the involution tangent. Indeed the first-order perturbation v corresponds to coefficient 1+y. This is an independent analytic consistency check; the contradiction needs only its already proved nontriviality, not a classification of every Q-deformation.

The quotient Theta^sharp/M is k given by constant term. T preserves it and acts trivially. Thus H1(Q,Theta^sharp/Theta^N)=H1(C2,k)=k, agreeing with the prescribed one-dimensional tangent. Its dimension does not rescue the factorization because the recipient-collapse argument applies in every dimension.

## F. Injectivity of restriction without a stronger imported gap

Writing a first-order lifted group action as (id+e c(g))rho(g) gives the cocycle equation. Identity-reducing coordinate conjugation changes c by a coboundary. The actual primary Proposition 2.4 identifies restriction with cohomological restriction. The argument can also be seen directly: subtract a coboundary so a cocycle with trivial restricted class is identically zero on N. Commutativity of G and the cocycle equation then force its value at u to be N-invariant. The order-two relation forces (1+T)c(u)=0. By the explicit preimage in section E, c(u)=(T-1)m for m in Theta^N. Subtract this coboundary; it leaves the zero N-values unchanged and kills u. Since N and u generate G, the whole cocycle vanishes. Thus restriction has zero tangent kernel, as required in A.

Restriction lands in the actual fixed subfunctor by the primary construction. Its inclusion into D_N is literally an inclusion of sets at A, so no separate identification of the tangent to a hull or a derived fixed object is needed.

## G. Finite exact diagnostics and their proper limits

The owned standard-library controls check seven complete rational identities by polynomial cross multiplication over GF4, all 16 additive-action relations, all 64 elements and 8,192 addition/multiplication compatibility tests for j on the cubic ring, its exact 16-element fixed subring and four-element reductions, the actual projective conjugacy, and the full set of 48 possible unit scalars for a deliberately wrong conjugator. Wrong weight, missing translation, and a wrong fixed-ring operation cause the owned verifier to fail under both normal Python and -O. No provided programme is executed.

A further diagnostic deliberately tests why finite jets cannot replace E. For M_L=y k[y]/(y^L), I compute the exact induced T and norm matrices over GF4 for every L=2,...,32. Its H1 dimension is 1 when L is even and 0 when L is odd. These nonzero classes at even cutoffs are boundary artifacts, not counterexamples to H1(Q,M)=0. For example the top odd monomial y^(L-1) becomes invariant modulo y^L although its first nonzero norm term occurs at degree L and is suppressed. The complete-module free-basis proof retains that term. Consequently neither a few zero truncated H1 values nor the nonzero truncated values prove a statement about the complete module without further reasoning. The packet explicitly uses the full-series module proof.

## H. Full scope and disposition

Sections B–F prove the two properties in A for exactly the manuscript's action, subgroup, quotient, and unframed category. Section A therefore proves the original all-prorepresentable-recipient impossibility. No tangent-dimension assumption, component prorepresentability, global mixed-characteristic basepoint, extension of f off the fixed functor, or Klein-four universal deformation ring is used.

The actual questions in OWR2008, the 2009 thesis, and arXiv1112.0352v1 do not assume the two component functors prorepresentable. Their neighboring conditional obstruction-space theorems expressly do. Both N and Q in this example are the exceptional involution case, so the extra hypotheses of that variant fail. The counterexample does not answer that conditional variant, and it changes if the category excludes nilpotent constant terms. These are exact original boundaries, not repairs or narrowed substitutes.

No substantive mathematical gap is identified in the original theorem. Its known action, conjugacy, nonprorepresentability pathology, and injection-collapse antecedent remain credited. A bounded reading of these four cited bodies cannot certify the absence of all prior negative factorization arguments or the date until which the question was open. No such exhaustive novelty assertion is made here.
