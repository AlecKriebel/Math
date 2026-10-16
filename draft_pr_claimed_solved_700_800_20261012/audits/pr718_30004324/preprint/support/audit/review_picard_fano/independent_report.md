# Independent adversarial review of the Picard/Fano mechanism

**PR:** #718. **Problem:** 30004324. **Frozen candidate:** `tangent_seshadri_30004324_v2/candidate_proof.md`, SHA-256 `dcad7d7677b1fff7fe1b659fd5b2f2c97e4daa0f0fe7b914a7752f19ad89c5a8`.

**Verdict: PASS.** I found no mathematical gap in the assigned target-definition, very-freeness, contracted-section, numerical descent, curve-lifting, ampleness, and Fano-theorem steps. I also independently checked the minimal-degree and pointed-family inputs needed by those steps. The conclusion is conditional only on the explicitly imported established theorems, with their actual hypotheses; it does not use the conjecture being proved as an input. This is an internal mathematical audit, not a finding of novelty or external peer review. No priority audit was conducted.

The review was performed without reading historical geometry-review arguments or the other new reviews. An initial broad index search accidentally displayed historical review filenames, headings, and one restatement of the target; it displayed no historical proof reasoning. Favorable-review claims embedded in the author's candidate were disregarded. No source or original attempt was edited, no shared Git operation was performed, and no external person was contacted.

## 1. Exact hypothesis and source match

The proposition under review is:

> Let (X/k) be a smooth integral projective variety, (dim X=n\geq1), with (k) algebraically closed of any characteristic. If a closed point (x\in X) has positive Fulger–Murayama relative tangent-bundle Seshadri constant, then (X\cong_k\mathbf P^n).

