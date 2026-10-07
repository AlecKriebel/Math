# Independent mathematical and verifier audit

Problem 30001288 / OWR-3481-005 / queue rank 973. Audit date: 7 October 2026.

## Verdict and exact scope

**Accept the mathematical packet as a carefully scoped unresolved investigation, with the supplied verifier correction. Do not accept it as a solution of the connected comparison.** The recommended queue disposition remains **unsolved, 5/5**.

The following conclusions survive this independent audit:

1. The formula actually printed in the primary report, using the full rational Chow sheaf and its full Albanese reflector, fails for the projective line in codimension one.
2. For this rational Chow sheaf over the complex numbers, taking the connected part before or after the Albanese reflector gives canonically isomorphic sheaves. The proof has the required transfer-compatible splitting, including when the component vector space is not finite-dimensional.
3. The candidate connected rational comparison holds for divisors and zero-cycles on smooth projective varieties, and in every nontrivial codimension of a product of a smooth projective curve with projective space. The separately formulated calculation for smooth open curves also holds.
4. Both connected projective targets are quotients of the same sum of curve Jacobian groups. The desired compatible isomorphism is equivalent to equality of their two presentation kernels. Neither inclusion of those kernels has been proved in general.
5. The full morphic target has a genuinely nonzero rational contribution over its finite coniveau Jacobian in Walker's examples. Later results about the finite Walker intermediate Jacobian do not settle the full-target comparison.

One implementation defect requires correction: Python optimization removes the original manifest verifier's `assert` checks. The minimal patch replaces these and the matrix rectangularity assertion with explicit exceptions. No author mathematical claim requires a correction patch.

This is an independent AI-assisted audit, not external human peer review, a novelty certification, a formal proof-assistant verification, or a certification of the problem's global open status. Standard foundational theorems used by the packet were checked for their relevant statements and hypotheses; this audit does not purport to reprove the foundations of motives, Picard schemes, Lawson homology, or mixed Hodge structures.

## Snapshot authentication and source handling

The original author manifest is independently pinned by

`e3849b16c9617fdbb72cd81ce14dd282ed2fbd1b64d01664e4c14411ac2cb892`.

Every original listed payload's byte count and SHA-256 matched. The original packet was read-only throughout; the test suite verifies that its file hashes remain unchanged. All corruptions were performed on temporary copies.

The correction changes only `checks.py` and the manifest entry required to record it, together with the manifest's candidate/review labels. The corrected candidate manifest is pinned by

`8dcbfa59690c015db89b9d0ef5e5c35258fbc3bbda70618799446dd147b4e518`.

The corrected verifier SHA-256 is

`3e61850708a4b6ff45cb6003a4b96ad7d036a7dd72d1e406612259d101f88147`.

All six supplied scholarly PDFs were independently rehashed. Fresh text extraction from each PDF matched its supplied extracted text byte for byte. The mathematical inspections below therefore refer to the authenticated PDFs, rather than unverified transcriptions. The primary report's printed pages 1760–1761 were also checked visually, including the tilde notation, rational convention, full Albanese construction, and absence of a connected-component superscript in Conjecture 5. No PDFs, source extracts, source-page images, datasets, or private coordination material are included in this audit deliverable.

`SOURCE_AUDIT_METADATA.json` records only public bibliography, URLs, hashes, sizes, inspected locations, extraction-match results, and limitations. Original HTTP retrieval status was not treated as a new audit-time retrieval; the audit independently checked the supplied bytes. The public arXiv record additionally confirmed the inspected ABV version and publication information. Two DOI opening attempts failed, without blocking inspection of the already supplied PDFs.

## 1. Categories, components, and the Albanese unit

### 1.1 Conventions and range

Write (F_X^p) for the rational homotopy-invariant sheaf with transfers obtained from (T\mapsto CH^p(T\times X)\otimes\mathbf Q). For the smooth projective comparison, the dimension/codimension conversion is (r=d-p), with the usual range (0\le p\le d), since Walker's cycle dimension is nonnegative. A codimension outside that range needs a separately stated convention and is not an additional result of this packet.

