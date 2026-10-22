# Independent audit: hook-shaped operator extendability

Problem 30005481 / OWR-12697711-017; supplied rank 951. Audit date: 7 October 2026.

## Disposition

**Accept the scoped mathematical partial results. The original conjecture remains unresolved after five substantive approaches.**

The sharp deformation threshold, the quadratic and determinantal results, the inverse-symbol criterion, and the two rational slice certificates withstand this independent review. No defect changing any stated theorem or certificate was found. One required, theorem-preserving wording correction is supplied below as an exact patch and a separately pinned corrected reading copy. Acceptance is of the explicitly limited partial results, not of a proof or disproof of the original equivalence, a novelty claim, or a fully self-contained reconstruction of the published base theorem.

The exact reviewed input is pinned by `MANIFEST.json`, SHA-256:

`a59097544b285a4d5452cad2b8dac7d80d4f437098b123f71e04ad06242d9fa7`.

All seven inventoried file sizes and hashes match. The original input files were preserved. No repository publication or queue change was performed.

### Required wording correction (no theorem changes)

In the opening conventions, replace “A scalar multiple of a map has the same extendability status” with “A **nonzero** scalar multiple of a map has the same extendability status.” The zero multiple is always extendable, so the unrestricted sentence is literally false. Every actual rescaling in the proofs is nonzero, particularly multiplication by -1/750; therefore this wording defect does not invalidate any result. Apply `WORDING_CORRECTION.patch` when preparing a corrected manuscript. The original remains untouched. The one-change reading copy `corrected/PARTIAL_THEOREMS.md` is 18992 bytes with SHA-256 `f2e0e866b9ae517ea1cdb3181546ab67f6afccd9dd604d537c64c3960984c65f`. `CORRECTION.json` pins both versions and the exact replacement. No formulas or other content were changed.

## 1. Primary source and conventions

I independently inspected the official OWR PDF, including a rendered image of printed p.868, and the arXiv PDF, including the weak-SOS definition on printed p.2. I read the relevant definitions, theorem statements, quintic proof discussion, and inverse-symbol argument. These identify the target as OWR 15/2023, Conjecture 3, and Blekherman–Lindberg–Shu, Conjecture 2.3. The primary publisher's search-indexed full-text page also retains Conjecture 2.3 in the 2025 article. A direct publisher-page request failed; this review does not treat that failed request or the retained error HTML as a full-text inspection.

Primary links:

- [OWR 15/2023, official PDF](https://ems.press/content/serial-article-files/47009?nt=1)
- [Symmetric Hyperbolic Polynomials, arXiv:2308.09653v1](https://arxiv.org/abs/2308.09653v1)
- [Published article, JPAA 229(2), 107869 (2025)](https://doi.org/10.1016/j.jpaa.2025.107869)
- [Publisher's indexed full-text page](https://www.sciencedirect.com/science/article/am/pii/S0022404925000088)

The audited conventions match the source:

1. The polynomial is homogeneous, invariant under coordinate permutations, and hyperbolic in the all-ones direction e; in particular p(e) is nonzero.
2. The cone is closed: u belongs when p(u+t e) has no positive zero. Boundary directions are included.
3. Weak SOS requires Delta_(u,v)p to be SOS for **every** u,v in that cone. A single all-ones Wronskian does not establish it.
4. For a full-degree centered-root input g=a product(t-r_i), the associated operator is a p(r-t e), extended linearly/continuously to the remaining inputs.
5. Diagonality is **degree-shifted**, not equal-power diagonality. For input degree bound n and output degree bound d, the rule is T(t^(n-i))=gamma_i t^(d-i) for i<=d, with zero output for i>d. The missing index i=1 is absent from the centered domain.
6. Source Section 4.1 uses that same shifted convention in its finite Pólya–Schur criterion. Definition 1.7 uses it for the extension. Thus the criterion applies to the entire degree-bounded input space, including lower-degree inputs, not just centered degree-n polynomials.

In particular, delta_d T = T delta_n follows on each allowed monomial: both sides multiply gamma_i t^(d-i) by 1-i. An inverse symbol f supplies the missing gamma_1; all remaining coefficients are fixed because the corresponding coefficients of g_0=(t-1)^(n-1)(t+n-1) are nonzero. This verifies the exact source-to-manuscript convention required for all five approaches. The derivative-evaluation extension g'(s t) in Approach 3 is diagonal in precisely this shifted sense.

The explicit scope 1<=d<=n and the nonzero leading coefficients avoid degree/index and zero-polynomial degeneracies. In particular, the proof of hyperbolicity for the deformed quintic checks p_epsilon(e) separately; it does not infer hyperbolicity merely from a possibly degenerate preserver.

Source-file integrity was also checked against the supplied public metadata: the OWR PDF is 644,489 bytes with SHA-256 b3a1780b4687ccb7ce238165c4fcb159f62ea86a3dc47bc2a3900806c400c4f5; the arXiv PDF is 238,960 bytes with SHA-256 29727705b3bcc867dfd43d7bab16fbad73562ac407b2f4302dd510b7f7ed5894. The supporting dissertation's reported 701,460 bytes and SHA-256 dee4c0081375592a313d79dd94e27f21b52d07adbdeba3f9b4f231380b07ae80 also match, but it is not needed as an independent theorem input.

## 2. Approach-by-approach mathematical review

### Approach 1: inverse symbols and critical values — accepted

Coefficientwise inversion of delta_d gives exactly F+c t^(d-1). The derivative identity H'=G/t^d is correct. Under Proposition 1's simple-root hypotheses, the d-1 positive roots of G are exactly the critical points of H. Its endpoint signs are (-1)^d infinity at zero and positive infinity at infinity. Each open monotonic interval has at most one zero of H+c; a zero at a simple critical point has multiplicity exactly two. Counting each such endpoint against its two adjoining intervals proves both directions of the claimed criterion, including equality cases.

The repeated-root argument is also valid: for an all-positive-root degree-d symbol, the derivative of delta_d(f)/f is strictly negative off the roots of f. Consequently a repeated positive root of G must be inherited from f, with its multiplicity increased by one. For the quintic G, the roots 1 and 2 would both have to be triple roots of a degree-five symbol. Negative-root symbols are excluded as well: their positive leading coefficient would force a positive constant in odd degree, whereas the inverse symbol's constant is -6.

The source's displayed sign for the quintic cannot override its operator definition. Direct substitution gives T_p(g_0)=-750G, as the manuscript states. The nonzero scalar normalization preserves the extension question.

This approach settles a real-algebraic extension test, not either implication involving weak SOS.

### Approach 2: quadratics and product closure — accepted

A symmetric quadratic decomposes into a mean-square term and a multiple of squared norm on the mean-zero subspace. After scaling to make its value at e positive, hyperbolicity gives exactly a m^2-b sum(x_i-m)^2 with a>0 and b>=0. The b=0 case is properly separated.

For b>0, the Lorentz reduction is legitimate on the effective variables. Every forward cone vector is a nonnegative sum of null vectors. Bilinearity in the two directions and the displayed null-pair identity therefore prove the SOS property for all cone pairs, including boundary directions. The A=B and A=-B degeneracies and the one-spatial-dimensional case are covered by the limiting-coordinate/embedding explanation.

The coefficient formula a b_0 t^2+2b b_2 is correct on centered inputs. Applying it to g_0 gives a t^2-b n(n-1); its inverse symbol a(t-r)^2 proves extendability. This uses shifted degree indexing correctly.

The product Wronskian identity is universally valid, and the product cone is the intersection of the factor cones. Thus the claimed **weak-SOS** closure follows. It does not prove extension closure for arbitrary products, does not preserve hook shape for arbitrary factors, and does not establish the cubic or quartic equivalence. The manuscript does not make those invalid extrapolations.

### Approach 3: shifted penultimate elementary forms — accepted

For s=1+nb nonzero, the change x -> x+b e_1(x)e is invertible and sends e to se. The hook expansion and p_b(e)=n s^(n-1) are correct. Differentiating the root product gives T_(p_b)g=(-1)^(n-1)g'(s t). Its extension to the full input space preserves real-rootedness by Rolle and real nonzero argument scaling, including s<0 and zero derivative outputs.

The Cauchy–Binet determinant formula is correct: for an orthonormal basis B of e-perp, all squared maximal minors are 1/n. Multiplying the pencil by sign(s) gives a pencil positive definite at e, without changing the relevant cone and except for a harmless nonzero scalar in its determinant.

For that pencil, the adjugate trace identity follows from differentiating the determinant on the open set of invertible matrices, then polynomial continuation. With A(u)=UU^T and A(v)=VV^T, cyclicity of trace and symmetry of adj(A) give exactly the Frobenius-square certificate. This works even when A(x), A(u), or A(v) is singular. The stated family is consequently both extendable and weakly SOS-hyperbolic in all the claimed dimensions.

The manuscript correctly stops short of extending this argument to an average of determinantal representations.

### Approach 4: exact SOS slice certificates — accepted as failed obstruction routes

The cone membership identity for w=(6,1,1,1,1) is correct. The source explicitly reports a computational non-SOS conclusion for Delta_(e,w)p, but neither this package nor this audit supplies a full-space rational separating functional.

I independently rebuilt p and its Wronskian using sparse coefficient dictionaries and Python rational arithmetic, without importing or executing the author verifier. Both restricted identities exactly match the supplied Gram matrices. Independently chosen positive-pivot congruence elimination gives:

- 7-by-7 first Gram matrix: inertia (4 positive, 0 negative, 3 zero).
- 8-by-8 second Gram matrix: inertia (6 positive, 0 negative, 2 zero).

All residual Schur matrices are exactly zero. Thus these PSD conclusions require no floating-point eigenvalues, no numerical optimization status, and no reliance on the author's selected principal blocks. Exact pivot values are recorded in `INDEPENDENT_CHECKS.json`.

The two restrictions really are SOS and cannot furnish the proposed restriction-based non-SOS obstruction. They do not imply that the full five-variable Wronskian is SOS. Nonextendability alone also cannot refute the conjecture; one would need weak SOS on that same polynomial.

### Approach 5: sharp deformation boundary — accepted, including equality

The family remains hook-shaped because

(e_1/5)D_e p = 680 e_1 e_4 - 74 e_1^2 e_3 + (21/5)e_1^3 e_2.

On a centered line the two minus signs from m=-t and differentiation cancel, yielding T_(p_epsilon)=(I+epsilon t d/dt)T_p. The degree-five Pólya–Schur symbol of the Euler multiplier has only positive roots for epsilon>=0. Together with the published hyperbolicity theorem for p and p_epsilon(e)=750(1+5epsilon), this proves the claimed hyperbolicity. The published base theorem is a legitimate cited input; its original computational SOS proof is not reproduced here as a separate exact certificate.

I derived the normalized operator symbol directly from multivariate p, inverted delta_5 coefficientwise, imposed the double-root condition at t=2, and divided out (t-2)^2. This independently produces the manuscript's endpoint cubic Q_epsilon. A Sylvester resultant determinant, rather than the author script's discriminant call, produces

Disc(Q_epsilon)=(4epsilon+1)(167620epsilon^3-8871epsilon^2+2820epsilon-752)/5184.

The logical reduction from that one endpoint symbol to **all possible extension symbols** is essential and is valid. For epsilon>0 the four positive critical points are alpha,1,beta,2, with alpha in (0,1) and beta in (1,2). Their types alternate maximum, minimum, maximum, minimum. The minimum at 2 is higher than the one at 1, while the maximum at beta is above the minimum at 2. Consequently a feasible horizontal level exists if and only if the maximum at alpha is at least the minimum at 2. Whenever any level works, the endpoint level -H_epsilon(2) already works. This proves necessity as well as sufficiency of the cubic test; it is not merely one successful candidate construction.

The cubic's strictly alternating coefficients exclude all nonpositive real roots. Its discriminant therefore tests exactly whether the endpoint symbol has five positive real roots counted with multiplicity. At discriminant zero its repeated roots remain admissible. In particular Q_epsilon(2)=8epsilon>0, so the root at 2 has exactly multiplicity two for epsilon>0. No strict-discriminant condition is needed, and the threshold is included.

Finally, D' has positive leading coefficient and negative discriminant, so D is strictly increasing; D(0)<0 gives a unique positive threshold. An independent Sturm root count also gives one real root. Exact rational evaluation sharpens its enclosure to

146702017518327/10^15 < epsilon_* < 146702017518329/10^15.

At epsilon=0, the separate repeated-root obstruction correctly rules out extension. Exact Sturm controls also confirm the endpoint cubic has only one positive real root at 1/7 and three at 1/6, 1, and 100. These controls supplement, but do not replace, the universal argument.

## 3. Exact computation record

The supplied `verify.py` was run successfully and reproduced the saved 206 assertions and all five section counts under SymPy 1.14.0. That rerun alone was not used as mathematical acceptance.

The separately written `independent_verify.py`:

- validates every original manifest entry;
- reconstructs multivariate p, directional derivatives, restrictions, and Gram identities using Fraction arithmetic;
- proves Gram PSD and rank by exact congruence elimination;
- derives the extension endpoint symbol directly from p;
- verifies the discriminant through a Sylvester determinant;
- performs exact threshold isolation and Sturm control counts;
- checks shifted-family operator identities in additional symbolic dimensions.

It passes 46 independently implemented checks. Its output is `INDEPENDENT_CHECKS.json`. The check count is bookkeeping, not a measure of proof strength. Universal reasoning, source hypotheses, all-direction SOS claims, and the implication from arbitrary symbols to the endpoint symbol were reviewed in prose above; they are not claimed to be formal proof-assistant certificates.

## 4. Five-approach count and remaining gap

The package contains five substantive mathematical routes, not five labels for the same computation:

1. Invert the extension symbol and characterize feasibility by critical values/multiplicity.
2. Reduce to quadratics and attempt construction through product closure.
3. Construct a definite determinantal representation for an all-dimensional shifted family.
4. Search for a non-SOS obstruction on two lower-dimensional slices, with exact certificates proving those routes fail.
5. Solve the extension boundary throughout a nontrivial hyperbolic deformation family.

Each route has a concrete argument or certificate and a correctly stated stopping point. Known background tools within those routes do not establish historical novelty.

The unresolved issue is the relation between extension and the SOS condition for every cone-direction pair. For general hook-shaped hyperbolic forms neither direction of the equivalence is established by this package. Even for the deformed quintic, the extension boundary is known exactly but the weak-SOS boundary has not been determined. The quintic at epsilon=0 is supported by the source as non-weak-SOS; the local certificates do not independently reproduce that full-space obstruction.

The proper status is therefore **unresolved, 5/5 approaches**, with accepted partial results. It must not be relabeled solved, disproved, or a counterexample.

## 5. Coverage limits

This audit checks the mathematics, exact certificates, cited definitions/theorem inputs, public source-file integrity, and pinned authored inputs. It does not independently recertify the completeness of the earlier corpus/repository duplicate searches or the full retained-corpus provenance statements in the readiness record. Targeted current primary-source searches found the published conjecture and no resolution, but absence from those searches is not proof of worldwide openness.

No copied primary-source text, downloaded paper, dataset contents, or private coordination material is part of this audit deliverable. No unproved claim of historical novelty is made.
