# Independent adversarial audit: Problem 2306111

Date: 2026-10-04 UTC. Rank 590; AMR-022-6111 / Hayman–Lingham Problem 6.111.

## Verdict

**ACCEPT AS AN UNSOLVED PARTIAL-RESULT PACKAGE.** No complete proof or counterexample is present. The three advertised partial results withstand this audit. No fatal mathematical error or mandatory mathematical correction was found. Retain `unsolved`, five substantive approach turns used out of five, and the explicit current-literature limitation.

This is an independent human-readable mathematical audit with finite computational controls, not formal proof verification. It does not certify novelty, comprehensive literature coverage, or that the problem is still open in 2026. The sharp lower inclusion into the starlike class remains unproved.

## 1. Frozen object and scope

Audited directory: `submission/`, as supplied to the reviewer. The SHA-256 of its `SHA256SUMS.json` is

`ae165b2cec8fdf989e9081fe0bfb1b0921aa788c24ded9f8192323a23f79aa8b`.

All 15 listed payload files match their recorded lengths and hashes. The manifest itself is a sixteenth file and is deliberately outside its own payload map. The same manifest and payload hashes were checked after review. No submission file was edited. All audit files and replay outputs are separate in `audit-independent/`. No remote writes were performed.

The reviewer read the complete mathematical argument, source gate, manifests, validation limits, status, five-route log, turn records, README, and computational source and outputs. Review included the primary source's rendered target page and extracted text, the complete selected corpus record, the relevant Yagmur theorem, and the live Fournier publisher page. The saved repository gate was read; its live branch/PR/code negative checks were **not independently repeated** in this audit. Publication coordination should recheck its own current repository state as appropriate.

## 2. Statement and parameter audit

The primary page agrees with the submitted closed weighted coefficient ball: the coefficient distance uses the weights n and a non-strict inequality. It asks for starlike normalized univalent functions throughout the unit disk, not merely local or global univalence and not merely a smaller disk.

Within -1 <= B < A <= 1, the second reported positive range is equivalent to A+B >= 0. The complement of the two reported ranges is exactly

-1 <= B < -(2+sqrt(3))/4, and B < A < -B.

Both equality boundaries belong to the recorded positive theorem. B=0 is never in the missing region. The B=0 formulas retained for the all-parameter deductions are nevertheless necessary and correct. The source gives no present-day status certificate.