The primary source works in characteristic zero with rational coefficients and retains 0-motivic objects. ABV §1.3 works étale-locally after inverting the exponential characteristic; over \(\mathbf C\), this imposes no additional restriction. Its use here with rational coefficients is legitimate. In this rational homotopy-invariant setting the Nisnevich/étale identification used in the packet is valid.

Evaluation at \(\operatorname{Spec}\mathbf C\) is exact for the sheaves under consideration. Left exactness holds for any sheaf evaluation; an étale epimorphism is also surjective on these points because a local lifting cover of this algebraically closed point has a section. This is used only over \(\mathbf C\), and is not asserted over arbitrary fields. It also shows that the Chow-sheaf value at this point is the original Chow group rationalized.

### 1.2 The unit really is epimorphic

ABV Lemma 1.3.3 gives an epimorphism of étale sheaves with transfers

\[
\mathbf Q_{\mathrm{tr}}(T)\longrightarrow \operatorname{Alb}(T)_{\mathbf Q}
\]

for every smooth test scheme (T). ABV Proposition 1.3.11 constructs the reflector by the same diagram of smooth representables mapping to a sheaf (F). Its presentation of (F) is a presentation **with transfers**, not merely a collection of maps of underlying sets. The 1-motivic subcategory is cocomplete and Serre in the ambient étale sheaf category, so the relevant colimits are ambient colimits. Taking the colimit of the displayed epimorphisms gives the unit

\[
u:F\longrightarrow\operatorname{Alb}(F)
\]

as an epimorphism. This use of colimits needs only their right exactness, not left exactness. ABV Lemma 1.3.12 supplies the universal property against arbitrary 1-motivic sheaves; using only the ordinary universal property against semi-abelian group schemes would not by itself establish that stronger statement.

Consequently the packet's use of a surjection on complex points is justified. It does not rely on a general principle that every reflector has epimorphic unit.

### 1.3 Components survive reflection

For any 0-motivic sheaf (D), adjunction gives natural identifications

\[
\operatorname{Hom}(\pi_0\operatorname{Alb}F,D)
 =\operatorname{Hom}(\operatorname{Alb}F,D)
 =\operatorname{Hom}(F,D)
 =\operatorname{Hom}(\pi_0F,D).
\]

Yoneda therefore identifies \(\pi_0\operatorname{Alb}F\) with \(\pi_0F\), compatibly with the component maps. ABV Theorem 3.1.4 applies over \(\mathbf C\) with rational coefficients and identifies this component sheaf for (F_X^p) as the constant sheaf with value (NS^p(X)_{\mathbf Q}). No finite-generation assumption on higher-codimension Néron–Severi groups is being imported from the divisor case.

### 1.4 The arbitrary rational splitting respects transfers

Let (D=\underline{NS^p(X)_{\mathbf Q}}) and (F^0=\ker(F\to D)). Choose a vector-space basis \((d_i)\) of (D(\mathbf C)) and Chow lifts (z_i\in CH^p(X)_{\mathbf Q}). Since

\[
\underline{\mathbf Q}=\mathbf Q_{\mathrm{tr}}(\operatorname{Spec}\mathbf C),
\qquad
\operatorname{Hom}_{\mathrm{tr}}(\underline{\mathbf Q},F)=F(\mathbf C),
\]

each (z_i) gives a morphism **with transfers**, with the standard degree transfers on the constant sheaf. Over this algebraically closed base, the constant sheaf (D) is the coproduct of those copies of \(\underline{\mathbf Q}\). Thus their coproduct map defines a section (s:D\to F). This works for an arbitrary basis cardinality; each element of a vector space has finite support in a basis.

The splitting gives (F=F^0\oplus D). Applying the additive component reflector and using that \(\pi_0(F\to D)\) is an isomorphism forces \(\pi_0F^0=0\). This argument does not assume that \(\pi_0\) preserves an arbitrary kernel. Applying the additive Albanese reflector next gives

\[
\operatorname{Alb}F=\operatorname{Alb}(F^0)\oplus D,
\qquad \pi_0\operatorname{Alb}(F^0)=0.
\]

