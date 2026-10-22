# Relation to prior methods: a bilateral route to the same conclusion

Alec Kriebel, 22 October 2026, v1.0.0. CC BY 4.0. This supporting deduction makes the close corollary relationship explicit. It is not a claim of a new stabilization mechanism, nor a quotation of a general theorem stated verbatim by Liu. The paper's direct unilateral proof does not depend on this second route.

DKW Lemma 5.1.8, Theorem 5.1.10 and Remark 5.1.11 supply coefficient stabilization and its bounded-vector extension. Liu, arXiv:1505.02215v1 §6.2, Lemma 6.8 and Proposition 6.10, supplies the related bilateral past/future identity and normality on each fixed future von Neumann algebra. His 'non-degenerated' hypothesis concerns faithfulness of the GNS representation, not faithfulness of the state. His displayed setup concerns bilateral bounded variables and the specified polynomial generation. The block-of-elements and bounded-net argument below supplies the arbitrary-unital-A extension and the original-representation bridge rather than silently attributing them as his stated DKW answer.

## Bilateral law and spatial shift

Let A, the finite-permutation-symmetric state psi, and the original GNS representation be as in the paper. Choose any bijection b:Z->N and pull psi back to the universal unital free product indexed by Z. Every finite partial relabeling extends to a finite permutation. Symmetry therefore implies that the restriction to positive copies has exactly the original joint law, independently of b; it also implies invariance under the bilateral shift on finite words. Norm density extends this invariance to the entire universal C*-algebra. The shift preserves the GNS null space and inner product, so in the bilateral GNS space K, with cyclic vector Omega, it is implemented by a unitary fixing Omega. Its automorphism alpha extends normally to the represented bilateral von Neumann algebra. No faithful state is needed.

Write C_k^Z=C*(positive-future copy images with j>k), for k in Z, and V_k=(C_k^Z)'', on K. Put M_+=V_0 and T_Z=intersection_{k>=0}V_k. All these are unital concrete algebras on K. Let finite-word vectors mean finite linear combinations of vectors w Omega, where w involves finitely many indices and arbitrary elements of A. Their span is dense, even when A or K is nonseparable.

## A normal expectation on each fixed future algebra

Fix k. For a finite family of finite-word test vectors choose n at least every test index. Choose L>=0 so k+L>=n. If a is a future polynomial from C_k^Z, then for every l>=L the finite index transport from its support shifted by L to its support shifted by l extends to a finite permutation supported strictly after n. It fixes all test words and transports whole indices, including every repeated occurrence. Thus

    <alpha^l(a) eta,zeta> = <alpha^L(a) eta,zeta>.

For a in V_k, norm-ball Kaplansky supplies bounded future-polynomial/C*-algebra approximants. Each fixed alpha^l and alpha^L is normal, hence WOT-continuous on bounded sets. The same coefficient identity therefore holds for every a in V_k. Notice that L depends only on k and the test indices, not on a. Uniform boundedness of alpha^l(a) and density of finite-word vectors extend the Cauchy property to every pair of vectors in K. A WOT limit E_k(a) exists, with norm at most ||a||. For any future cutoff j, alpha^l(a) belongs to V_j for sufficiently large l, so its WOT limit lies in T_Z. The limits agree on overlapping future algebras.

Every tail element is fixed by alpha. Indeed, for any finite-word test family with indices<=n, a tail element belongs to V_n. The same coefficient identity, now for shifts0 and1 in that future algebra, gives <alpha(a)eta,zeta>=<a eta,zeta>. Density and boundedness give alpha(a)=a. Consequently E_k fixes T_Z. As a WOT limit of unital completely positive maps, E_k is unital completely positive. It is a contractive projection onto the C*-subalgebra T_Z and hence a conditional expectation, equivalently by the usual norm-one projection theorem (or the multiplicative domain of a unital CP map fixing T_Z).

