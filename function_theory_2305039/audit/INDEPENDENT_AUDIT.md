# Independent audit: Function Theory Problem 5.39

Date: 3 October 2026. Problem ID: 2305039. Rank: 524.

## Verdict

**Accept the stated partial results. Retain the overall status `unsolved`, with five substantive attempts recorded.** No blocking mathematical defect or necessary correction was found in the frozen public package. This is a mathematical review and an exact-arithmetic replay, not a formal proof-assistant certification or a historical-priority determination.

The accepted conclusions are:

1. The universal radius is exactly \(r_p=1/2\) for \(0<p\le2\).
2. \(r_p\) is nonincreasing in \(p>0\).
3. \(\sqrt2-1\le r_p\le1/2\) for all finite \(p>0\).
4. \(r_p\le99/200\) for \(p\ge14\).
5. \(\lim_{p\to\infty}r_p=\sqrt2-1\).

The exact finite-exponent values for \(p>2\) are not established. The full problem must not be described as solved. No extremality or sharpness of the rational counterexample is established.

## Frozen input and reproducibility

The supplied frozen-input manifest has SHA-256

`859ac2d89b2503ee2e36fb51db83efaad6323059ea819476838f0dfac4e11f8f`.

All seven public input files match the manifest's byte lengths and hashes. They were preserved unchanged. `INPUT_HASHES.json` records their public, package-relative identities and hashes. This audit introduces only files in `audit/`.

The author's verifier was read in full and replayed twice. Both outputs were byte-identical to the supplied `artifacts/verification.json`, reporting 36 passing checks. The independent audit program reports 43 passing checks, including frozen-input integrity, direct-composition coefficient reconstruction, exact strict margin, optimizer parameter checks, perturbation coefficients, and the author-verifier replay. These counts include bookkeeping and finite checks; neither count measures proof completeness.

To reproduce from the package root:

```sh
python artifacts/verify.py
python audit/verify_independent.py
```

The audit program uses Python's standard library and the sibling public artifacts only. It does not require any downloaded paper, external package, account, or network access.

## Primary statement and source scope