Hence the map induced by the original inclusion (F^0\hookrightarrow F) identifies \(\operatorname{Alb}(F^0)\) with the kernel of the component map of \(\operatorname{Alb}F\). Its canonicity follows from this description by the original inclusion and canonical kernel, even though the proof chose (s). The proposed equality is therefore a sheaf isomorphism, not only an abstract equality of complex-point groups.

**Audit disposition:** all component/unit arguments accepted under the explicitly stated base and coefficient hypotheses. They do not justify commuting Alb with kernels over an arbitrary base or integrally.

## 2. Literal formulation and coefficient defects

For every smooth (T/\mathbf C), the projective-bundle formula gives

\[
CH^1(T\times\mathbf P^1)_{\mathbf Q}
 =\operatorname{Pic}(T)_{\mathbf Q}\oplus CH^0(T)_{\mathbf Q}h.
\]

The first presheaf becomes zero after sheafification: each of its finitely many line-bundle representatives trivializes on a common Zariski cover. The second is the constant rational sheaf, one copy on each connected component. Its transfer structure is the usual degree structure. Therefore (F^1_{\mathbf P^1}=\underline{\mathbf Q}), and the Albanese reflector fixes it because it already is 0-motivic and hence 1-motivic.

By Walker's zero-cycle comparison, (L_0H_1(\mathbf P^1)=H_1(\mathbf P^1,\mathbf Z)=0), so its morphic Jacobian is zero. The literal comparison consequently has groups \(\mathbf Q\) and zero on its two sides. This contradiction survives rationalizing the right side. The example satisfies smoothness, connectedness, projectivity, and every other relevant geometric hypothesis.

The primary printed formula was independently checked; the issue cannot be dismissed solely as a catalogue transcription error. Nevertheless, this proves nothing adverse about the corrected connected formula, whose two sides in this example are both zero.

The coefficient warning also stands independently: an elliptic curve's complex points have nonzero finite-order elements, whereas tensoring any abelian group with \(\mathbf Q\) gives a torsion-free group. An integral elliptic Jacobian and its rationalization cannot be identified as abstract groups. This is a coefficient mismatch, separate from the component mismatch.

**Audit disposition:** the literal defect is proved. It is not counted as solving the separately formulated connected problem.

## 3. Divisors and zero-cycles

### 3.1 Divisors

For smooth projective (X), the codimension-one Chow presheaf is the line-bundle presheaf. The pullback of \(\operatorname{Pic}(T)\) disappears on sheafification, leaving the relative Picard sheaf. A complex point of (X) permits rigidification; characteristic zero and projectivity give the usual Picard scheme, with abelian identity component and finitely generated discrete component group. Norms agree with codimension-one transfers, so the identification is valid in the transfer category used by Alb.

The rationalized Picard sheaf is 1-motivic, so the reflector fixes it, and its connected part is \((\operatorname{Pic}^0_X)_{\mathbf Q}\). Walker Example 5.5 identifies the divisor morphic map and target with the ordinary Picard map and its Picard variety. Both maps assign the same algebraically trivial line bundle its Picard point. This proves the stated canonical, map-compatible rational comparison, rather than just an equality of dimensions. ABV Proposition 3.3.2 is consistent with the same calculation in its stated smooth projective case.

### 3.2 Zero-cycles

For smooth projective (X) of dimension (d), motivic duality identifies

\[
\underline{\operatorname{Hom}}(M(X),\mathbf Q(d)[2d])\simeq M(X).
\]

Its zeroth homotopy sheaf is therefore the codimension-(d) Chow sheaf. The universal map from this sheaf to 1-motivic sheaves is the rational Serre–Albanese scheme. Here the extension from the ordinary semi-abelian universal property to all 1-motivic sheaves is justified by ABV Lemma 1.3.12, or directly by Proposition 3.3.5 together with Remark 3.3.6. The degree component is \(\mathbf Q\); its kernel is the ordinary Albanese variety rationalized.

