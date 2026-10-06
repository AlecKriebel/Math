# Fresh mathematical audit of the CM-reduction eightfold

Date: 6 October 2026. Problem 30002364, OWR-12495-004.

## Disposition

**Mathematical pass by this independent reviewer.** The authored construction gives a simple CM eightfold over the algebraic numbers whose every power has only Lefschetz Hodge classes, with a geometrically simple characteristic-5 reduction having non-Lefschetz Tate classes in codimension two. I found no mathematical correction necessary to Sections 2–6. The checks below are an independent mathematical audit, not formal verification or a claim of established novelty.

The literature conflict is substantive. The unrestricted lift equivalence in *Angle ranks of abelian varieties*, Remark 3.5, is incompatible with this construction. The precise failed inference is the claim that averaging a CM type over local embedding fibers preserves the dimension of its Galois orbit span. The formula itself is correct; that equality need not hold. This audit does not claim that the cited authors have accepted this conclusion or published an erratum.

The accepted reviewed text is the scope-clarified archive with SHA-256 f1feb693ca4018fa17eaae271b4020e79fe3b8d41bd9618a50af3664c4625f8d (14,650 bytes). Its independently applied patch changes only the converse clarification and an additional independently inspected primary-source citation; the forward construction is unchanged.

The second question needs a quantifier distinction. The packet correctly states Sugiyama's complete-splitting theorem, which gives a class of CM-variety/prime pairs. If the existential question is read as asking for a class of varieties with the converse valid at every prime, the class of CM elliptic curves already supplies an unconditional affirmative answer; a short proof is included below. No general pointwise converse is asserted.

## 1. Inputs and scope

I inspected the complete authored proof, finite checker, external bootstrap, external manifest, status, source metadata, and validation receipt before executing packet code. The immutable author archive is pinned by SHA-256

32f5ec9f310f62566906cf6b0ff4a1e8cef5a6e9442ecb995c91525a1fb9879e

and has 14,326 bytes. All four supplied external pins match. All five archived files match both the strict inventory and their byte/hash records. The original files were not edited.

I independently loaded the complete catalog, problems, and research-report datasets, rather than projected records. Their three whole-file hashes and sizes match the authored metadata. The complete selected problem record paired with the complete corresponding report, serialized with default `json.dumps(..., sort_keys=True)`, reproduces

0eb5caff364b4dc0f08d4a19fc02dcee04c195e9f3cee4034230731e6c5b8938.

The complete pair was used without projecting fields. The statement hash also matches. Only public dataset hashes, byte counts, record counts, and match results are reproduced in the safe verification metadata.

## 2. The field and the actual prime

Let a and b be the positive square roots of 3+sqrt(6) and 3-sqrt(6). The polynomial X^4-6X^2+3 is Eisenstein at 3. Hence Q(a) has degree 4 and contains K=Q(sqrt(6)). If sqrt(3) belonged to Q(a), the latter would equal K(sqrt(3)). Writing a=u+v sqrt(3), with u,v in K, and squaring shows uv=0. If v=0, 3+sqrt(6) would be a square in K, contradicting its norm 3; if u=0, (3+sqrt(6))/3 would be a square, contradicting its norm 1/3. The norm of a square in K is a rational square. Thus sqrt(3) is not in Q(a).

Since ab=sqrt(3), adjoining b doubles the degree. All roots are real, so L=Q(a,b) is a totally real Galois field of degree 8. The maps r:(a,b)↦(b,-a) and s:(a,b)↦(a,-b) preserve the defining relations and generate D4 of order 8. E=L(i) is a CM field of degree 16 with Galois group D4×C2 and central complex conjugation c.

At 5 the polynomial is separable and factors as (X^2-4)(X^2-2). A local root a congruent to 2 has a unique Hensel lift in Q5; then sqrt(6)=a^2-3 is congruent to 1. The remaining root b lies in the unramified quadratic extension, because its squared residue is 2. The root i congruent to 2 also lies in Q5. These choices give an embedding into an unramified quadratic extension of Q5, hence an actual prime P of E. Frobenius fixes a and i and negates b. Its decomposition group is exactly {1,s} and the local degree is 2. Unramifiedness follows from the discriminant 2^10·3^3 and the unramified adjunction of i at 5.

This does not confuse a prime of E with a good-reduction model. An algebraic-number-field model of the CM abelian variety can be enlarged to contain E and the action and to acquire good reduction above this chosen prime. Because E is Galois, containing E contains every conjugate embedding required by the Shimura–Taniyama theorem. Its residue degree is a multiple of 2, consistent with the half-integral normalized slopes.

## 3. CM existence, polarization, primitivity, and Hodge classes

