# Independent adversarial audit: KOU-21.113 / ID 2622 / rank 471

**Verdict: PASS as a five-attempt, unresolved partial-research package. No proof or counterexample to the general problem is certified. No blocking mathematical or computational repair was found.**

Audit date: 3 October 2026 UTC. Frozen author manifest SHA-256: `ec940c94419e8eaaf664e67aca5eb14199aad0ae79cadcc465414ee399ef1179`. Supplied WIP commit: `216606ca92bee28f2a55afd51aea3f80a54185ad`.

The verdict concerns the 12 payload files listed by `AUTHOR_MANIFEST.json`, plus that manifest itself. All byte counts and SHA-256 hashes were independently checked. Remote repository verification is outside the scope of this mathematical audit. The frozen author files were unchanged. The new calculations below are audit controls for the existing claims, not an additional proof attempt.

## 1. Source, exact question, and hypotheses

The current official October 2026 Notebook was independently fetched through the link in the editors' 30 September update. Printed page 194 (PDF page index 193) gives the stated question, attributed to G. Robinson, without a solved or AI-solution marker. The preserved page image was also visually inspected. The live PDF text agrees with it.

The exact setup is a finite group G and a prime p. A p-element includes the identity. The function Psi is zero at elements with order divisible by p; at p-regular y its value is the number of p-elements of C_G(y). Part (a) asks for ordinary-character positivity. Part (b) asks for a projective RG realization, with R a complete discrete valuation ring of characteristic zero, fraction field K splitting G and all subgroups, and residue field F = R/J(R) of characteristic p splitting G and all subgroups. Characters and Brauer values must be interpreted using a consistent root-of-unity identification. F need not literally be algebraically closed; extension to a splitting algebraic closure in the A5 argument is legitimate.

These hypotheses supply finite projective lifts, projective covers, Brauer/projective duality, and Krull–Schmidt decomposition. In particular, the paper's cited virtual-projectivity result is indispensable: one does not obtain integral projective coefficients merely by observing that an arbitrary function vanishes on p-singular elements. Here Psi is a generalized ordinary character, and the cited theorem gives its integral expansion in projective indecomposable characters. With PIM characters Phi_i dual to irreducible Brauer characters phi_i under the p-regular pairing, Psi is genuinely projective exactly when every coefficient <Psi,phi_i> is nonnegative.

The live University of Aberdeen publication record and publisher search result independently confirm Robinson's Journal of Algebra 690 (2026), 37–74 paper, DOI 10.1016/j.jalgebra.2025.11.001, with the universal assertions still conjectural and the PSL(2,q) and SL(2,q) cases established for every prime p and prime power q. The preserved author PDF is visibly arXiv v4, 21 October 2025, with document date 22 October; a fresh pdftotext extraction exactly matches the preserved text. Its Theorem 14.1 and Corollary 14.2 state those two families. Theorem 3.2 supplies the normal-subgroup cases; Remark 5.1 supplies the centralizer identity, truncated conjugation projective, and central p'-quotient reduction; Theorem 7.3 supplies the stronger centralizer-normal-complement ordinary case. The references in the attempts correctly refer to v4 numbering.

Schroeder's September 2026 preprint is relevant but concerns a different function: Pi_{p',G}(y) = |C_G(y)| on p-regular y. Its Example 2.6 explicitly distinguishes Robinson's p-element count. The proof of Theorem 3.3(i) gives nonnegative integral PIM coefficients for this larger function, although the theorem's headline states ordinary positivity. Thus the author's use of it for Lambda is valid; it is not a solution for Psi.

No exhaustive historical-priority or global literature-status claim is certified. The source gate appropriately limits its negative search and discloses the failed catalogue/final-version downloads.

Primary links:
- Notebook: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf
- Editors' update: https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/
- Robinson publication: https://abdn.elsevierpure.com/en/publications/a-generalized-character-related-to-the-p-local-structure-and-repr/
- Robinson v4: https://arxiv.org/abs/2505.03976v4
- Schroeder: https://arxiv.org/abs/2609.26464

## 2. Attempt-by-attempt mathematical audit

### Attempt 1: PASS