Walker Proposition 2.5, Theorem 4.21, and Example 5.5 identify the zero-cycle Lawson group with (H_1(X,\mathbf Z)) as an MHS and the morphic map with the classical Albanese map. Both maps send ([x]-[x_0]) to the based Albanese image. Such differences generate degree-zero cycles on a connected smooth projective variety. Compatibility determines the comparison, and changing the base point does not change its formulation on degree-zero cycles.

**Audit disposition:** both special cases accepted. The zero-cycle duality is not available in the same form for a general higher internal-Hom object, and no such reduction is claimed.

## 4. Products of curves with projective space

Let (X=C\times\mathbf P^m), with (C) a smooth connected projective curve. The Chow projective-bundle decomposition is compatible with sheafification and transfers. For a curve, (F_C^q=0) when (q>1): its values at function fields vanish by dimension, and an unramified homotopy-invariant sheaf injects into its generic values. Negative codimensions give zero by convention. The only terms are (F_C^0=\mathbf Q) and (F_C^1=(\operatorname{Pic}_C)_{\mathbf Q}).

Consequently, for (1\le p\le m), the full sheaf has two rational component classes and one connected Jacobian factor; for (p=m+1), it has one component class and the same connected factor. This verifies the packet's distinction between the interior and top-codimension component counts. The (m=0) case is included.

For (r=m+1-p\), Nie's projective-bundle theorem gives summands indexed by (i\) with Lawson index (r-i\) and homological degree (2(r-i)+1\). If (i>r\), the degree is negative. If (r-i>1\), the curve has no cycles of that dimension. If (r-i=1\), its top-dimensional cycle space is discrete, with zero first homotopy group. Thus exactly (i=r\) remains, and the group is (H_1(C,\mathbf Z)\).

The map that survives is realized by the actual algebraic family (c\mapsto\{c\}\times\mathbf P^r\). Walker Theorem 4.22(5) applies because both varieties are projective and this is a family of cycles of the required dimension. It is a morphism of the **normalized** IMHSs. An underlying bijective morphism is an isomorphism here because the forgetful functor on IMHSs is exact and conservative; one need not posit a Hodge structure on each formal negative-index summand of the projective-bundle formula.

For the Chow inverse, intersect with (h^r\) and push forward to (C\). On a term with fiber \(\mathbf P^i\), an exponent (j>i\) gives zero by excess hyperplane intersection, (j<i\) gives zero on pushforward because a positive-dimensional fiber remains, and (j=i\) gives the original class. The resulting projector matches the unique surviving Lawson term. The cycle maps are therefore compatible.

**Audit disposition:** all claimed product cases accepted. This is a result for (C\times\mathbf P^m\), not a claim that every variety has a curve-and-Tate motive. The report's title for the approach should be understood at this stated scope; no extension to arbitrary bases is implied.

## 5. Smooth open curves and the Borel–Moore distinction

Let (U=C\setminus D\), where (D=\{p_1,\ldots,p_n\}\) is nonempty and consists of distinct complex points. Chow localization on a smooth test scheme (T\) gives a right-exact sequence whose boundary term sheafifies to \(\mathbf Q^n\), and whose middle term sheafifies to \((\operatorname{Pic}_C)_{\mathbf Q}\). Its boundary columns are the classes of \(\mathcal O_C(p_i)\). The cokernel remains 1-motivic because this category is closed under cokernels in the ambient category.

Split the degree using (p_1\). The columns then have form \(([p_i-p_1],1)\). Subtracting the first column from the others kills the degree contribution in those columns; the first column kills the degree factor itself. Hence

\[
F_U^1=(J(C))_{\mathbf Q}/\operatorname{im}(\mathbf Q^{n-1}\to(J(C))_{\mathbf Q}),
\quad e_i\longmapsto[p_i-p_1].
\]

This is a connected 1-motivic sheaf. Replacing (p_1\) changes a generating set of the intrinsic degree-zero boundary-divisor group, not the quotient.

Walker Proposition 2.5 and Theorem 4.21 identify the relevant zero-cycle homology with **Borel–Moore** homology as an MHS. The localization sequence is

\[
0\to H_1(C)\to H_1^{\mathrm{BM}}(U)\to
\ker(\mathbf Z^n\xrightarrow{\sum}\mathbf Z)\to0.
\]

