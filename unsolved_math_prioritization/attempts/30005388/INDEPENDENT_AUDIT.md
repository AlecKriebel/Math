# Independent audit: involutive Arf equality on smooth torsion

Date: 2026-10-08. Target: problem 30005388. Input: the complete authored public packet identified by ORIGINAL_INPUT_INVENTORY.json.

## Decision

Accept the mathematical content as a **five-approach partial audit**, subject to the scope below. The target remains unresolved by this work, the proof-search budget remains exhausted at 5/5, and there is no full proof or actual-knot counterexample. No sixth proof route was undertaken.

A material validation gap was found in the original verifier: replacing the correct tensor involution by the naive tensor product still returned PASS. The original code found different maps for that incorrect matrix instead of checking the report's literal certificates, and did not check that the tensor matrix itself satisfied the horizontal square axiom. This does **not** invalidate the displayed mathematical certificates, which pass independent checking with the correct tensor law.

Accept the corrected derivative verifier, verify_hardened.py, together with its exact CORRECTION.patch and the independent checker. Do not describe the original two negative controls as adequate coverage of the tensor formula. The original packet is preserved byte for byte.

## Source and scope verification

The source numbering was checked against the published Kang–Park article, not inferred solely from the original preprint. Definitions 2.3 and 2.5 give the horizontal object and almost-local maps. The tensor formula preceding Proposition 2.6 includes its derivative correction. Example 2.9 supplies the figure-eight model. Theorem 2.11, Corollary 2.12, and Example 2.14 supply, respectively, the comparison structure, the torsion image, and the quasi-alternating equality. Question 1.6 is the exact target. These passages are on PDF pages 4, 8–9, and 12–14 of the retained published PDF. The publisher's page confirms the 2026 volume citation and 2024 online publication date. [Kang–Park, published article](https://ems.press/journals/jems/articles/14298076); [published PDF](https://ems.press/content/serial-article-files/48375).

The matching question in OWR 4/2023 is Question 4 on printed page 251. This establishes the target's source, not its worldwide status today. [Official report](https://publications.mfo.de/bitstream/handle/mfo/4017/OWR_2023_04.pdf?sequence=4).

The audit below independently recomputes the packet's elementary algebra. It does not re-prove the cited Floer-theoretic foundations, recognize which abstract complexes arise from knots, compute a new knot involution, or infer knot torsion from formal algebra.

## 1. Additive-character route

Accepted.

Let D=A+Arf. For any t in the smooth concordance torsion subgroup, D(2t)=0. On every quasi-alternating torsion generator q, D(q)=0, and additivity gives D(Q)=0. Thus D factors uniquely through T/(2T+Q), and vanishes exactly when its factor does. The quotient need not be zero; the argument establishes no classification of its elements.

If mt=0 with m odd, m acts as the identity on F_2, so A(t)=Arf(t)=0. This implication neither asserts nor excludes nonzero odd-order smooth concordance torsion.

For the figure-eight class e, set y=x−A(x)e. Then A(y)=0 and Arf(y)=Arf(x)+A(x). This proves the stated equivalence with vanishing on ker A. It does not identify that kernel.

The F_2^2 countermodel is valid: a(u,v)=u and b(u,v)=u+v are additive, agree at e=(1,0), and differ at (0,1). Consequently, agreement on e, even multiples, and image size cannot force the desired equality. The independent checker exhausts this finite group and tests the kernel identity.

## 2. Long-box route

Accepted with the stated formal-complex limitation.

### Differential, gradings, and localization

For the displayed five generators, both length-two paths from a to d have coefficient U^n V^n and cancel over F_2; every other length-two path is zero. Each differential term has the required bidegree. The involution family is skew-graded and semilinear in the exchange U↔V.

After inverting U, replacing b by b+(V/U)^n c splits the square into the contractible pairs a→U^n b' and c→U^n d. The only surviving localized tower is x. The same argument with U and V exchanged applies after inverting V.

For n>1, the horizontal differential has no linear-U term, so its hat derivative is zero. The hat j_0 is an involution, and its companion derivative has the zero lift. Inclusion and projection of x satisfy the required maps. Hence the unmodified horizontal object represents O.

The contributions to the Euler polynomial are +1 from each of a,d,x and −t^n,−t^(−n) from b,c. Thus it is 3−t^n−t^(−n), equal to 5 at −1 for odd n and 1 for even n. The determinant/Arf residue interpretation is conditional on realization by a knot. It is not an Arf invariant assigned to arbitrary formal complexes.

### Full square obstruction and repair

Direct formal differentiation gives Phi Psi(a)=(n mod 2)U^(n−1)V^(n−1)d; it vanishes on the other basis elements. Since j_0^2=1, the odd-n defect has a coefficient outside the ideal (U^n,V^n). Every coefficient of dH+Hd belongs to that ideal for any polynomial homotopy H. The defect is therefore not nullhomotopic over F_2[U,V]. Localization would change the coefficient ring and cannot remove this obstruction in the required category.

