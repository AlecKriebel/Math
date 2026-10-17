# Independent audit of cellularization vanishing

## Verdict

**Accepted for the full stated mathematical scope. No proof correction is required.**

The audited argument proves that, for every prime p, every field k of characteristic p, and every compact Lie group G whose component group is not p-nilpotent, the canonical map

\[
\Gamma_k C_*(\Omega((BG)^\wedge_p);k)\longrightarrow C_*(\Omega((BG)^\wedge_p);k)
\]

is zero on all homotopy groups. Completion is applied to BG before taking loops.

This covers the positive-dimensional case in Greenlees's Question 2.2 and does not require an orientable adjoint action. This verdict records the separate mathematical audit of the specified proof. The manuscript and audit are AI-assisted and unrefereed. Acceptance does not mean external human peer review, journal acceptance, formal proof-assistant certification, or a novelty certificate. It is not a claim that the map is null in the derived category.

The distributed [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md) has **15,361 bytes** and SHA-256:

`c985406f6b9b456a220baecc70f836dd98bb0ba950a153b08e35e5677ff8b23b`

This public edition preserves every analytic argument of the accepted proof. Editorial changes reconcile completed acceptance, remove private coordination references and bind the distributed report. No mathematical proof correction was required. References below to the candidate describe the proof reviewed by the original audit.

Audit date: 10 October 2026. Problem: 30006658 / OWR-14299915-021.

## Exact target and source correspondence

The official Oberwolfach report identifies J. P. C. Greenlees as the author of the contribution beginning on printed p. 592. Question 2.2 appears on printed p. 594, PDF page 54. It asks about the full homotopy map for a positive-dimensional compact Lie group with non-p-nilpotent component group. The nearby untwisted duality theorem has an orientation hypothesis; the question's cellularization map still makes sense without that identification. The candidate proves this broader formulation directly. See the [official report](https://ems.press/content/serial-article-files/53607?nt=1).

The exact map is an R-module cellular approximation, not a transfer on ordinary group homology, a completion of kG substituted for chains without justification, or merely a projection to component-group homology.

## Lemma 1 and graded signs

The finite-ideal theorem is correct. Lomp's §2.4 explicitly gives the finite one-sided ideal criterion for free Hopf algebras over a coefficient ring; over a field this is the required ordinary result. The candidate also supplies an adequate proof, so its use is not dependent on an unsupported attribution to Sweedler. See [Lomp's primary manuscript](https://arxiv.org/pdf/math/0307046), pp. 4–5.

The important details of the supplied argument check as follows:

1. The coefficient space obtained by contracting the second factor of the coproduct of a finite-dimensional ideal is finite-dimensional and contains that ideal.
2. Coassociativity makes this coefficient space a right coideal. The displayed antipode cancellation proves closure under right multiplication. Thus it is a right Hopf module, with precisely the required compatible action and coaction.
3. The coinvariants in the regular right comodule lie in k times the unit: applying the counit to the first tensor factor proves this immediately.
4. The Hopf-module theorem therefore forces the ambient Hopf algebra to be finite-dimensional if this coefficient space is nonzero and finite-dimensional.
5. The left-ideal reduction through the opposite-and-coopposite Hopf algebra is legitimate with the same antipode. No inverse antipode is required.

In odd characteristic the underlying graded Hopf algebra cannot simply be treated as an ordinary Hopf algebra. The candidate correctly handles this using parity bosonization. Its multiplication, coproduct, counit and antipode formulas agree: when checking coproduct multiplicativity, the relevant sign exponent is

\[
(|h_2|+i)|a_1|+i|a_2|=|h_2||a_1|+i|a|\pmod2.
\]

This is exactly the graded bialgebra sign combined with the smash-product sign. The antipode formula respects both convolution identities. A graded left ideal remains a left ideal after adjoining the parity element because the parity action preserves it; the analogous right-ideal assertion also holds. The bosonized algebra has twice the vector-space dimension.

In characteristic two every Koszul sign is 1, so forgetting the grading really does give an ordinary Hopf algebra. No semisimplicity of kC2 is invoked, and the proof does not need bosonization in characteristic two.

## Lemma 2 and finite approximation

This is the decisive categorical step and it is sound.

DGI Definition 4.6 and Remark 4.8 give a compact proxy K with Loc(K) = Loc(k). DGI Theorem 4.9 applies to the compact object K; it is not being improperly applied to the possibly noncompact residue field. With E = End_A(K), the right-E-module convention and the inverse functor \(-\otimes_E^{\mathbf L}K\) are consistent with DGI's conventions. See [Dwyer, Greenlees and Iyengar](https://arxiv.org/pdf/math/0510247), §4; the retained publisher version has the relevant theorem on printed p. 376.

Here is an independent check of the approximation argument. Choose a semi-free DG right-E resolution F of a module N. Its generators admit a well-order such that each generator's differential is a finite linear combination of earlier generators. Form the dependency tree of a finite collection of generators. Each vertex has finitely many children, and there can be no infinite path because the labels strictly decrease in a well-order. A finitely branching infinite tree would have an infinite path, so the entire dependency tree is finite. Its closure therefore generates a finite semi-free submodule.

The finite dependency-closed subsets are directed under union and exhaust F. Their inclusions are relative semi-free maps. Filtered colimits of complexes compute their homotopy colimit, and every element and every homology class of F is represented in one such finite submodule. This argument remains valid for an unbounded DG algebra and does not impose a bound on the degrees of all generators.

Derived tensor with K preserves this homotopy colimit and carries each finite semi-free submodule to an object finitely constructed from K. Since K is finitely constructed from k, each resulting A-module P has finite-dimensional **total** homotopy: finite sums, suspensions, cones and retracts preserve that property. The resulting maps P to M are A-linear. This proves exactly the class-by-class factorization used in Proposition 3.

The argument never tries to commute Hom_A(k,−) with arbitrary coproducts or assumes that k itself is compact. It also makes no invalid inference that all cellular modules are themselves finite-dimensional.

## Proposition 3 and the canonical map

For an A-linear map P to A, its image on homotopy is a graded left ideal in the regular left module \(\pi_*A\). The total homotopy of P is finite-dimensional, so this image is a finite-dimensional graded ideal. Lemma 1 forces it to be zero when \(\pi_*A\) is infinite-dimensional.

Lemma 2 applies this argument to every individual class in any k-cellular source M. Therefore every A-linear map from M to A is zero on homotopy. The canonical cellularization map is one such map. If right-module conventions are preferred, the right-ideal version of Lemma 1 gives the identical conclusion.

No multiplicative structure on the source is required. No assumption that the image is a Hopf ideal is made. The conclusion concerns induced homotopy maps, and does not imply a null morphism: the proof does not invoke any false detection of morphisms by homotopy groups.

## Topological hypotheses and arbitrary fields

DGI §5.7, printed p. 382 in the publisher version, explicitly treats X = (BG)^∧p for an arbitrary compact Lie group, over Fp, and proves proxy-smallness for both cochains on X and chains on its loop space. Its proof uses the finite homogeneous space SU(n)/G, Eilenberg–Moore convergence and double centralizers; no orientation assumption occurs there. The orientation assumption used later for Gorenstein duality is irrelevant here. The hypotheses cited in §4.22 and Proposition 4.17 are supplied within §5.7.

Extension of scalars from Fp to k preserves finite constructions, retracts and colimits. Consequently a compact proxy K0 extends to a compact proxy for k over the extended chain algebra. Chains, rather than infinite cochain duals, are being extended: \(C_*(Y;k)=C_*(Y;\mathbb F_p)\otimes_{\mathbb F_p}k\). Flatness gives the corresponding equality in homology. This works for arbitrary, including infinite and transcendental, field extensions.

Pontryagin multiplication, the diagonal and the inverse in a loop-group model induce a graded Hopf algebra structure on loop homology. The homological Künneth isomorphism over a field supplies the tensor-product coproduct. Neither connectedness of the loop space nor finite total homology is required for this step.

Ishiguro's Proposition 1.3(a), printed p. 199, says that p-compactness of BG implies p-nilpotence of its component group. The definition and discussion on pp. 195 and 198 identify p-compactness here with finite total mod-p homology of the completed loop space. The candidate uses the correct contrapositive, not the generally false converse. Thus its homology is infinite-dimensional under the hypothesis in the question. Extension of a vector-space basis to k preserves infinite dimension. See [Ishiguro's primary article](https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf).

