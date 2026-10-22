# Attempt 5 — a finite section certificate and a concrete remaining extension

Fifth and final substantive author proof attempt. It seeks a general integer growth certificate from finite sections of G. It produces a rigorous all-n lower bound, but does not match it to a universal upper bound. The universal problem remains unsolved after 5/5 attempts.

## 1. Every abelian chief action supplies an affine section in the variety

Let T be any section of finite G, and let A/B be an abelian chief factor of T: B and A are normal in T, and A/B is a minimal nontrivial normal subgroup of T/B. Set M=A/B. It is elementary abelian, say over F_p. Write

C_T(A/B)={t in T : [a,t] in B for every a in A},
Q=T/C_T(A/B).

The T-action on M is irreducible; after dividing by its kernel, Q acts faithfully. Apply the split-section construction of attempt 2 to the group T/B with abelian normal subgroup M. It yields

M semidirect (T/A) in var(T/B), hence in var(G).

The kernel K of the action of T/A on M is C_T(A/B)/A. The subgroup 0 semidirect K is normal in this split group: K is normal in T/A and acts trivially on M. Quotienting by it yields

M semidirect Q in var(G).                                  (12)

Attempt 2 proves that the root limit of this affine group is |Q|, including Q=1. Thus

liminf a_G(n)^(1/n) >= |T/C_T(A/B)|.                        (13)

This requires neither splitting of the original extension nor a complement to the chief factor in T.

## 2. A finite integer lower certificate

For nontrivial G define lambda(G) as the maximum of the following finite set of positive integers:

- 1;
- |T| for every section T of G that is monolithic with nonabelian monolith;
- |T/C_T(A/B)| for every abelian chief factor A/B of every section T of G.

There are only finitely many sections and normal-subgroup pairs, so this is a well-defined integer. Theorem 1 of Olshanskii supplies the lower bound |T| for the second kind of section; (12)–(13) supply the third kind. Quotient and subgroup closure ensure all these groups lie in var(G). Consequently

liminf a_G(n)^(1/n) >= lambda(G).                           (14)

For lambda(G)>1, the actual proofs give c lambda(G)^n <= a_G(n) for a fixed c>0 and all sufficiently large n. When lambda(G)=1, a_G(n)>=n log p for a prime p dividing |G| supplies a stronger-than-constant lower bound.

If an independently justified upper bound of the form a_G(n)<=P(n)lambda(G)^n is available, with P a fixed polynomial, then the full original conclusion follows for G. This is a sufficient certificate, not a proof that such an upper bound always exists.

The stronger identity “potential = lambda(G)” is only a proposed route here. These arguments do not prove it, and the original question could conceivably have an affirmative answer even if that stronger formula fails.

## 3. A concrete remaining test: SL(2,3)

Take G=SL(2,F_3), of order 24. Its center Z has order 2, is its unique minimal normal subgroup, and is central. Thus the monolith action in G itself is trivial and attempt 2 does not apply. The central extension over G/Z has no complement. The included exact matrix enumeration verifies all these claims using 24 matrices and all their subgroups.

The quotient G/Z has order 12 and an abelian minimal normal subgroup of order 4 on which the quotient of order 3 acts faithfully. This is the usual A_4 quotient, but the faithful-action conclusion can be checked directly: the normal order-8 quaternion subgroup Q_8 of G maps to the order-4 monolith, and its centralizer modulo Z is Q_8 itself. Therefore attempt 2 gives quotient root limit 3.

For the original group G, section 2 gives the lower bound 3, while the central-extension estimate from attempt 4 gives upper bound 9. Thus our proven information is

3 <= liminf a_G(n)^(1/n) <= limsup a_G(n)^(1/n) <= 9.         (15)

This is not a claim that SL(2,3) is unsolved in the literature, and it is not a counterexample. It is a precise group on which the methods developed in this packet have not closed the gap. Even a proof that this particular base is 3 would not settle the universal question.

## 4. What the five attempts establish and what they do not

We have proved convergence and integrality for finite nilpotent generators, finite joins of settled cases, abelian extensions whose quotient has a nonabelian monolith, groups with self-centralizing abelian minimal normal subgroups, and split semisimple abelian extensions of settled quotients. We obtained exact limsup/liminf max rules in the split semisimple case, a quadratic-log bound for central extensions, and the finite section lower certificate (14).

None of these arguments proves a matching universal upper bound when abelian layers have nontrivial action kernels or when extension and module layers do not split. In particular, an integer lower bound and an integer upper bound do not imply an integer limit. No step establishes equality of liminf and limsup for every G.

## Final verdict

**Unsolved after 5/5 substantive author attempts.** No complete proof, counterexample, novelty claim, or first-resolution claim is made. The exact remaining task is to prove convergence and integrality for all finite-group-generated varieties or exhibit a genuine finite-group counterexample. Finite computations here validate limited structural examples only.