The definition and exact question were checked in both extracted text and rendered pages of [Hayman and Lingham, Research Problems in Function Theory, arXiv:1809.07200](https://arxiv.org/abs/1809.07200), printed pp. 98–100. The class is all holomorphic \(f\) and all holomorphic disk self-maps \(\phi\) fixing zero, with \(g=f\circ\phi\). There is no univalence assumption on \(f\) in Problem 5.39. The uniform derivative-mean radius in the manuscript matches the source question. The adjacent univalence assumption in Problem 5.38 must not be transferred into this problem. The update is a statement about progress reported to the authors by 2018, not evidence of the present literature's completeness.

The full relevant coefficient arguments in [Reich, An inequality for subordinate analytic functions (1954)](https://msp.org/pjm/1954/4-2/pjm-v4-n2-p08-s.pdf), printed pp. 263–265, were read, including the continuation of Lemma 5 and the partial-summation proof of Lemma 6. They support the classical coefficient ingredients. The authored proof also establishes those ingredients independently.

The extracted Section 2 and proof of Theorem 1 of [Khasyanov, arXiv:2503.16313](https://arxiv.org/abs/2503.16313), pp. 3–5, were read for scope. Their weighted square-coefficient setting is not a determination of the arbitrary-\(p\) question here, and the present proofs do not depend on the stated extremal classifications.

The original Goluzin proof is not certified as inspected by this audit. The package expressly discloses its access limit; no unsupported original-proof-access claim is needed for the mathematics. Prior repository searches and the author's broader literature search were not independently repeated. They are bounded provenance statements, not premises of the accepted proofs. This review makes no exhaustive literature or novelty claim.

## Detailed mathematical review

### 1. Ordinary integral-mean contraction

Lemma 1 is valid for every positive real exponent, including exponents below one. Subharmonicity, not norm convexity, is the relevant fact. Schwarz's lemma puts \(\phi(r\mathbb D)\) inside \(r\mathbb D\), so the harmonic majorant \(U\) may be composed with \(\phi\). Its circle mean is its value at zero. Boundary images on the radius-\(r\) circle cause no failure: the harmonic majorant is continuous to that boundary, and radial passage gives the displayed inequality. Rotation maps and constant maps are included.

### 2. Quadratic estimate and truncation

The first \(N\) nonconstant coefficients of \(F_N\circ\phi\) agree with those of \(f\circ\phi\), since \(\phi(0)=0\). The omitted constant \(a_0\) has no effect. Applying the contraction to the polynomial \(F_N\) at \(t<1\), discarding only nonnegative squared coefficients, and letting \(t\uparrow1\) gives every required finite coefficient-sum inequality. There is no assumption that the original \(f\) belongs to a boundary Hardy class.

For \(r\le1/2\), the derivative weights \(n^2r^{2n-2}\) are nonnegative and nonincreasing, including the equality of the first two weights at \(r=1/2\). Finite summation by parts has a nonnegative terminal term and yields the stated inequality for every \(N\). Passage to the infinite derivative series is valid because \(r<1\) and both derivatives are holomorphic. The endpoint \(r=1/2\) is genuinely covered.

### 3. Local extension, zero removal, and Hölder

This is the main potential point of failure, and it passes review.

- An input holomorphic on a neighborhood of the closed radius-\(r\) disk is uniformly approximable there by its Taylor polynomials: that neighborhood contains a slightly larger concentric disk. Its composition is approximated uniformly as well because \(\phi(\overline{r\mathbb D})\subseteq\overline{r\mathbb D}\). Boundedness of \(\phi'\) on the circle then permits passage through the weighted integral for any \(q>0\). No unproved global Hardy-space extension is used.
- For a nonzero \(h\) without boundary zeros, there are finitely many interior zeros. Each listed radius-\(r\) Blaschke factor has modulus one on the boundary and at most one inside. After removable singularities are filled, \(K=h/B\) is holomorphic and zero-free on the closed disk. Compactness and the absence of boundary zeros allow a slightly larger disk on which it remains holomorphic and zero-free, so the logarithm exists there.
- The power \(F=\exp((p/q)\log K)\) need only exist on that slightly larger disk, exactly the class covered by the local extension. It satisfies \(|F|^q=|K|^p\).
- For \(\alpha=p/q\in(0,1)\), the manuscript's product \(A^\alpha D^{1-\alpha}\) is exactly \(|\phi'|^p|K\circ\phi|^p\). Both \(A\) and \(D\) have means bounded by the same quantity \(\langle|F|^q\rangle_r\), respectively by the assumed weighted inequality and ordinary subordination. Hölder with exponents \(1/\alpha\) and \(1/(1-\alpha)\) proves the conclusion.
- Boundary zeros are removed by choosing dilates \(h(sz)\) with \(s\uparrow1\) avoiding the finitely many relevant zero moduli. Uniform convergence on the closed disk justifies the limit. The identically zero input is handled separately.

Every holomorphic input \(h\) on the unit disk has a primitive there. Thus the universal derivative inequality supplies precisely the universal input hypothesis required by the lemma. The constructed \(F\) may depend on \(h,p,q,r\); universality in the hypothesis permits that dependence.

### 4. Radius quantifiers and monotonicity

The extrapolation first works for a fixed \(r,\phi\), then for every \(\phi\), then for every \(r\) in any interval admissible at exponent \(q\). Thus the entire admissible-radius set for \(q\) is contained in that for \(p<q\). Taking suprema gives \(r_p\ge r_q\), in the claimed direction. No monotonicity in the radial variable for an individual ratio is assumed.

The pair \(f(z)=z,\phi(z)=z^2\) gives derivative means \(1\) and \(2r\) for every positive \(p\), so all radii larger than \(1/2\) fail. Together with the quadratic estimate and extrapolation, this proves the exact result for \(0<p\le2\).

A counterexample at a single radius \(r_0\) excludes every admissible interval endpoint \(R>r_0\), since such an interval contains \(r_0\). Hence it gives \(r_p\le r_0\) under the source's strict-interval definition. Attainment of the supremum is unnecessary.

### 5. Universal lower bound and infinite-exponent limit

The Schwarz–Pick estimate for \(\omega=\phi/z\) is valid after filling the removable singularity at zero. The unimodular-constant case is correctly separated. For \(r\le\sqrt2-1\), the factorization

\[
1-t-k(1-t^2)=(1-t)(1-k(1+t)),\qquad k=r/(1-r^2)\le1/2,
\]

has nonnegative factors for \(0\le t\le1\). Multiplication by the nonnegative composed input and ordinary mean contraction prove the lower bound for every positive \(p\).

Above that radius, the optimizing \(t=(1-r^2)/(2r)\) lies in \((0,1)\). The chosen real \(a=(t-r)/(1-tr)\) satisfies

\[
1-a^2=\frac{(1-t^2)(1-r^2)}{(1-tr)^2}>0,
\]

so the map is admissible even when \(a<0\). Direct differentiation gives \(\phi_a'(r)=k+1/(4k)>1\).

The large-\(p\) argument has the right order of quantifiers. Fix any \(r>\sqrt2-1\), then fix its map \(\phi_a\). By continuity, \(|\phi_a'|\ge1+\delta\) on an arc of positive normalized measure \(m\), for some \(\delta>0\). Its \(p\)-th mean power is at least \(m(1+\delta)^p>1\) for every sufficiently large real \(p\). Thus \(r_p\le r\) eventually for each such fixed \(r\). Combining this with the uniform lower bound proves the claimed limit. There is no exchange of an infinite-dimensional supremum with a limit and no assertion that the same map works for every radius.

### 6. Perturbation around the squaring map

The derivative expansion through order \(a^2\), the Laurent coefficients at \(r=1/2\), and all four circle moments are correct. The modulus stays bounded away from zero for sufficiently small real \(a\), so the real-power expansion is uniform for each fixed \(p>0\). Its second-order coefficient is exactly \(p(p-16)/64\). This gives a strict violation for \(p>16\), and continuity moves the violation below \(1/2\). The zero coefficient at \(p=16\) is correctly left inconclusive. This argument does not assert sharpness or a result for all \(p>2\).

### 7. Rational \(p=14\) certificate

The disk-map admissibility identity and chain-rule rational expression are correct. The independent reconstruction starts instead from

\[
\phi(z)=az+(1-a^2)\sum_{n\ge2}(-a)^{n-2}z^n,
\qquad g=\phi+\phi^2/10,
\]

then differentiates and takes the seventh power. It reproduces every displayed coefficient through degree ten. For \(a=2/3,r=99/200\), the independent exact difference is

\[
\frac{171427691243281345585321685814196084464053669376850321}
{29893556250000000000000000000000000000000000000000000000}>\frac1{200}.
\]

Parseval applies because \((g')^7\) is holomorphic beyond the relevant circle. Every omitted term is nonnegative; no tail estimate, floating-point tolerance, cancellation assumption, or numerical quadrature is used to certify the violation. The right mean is the exact polynomial Parseval sum for \((1+z/5)^7\).

The step from \(p=14\) to every \(p\ge14\) is justified by the proved monotonicity of optimal radii. It does not require, and the manuscript does not claim, that this identical pair has a violating mean ratio for each larger exponent.

## Findings and remaining limitations

- Blocking findings: none.
- Required corrections to the frozen author package: none.
- The five recorded attempts are materially distinct: classical coefficient comparison, downward extrapolation, a perturbative obstruction, an exact nontrivial-input certificate, and pointwise optimization with a large-exponent limit. Their limits are accurately recorded.
- The main unresolved requirement remains a sharp universal inequality with matching extremizers or extremizing sequences for each finite \(p>2\).
- The audit accepts only the package's partial mathematical claims. It does not promote the overall problem to solved, infer historical novelty, certify uninspected source access, or treat arithmetic test counts as analytic proofs.

All audit deliverables contain original analysis and verification code. No source-paper copies or unrelated material are included.
