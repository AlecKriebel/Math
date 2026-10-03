# Independent adversarial audit

**Target:** 30005507 / OWR-13750328-012, Frobenius–Schur Indicators in Real Nilpotent Blocks  
**Date:** 3 October 2026  
**Decision:** **PASS — SCOPED PARTIAL / UNSOLVED (five approaches)**

The frozen ten-file packet is mathematically suitable for release as an explicitly unresolved investigation. No blocking error was found in its stated partial results. It neither proves the general conjecture nor supplies an actual counterexample. Its numerical obstruction defeats only a specified inference from incomplete numerical data; its conditional reconstruction retains the missing local hypotheses.

This decision is an audit of the frozen packet, not a certificate that the conjecture remains unresolved in all literature. The mathematical source statements were independently checked against the supplied primary paper and original Oberwolfach report. No new remote publication, repository operation, or live literature/history search was performed. The packet's bounded search and provenance descriptions are not upgraded to independently exhaustive claims.

## 1. Integrity and independent controls

All ten release filenames, byte lengths, and SHA-256 values match the frozen author manifest. The original verifier was executed with a non-main run name, so it did not rewrite its frozen JSON. Its computed result equals the frozen JSON exactly: 32 compatible marked Q8 extensions, 160 model-character indicator comparisons, and 800 inner products. Hashes were checked again after the replay.

A separate, standard-library verifier was written without importing the author's group or character routines. Its main tests require no scholarly PDF, source corpus, private context, network access, or third-party package. It constructs explicit representations over Q(zeta_8), performs exact rational arithmetic, and adjoins a primitive cube root for the induced model characters. It tests the following additional families:

| Base group D | Automorphisms | Compatible marked (alpha,z) pairs | Irreducible characters |
|---|---:|---:|---:|
| C1 | 1 | 1 | 1 |
| C2 | 1 | 2 | 2 |
| C4 | 2 | 6 | 4 |
| C8 | 4 | 16 | 8 |
| D8 | 8 | 16 | 5 |
| D16 | 32 | 48 | 7 |
| Q16 | 32 | 48 | 7 |
| **Total** | | **137** | |

Here D8 and D16 have orders 8 and 16. Marked presentations are not counted as pairwise nonisomorphic groups. Exact output counts are in `independent_results.json`; the controls include:

- Exhaustive associativity for the constructed extension tables: 3,280,008 triples.
- 909 corrected-flip, invariant-space, and biduality tests, including 108 tests involving non-real character values.
- Full local square-count Fourier identities at 1,821 group elements.
- 337 central cyclic quotient root-count identities, including central elements of order greater than two.
- 21 character-side central-quotient identities in actual principal 2-blocks of the tested 2-groups.
- 909 direct induced model-character indicator sums and 6,233 pairwise model-character inner products across all 137 extensions.
- The complete 64-element Q8 × Q8 product-character Fourier calculation.

These checks extend the packet's arithmetic coverage. They still test local group calculations and solvable models, not arbitrary nilpotent blocks. They are audit controls, not a sixth mathematical approach or new evidence from the unresolved ambient cases.

### Controls that must fail when a formula is altered

1. In D8 = <r,s | r^4=s^2=1, srs=r^-1>, take alpha(r)=r, alpha(s)=rs and z=r. These data occur inside D16, with t an outside rotation and t²=r. The degree-two corrected indicator is +1. Replacing z by z^-1 gives -1. Omitting the correction makes the plain flip fail to commute with the invariant projection. Replacing the biduality map rho(z) by the identity also fails equivariance. This covers the noncentral-square case absent from the author's Q8 tests.
2. Take D=C4 inside E=C8 and let u generate D. There are two outside square roots of u, one outside involution in E/<u>, and no outside involution in E. Thus 2=2·1−0; dropping the factor 2 fails.
3. The incorrect Q8 × Q8 sign assignment has the right scalar value but differs from the true full Fourier data at six elements, for the fixed assignment used by the control. This is a diagnostic of the missing information, not a claim that any block has those incorrect signs.

## 2. Exact target and attribution

The packet retains all four essential restrictions: a **real, nilpotent, nonprincipal 2-block** of a finite group. It uses its actual defect pair (D,E), with [E:D]=2. It does not replace the pair by the abstract defect group, forget the embedding D≤E, or extend the assertion to arbitrary blocks with one simple module. The D=1 boundary is included correctly.

