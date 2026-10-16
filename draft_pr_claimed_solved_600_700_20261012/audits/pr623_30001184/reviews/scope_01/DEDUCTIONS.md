# Independent deductions for PR623 / 30001184

These are mathematical reconstructions by the source-scope adversary. They do
not use a previous audit verdict. They concern the fixed expectation and fixed
dilation in the candidate, not existence of some different dilation.

## 1. General fibre-evaluation mechanism

Let C = C(X,M_d), let x0 be a point of X, and let A be a unital C*-subalgebra
whose evaluation at x0 is all of M_d. Let D be the constant diagonal algebra,
contained in A, and p(f)=Delta(f(x0)). Then p is a conditional expectation
onto D: evaluation and diagonal extraction are unital CP, p fixes D, and
diagonal multiplication makes p a D-bimodule map.

The GNS correspondence of p is M_d with right action by D and inner product
<z,w>=Delta(z* w). Each diagonal entry of <z,z> is the squared length of a
column; therefore this is a definite inner product. The left action is
pi(f)z=f(x0)z. The vector I is cyclic because evaluation(A)=M_d, and it is a
unit vector. In particular,

    ker pi = {f in A : f(x0)=0}.

This identifies the kernel of the entire left representation. It is not an
inference from one scalar vector state. In this special example the vector-null
condition p(f* f)=0 happens also to imply f(x0)=0, because Delta is faithful
on positive matrices. That equivalence does not hold for general expectations.

Suppose theta_t(f)(x)=u_t(x) f(F_t(x)) u_t(x)*, with a continuous base flow F
and a unitary cocycle u. Then descent requires every relation in the evaluation
image at x0 to remain a relation at F_t(x0). More precisely, kernel invariance
is equivalent to existence of a homomorphism beta_t on evaluation(A) satisfying

    beta_t(f(x0)) = u_t(x0) f(F_t(x0)) u_t(x0)*.

Forward generation A=C*(theta_r(D):r>=0) does not make this compatibility
automatic: it controls generators, while evaluation erases relations among
their values at other base points. This is a structural model of the failure,
without an unrelated direct summand.

## 2. Reconstruct the continuous model

Take the two-endpoint compactification X=[-infinity,+infinity]. Translation
fixes endpoints. It is a jointly continuous group action: neighborhoods of an
endpoint are tails, and a bounded interval of translation parameters preserves
every sufficiently far tail. Set

    g(x)=0 (x<=0), g(x)=arccos(exp(-x))/2 (x>0),
    g(-infinity)=0, g(+infinity)=pi/4, V(x)=R(g(x)),
    R(z)=[[cos z,-sin z],[sin z,cos z]],
    u_t(x)=V(x)*V(x+t),
    alpha_t(f)(x)=u_t(x)f(x+t)u_t(x)*.

The cocycle telescopes, so alpha is an automorphism group. Joint continuity
on each compact time interval times compact X gives point-norm continuity for
every fixed f. No bounded generator or operator-norm continuity of alpha_t is
required. The cusp of g at zero is permissible.

Put A=C*(alpha_r(D):r>=0), theta=alpha restricted to A, and x0=0. A is unital
and separable; theta_t is an injective unital endomorphism, continuous in point
norm, and preserves A because r maps to r+t. The stated forward generation is
an exact equality, not a heuristic comparison with the ambient C.

With q=diag(1,0), theta_t(q)(0)=R(g(t))qR(g(t))*. Its diagonal is

    ((1+exp(-t))/2, (1-exp(-t))/2).

Thus p theta_t on D is the two-state semigroup P_t=J+exp(-t)K, where J and K
are complementary rank-one idempotents, J+K=I and JK=KJ=0. This proves the
semigroup law for all nonnegative real times. Positivity and unitality are
entrywise clear, and positive maps on a commutative algebra are CP. Its time
continuity is uniform because D is finite dimensional.

At s=log(2), Q=theta_s(q)(0) has entries 3/4,1/4 and off-diagonal sqrt(3)/4.
Consequently qQ(1-q) supplies a nonzero e12, its adjoint supplies e21, and
q and 1-q supply the diagonal units. Evaluation(A)=M2. Section 1 applies.

The full GNS right D-module is the direct sum of its two column spaces C2.
Every D-linear adjointable operator acts separately on those spaces, hence

    B^a(E)=M2 direct-sum M2,
    pi(A)={(z,z): z in M2}.

The module is full since <I,I>=1_D. This is fullness of the module, not a
claim that the original unital general dilation is a full weak dilation.

