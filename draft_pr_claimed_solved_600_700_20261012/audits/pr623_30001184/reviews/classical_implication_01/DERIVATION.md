# A short corollary of the BFH clock construction

This is an independent implication audit of PR623 at original head
`947442c091ae617804c6a0d07b98ff2c50368798`. It concerns the generation-only
counterexample claim in the packet, not the conditional extension problem after
kernel invariance has been assumed. Initial conclusion was reached without
reading the priority reviewer's conclusions.

## Exact conclusion

The construction in Burgarth, Facchi and Hillier (BFH), *Control of quantum
noise: on the role of dilations*, arXiv:2010.00279v2 (25 July 2022), Definition
4.1 and Theorem 4.4, proof Steps 1-2, provides a short complete deduction of the
following assertion:

There is a unital separable C*-algebra A with an injective point-norm continuous
endomorphism semigroup theta, a unital embedding of B=C^2, and a conditional
expectation i p onto i(B), such that A=C*(theta_r(i(B)):r>=0), the compression
p theta_t i is the two-state exponential decay semigroup, and the kernel of the
left GNS representation of p is not invariant under theta.

The prior paper does not state this GNS-kernel corollary or claim to answer the
OWR problem. The deduction below adds only an explicit elementary Kraus
completion, forward-generated restriction, a continuity check, and an elementary
finite-dimensional derivation obstruction. An exact witness is also given.

## 1. The existing clock mechanism, specialized explicitly

Let X=[[0,1],[1,0]] on H0=C^2, let H1=C^2 be the finite bath, and let
S:H0->H1 tensor H0 send v to e1 tensor v. For t>=0 put

    g(t) = (1/2) arccos(exp(-t)),
    g(-t) = -g(t),
    W(t) = [[cos(g(t)) I2, -sin(g(t)) X],
            [sin(g(t)) X,  cos(g(t)) I2]].

This is unitary, W(0)=I4, and W(-t)=W(t)*. Its first bath column is exactly
the two Kraus operators cos(g(t)) I2 and sin(g(t)) X. Consequently

    S* W(t)* (I2 tensor b) W(t) S
      = cos^2(g(t)) b + sin^2(g(t)) X b X
      = Phi_t(b),                    b in M2, t>=0.

Write L=(Ad_X-id)/2. Since Ad_X is an involution,

    Phi_t = (id+Ad_X)/2 + exp(-t)(id-Ad_X)/2 = exp(t L).

This is an analytic UCP semigroup. Thus it is within BFH's finite-dimensional
analytic-channel category. The unitary W is a choice of the finite Kraus
completion used in Step 1. No general Choi eigenvalue regularity assertion is
needed for this specialization.

Set U(x,y)=W(x)W(y)*. BFH Step 2, equation (11), gives on L2(R,C^4)

    (Uhat(t) xi)(x) = W(x)W(x-t)* xi(x-t).

Equivalently Uhat(t)=M_W T(t) M_W*, where T(t) is ordinary translation.
This is a strongly continuous unitary group. Its action by Ad(Uhat(t)*) on
matrix-valued multiplication operators is

    alpha_t(f)(x) = W(x)W(x+t)* f(x+t) W(x+t)W(x)*.              (1)

It is a group of unital *-automorphisms of C_b(R,M4). The group law follows
by cancelling W(x+t)*W(x+t). This is precisely the point-localized clock
construction, with BFH Option 1's evaluation state at x=0 and its finite pure
bath state. The clock is classical and the Hilbert-space implementation is on
the separable L2 space used by BFH.

## 2. Forward generation and the required continuity

For either B=M2 or B=D=C^2 (diagonal matrices in M2), let i(b)(x)=I2 tensor b
and define

    A_B = C*(alpha_r(i(B)): r>=0),
    theta_t = alpha_t restricted to A_B,                t>=0.

Then theta_t(A_B) is contained in A_B, theta_t is unital and injective, and the
required forward-generation equality holds by definition.

Strong continuity of Uhat DOES NOT by itself prove point-norm continuity of
alpha on C_b(R,M4): even scalar translations on C_b(R) need not have this
property. This potential hidden assumption is eliminated explicitly here.
The function g has limits -pi/4 and pi/4 at the two ends of R, hence is uniformly
continuous (continuous on each compact interval, with arbitrarily small
oscillation in each sufficiently far tail). W is therefore uniformly continuous.
For any b and any real s,t,

    ||alpha_t(i(b))-alpha_s(i(b))||
      <= 2 ||b|| sup_x ||W(x+t)-W(x+s)|| -> 0 as t->s.

