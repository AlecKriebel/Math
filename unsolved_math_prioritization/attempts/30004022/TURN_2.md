# Turn 2: rigidity of the imaginary-axis scalar-subordination ansatz

**Disposition: a second partial obstruction; the original broader representation problem is unresolved.** Turn 1 ruled out retaining the fixed positive arcsine factor. This turn examines a different mechanism: retaining the symmetric scalar mapping class and inserting the original nonsymmetric input Cauchy transforms into the displayed scalar equations. No literature-priority claim is made.

## 1. A precise analytic question

For a probability measure mu on R use the Cauchy transform

    G_mu(z) = integral (z-x)^(-1) dmu(x),   z in C minus R.

Let eta be a symmetric probability measure. Suppose an analytic function N maps the upper half-plane to the lower half-plane, takes the positive imaginary axis into the negative imaginary axis, and satisfies

    N(iy)/(-iy) -> a > 0 as y -> infinity.

Assume the scalar equation

    N(z) G_mu(N(z)) = (1 + z G_eta(z))/2       (1)

holds for every z in the upper half-plane. These are the relevant mapping and asymptotic features of either source subordination function, expressed without assigning a value to the source's normalization constants.

**Proposition. Under these hypotheses, mu must be symmetric about zero.** This statement has no support or moment restriction. Thus an unchanged continuation of the symmetric imaginary-axis mapping class with the original input Cauchy transforms cannot handle genuinely nonsymmetric laws. Applied to both equations, it forces both input laws to be even.

## 2. Proof for arbitrary probability measures

Write N(iy)=-i s(y), where s(y)>0. The function s is continuous, and s(y)/y tends to a>0. In particular it is unbounded. Since eta is symmetric,

    iy G_eta(iy) = integral y^2/(y^2+x^2) deta(x)

is real. All integrands are bounded; no first-moment assumption is needed. Equation (1) therefore says that (-is(y))G_mu(-is(y)) is real, or equivalently that G_mu(-is(y)) is purely imaginary. Conjugation gives the same property for G_mu(is(y)).

The continuous image of an interval is an interval. Because s is unbounded, its image on any sufficiently long tail contains a nonempty real interval in (0,infinity), indeed a ray above any chosen starting value. Hence G_mu(is) is purely imaginary for all s in some nonempty interval.

Let mu_ref be the reflected measure, mu_ref(E)=mu(-E). For s>0,

    G_mu_ref(is) = -G_mu(-is) = -conjugate(G_mu(is)).

Thus G_mu(is)=G_mu_ref(is) on that interval. Both Cauchy transforms are holomorphic on the upper half-plane. Their difference has zeros with an accumulation point inside that domain, so the identity theorem makes them identical there. Uniqueness of the Cauchy transform of a finite Borel measure gives mu=mu_ref. This proves the proposition.

Only the imaginary-axis invariance, nonconstant range and the real target along that axis were essential. Finite moments, Taylor expansions at infinity and determinate moment sequences were not used. The positive asymptotic slope supplies the nonconstant range and excludes degenerate constant functions.

## 3. Explicit centered two-point obstruction

The preceding argument could be misread as only a failure to subtract the input mean. The following exact example rules that out. Let X=P-p with P a projection of trace p in (0,1), p!=1/2. Its law is

    mu_p = (1-p) delta_(-p) + p delta_(1-p).

It has mean zero and variance t=p(1-p)>0. Direct evaluation gives, for every s>0,

    Im[(-is)G_mu_p(-is)]
       = s t (2p-1) / ((s^2+p^2)(s^2+(1-p)^2)).     (2)

The denominator is strictly positive and the numerator is nonzero. Thus no value N(iy) on the negative imaginary axis can satisfy (1) for this input and any symmetric eta, even at one y>0. This is stronger for this family than the general identity-theorem argument.

Taking eta as the law of i(XU-UX), with U a free centered self-adjoint unitary, is legitimate: the commutator equals i(PU-UP), and conjugation by U changes its sign, so its law is symmetric. The same centered family therefore supplies both Turn 1's multiplicative obstruction and the present scalar imaginary-axis obstruction. Centering does not alter a commutator, and it does not repair this failure.

For p=1/2, the two-point law is even and (2) vanishes, as it should. The deterministic limits p=0 and p=1 also make (2) zero; their variances vanish and they fall outside the positive-slope transform normalization assumed above. Replacing p by 1-p reverses the sign in (2), matching reflection. None of these boundary observations asserts existence of a full source subordination pair by itself.

## 4. What is and is not excluded

The source's symmetric equations involve two functions in the even Nevanlinna mapping class, together with the original even input Cauchy transforms. This proof rules out keeping those same restrictions and equations for nonsymmetric original inputs. It does not rule out general Nevanlinna functions that leave the imaginary axis, a larger matrix-valued system, changed scalar equations, or replacement input laws justified by a separate positive construction. The source already handles a specific symmetric free-square-root replacement subclass; that restricted positive construction is not extended by the present argument.

In particular, the existence of older general functional-equation systems is not contradicted: they need not obey the stronger imaginary-axis constraints tested here. The substantive conclusion is a necessary change of representation mechanism, not a solution of the request for a suitable new mechanism.

## 5. Route update

Two tempting universal continuations are now blocked by proofs: fixed arcsine positive factorization, and the unchanged symmetric scalar mapping class using original Cauchy transforms. A next route must genuinely change the auxiliary representation rather than repackage either assumption.

`verify_turn2.py` checks the exact two-point transform identity, mean and variance, strict signs, reflection and boundary cases using rational arithmetic and symbolic polynomials. These are controls on the explicit family; the arbitrary-measure analytic rigidity is proved above, not inferred from them.

Estimated completion toward the full source target: 15%, low confidence. Two of five genuine author turns used; three remain. Independent review is pending.