It is normal on each V_k. To see this without a separability/sequential assumption, let a_lambda be a bounded WOT-convergent net in V_k with limit a. On each finite-word test pair the coefficient of E_k(a_lambda) equals that of one fixed normal map alpha^L(a_lambda), with the same L for all lambda. These coefficients converge to those of E_k(a). The uniform bound extends convergence to arbitrary vector pairs. In particular E_k preserves suprema of bounded increasing positive nets, which is normality. This is the bounded-net extension of the prior Liu mechanism, not a normality assertion on the entire bilateral algebra.

In particular E_+=E_0 is normal on M_+ and fixes T_Z. Normal Kaplansky approximation in M_+ gives

    T_Z = WOT-closure E_+(C_0^Z),

with inputs and outputs of norm at most the norm of the chosen tail target. The WOT/ultraweak passage here is valid on bounded sets: approximate any trace-class functional by finite sums of vector coefficients, using the uniform norm bound.

## Restriction to the original representation and tail lifting

Let H_+=closure(C_0^Z Omega). It reduces M_+: its projection commutes with the unital C*-algebra and hence its bicommutant. Restriction to H_+, identified with the original GNS Hilbert space by equality of the positive joint law, gives a normal surjective *-homomorphism

    rho:M_+ -> M_original.

A normal *-homomorphism has von Neumann-algebra image, by its central-kernel decomposition. Its image here is the algebra generated by the original positive copies. Similarly,

    rho(V_N) = C_N_original''

for every N>=0: both sides are the von Neumann algebra generated by the corresponding future images. Normality and bounded Kaplansky approximation justify this generator statement; it is not a statement about an arbitrary nonnormal C*-quotient.

It does not follow formally that rho commutes with arbitrary intersections. Prove the needed instance. Given t in T_original and r=||t||, the sets

    K_N={s in V_N: ||s||<=r and rho(s)=t}

are nonempty, nested, and ultraweakly compact subsets of the norm-r ball of M_+. Nonemptiness with the exact norm bound follows from the central-kernel decomposition of the normal surjection rho restricted to V_N: its complementary central summand is isomorphic, isometrically, to C_N_original''. Compactness uses the ultraweak compactness of a von Neumann norm ball and normality of rho. The finite-intersection property gives s in intersection_N K_N. Thus s belongs to T_Z, ||s||<=r and rho(s)=t. Conversely rho(T_Z) is contained in T_original. We have proved rho(T_Z)=T_original.

For x in C_0^Z, shift covariance and normality of rho on bounded nets give

    rho(E_+(x))
      = WOT-lim_l rho(alpha_Z^l(x))
      = WOT-lim_l alpha_original^l(rho(x))
      = F_original(rho(x)).

The positive C*-image rho(C_0^Z) is exactly pi_original(free product): it is norm closed and has the same copy generators. Apply bounded normal Kaplansky approximation to a tail lift s. Its approximants x_lambda in C_0^Z have norm at most ||s||<=||t||. Then F_original(rho(x_lambda))=rho(E_+(x_lambda)) tends WOT to t, proving the paper's bounded density and hence D''=T again.

The last identity is only asserted on C*-inputs. E_+ need not descend through rho on all M_+. A blanket normal-descent assertion would contradict the possible nonnormality of F in the original representation; no such assertion is used here.

## Source versions and exact scope of the contribution

The current DKW arXiv-v3 response carries internal August 2021 headers although arXiv labels v3 September 2014; it is not authenticated as identical to historical 2014 or publisher bytes. The inspected Liu lemma numbers refer to arXiv:1505.02215v1. Both AMS full-body routes returned403, and the dissertation body was not recovered. DKW's quantum-symmetric case and normal-expectation cases are prior. This deduction does not establish D subset pi(free product), equality of the recursive C*-algebra with the first stage, arbitrary fixed-point/tail equality, or an unrestricted normal extension of F.

A bounded project source audit found no authenticated earlier publication of the full arbitrary-A generation answer, but no worldwide-firstness, historical novelty or continuing-openness certificate follows. The full theorem is best described as a short general deduction of the prior stabilization/future-expectation method. Both catalog aliases 30003208 and 30002897 are one question. The proof was already public in project PR1329 on 13 October 2026; this note is dated 22 October 2026 and is not backdated. Extensive AI involvement and unrefereed status are disclosed in the paper and README.