For the displayed repair, the only nonidentity term of j_(lambda,mu)^2 is lambda mu U^(n−1)V^(n−1)(a↦d). Thus the relation holds precisely when lambda mu=n mod 2 within this two-parameter family. This is not a classification of all possible involutions.

When n>1 and lambda=mu=1, the hat involution fixes x and sends a to a+x. A map O→C sends 1 to x and is local. A map C→O must send x to 1. In this reduced hat complex there are no nonzero chain homotopies, so equivariance on a would force 1=0. Therefore O<C strictly. Translation preserves strict inequalities in the local-equivalence group, giving O<C<2C<...; C has infinite order. No smooth knot is inferred to realize it.

All grading-preserving polynomial maps for these examples are covered: a coefficient of a map to or from the degree-(0,0) tower can be nonzero only when the other coordinate of the source/target generator is zero. The eligible basis generators are a,x, and additionally d when n=1, all of degree (0,0). Thus all eligible coefficients are constants. This closes the possible nonconstant-map loophole.

For n=1 the repair is the figure-eight model; the explicit tensor certificates below establish its square is O. For even n, j_0 satisfies the full square relation and the horizontal object is O. These are mutually consistent cases.

## 3. Tensor-descent route

Accepted mathematically; original verification corrected.

The involution is J=j⊗j+(Phi j)⊗(j Phi). The order of composition and the derivative correction matter.

For the literal inclusion g(1)=ad+bc+cb+da+xx:

- d(ad)=Ubd and d(bc)=Ubd;
- d(cb)=Udb and d(da)=Udb;
- d(xx)=0.

Thus dg=0. For the literal projection with the same five-element support, the only potentially nonzero values on differentials are the cancelling pairs on ac and ca. Hence fd=0. All five support elements have bidegree (0,0).

Under the naive j⊗j, the inclusion has equivariance defect dd. Its correction term contributes exactly dd, cancelling the defect. Dually, the naive projection has a nonzero equivariance defect on aa, cancelled by the correction. The independent checker tests every basis element, rather than only these explanatory witnesses.

After U localization, the square summands are contractible. Only xx survives, and both literal maps send that tower nontrivially. Therefore both maps are local. For E itself the exhaustive eligible-map calculation finds no map either way with O. In particular, E is not O while E⊗E is O.

This is a valid counterexample to unrestricted tensor-root descent, not a counterexample to A=Arf. The norm of a fixed vector in characteristic two under a twofold symmetry is zero. The polynomial observation is also correct: for even m and symmetric Delta, Delta^m is the norm of Delta^(m/2), up to the usual Laurent unit. Evaluating at −1 loses the remaining mod-eight distinction. The odd-order case was already disposed of by the character argument.

### Reproduced validation defect

The single source mutation

    jt = add(tensor(j, j), tensor(mul(phi, j), mul(j, phi)))

replaced by

    jt = tensor(j, j)

returns PASS in the original verifier in normal, -O, and -OO modes. Its solver changes the inclusion support to ad,bc,cb,da,dx,xx and the projection support to ad,ax,bc,cb,da,xx. These are not the report's certificates.

More seriously, the naive tensor matrix is not even a horizontal almost-iota structure with the displayed tensor differential. For P=hat(d/dU)(d_tensor) and Psi'=J_naive P J_naive, the defect

    J_naive^2 + 1 + P Psi'

takes aa to bc+cb+dd. Thus the original PASS cannot validate that tensor object.

The corrected verifier checks the tensor grading, square axiom, and derivative commutation, then fixes the literal supports ad,bc,cb,da,xx for both maps and checks them. The same naive-tensor mutation now fails at `tensor horizontal square axiom` in all three optimization modes. The independent implementation also rejects it at literal inclusion equivariance. Positive output is byte-identical to the original saved exact result. CORRECTION_VALIDATION.json verifies that the patch applies cleanly and produces the exact delivered hardened bytes.

## 4. Surgery/spin route

Accepted, including the restriction of what the counterexample rules out.

