# Independent original-source and prior-result review: PR1260 / 30000663

**Verdict: full prior negative coverage of the literal original quotient question.** The map on the exact surface in PR1260 is globally étale and commutes with the identical effective multiplicative-group action; its algebraic quotient is ramified. I found no mathematical gap in this counterexample or mismatch with the catalog target. The existing construction is credited to Adrien Dubouloz and Karol Palka, *The Jacobian Conjecture fails for pseudo-planes*, Advances in Mathematics 339 (2018), 248–284, [DOI 10.1016/j.aim.2018.09.020](https://doi.org/10.1016/j.aim.2018.09.020). No new mathematical result or earliest-priority conclusion follows from this review.

This is a new independent AI mathematical/source audit of the pinned eight-file PR, not a claim that the historical edition already contained a second independent audit. It is unrefereed and is neither external human peer review nor formal proof-assistant certification. Only the review/checker/receipts authored in this directory are new. The earlier mathematical publications, their dates, and their authorship remain separate from these review artifacts.

## Exact input and original quantifiers

The reviewed head is `a033499db12d47fdf9fb6fce5c6a0f1044dc9a07`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. A fresh live read matched this head. All eight actual head files and the full PR body were read; the base-to-head diff has exactly eight additions under `attempts/30000663/`, with no QUEUE change. The target's cached original statement hashes to `f029af39895f8c62ff9e7adfadcb05783c141cd59b4882d2cd15278ffc869c0d`, equal to the head catalog binding. The original cached research report is empty; its dated “open” label is not evidence against an actual prior construction.

I freshly recovered [the official OWR 01/2007 PDF](https://ems.press/content/serial-article-files/46087?nt=1), 641,506 bytes, SHA-256 `a9b3fa5ac48466165296f9825711a2fb3e05e142e0585bc969d19005c9157ca7`. Miyanishi's contribution is the entire printed p.74 / PDF p.70. I read PDF pp.69–71 and visually inspected p.70, so the beginning and end of this contribution are established independently of the PR's extraction.

The contribution starts with a normal affine complex variety, an effective algebraic-group action, and an unramified endomorphism commuting with that action. Its quotient question asks whether the induced endomorphism of the algebraic quotient is unramified. Surjectivity and properness are absent. The finiteness assertions are conjectural conclusions, not extra hypotheses on the selfmap. Even if one separately imposes the displayed conditional hypothesis that the base map is finite, this example's base map is finite. The Euler-number-one condition belongs to the separate automorphism question. The factorial surface conditions occur in the additive-group special case and subsequent derivation question; they are not hypotheses on the general quotient question. There is no license to move any of these conditions onto target 30000663.

The source's printed affirmative assertion for connected reductive groups is incompatible with the counterexample below, because the multiplicative group is connected reductive. This is a mathematical contradiction to that unrestricted assertion, rather than a reason to silently strengthen the question. The answer proved here is to the literal original and catalog formulations. A formulation requiring surjectivity remains outside this result.

## Independent complete reconstruction of the needed counterexample

Put `A=C[x,y,z]/(x²y−z²+1)` and `X=Spec A`. The defining polynomial is primitive as a polynomial in `y` over `C[x,z]`, and is linear irreducible over `C(x,z)`. Gauss's lemma makes `A` a domain of dimension two. Its gradient is `(2xy,x²,−2z)`. Simultaneous vanishing would require `x=z=0`, impossible on `X`. Thus this integral affine complex surface is smooth and therefore normal.

Let `G=Gm` act by `t·(x,y,z)=(tx,t⁻²y,z)`. It preserves the equation and is effective, as seen at `(1,0,1)`. Define

`φ(x,y,z)=(2xz,y,2z²−1)`.

If `F=x²y−z²+1`, then `F∘φ=4z²F`, so the polynomial map is a regular selfmap everywhere. Its three coordinates have weights `(1,−2,0)` under the source action. These are exactly the target weights; in particular no isogeny `t↦t²` and no changed target action enters the equivariance statement.

Use target coordinates `(u,v,w)` with `B=C[u,v,w]/(u²v−w²+1)`. Define two target opens `U1=D(w+1)` and `U2=D(v(w−1))`.

On `U1` the inverse-image algebra is

`B[1/(w+1)][t]/(t²−(w+1)/2) ≅ A[1/z]`.

The inverse formulas are `x=u/(2t), y=v, z=t`; `t` is a unit. For the surface equation, multiplying by `4t²` gives `u²v−4t⁴+4t²=u²v−w²+1=0`. The coordinate compositions give `u=2xz`, `v=y`, `w=2z²−1` exactly. The monic quadratic makes the algebra finite free of rank two, and `2t` is invertible since `(2t)·t/(w+1)=1`. This proves finite étaleness on this chart.

On `U2` the inverse-image algebra is

`B[1/(v(w−1))][s]/(s²−(w−1)/(2v)) ≅ A[1/(xy)]`.

Both `v,w−1` are units and hence so is `s`. The inverse formulas are `x=s, y=v, z=u/(2s)`. The identities `s²v=(w−1)/2` and `u²/(4s²)=(w+1)/2` verify the surface equation and both coordinate compositions, including the third coordinate. The derivative unit identity is `(2s)·vs/(w−1)=1`. This is again a finite free étale algebra of rank two. The exact pullback of the inverted target function is `2x²y²`, so its source localization is indeed `A[1/(xy)]`.

These are a cover of the entire source: `z=0` implies `x²y=−1`, so both `x` and `y` are nonzero and the second chart applies. At `x=0` one has `z=±1`, so the first chart applies, including the two points with `x=y=0`. Therefore the argument proves global flatness and unramifiedness, hence global étaleness, rather than generic nonsingularity alone.

As a separate check, the ambient derivative has determinant `8z²`. Its vanishing at `z=0` does not detect ramification of the surface map. At such a point `x,y≠0`, and the tangent map is `(dx,dy,dz)↦(2x dz,dy,0)` on the source plane `2xy dx+x²dy=0`. Its kernel is zero. On the locus `z≠0` the ambient derivative is already invertible and maps the smooth two-dimensional tangent planes isomorphically. This explicitly disposes of the most plausible false negative at the exceptional locus.

For the invariant ring, weights on monomials give `i−2j=0`, hence `C[x,y,z]_0=C[x²y,z]`. The degree-zero part of the principal ideal generated by the homogeneous degree-zero polynomial `F` is exactly `F·C[x²y,z]`: take weight components of any multiplier, using that multiplication by nonzero `F` is injective. Thus

`A^G=A_0=C[q,z]/(q−z²+1)=C[z]`.

This is a ring calculation, with no assumption that a categorical quotient is a geometric orbit space. The induced quotient map is `ψ(z)=2z²−1`. Its relative differential module is `C[z] dz/(4z dz)`; the fiber at `z=0` is nonzero. Equivalently, `ψ(z)+1=2z²` has ramification index two there. This supplies the required failure of unramifiedness.

The image is exactly `U=U1∪U2=X\V(v,w+1)`. To see the union equality on `w=−1`, the surface equation gives `u²v=0`, and membership in `U2` is exactly `v≠0`. Each rank-two chart is faithfully flat, so every point of either target open is in the image. Alternatively over `C`, if `w≠−1`, choose either nonzero root `z²=(w+1)/2`, then `x=u/(2z), y=v`. If `w=−1,v≠0`, necessarily `u=0`; choose either root `x²=−1/v`, and put `z=0,y=v`. There are two distinct preimages in each case. The omitted locus is the entire target line `(u,0,−1)`, for arbitrary `u`, not only its origin. It has no preimage because `y=0` forces `z=±1` and thus `w=1`.

Finiteness and étaleness are local on the target, so `X→U` is finite étale of degree two. Its composition with the open immersion `U→X` is dominant and nonsurjective. The omitted line excludes surjectivity and, since the image is dense and not closed, properness. Both properties were checked rather than assumed. The original question requires neither. The difference in stabilizers is also permissible: a point with `z=0` has trivial stabilizer, whereas its image `(0,y,−1)`, `y≠0`, has stabilizer `μ2`. Equivariance alone does not preserve stabilizers.

The essential imports in this direct proof are standard: Gauss's lemma, the hypersurface Jacobian criterion and smooth-implies-normal, the grading description of torus invariants, the monic-polynomial/unit-derivative étale criterion, target locality and faithful flatness of nonzero constant-rank finite étale algebras, and the relative-differential unramifiedness criterion. No nonstandard classification, simply-connectedness theorem, surface completion theorem, Thom existence lemma, or general converse from the cited paper is needed to complete this explicit counterexample.

## Published construction, version identity and essential proof inspection

I freshly downloaded and actually read [arXiv:1701.01425v2](https://arxiv.org/pdf/1701.01425v2): 597,765 bytes, SHA-256 `41150cfda4fdf477efefc7d2ce55bc5fb49941705620b567b3333df5fe84281e`, 26 pages. Text read: pp.1–4, 6–11, 17–21. Visual inspection: pp.18–21. This includes the surface and action, quotient and degenerate fibers in Examples 2.11–2.12; the étale conventions; Lemma 2.18 with its multiplicity proof; the relevant same-action fiber argument in Lemma 2.22(2); Lemma 4.1; all of Theorem D's statement, converse and proof; and Example 4.3 with its continuation. The entire classification and every paper cited by those sections have not been audited.

Example 4.3's Chebyshev formula at `d=2, λ=1` gives precisely `(2xz,y,2z²−1)` on the same surface. A necessary-form discussion by itself would not prove existence. Here the converse in Theorem D additionally applies: in that theorem's normalization take

`k=r=d=2, a=1, α=0, R0(t)=4, R1(t)=1−2t, R2(t)=1, λ=2`.

Equation (4.3) becomes `4t(1−t)=1−(1−2t)²`; the degrees in (4.4) are `(d0,d1,d2)=(0,1,0)`; `(1−t)R0R1R2=4(1−t)(1−2t)` has distinct roots; `R1(0)=R2(0)=1`, `R0(0)=4`; `k|r`, `a=1`, and the congruence (4.7) all hold. Formula (4.6) then has coordinates `2xz, y, 2z²−1`. The two different uses of the scalar symbol in Theorem D and Example 4.3 are not interchanged.

The essential part of that converse constructs a polynomial with the required branching profile and applies the multiplicity criterion. In this specialization the explicit polynomial `4t(1−t)` supplies existence, so no black-box existence theorem is required. Lemma 2.18's divisor calculation compares the multiplicity of each contracted-by-the-fibration curve with its image multiplicity. For this map, at each `z=±1` the components `y=0` and `x=0` have multiplicities one and two, respectively, and map to their respective components over `w=1` with base ramification one. The reduced fiber `z=0` maps into the multiplicity-two component `u=0,w=−1` away from the intersection, matching base ramification two. General fibers map by multiplication by nonzero `2z`. Quasi-finiteness at all points, needed in an application of the general converse, follows here from the independently proved two charts and two-point fibers. Thus no possibly implicit quasi-finiteness step in the general lemma is used as a substitute for proof. The source proof is consistent with the direct certificate in precisely the specialization used.

Crossref's fresh record, the DOI publisher redirect, the primary publisher's indexed bibliographic page, and the current arXiv page agree on title, both authors, journal, volume, pages, and journal DOI. The current arXiv history has only `v1` (2017-01-05) and `v2` (2018-09-05). The unversioned PDF freshly equals the explicit v2 bytes. The canonical arXiv DOI `10.48550/arXiv.1701.01425`, versioned/unversioned arXiv pages and PDFs are aliases of this same paper, not additional independent solutions. A primary institutional publication listing associates HAL `hal-01429264`; that is another repository lead for this same title and DOI, not another credited solution. The retrieved HAL page is a challenge page, so no HAL body/version is certified.

The publisher-formatted mathematical body was not accessible: the PDF endpoint returned 403, and its text API returned 429. The DOI redirect itself returned a linking page, not article text. I therefore authenticate the published identity and reconstruct the inspected author v2 construction, but do not claim publisher-PDF inspection or byte identity, or that every general theorem/dependency in the journal paper was independently verified. Those access limits leave no gap in the explicit counterexample just proved. They are preserved in the proposed ledger wording.

## Adversarial checks and reproducibility

The new `verify_independent.py` is a standard-library-only checker authored after the source/proof reads. No downloaded mathematical programs were executed. It uses rational polynomial arithmetic and exact finite-field elimination, without floating point or removable `assert` guards. Its rational normal form eliminates `z²` by the surface equation and checks map preservation, both inverse-chart surface identities with cleared denominators, the derivative-unit identities, exact localization pullbacks, source/target action weights, and the Theorem D parameters. The general mathematical arguments above, not bounded enumeration, establish the algebra and all complex points.

All three actual runs (ordinary Python, `-O`, `-OO`) produced byte-identical passing JSON. Each run checks 57 invariant monomials through total degree 16, all 1,098 points on the surface over the seven fields of orders 3,5,7,11,13,17,19, all 1,098 surface tangent kernels, 15,720 same-action evaluations, exact chart coverage and rational fiber counts. The exceptional checks include 150 points with `x=0`, 68 with `z=0`, and 14 with `x=y=0` across those fields. Rational fibers may be empty because a square root need not be rational; the checker correctly checks zero-or-two rational points, not false surjectivity on rational points.

Fourteen deliberately false variants are rejected in every mode (42 rejections total): changing the first-coordinate coefficient, quotient constant, quotient quadratic coefficient, second-coordinate sign, or missing first-coordinate factor; changing the action weight or twisting the target action; changing the first-chart sign or second-chart denominator; corrupting `R0`, the theorem scalar, or degree; claiming only the origin is omitted; and using the characteristic-two version of the quadratic étale criterion. A false inference from the ambient determinant at `z=0` is directly opposed by the exact tangent-kernel tests and the written local proof. These controls test actual altered mathematical inputs and stated boundary conditions, rather than checksums alone.

## Duplicate/package search, proposed row and exact remaining limits

The new numeric-gid GWS read at 2026-10-22 08:57:31 UTC preceded substantive mathematics: workbook `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, gid `1254632077`, returned 43-column range `A1:AQ1178` with 191 nonempty rows. No exact problem, original code, author or journal/arXiv lead was present. This is a bounded ledger observation, not a worldwide priority search. The current 28 repository release records likewise contained no target/source-alias match. Five exact Zenodo API searches returned 403; empty web-index results do not repair that limitation. No absence of existing external packages, earliest resolution, or global novelty is certified.

`proposed_row.json` and the identical four-cell TSV contain a local-only, four-literal-string proposal. B is exactly empty, C is the authenticated existing journal DOI, and D credits Dubouloz–Palka, states the full original negative scope and nonsurjectivity, distinguishes author-v2 inspection from publisher-body inspection, and identifies the review as AI-only. The row is not a claim that a new project deposit or DOI exists. No service write, upload, DOI reservation, release, merge, Git mutation, CASE/cursor edit or outreach was performed.

There is **no remaining mathematical or original-target coverage gap** for the literal negative answer. Publisher-body access, exhaustive external-package/priority coverage, human peer review, and the strengthened surjective variant remain unverified or outside scope. They must not be converted into accepted claims. The bounded absence of duplicate leads is not a novelty proof. Previous sealed PR1235, PR1239 and PR1253 review directories were preserved and checked read-only at closure. This review's complete seal includes private inputs and all nested manifests, excluding only its exact own seal file; the separate public manifest does not authorize distribution of the private source or ledger bodies.
