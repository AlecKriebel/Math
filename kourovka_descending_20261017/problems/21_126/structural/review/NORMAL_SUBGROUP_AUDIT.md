# Fresh normal-subgroup adversarial audit

Verdict: **PASS as a derived partial theorem**, with no claim of originality and no resolution of Kourovka 21.126.

## Exact claim checked

Every finitely presented subgroup N that is normal in its ambient right-angled Artin group A satisfies the intrinsic bound δ_N ≼ exp(n). The proof does not establish the same conclusion for a subgroup normal merely in another subgroup of A, or for an arbitrary finitely presented subgroup. It does not exclude superpolynomial subexponential Dehn functions.

## Primary-source checks

I read the cached full statements, not only abstracts or search snippets. Casals-Ruiz–Lopez de Gamiz Zearra, arXiv:2206.12182v2, Corollary 2.6 across printed pp8–9, explicitly states that a finitely generated full normal subgroup of a finite-graph RAAG has finite-by-abelian and abelian-by-finite quotient. The definitions on printed p1 use intersection with each directly indecomposable factor; subdirectness is not required. Llosa Isenrich, arXiv:2404.12334v2, Corollary 1.3 on printed p2, explicitly allows a homomorphism from a finitely presented synchronous or asynchronous automatic group to any finitely generated abelian group, with finitely presented kernel, and concludes an exponential bound. Surjectivity is not needed in its printed formulation. The cached PDF itself identifies version 2 and 30 October 2024, although its download URL omitted the version suffix.

The established inputs that finite-graph RAAGs are automatic, finite extensions of finitely presented groups are finitely presented, and finite-index subgroups have the same coarse Dehn function are used with their ordinary hypotheses. The normal proposition does not require the finite extension K itself to be a RAAG or automatic.

## Attempts to falsify each reduction

1. **Infinite ambient graph:** a finite generating set of N has finite support S, so every element of N lies in A(S). Normality in all of A implies normality under A(S). No assertion that a subgroup merely contained in A(S) is normal there is made.
2. **Non-full subgroup:** if N intersects an indecomposable factor A_i trivially, the projection deleting it has kernel on N equal to that intersection. Its image is normal in the remaining product because that projection is onto. Isomorphism preserves finite presentation. Repeating may change the image's intersections with other factors; the proof correctly retests and does not claim that they remain unchanged. There are finitely many factors, so it terminates with a full image, or the trivial group. Diagonal subgroups of free abelian groups exemplify why using the image, rather than claiming containment in a complementary product, matters; the argument treats them correctly.
3. **Finite-by-abelian versus virtually abelian:** these properties are not interchangeable in general. The cited corollary supplies the stronger property actually needed. A finite normal subgroup with abelian quotient contains the commutator subgroup; hence Q' is finite. No inference from virtual abelianness alone is used.
4. **K construction:** K=π⁻¹(Q') is a subgroup containing M with [K:M]=|Q'|<∞. The quotient B/K=Q/Q' is finitely generated abelian because B is finitely generated. Thus the coabelian theorem applies after finite presentation is passed from M to its finite extension K. Q/Q' may have torsion; this is allowed by the cited theorem.
5. **Finite-index and trivial boundaries:** N=1 satisfies the claimed coarse upper bound; N finite-index in A, N=A, a central normal subgroup, and a diagonal normal subgroup of an abelian RAAG introduce no exception. The argument never requires N proper or its quotient torsion-free. If K=B, the zero abelian target is also permitted; independently the automatic ambient bound already suffices.
6. **Scope:** no distortion estimate is identified with a Dehn function. This result blocks only a superexponential example which is normal in some RAAG embedding. A virtually compact special group's normal kernel need not be normal in its larger RAAG, so the argument gives no prohibition on a general Rips construction.

No substantive objection remains for the exact proposition. This audit checks the logical application of established theorems, not a new reconstruction of every proof inside those published external results. It provides no evidence that either branch of the full Kourovka problem is solved.

Audit completed 2026-10-24T21:14:14.975916+00:00.