Primary source: [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed page 156 / PDF page 157. Its archived PDF matches SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.

## 3. Proposition 1: sharp uniform univalence

### Lower inclusion

The real-part minimum for h(w)=(1+Aw)/(1+Bw) over |w| <= t is (1-At)/(1-Bt). Denominators are positive for every allowed parameter pair and t<1. The minimum is positive even when A=1 or B=-1, because these are interior-disk estimates. Thus the Janowski condition does imply convexity of f.

For nonzero z=re^(i theta), differentiation along the radius gives

 d/dt log|f'(t e^(i theta))| = Re(p(t e^(i theta))-1)/t.

Schwarz's lemma and the preceding minimum imply the submitted derivative bound m(r). The integral has its removable limiting value at t=0. For B != 0, differentiating log m(r) gives -(A-B)/(1-Br)<0; for B=0 it gives -A<0, since A>0 in that case. Therefore m(r)>delta for r<1. B cannot equal 1 because B<A<=1, so the limit m(1)=delta is always finite and positive. The B=0 expression is also the continuous B-to-zero limit.

The weighted coefficient estimate |h'(z)| <= r delta is valid for infinite perturbation series, since their absolute weighted sum is finite. Thus |h'/f'|<1. Consequently Re(g'/f')>0 on the whole disk, including z=0. Composition with the conformal inverse of f is legitimate on the convex open domain f(D). Integration over each line segment in this domain proves injectivity of g without relying on an unsupported implication from nonvanishing derivative. This closes the global-univalence step.

### Sharpness and quantifiers

The extremal f0' is a nonvanishing analytic function: Re(1+Bz)>0 on D permits the stated logarithm branch. Its primitive satisfies the correct Janowski differential equation, is convex, and is normalized. At z=-r its derivative is exactly m(r), a positive real number. For every eta>delta, the perturbation (eta/2)z^2 has exactly coefficient distance eta and forces a derivative zero strictly inside D by the sign change m(r)-eta r. This gives an actual failure of local univalence, not merely equality at a boundary point.

The conclusion is a **uniform** sharp radius for each fixed pair (A,B), over all permitted centers. It is not a statement that every individual center has exact radius delta; for example, the identity center admits the larger radius 1 when delta<1. The package's wording already uses the correct uniform quantifier.

The sharpness argument also proves that any positive answer to the original starlikeness inclusion could not have a larger uniform coefficient radius. It does **not** prove that inclusion at delta. The distinction is preserved in the submission. If an open coefficient-ball convention were used instead, any radius eta>delta would still fail by choosing an intermediate perturbation norm between delta and eta. The source and package consistently use the closed ball, so no convention change is needed.

## 4. Proposition 2: exact quadratic-witness reduction

This is the most delicate claim and passes independent inspection.

For fixed theta and z, the coefficient of c_n in the real pencil is

 (n cos(theta)-2i sin(theta)) z^(n-1).

Its modulus divided by the coefficient weight n is at most r, because n>=2. At n=2 the factor is exactly 2z exp(-i theta), so every complex value in the radius-r operator image ball is attained by a single quadratic coefficient. The norm is therefore exactly r, including all theta and not merely one selected direction.

The real matrix columns are d and -2i q. Its Gram off-diagonal entry is -2 Im(d conjugate(q)); its trace and discriminant give precisely equation (4). In particular, the 16 in that discriminant and the 4 in the determinant inequality (9) are correct. Its Gram determinant simplifies to 4 Re(d conjugate(q))^2. Direct numerical construction of the matrix independently confirms these identities.

If sigma>eta r everywhere, perturbation cannot make any pencil member vanish. The theta=pi/2 member excludes all nonzero zeros of g. Hence W=zg'/g is analytic on D after its removable extension at 0, where W(0)=1. The other pencil members exclude every purely imaginary value, since 2 tan(theta) ranges over all real numbers. Connectedness then puts W in the right half-plane. This establishes starlikeness, not just absence of zeros.

Conversely, compactness of the real unit circle gives an attaining direction when sigma<=eta r. Formula (7) has coefficient norm sigma/r, so the constructed quadratic perturbation lies in the **closed** coefficient ball even at equality. If its pencil equation comes from cos(theta)=0 it has a forbidden second zero; otherwise it either has a second zero or reaches a purely imaginary logarithmic derivative. Both violate normalized starlikeness. No hidden assumption of an attained infimum over points z is made.

Therefore any failure of the complete coefficient-neighborhood inclusion has a quadratic witness, but showing that no such witness exists is still the full remaining mathematical problem. Equation (9) correctly uses strict positive definiteness and is equivalent to the stated pointwise singular-value condition. A derivative lower bound alone controls only one Gram diagonal and cannot supply its determinant.

## 5. Explicit models, measure representation, and finite tests

The primitive formula in section 4 is correct: differentiating its numerator produces the factor A, so division by A is appropriate. A=0 and B=0 are explicitly removed by integration or limits. The log and half-plane special cases are correct.

On the negative radius in the missing parameter region, d=m(r)>0 and q is the average of (1+brt)^(-beta), at least d. The two matrix columns are orthogonal, and their smaller norm is d. Hence the boundary limit sigma=delta at z=-1 is valid. It is not an interior obstruction: for every interior r, m(r)>delta r. This is a correct sharpness stress test, not a proof that this ray or model is globally extremal.

The elementary quadratic control family's sharp radius 1-2|a| is also correct. At the lower radius, its neighborhood is contained in the identity neighborhood of radius 1. The latter is starlike by the submitted coefficient calculation, with strictness supplied by r<1. Increasing the quadratic coefficient beyond modulus 1/2 forces an interior derivative zero. The imposed |a|<=1/4 is sufficient for convexity and causes no edge problem.

At B=-1, the Herglotz representation is exact for all probability measures. The logarithms have the right normalization; locally uniform integration justifies the formula for f'. Conversely the construction has a nonzero derivative and a positive-real-part convexity criterion, so it does belong to the claimed class. For b<1 the Janowski image is a convex disk, and at b=1 it is a half-plane. Thus the finite weighted averages do give a valid subclass. No unjustified complete representation for b<1 is asserted.

The 15 fixed searches and four exploratory seeds were replayed with exactly the submitted bounds, seeds, and iteration limits, without enlarging the proof-search budget. The fixed-search JSON and exploratory stdout match byte-for-byte. The ordinary control output matches parsed JSON; its captured stdout has one extra terminal newline from print(), which has no mathematical effect.

Additional independent controls constructed the real matrix directly in 5,000 cases, checked the exact identity-center boundary behavior and rational derivative-zero bracket, differentiated the extremal at high precision for parameter-edge controls, and recomputed the existing 15 stored search points with 60-digit mpmath quadrature rather than the submitted Gaussian quadrature. All passed. Details and exact numerical residuals appear in `INDEPENDENT_RESULTS.json`.

These tests do not establish the missing universal inequality. The optimizer is not globally certified, quadrature is not interval-validated, angles near the singular phase are excluded, only finitely many parameter pairs are considered, and an arbitrary Herglotz measure need not have finite support. For b<1 there are also centers outside the displayed subclass. A strict, rigorously certified boundary violation could be continued inward; an approximate equality or a positive search outcome cannot.

## 6. Proposition 3: source-dependent smaller disk

The dilation step is valid: omega(rz)/r is analytic, vanishes at 0, and has modulus at most |z|<1. Thus f(rz)/r is in K[rA,rB]. The coefficient distance of the dilated perturbation is at most r delta, and delta(rA,rB)=m(r)>delta>=r delta.

In the missing range, R=c0/|B| lies in [c0,1), so evaluation at r=R is permissible and sends the lower parameter to exactly -c0. The recorded theorem includes this boundary. It follows that g_R is starlike on D, equivalently that the restriction of g to |z|<R has a starlike image about 0. The infimum guaranteed R over missing parameters is exactly c0, attained when B=-1.

**R is a guaranteed domain-of-starlikeness radius, not a proved sharp domain radius.** The package makes no sharpness claim for R. It also does not upgrade this smaller-disk result plus global univalence to starlikeness on the outer annulus. Its dependence on the theorem as recorded by Hayman–Lingham is clearly declared; this audit did not obtain or verify the original 1989 proof.

## 7. Literature and provenance limits

The 2020 Fournier publisher page confirms the article identity and presents subscription-preview content. Its accessible abstract does not identify the precise questions resolved. This audit did not obtain its full text and does not infer an answer from the title, abstract, citation list, or the lack of a search hit. The material literature gap must remain.

- [Fournier 2020](https://doi.org/10.1007/s40315-020-00347-4)
- [Sheil-Small–Silvia 1989](https://doi.org/10.1007/BF02820479)

The inspected Yagmur theorem displays (A-B)t/[8(t+1)], with positive t, so its radius is at most (A-B)/8<=1/4. In the target's missing range, (1+b)^(-beta)>1/4. This confirms that the displayed theorem does not itself furnish the requested radius; it is not a comprehensive assessment of all possible consequences of that paper.

The two private pinned corpora and the Yagmur PDF were rehashed and agree with the submitted source manifest. They were not copied into the audit deliverables. Neither source PDFs, corpus contents, extracted source text, nor screenshots are included in the publication-oriented audit files. Hash matching establishes byte identity only.

## 8. Disposition and corrections

Mandatory mathematical corrections: **none**. See `CORRECTIONS.md` for optional clarity notes and the conditions that must survive any later summary or publication.

The only unresolved mathematical assertion is still the universal strict lower bound sigma_f(z)>delta(A,B)|z|, over every missing parameter pair, every center in the class, and every nonzero interior point, or a certified violation within those exact quantifiers. This audit contributes verification rather than a sixth research approach. The package remains **unsolved, 5/5**, and must not be promoted to `claimed_solved` or `already_solved`.
