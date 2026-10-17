# A rigorous dual-to-tight bridge using complex perturbations

Date: 2026-10-14 UTC. This is an authored proof, not a claim that the lemma or its application is new.

## Result and exact hypotheses

Let H be a complex Hilbert space and let U=(U_i)_(i in I) be a countable family of complex-linear unitary operators, including U_0=I. For a vector x whose orbit (U_i x) is a frame for all H, let F_x be its ordinary positive invertible frame operator. Define:

- P(x): F_x^(-1/2) U_i x = U_i F_x^(-1/2) x for every i.
- Q(x): F_x^(-1) U_i x = U_i F_x^(-1) x for every i.

The following implication holds:

    [P(x) for every complete frame vector x of U]
       implies
    [Q(x) for every complete frame vector x of U].

Consequently, the existence of a canonical-dual counterexample implies the existence of a canonical-tight counterexample for this SAME unitary system, SAME Hilbert space, SAME generator count, and SAME indexing. This is an existence implication over a family of generators. It is NOT the pointwise claim Q(x) fails => P(x) fails for that same x.

The complex scalar hypothesis is used in the perturbations below. No conclusion for a class restricted to real-valued generators follows from this lemma alone. No group-closure or multiplicativity hypothesis on U is needed.

## Proof by explicit perturbations

Fix a frame vector x, with atoms x_i=U_i x and frame operator F. Assume P(x); otherwise x itself is already a canonical-tight counterexample. Put

    y=F^(-1/2)x,       y_i=F^(-1/2)x_i=U_i y,
    A=F^(1/2).

Then (y_i) is a Parseval frame and x_i=A y_i. For each real t define the two single generators

    z_t^+=x+i t y,     z_t^-=x-i t y.

Their indexed U-orbits satisfy

    U_i z_t^± = (A±i t I)y_i.

Because (y_i) is Parseval, the frame operator of each orbit is exactly

    F_t=(A±i t I)(A∓i t I)=F+t²I.

In particular, both are complete frames for every t, with frame bounds a+t² and b+t² whenever aI≤F≤bI and a>0. This step does not require commutation of A with any U_i.

Suppose the canonical tightenings of both z_t^+ and z_t^- preserve the given U-indexing. With B_t=(F+t²I)^(-1/2), their identities are

    B_t(x_i+i t y_i)=U_i B_t(x+i t y),
    B_t(x_i-i t y_i)=U_i B_t(x-i t y).

Subtracting and dividing by 2it, for t≠0, gives

    B_t y_i = U_i B_t y.                                      (1)

If P holds universally, (1) holds for every nonzero t. Since F≥aI>0, continuous functional calculus gives convergence in operator norm

    (F+t²I)^(-1/2) -> F^(-1/2)       as t -> 0.

Taking the limit in (1) yields

    F^(-1)x_i=F^(-1/2)y_i=U_i F^(-1/2)y=U_i F^(-1)x.

This is Q(x). The argument applies to every frame vector x, proving the implication.

The proof only needs P(z_t^+) and P(z_t^-) along one sequence of nonzero t tending to zero, rather than at every parameter.

## Quantitative version and a concrete counterexample family

Suppose a dual defect is known at an index i:

    delta = ||F^(-1)x_i-U_i F^(-1)x|| > 0.

If P(x) fails, there is nothing further to construct. If P(x) holds, retain the definitions above and put

    d_t=B_t y_i-U_i B_t y,
    E_t^±=B_t U_i z_t^±-U_i B_t z_t^±.

Thus d_0 is the displayed dual defect vector and

    E_t^+-E_t^-=2it d_t.                                    (2)

For F≥aI, scalar calculus gives

    ||B_t-F^(-1/2)|| ≤ t²/(2a^(3/2)).

Since ||y_i||=||y||, it follows that

    ||d_t-d_0|| ≤ t² ||y||/a^(3/2).

Choose any nonzero t with

    t² ||y||/a^(3/2) ≤ delta/2.

Then ||d_t||≥delta/2, and (2) implies

    max(||E_t^+||,||E_t^-||) ≥ |t| delta/2 > 0.

