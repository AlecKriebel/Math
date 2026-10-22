# Author approach 2: compare through annihilator multiplication

Aim: replace the obstructed lifting route by a canonical reverse-direction comparison, and determine exactly what information it can lose.

## The multiplier and its kernel

Let 0→D→B→Q→0 be an exact sequence of abelian groups and suppose eD=0. Define

    mu_e:Q→B,       b+D↦eb.

This is well-defined because e(b+d)=eb. It satisfies mu_e q=e id_B and q mu_e=e id_Q. Moreover

    ker(mu_e)=B[e]/D,

since mu_e(b+D)=0 exactly when b∈B[e]. Thus two maps f,g:S→Q have equal multiplier transforms if and only if f-g takes values in B[e]/D. Equality after multiplication is sufficient for equality before multiplication precisely when the possible difference has zero image in this kernel. A useful sufficient condition is B[e]=D.

There is a related exact sequence

    0→B[e]/D→Q[e] --theta--> D∩eB→0,
    theta(b+D)=eb.

The middle expression belongs to D because the coset is e-torsion; it is independent of the representative because eD=0. Its image is exactly D∩eB, and its kernel is B[e]/D. This separates torsion invisible to multiplication from torsion caused by a genuinely nonsplit extension.

## Application to the motivic targets

For D_{i,r}=r[A] cup K_{i+1}^M(F), one may take

    e=ord(r[A])=exp(A)/gcd(exp(A),r).

Bilinearity gives eD_{i,r}=0. For a fixed base algebra, keep this integer e fixed after field extension; it still annihilates the extended denominator even if the exponent drops. The construction commutes with field restriction and with the cycle-module operations whenever defined. Applied to sigma_r^1, or to beta_1 with r=1, it gives an unquotiented degree-four invariant.

Kahn's universal-invariant theorem (Theorem 10.7) implies that for the fixed base algebra A there is a coefficient k modulo the order of the cyclic invariant group such that

    mu_e sigma_r^1 = k c_A.

The same conclusion applies to mu_exp(A) beta_1. The existence of such coefficients is a prior result in this setting, also formulated by Wouters Proposition 4.1. Here it is used as an attempted route to the unknown comparison, not asserted as its solution. Determining the coefficients is only one part of the problem: even equality of these coefficients does not remove B[e]/D.

This obstruction is sharp at the abelian-group level. For B=(Z/2)², D=<(1,0)>, e=2, the quotient Q≅Z/2 is nonzero but mu_2=0. The zero and identity maps Z/2→Q have identical multiplier transforms. This example is a group-theoretic diagnostic only; it is not claimed to arise from a central simple algebra.

In the concrete field of approach 1, however, B=Q/Z and D=B[2]. Thus mu_2:B/D→B is an isomorphism. Kahn's theorem c_A=sigma_2^1 for exponent-two algebras and Rost's injectivity give c_A(s)=1/2. Therefore

    mu_2(sigma_1^1(s))=c_A(s),
    q_1(c_A(s))=0 != sigma_1^1(s).

The correct multiplier comparison and the failed quotient comparison coexist. This is the practical reason that saying the invariants are “the same” without naming the coefficient arrow is unsafe.

## Outcome and gap

This approach produces a canonical comparison, an exact kernel, and a criterion for recovering equality from a multiplier computation. For the general problem the scalar coefficients and the residual invariant with values in B[e]/D are uncomputed. Universality in the unquotiented target cannot erase either gap.