The right term has type ((0,0)\). The connecting morphism from its Hodge classes to (J(H_1(C))\) assigns a boundary divisor its Abel–Jacobi class, by the localization-extension construction of the Abel–Jacobi map. The Jacobian of the type-((0,0)\) term vanishes. Walker's six-term exact sequence thus gives the quotient by the integral subgroup generated by \([p_i-p_1]\). Tensoring with \(\mathbf Q\) gives exactly the sheaf quotient's complex points. Evaluation is exact at \(\mathbf C\), as already checked.

The map compatibility is not obtained by applying the projective-only surjectivity theorem blindly to (U\). Rather, localization functoriality relates the maps on (C\) and (U\). Every divisor class on (U\) lifts to a divisor on (C\), and subtracting its degree times (p_1\) produces a degree-zero lift with the same restriction. Thus every such class is algebraically trivial and the projective comparison induces the claimed quotient comparison.

Two useful edge checks are correct:

- For any punctured projective line with nonempty boundary, both cycle-theoretic targets are zero. In particular (\mathbf G_m\) has (H_1^{\mathrm{BM}}\) of type ((0,0)\), while its ordinary generalized Albanese is (\mathbf G_m\). Ordinary homology would give a different Hodge structure and would invalidate the argument.
- For (E\setminus\{0,e\}\), with (e\) nontorsion, the rational target is (E(\mathbf C)_{\mathbf Q}/\mathbf Qe\). The ordinary generalized Jacobian instead has a one-dimensional toric part.

ABV Proposition 3.3.3 concerns a long exact sequence of **derived** higher Picard sheaves and requires a smooth closed embedding of pure codimension. The packet correctly avoids promoting this open-curve computation to an underived localization or five-lemma argument in arbitrary dimension.

**Audit disposition:** accepted with its explicit smooth-curve, finite reduced nonempty boundary, and Borel–Moore hypotheses.

## 6. Common curve generators and the exact remaining obstruction

For smooth projective (X\), set (V=CH^p(X)_{\mathrm{alg}}\otimes\mathbf Q\). Algebraic equivalence is generated by differences of fibers of curve families; normalization and completion of the parameter curves, together with closure of the family, allow smooth projective parameters. ABV Remark 2.4.3 provides the needed curve characterization. Correspondences descend through rational equivalence, and Abel's theorem identifies degree-zero Chow groups of the parameter curves with their Jacobians. Thus

\[
B=\bigoplus_{(C,\Gamma)}J(C)(\mathbf C)_{\mathbf Q}\longrightarrow V
\]

is a surjection. A set of representatives suffices; there is no proper-class problem or claim that a single curve generates (V\).

The unit (F_X^p\to\operatorname{Alb}(F_X^p)\) is epimorphic by §1.2 and surjective on complex points. If a target point lies in the connected component, any lift has zero component class because the two component maps identify under \(\pi_0\operatorname{Alb}F=\pi_0F\). ABV Theorem 3.1.4 says precisely that this lift is algebraically trivial. Hence (V\to A_X^p(\mathbf C)\) is surjective. Walker Theorem 5.7 supplies (V\to W_X^p\) as a surjection; its projectivity hypothesis is satisfied.

With (a,w\) the resulting maps out of (B\), their kernels (R_A,R_W\) define the two quotient groups. The kernel (R_{\mathrm{rat}}=\ker(B\to V)\) is contained in both. This notation denotes the whole presentation kernel of the Chow group, including redundant family presentations; the audit does not read it as an explicit generating list of rational-equivalence relations.

A map compatible with all these generators must take (a(b)\) to (w(b)\). It is well-defined exactly when (R_A\subseteq R_W\), and then it is surjective with kernel (R_W/R_A\). It is an isomorphism exactly when (R_A=R_W\). Uniqueness follows from surjectivity of (a\). This is an elementary quotient argument and makes no unsupported universality claim.

The example (a(x,y)=x\), (w(x,y)=y\) on \(\mathbf Q^2\) correctly shows that equal quotient dimensions and common generators do not identify the compatible quotient maps.

