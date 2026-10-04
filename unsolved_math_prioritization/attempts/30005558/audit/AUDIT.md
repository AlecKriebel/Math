# Independent adversarial audit: genus-one admissible-cover Hodge integrals

Date: 3 October 2026. Catalogue ID: 30005558. Original question: OWR-13750339-002.

## Verdict

**PASS: the frozen argument gives a complete source-based resolution of the stated connected-cover problem.** No blocking mathematical error was found. The result should be described as an explicit deduction from the 2025 theorem, with full credit to its authors, rather than a new solution or a newly proved independent theorem.

This verdict applies specifically to connected degree-d admissible covers of a moving genus-one target, with 2n ordered simple branch points, n >= 1, unmarked unramified sheets, and automorphism-weighted stack integration. It does not authorize an identification with a disconnected Hurwitz invariant or a stable-map invariant without the stated correction.

Frozen inputs:

- `public/SHA256SUMS`: SHA-256 `264750b5784f2d13ad1fd6367e997ec0484936abc22cdfacb27a9573a2a2fbc3`
- `public/PROOF.md`: SHA-256 `89b64f17c36c181ae7402a39cb84009c48e2a7b4f0ff686e1b8adc8f12cc8308`

All six entries in the frozen manifest verified before and after the audit. The frozen public files were not modified. This audit performed no repository publication or other remote writes.

## 1. Question and theorem gate

