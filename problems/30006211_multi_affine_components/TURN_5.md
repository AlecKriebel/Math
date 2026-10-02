# Turn 5: a two-equation product construction and a late-found prior resolution

AI-assisted mathematical research; independent review pending. Target: 30006211 / OWR-14299088-013. Fifth and final author turn, 2 October 2026.

## 1. Exact source and disposition

The source is Basu's problem, joint work with Perrucci, in Oberwolfach Reports 9/2025, printed pp. 445–446, https://ems.press/content/serial-article-files/51353 (DOI 10.4171/OWR/2025/9). It asks for a bound depending on total degree alone for the number of connected components of the common real zero set of two multi-affine polynomials in arbitrarily many variables. Multi-affine means degree at most one in each variable. The domain is all of real affine space. No smoothness, transversality, symmetry or genericity hypothesis is imposed.

The following construction answers that literal question negatively. During the final literature reconciliation, a public preprint by Alper Ferudun dated 30 September 2026 was found and its full proof read. It already gives the negative answer by the same sum-of-squares/product mechanism, using one extra variable. Therefore the recommended disposition is a **credited prior resolution (already_solved), five author turns used**, rather than a new claimed discovery. See PRIOR_RESOLUTION_ADDENDUM.md. Earlier turns' unresolved labels are historical checkpoints, not the final assessment.

## 2. Explicit construction without an auxiliary variable

For each integer m >= 2, in the 2m independent real variables x_1,y_1,...,x_m,y_m put

f_i = x_i y_i - 1,
F_m = sum_i f_i,
H_m = sum_{i<j} f_i f_j.

Then F_m has total degree 2, H_m has total degree 4, and both are multi-affine. Indeed f_i uses only its own variable pair, and products f_i f_j for i != j repeat no variable. The degree-four monomial x_1 y_1 x_2 y_2 has coefficient 1 in H_m, so the degree is exactly four, with no cancellation. All coefficients are integers.

The polynomial identity

F_m^2 - 2 H_m = sum_i f_i^2

follows by expanding a square. At a common real zero of F_m and H_m its right side is zero, hence each f_i is zero. Conversely f_i=0 for every i implies F_m=H_m=0. Consequently

Z_R(F_m,H_m) = product_{i=1}^m {(x_i,y_i): x_i y_i=1}.

No coordinate x_i or y_i vanishes there. For each sign vector s in {+1,-1}^m define

C_s = {(s_1 a_1,s_1/a_1,...,s_m a_m,s_m/a_m): a_i>0}.

The displayed parametrization is a homeomorphism (0,infinity)^m -> C_s; its inverse takes absolute values of the x_i. Thus C_s is nonempty and path connected. Each C_s is relatively open, since its signs are specified by strict inequalities, and relatively closed since its complement is the finite union of the other open sign classes. They partition the zero set. Any connected subset lies in a single class, so these are precisely its connected components. Therefore

b_0(Z_R(F_m,H_m)) = 2^m.

This tends to infinity with m while the degree bound remains 4. No bound depending only on total degree can exist in the source's generality. If both displayed polynomials must have degree exactly 4, replace the pair by H_m and H_m+F_m; they have the same common zeros and both degrees are exactly 4. If an odd ambient dimension is desired, adjoin a free unused variable, which does not change the component count.

This is a real argument, relying on the positivity of squares. The common real set is a smooth product of hyperbolas, though the two chosen equations are not a transverse presentation: their Jacobian rows are dependent on that set. The source does not require a regular complete-intersection presentation. No claim is made for that extra restriction.

## 3. General product encoding

Let f_1,...,f_k be multi-affine real polynomials of degree at most e, each supported on a variable set disjoint from all the others. Set F=sum f_i and H=sum_{i<j}f_i f_j. The same identity proves Z_R(F,H)=product_i Z_R(f_i), with free Euclidean factors if there are unused coordinates. F,H are multi-affine of degrees at most e and 2e. Thus one obtains the product's component count with two equations and without introducing an auxiliary coordinate. Empty factors give the empty set. Constant or zero factors cause no difficulty in the identity. Finite products of these semialgebraic sets have the product of their component counts.

Taking each f_i to be a product of e separate variables minus 1 gives 2^((e-1)k) components in ek variables for e>=2 and k>=2, with degrees exactly e and 2e. The one-block component count is the classical extremal example in Basu–Perrucci, Example 2.1, not a new result.

## 4. Relation to prior turns and the literature

Turn 1's nonnegative restriction theorem assumes one defining polynomial is affine; F_m is quadratic, so it does not apply. Turn 2 permits equations linear in disjoint product blocks; H_m is quadratic in those blocks, outside that family. Turns 3–4 concern bilinear pairs of degree at most two; the quartic equation is outside their scope. There is no contradiction with those upper bounds.

Ferudun's Theorem 1.2 uses T=sum x_i y_i, E=sum_{i<j}x_i y_i x_j y_j and the pair P=x_0-T, Q=x_0 T-2E-2T+m. It proves Q=T P+sum_i(x_i y_i-1)^2. Thus its real zero set is {x_0=m} times exactly the same product of hyperbolas. His Lemma 3.1 already states the disjoint-variable product encoding with an auxiliary variable. Setting that auxiliary variable to its forced zero value in the centered lemma gives precisely our pair up to nonzero constant multiples. This is an elementary elimination/specialization of the same construction, not an independent new solution mechanism.

The prior preprint is unrefereed and AI-assisted. We directly verify its negative-answer identity and topology; its publication does not certify peer review or priority. The older Basu–Perrucci hypersurface theorem, sharp product example and three-polynomial construction are explicitly credited. We make no novelty claim for any partial in the preceding turns. The cases of two general multi-affine polynomials with degree bounds 2 or 3 are not settled by this packet.

## 5. Reproducibility and limits

Run python turn5/check_counterexample.py and compare stdout with turn5/verification.json. The 4,216 exact assertions check sparse polynomial identities and degrees for m=2,...,12, sign witnesses and bounded integer controls. They supplement, rather than establish, the all-m argument above. No external downloaded program was run. The complete five-turn packet requires independent mathematical/source review before a final public disposition.
