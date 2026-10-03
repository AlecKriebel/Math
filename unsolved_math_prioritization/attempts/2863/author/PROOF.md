# Rank-one skein recognition: a torsion obstruction and the remaining gap

**2863 / KP-3.65. Unsolved after five approaches. No solution or counterexample is claimed.**

## 1. The problem and coefficient rings

Let Y be a closed, connected, oriented, prime 3-manifold. Put

- R0 = Z[A,A^{-1}];
- R = Q[A,A^{-1}];
- F = Q(A);
- M = S(Y,R) = S(Y,R0) tensor_R0 R;
- r = dim_F(M tensor_R F).

Problem 3.65 in the 2026 K3 problem list asks whether r=1 forces Y to be homeomorphic to S^3 or S^1 x S^2. The assertion concerns dimension after localization to F. It does not assert that M is cyclic or finitely generated over R. Coefficient extension here is valid directly from the presentation of a skein module by links and the skein relations.

The final Detcherry–Kalfagianni–Sikora paper [DKS] asks the stronger question r>=2 for every other prime Y, as **Question 10.5**, journal p. 43 (preprint v3, p. 42). K3's reference to Question 10.3 is a numbering mismatch. Rank-one recognition alone does not exclude r=0; this note keeps these two questions distinct.

The following is a conditional reduction, not an unconditional recognition theorem:

> If r=1 and Y is not S^3, the torsion submodule T of M has a nonzero fiber T/p_N T for **every** odd positive N, where p_N=Phi_{2N}(A). This conclusion does not require a decomposition of M into cyclic modules.

In particular, rank one together with the absence of p_N-torsion for even one such N forces S^3. The unresolved step is to exclude the indicated all-orders torsion behavior for prime manifolds other than S^1 x S^2, or to bypass this obstruction by another argument.

## 2. Precisely stated external inputs

We use these established results; the arguments below do not reprove their quantum-topological or gauge-theoretic foundations.

1. [DKS, Theorem 2.1]: for a primitive root zeta of order 2N, N>=3 odd, the complex skein specialization has dimension at least d whenever X(Y), the set of SL(2,C) characters, contains d distinct points. At N=1 the same assertion follows from the character-ring description of S_{-1}(Y) and evaluation on d distinct closed points. The latter ring need not be reduced.
2. [Z, Theorem 9.4]: an integral homology 3-sphere other than S^3 admits an irreducible SL(2,C) representation.
3. For the separate route in Section 8 only, [DKS, Theorems 1.7 and 9.1] give nonvanishing of the empty skein for a rational homology sphere and an F-linear evaluation map using quantum invariants at odd root orders.

The detailed reading and dependency limits are in SOURCE_GATE.md. The substantive algebra in Sections 3–7 is proved here.

## 3. An elementary specialization lemma with no finite-generation assumption

Let R be a principal ideal domain, F its fraction field, p a prime element, k=R/(p), and M any R-module of finite generic rank r. Let

T = {m in M : f m=0 for some nonzero f in R}, and Q=M/T.

Then Q is torsion-free and has rank r. There is an exact sequence

0 -> T/pT -> M/pM -> Q/pQ -> 0,                         (1)

and

 dim_k(Q/pQ) <= r.                                    (2)

**Proof of (1).** The only point beyond right exactness is injectivity on the left. If t in T equals p m, choose nonzero f with f t=0. Then (fp)m=0, so m lies in T. Consequently T intersect pM = pT, as required. This proves (1) without assuming a splitting of M or invoking a finitely generated structure theorem.

**Proof of (2).** If r+1 residue classes in Q/pQ were independent, lift them to q_1,...,q_{r+1} in Q. Their images in F tensor_R Q are dependent. Clear denominators in a nonzero dependence. Because Q is torsion-free, this gives a relation sum a_i q_i=0 in Q, with coefficients a_i in R not all zero. Divide the coefficients by the largest common power p^e. Cancellation is valid because Q is torsion-free. At least one resulting coefficient is not divisible by p. Reducing modulo p gives a nonzero k-linear dependence among the chosen residue classes, a contradiction. Therefore no independent family of size r+1 exists.

For each nonnegative integer d with dim_k(M/pM)>=d, (1) and (2) imply

 dim_k(T/pT) >= max(0,d-r).                            (3)

This is understood as an inequality for every finite d if M/pM is infinite-dimensional. In that event T/pT is infinite-dimensional too. No claim about uncountable cardinal equality is needed.

### The distinction between torsion and its fiber

If T/pT is nonzero, M contains a copy of R/(p). Indeed, choose t in T whose class modulo pT is nonzero, and let (f) be its annihilator. If f and p were coprime, a Bezout identity would give t in pT, a contradiction. Write f=p^e g, e>=1, with g coprime to p. Then u=p^{e-1} g t is nonzero, p u=0, and R u is isomorphic to R/(p).

The converse is false. In D=R[1/p]/R, there is nonzero p-torsion but pD=D, so D/pD=0. Also R/(p^e) contributes **one** dimension over k to its specialization, regardless of e; its R-primary length is e. We consistently count T/pT, not the total length of the p-primary torsion.

