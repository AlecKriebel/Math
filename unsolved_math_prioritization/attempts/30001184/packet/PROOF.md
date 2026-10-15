# A generated continuous dilation whose GNS kernel is not invariant

## Result and precise scope

There is a unital, separable C*-algebra A, a point-norm continuous semigroup
(theta_t)_{t >= 0} of injective unital *-endomorphisms of A, a unital embedding
of B = C^2 into A, and a conditional expectation p: A -> B such that:

1. A = C*(theta_t(B): t >= 0);
2. T_t = p theta_t|_B is the uniformly continuous two-state Markov semigroup
   with transition matrix

       P_t = (1/2) [[1 + exp(-t), 1 - exp(-t)],
                    [1 - exp(-t), 1 + exp(-t)]];

3. if pi is the left action in the GNS B-correspondence of p, then
   theta_s(ker pi) is not contained in ker pi for s = log 2.

Consequently no maps on pi(A), or on all adjointable operators of that fixed
GNS module, can intertwine pi with this dilation. Generation by the observed
algebra and its forward time shifts does not suffice for the two-stage
GNS-extension proposal in OWR-3392-012.

This is a counterexample to that universal generation-only assertion. It does
not claim that, whenever kernel-invariance is separately assumed, every
induced endomorphism semigroup fails to extend. Nor does it rule out stronger
conditions involving the expectation, a corner dilation, a different GNS
module, or a different dilation of the same Markov semigroup. Any condition
logically weaker than the generation hypothesis alone also cannot suffice:
this example satisfies the generation hypothesis itself.

## 1. Continuous ambient dynamics

Let X = [-infinity,+infinity] be the two-point compactification of the real
line, with its order topology. This is a compact metrizable space. Write
C = C(X,M_2(C)). Put

    g(x) = 0                                      for x <= 0,
    g(x) = (1/2) arccos(exp(-x))                   for x > 0,
    g(-infinity) = 0,     g(+infinity) = pi/4.

This defines a continuous real-valued function on X. For a real angle z let

    R(z) = [[cos z, -sin z], [sin z, cos z]],
    V(x) = R(g(x)).

For t in R, translation x -> x+t fixes both endpoints of X. It is a
homeomorphism, and (t,x) -> x+t is jointly continuous on R x X. Set

    u_t(x) = V(x)* V(x+t),
    alpha_t(f)(x) = u_t(x) f(x+t) u_t(x)*.

The cocycle equality

    u_s(x) u_t(x+s) = V(x)* V(x+s) V(x+s)* V(x+s+t)
                    = u_(s+t)(x)

proves alpha_s alpha_t = alpha_(s+t). Each alpha_t is a unital
*-automorphism of C, with inverse alpha_(-t).

For completeness, this group is point-norm continuous. For a fixed f in C,
the function (t,x) -> u_t(x) f(x+t) u_t(x)* is jointly continuous. On every
compact t-interval times X it is uniformly continuous, so its supremum-norm
variation tends to zero as t tends to any fixed t_0. This is continuity of
t -> alpha_t(f); uniform continuity of t -> alpha_t in operator norm is not
needed or asserted.

## 2. Enforce exactly the proposed generation condition

Let D be the constant diagonal matrices in C, identified with B = C^2.
Define the C*-subalgebra

    A = C*(alpha_r(D): r >= 0)  contained in C.

This is unital and separable. For every t >= 0,
alpha_t(alpha_r(D)) = alpha_(t+r)(D), hence alpha_t(A) is contained in A.
Let theta_t be this restriction. It is unital, injective, and point-norm
continuous, since it is the restriction of alpha_t. Surjectivity on A is
not needed. By the definition of A,

    A = C*(theta_r(D): r >= 0).

Thus there is no added independent algebraic summand: every element of A is
norm-approximated by *-polynomials in the observed time translates. The
ambient algebra C is only a construction device; the dilation algebra is A.

Let Delta: M_2(C) -> D denote diagonal extraction and define

    p(f) = Delta(f(0)),
    i(b) = the constant diagonal matrix b.