**Audit disposition:** the reduction is valid. The general equality (R_A=R_W\), and even either inclusion, remain unproved. This is the central mathematical gap, unchanged by the audit.

## 7. Full Lawson kernel, finite Walker quotient, and periods

### 7.1 The exact sequence uses the correct category

For smooth projective (X\), Walker Proposition 2.8 identifies the image of

\[
L=L_rH_{2r+1}(X)\longrightarrow H_{2r+1}(X,\mathbf Z(r))
\]

with (N=N_{r+1}H_{2r+1}(X,\mathbf Z(r))\). Let (K\) be the kernel. The objects and maps are in Walker's category of countable ind-MHSs with bounded filtration lengths. Section 3 establishes \(\operatorname{Ext}^i(\mathbf Z(0),-) =0\) for (i\ge2\) in that category, giving the six-term sequence and right exactness of (J\).

The subgroup (N\) is a finitely generated sub-MHS of the smooth projective Betti group, with rational weight (-1\). Its Hodge classes \(\Gamma(N)\) are its finite torsion subgroup. Therefore the relevant part of the six-term sequence, followed by the exact functor \(-\otimes\mathbf Q\), yields

\[
0\to J(K)_{\mathbf Q}\to J_r^{\mathrm{mor}}(X)_{\mathbf Q}
\to J(N)_{\mathbf Q}\to0.
\]

All hypotheses needed for this short exact rational sequence are satisfied. In particular, the left injectivity is not asserted integrally without quotienting by the image of \(\Gamma(N)\). The accidental left-exact wording elsewhere in Walker's proof is unnecessary; the actual six-term statement is right exact.

### 7.2 Walker's nonvanishing survives rationalization

The precise hypotheses of Walker Theorem 6.2 are an integer (r\ge2\), a smooth projective (Y\) of dimension (2r+1\) obtained from the construction in Theorem 6.1, and a smooth projective curve (C\) of genus at least one. Then (X=Y\times C\), of dimension (2r+2\). In the packet's codimension notation these examples have (p=r+2\); they are not divisor or zero-cycle examples.

The proof produces nonzero weight-(-1\) content in (K_{\mathbf Q}\) and shows that the kernel of the full morphic map to the classical algebraic Jacobian contains a quotient (V/\Lambda\), where (V\) is a nonzero complex vector space and \(\Lambda\) is countable. This quotient really has nontorsion elements: its torsion classes lie in \((\mathbf Q\Lambda)/\Lambda\), a countable subgroup, whereas (V/\Lambda\) is uncountable. More explicitly,

\[
(V/\Lambda)\otimes\mathbf Q\simeq V/(\mathbf Q\Lambda)\ne0.
\]

Walker Corollary 5.9 and Remark 5.10 give an isogeny (J(N)\to J_a\) in the smooth projective case, so its kernel is finite. An element of infinite order in the kernel over (J_a\) cannot be accounted for solely by this finite isogeny kernel. Combining this with the exact sequence above proves the packet's nonvanishing (J(K)_{\mathbf Q}\ne0\) for these examples.

Suzuki Theorem 1.1 and Achter–Casalaina-Martin–Vial's opening definitions and Theorems A–B concern the finite coniveau Jacobian. Poincaré duality identifies its lattice with (N^{p-1}H^{2p-1}(X,\mathbf Z(p))\). The support dimension (r+1=d-(p-1)\) checks the index conversion. Those results do not identify the kernel of the full Lawson group and do not imply its disappearance.

### 7.3 Weight-zero quotients can impose relations

For an extension (0\to H\to E\to\mathbf Z(0)\to0\), with (H\) of weight (-1\), let (e\in J(H)\) be its extension class. The connecting map sends (1\) to (e\). Since (J(\mathbf Z(0))=0\), the six-term sequence gives (J(E)=J(H)/\mathbf Ze\), and rationalization gives (J(H)_{\mathbf Q}/\mathbf Qe\). Thus a weight-zero quotient may impose a nonzero relation even though its own Jacobian vanishes. Taking only the weight-(-1\) piece would miss it.

