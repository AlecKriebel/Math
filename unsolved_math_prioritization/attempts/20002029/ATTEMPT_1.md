# Attempt 1: the undifferentiated-Schouten ideal

## Target and outcome

Extend the derivative-free test to expressions with derivatives, without confusing locally conformally flat testing with arbitrary metric jets. This attempt proves a general vanishing lemma and a critical-weight length bound, but not the full problem.

Use P=(Ric-Jg)/(n-2), J=R/[2(n-1)], and the exact law

    P_hat = P - Hess(u) + du tensor du - (|du|^2/2)g,  g_hat=e^(2u)g.

All complete contractions below use the metric; no orientation tensor is introduced.

## Vanishing lemma

Suppose I is a scalar conformal invariant and admits an expression in which every summand contains an undifferentiated factor P (other factors may be arbitrary covariant derivatives of P). Then I=0.

At any chosen point x, prescribe u(x)=0, du(x)=0 and Hess(u)(x)=P(x). Such a smooth function exists by prescribing its finite Taylor polynomial and multiplying by a cutoff. The displayed law gives P_hat(x)=0 and g_hat(x)=g(x). Every summand of the specified formula vanishes at x, irrespective of the transformed higher jets. Conformal covariance gives I_g(x)=I_hat(x)=0. Since g and x were arbitrary, I vanishes identically. No integration, field equation, or conformal flatness assumption is used.

This concerns a representative all of whose summands lie in this ideal. It does NOT justify deleting individual P-containing terms from a general invariant expression: those terms can participate in cancellations of conformal variations.

## Critical-weight consequence

A contraction of L factors nabla^(r_s)P has constant-rescaling weight

    -2L - sum_s r_s.

At weight -n, a monomial with no undifferentiated P has all r_s>=1, hence n>=3L. Therefore, if a candidate invariant has a representative whose every monomial has L>n/3, it is identically zero. Equivalently, restriction to a pointwise gauge P=0 annihilates all such monomials, and a nonzero invariant must retain at least one monomial of length L<=floor(n/3).

Examples: the entire length >=3 sector vanishes in n=8; length >=4 in n=10; length >=5 in n=12. These statements are about candidates wholly contained in the specified sector. They are not an assertion that the short part of an arbitrary invariant is separately invariant.

## Why this does not solve the problem

For n=6, contractions of two copies of nabla P and one copy of nabla^4 P survive this bound. For n=8, products involving nabla^2 P survive. Higher ordered derivatives retain Cotton and curvature-commutator information after P=0. The construction does not make all Schouten jets vanish. The Bach-norm example in dimension four is an explicit warning against that false extension.

## Prior work and verification

The gauge is a finite-order special case of Fefferman–Graham, The Ambient Metric, Proposition 8.4 and its following remark (Schouten normalization). This elementary consequence may be standard; no novelty claim is made. The proof is independent of the cached conformally-flat realization and works at every metric jet. All quantifiers and the representative-versus-summand distinction have been checked.