The requested height-preserving bijection and its coset-square indicator formula agree with Sambale's Conjecture B in *Real characters in nilpotent blocks*, and with Conjecture 2 on printed p.1055 of the original report. Theorem 3 on p.1056 states precisely the abelian/dihedral defect and solvable/quasisimple ambient cases. The paper attributes the dihedral case to Murray, obtains the abelian case in Theorem 10, derives the quasisimple case using An–Eaton, and proves the solvable case in Theorem E. The frozen packet does not claim any of these cases as new.

The report's Conjecture 4 has materially stronger local data: a compatible subsection, a unique projective indecomposable character in its local block, and an orbit-by-orbit equation for each y with y²=x. It must not be confused with the scalar projective-indicator Conjecture C in the paper. The packet distinguishes these formulations and the adjacent target correctly. Its reference to the later dihedral paper is contextual; the stronger local equation itself is directly visible in the original report and is not needed as an additional unverified theorem.

The paper explicitly says its implication from Conjecture C to B is not block-by-block. The packet respects this warning throughout. None of the inspected primary statements supplies the general missing theorem. This is a bounded source check; it is not an independent repetition of the author's live search or historical duplicate search.

Primary references:

- [Original Oberwolfach report, pp.1055–1056](https://ems.press/content/serial-article-files/47014?nt=1), [DOI 10.4171/OWR/2023/19](https://doi.org/10.4171/OWR/2023/19).
- [Sambale, Real characters in nilpotent blocks](https://arxiv.org/abs/2301.13440), especially Theorem A, Conjectures B–C, Definition 7 and the following paragraph, Proposition 8, and Theorems 10, 13–14 and E.
- [Author's version of that paper](https://benjaminsambale.github.io/pdfs/realnilpotent.pdf), internally dated 5 February 2023 in the supplied copy.

## 3. Attempt 1: universal model and induction

**Result: PASS with the stated existing-model scope.**

The normal subgroup H=C3×D has index two in G=C3⋊E. The two conjugates of theta⊗lambda are distinct because their C3 restrictions differ. Clifford theory therefore gives an irreducible induced character of degree 2lambda(1), and gives the asserted complete parametrization. The model's unique nonprincipal block, nilpotence, realness, and defect pair are existing facts explicitly recorded after Definition 7 of the primary paper; the packet cites rather than invents them.

For the indicator sum, the H contribution is zero because squaring permutes C3 and the sum of either nontrivial C3 character is zero. Outside H, every (a,e) has square (1,e²). The induced character at that square has the two displayed lambda terms, and conjugation by t permutes the outside coset. Dividing their total contribution by 6|D| gives exactly the stated |D|^-1 coset-square sum. This argument handles a noncentral t² and non-real lambda.

The height normalization is correct: |G|_2=2|D|, so the defect offset is one, while the induced degree has 2-part 2lambda(1). A degree-2^h character of D consequently gives height h. At D=1 the model is S3 and the degree-two defect-zero character has indicator +1.

The C4≤D8 illustration correctly distinguishes the model block from the group-algebra block of C4. Its purpose is to show that forgetting the extended pair and form structure loses indicator information. It does not compare blocks with the same defect pair and does not contradict the conjecture. The unresolved transfer to arbitrary B remains visible.

## 4. Attempt 2: corrected flip, forms and coherence

**Result: PASS, including the noncentral z convention.**

With alpha(d)=tdt^-1 and z=t², the relations alpha²=Ad(z) and alpha(z)=z have the stated orientation. For pi(d)=rho(d)⊗rho(alpha(d)) and R=(I⊗rho(z))S, direct multiplication yields

    R pi(d) = pi(alpha(d)) R,
    R² = rho(z)⊗rho(z) = pi(z).

Thus R commutes with the averaging projection and squares to one on its image W. The invariant space is naturally Hom_D(V*, V∘alpha); Schur's lemma gives dimension zero or one. This proves the stated nonzero criterion without assuming that alpha itself is an involution.

The trace identity has the correct order of factors. In pi(d)R, the second factor before the flip is rho(alpha(d))rho(z); tracing produces lambda(d alpha(d) z), and (dt)²=d alpha(d) z. Therefore Tr(R|W)=g(lambda), including the sign. There is no missing complex conjugation in this trace calculation.

For tau(d)=alpha(d)^-1, tau is an anti-automorphism, tau²=Ad(z), and tau(z)=z^-1. Applying the contravariant duality twice gives action rho(z d z^-1) on the ordinary vector-space bidual. The map v↦rho(z)v is therefore the required intertwiner; ordinary evaluation without rho(z) is generally not an intertwiner. The identity tau(z)=z^-1 also supplies the usual compatibility of this weak biduality.

A morphism to the dagger dual corresponds exactly to the displayed invariant bilinear form. Under the natural pairing of invariant forms with W, its adjoint is the transpose of R:

    B(v,w) ↦ B(w,rho(z)v).

Its square is the identity because pi(z) acts trivially on invariants. Hence the form-space trace really is the same g(lambda), not merely its absolute value.

The positive coherence equation is well typed. Both sides map F(V) into F(V^dagger)*. Naturality of a applied to f:V→V^dagger, followed by that equation, shows that f↦a_V F(f) intertwines the two adjoint involutions. Since the block is real, ordinary contragredient duality stays inside its ordinary representation category. The trace on a simple's invariant-form space is its ordinary Frobenius–Schur indicator. Consequently the conditional implication is valid, provided F also has the expressly required height compatibility.

The rescaling warning is correct on a duality-fixed simple. These dualities are complex-linear on morphisms, so dualizing a scalar does not conjugate it. Scaling the comparison changes both sides of coherence by the same scalar; it cannot reverse a negative coherence defect. No form-preserving Morita equivalence is actually constructed or silently assumed.

When alpha is the identity, z is central, and the formula g(lambda)=omega_lambda(z)epsilon_D(lambda) follows immediately. The two Q8 extensions correctly keep the duality permutation fixed while changing the degree-two sign. The transpose/symplectic-transpose algebra analogy is likewise valid. Both examples illustrate why the extra sign information is indispensable; neither is a same-pair block counterexample.

## 5. Attempt 3: numerical underdetermination

**Result: PASS as an obstruction to the stated inference only.**

At each height, matching the three indicator counts is necessary and sufficient for an arbitrary height-preserving indicator bijection. Theorem A supplies the real-character counts using the extended stabilizer, with Proposition 8(i) relating that action to E. Nilpotent-block parametrization supplies total counts and the single decomposition column lambda(1). Thus the scalar projective formula really yields the displayed single weighted equation.

The Q8 × Q8 character calculation is exact: 16 linear positive characters, 8 degree-two negative characters, and one degree-four positive character. Its scalar sum is 4. Changing two of the degree-two signs to positive and the degree-four sign to negative gives the same scalar sum and preserves all real counts and positive height-zero signs. The remaining integer equation has exactly the two stated solutions.

Neither assignment conflicts with the listed numerical constraints, but only the first is asserted to be realized by the specified local pair. The paper's additional local restrictions are not assumed in this numerical argument. The frozen text repeatedly identifies the second assignment as hypothetical and explicitly declines a counterexample claim. That distinction is necessary and is maintained.

The assertion that one unknown signed count is determined by the scalar formula, or that enough independent equations determine all counts, is elementary linear algebra under exactly those hypotheses. It does not assert the existence of the additional equations for arbitrary blocks.

## 6. Attempt 4: reconstruction and quotient factors

**Result: PASS as a conditional reconstruction.**

The square-count function is D-class-invariant, has total mass |D|, and is invariant under inversion. Character orthogonality gives its Fourier coefficients as conjugates of the coset-square averages. Those averages are real by Attempt 2, so the stated expansion is correct.

The decomposition-number form d^u_(Gamma(lambda),phi_u)=sigma(u)lambda(u), with sigma(u)=±1, is used only for nilpotent blocks with the designated 2-rational positive height-zero character. These are the structural facts used in the primary paper's Theorem 14. The packet does not assert them for arbitrary blocks with l(B)=1.

Assuming the full subsection identities, multiplying by sigma(u) and taking the trivial-character coefficient gives

    1 = |D|^-1 sum_u sigma(u)q(u) ≤ |D|^-1 sum_u q(u) = 1.

Each summand of q is nonnegative. Therefore every place with q(u)>0 has sigma(u)=1; signs elsewhere have no effect. Fourier uniqueness then fixes every indicator for this particular Broué–Puig bijection. No converse from the bare existence of some matching bijection is claimed.

### Character-side quotient identity

For central 2-element u, Schur's lemma gives the central scalar of an irreducible character. If the character is real, that scalar is ±1, and it is +1 exactly for characters inflated from the quotient by <u>. Non-real characters contribute zero to the indicator sum. Generalized decomposition at central u is this scalar times the ordinary decomposition number; deflation preserves the latter. Separating the +1 constituents therefore gives

    sum epsilon(chi)d^u_(chi,phi) = 2epsilon(bar(Phi)) − epsilon(Phi).

The factor 2 is forced by this separation. Inflation of bar(Phi) is being used to compare ordinary constituents, not to claim that inflation preserves projectivity. The packet makes that distinction. The identity applies more generally than nilpotent blocks when the stipulated unique Brauer character is present.

### Root-count quotient identity

For a central cyclic subgroup Z=<u>≤D0, each outside involution in E0/Z is represented by e with e²=u^k. If |u|>1, exactly two lifts square to 1 when k is even and exactly two square to u when k is odd. These two alternatives partition the quotient's outside involutions, yielding

    #outside roots of u = 2I(E0/Z,D0/Z) − I(E0,D0).

For u=1 the same displayed formula is tautological. This proof does not assume |u|=2 and is valid with the stated centrality condition. In the block application, the central 2-subgroup is contained in the local defect group. Centrality in E0 is essential; the formula has not been extended to arbitrary noncentral quotients.

### Scope of the unsupplied hypotheses

To combine the two identities, the scalar projective formula must hold for the relevant local block and its dominated central quotient, not merely for the starting block. Nilpotence ensures the needed one-Brauer-character conditions in the applicable local sections. The subsection and defect pairs must be chosen compatibly as in the primary paper; arbitrary incompatible local choices are not covered.

For a nonprincipal starting block, the relevant correspondents and central quotients stay in the nonprincipal setting needed by Conjecture C. Non-real local blocks contribute zero and use the convention with no outside local coset. For nonsplit real local pairs, Proposition 8(ii), together with l(b)=1, gives a zero projective indicator and a zero involution count. Split quotients can still arise from nonsplit extensions: if e²=u, its quotient image is an outside involution. The packet correctly identifies these split local or quotient cases as the unresolved uses.

The argument therefore reproduces the conditional reduction of Theorems 13–14 without concealing an induction assumption. A proof of the scalar formula for one initial block alone would not discharge it.

## 7. Attempt 5, summaries and final disposition

**Result: PASS for the advertised finite scope.**

The original program enumerates all images of the marked Q8 generators, verifies the automorphisms and extension compatibility, and checks the constructed extension laws. Its 24 automorphisms and 32 compatible pairs are correct. Its values lie in exact integer arithmetic in Z[zeta_3]. All 800 inner products and 160 direct square sums reproduce the frozen result.

The eight ordered indicator vectors, each occurring four times, and the four forms up to permutation of the nontrivial linear characters agree with the output. The degree-two coordinate is correctly last. The listed outside-involution counts and the alpha=identity sign diagnostic are correct. The outside-square support is {1,−1} in both diagnostic extensions, but its multiplicities are reversed. Square support by itself consequently does not determine the nonlinear sign.

The README and research log accurately summarize the proof boundaries. The five approaches are distinguishable mathematical mechanisms, although none settles the target. Their subjective progress percentage is explicitly described as a planning estimate and has no evidentiary role in this audit. No new theorem or priority claim is attached to the known model or published reconstruction.

**Release disposition:** accept the packet only with its existing **unsolved, 5/5** classification and explicit conditional/finite boundaries. No mandatory correction to the frozen mathematical text is required. The audit provides no permission to relabel the target solved, claim a conjecture counterexample, generalize the equivalence criterion into an existence theorem, or report the finite models as unresolved ambient cases.

## Reproduction and artifact scope

Run `python3 independent_controls.py` in this audit folder. It writes only `independent_results.json` alongside itself. If the original release and author manifest occupy their existing sibling locations, it additionally verifies their hashes and performs a read-only replay. When those files are absent, all independent controls still run and the optional frozen replay is marked not requested.

The audit deliverables are this report, the portable verifier, its exact JSON results, a compact verdict, and a checksum manifest. No scholarly PDF, full source text, raw catalogue, private context, or operational history is included in them.