The [official 2023 report](https://ems.press/content/serial-article-files/47021), printed page 1492, asks for the higher-degree analogue of the displayed admissible-cover Hodge series. I inspected both its extracted text and rendered page. The factor `(2n-1)!`, the source Hodge classes, and the change `q=-exp(iu)` match the frozen statement. The degree-two identity is `tan(u/2)/24`. The report is not asking only for rationality; the rational function itself is required.

The decisive input is [Iribar López–Pandharipande–Tseng, arXiv:2506.12438v2](https://arxiv.org/abs/2506.12438v2), Theorem 1 and equation (0.5). Its one-divisor formula is unconditional. The later nondegeneracy assumption concerns reconstruction of additional invariants. I checked the complete argument in Sections 2 and 3, including the fixed-target calculation, Hodge-line inclusion, relative/descendent correction, connected/disconnected calculus, and trace evaluation. In particular, the factor `P(1+log P)` already occurs in the source's families stable-map calculation. That provides a useful consistency check, but does not replace the separate admissible-cover argument audited below.

The correspondence input is [Pandharipande–Tseng, August 2025 revision](https://people.math.ethz.ch/~rahul/HilbC2-2025-August.pdf), Theorem 4. I checked Section 0.6, the orbifold normalization in Section 3.2, and the full correspondence proof in Section 11.1. The paper's Section 0.7 also explicitly identifies the orbifold virtual contribution with the associated Hurwitz–Hodge integrand. Standard prior genus-zero, R-matrix and virtual-localization results remain stated theorem dependencies, rather than being reproved here.

The rationality gap in the published 2019 argument is genuine and acknowledged in the revision. The 2025 divisor paper's footnote 7 states that the needed analytic-continuation correspondence was unaffected. The frozen argument uses the revision and obtains rationality of this particular divisor invariant directly from its explicit trace formula. It therefore does not silently rely on the defective earlier rationality argument.

## 2. Compactification, Hodge classes and source components

The relevant compactification is the admissible-cover stack, or its normalization by twisted stable maps. Normalization has generic degree one and preserves integrals of the pulled-back Hodge classes against the fundamental class. Hodge bundles refer to the complete coarse source curve, with unstable rational components contracted when necessary. Such contractions do not change `H^1(O)` or the Hodge bundle.

Connected components of the complete source must be distinguished from irreducible components of a nodal source. The frozen argument uses the former. An irreducible source can split at a boundary point while the full connected source and its arithmetic genus remain unchanged. On an étale labeling cover of the relevant moduli component, its connected components, degrees and allocation of branch markings can be tracked. Symmetric statements descend. Equivalently, the orbits of global monodromy determine these components, including at the admissible boundary. The normalization has no extra maximal-dimensional components supported only over singular targets.

Every connected source component maps with positive degree onto the full target. Riemann–Hurwitz gives genus `1+b/2` for a component carrying b simple branch points; b is even. A component with no such branch point has arithmetic genus one. Nodes do not create an additional free branch count: the balanced admissibility condition supplies the matching node contributions.

Let h be the target Hodge class, pulled back from the stabilized one-pointed target. Then `h^2=0`. For every positive-degree connected component C, pullback of dualizing differentials embeds the target Hodge line into the source Hodge bundle. The node calculation uses logarithmic dualizing differentials: locally, `x=u^e` takes `dx/x` to `e du/u`, with the corresponding balanced expression on the other branch. Trace composed with pullback is multiplication by the degree. In characteristic zero this gives a split line inclusion, including at the nodal boundary. Finite flatness of the coarse nodal covering map is not needed for this differential statement.

Consequently, for source genus g,

- `lambda_g = h lambda_(g-1)`;
- `h lambda_g = 0`;
- for g >= 2, Mumford's relation gives `lambda_(g-1)^2 = 2 lambda_g lambda_(g-2)`;
- hence `lambda_g lambda_(g-1) = 0`, as a class, not only after integration.

The genus-one case must be treated separately. The frozen proof does so: its source Hodge line is isomorphic to the target line. It does not incorrectly apply the genus-at-least-two identity involving `lambda_(g-2)` to genus one.

## 3. Localization degree and elimination of multiple branched components

Set `s=t1+t2`, `v=t1*t2`. For each connected source of genus g, the normal factor is

`N_g = product_j (t1-alpha_j)(t2-alpha_j) / v`.

The denominator occurs once per connected component because `H^0(O_C)` has dimension one. There is no denominator for every sheet. For g >= 2, put `b=2g-2` and `A_g=lambda_g lambda_(g-2)`. Direct expansion and the preceding relations give:

- terms of codimension greater than b vanish;
- the codimension-b term is `(s^2/v) A_g`;
- `h [N_g]_(b-1) = -s A_g`.

For g=2, the term with `lambda_(g-3)` is zero by convention, and the last relation still holds. For g=1, `N_1=1-(s/v)h`.

Suppose a disconnected cover has total branch number B and r branched connected components. Its base stack has dimension B, and the maximal codimensions from the branched factors add to B. If no unramified component contributes h, every branched factor must have maximal codimension, yielding a factor `h^r`. If exactly one unramified factor supplies h, exactly one branched factor drops by one codimension; the other r-1 maximal factors and the unramified factor again supply `h^r`. More than one unramified h-factor vanishes immediately.

Thus r >= 2 contributes zero in every case. This is a class-and-dimension argument on the compactification, not an open-locus count. It allows branch collisions and nodal target degenerations. In particular, the tempting possibility of two independently branched degree-two components does not leave a hidden contribution in degree four.

For one branched component and ell unramified components, multiply its factor by `1-ell(s/v)h`. Its required top term is

`(s^2/v) A_g - ell(s/v) h [N_g]_(b-1) = (s^2/v)(1+ell) A_g`.

The extra ell is essential. Discarding the lower Hodge-degree term of the branched component before doing this multiplication would incorrectly lose it.

## 4. Attachment counts, automorphisms and boundary pushforward

For a fixed smooth elliptic target, connected unramified covers of degree m are classified by index-m sublattices. There are `sigma_1(m)` isomorphism classes and m deck transformations per cover. The weighted number is therefore `sigma_1(m)/m = sigma_(-1)(m)`.

The exponential formula correctly accounts for repeated isomorphic components and their permutation automorphisms. Writing `L(Q)=sum_m sigma_(-1)(m) Q^m`, the unweighted attachment series is `exp(L)=P`, while counting the number of connected attachments gives `P L`. The total correction is consequently `P(1+L)`.

These are generic stack degrees. After forgetting the unramified attachments and normalizing or rigidifying the target as required at nodes, the map is proper and generically finite over the branched-cover stack. The branched Hodge class and h pull back from that stack. Projection formula therefore computes the pushforward of the fundamental cycle using the generic degree. Boundary ramification does not add a new top-dimensional contribution or an arbitrary extra stabilizer multiplier. This is why counting only smooth-target covers is sufficient for this specific degree computation, although it would not by itself prove a general boundary intersection identity.

A concrete degree-four check is informative. A degree-two branched component may have a degree-two connected unramified attachment, weighted `3/2` and multiplied by 2, or two degree-one attachments, weighted `1/2` and multiplied by 3. Their sum is `9/2`, exactly the coefficient of `Q^2` in `P(1+L)`. In degree three, the unwanted disconnected term is exactly twice the degree-two connected series.

All branch points lie on the unique contributing branched component. The extra unramified sheets are not individually marked. There is consequently no further binomial or sheet-label factorial.

## 5. Phase, free branches and coefficient extraction

For the transposition partition tau, `length(tau)-d=-1`. The correspondence gives `Hilb(tau)=i Sym(tau)`. Since `D=-tau`, this becomes `Sym(tau)=i Hilb(D)`. Combining it with the negative `1/24` in the divisor theorem gives the frozen phase `-i/24`. The degree-two identity independently fixes the sign.

The distinguished insertion contributes one branch point. The remaining `b=2n-1` branch points are quotiented by their symmetric group in the orbifold definition. Thus their contribution is divided by `(2n-1)!`, exactly as in the question. It is not divided by `(2n)!`.

Dividing the disconnected series by `P(1+L)` cancels the theorem's `1+L`. Counting occurrences of parts in partitions then turns its remaining normalized trace into the divisor sum. This proves the displayed rational and cotangent forms. Finally, the Laurent pole cancels for each divisor separately, and the cotangent coefficients give

`I_(d,n) = |B_(2n)| (sigma_(2n+1)(d)-sigma_1(d))/(48n)`.

The extension to d=1 is harmless: both the empty branched stack and the formula give zero. The stated range n >= 1 is necessary and is respected throughout. There is no asserted unramified n=0 integral with the displayed factorial or Hodge indices.

## 6. Degree-five source discrepancy

I inspected the rendered source page, so the discrepancy is not an extraction artifact. With `R_d=T_d+sum_a sigma_(-1)(a)T_(d-a)`, the partition trace at q=0 gives

`T_2=-1, T_3=-4, T_4=-12, T_5=-26`,

hence `R_5=-26-12-6-4/3=-136/3`.

The displayed degree-five example on page 7 has the opposite constant. More decisively, the independently written verifier proves that its entire displayed rational function equals `-R_5`, not `R_5`. The theorem's expansion starts

`-136/3 - 277q/6 + 41q^2/6 - 17q^3/3 - 151q^4/6 - 127q^5/6 - 101q^6/3 - 277q^7/6`.

Thus the printed rational example and its accompanying series contain one overall sign inconsistency with the theorem and their preceding trace combination. The frozen proof uses the trace theorem, whose sign agrees with degrees two, three and four and with the source's derivation. Calling this an example-level sign error is justified; it is not being waved away to conceal a disagreement with the theorem.

## 7. Exact controls and limits

- The supplied verifier passed all 248 exact assertions. Its output was byte-for-byte identical to the frozen `verification.json`.
- A separately authored verifier, which does not import the supplied verifier, passed 123 additional exact assertions. It uses dynamic partition counts, recursive formal division, direct cotangent expansion, and a full rational comparison of the degree-five example.
- Independent ranges: degree 1–12 for extraction and inversion, degree 1–8 and branch-pair index 1–7 for coefficients, and unramified attachment counts through degree 12.
- The degree-two values `1/48`, `1/96`, `1/48` for n=1,2,3 include the restored factorials.

These controls support the algebra, normalization and transcription. They are not a formal proof of the geometric correspondence, Hodge identities, compactification facts or virtual localization. The geometric reasoning and explicit theorem dependencies above are essential to the verdict. No new priority is claimed, and this independent audit remains an AI-assisted, unrefereed review.