Evaluation at 0 is a unital *-homomorphism, and Delta is unital completely
positive. Thus p is unital completely positive. Moreover p i = id_D, and
p(i(b_1) f i(b_2)) = b_1 p(f) b_2. Consequently i p is a positive,
contractive, idempotent D-bimodule projection of A onto i(D): it is a
conditional expectation. This verifies the source's general-dilation
condition, with the expectation oriented A -> B.

## 3. The compression is a genuine Markov semigroup

At x=0 and t>=0, V(0)=1 and u_t(0)=R(g(t)). For b=diag(b_1,b_2),

    p theta_t(b)
      = diag(cos^2(g(t)) b_1 + sin^2(g(t)) b_2,
             sin^2(g(t)) b_1 + cos^2(g(t)) b_2).

Because cos(2g(t))=exp(-t), this is exactly the matrix P_t in the theorem.
If J=(1/2)[[1,1],[1,1]] and K=(1/2)[[1,-1],[-1,1]], then
J^2=J, K^2=K and JK=KJ=0, so

    P_s P_t = (J+exp(-s)K)(J+exp(-t)K)
            = J+exp(-(s+t))K = P_(s+t).

The P_t are positive stochastic matrices, hence unital completely positive
maps on C^2, and P_0 is the identity. Their entries vary continuously, even
analytically, with t. Thus (A,theta,i,p) is a unital dilation of a genuine
uniformly continuous Markov semigroup for every real t>=0, not only at a
single time or at integer times.

## 4. Identify the GNS representation kernel

The Hilbert D-module M_2(C), with right action by diagonal multiplication and
D-valued inner product

    <z,w> = Delta(z* w),

is a concrete GNS correspondence for p once A acts by f.z = f(0)z and the
cyclic vector is xi=I_2. The inner product is definite: if Delta(z*z)=0,
both columns of z have squared norm zero, so z=0. It is complete because
it is finite-dimensional.

To verify cyclicity, let q=diag(1,0) and choose s=log 2. Since
exp(-s)=1/2, g(s)=pi/6, and the evaluation of theta_s(q) at 0 is

    Q = [[3/4, sqrt(3)/4], [sqrt(3)/4, 1/4]].

The evaluation image of A contains q, I_2 and Q. It therefore contains
q Q (I_2-q)=(sqrt(3)/4)e_12 and its adjoint, as well as the two diagonal
matrix units. It is all of M_2(C). Hence A xi D spans this module.

The canonical left representation is therefore

    pi(f)z = f(0)z,
    ker pi = {f in A: f(0)=0}.

This is the representation kernel, not merely the null space of a single
vector state. One can also check it without identifying the module: if
f(0)=0, then p(h* f* f h)=0 for every h in A, so pi(f)=0; conversely
pi(f)=0 implies p(f*f)=0 and thus f(0)=0 by faithfulness of Delta on
positive 2x2 matrices.

The module is full, since <xi,xi>=1_D. Its adjointable operators are
B^a(E) = M_2(C) direct-sum M_2(C), acting separately on the two columns.
Under this identification pi(A) is the diagonal copy {(z,z):z in M_2(C)}.
Fullness and finite-dimensionality of the GNS module do not prevent the
obstruction below.

## 5. An exact element that leaves the kernel

Retain s=log 2 and put q_s=theta_s(q). The self-adjoint element

    a = q q_s q - (3/4)q

belongs to A. From Q above, a(0)=0, so pi(a)=0.

At the point x=s, the cocycle angle for theta_s is

    delta = g(2s)-g(s)
          = (1/2)arccos(1/4) - pi/6.

Thus q q_s(s) q=cos^2(delta)q. The angle-difference identity gives

    cos(2 delta)
      = cos(arccos(1/4)-pi/3)
      = (1+3 sqrt(5))/8,

and therefore

    cos^2(delta) = (9+3 sqrt(5))/16,
    a(s) = d q,      d = (3 sqrt(5)-3)/16 > 0.

Applying theta_s and evaluating at 0 now gives

    (theta_s(a))(0) = R(pi/6) a(s) R(pi/6)* = d Q != 0.

In particular

    p theta_s(a) = d diag(3/4,1/4) != 0.

Hence theta_s(a) is not in ker pi, although a is. The kernel is not invariant.

