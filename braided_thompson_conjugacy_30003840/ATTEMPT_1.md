# Attempt 1 — Restricting the ambient conjugator

**Aim.** Try to inherit conjugacy decidability from the ambient group V_br. **Outcome:** an exact transporter reduction, and a concrete obstruction to simply reusing ambient conjugacy. The target remains unresolved.

Write G = V_br, pi: G -> V, K = ker(pi), Q = F or T and H = pi^(-1)(Q). These definitions and the announced ambient theorem are credited in SOURCE_GATE.md.

## 1. The exact missing test

Suppose a,b belong to H. First run the ambient conjugacy decision procedure. If they are not conjugate in G, they are not conjugate in H. If they are, find one h in G with b = h a h^(-1), by enumerating G-words and using the effective word problem. This enumeration terminates because the ambient decision has already answered yes.

**Proposition 1.** With this h,

    a and b are conjugate in H
      iff pi(h) pi(C_G(a)) intersects Q.

**Proof.** Every ambient conjugator from a to b is h c for some c in C_G(a): if x a x^(-1)=b=h a h^(-1), then h^(-1)x commutes with a. Conversely h c is a conjugator for every such c. It lies in H exactly when pi(h) pi(c) belongs to Q. This proves both directions. The multiplication side is important: the coset is h C_G(a), not a guessed arbitrary coset. ∎

Membership of a given element in H is easy: compute its braid permutation and check that its tree-permutation-tree map preserves linear or cyclic order. But testing every element of the infinite coset is only a positive semidecision. Ambient decidability plus subgroup membership does not supply a terminating negative test.

Also, pi(C_G(a)) is contained in C_V(pi(a)), but equality has not been shown and must not be substituted. A quotient element commuting with pi(a) need not admit a lift commuting with the braided element a. This is exactly where invisible braid data can enter.

## 2. A concrete failure of conjugacy inheritance for F_br

Fix any rooted binary tree T with three leaves and identify B_3 with the subgroup of G consisting of (T,beta,T). Let

    a = (T, sigma_1^2, T),
    h = (T, sigma_2, T),
    b = h a h^(-1).

Both a and b lie in K, because their braids are pure. They are conjugate in G by construction.

For a pure braid p, let L_ij(p) be half the signed number of crossings between the strands that start at i and j. This is an integer and an additive homomorphism on PB_n. Conjugation by a general braid permutes the pair labels. Thus the only nonzero pairwise linking number of sigma_1^2 is L_12=1, while that of sigma_2 sigma_1^2 sigma_2^(-1) is L_13=1.

Zaremsky's established character omega_0 on F_br records the linking of the first and last strands. It is well defined under strand cloning: splitting an endpoint strand preserves its linking with the opposite endpoint, and splitting an interior strand changes neither endpoint. It is additive because the intermediate braids are pure and matching refinements preserve these endpoint strands. Consequently it is invariant under conjugation in F_br.

Here omega_0(a)=0 and omega_0(b)=1. Therefore a and b are **not** conjugate in F_br, despite being conjugate in V_br. This is a witness against the proposed inheritance step, not against decidability of F_br itself. The witness and the character argument work for any shape of T.

## 3. What would complete this route

A uniform algorithm for the coset-intersection problem in Proposition 1, for the actual images of ambient centralizers and Q=F,T, would finish this approach. The ambient theorem by itself gives no such algorithm. No finite generating set for every C_G(a), effective description of its quotient image, or solution of the required intersection problem is proved here. Treating the existing V_br result as a solution of Question 48 would therefore be incorrect.

**Substantive result of this attempt:** the correct restriction problem and an explicit three-strand witness showing that the restriction really matters.
