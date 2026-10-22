# Independent Frobenius and divisor audit

2026-10-16. Immutable candidate head `cc45ec9dc93515593c3b2a228def86c3a562e13f`, PR 799, problem 30002364. Reviewed operative `corrected/PROOF.md`, original author proof/code, both historical mathematical reviews, README and aggregate verdict. Target-only preregistration preceded their release. No root or contemporary peer findings were read. This audit did not run author code, resume exhausted proof search, mutate Git, publish, or communicate outside the agent team.

**Disposition: mathematical pass for the completed corrected candidate.** I found no counterexample or missing hypothesis in its forward construction. My independent arithmetic reproduces the claimed eightfold and actual codimension-two Tate obstruction. The corrected converse answers the literal existential question through the known CM elliptic class; its separate complete-splitting statement concerns specified pairs. This is an adversarial AI audit, not formal verification, human peer review, a priority determination, or an accepted erratum to the literature.

## Arithmetic reconstruction independent of supplied matrices

The field argument withstands a direct check. Eisenstein gives degree four for Q(a). Over Q(sqrt(6)), the possibility sqrt(3) in Q(a) would force either 3+sqrt(6) or (3+sqrt(6))/3 to be a square. Their norms are 3 and 1/3, neither a rational square. Thus the real splitting field has degree eight; adjoining i doubles it. The substitutions r(a,b)=(b,-a), s(a,b)=(a,-b) act on the actual generators and generate the stated group. All roots of the quartic are real, so complex conjugation is exactly c on i. This identifies a CM field, not merely an abstract candidate group.

The independent code uses signed substitutions on a,b,i and residue homomorphisms into F25=F5[u]/(u²-2). It classifies primes as residue maps modulo Frobenius, rather than using the author's average vector or matrix. At P the triple is (2,u,2). Frobenius fixes 2 and negates u, so the actual decomposition subgroup consists of the identity and s. Separability modulo 5 and the quadratic adjunction give eight unramified primes of local degree two.

For each automorphism phi, the residue map rho_P composed with phi has kernel phi^-1(P). Counting CM-type elements with the same kernel computes the slope of pi at that prime. To compute the valuation of h(pi) at v, compose rho_v with h. This implements the primary fiber formula directly. In group notation its fiber is D t^-1 h, agreeing with the candidate's left averaging, not a right average.

The resulting exact values are:

| Quantity | Independent result |
|---|---:|
| centered Hodge rank / eight-by-eight determinant | 8 / 256 |
| centered Frobenius rank / rank including weight | 4 / 5 |
| distinct embedding valuation columns | 16 |
| geometric degree-two Tate directions | 8 |
| codimension-two Tate / divisor-product dimensions | 32 / 28 |
| Newton multiplicities | 0⁶,(1/2)⁴,1⁶ |

All exterior degrees were enumerated, not only the claimed relation. Tate dimensions by codimension are (1,8,32,80,114,80,32,8,1); divisor-product dimensions are (1,8,28,56,70,56,28,8,1). Four exterior monomials account for the codimension-two quotient. The result is neither ordinary nor supersingular. Multiplication of each slope by the local degree two is integral, so the local division-algebra invariants introduce no Honda–Tate inconsistency.

## Geometry and all finite extensions

The required CM existence is classical rather than an inference from a rank table: the analytic torus Phi(E⊗R)/Phi(O_E) admits an integral trace Riemann form. A totally imaginary element with the required signs is obtained by real weak approximation; scaling makes its form integral. Descent and potential good reduction are applicable. Extend a field of definition to contain E, all action maps, and a place above the selected P, then further to achieve good reduction. Since E is Galois and unramified at 5, the primary maximal-order version of the slope theorem applies. Its output is an actual Frobenius element pi in O_E; no independent principal-ideal assumption is being smuggled in.

For the Hodge assertion on **every** power, the sixteen embedding characters occur with arbitrary copy multiplicities. The full centered rank forces each embedding multiplicity to equal its conjugate multiplicity in any invariant even wedge. Every such wedge pairs into degree-two invariants. The Lefschetz (1,1) theorem and scalar descent therefore give divisor generation on all powers. The distinct characters make the rational commutant E. The usual equivalence for weight-one Hodge structures identifies End⁰(A)=E; a field has no nontrivial idempotent, proving simplicity and primitivity rather than presupposing them.

No two different conjugates of pi have a root-of-unity quotient, because their complete valuation columns differ. Hence pi^n has sixteen distinct conjugates for **every** positive n, and Q(pi^n)=E. Its centralizer on the rank-one E⊗Q_l module is exactly E⊗Q_l. Tate's finite-field endomorphism theorem applies separately over each F_(q^n). Taking their union proves geometric End⁰(A0)=E. Thus no later extension creates new simple factors or endomorphisms that could eliminate the obstruction. This is stronger than a test at the initially chosen finite field.

There is a separate check on the actual divisor space. A degree-two Tate wedge requires opposite centered columns. Exactly eight pairs meet that test, namely (h,ch). Conversely each has eigenvalue one, since pi·c(pi)=q. Alternatively, a polarization has Rosati c on E, so NS(A0)⊗Q has dimension [E^c:Q]=8 by the standard Néron–Severi/Rosati correspondence. Its injective cycle map fills the eight-dimensional degree-two Tate space. This directly checks the divisor algebra after reduction.

For e=(0,1,0,1,0,-1,0,-1), all p-adic valuations of R=r(pi)r³(pi)/((rs)(pi)(r³s)(pi)) vanish. Away from p, pi and its conjugates are units because both pi and q/pi are integral. Thus R and R^-1 are integral. Every archimedean absolute value of R is one by the Weil property. Kronecker's theorem makes R a root of unity. The four distinct eigenlabels (r,r³,crs,cr³s) therefore define a nonzero Tate line in H⁴(2) after some finite extension. They contain no conjugate pair, whereas all divisor products contain two. Linear independence of the exterior basis excludes this line from the product image. Both spaces descend to Q_l, so strict inclusion over a splitting field proves strict inclusion over every Q_l, l≠5. No numerical-equivalence assumption or conjecture about algebraicity is used.

## Published conflict and remaining limits

I independently read the setup, Proposition 3.1, and Remark 3.5 of [Angle ranks, v3](https://arxiv.org/abs/2112.02455v3). Absolute simplicity and the exclusion of supersingularity do apply here. The remark supplies no ordinary or completely split condition, and concludes an unrestricted lift equivalence. The candidate's ranks refute the intervening inference that averaging preserves the orbit-span dimension. A hidden change from centered rank to rank including weight cannot explain 8 versus 4 (or 9 versus 5). Its finite-field valuation criterion remains consistent with the calculation.

The primary slope theorem was checked in [Milne's CM notes](https://www.jmilne.org/math/CourseNotes/CM.pdf), [Milne 2001, Appendix A.8](https://www.jmilne.org/math/articles/2001aP.pdf), and [Conrad, Theorem 2.1 and Remark 2.2](https://math.stanford.edu/~conrad/vigregroup/vigre04/stformula.pdf). This audit did not inspect the final CCO proposition or original Dodson article and makes no claim about their unseen text. Neither is a necessary dependency of this direct proof. The literature-conflict disclosure must remain; no outside author's acceptance or published correction is implied.

The strongest verified result is the completed corrected construction and its stated elementary converse class. No exact mathematical gap remains identified by this audit. External priority and broader current literature status are unresolved and are separate from truth. The finite checker certifies the arithmetic described above; the mathematical bridges are prose verification of established theorems, not proof-assistant output.