If endomorphisms beta_t on pi(A) satisfied beta_t(pi(f))=pi(theta_t(f)), the choice
f=a would yield beta_s(0)=pi(theta_s(a))!=0. Thus there is no induced
endomorphism at this time. In particular, there cannot be an E0-semigroup
on B^a(E) restricting to the specified represented dynamics. The obstruction
occurs before any product-system classification or extension theorem can
apply.

## 6. Hypotheses that must not be silently added

- The construction is in the C*-algebra setting explicitly permitted by the
  source. It makes no claim about a normal, strongly continuous von Neumann
  version. Merely taking biduals would require a new continuity check.
- The maps theta_t are injective and point-norm continuous; the Markov maps
  T_t are uniformly continuous. There is no discrete-time loophole.
- The expectation p is not faithful; that is allowed in the source, whose
  first stage explicitly concerns a nonfaithful GNS representation. Imposing
  faithfulness of p would remove this particular first-stage obstruction.
- This is a general unital dilation, not a weak/corner dilation. If it were
  weak with unital i, its corner projection would be 1 and p would be the
  identity on A, which it is not.
- It is not strong in the sense p theta_t = T_t p on all A: the witness has
  p(a)=0 but p theta_s(a)!=0. The source's displayed definition of a general
  dilation does not impose this extra equation.
- Algebraic generation is different from uniqueness or minimality of a
  Markov dilation with specified multitime moments. Those stronger notions
  cannot be imported from a theorem about a different dilation category.
- The ambient dynamics uses the explicit continuous unitary cocycle u_t.
  This is a construction of the given dilation, not a claim that cocycle
  conjugacy permits replacing it when asking for its fixed GNS extension.
- No product system is assumed. A product-system existence theorem that
  constructs some dilation of T does not prove that this particular theta
  descends through this particular pi.

A useful necessary compatibility condition for any revised proposal is
precisely that, for every a in A,

    [p(h* a* a h)=0 for all h in A]
       implies
    [p(h* theta_t(a)* theta_t(a) h)=0 for all h in A].

This is an exact reformulation of GNS-kernel invariance, not a new sufficient
minimality theorem and not a resolution of the conditional extension problem.
A condition weaker than forward generation alone cannot repair the failure;
a successful replacement must add a restriction not satisfied here. The
search for broadly useful stronger conditions is left open.

## Sources and status

The target is the first problem in Michael Skeide's section on the module
approach, pp. 542-543 of *Mini-Workshop: Product Systems and Independence in
Quantum Dynamics*, Oberwolfach Reports 6 (2009), 493-548,
[DOI 10.4171/OWR/2009/09](https://doi.org/10.4171/OWR/2009/09).
The general-dilation definition used here is on pp. 497-498 of the same report.
The report's reversed domain/codomain in the problem's expectation notation is
resolved using that definition and its diagram.

The distinction between general, strong, and weak dilations is also explicit
in Appendix B(i), pp. 211-213 of the inspected v3 of Shalit and Skeide,
*CP-Semigroups and Dilations, Subproduct Systems and Superproduct Systems:
The Multi-Parameter Case and Beyond*,
[arXiv:2003.05166v3](https://arxiv.org/abs/2003.05166v3), later published in
Dissertationes Mathematicae 585 (2023),
[DOI 10.4064/dm823-5-2022](https://doi.org/10.4064/dm823-5-2022).
That work distinguishes its weak-dilation theorems from general dilations;
its abstract is not a resolution certificate for the present question.

This document supplies an explicit candidate counterexample, not a verified
claim of literature priority. Bounded literature searches found no earlier
matching resolution. Independent mathematical and source review is required
before accepting the candidate.

A later related formulation is in Section 5, p. 34 of Skeide and Sumesh,
*CP-H-Extendable Maps between Hilbert modules and CPH-Semigroups*,
[arXiv:1210.7491v2](https://arxiv.org/abs/1210.7491v2), subsequently published
in J. Math. Anal. Appl. 414 (2014), 886-913,
[DOI 10.1016/j.jmaa.2014.01.024](https://doi.org/10.1016/j.jmaa.2014.01.024).
The inspected passage raises the general GNS-extension question; it is not
used as a theorem establishing either a positive or negative answer.
