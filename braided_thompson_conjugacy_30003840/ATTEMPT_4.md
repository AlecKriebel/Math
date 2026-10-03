# Attempt 4 — Twisted conjugacy in the split F extension

**Aim.** Use the decidable classical F quotient and the split extension to deal with general F_br elements, rather than only K. **Outcome:** an exact twisted-conjugacy/centralizer reduction and explicit linear obstructions. The reduction does not supply the missing decision algorithm; its direct extension to T_br is invalid.

The established split extension is

    F_br = K semidirect F.

Let s:F -> F_br be the braid-free section and let alpha_f(k)=s(f) k s(f)^(-1). Write a general element as (a,f)=a s(f), with a in K, f in F. Use the multiplication convention

    (a,f)(b,g) = (a alpha_f(b), fg).

All these conversions are effective using tree-braid-tree operations. The splitting is credited to the standard structure results described in SOURCE_GATE.md.

## 1. Normalize the quotient first

For inputs (a,f) and (b,g), conjugacy in F_br implies conjugacy of f,g in F. Apply the credited classical F conjugacy algorithm. If the answer is no, the braided elements are not conjugate. If yes, find t in F with g=t f t^(-1). Conjugating (b,g) by s(t)^(-1) turns it into

    (alpha_(t^(-1))(b), f).

Replace b by this normalized kernel coordinate. The two quotient coordinates are now exactly the same f.

## 2. Solve the conjugation equation without dropping a term

**Proposition 4.1.** The normalized elements (a,f),(b,f) are conjugate in F_br iff there are k in K and z in C_F(f) satisfying

    b = k alpha_z(a) alpha_f(k^(-1)).                  (4.1)

**Proof.** A general conjugator is (k,z), whose inverse is (alpha_(z^(-1))(k^(-1)),z^(-1)). Multiplication gives

    (k,z)(a,f)(k,z)^(-1)
      = (k alpha_z(a) alpha_(z f z^(-1))(k^(-1)), z f z^(-1)).

Its second coordinate equals f exactly when z centralizes f. Under that condition the first coordinate is precisely (4.1). This proves necessity and sufficiency and supplies the conjugator whenever k,z are found. ∎

Equivalently, consider the alpha_f-twisted conjugacy classes in K, where v is related to u if v=k u alpha_f(k^(-1)). Since alpha_z commutes with alpha_f for z in C_F(f), the centralizer acts on those classes. The remaining question is whether the class of b is in the orbit of the class of a.

This form separates two difficulties rather than concealing either: twisted conjugacy in the infinite direct-limit kernel, and the orbit of the quotient centralizer on its classes. An algorithm for C_F(f) alone would not answer that orbit question.

## 3. A computable necessary quotient equation

Let M be the additive linking-function image from Attempt 2 and write lambda_a,lambda_b for the images of a,b. The action of f on M is

    (f . lambda)(x,y)=lambda(f^(-1)x,f^(-1)y).

Applying lambda to (4.1) yields the necessary equation

    lambda_b - z . lambda_a = (1 - f) . nu,
    for some z in C_F(f) and nu in M.                  (4.2)

All terms for any proposed k,z are finite-step functions and can be compared after a common finite dyadic refinement. This does not yet make existential membership in the infinite image (1-f)M decidable.

For any finite orbit O of unordered distinct pairs under f, summing a function of the form nu-f.nu over O gives zero: f permutes O and the terms cancel. Thus (4.2) implies

    sum_(v in O) (lambda_b(v) - (z.lambda_a)(v)) = 0.  (4.3)

For f in F every finite orbit of individual Cantor points is fixed, since its action is increasing. A finite orbit of unordered pairs similarly fixes both points. Therefore the useful specialization is the whole restriction to pairs of fixed points of f:

    lambda_b(x,y) = lambda_a(z^(-1)x,z^(-1)y)
    whenever f(x)=x and f(y)=y.                      (4.4)

The centralizer preserves Fix(f), so this is an actual orbit restriction, not an arbitrary relabeling. In particular F fixes the two endpoint Cantor sequences 000... and 111..., giving the familiar endpoint-linking obstruction of Attempt 1. If f fixes a clopen region, the restriction retains a finite linking pattern on that region. If f is a one-bump element, this endpoint test can be much weaker. No claim of sufficiency for (4.2), (4.3), or (4.4) is made.

## 4. Why abelianization cannot repair the reduction

At f=identity, (4.1) is ordinary K-conjugation combined with the F action, exactly the kernel-input problem of Attempt 3. Equation (4.2) then reduces to equality of F-orbits of linking functions. The nontrivial zero-linking commutator versus the identity from Attempt 2 satisfies that equation but is not conjugate. Thus even the easiest quotient coordinate disproves sufficiency of the abelianized equation. A nonabelian solution of (4.1), not just a linear equation, is required.

There is one fully solved special case: when a=b=identity, the inputs are braid-free elements s(f),s(g). They are conjugate in F_br iff f,g are conjugate in F. Necessity follows by pi; sufficiency follows by lifting any F-conjugator using s. This is a consequence of the existing classical F algorithm, not a solution for arbitrary braiding.

## 5. The same splitting cannot be assumed for T_br

T contains a nontrivial involution, represented by exchanging the two half-circle intervals. V_br is torsion-free, a credited standard property, hence its subgroup T_br is torsion-free. A homomorphic section T -> T_br would inject that involution, a contradiction. Consequently the T extension does **not** split.

One may select lifts of T elements set-theoretically, but their multiplication introduces a K-valued factor set. Omitting that factor set would make (4.1) false in the T setting. This attempt therefore does not transfer the F semidirect-product calculation to T by a change of letters.

**Substantive result:** the exact general-F_br conjugacy equation, its linking-function obstruction, a solved braid-free subcase, and a rigorous obstruction to an unjustified T_br splitting shortcut.