For a generator alpha_r(i(b)), its theta orbit is alpha_(t+r)(i(b)), so has the
same continuity. Multiplication and adjoints preserve this property on finite
*-polynomials. Contractivity of alpha and norm approximation extend it to every
element of A_B. Thus theta is point-norm continuous. Rational nonnegative shifts
and a finite basis of B generate a dense subalgebra, proving separability.

This check uses no compactification modification of BFH's clock and no assertion
of point-norm continuity on the full C_b ambient algebra. One could equivalently
work with bounded uniformly continuous functions, or with functions having both
endpoint limits, for this explicit W.

## 3. The expectation and the same Markov semigroup

For B=M2 define p(f)=S*f(0)S. For B=D define

    p(f)=Delta(S*f(0)S),

where Delta extracts the system diagonal. In both cases p is UCP, p i=id_B, and

    p(i(b1) f i(b2)) = b1 p(f) b2.

The equation follows from i(b)S=Sb and, in the D case, the D-bimodule property
of Delta. Therefore i p is a contractive positive idempotent B-bimodule map of
A_B onto i(B), hence a conditional expectation. Restriction to the generated
algebra loses none of these properties. There is no need for faithfulness of p.

By (1), evaluation at zero gives alpha_t(i(b))(0)=W(t)*i(b)W(t). Thus
p theta_t i=Phi_t for B=M2. On B=D the same map preserves D and is

    T_t(b1,b2) = (1/2)*((1+exp(-t))*b1+(1-exp(-t))*b2,
                        (1-exp(-t))*b1+(1+exp(-t))*b2).

This is exactly the packet's two-state decay semigroup, at every real t>=0.
It is uniformly continuous and unital. Only compression on i(B) has been used;
the stronger equation p theta_t=T_t p on all A_B has not been imported.

## 4. Finite GNS image without confusing the two kernels

Let F be the finite-dimensional evaluation image {f(0):f in A_B} in M4.
The GNS module embeds isometrically as follows. For B=M2, take the span of

    f(0) S b in M_(4,2),
    <z,w> = z*w.

For B=D use the same span, right diagonal multiplication, and

    <z,w> = Delta(z*w).

In the second case the inner product is definite because its entries are the
squared norms of the two columns. In both cases it agrees on generators with
<a tensor b,c tensor d>=b* p(a*c) d. Its completion E is a finite-dimensional
complex vector space. The left GNS representation pi(f) is the restriction of
left multiplication by f(0) to E; this is *-stable because F is a C*-algebra.
Consequently C=pi(A_B) is a finite-dimensional C*-algebra.

The vector-null condition f(0)S=0 is NOT asserted to be the representation
kernel. The latter requires f(0)z=0 for every z in E. We only use these valid
implications: f(0)=0 implies pi(f)=0, and pi(f)=0 implies p(f)=0. The latter
also follows from p(f)=<S,pi(f)S>. No identification of these two kernels is
necessary for either proof below.

Define j=pi i and pbar:C->B by pbar(pi(f))=p(f). This is well-defined because
ker(pi) is contained in ker(p), or directly by pbar(c)=<S,cS>. It is UCP,
pbar j=id_B, and

    pbar(j(b1) c j(b2)) = b1 pbar(c) b2.                        (2)

Thus j is faithful and the expectation factors correctly through the GNS image.

## 5. The proposed finite-dimensional deduction is complete

Suppose theta_t(ker(pi)) is contained in ker(pi) for every t>=0. Then

    beta_t(pi(f)) = pi(theta_t(f))

is a well-defined unital *-endomorphism semigroup on C. It is point-norm
continuous, because each c in C has a representative f and
||beta_t(c)-beta_s(c)|| <= ||theta_t(f)-theta_s(f)||. C is finite-dimensional,
so continuity also holds in the operator norm of the linear maps beta_t.

For completeness, its bounded generator requires no unproved regularity claim.
Choose h>0 small enough that R=integral_0^h beta_s ds is invertible, since
R/h tends to id. The semigroup equation gives

    beta_t R = integral_t^(t+h) beta_u du,
    (d/dt)(beta_t R) = beta_(t+h)-beta_t = beta_t(beta_h-id).

Hence beta_t is differentiable, with bounded generator
delta=(beta_h-id) R^(-1). Differentiating beta_t(xy)=beta_t(x)beta_t(y) at zero
shows that delta is a derivation.

For the projection q=diag(1,0) in B and e=j(q), differentiating e^2=e gives

    delta(e)=delta(e)e+e delta(e),
    e delta(e) e = 0,
    (1-e) delta(e) (1-e) = 0.

Equation (2) forces the corresponding diagonal corners of pbar(delta(e)) to
vanish. But differentiating the actual compression gives

    pbar(delta(e)) = T'_0(q) = diag(-1/2,+1/2),