The fiber of x -> x_{p'} above a fixed p-regular y is precisely {uy: u in C_G(y) is a p-element}. This proves the normalization 1/|G| and conjugation in A_G(f). A_G is conjugate-linear in f. Its values on ordinary or Brauer irreducibles are the relevant generalized ordinary or projective coefficients, respectively.

Primary decomposition commutes with any homomorphism, including a quotient by a normal subgroup that is not a p-group. Uniform quotient fibers prove A_G(Infl f) = A_{G/N}(f), with no missing factor of |N|. This does not say that Psi itself inflates through an arbitrary quotient.

The least-order ordinary-counterexample argument is valid: a negative irreducible coefficient descends to the quotient by that character's kernel, so the witness must be faithful. A linear character's p'-factor is an actual homomorphism on G; its average is zero or one. Therefore the ordinary witness is nonlinear. This uses no invalid positivity claim about arbitrary weighted roots of unity.

For normal p-subgroups N, every simple FG-module has N in its kernel, so the quotient parametrizes every irreducible Brauer character. Together with the averaging identity this proves exact invariance of the full PIM coefficient vector. It does not falsely claim that inflation of a projective quotient module remains projective across a p-kernel. The resulting equivalence and O_p(G)=1 minimal-counterexample reduction are sound.

For a central p'-subgroup Z, the inverse image of a cyclic p-subgroup has a unique complement to Z: existence and conjugacy follow from Schur–Zassenhaus (the p-group quotient is soluble), and centrality makes conjugate complements equal. Hence every quotient p-element has a unique p-element lift. If uZ commutes with yZ, the commutator [u,y] lies in central Z and has p-power order because u does, so it is trivial. This proves the claimed pointwise inflation of Psi. The idempotent e_Z is defined because |Z| is a unit in R; RG e_Z is R[G/Z] as an R-algebra with identity e_Z. Projectivity is preserved in this direct summand. The converse follows by the same block component or by character expansion. Both ordinary and projective positivity are invariant here.

Direct-product Psi values multiply. Ordinary and Brauer irreducibles are exterior tensors in the splitting setup; PIM expansions therefore form outer products. Each factor has coefficient 1 at the trivial ordinary or trivial Brauer character. This last fact is essential to the reverse implication, since it exposes any negative coefficient in either factor. Centerlessness and direct indecomposability are consequently valid for a least-order projective counterexample. The normal-p-free conclusion is not asserted here for a least-order ordinary counterexample.

### Attempt 2: PASS

Expanding induction and changing x by conjugation cancels exactly |G| from the sum over conjugating elements. The remaining denominator is |H|, and the condition is x_{p'} in H, not x in H. The conjugate lambda value is correct.

Power maps by integers coprime to |G| are permutations of the underlying finite set, even though they need not be group homomorphisms. They preserve the condition x_{p'} in H. Every unit modulo m lifts to a unit modulo |G|, since m divides |H| and one can avoid additional prime divisors by CRT. It follows that T_j is constant on primitive-root orders. With t_d denoting the count per individual primitive d-th root, the sum is sum_{d|m} mu(d)t_d. There is correctly no extra Euler-phi factor. For d=1, the index m/d is understood modulo m.

The two positive cases are sound. For p-power-order lambda every term is 1, while the cited generalized-character result supplies integrality. For p'-subgroups H, all elements are p-regular and restriction of Psi is exactly the conjugation permutation character on G_p; Frobenius reciprocity supplies nonnegativity. Neither case permits replacing arbitrary irreducibles by nonnegative combinations of those induced characters. The note correctly distinguishes the alternating Mobius expression's integrality from its unknown nonnegativity.

The S4/A4 and S5/C6 values were independently recomputed by a direct induction average, not only by evaluating the claimed fiber formula. They are respectively (16,4,4) with coefficient 1 and (56,2,2) with coefficient 9. An additional composite-order audit control with G=S3 x C10, H=C3 x C10, p=2, m=15 gives t_1=8, t_3=2, t_5=8, t_15=2. The Mobius numerator 8-2-8+2=0 agrees with direct induction in Q[z]/Phi_15(z). This tests the per-root normalization beyond the prime-m examples.

### Attempt 3: PASS

Subtracting the ordinary average of chi gives the displayed correction formula. Inversion invariance makes the total real, so replacing sums of conjugates by sums of real parts is legitimate. For a pure p-element u the summand chi(1)-Re chi(u) is nonnegative by unitarity. The absence of mixed-order elements is equivalent to every nonidentity p-element having a p-group centralizer. The resulting ordinary-character special case is correctly weaker than the cited Robinson theorem.

In C6 at p=2 the pure contribution is 2 and the two mixed contributions are -1 each. Their total is zero. The eigenline factor eta(1-zeta) and its sign are correct. This disproves only a termwise-positivity shortcut.

The average of Psi is 1. If Psi were a permutation character, Burnside's lemma would force a transitive G-set of degree |G_p|, hence |G_p| must divide |G|. S3 at p=2 has degree 4 and group order 6, so this is impossible; its ordinary character is nevertheless 1 + sign + standard. The A5 degree 16/order 60 control is also valid. These arguments do not prohibit general projective linear modules or disprove Psi positivity.

### Attempt 4: PASS

The signs a+b=-1 and ab=-1 are consistent throughout. Alpha=1+chi_3 has the stated values, is an ordinary character, vanishes on all characteristic-2 singular classes, has degree 4, trivial multiplicity 1, and strictly positive real values on all regular classes. Its pairing with the opposite natural degree-2 Brauer character is exactly -1, with denominator 60 and weights 1,20,12,12. Consequently alpha is not projective. It is a different function from Psi, as the note repeatedly states.

The natural SL(2,4) module and its Frobenius twist are absolutely irreducible: the upper and lower nontrivial unipotents have incompatible unique invariant lines, and this remains true over the algebraic closure. Their Brauer eigenvalue sums and the Frobenius interchange of the two order-5 classes are correct. The degree-4 ordinary character has 2-defect zero; its reduction is irreducible. There are exactly four regular classes, so the four displayed irreducibles exhaust the Brauer characters. Any swap of the two degree-2 labels merely swaps which coefficient of alpha is negative.

For the actual Psi, centralizers at orders 3 and 5 are cyclic of those orders, giving (16,0,1,1,1). In the five-point action a Sylow V4 has orbits of sizes 1 and 4. The augmentation basis e_i-e_fixed on the regular orbit identifies Res_P(W) with RP exactly over R, not just after scalar extension. Averaging a P-linear splitting divides only by [G:P]=15, a unit in R. Hence W is RG-projective. The diagonal tensor product with an R-free lattice preserves projectivity via the stated free-module change of basis and direct-summand argument. Thus W tensor W genuinely realizes Psi. This proof does not assume that every simple modular representation has an ordinary lift.

The independent matrix/class-algebra controls give ordinary coefficients (1,1,1,1,1), PIM coefficients (1,0,0,1), alpha coefficients (1,0,-1,0), and PIM degrees (12,8,8,4). These agree with all author values.

### Attempt 5: PASS

The construction sum_i P_i tensor S_i^* is in characteristic p. Tensoring a projective with any finite-dimensional module preserves projectivity for the diagonal action. Projective/Brauer column orthogonality gives centralizer values on p-regular elements; projective lifting over the complete DVR supplies an ordinary projective character with those values and zero singular values. This validates Lambda without incorrectly lifting arbitrary S_i individually.

The identity Lambda_G = sum_{y in G_{p'}/G} Ind_{C_G(y)}^G Psi_{C_G(y)} has the correct denominator and conjugation directions. At regular x, reorganizing the induction sum gives, for each y, a sum over z in y^G intersect C_G(x) of |C_{C_G(x)}(z)_p|. Summing y is the primary-part fiber partition inside C_G(x). All terms vanish at singular x.

Minimality is used precisely where required: in a centerless least-order projective counterexample, the nonidentity regular y have proper centralizers. Only under the assumption that all smaller groups satisfy the conjecture are the induced terms in D genuine projectives. Then Psi=Lambda-D is a virtual-projective identity, not positivity.

The coefficients r_phi=sum_{regular class reps z} conjugate(phi(z)) and d_phi=sum m_{y,phi,beta} c_{beta,C_G(y)} are correct. Restriction of a Brauer character records nonnegative composition multiplicities; semisimplicity of the restriction is unnecessary. Frobenius reciprocity applies to the regular pairing. Under minimality both r and d are nonnegative integer vectors, but this does not imply their difference is. The missing condition d_phi <= r_phi for each phi is exactly the conjectured projective positivity in this formulation.

For finite projectives over the complete splitting DVR, PIM characters distinguish the indecomposable summands. Therefore the componentwise condition is equivalent to existence of a split embedding L_G into T_G. This equivalence does not construct the embedding. The note correctly leaves it unresolved.

In A5, the two separate order-5 classes must both contribute, giving D=Ind_C3(1)+2 Ind_C5(1). The independent exact vectors r=(4,0,0,3) and d=(3,0,0,2) agree. Their degree check is 60-44=16. The identity basis vector gives a direct trivial summand in each conjugation permutation module; the trivial module is not projective when p divides |G|. Thus equality of Brauer characters with a projective module does not establish projectivity of those permutation modules or provide the needed split embedding.

## 3. Reproducibility and independent controls

Both supplied scripts were run from isolated temporary copies so their output-writing behavior could not touch the frozen package. Each produced byte-identical JSON to the manifested output.

The new `independent_controls.py` imports neither author checker. It constructs multiplication tables, inverses, centralizers, and conjugacy classes independently. SymPy's permutation machinery supplies S3/S4/S5; SL(2,3) and SL(2,4) are constructed directly as determinant-one matrices over the corresponding finite fields. A5's ordinary table is recovered by exact simultaneous class-algebra eigenvectors, rather than replaying the author's character table. The natural modular traces and projective-line action are reconstructed from F4 matrices.

Verified controls:
- 14 group/prime cases across S3, S4, S5, SL(2,3), SL(2,4), and C6: 660 elementwise primary-fiber comparisons and 660 elementwise full centralizer-induction identities.
- 10 normal-quotient/prime cases: 204 elementwise primary-part compatibility checks, plus all quotient class-indicator averages.
- A nonsplit central p'-quotient: SL(2,3) -> A4 at p=3, with pointwise Psi inflation.
- S3 x C2 and S3 x C3 at p=2: pointwise direct-product identities.
- The two stated induced-linear examples, checked by direct induction as well as fiber counts.
- A composite m=15 Mobius/direct-cyclotomic induction control with H containing p-elements.
- S4/V4 -> S3 at p=2: explicit full Brauer coefficient vectors (1,1) on both sides.
- A5 matrix reconstruction: classes, ordinary degree list, natural Brauer values, PIM coefficients and degrees, Sylow orbit/free-lattice character control, tensor-square Psi identity, and Lambda-D coefficient balance.
- C6 signed pure/mixed corrections.

The scripts and their exact output are in this audit directory. These finite checks strengthen confidence in signs, normalizations, class weights, and proof boundaries; they do not prove the universal conjecture.

## 4. Repairs, scope, and release recommendation

**Required repairs: none.**

Useful nonblocking clarifications for a future edit, without changing the mathematical content:
1. Expand the first occurrence of “appropriate splitting p-modular system” into the exact complete-DVR, characteristic, and all-subgroups splitting hypotheses stated above. They are implicit in the package and correctly inherited from the source, but spelling them out improves standalone readability.
2. State once that the “trivial coefficient” in the projective discussion means the coefficient of the projective cover of the trivial Brauer module, not an actual trivial projective module when p divides |G|.
3. Keep the ordinary minimal-counterexample witness and the stronger projective minimal-group reductions separately worded; one should not infer that an ordinary-positive/projective-negative example has a negative ordinary coefficient.
4. Preserve the current explicit limitations: the A5 alpha example is not Psi; non-permutation and negative mixed-term controls attack proposed proof mechanisms only; no new group family or novelty is claimed; and the final componentwise domination is an unproved substantive step.

**Exact passed scope:** sound partial reductions, exact formulas, credited special cases, valid counterexamples to overstrong proof shortcuts, and reproducible bounded controls, across five distinct attempts. **Not passed as solved:** either universal assertion, a universal Mobius-fiber inequality, a universal mixed-term domination theorem, or the final split-embedding assertion. The record should remain `unresolved` with the audit outcome separately recorded as PASS.