## 4. Application to roots of unity

Return to R=Q[A,A^{-1}] and p_N=Phi_{2N}(A). This is a nonunit irreducible element; k_N=R/(p_N) embeds in C by A -> zeta, for each primitive root zeta of order 2N. Base change gives

 S_zeta(Y) = (M/p_N M) tensor_{k_N} C.

Extension of fields preserves vector-space dimension, including the assertion of containing d independent vectors for every finite d. The first input of Section 2 and (3) therefore yield:

**Proposition.** If M has finite generic rank r and X(Y) contains d distinct characters, then, for every odd positive N,

 dim_{k_N}(T/p_N T) >= max(0,d-r).                     (4)

If X(Y) is infinite, every one of these torsion fibers is infinite-dimensional.

This argument generalizes the elementary specialization step, not the quantum theorem that supplies the lower bound. At N=1, p_1=A+1 and the character-ring description supplies that bound directly. At higher odd N it is exactly the root-of-unity input [DKS].

## 5. When does a closed 3-manifold have only one character?

**Lemma.** For a closed, connected, oriented 3-manifold Y, X(Y) has one point if and only if Y is S^3.

**Proof.** The forward implication uses [Z]. First suppose H=H_1(Y;Z) is nonzero. It is a finitely generated abelian group, so it has a nontrivial homomorphism lambda:H -> C*. Compose the abelianization map with

 h -> diag(lambda(h), lambda(h)^{-1}).

For some h, lambda(h) is not 1. Its trace differs from 2, because z+z^{-1}=2 with z nonzero implies (z-1)^2=0 and hence z=1. Thus this character differs from the trivial character, contradicting the singleton assumption.

We have proved H_1(Y;Z)=0. Poincare duality and the universal coefficient theorem now show that Y is an integral homology sphere. If Y were not S^3, [Z] would give an irreducible representation. Its character is different from that of the trivial representation: characters distinguish semisimple representations, and an irreducible two-dimensional representation cannot have trivial semisimplification. This is the usual SL(2,C) character correspondence used in [DKS, Section 1]. It contradicts the singleton assumption. Conversely pi_1(S^3) is trivial, so its character set is a singleton. QED.

The primeness assumption was not needed for this lemma.

**Corollary (rank-one torsion obstruction).** If r=1 and Y is not S^3, then T/p_N T is nonzero, and M contains R/(p_N), for every odd positive N.

**Proof.** The lemma gives two distinct characters. Apply (4) with d=2 and then the last part of Section 3. QED.

Consequences, each still conditional on r=1:

- If T/p_N T=0 for one odd N, then Y is S^3.
- It suffices that M contain no submodule R/(p_N) for one odd N.
- It suffices that T be finitely generated: a product f of annihilators of a finite generating set kills T, and only finitely many distinct cyclotomic primes divide f. Choose an odd N outside that finite set. Multiplication by p_N is then invertible on T by Bezout, so T/p_N T=0.
- In particular this proves the known tame and finitely generated cases. Tameness includes the absence of one such cyclic submodule. No assertion that generic rank one implies any of these additional conditions has been made.

S^1 x S^2 is therefore necessarily on the torsion side of the obstruction. Its generic rank-one behavior, recorded in K3 from Hoste–Przytycki, does not contradict the corollary, which concludes S^3 only when the extra torsion hypothesis holds.

## 6. Quantitative abelian-character controls

These observations make (4) explicit without computing irreducible characters.

If H_1(Y;Z)=H is finite, the number of diagonal characters is

 d_ab = (|H| + |H[2]|)/2,                             (5)

where H[2]={h:2h=0}. To prove this, diagonal characters are indexed by homomorphisms lambda:H -> C*, with lambda and lambda^{-1} having the same trace. Those are the only identifications. Indeed, if lambda has some value a not equal to +/-1, replace a second homomorphism mu by its inverse if necessary so that mu(g)=lambda(g)=a at such a g. Equality of traces at h says mu(h) is lambda(h) or its inverse. Equality at gh forces

 (a-a^{-1})(lambda(h)-lambda(h)^{-1})=0

in the inverse case, so mu(h)=lambda(h) in that case too. If lambda takes only values +/-1, equality of each trace already determines mu=lambda. Thus the identifications are precisely inversion orbits.

The dual of a finite abelian group has |H| elements and |H[2]| inversion-fixed elements. Counting one-point and two-point orbits proves (5). Therefore at generic rank one,

 dim_{k_N}(T/p_N T) >= (|H|+|H[2]|)/2 - 1

for every odd N. When H is trivial, this particular bound is zero; [Z] supplies the extra character for a nontrivial homology sphere.

If b_1(Y)>0, the quotient H_1(Y;Z) -> Z gives infinitely many characters by sending 1 to z in C*, modulo z <-> z^{-1}. Hence the torsion fibers in (4) are infinite-dimensional whenever r is finite.

