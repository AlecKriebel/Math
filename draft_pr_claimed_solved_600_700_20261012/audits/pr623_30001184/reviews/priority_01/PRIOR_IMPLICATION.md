# Independent prior-result implication audit

This is a reviewer derivation, not a claim that the cited authors explicitly
stated the OWR negative answer. Input is the frozen PR623 theorem, including
its compression-only general C*-category. All statements below concern fixed
expectation GNS representations.

## A finite-image obstruction, with proof

Let (A,theta,i,p) be a unital general dilation of a norm-continuous Markov
semigroup T on a finite-dimensional unital C*-algebra B. Let (E,xi,pi) be the
expectation GNS correspondence. Suppose R=pi(A) is finite-dimensional and
theta is point-norm continuous. If ker pi is invariant under every theta_t,
then the generator of T is a *-derivation on B.

Indeed define beta_t(pi(a))=pi(theta_t(a)). Kernel invariance makes this a
well-defined unital *-endomorphism semigroup on R. Its point-norm continuity
follows by lifting a basis of finite-dimensional R to A. In finite dimension
this is operator-norm continuity. For sufficiently small h>0 the operator
F_h=h^(-1) integral_0^h beta_s ds is invertible, since F_h tends to I. The
identity beta_t F_h=h^(-1) integral_t^(t+h) beta_u du proves differentiability:

    beta'_t=(beta_(t+h)-beta_t) F_h^(-1)/h.

Differentiating beta_t(xy)=beta_t(x)beta_t(y) at t=0 shows that delta=beta'_0
is a *-derivation. This proof uses no inner implementation or recurrence
assumption. Equivalently, continuity makes beta_t invertible near zero;
beta_t=(beta_(t/n))^n then makes every beta_t an automorphism.

The map pbar:R->B defined by pbar(pi(a))=p(a) is well-defined because
p(a)=<xi,pi(a)xi>. Its embedding j=pi i is injective, since pbar j=id_B.
After identifying B with j(B), pbar is a conditional expectation: its
bimodularity follows from that of p. In particular,

    L(bc)=pbar(delta(j(b)j(c)))
         =pbar(delta(j(b)))c+b pbar(delta(j(c)))
         =L(b)c+bL(c),

where L=T'_0. Thus L is a derivation. For B=C^2 every derivation is zero:
if q=(1,0), the identity delta(q)=q delta(q)+delta(q)q gives both diagonal
coordinates of delta(q) zero. The specified two-state Markov generator has

    L(q)=(-1/2,+1/2),

so it cannot arise if the finite GNS kernel is invariant at all times. More
generally a finite-dimensional dissipative Markov generator cannot arise this
way; pbar delta j would have to be a derivation.