This behavior does not itself contradict the motivic target category. A point (e\in A(\mathbf C)\) of an abelian variety defines a morphism \(\underline{\mathbf Q}\to A_{\mathbf Q}\) by transfers Yoneda. Its cokernel is 1-motivic, and is connected by right exactness of \(\pi_0\). Exact evaluation at \(\mathbf C\) identifies its points with (A(\mathbf C)_{\mathbf Q}/\mathbf Qe\). A 1-motivic sheaf need not be a finite-type abelian variety.

**Audit disposition:** the full-kernel and period calculations are accepted. They invalidate a shortcut through the finite Walker quotient, not the corrected comparison itself.

## 8. Executable checks, corruption tests, and patch

### 8.1 Original positive controls

The original script was run in normal and optimized child interpreters. Its deterministic JSON agrees exactly with the frozen `CHECK_RESULTS.json`, including the stated **73,323** finite assertions. The correction preserves that output exactly. The finite assertions use the explicit `require` function and remain active under `-O`.

The author controls are correctly described as finite algebra/index controls. Several are intentionally tautological or formal models of the geometric calculation; their count must not be presented as evidence that a motivic comparison theorem has been proved.

### 8.2 Independent reconstruction

`audit_checks.py` reconstructs rather than merely reruns key finite calculations:

- 21,297 matrices with entries in \(\{-1,0,1\}\), up to size (3\times3\), have their rank determined by determinant minors and compared with the author's elimination routine and a separate audit reduction routine.
- The projective-bundle indices, connected/component counts, and hyperplane projectors are recomputed, including edge codimensions and the truncated-polynomial pushforward description.
- 810 pairs of relation maps include zero maps and rank-deficient maps; nullspace inclusion is checked against rowspace inclusion. Further multi-output projection cases test strict quotient kernels, not just equal-dimensional quotients.
- 392 boundary matrices are reduced by explicit integral column and row operations into a degree block and boundary-difference block.
- 324 split-component models use varying sections, checking that the canonical map on the connected summand is independent of that choice.
- Period saturation is tested by the rank change after adding a new rational relation.

Each wrapper run completes **57,135** explicit checks in total, including regression assertions. This is separate from the author's 73,323 assertions. None of these controls implements Chow groups, sheaves, IMHSs, or algebraic cycles.

### 8.3 Optimization is exercised in the children

Two wrapper runs are recorded, one normal and one with `python3 -O`. **Each wrapper explicitly starts both normal and `-O` child interpreters.** Merely optimizing a test wrapper does not optimize its subprocesses; this audit does not make that mistake. Each wrapper records 56 verifier/invalid-input regression cases. Across both wrappers, eight additional baseline runs compare the full deterministic author JSON.

Four corruption classes are incorrectly accepted by the original verifier under `-O`:

1. Same-byte-count payload alteration.
2. Payload extension changing its byte count.
3. A wrong recorded byte count.
4. A wrong recorded SHA-256.

The original prints `Manifest integrity: PASS` in those optimized cases, because both integrity checks are `assert` statements. Normal execution rejects them. Missing files and invalid JSON still fail under optimization for unrelated I/O/parser reasons; that does not repair the bypass.

`CORRECTION.patch` replaces both manifest assertions with explicit conditional `ValueError` checks. It also makes the rank rectangularity precondition explicit, since the original optimized routine silently accepts a ragged input used by the regression test. The corrected verifier rejects every one of the four integrity corruptions in both child modes, and the ragged input in both modes. A deliberately false finite control fails in both original and corrected interpreters under both optimization choices.

### 8.4 A checksum list is not an authenticated inventory

The minimal patch deliberately retains the original verifier's scope: validate listed payload hashes and sizes. It does **not** add external manifest authentication or complete inventory validation. Both original and minimally patched verifiers can accept an unlisted extra file, a removed manifest entry, a duplicate entry, or a coherently altered payload together with its updated manifest entry. This is documented rather than concealed.