which has nonzero diagonal corners. This is impossible for B=M2, and is also
impossible for B=D, where any element with both diagonal corners zero is zero.
Thus the representation kernel fails invariance for at least one t>0.

Every step applies to the fixed expectation-GNS representation. It does not
silently replace the expectation, use a different dilation, or assume a
compatible extension on a larger algebra.

## 6. Exact witness, independently avoiding the generator argument

The failure can be located at the packet's same time s=log(2). Work with B=D,
q=i(diag(1,0)), q_s=theta_s(q), and

    a = q q_s q - (3/4)q in A_D.

For any real angle z, conjugating q by the block unitary W with angle z gives
q W* q W q=cos^2(z)q. Therefore a(0)=0 because g(s)=pi/6, so pi(a)=0.
At x=s, the cocycle in (1) has angle -[g(2s)-g(s)]. Thus

    a(s) = d q,
    d = cos^2(g(2s)-g(s))-3/4 = 3(sqrt(5)-1)/16 > 0.

Applying (1) again,

    theta_s(a)(0)=d W(s)* q W(s),
    p theta_s(a)=d diag(3/4,1/4) != 0.

Consequently pi(theta_s(a)) is nonzero, while pi(a)=0. This is a
representation-kernel counterexample, rather than a vector-null counterexample.
The matrix orientation is the Ad(Uhat(t)*) orientation actually used in BFH.

In fact the same witness works at every positive time, and for both B=D and
B=M2. For s>0 set u=exp(-s) and

    a_s = q theta_s(q) q - ((1+u)/2)q.

Then a_s(0)=0. The angle-difference identity gives

    d_s = cos^2(g(2s)-g(s))-cos^2(g(s))
        = ((1-u^2)/2) [sqrt(1+u^2)-u] > 0,
    a_s(s)=d_s q,
    p theta_s(a_s)=d_s diag((1+u)/2,(1-u)/2) != 0.

Here cos(2g(2s)-2g(s))=u^3+(1-u^2)sqrt(1+u^2); the factorization follows by
subtracting u. Positivity of this coefficient holds because 0<u<1 and
sqrt(1+u^2)>u. At s=0 the witness is zero, as required; as s tends to infinity
d_s tends to 1/2. Thus no positive-time theta_s respects the GNS kernel in
either explicit specialization.

This is a selfadjoint nonzero kernel witness, not a globally positive element
of the odd-extension clock algebra. For example, at s=log(2) and x=-s/2,
g(x+s)-g(x)=2g(s/2), so a_s(x)=(exp(-s)-3/4)q=-(1/4)q. The globally
positive witnesses obtainable with the packet's clipped negative-time extension
are a distinct additional property. Global positivity is unnecessary for the
kernel-invariance counterexample or the short prior-construction corollary.

The derivation in Section 5 and the explicit witness are separate checks of the
same claim. The accompanying dependency-free exact arithmetic script verifies
the finite 4x4 matrices and the radical coefficient; continuity and the GNS
factorization are proved above, not inferred from sampled numerical checks.

## Priority interpretation and precise limits

The original packet's strongest verified result is mathematically correct, but
its universal negative claim is already a short specialization and elementary
corollary of the prior BFH clock mechanism. The choice B=D even supplies the
same base algebra and Markov semigroup. No new central dilation mechanism is
needed. This audit establishes that specific prior implication, for use by a
priority gate that excludes short corollaries of prior work. It does not
adjudicate a universal historical firstness claim.

This is not evidence that BFH's authors explicitly settled the OWR question;
their stated Theorem 4.4 concerns dynamically decouplable autonomous dilations.
Nor is it a theorem that every BFH dilation for every analytic channel is
point-norm continuous on the full C_b clock algebra. The explicit channel and
completion above resolve exactly the continuity needed for this counterexample.
The conditional extension question after kernel invariance is assumed remains
outside this result, as do normal von Neumann and weak/corner dilation variants.

## Primary references

- Burgarth, Facchi and Hillier, [arXiv:2010.00279v2](https://arxiv.org/abs/2010.00279v2),
  pp. 5, 9-12; journal version Annales Henri Poincare 24 (2023), 325-347,
  [DOI 10.1007/s00023-022-01211-y](https://doi.org/10.1007/s00023-022-01211-y).
- OWR target: [DOI 10.4171/OWR/2009/09](https://doi.org/10.4171/OWR/2009/09),
  general-dilation definition p. 498, GNS discussion pp. 498-499, first problem
  pp. 542-543. The domain/codomain typo in the problem's p notation is reconciled
  with the introduction's definition, as in the original packet.
