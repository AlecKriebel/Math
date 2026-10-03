# Independent route, fixed before any old review or computation was read

2026-10-03 10:26:31 UTC. Completion estimate: 20% of this independent audit.

Read only the literal original source_record.json and KNOWN_THEOREM.md, plus
the repository AGENTS.md. I have not read earlier reviewers, their verdicts,
their code, or their numerical outputs. The parent assigned a separate
divergence/shear audit, whose findings I have not received.

The exact hypothesis is an existing determinant-one polynomial automorphism
over A=R[t]/(t^m), R any commutative unital Q-algebra, m,n>=1. My mechanism is
the successive-jet group filtration, with exact arithmetic over nonreduced
and zero-divisor coefficient rings. The central check is that no division
by a nonunit of R or cancellation of t in A is being smuggled into the proof.

Let K_r be the subgroup of automorphisms congruent to the identity modulo
t^r. For 1<=r<m, the rth coefficient of an element of K_r is well defined
in R[Y]^n, because A[Y] is the direct sum of its m t-coefficient modules,
even when R has zero divisors. Products add this coefficient, inverses
negate it, and the determinant-one condition makes it divergence free.
Every mixed term has order at least 2r>=r+1, including r=1. Thus K_r/K_(r+1)
embeds in the additive module of divergence-free vectors. The source's
finite shear lemma would make every required coefficient the reduction of
a genuine polynomial automorphism with a genuine inverse over R[t].

The base reduction sigma_0 is an actual automorphism, because its inverse
is the reduction of the supplied inverse. Extending both maps constantly
to R[t] works for arbitrary nonlinear and wild base automorphisms; it is
not an assertion that a determinant-one endomorphism is invertible.
The factorization sigma=A_r o rho_r with A_(r+1)=A_r o Phi_r and
rho_(r+1)=Phi_r^(-1) o rho_r preserves order. This ordering needs direct
noncommuting tests. Finite r=1,...,m-1 gives a finite product, not formal
integration or a convergent infinite series.

Clarification added 2026-10-03 after the universal proof was written: K_r in
this initial route means the subgroup of the determinant-one automorphism
group, as required by the target. For unrestricted automorphisms, its jet
quotient instead embeds in all polynomial vectors, without a divergence
restriction. This clarification does not import any earlier review.

Planned falsifiers: replacing 2r>=r+1 by a stronger congruence at r=1;
using the correction on the wrong side; dropping cross terms altogether
at higher jets; demanding a tame base reduction; admitting arbitrary
Jacobian-one endomorphisms; assuming derivative zero implies constancy
without characteristic zero. Exact quotient-ring tests will include
Q[epsilon]/epsilon^2, Q[u,v]/(uv), and Q[e]/(e^2-e), multiple jets, and
nonlinear constant maps. Finite successful tests will be labelled
corroboration, not the proof for all R,m,n.