Every displayed sign choice selects exactly one embedding in each conjugate pair, so it is a CM type. The analytic CM construction with an O_E-stable lattice is polarizable: choose an element of E that is imaginary under c with the required positive imaginary signs on the CM type, using weak approximation in the totally real field, and scale the resulting trace alternating form to be integral. The resulting complex torus is an abelian variety with O_E action. Milne's CM notes, Proposition 3.12, supply the classification/existence statement, and Proposition 7.9 supplies descent to the algebraic numbers. The maximal-order condition is therefore genuinely available, not silently imposed after fixing an unrelated variety.

For the specified signs, the matrix of conjugate centered Hodge cocharacters has determinant 256. I independently reconstructed D4 as permutations of the four roots and reconstructed the CM-type indicator on all sixteen automorphisms. Its centered 16×16 orbit matrix has rank 8; its uncentered indicator matrix has rank 9. Consequently the Mumford–Tate torus is the full norm-similitude torus T of dimension 9. Its sixteen embedding characters on H^1 are distinct.

The centralizer of this torus in End_Q(H^1) has dimension 16 and contains E, so it is exactly E. The correspondence between rational homomorphisms of abelian varieties and rational homomorphisms of their weight-one Hodge structures gives End^0(A)=E. A nontrivial isogeny decomposition would give a nontrivial idempotent in this field, so A is simple. Its type is therefore primitive. Independently, the exhaustive finite calculation gives trivial left and right stabilizers for the CM type; in particular its reflex field is E.

For every power A^n, a splitting coefficient field decomposes H^1 into n copies of each embedding character. A Tate-twisted even-degree wedge is invariant under the full torus precisely when each embedding and its conjugate occur equally often. The invertible centered matrix imposes precisely these equations. Every balanced wedge factors into conjugate-pair degree-two wedges, including pairs drawn from different copies. Degree-two rational Hodge classes are divisor classes by the Lefschetz (1,1) theorem. Taking invariants of a torus and images of the multiplication maps commutes with scalar extension. This proves the all-powers Hodge-Lefschetz assertion over Q, not merely a statement about individual monomials over a splitting field.

## 4. Good reduction and orientation of the slope formula

Milne's CM notes, Proposition 7.12, gives potential good reduction. Theorem 8.1 requires good reduction, all conjugates of E in the coefficient field, unramifiedness of 5 in E, and the maximal-order action. All have been supplied. Its conclusion gives an actual Frobenius element pi in O_E; it is not necessary to infer an element of E from unspecified local eigenvalues. The Weil property yields pi·c(pi)=q.

The convention in Milne 2001, Appendix A.8, explicitly defines the type through H^{1,0} and the fiber at v through phi^{-1}P=v. It agrees with the packet. For the conjugate h(pi) at the prime tP, one evaluates pi at h^{-1}tP. The embeddings carrying h^{-1}tP to P form exactly

D t^{-1}h.

Thus the centered valuation is one half of f(t^{-1}h)+f(st^{-1}h), as asserted. Replacing this by a right average is not an innocuous choice of notation in this noncommutative example.

My independent implementation did not reuse the author's multiplication table, averaging function, matrices, or determinant routine. It represents automorphisms as root permutations, represents primes as right cosets gD, and counts the actual fibers phi^{-1}D directly. This yields eight primes of degree 2, centered slope rank 4, full slope rank 5, and sixteen distinct signed valuation columns. Its Newton multiset is 0^6,(1/2)^4,1^6. The finite-field abelian variety is neither ordinary nor supersingular.

## 5. Endomorphisms, the center, and inseparability

The essential issue is whether new endomorphisms could make the rank drop harmless. It does not happen here.

For two different embeddings h and k, some prime has different valuations on h(pi) and k(pi). Their quotient is therefore not a root of unity. In particular h(pi^n) and k(pi^n) are different for every positive n. Since E is Galois of degree 16, Q(pi^n)=E for every n.

Smooth proper base change and characteristic-zero comparison make H^1 of the reduction free of rank one over E⊗Q_l. Multiplication by pi^n has sixteen different eigenvalues over a splitting coefficient field. Its commutant therefore has dimension 16 and is exactly E⊗Q_l. Tate's finite-field endomorphism theorem identifies this with End^0 over F_{q^n}, tensored with Q_l. The E action is already present. Hence the rational endomorphism algebra over every such extension is E, and taking the union over finite extensions gives geometric End^0(A_0)=E. It is a field, so the reduction is geometrically simple and its center is E.

There is no inseparability exception: these comparisons use l different from 5, and Tate's theorem includes all endomorphisms, not just separable isogenies. As a separate Honda–Tate consistency check, every local invariant s_v·[E_v:Q5] is integral: the degree is 2 and the slopes are 0,1/2,1. Thus no noncommutative division algebra is forced by a hidden half-integral invariant. This consistency check supplements, rather than replaces, the centralizer argument.