At least one of z_t^+, z_t^- is therefore a canonical-tight counterexample, with the explicit frame bounds a+t²,b+t². In particular, if x has dual failure but its own tightening preserves structure, canonical-tight failure occurs arbitrarily close to x among these two complex directions. The sign is not selected by this argument; the finite candidate pair and lower bound are rigorous.

## Application to classical dyadic wavelets

Take H=L²(R;C),

    Df(s)=sqrt(2)f(2s),     T_k f(s)=f(s-k),
    U_(j,k)=D^j T_k,        j,k in Z.

All operators are unitary and complex-linear, and U_(0,0)=I. Every perturbed vector z_t^± remains one function in this very same L²(R), and its orbit uses exactly D, integer translations, and the natural pair (j,k). There is no direct-sum representation, oversampling, altered translation lattice, extra generator, or relabeling.

Bownik–Lemvig, *The canonical and alternate duals of a wavelet frame*, ACHA 23 (2007), 263–272, Theorem 1 on p.263, provides a single-generator dyadic complete frame whose canonical dual is not a single-generator wavelet system. The operator conventions are stated on p.264; the precise indexed local-commutant condition for the canonical dual is spelled out on p.265. Their Section 3 proves the example (Lemmas 1–2 and Theorem 3, pp.268–271); taking J=1 suffices. This verified statement supplies a frame vector for which Q fails.

The bridge therefore proves that the universal fixed-index canonical-tight assertion for classical dyadic single-generator frames is false. It does not identify the original Bownik–Lemvig generator itself as a tight counterexample, and it does not claim that the perturbed generator retains smooth bandlimited regularity. Those extra statements do not follow from this proof and are not needed for the all-L² contract.

Primary source:
https://pages.uoregon.edu/mbownik/papers/29.pdf
DOI: https://doi.org/10.1016/j.acha.2007.04.004

This application relies on the corrected 2007 theorem, not the flawed frame-operator argument in the 2002 predecessor. It uses neither the abstract's broad wording about generator counts nor a single example alleged to exclude every finite count.

## Why local commutant functional calculus alone is insufficient

For a fixed generator x, the local commutant is

    C_x(U)={B: BU_i x=U_i Bx for every i}.

It is a norm-closed linear space. The hypotheses BAx=ABx at the single point x do not automatically persist at another point such as Cx. For example, trying to multiply two local identities leaves the unproved equality

    B U_i Cx = U_i B Cx.

Thus one may not simply square F^(-1/2) in the local commutant, nor infer failure of F^(-1/2) from failure of F^(-1) at the same vector. The perturbation proof uses only linear combinations of generators, direct frame-operator calculations, subtraction of two valid indexed identities, and norm-continuity of functional calculus. It introduces no closure-under-products assertion.

## Optional converse: the universal properties are equivalent

For completeness, universal Q also implies universal P. This converse works over real or complex Hilbert spaces.

Fix x, write A=F^(1/2), and let (y_i)=(F^(-1/2)x_i) be the canonical Parseval frame, without assuming it has U-structure. Set a_0(s)=s on the compact interval [sqrt(a),sqrt(b)] and recursively

    a_(n+1)(s)=(a_n(s)+1/a_n(s))/2.

Assume Q for every frame vector. Define x_0=x and, recursively, let x_(n+1) be one half of x_n plus its canonical-dual generator. Induction gives

    U_i x_n=a_n(A)y_i,
    F_n=a_n(A)^2.

Indeed, universal Q identifies the canonical dual orbit with a_n(A)^(-1)y_i, so the next generator has the displayed next orbit. Every a_n is positive and bounded away from zero on the compact spectral interval, making every intermediate orbit a complete frame.

After one step a_n(s)≥1. For u≥1, writing r=(u-1)/(u+1) gives r_new=r² under u_new=(u+u^(-1))/2. Compactness therefore implies a_n -> 1 uniformly. Hence x_n -> y and U_i x_n -> y_i, while boundedness of U_i also gives U_i x_n -> U_i y. Consequently y_i=U_i y for every i, which is P(x).

This converse is not needed to apply the Bownik–Lemvig counterexample.