The independent audit's `strict_verify` adds the separately supplied manifest digest, fixed expected payload inventory, identity/schema checks, unique permitted filenames, nonnegative integral sizes, digest-format checks, and symlink rejection. It rejects **every corrupted packet copy** in the regression suite, including those four cases. Its checks use explicit exception logic and stay active when the wrapper itself is optimized. The trusted manifest digest must be supplied independently; a digest recomputed from an untrusted changed manifest is not authentication.

### 8.5 Reproducibility

Apply `CORRECTION.patch` to a separate copy of the author packet, preserving the original. The resulting `AUTHOR_MANIFEST.json` must have the corrected digest stated above. Then run, replacing the two bracketed paths with those copies:

```text
python3 audit_checks.py --packet ORIGINAL --corrected-packet CORRECTED
python3 -O audit_checks.py --packet ORIGINAL --corrected-packet CORRECTED
```

The two recorded result files give the complete per-case outcomes and exact counts. They omit local source paths and raw subprocess output; output hashes and exception types suffice for verification metadata.

## 9. Remaining gaps and release conditions

The only general comparison criterion established is equality of (R_A\) and (R_W\). There is still no construction of the canonical comparison in every codimension, no proof of either relation inclusion, and no general treatment of singular varieties or nonproper higher-dimensional varieties. The finite coniveau quotient does not eliminate the full morphic kernel. No assertion that all 1-motivic sheaves are finite-dimensional abelian varieties is admissible.

The five substantive approach families in the packet are distinct mathematical approaches. Source retrieval, wording checks, inherited-attempt checks, scripting, packaging, and this independent review are not additional attempts.

The original inherited-attempt gate is a historical bounded search report. This audit authenticated its packet files but did not rerun the large datasets, branch enumeration, or repository-wide search, and does not independently certify those historical match counts. The mathematical audit does not depend on completeness of that gate. A small additional public literature search found the original primary discussions and finite Walker-target work; it supplies no global absence theorem about later research.

For a source-free release, preserve the unresolved disposition and attach this audit and its exact correction. A release that uses the original uncorrected `--verify-manifest` under optimization must not claim integrity verification. If later edits change any payload or the manifest, the present digest-bound acceptance does not automatically apply to those changed bytes; regenerate and recheck the appropriate manifests and record the revised scope. Historical author statements that review was pending describe the frozen author snapshot; this separate audit supplies the newer, limited disposition.

## References used in the audit

- [OWR] Joseph Ayoub, “n-Motivic Sheaves,” in *Algebraic K-Theory and Motivic Cohomology*, Oberwolfach Report 31/2009, printed pp. 1760–1762. [Official PDF](https://ems.press/content/serial-article-files/46231?nt=1).
- [ABV] Joseph Ayoub and Luca Barbieri-Viale, *1-motivic sheaves and the Albanese functor*, inspected arXiv:math/0607738v2; journal publication, *J. Pure Appl. Algebra* 213 (2009), 809–839. [Version record](https://arxiv.org/abs/math/0607738).
- [W] Mark E. Walker, *The morphic Abel–Jacobi map*, *Compositio Mathematica* 143 (2007), 909–944. [Publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4A44146CE680F4F3C857048FDEDD9F48/S0010437X07002278a.pdf/the-morphic-abel-jacobi-map.pdf).
- [N] Zhaohu Nie, *Blow-up formulas and smooth birational invariants*, *Proc. Amer. Math. Soc.* 137 (2009), 2529–2539. [Public scholarly PDF](https://irma.math.unistra.fr/~lfu/Activities/supporting%20files/Nie_Blow%20up%20formulas%20and%20smooth%20birational%20invariants.pdf).
- [S] Fumiaki Suzuki, *Factorization of the Abel–Jacobi maps*, *Épijournal de Géométrie Algébrique* 5 (2021), article 20. [Journal PDF](https://epiga.episciences.org/8881/pdf).
- [ACV] Jeffrey D. Achter, Sebastian Casalaina-Martin and Charles Vial, *The Walker Abel–Jacobi map descends*, inspected arXiv:2101.07506v2; journal publication, *Mathematische Zeitschrift* 300 (2022), 1799–1817. [Public manuscript](https://arxiv.org/pdf/2101.07506).