The mod-2 homology grading is not a replacement for these bounds on the generic module. The skein relations preserve link classes in H_1(Y;Z/2), so the module splits into corresponding summands. It does not follow that every summand remains nonzero after localization. The known S^1 x S^2 example already rules out a universal assertion r >= |H_1(Y;Z/2)|.

## 7. Algebraic examples showing the exact limitation

Let p_N=Phi_{2N}(A), N positive odd, and form the abstract module

 E = R direct-sum (direct-sum over odd N of R/(p_N)).

Then E tensor_R F is F. At every primitive root of order 2N, precisely the N-th torsion summand survives, so its specialization has dimension 2. Other summands vanish because distinct cyclotomic polynomials are coprime. Thus generic rank one is compatible with all the root-of-unity dimension bounds for a hypothetical character set of size 2.

There is no claim that E is realized as a manifold skein module. It is an algebraic counterexample to an attempted implication from generic rank and specialization dimensions alone. It is not a counterexample to KP-3.65.

Likewise,

 E_infinite = R direct-sum (direct-sum over odd N and j>=1 of R/(p_N))

has generic rank one and infinite-dimensional fibers at all of these roots. It cannot be ruled out by the character-count inequalities alone. Even the finitely generated example R direct-sum R/(A+1) already invalidates the inference that a rank-one generic fiber forces a one-dimensional fiber at A=-1. That example is not compatible with a two-character lower bound at all other odd orders, which is why E, rather than that finite example, is the appropriate all-orders control.

For a torsion-free countercontrol, R[1/p] has generic rank one but zero fiber at p. Consequently one cannot replace the inequality dim(Q/pQ)<=r in Section 3 by equality without additional hypotheses.

## 8. Quantum-evaluation and Dehn-filling routes

For a rational homology sphere, the empty skein is nonzero by the third input of Section 2. If its generic rank is one, every fixed skein L is f_L(A) times the empty skein for some f_L in F. Applying the F-linear evaluation map gives

 RT_zeta(Y,L) = f_L(zeta) RT_zeta(Y,empty)

at all but finitely many of the odd-order roots under consideration. Thus one route to refuting rank one for a particular Y is to find a fixed L for which no such rational function exists. No uniform construction of such an L for all the remaining prime manifolds is obtained here.

Finite root data cannot prove that rational-function nonexistence. For any finite set of distinct cyclotomic primes p_i and any compatible values given by residues a_i in R/(p_i), the Chinese remainder theorem produces a polynomial f in Q[A] satisfying f=a_i modulo each p_i. This proves exact interpolation for any such finite collection, without asserting compatibility for arbitrary complex assignments.

Nor may injectivity of the evaluation map be assumed. Kitaeff [K, Theorem 1.10] proves a nonzero kernel element even in a fixed homology sector for a torus mapping torus. That is a limitation of the method, not a rank-one example.

The Dehn-filling finite-generation method provides a real but restricted positive result. [DKS, Theorem 4.3] proves finite generation over Z[A,A^{-1}] for figure-eight fillings away from slopes 0,+4,-4, and for (2,2n+1)-torus-knot fillings away from slopes 0,4n+2. Every rank-one member of those finite-generation classes is S^3 by Section 5. The proof relies on peripheral annihilators with unit corner coefficients over the Laurent polynomial ring; invertibility merely over F does not suffice. Rank-one localization gives no uniform control of denominators or annihilators for the whole integral module. The exceptional slopes and general prime manifolds cannot be discarded by this argument.

## 9. Honest conclusion

The five approaches establish a necessary all-orders torsion-fiber condition, recover conditional recognition, and exhibit exact algebraic obstructions to removing the hypotheses by specialization alone. No closed prime manifold outside the stated exceptions has been proved to have rank one, and no proof excludes all such manifolds. The disposition remains **unsolved**, with five substantive approaches recorded. The elementary deductions are not claimed as a new solution, a novel published theorem, or a priority claim.

## References

[K3] R. I. Baykur, R. C. Kirby, and D. Ruberman, *K3 — A New Problem List in Low-Dimensional Topology* (2026), Problem 3.65, pp. 178–179. Author-posted source: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf

[DKS] R. Detcherry, E. Kalfagianni, and A. S. Sikora, *Kauffman bracket skein modules of small 3-manifolds*, Advances in Mathematics 467 (2025), 110169. https://doi.org/10.1016/j.aim.2025.110169 ; version used for local proof reading: https://arxiv.org/abs/2305.16188v3

[Z] R. Zentner, *Integer homology 3-spheres admit irreducible representations in SL(2,C)*, Duke Mathematical Journal 167 (2018), 1643–1712. https://doi.org/10.1215/00127094-2018-0004 ; author manuscript: https://zentner.app.uni-regensburg.de/splicing.pdf

[K] E. Kitaeff, *The Gilmer-Masbaum map is not injective on the skein module*, New York Journal of Mathematics 32 (2026), 423–435. https://nyjm.albany.edu/j/2026/32-20.html