This is the expectation-bimodule version of the bounded-Hamiltonian/quantum
Zeno first-derivative obstruction. It is independently proved here and is
not attributed as a theorem about fixed GNS kernels in
[vom Ende, Theorem 1](https://arxiv.org/abs/2211.08351v3).

## Literal BFH example already yields a source counterexample

The primary antecedent is
[Burgarth, Facchi and Hillier, v2](https://arxiv.org/abs/2010.00279v2),
published online 24 July 2022 in Annales Henri Poincare,
[DOI 10.1007/s00023-022-01211-y](https://doi.org/10.1007/s00023-022-01211-y).
The relevant public construction predates PR623 by years. The original v1
was submitted 1 October 2020. Its Section 2 amplitude-damping example,
Section 3 point-localized clock state, and Theorem 4.4 Step 2 equation (11)
provide the ingredients; this paragraph identifies their location, while the
following compactification and GNS argument are this reviewer's deductions.

For the literal amplitude-damping model, let Hflip be the fixed self-adjoint
flip-flop matrix on the two qubits. Its unitary path is

    U(x)=exp(-i G(x) Hflip),
    G(x)=sgn(x) arccos(exp(-|x|/2)), G(0)=0.

The two finite limits of G are plus/minus pi/2. Hence U extends continuously
to the two-point compactification X=[-infinity,+infinity]. With W=U*, define
on C(X,M4)

    u_t(x)=W(x)* W(x+t),
    alpha_t(f)(x)=u_t(x) f(x+t) u_t(x)*.

The cocycle identity telescopes. Translation fixes the endpoints and is a
jointly continuous group, so alpha is a point-norm continuous automorphism
group. This is the C*-observable form of the BFH clock formula, with its
orientation matched to the Heisenberg compression. Put i(b)=constant
I_bath tensor b, and p(f)=<1_bath|f(0)|1_bath>, with the bath vector from
the amplitude-damping model. Then p i=id and p is a B-bimodule UCP map.
The displayed BFH finite-unitary dilation gives

    p alpha_t i = Phi_t,

the unital Heisenberg amplitude-damping Markov semigroup on B=M2. In
particular, for the decaying-level projection q, Phi_t(q)=exp(-t)q.

Now set A=C*(alpha_r(i(B)):r>=0) and theta_t=alpha_t|_A. A is unital,
separable, invariant for t>=0 and exactly forward-generated; theta is
injective and point-norm continuous. The restriction of p remains a
conditional expectation. All f with f(0)=0 act trivially in its GNS module,
because p(h* f* f h)=0 for every h. Therefore pi(A) is a quotient of the
finite-dimensional fibre A(0) subset M4 and is finite-dimensional.

If the GNS kernel were invariant at all times, the lemma would make Phi'_0
a derivation. But Phi'_0(q)=-q, whereas a derivation has
q delta(q) q=0. Contradiction. Thus this literal prior explicit model, after
routine compactification and forward restriction, already furnishes a
counterexample to the original universal generation-only source proposal.
There is no remaining mathematical gap in that implication.

The generic BFH theorem only promises the stated strong continuity of its
implementing unitary, and its unrestricted C_b(R) algebra need not have
point-norm continuous translations. Importing that generic conclusion without
checking the algebra would be invalid. The finite limits of the explicit
amplitude-damping path are precisely what justify the compact category used
above. No normal von Neumann claim is obtained.

## The exact symmetric two-state semigroup

The target P is equally available using the same known clock mechanism.
Let Xflip=[[0,1],[1,0]], g(t)=arccos(exp(-t))/2 for t>=0, and extend g
continuously to all real times by g(-t)=-g(t). It has finite endpoint limits.
Write c=cos g and s=sin g and use the standard block unitary

    U(t)=[[c I2,-s Xflip],[s Xflip,c I2]].

Compressing U(t)*(I2 tensor b)U(t) to the first bath vector gives

    Phi_t(b)=c(t)^2 b+s(t)^2 Xflip b Xflip.

This is the bit-flip Markov semigroup. On diagonal b it is exactly P_t.
Apply the same compactified clock construction and restrict its observed
algebra to B=C^2 (constant I_bath tensor diagonal matrices). Define p by
clock evaluation at zero, bath compression, and diagonal extraction. This is
a conditional expectation onto B. Its generated algebra has finite GNS image,
so the lemma proves noninvariance at some positive time.

This derivation settles the exact existence/negative-generation claim from
standard finite-unitary dilation plus the prior clock method. The candidate's
M2 rather than M4 implementation and exact witness at log 2 are a cleaner
explicit realization. The candidate's strict concavity argument further
shows failure at every positive time. That quantified strengthening is not
stated by the cited BFH theorem and is not established by the all-time lemma
alone. Neither that small refinement nor the choice of P makes the general
clock/evaluation/cocycle mechanism new.

## Priority meaning

An implication proved now is not evidence that an earlier author explicitly
published or recognized that implication. Accordingly the audit separates:

- The clock/evaluation method and first-derivative obstruction are published
  antecedents and require credit.
- The exact negative source conclusion is already a short consequence of
  those antecedents, with no mathematical gap in the derivation above.
- No primary publication explicitly asserting the fixed-GNS,
  forward-generation OWR counterexample was located in the bounded search.
- The candidate can at most be framed as an explicit small-model observation
  connecting these known constructions to the particular fixed-GNS proposal,
  with an all-positive-time witness refinement. The audit does not certify
  that even this connection/refinement is first in the literature.

If a priority gate requires a materially new construction or substantial new
mathematical consequence, this candidate fails that novelty standard. If a
credited explicit corollary resolving the proposed source formulation is
eligible, it can be accepted with mandatory credit and that exact framing.
There is no evidence here for independent-development or plagiarism claims.