The independent staircase calculation enumerates homogeneous chain combinations with their actual U exponents. For one trefoil, degree-zero p and q are outside the nonpositive quadrant; their U multiples give the required tower image. For two trefoils, the complete degree-zero list is pp,pq,qp,qq,Urr, all outside the quadrant. U(pq) lies in the quadrant and represents U times the tower generator. Hence V_0(T)=V_0(T#T)=1.

Ni–Wu Proposition 1.6 at p=q=1, i=0, together with V_0=H_0 from Lemma 2.7, gives d(S^3_1(K))=−2V_0(K). Thus the two surgery constructions in the packet have d-values −2 and −4. Additivity and integral-homology-cobordism invariance of d rule out their being homology cobordant. This disproves general additivity of the surgery operation. The example contains infinite-order knots and does not disprove a hypothetical torsion-only replacement. [Ni–Wu, source PDF](https://arxiv.org/pdf/1009.4720).

The Hendricks–Manolescu author preprint explicitly gives ordinary V_0(4_1)=0 with Arf(4_1)=1 on page 6. Its proof of Corollary 1.8 on page 64 states the generalized Rokhlin surgery formula; setting the surgery coefficient to one yields the Arf identity used here. This also supplies an inspectable source for that identity without relying on OCR of the scanned Kirby book. The normalization is the mod-two Rokhlin invariant. [Hendricks–Manolescu](https://web.stanford.edu/~cm5/hfi.pdf).

Hendricks–Mallick's Section 4 explicitly discusses long-box local-equivalence models and their earlier provenance. Its cabling formulas concern underlined/overlined V_0; they do not furnish the missing universal A/Arf identification. The attribution warning in the packet is appropriate. [Hendricks–Mallick, Section 4](https://arxiv.org/html/2409.02192v2#S4).

## 5. Actual-knot family and torsion-only rank test

Accepted with all realization, normalization, and torsion hypotheses retained.

HKL Proposition 1.1 gives negative amphichirality and order dividing two; it does not say every family member has exact order two. Corollary 1.2 supplies the topologically slice differences when the companion is topologically slice. Section 2.1 computes the branched-cover homology order 4n^2+1. Theorems 1–3 and Corollary 3.3 concern the selected infinite nonslice families. [Hedden–Kim–Livingston](https://arxiv.org/html/1212.6628v2).

Independently, the surgery linking matrix has diagonal entries −2n,2n and off-diagonal entries 1; the absolute determinant is 4n^2+1. Its mod-eight class is 1 for even n and 5 for odd n. The determinant/Arf criterion therefore gives Arf(K_(J,n))=n mod 2. The untied rational knot is alternating, hence quasi-alternating. The cited quasi-alternating result and additivity now yield all stated formulas for L_(J,n).

If A(L)=1, L cannot be slice since the invariant vanishes on the identity. Combined with order dividing two, this would establish exact order two. No missing non-sliceness proof is needed after such an A computation. But no such computation is supplied here; the actual involution matrices remain missing.

### Independent proof of the membership criterion

Work only with the assumed homogeneous reduced basis, positive n_i, one normalized free generator x of bidegree (0,0), and the correct hat involution. Let Z be the span of the torsion cycles z_i and W=im(1+iota).

Necessity: a local map to O sends x to 1. Since U^(n_i)f(z_i)=f(dy_i)=0 in the torsion-free target, it sends every z_i to zero. Hat equivariance makes its constant-term functional vanish on W. Thus x cannot lie in Z+W.

Sufficiency: if x is outside Z+W, take a linear functional annihilating Z+W and taking x to 1. To ensure the needed grading, first project onto bidegree (0,0). That projection preserves Z and commutes with the skew-graded involution, so it preserves W. Composing a separating functional on that component with the projection yields a grading-correct functional on the whole hat space. Extend it F_2[U]-linearly. It kills the differential, is hat-equivariant, and is local.

This projection argument is useful because W need not be a direct sum of individual bidegrees: 1+iota can mix two swapped bidegrees. One should not silently assume a homogeneous basis for all of W. No such assumption is needed for the criterion as used in the packet.

Hence x outside Z+W is exactly the existence of a local map C→O under the stated normalization. For a genuinely torsion knot, the only classes are O and E, and E has no such map. Therefore outside gives A=0 and inside gives A=1.

Dropping torsion is invalid. The repaired odd long box with n>1 has x=(1+iota)a in W and nevertheless has infinite order, not class E. The independent checker includes this negative scope control. It also checks O and E directly, and a separate elementary vector-space control shows why Z cannot be omitted from Z+W. That latter vector-space control is not asserted to be a knot complex.

## Execution and evidentiary limits

The complete validation used real UID and effective UID 1000. All three implementations were run against read-only snapshots. Append and file-creation attempts were denied by the operating system with errno 13, for each implementation. All snapshot hashes and every original public-file hash were unchanged afterward.

Across normal, -O, and -OO modes, there were 84 process runs:

- 9 positive runs, three implementations in three modes;
- 12 built-in negative-control runs for the original and hardened verifiers;
- 33 independent semantic-mutant runs, all rejected;
- 15 original source-mutant runs, including the 3 reproduced naive-tensor false acceptances;
- 15 hardened source-mutant runs, all rejected.

These counts intentionally include the baseline failures of validation. They must not be summarized as 84 successful mathematical verifications or as universal mutant rejection by the original.

The independent checker uses vector actions and exhaustive chain enumeration, and imports no original-verifier function. It checks 80 formal parameter choices, the literal tensor maps, two trefoil computations, 257 integer determinant residue controls, the elementary character countermodel, and the rank-test scope controls. Negative parameter values in the determinant arithmetic are algebraic controls, not an enlargement of HKL's positive-n family.

The all-n mathematical assertions are proved above and in the original reports. Finite test ranges are not offered as proofs of those assertions. No source documents, source text, dataset contents, or private coordination material are part of this derivative's public deliverables.

## Final disposition

- Mathematical partial audits: accepted within the stated scope.
- Original mathematical conclusions: no correction required.
- Original verifier tensor coverage: materially incomplete; corrected derivative supplied.
- Exact target: unresolved in this work.
- Budget: exhausted, five of five approaches.
- Full candidate: none.
- Actual-knot counterexample: none.
- Worldwide openness or novelty: not established or claimed.