## 6. Actual Tate classes and exclusion from the Lefschetz algebra

The relation e=(0,1,0,1,0,-1,0,-1) gives zero valuation for

R=r(pi)r^3(pi)/((rs)(pi)(r^3s)(pi))

at every prime above 5. Away from 5, both pi and q/pi are integral, so pi and every conjugate are units there. Thus R is a global algebraic unit. Its complex conjugates all have absolute value 1 because all conjugates of pi have absolute value sqrt(q). Kronecker's theorem makes R a root of unity.

The four eigenlines with labels r,r^3,crs,cr^3s are distinct; their exterior product is nonzero. In H^4(2) its eigenvalue is R, hence it is fixed over a finite extension. This is an honest cohomological Tate line, not merely an abstract multiplicative relation that would require unavailable repeated exterior factors.

Every degree-two Tate wedge must have opposite centered valuation columns. The exhaustive check gives exactly the eight conjugate pairs. Conversely, these pairs have eigenvalue pi_h·pi_ch/q=1. Tate's theorem for divisors therefore identifies the full degree-two Tate space with the divisor space. Products of two divisor classes have two conjugate pairs among their labels. The displayed wedge has no conjugate pair. Distinct exterior monomials are linearly independent, so it lies outside the divisor-product image. This argument does not require any conjectural comparison between numerical and homological equivalence.

For rational descent, choose one finite extension killing all finitely many root-of-unity eigenvalues. The Tate kernel and divisor-product image are Q_l-subspaces, and their scalar extensions are the spaces just analyzed. A strict inclusion after scalar extension is a strict inclusion before it. This works for every l≠5, without requiring E to split over Q_l itself.

### An explicit uniform extension and dimension check

The commutator subgroup of D4×C2 is generated by r^2. Its fixed field is Q(sqrt(2),sqrt(3),i)=Q(zeta_24), because sqrt(3)=ab and sqrt(2)=sqrt(6)/sqrt(3). It has degree 8. Any root of unity in E generates an abelian extension and is therefore in this fixed field. The roots of unity in Q(zeta_24) are precisely mu_24. Hence every normalized even-degree Frobenius product with zero valuations has order dividing 24. Passing from F_q to F_{q^24} suffices for all geometric Tate classes.

The independent exhaustive exterior-monomial calculation gives the dimensions, by codimension 0 through 8:

- Tate: 1, 8, 32, 80, 114, 80, 32, 8, 1.
- Lefschetz: 1, 8, 28, 56, 70, 56, 28, 8, 1.

In particular the codimension-two quotient has dimension 4. These dimensions are stronger diagnostics than the single relation and are symmetric as expected under duality. They concern cohomology classes only. No nonalgebraicity claim follows.

## 7. Resolution of the published conflict

I inspected the arXiv PDF, including its actual rendered page 6, and the publisher's current HTML. The setup is absolute simplicity, with supersingularity subsequently excluded. The remark does not state ordinary reduction, a completely split prime, or a specified canonical CM lift. The constructed reduction satisfies its explicit setup. Its K/L notation mismatch cannot rescue the assertion here, because both the CM field and the Galois closure of the Frobenius field are E. Nor can rank normalization rescue the concluding equivalence: the centered dimensions are 8 and 4, or 9 and 5 after adding weight.

The averaging formula is a quotient of local embedding data. It need not preserve the Galois-orbit span. Here it removes four dimensions while the right stabilizer of the averaged data remains trivial, so the Frobenius field and geometric endomorphism algebra still have degree 16. This is the precise error in applying the remark to an arbitrary lift. It does not challenge the paper's Proposition 3.1, which correctly detects the finite-field rank from valuations, or by itself invalidate the paper's other results.

There is an additional diagnostic against treating the unqualified mention of a lift as a hidden remedy. Exhaustively enumerating all 256 E-CM types gives exactly two with the specified local fibers; both have centered Hodge rank 8. Selecting another compatible type on the same maximal CM field does not produce rank 4.

A valid sufficient restriction for equality is complete splitting in the Galois closure, when the local averaging is trivial; this is the restriction actually used in Sugiyama's theorem. The audit does not invent an unstated restriction for the published remark. Its unrestricted equivalence needs qualification or correction.

The original Chai–Conrad–Oort proposition and the original Dodson publisher PDF were not successfully retrieved. This limitation remains explicit. Neither is a necessary dependency of the accepted construction: the slope formula and its convention were read directly in Milne's Appendix A.8 and Theorem 8.1/Corollary 8.3, and the two ranks were calculated directly without relying on Dodson's terminology. No statement about the unseen original proposition is inferred from a possibly differently numbered draft.

