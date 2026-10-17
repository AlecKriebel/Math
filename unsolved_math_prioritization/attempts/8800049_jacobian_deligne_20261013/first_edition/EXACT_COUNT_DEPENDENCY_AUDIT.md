# Exact polarized-count dependency audit

**Disposition: PASS with the explicit ideal-isomorphism guard below.** The integer used by the counted-model bridge is unconditionally computable for every promised ordinary absolutely simple degree-six input. It counts actual principally polarized Fq-isomorphism classes, without automorphism weights. There is no Bass, maximal-order, odd-characteristic, or GRH hypothesis. This is a targeted dependency audit within the existing first pass, not an implementation or a new proof attempt.

## 1. Precisely inspected primary dependencies

Write **P** for Marseglia, *Computing square-free polarized abelian varieties over finite fields*, [arXiv:1805.10223v3](https://arxiv.org/abs/1805.10223v3), Math. Comp. 90 (2021), 953–971. PDF page numbers below refer to that 18-page version.

- P, conventions p.3: morphisms are over the specified base field.
- P, Remark 4.1 p.5: a simple ordinary class has irreducible Frobenius polynomial. The square-free classification applies.
- P, Theorem 3.2 p.5, Theorem 4.3 and Corollary 4.4 p.6: the categorical equivalence identifies Fq-isomorphism classes with all fractional R-ideal classes.
- P, Corollary 4.6 pp.6–7: the endomorphism ring and automorphisms of the object represented by I are S=(I:I) and S^×.
- P, Theorem 5.2 p.8 and Theorem 5.4 pp.9–10: the dual ideal is bar(I)^t; principal polarization means aI=bar(I)^t, bar(a)=-a, and Phi-positivity. Polarized isomorphism uses a=bar(u)a'u.
- P, equation (5.1) p.9, Algorithm 2 and Theorem 6.3 p.11: the computable CM type uses one prime above p in the splitting field and a compatible complex embedding.
- P, Algorithm 1 pp.10–11 and Algorithm 3/Theorem 6.4 pp.11–12: enumeration interfaces. P, Remark 6.5 p.13: the principal case has S=bar(S).

Write **I** for Marseglia, *Computing the ideal class monoid of an order*, [arXiv:1805.09671v3](https://arxiv.org/abs/1805.09671v3), J. London Math. Soc. 101 (2020), 984–1007. Its 20-page PDF was independently retrieved for this audit. The relevant results are Proposition 3.7 p.5 (Bass simplification), Remark 3.8 pp.5–6 (arbitrary-order units/Picard groups), Proposition 4.1 p.6 and Corollary 4.5 p.7 (weak equivalence and ideal isomorphism), Theorem 4.6 pp.7–8, Proposition 5.1 p.8 (complete enumeration), and Algorithm 5/Theorem 6.5 p.12 (exact isomorphism).

For unconditional number-field computability use Lenstra, *Algorithms in algebraic number theory*, [arXiv:math/9204234v1](https://arxiv.org/abs/math/9204234), Theorem 5.4 and the following construction, PDF pp.23–24. These give finite bounded-height S-unit enumeration and the kernel/cokernel construction of units and the class group. Its separate complexity Theorem 5.5 is unnecessary.

## 2. All ideal classes, with an explicit disjoint enumeration

Let K=Q[x]/(h), pi=x mod h, and R=Z[pi,q/pi]. The promised input makes K a sextic CM field and h square-free. Full R-ideals are full integral lattices in K, including those noninvertible in their own multiplicator ring.

Here is a precise realization of the ICM call, using I's theorem statements rather than interpreting abbreviated pseudocode beyond its stated objects:

1. Compute O_K. Enumerate the finitely many over-orders S of R through subgroups of O_K/R, testing ring closure.
2. For each S put f=(S:O_K). Enumerate the finite collection of S-stable additive lattices f subseteq J subseteq O_K. Retain only (J:J)=S.
3. Deduplicate these lattices by the exact weak-equivalence test 1 in (J:J')(J':J).
4. Multiply each retained weak representative by one representative of each class in Pic(S).

Every ideal class appears, by I, Proposition 5.1 with T=O_K. The action in Theorem 4.6 is free with precisely the weak classes as its orbits. The multiplicator-ring filter makes the different S-lists disjoint. Thus this yields each ideal class exactly once. It does not replace the answer by the union of Pic(S), a simplification justified only for Bass orders.

## 3. Defensive degree-one ideal-isomorphism guard

For one representative I let H=bar(I)^t, S=(I:I), and C=(H:I). The following exact procedure should be explicit in the synthesis:

1. Test C(S:C)=S. If false, reject I as having no principal polarization.
2. Decide whether the invertible S-ideal C is principal. If not, reject. Otherwise compute x0 with C=x0S.
3. Test x0I=H as equality of integral lattices. If false, reject. If true, continue with all multipliers x0S^×.

Equivalently, use I's full ideal-isomorphism Algorithm 5, including its weak-equivalence test, and verify the returned equality.

**Why the guard loses nothing.** If aI=H, then C=(aI:I)=aS. Therefore every genuine solution passes invertibility and principality. All generators of C differ by an S-unit, which preserves I. Consequently if x0I differs from H, no other generator can repair it. Conversely equality gives an actual isomorphism, and every isomorphism I to H is exactly x0u for u in S^×.

P's polarization pseudocode states a principal-colon condition, whereas the cited I, Corollary 4.5 explicitly assumes weak equivalence. Recording the equality above removes any dependence on how that preliminary check is understood. This audit does **not** assert that the published algorithm fails on its special conjugate-dual inputs.

## 4. Complete finite unit filtering

Success of the guard forces S=(H:H)=bar(S). Put U=S^× and D={u bar(u):u in U}. Then D is a subgroup of U, and every element of D is totally positive in the real subfield.

The group Q=U/D is finite. Indeed, u/bar(u) is an algebraic-integer unit all of whose complex absolute values are one, hence a root of unity. If w is the order of the roots of unity in K, then

u^(2w)=(u bar(u))^w.

Thus Q is a finitely generated abelian group of exponent dividing 2w. Compute its finite coset representatives and, for each representative u, test

a=x0u, bar(a)=-a, and Im(phi(a))>0 for every phi in Phi.

Both tests are invariant under D: multiplication by a totally positive real norm preserves total imaginarity and every prescribed imaginary sign. Hence filtering one representative per Q-class produces exactly one representative of every principal-polarization orbit. There is no need to assume that I is invertible.

For an especially conservative implementation, a finite generating set g1,...,gt for U suffices: enumerate all products of the gj with exponents from 0 through 2w-1, then remove duplicates modulo D. Norm membership is decidable without approximate logarithmic equality: for b, first test total reality and positivity, then enumerate v in the lattice S with v bar(v)=b. At each complex place, |phi(v)| is fixed as sqrt(phi(b)), so this is a bounded finite lattice search. Finally test v in S^× and the norm identity exactly. This gives a terminating duplicate test.

## 5. Unconditional arithmetic and CM choices

The standard exact number-field operations can all be implemented with certified finite arithmetic. Lenstra's bounded-height construction gives a specific unconditional route to full units and the maximal-order class group; I, Remark 3.8 supplies the finite conductor-quotient passage to any order S. To decide principality of an invertible S-ideal, use its class in the fully computed Pic(S). In the zero class, exhaustive enumeration for a generator terminates because one exists; a proposed generator is checked by lattice equality. Invertibility is itself the displayed colon/product equality.

One can alternatively make the generator decision wholly bounded. Choose a full-rank subgroup of S-units. Its logarithmic fundamental parallelepiped bounds the embeddings of a possible generator after multiplication by one of those units; the absolute norm of a generator is fixed by the lattice covolume ratio. Enumerate the resulting finite lattice box and test aS=C. Full-rank independent units can be found by enumeration and a certified nonzero logarithmic minor; Dirichlet's theorem ensures that this search stops. No exact decision about a vanishing transcendental logarithmic expression is needed.

The CM type is fixed once by P's Algorithm 2, not varied to force positivity. Splitting fields, primes above p, and conjugate algebraic embeddings are finite exact data. Positive valuation is a prime-ideal membership computation. The three imaginary signs are signs of real algebraic numbers after an exact test bar(a)=-a. Since a is nonzero, none of those imaginary parts vanishes. Certified real-root isolation decides each sign. The arbitrary compatible choice is part of the Deligne equivalence; it does not introduce additional classes to sum over.

A fast implementation is not the proof of termination. In particular an uncertified GRH class group cannot be used as a stopping certificate, and merely placing a potentially nonterminating certification wrapper around a heuristic computation is insufficient. The unconditional finite constructions above are enough; no claim about their practicality is made.

## 6. Why the result is the required unweighted Fq count

For each ideal representative, the preceding procedure counts the orbits of principal polarization morphisms under all Fq-automorphisms of its underlying object. The ideal equivalence is R-linear, therefore Frobenius-compatible; it is not a geometric equivalence or an additional quotient by automorphisms of K. Distinct unpolarized Fq-classes cannot become isomorphic as polarized Fq-objects. Summing the orbit cardinalities over the complete ICM list therefore gives

N(q,h)=sum_[I] #(principal-polarization multipliers on I modulo S^×).

Each class contributes one, independently of the size of its stabilizer. Every loop is finite or has the stated existence-based stopping proof. No step excludes p=2. This establishes exactly the finite unweighted integer needed to stop the model enumeration.

**Scope:** The audit verifies the arithmetic stopping certificate and its source hypotheses. It does not validate the later projective-model enumeration or geometric Jacobian-recognition steps, does not execute a nontrivial numerical instance, and makes no originality claim.
