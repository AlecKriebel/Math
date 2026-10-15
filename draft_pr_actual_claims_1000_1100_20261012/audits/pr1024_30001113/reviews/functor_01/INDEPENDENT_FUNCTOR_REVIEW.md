# Independent adversarial review: actual deformation functors

Reviewer task: family B for PR #1024 / problem 30001113, head
`37b4b2fa44368f49e534e4982bd11f5667e0bf36`.
Input: submitted `current/COUNTEREXAMPLE.md`, SHA-256
`055da7260c2d05c988aafdf99076f85dc8d03c5151dc1b48e301ad7b8aa7d249`.

## Verdict and claim tested

**No mathematical or source-scope blocker found in this family.** The submitted
argument gives an exact negative instance of the unrestricted OWR question and
arXiv v1 Question 4.4. It applies to the actual equivalence-class functors, not
merely to their versal hulls. Its statement that *every* prorepresentable
recipient is excluded is justified.

The claim tested is this: for the action of G=(F_4,+) on k[[t]] given by
rho(a)(t)=t/(1+at), with N=F_2 and Q=G/N, there are no prorepresentable F and
natural maps f:D_N^Q->F, g:D_Q->F for which (res,ind) factors through
E=D_N^Q x_F D_Q and D_G->E is smooth in the source's category.

This review does **not** establish novelty or settle the variant with additional
prorepresentability assumptions on D_N and D_Q. Neither novelty nor that
variant is needed for the mathematical counterexample, but neither should be
claimed in a preprint. The priority audit remains a separate requirement.

## Primary-source scope audit

Original sources were obtained independently from their primary hosts:

1. [arXiv:1112.0352v1](https://arxiv.org/pdf/1112.0352v1), pp.2-5 and 13-15.
   Definitions 1.1-1.2 use a perfect field, a faithful local action, local
   Artinian W(k)-algebras with residue k, and conjugacy reducing to identity.
   The tangent and smoothness definitions appear on p.3. Proposition 2.4
   identifies restriction on tangents with cohomological restriction.
   Question 4.4 on p.13 requests F with tangent
   H^1(Q,Theta-sharp/Theta^N), two natural maps, factorization, and smoothness.
   It does not assume D_N or D_Q prorepresentable. Remark 4.5 adds such
   assumptions for a ring formula, and Theorem 4.9 on p.15 states them
   explicitly for a different obstruction-space result. The introduction
   likewise distinguishes the unrestricted question from later assumptions.
2. [OWR 54/2008](https://ems.press/content/serial-article-files/46200),
   printed pp.3038-3040, PDF pages 10-12. The question on p.3039 has the same
   requested factorization and tangent. Theorem 3 on p.3040 explicitly adds
   prorepresentability of D_N and D_Q. The preceding explanation about
   assumptions needed for the main result does not impose them on the question:
   the abstract itself distinguishes question and theorem.
3. [Byszewski-Cornelissen, AIF 59 (2009)](https://aif.centre-mersenne.org/item/10.5802/aif.2450.pdf),
   pp.878-879, 884, 895-896. Its category and equivalence agree with the
   2011 source. Section 2.1 explicitly allows a constant coefficient in m_A
   when the linear coefficient is a unit. It gives ring-substitution
   composition as (phi psi)(t)=psi(phi(t)). Proposition 4.1 supplies the
   same involution example and conjugacy over k[e]/e^3. The submitted proof
   independently checks that identity and does not need the proposition's
   universal-ring argument.

There is no algebraic-closedness, odd-characteristic, fixed-section,
zero-constant-term, or prorepresentability hypothesis in the questions that
would exclude this example. k=F_4 is perfect. Rings of characteristic two are
valid W(k)-algebras via W(k)->k. All ring maps used fix k, so induce the required
residue-field map. Nilpotent constants are essential here, and changing the
category to section-preserving automorphisms would change the problem.

## Exact class over the third-order ring

Let B=k[e]/(e^3), A=k[e]/(e^2), p:B->A, and j(e)=e+e^2. We have j^2=id, and j
is a local W(k)-algebra automorphism. Its action on an arbitrary element is

    j(c0+c1 e+c2 e^2)=c0+c1 e+(c1+c2)e^2.

Thus B^j=k+k e^2, and p(B^j)=k exactly.

For sigma_a(y)=(y+a)/(1+y), take a=e. The denominator is a unit, the constant
coefficient is nilpotent, and the linear coefficient is 1+e, a unit. Therefore
sigma_e is an allowed continuous automorphism of B[[y]]. Continuity also
follows directly: because its constant coefficient is nilpotent, arbitrarily
high powers of its argument tend to zero y-adically. Its matrix is

    M_e = [[1,e],[1,1]],        M_e^2=(1+e) I.

The determinant 1+e is a unit, and its reduction is the nonidentity residual
involution; hence it defines a faithful Q-action lifting the required action.
The identity-reducing coordinate change chi(y)=(1+e)y+e is represented by
C=[[1+e,e],[0,1]]. Direct multiplication gives

    M_(e+e^2) C = [[1+e,e^2],[1+e,1+e]]
                 = (1+e) C M_e.

As ordinary functions this is sigma_(e+e^2) o chi=chi o sigma_e. As ring
automorphisms, composition reverses the displayed function order, so
sigma_(e+e^2)=chi^(-1) sigma_e chi. Both conjugating directions are allowed by
the source's equivalence relation. Consequently x=[sigma_e] in D_Q(B) is fixed
by j. No relation between two merely *hull* parameters was substituted for
equality in D_Q(B).

Boundary check: this conjugacy is specific to e^3=0. The same displayed matrix
identity has an e^3 discrepancy over k[e]/e^4. The proof does not claim it at
that order and does not need it there. Its use of a third-order ring is precise.

## Nonzero tangent for arbitrary allowed conjugators

Write v=p_*x. An arbitrary identity-reducing coordinate change over A has the
form chi(y)=y+e f(y) with f in k[[y]], including an arbitrary constant term.
Suppose sigma_e and sigma_0 were conjugate. One equivalent orientation of
the conjugacy equation, expanded to first order, would require

    1/(1+y) = f(sigma_0(y)) - sigma_0'(y) f(y).

At y=0 the right side is f(0)-f(0)=0; the left side is 1. Characteristic two
does not change this contradiction. The inverse conjugating orientation
changes only a sign, which also leaves it intact. Hence v is nonzero even
against the full infinite-dimensional coordinate-change group. Restricting
conjugators to fractional-linear changes is unnecessary.

An independent cohomological calculation below identifies T D_Q with k and v
with its generator. This is an extra check, not an assumption in the argument.

## Arbitrary prorepresentable recipient: no hidden pointedness assumption

Fix any natural eta:D_Q->F with F naturally isomorphic to h_R. After transporting
eta along that natural isomorphism, write psi=eta_B(x):R->B. Naturality at j
and the actual equality j_*x=x imply j o psi=psi. This equality holds for
every r in R, so psi(R) is contained in B^j. Therefore p o psi has image in
the constant coefficient subfield k of A.

A local W(k)-algebra map R->k is necessarily the residue map r_R: R->k:
W(k) already fixes the identified residue field. Accordingly

    eta_A(v)=p o psi=(k->A) o r_R.

This is exactly the basepoint of F(A), even if R has mixed characteristic,
relations, or obstructed directions. No tangent-linearity, versality,
smoothness, dimension bound on F, or prorepresentability of D_Q was used.

Naturality at s:k->A also implies every map f:D_N^Q->F sends the base-change
class 0_N to the same residue-basepoint. The invariant functor has its genuine
basepoint: the residual restricted action is Q-fixed over k; naturality of
the Q-action preserves this under s. Explicitly, choose the constant base
changes of rho(g) as the lifts defining Q's action, and they conjugate the
constant restricted action to itself. It is unnecessary to extend f to D_N
or to identify D_N^Q with the functor represented by a hull's coinvariants.

## Independent exact computation of the restriction kernel

This computation was reconstructed to test the final contradiction without
assuming another review family's result.

For N, y=t^2/(1+t) is fixed, t satisfies t^2+yt+y=0, and the polynomial is
separable over k((y)). The extension has degree two: ord_t(y)=2, which forces
degree at least two, while the equation bounds it above. Thus the fixed field
is k((y)); intersecting with k[[t]] gives k[[y]]. The quotient generator sends
y to y/(1+y), using u(u+1)=1 in F_4.

For b(y)d/dy, the unique extension of the derivation to the separable field has
coefficient a(t)=b(y)(1+t)^2/t^2, since y'=t^2/(1+t)^2. This preserves k[[t]]
if and only if 2 ord_y b-2>=0, equivalent to b in y k[[y]]. Invariance under
N follows from uniqueness of extension; conversely an N-invariant derivation
restricts and is recovered this way. Thus Theta^N corresponds exactly to

    M=y k[[y]] d/dy.

The Q action on coefficient functions is

    T f=(1+y)^2 f(y/(1+y)).

Let z=y^2/(1+y), which is fixed by Q. Every f in k[[y]] has a unique expansion
A(z)+y B(z), with A,B in k[[z]]: successively match even and odd leading
degrees, since z^n has leading term y^(2n). Convergence is y-adic; uniqueness
uses distinct parity of the leading valuations. Such f lies in y k[[y]] iff
A is divisible by z.

Since T(h(z))=(1+y)^2 h(z), T(y h(z))=(y+y^2)h(z), and y^2=z(1+y),

    (T+1)(A+y B)=y^2(A+B).

For the full coefficient module k[[y]], the kernel is (1+y)k[[z]] and the
image is y^2 k[[z]]=z(1+y)k[[z]]. Therefore

    H^1(Q,k[[y]] d/dy) = (1+y)k[[z]] / z(1+y)k[[z]] = k.

For M the condition A in z k[[z]] makes the kernel y^2 k[[z]], while choosing
A=0 and arbitrary B shows that the image is also y^2 k[[z]]. Hence

    H^1(Q,Theta^N)=H^1(Q,M)=0.

The first-order perturbation sigma_e-sigma_0=e/(1+y) gives the cocycle
coefficient (1/(1+y))/sigma_0'(y)=1+y; its class indeed generates
the preceding k quotient.

By inflation-restriction, restriction H^1(G,Theta)->H^1(N,Theta) has zero
kernel. One can also see the relevant part directly: if a tangent cocycle's
restriction is a coboundary, first subtract that coboundary. Then its N values
vanish. The cocycle equations imply its values are N-invariant and constant
on N cosets, so it is inflated from a Q cocycle in Theta^N. The vanishing just
proved makes it a coboundary. This avoids needing freeness of higher-order
deformation fibers or prorepresentability of either action functor.

The map D_N^Q(A)->D_N(A) is a literal inclusion of sets. Thus restriction
into the actual invariant functor has zero tangent kernel as well.

## Formal smoothness: quantifier and residual-fiber audit

Suppose arbitrary natural f,g and F satisfy the proposed factorization. The
preceding arguments give

    f_A(0_N)=g_A(v)=the residue-basepoint of F(A).

Hence (0_N,v) belongs to E(A). All four action/invariant functors have one
residual point, and F(k) is a singleton, so E(k) is a singleton. The surjection
A->k is small: its kernel (e) is annihilated by m_A=(e). Smoothness in the
source definition would therefore lift this pair to w in D_G(A), with

    res(w)=0_N,       ind(w)=v.

The zero restriction forces w=0_G by the exact tangent-kernel calculation.
Induction is natural, so ind(0_G)=0_Q by base change from k. This contradicts
v!=0. The contradiction is independent of the requested tangent space of F
and independent of whether f,g realize the cohomological gamma/sigma maps.

For completeness, Theta-sharp/Theta^N is the constant coefficient quotient k
with trivial Q action. Thus H^1(Q,Theta-sharp/Theta^N)=k, matching the prescribed
tangent. That match is not needed for the stronger impossibility statement.

## Adversarial attempts and exact remaining gap

- Removing nilpotent constants invalidates sigma_e, but is a change to the
  source category, contradicted by the primary definition in AIF section 2.1.
- Allowing nonlinear or constant first-order coordinate changes does not make
  v zero: the constant-coefficient contradiction treats all f in k[[y]].
- Picking a different natural g, a different tangent dimension, a mixed
  characteristic R, or a different presentation of F does not evade the
  fixed-image argument. It uses only a natural representing isomorphism.
- Picking f on the invariant functor without an extension to D_N does not
  evade the argument. Only its actual basepoint is evaluated.
- Replacing D_Q by a hull would lose the fixed-class premise; the proof avoids
  this and establishes the premise in D_Q itself.
- A concern about source composition order disappears after translating the
  function identity into the reversed ring-substitution order. Both resulting
  coordinate changes reduce to identity.
- Taking N trivial or Q prime to p does not create this example; those are
  different data. The present N and Q are both C_2 in characteristic two.
- The additional prorepresentability hypotheses of Theorem 4.9/Theorem 3
  exclude this example. They do not occur in either question. The preprint
  must retain this exact scope distinction.

**Strongest verified result:** the submitted example excludes every
prorepresentable recipient for a smooth restriction-induction factorization
in the original unrestricted category, already at the tangent lifting problem.
**Remaining mathematical gap in this family:** none found. **Remaining program
gap:** novelty/priority, other review families, and final publication package
audit are outside this independent review's verdict.

The arithmetic checker accompanying this report is independently written and
checks the exact finite ring identities, not the submitted PASS results. Those
finite checks corroborate explicit identities; the infinite-series and
all-natural-map conclusions are justified by the derivations above.