The 2007 article is the author's explicit restatement of his 2001 Proposition 3.1. The audit inspected that primary restatement, not the original 2001 article. This is adequate evidence for the invoked theorem and agrees with the candidate's disclosure.

## Prior work and boundary checks

Greenlees's current [arXiv manuscript](https://arxiv.org/abs/2504.03050) remains version 3, dated 27 April 2026, on the abstract page inspected for this audit. Its §2.C corroborates proxy-smallness. Lemma 6.2 treats the finite-group case. Lemma 6.5 and Remark 6.6 supply restricted compact-Lie conclusions involving a nilpotent action and a spectral-sequence collapse; the candidate does not misidentify them as a proof of the unrestricted question.

The infinite-dimensional hypothesis is necessary for the proposed general criterion: for a connected compact Lie group the completed loop homology is finite-dimensional, and the cellularization can be an equivalence. This produces no contradiction. The example O(2) × S3 at p = 3 has non-3-nilpotent component group C2 × S3 and a nonorientable one-dimensional adjoint representation. It is admissible for the broad claim; it is not presented as a direct computation of the cellularization map.

## Recorded independent checks and inspection evidence

The independent audit recorded that all six source byte counts and SHA-256 values in [SOURCE_METADATA.json](SOURCE_METADATA.json) matched the inspected PDFs. The reviewed proof remained unchanged through completion of that audit. Primary PDFs were independently extracted during the audit; the decisive Oberwolfach, DGI, Ishiguro and Lomp pages were also rendered and visually inspected. The published metadata records that history without distributing source PDFs, extracted source text or images.

The independent audit recorded that the candidate's algebra checks passed in both ordinary and optimized Python, with identical output. A separate implementation was written for the parity bosonization of the **infinite noncommutative tensor Hopf superalgebra** on one even and one odd primitive generator. Operations use exact, untruncated words; only tested input lengths are bounded. For each of characteristics 2, 3, 5 and 7 it checks:

- 900 multiplicativity pairs;
- 126 coassociativity inputs;
- 252 left/right antipode cases.

All passed in the recorded audit, and ordinary and optimized runs gave identical results. This independently exercises mixed parity, noncommutativity and the characteristic-two boundary. These bounded calculations validate conventions and do not substitute for the general Hopf-module proof or the categorical argument.

The original provisional status preceded this completed audit. The public [STATUS.json](STATUS.json) records the subsequently accepted full scope; this is editorial reconciliation, not a mathematical correction or a new proof attempt. No required mathematical correction, unresolved hypothesis or scope restriction remains. Local editorial packaging itself performed no new scholarly-source retrieval, source-file rehash, source inspection, literature search or mathematical test rerun. A separately recorded supplemental bibliographic check is disclosed in SOURCE_REVIEW.md, including successful published Section 6 inspection and the unverified published-PDF identity. The analytic proof does not depend on any omitted program or raw computational output.