## 3. Independent infinitesimal obstruction

This argument forces failure of GNS descent without using the explicit kernel
witness from the packet.

Assume all theta_t preserve ker pi. Then beta_t(pi(f))=pi(theta_t(f)) defines
a point-norm continuous unital endomorphism semigroup of M2. Continuity holds
because every represented element has a lift and pi is contractive. In finite
dimension point-norm continuity is continuity in norm of the linear operators
beta_t.

For sufficiently small epsilon>0, S=integral_0^epsilon beta_r dr is invertible:
S/epsilon tends to the identity. The identity

    beta_t S = integral_t^(t+epsilon) beta_r dr

shows that beta_t is right differentiable at zero and differentiable for
positive t. Put delta=beta'_0. Differentiating beta_t(ab)=beta_t(a)beta_t(b)
gives delta(ab)=delta(a)b+a delta(b). In particular, q^2=q gives

    delta(q)=delta(q)q+q delta(q),
    q delta(q) q=0, (1-q)delta(q)(1-q)=0,
    Delta(delta(q))=0.

But Delta(beta_t(q))=T_t(q), whose derivative at zero is
diag(-1/2,+1/2), nonzero. Contradiction. Therefore a kernel failure must occur.
This independently ties the obstruction to irreversible first-order decay
compressed from a finite represented algebra, rather than to a guessed
trigonometric constant. It also rules out a compatible endomorphism semigroup
on all B^a(E): such a semigroup would restrict to beta_t on pi(A).

## 4. Exact witness and positive margin

The failure can be located at s=log(2). Let

    a=q theta_s(q) q-(3/4)q.

Its value at zero is zero. At x=s the angle in theta_s(q) is

    delta=g(2s)-g(s)=arccos(1/4)/2-pi/6.

Using sin(arccos(1/4))=sqrt(15)/4 gives

    cos(2 delta)=(1+3 sqrt(5))/8,
    cos^2(delta)=(9+3 sqrt(5))/16,
    a(s)=d q, d=3(sqrt(5)-1)/16>0.

Thus theta_s(a)(0)=dQ and p theta_s(a)=d diag(3/4,1/4), whereas p(a)=0.
Moreover theta_s(a)^*theta_s(a)(0)=d^2 Q, so even the GNS vector norm is
strictly nonzero after evolution. The positivity margin is d approximately
0.2317627457812106; this is not a floating-point sign decision.

## 5. Strongness, faithfulness, and reasonable repair routes

The exact witness violates p theta_s=T_s p on A, so it is not strong. This is
consistent with being a general Markov dilation. With the unital embedding,
a weak/corner dilation would have corner projection i(1)=1 and expectation
equal to the identity on A; this expectation does not. Therefore theorems
whose scope is weak Markov dilations are inapplicable.

Faithful p is a genuine extra sufficient assumption for the first stage:
pi(a)=0 implies p(a*a)=0, and faithfulness implies a=0. It does not itself
prove extension to B^a(E). Another elementary first-stage repair is strongness
plus surjectivity of theta_t. If a is in ker pi, every h=theta_t(k) satisfies

    p(h* theta_t(a)*theta_t(a)h)
      =p(theta_t(k*a*ak))=T_t(p(k*a*ak))=0.

Surjectivity makes this every h in A, so theta_t(a) is in ker pi. Strongness
without surjectivity is not established by this calculation: h need not be
in theta_t(A). No positive extension theorem is inferred here.

Replacing the conjecture by the exact GNS-kernel-invariance implication is a
restatement of the central first-stage difficulty. It is blocked as a proposed
new minimality mechanism until new evidence proves it from a useful external
condition. Extension conditional on invariance is a separate unresolved step.

## 6. Quantifier calculation

Let G denote forward generation and let Dn denote the desired conjunction of
kernel descent and compatible extension for a fixed dilation. The verified
counterexample gives an admissible quadruple with G and not Dn. Therefore

    for all general dilations, G implies Dn

is false. A counterexample to the first conjunct refutes the two-stage universal
conclusion; a second-stage counterexample with invariant kernel is unnecessary
for that negative result. It does not imply that the conditional statement
invariance implies extension is false.

If H is logically weaker than G (G implies H on admissible quadruples), the
same example has H and not Dn. Hence no such weaker H can be universally
sufficient. An incomparable or stronger condition is not covered. In
particular, an existential claim that this Markov semigroup has some other
module/weak dilation is neither refuted nor required to fail.