## 8. Exact target and the two directions

The OWR question's first direction is unrestricted over CM abelian varieties and primes. A simple eightfold is within its scope, and a failure on A_0 itself implies failure of the all-powers property. This construction therefore gives a negative answer to that direction.

Sugiyama's Theorem 0.1(2)(b) in arXiv:1301.4005 gives equivalence when the chosen prime of the Galois closure of End^0(A) is unramified of absolute degree one. For a Galois field this is complete splitting. The OWR theorem is worded using a prime of the reflex field instead. The packet correctly retains the stronger directly inspected preprint condition rather than merging the statements. Sugiyama's abelian-CM-field forward result concerns simple factors of reduction; E is nonabelian, so it does not apply here. The complete-splitting result also does not apply because D has order 2.

For the literal existential converse without a prime condition, take the class of CM elliptic curves B. Their centered Hodge cocharacter matrix is the nonzero one-by-one matrix. The same invariant argument as in Section 3 says that all Hodge classes on every B^n are products of degree-two Hodge classes, hence of divisors. This conclusion is independent of a reduction or its Tate classes. Thus, for every B in that class and every reduction B_0, the Tate-Lefschetz property of B_0 implies the Hodge-Lefschetz property of B. This is an elementary known class, not a claimed new converse theorem. The richer complete-splitting theorem provides the useful nontrivial comparison under its stated restriction.

## 9. Execution, limits, and recommendation

The authenticated original checker passes under normal and optimized semantics, after relocation to a path containing spaces, and with a hostile working directory and Python environment. Twenty-three independent control cases all have their expected result. Shadow modules, cache directories, altered or missing files, symlink members or roots, a mutated/symlinked/internal manifest, and non-isolated invocations are rejected as applicable. A payload marker verifies that untrusted test files were not executed. The bootstrap itself and all expected executable bytes were inspected and pinned before execution.

The independent permutation/fiber diagnostic passes under both `python -I -S` and `python -I -S -O`, with identical output. It neither imports the author's checker nor reuses its matrix-generation code. The finite programs certify finite arithmetic and their declared tests; the CM existence, comparison theorems, Tate theorem, and invariant-theoretic arguments are the separately reviewed mathematical steps above. This is not machine-checked formal proof, and the integrity harness is not a claim to defeat concurrent privileged filesystem modification.

No mathematical correction patch is required to the original forward argument. I independently inspected and applied the 6,007-byte scope/source patch with SHA-256 6ea4f8b41eb68763a92e8ec1b94f48a3a95b8e1ca6e3d3e323a08e85a11b6f6f, using patch with zero fuzz. All five resulting files byte-match the corrected archive; PROOF.md has SHA-256 e6955e4c7e5379e103de79ad3e5dc427d36adab8d36409f81647cbc173495a79. The corrected archive passes a further 23 controls, and the actual independently patched directory passes its externally pinned bootstrap under normal and optimized semantics. The source addition was checked directly in Brian Conrad's original formula notes, including rendered page 3. Those notes confirm the normalized fiber formula, its independence under finite base extension, and that ordinary reduction is unnecessary.

This reviewer accepts those exact corrected bytes. The other four original author files deliberately remain historical pre-audit records, not final acceptance statements. Overall acceptance still requires combining both fresh reviews. Retain the literature-conflict disclosure and avoid novelty, published-erratum, or peer-review claims. Nothing was published by this reviewer.

## References inspected

- Rin Sugiyama, *Lefschetz classes of simple abelian varieties*, OWR 32/2013, pp. 1889–1892. https://ems.press/content/serial-article-files/46461?nt=1
- Rin Sugiyama, *Remark on nondegeneracy of simple abelian varieties with many endomorphisms*, Theorem 0.1 and its proof. https://arxiv.org/abs/1301.4005
- J. S. Milne, *Complex Multiplication*, version 0.10, Propositions 3.12, 7.9, 7.12; Theorem 8.1 and Corollary 8.3. https://www.jmilne.org/math/CourseNotes/CM.pdf
- J. S. Milne, *The Tate Conjecture for Certain Abelian Varieties over Finite Fields*, Appendix A.8. https://www.jmilne.org/math/articles/2001aP.pdf
- Taylor Dupuy, Kiran S. Kedlaya, David Zureick-Brown, *Angle ranks of abelian varieties*, Proposition 3.1, Remark 3.5, and surrounding setup. https://arxiv.org/abs/2112.02455v3 ; https://link.springer.com/article/10.1007/s00208-023-02633-7

- Brian Conrad, *Shimura–Taniyama formula*, Theorem 2.1 and Remark 2.2. https://math.stanford.edu/~conrad/vigregroup/vigre04/stformula.pdf