This matches [Fulger–Murayama, Conjecture 4.9](https://par.nsf.gov/servlets/purl/10198624), printed p. 17, and the [Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1), printed p. 3289. The report's p. 3288 uses quotient projectivization and multiplicity of the full pushed-forward curve cycle, precisely as the candidate does. Global nefness is not an additional hypothesis.

For an integral curve (\Gamma\subset\mathbf P(E)) mapping onto (C\ni x) with total generic degree (q), the denominator is (q\operatorname{mult}_x C), not merely (\operatorname{mult}_x C). The tautological line bundle restricts positively on vertical projective-space fibers, but vertical curves are excluded from the defining infimum. These conventions are used consistently.

I directly downloaded and inspected the final-numbering NSF manuscript; its hash agrees with the author's recorded source hash. The [arXiv v2 manuscript](https://arxiv.org/pdf/1903.00610v2) corroborates the same inputs using numbering 3.23/3.24 and 5.6/5.8/5.9. The initial web-tool failures for the NSF URL do not mean the source went uninspected.

## 2. Independent check of positivity on rational curves

Let (C\subset X) be an integral rational curve through (x), and let (f:\mathbf P^1\to C\hookrightarrow X) be its normalization. Write

\[
f^*T_X\cong\bigoplus_{i=1}^n\mathcal O(a_i),\qquad m=\operatorname{mult}_xC.
\]

The candidate's normalized minimum-slope computation is correct. A Frobenius pullback sends every summand to (mathcal O(p^ea_i)), so division by (p^e) restores the same minimum. This is a special feature of (mathbf P^1); replacing normalized minimum slope by ordinary minimum slope on arbitrary curves would not be justified. The inspected Example 3.20 and Corollary 3.21 of Fulger–Murayama supply the general curve formula.

There is also an elementary independent verification, avoiding that formula. Each quotient (f^*T_X\twoheadrightarrow\mathcal O(a_i)) determines a morphism

\[
s_i:\mathbf P^1\longrightarrow\mathbf P(T_X).
\]

Its projection to (X) is (f). Hence (s_i) is birational onto its integral image (\Gamma_i): the intermediate function field lies between the identical fields (k(C)=k(\mathbf P^1)). The pulled-back tautological line bundle is (mathcal O(a_i)), and the full pushforward is (C), with generic degree one. Consequently

\[
\epsilon(T_X;x)\leq\frac{\xi\cdot\Gamma_i}{\operatorname{mult}_xC}
=\frac{a_i}{m}.
\]

Strict positivity forces every integer (a_i\geq1). This proves very-freeness in every characteristic directly from the actual definition, for singular or immersed rational images as well as embedded ones. No global nefness or semicontinuity claim enters.

The normalization map has nonzero generic differential: on an open subset of the integral curve it is an isomorphism, and that open subset can be chosen smooth over the perfect field (k). Thus a nonzero map (mathcal O(2)\to\bigoplus_i\mathcal O(a_i)) exists, forcing some (a_i\geq2). Therefore

\[
-K_X\cdot C=\deg f^*T_X=\sum_i a_i\geq n+1.
\]

Only the weaker positive value is needed later. A purely inseparable multiple cover may have zero differential; the proof does not apply the differential argument to such a cover. If a nonconstant map (g:\mathbf P^1\to X) has image (C), it factors through this normalization, with a finite map (h:\mathbf P^1\to\mathbf P^1) of total degree (e). Then (g^*T_X=h^*f^*T_X=\bigoplus_i\mathcal O(ea_i)) is still ample. This covers the map-level positivity used by the imported Fano theorem without any separability assumption on (h).

## 3. Existence and the family inputs required by the numerical argument

The specified-point existence input is genuine. Fulger–Murayama Corollary 4.6 uses the one-point hypothesis and, in its proof, produces a rational curve through that same point. It does not merely assert a rational curve through a general point of (X). Invoking its existence conclusion is legitimate even though the candidate does not reprove all its underlying bend-and-break and uniruledness results.

Choose a very ample (A) and the least positive (A)-degree (d) of a rational image through (x). The following checks close the potential gaps needed for Lemma 5.

1. **Geometric extension.** If an algebraically closed extension (K/k) contained a rational image of smaller degree (c) through (x_K), its normalization gives a degree-(c) map from (mathbf P^1_K), with a chosen preimage of (x_K) moved to (0). Fixed-degree maps to the given projective embedding form a finite-type scheme, and evaluation at (0) equal to (x) is a closed condition. A (K)-point makes this finite-type (k)-scheme nonempty, hence it has a (k)-point. That map has a nonconstant rational image through (x) of degree at most (c<d), a contradiction. This uses algebraic closedness, not uncountability.

2. **Pointed boundary.** A genus-zero stable map of total degree (d) with its mark evaluating to (x) has a tree of rational components. Along a path from the marked component through contracted components, the first nonconstant component has a rational image through (x). Lüroth's theorem applies to a subfield of (K(t)) without a separability assumption. If that component covers its image with degree (e), then (d\geq e(A\cdot C)\geq d). Positivity of every nonconstant degree term forces it to be the unique nonconstant component and forces (e=1).

3. **Contracted components.** Any contracted subtree with (t>0) vertices has one attachment to the unique nonconstant component, and at most one mark. Its total count of special-point incidences is (2(t-1)+1+m\leq2t), whereas stability requires at least (3t). Thus there is no contracted subtree. Every geometric source is a smooth (mathbf P^1), birational onto its image. Inseparable covers of degree greater than one are excluded by the same integer-degree equality.

4. **Actual universal family.** The stable-map stack is proper with projective coarse scheme in the inspected [Abramovich–Oort Theorem 2.8 and §2.5](https://arxiv.org/pdf/math/9808074). Here the actual evaluation fiber has no automorphisms. Generic injectivity of (df) also kills infinitesimal automorphisms in characteristic (p). A finite group scheme with one geometric point and zero tangent space is the identity group scheme. Fiberwise trivial finite inertia becomes globally trivial by the identity-section splitting and Nakayama's lemma. [Stacks 04SZ](https://stacks.math.columbia.edu/tag/04SZ) then gives an algebraic space. The proper map to the full coarse scheme is quasi-finite because its geometric fibers have at most one point; [Stacks 03XX](https://stacks.math.columbia.edu/tag/03XX) and [02LS](https://stacks.math.columbia.edu/tag/02LS) make it a finite morphism of schemes and hence projective. No wild coarse-space base-change claim is required.

5. **Smooth (mathbf P^1) family and marking.** Restricting the actual universal curve to a reduced integral projective component (H) gives a proper flat family (pi:U\to H) with geometric fibers (mathbf P^1), a genuine section (sigma), and a morphism (e:U\to X). Fiberwise smoothness makes (pi) smooth. The relation (e\sigma=x) holds as a morphism, by the definition of the evaluation fiber; it is not merely a statement about closed points. The degree-one line bundle (mathcal O_U(sigma)) makes (U) a projective-line bundle over (H). In particular there is no Brauer obstruction concealed by assuming a universal section.

6. **Surjectivity.** At a chosen normalization map (f),

   \[
   H^1(\mathbf P^1,f^*T_X(-0-\infty))
   =\bigoplus_iH^1(\mathcal O(a_i-2))=0.
   \]

   The fixed-source evaluation with (0) mapping to (x) is consequently smooth at (f), so its image contains a nonempty open subset. The map from the pointed Hom scheme to the smooth-domain marked stable-map space is locally the quotient by the smooth connected group (operatorname{Aut}(\mathbf P^1,0)). Its fiber is the scheme of parametrizations of a pointed (mathbf P^1). Thus the smooth local component at (f) maps into the selected component (H); it cannot jump to an unrelated component. The corresponding two-point deformations evaluate through (U). Since (U) is proper, (e(U)) is closed; since (X) is irreducible and this image contains a nonempty open subset, (e) is surjective. This uses deformation smoothness, not characteristic-zero generic smoothness. The two-point deformation calculation is also consistent with [Gounelas, Proposition 4.7](https://ems.press/content/serial-article-files/26314?nt=1).

An additional base-change subtlety is harmless: the very-freeness calculation is needed at the original (k)-map (f), whereas the geometric-boundary exclusion only needs the geometric-extension minimum and degree arithmetic. The proof does not silently require positivity of the Seshadri constant to have already been proved invariant under every algebraically closed extension. Constancy of fiber degrees then propagates the needed anticanonical degree through (H).

## 4. Fiberwise degree zero really gives descent

Fix any Cartier divisor (D) on (X). Since (H) is connected and the family is proper and flat, the integer degree of (e^*mathcal O_X(D)) on its fibers is constant. Birationality of each fiber map identifies it with (b=D\cdot C). Likewise the (A)-degree is the fixed positive integer (d). This applies to arbitrary (D), including ones of negative or zero degree; no positivity is asserted here.

Set

\[
L=\mathcal O_X(dD)\otimes A^{-b},\qquad M=e^*L.
\]

On every geometric fiber (U_{\bar h}\cong\mathbf P^1),

\[
\deg M|_{U_{\bar h}}=db-bd=0,
\]

so (M|_{U_{\bar h}}\cong\mathcal O_{\mathbf P^1}). This implication would be false for a higher-genus family; genus zero is essential. In this family (h^0=1), (h^1=0) on every geometric fiber. Proper flat cohomology and base change gives the rank-one locally free bundle (B=\pi_*M), with arbitrary base change, and adjunction (pi^*B\to M). On each geometric fiber this is the nonzero evaluation map (mathcal O\to\mathcal O), hence an isomorphism. The locus where a map of line bundles fails to be an isomorphism cannot meet any geometric fiber, so it is empty. Thus (M\cong\pi^*B).

The cited [Stacks 0B91](https://stacks.math.columbia.edu/tag/0B91) provides the derived base-change input. Alternatively, the reduced base (H), proper smooth connected curve fibers, and [0GKA](https://stacks.math.columbia.edu/tag/0GKA) satisfy all hypotheses of the direct descent result [0EX7](https://stacks.math.columbia.edu/tag/0EX7). Neither route needs normality of (H), separability of (e), nor an unproved claim that a fiberwise degree-zero line bundle is globally trivial.

Pulling the descent isomorphism back along the actual marking gives

\[
B\cong\sigma^*\pi^*B\cong\sigma^*e^*L
\cong L|_x\otimes_k\mathcal O_H\cong\mathcal O_H.
\]

The last isomorphism amounts only to choosing a basis of the one-dimensional (k)-space (L|_x). Hence (e^*L\cong\mathcal O_U). The contracted section, not merely the existence of a proper unpointed curve family, supplies this conclusion.

## 5. Curve lifts under a surjection, including inseparability

To deduce numerical triviality on (X), the test curve must be completely arbitrary. Let (Gamma\subset X) be an integral proper curve, of any genus, possibly singular and possibly avoiding (x), with generic point (eta).

Surjectivity of (e) implies that the finite-type (k(Gamma))-scheme (U_eta) is nonempty. Choose a closed point (z\in U_eta). Its residue field (K) is a finite extension of (k(Gamma)), of total degree (q>0). The reduced closure of the corresponding point in (U) is an integral closed subscheme (Gamma'). Its function field is (K); since (U) is finite type over (k), (dimGamma'=\operatorname{trdeg}_kK=1). It is a proper curve and dominates (Gamma). Its generic degree is exactly (q), without deleting the inseparable factor.

A nonconstant proper morphism between integral proper curves is finite. The line-bundle degree formula therefore gives

\[
0=\deg(e^*L|_{\Gamma'})
=q\deg(L|_\Gamma).
\]

This formula is independently corroborated by [Stacks Lemma 33.44.11](https://stacks.math.columbia.edu/tag/0AYQ). All degrees here are integers. In characteristic (p), even when (p\mid q), the positive integer (q) is not zero in this equality. It follows that (deg(L|_Gamma)=0). There is no illicit division by a zero field element and no Bertini or separable-multisection assumption.

Thus (d[D]=b[A]) in (N^1(X)_\mathbf R) for every Cartier divisor. Smoothness ensures that line-bundle/Cartier-divisor classes furnish this space. The ample class ([A]) is nonzero, since its degree on the chosen curve is (d>0), so the Picard number is exactly one. The argument does not assert that (L) is trivial on (X), nor that the entire Picard group is generated by (A); those stronger statements are unnecessary.

## 6. Numerical equivalence propagates to the needed top intersections

Let (P=-K_X), (b=P\cdot C>0), and (c=b/d>0). The preceding result is (P\equiv cA). To make the top-intersection inference fully checkable, put (N=P-cA), which has zero intersection with every integral curve on (X). For an integral (r)-dimensional subvariety (Z\subset X), multilinearity gives

\[
(P^r-c^rA^r)\cdot Z
=N\cdot\left(\sum_{j=0}^{r-1}P^{r-1-j}(cA)^j\cap[Z]\right).
\]

Each term in parentheses is a real one-cycle class, representable by a linear combination of integral curves. Numerical triviality of (N) annihilates its intersection degree with that entire one-cycle. Consequently

\[
P^r\cdot Z=c^rA^r\cdot Z>0.
\]

This explanation requires neither (Z) smooth nor those one-cycles effective; signed cycle representatives suffice. It does not confuse equality of classes in (N^1) with equality of Chow classes. The positivity on the right follows from ampleness of (A), and (P) is Cartier because (X) is smooth. The exact arbitrary-characteristic [Fujino–Miyamoto Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf) then applies and makes (-K_X) ample. This is a bona fide Fano reduction, not merely a proof of strict nefness, which would be insufficient.

## 7. The imported Fano clause and circularity check

The final-numbering source, Proposition 4.8(1), applies to a smooth projective Fano variety over an algebraically closed field, with positivity of (epsilon(T_X;x)) at some point, and concludes projective space. There is no characteristic-zero or general-point condition in clause (1). Those conditions belong to the separate clause (2), which this proof does not invoke. Its proof invokes Kollár's established Theorem V.3.2; the conjecture immediately following the proposition is not used to establish it. This is clear in both inspected versions of Fulger–Murayama.

At invocation, the proof has established every required additional hypothesis independently: ampleness of the Cartier divisor (-K_X). It retains the original field and original point (x), so positivity does not have to be transported to another point. I did not independently inspect the complete Kollár monograph or reprove its theorem; the audited imported result is the published Fulger–Murayama proposition, with its source-chain dependence disclosed. This is ordinary theorem use, not a remaining mathematical gap within the candidate's stated dependency boundary.

## 8. Edge cases and attempted falsifications

| Challenge | Check and outcome |
|---|---|
| (n=1) | (T_X) is a line bundle of degree (2-2g); the constant on the smooth curve is that degree. Positivity forces (g=0), and algebraic closedness gives (X\cong\mathbf P^1). The family argument is consistent even when (H) is a point. |
| Characteristic (2) or (p\mid q) | Splitting and cohomology remain valid. Degree identities are integer identities. Only normalization maps are used for the nonzero differential assertion. |
| Singular rational image with several branches over (x) | The quotient-section argument uses its normalization, full curve multiplicity (m), and image cycle degree one. The mark may choose any preimage; no uniqueness is required. |
| A mark initially on a contracted component | Following the constant-(x) path reaches a rational image through (x). Minimality and the special-point count remove every contracted component. |
| A higher-genus or (x)-avoiding test curve | The numerical step uses generic-fiber closed-point lifts and does not invoke the original positivity hypothesis for the test curve. |
| Nonseparable evaluation (e) | The curve-lift proof takes total extension degree. The proof of surjectivity uses smooth evaluation only at the chosen very free map. |
| Non-normal parameter space | Reduced integral (H) suffices for the quoted descent route; the direct cohomology proof needs no normality. |
| Countable algebraically closed base field | Existence of a (k)-point on a nonempty finite-type scheme replaces any very-general-point or uncountability argument. |
| Linear versus numerical equivalence | Only numerical triviality is pulled down from (U). The Fano conclusion uses all-dimensional Nakai–Moishezon, with the explicit telescoping intersection argument above. |
| Hypothetical irrational coefficient | Every needed coefficient is the rational number (b/d); there is no limiting numerical approximation. |
| Known non-projective-space examples | A quadric surface has a rational ruling with tangent splitting containing (mathcal O(0)); a product with a positive-dimensional factor has a fiber with a trivial quotient; an elliptic curve has tangent degree zero. These fail the strict-positivity hypothesis at the relevant point and do not falsify the argument. |
| (n=0) if included | A smooth integral projective zero-fold over algebraically closed (k) is already (mathbf P^0); no tangent constant is needed. |

There is no computational theorem claim here. Finite checks of special cases would not validate the general result; the checkable artifacts are the algebraic arguments and matched primary-source statements.

## 9. Review disposition

**Essential corrections required:** none in the assigned mathematical mechanism. **Counterexamples found:** none. **Exact remaining internal mathematical gap:** none identified under the explicitly cited established dependencies.

For a short preprint, I recommend retaining the full arbitrary-characteristic and fixed-point hypotheses visibly, presenting the contracted-section numerical lemma as a standalone lemma, and including the short one-cycle telescoping argument. The direct quotient-section proof of very-freeness can simplify the presentation and make the Frobenius issue transparent without requiring a general slope theorem. These are presentation improvements rather than repairs needed for PASS.

Publication still requires the separate requested novelty/priority work and reviews of the actual final preprint, references, and package. This report neither performs nor prejudges those stages. It provides no basis for asserting human peer review.
