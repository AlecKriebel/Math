# Fresh adversarial preprint audit — round 1

**Completed:** 2026-09-23 13:37 UTC. **Review completion estimate:** 100% of this bounded soundness and framing audit. This is not a probability of correctness or a priority certification. **Reviewer:** independent AI-assisted internal review, not external peer review.

| Audited artifact | SHA-256 |
|---|---|
| `paper/main.tex` | `60eeb6a9ffb5e5eb2583469da9605997ba86b5a8ebe1b94eb7560bda45b0c94a` |
| `paper/main.pdf` | `b1f27c3e8fc342bf6a4f4c191e3f6193b9548e8df7550bfa6905351ddbfcf7b4` |

## Verdict and required fixes

**Ready as a mathematically sound, accurately framed, unrefereed preprint. No required mathematical or framing correction was identified.** The stated quantitative strong deformation retraction is proved for both specified metrics in all stated finite dimensions. The suggestions below are optional editorial improvements, not conditions of readiness. No journal novelty or acceptance judgment is intended.

I audited the source and complete compiled PDF before reading earlier reports. I did not read or rely on the previous algebra, geometry, final-manuscript, or verification-summary reviews. After completing the proof audit, I inspected the ancillary materials and priority report. No person was contacted; no manuscript or other publication file was edited; no commit, push, release, or deposit was made.

## Independent proof checklist

| Falsification target | Finding and reason |
|---|---|
| Noncommuting algebra | **No issue.** Left multiplication by I+tU and right multiplication by I+tV reduce (6) to `(U+tI)(I+tV)−(I+tU)(V+tI)=(1−t²)(U−V)`. The mixed tUV terms cancel in the same order; no U,V commutation is used. |
| Derivative | **No issue.** Product-rule differentiation gives `ER−(W+tI)R tER=(I−tF_t(W))ER=(1−t²)RER`, where `R=(I+tW)^−1`. This is an ambient matrix derivative and remains valid at both endpoints. |
| Spectral confinement | **No issue.** The eigenvector sphere-path argument proves `|θ|≤dν(I,W)` for either norm. Source diameter π and L≤1/2 place the entire normalized image in the closed semicircle. |
| Inverse and unitarity | **No issue.** The Gram identity is positive with lower bound `(1+t²)I` on the stated domain. Two inverse factors yield exactly `(1−t²)/(1+t²)`. Equality of the two Gram matrices directly gives unitarity. |
| Metric normalization | **No issue.** Closed one-parameter subgroups have length 2π times an integer vector's Euclidean or maximum norm, whose smallest nonzero value is one. Hilbert–Schmidt geodesics are translates of one-parameter subgroups. The paper explicitly avoids an arbitrary-invariant-metric claim. |
| Intrinsic versus chordal length | **No issue.** The argument integrates the derivative along the normalized image of a source geodesic. Every point on this curve lies in the semicircle. No target geodesic-convexity assertion or arbitrary-pair intrinsic contraction is assumed. |
| Nonsmooth input | **No issue.** Lipschitz restrictions to source geodesics are absolutely continuous, also in ambient matrix norm because `||U−V||ν≤dν(U,V)`. The ordinary almost-everywhere chain rule and integral of norm speed apply. Differentiability of the operator norm itself is unnecessary. |
| Length-speed identification | **No issue.** Independently, nearby unitary differences have singular values `2|sin(θj/2)|`, while an exponential path has length equal to the relevant norm of θ. Their ratio tends to one locally, identifying intrinsic speed with ambient norm speed. |
| Input and time continuity | **No issue.** The 2δ normalization bound and `(1+2q_t)δ` output bound are correct. Compactness and the uniform resolvent bound supply time continuity uniformly in W. Intrinsic and matrix-norm metrics induce the same uniform topology on fixed U(N). |
| Arbitrary parameter spaces | **No issue.** For any topological Y, the direct rational formula on `[0,1]×Y×S^(n−1)` is continuous. Neither smoothness nor compactness of Y is needed. |
| Retraction and equivariance | **No issue.** The endpoints and fixed constants are as claimed; evaluation at p is preserved for all t. Normalization under QΦR is conjugation by R, proving the claimed frame equivariance. No contraction of U(N) itself is asserted. |
| Closed threshold and dimensions | **No issue.** L=1/2, t=0, t=1, N=1, antipodal points, and repeated eigenvalues ±i are covered without a strict spectral margin. The proof is dimension-independent for n≥2 and finite N≥1. |
| S⁰ | **No issue.** With the stated angular distance π, the transformed angle has derivative in θ between 0 and q_t and vanishes at θ=0. Thus each absolute angle contracts by q_t, yielding both asserted intrinsic distance bounds. |
| Excluded boundary | **No issue in the actual claim.** At W=−1, t=1/2 the scalar angular derivative is 3 while q_t=3/5; at t=1 the denominator vanishes. This falsifies an unrestricted-domain claim, which the paper does not make. |

For an independent check of the S⁰ Hilbert–Schmidt distance formula, apply the sphere-path bound to an orthonormal eigenbasis v_j and then the integral triangle inequality:

`∫(Σj ||U′v_j||²)^(1/2) ≥ (Σj (∫||U′v_j||)²)^(1/2) ≥ (Σj |θ_j|²)^(1/2)`.

The diagonal exponential path attains the bound. For the operator norm, the individual eigenvector lower bounds and the same exponential path suffice. Thus this boundary paragraph does not conceal a missing geometric assertion.

## Sources and publication framing

I checked [Gromov's original manuscript](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf), printed pp. 35–36, and [Neretin's book](https://www.mat.univie.ac.at/~neretin/lectures/ems.pdf), §1.7.9, Theorem 7.5, printed p. 42. The printed question has threshold 1/2 and continuous dependence on the map. The surrounding threshold-1 and sphere-fibration discussions are distinct. Neretin supplies the cited Cayley chart. The manuscript's Cayley scaling identity and logarithm observation for L<1 are correct.

The paper, README, site, metadata, and deposit description consistently acknowledge classical machinery, a bounded priority search, finite diagnostic limitations, AI assistance, and unrefereed status. I found no unjustified claim of first discovery, external peer review, formal verification, an assigned DOI, or sublevel preservation below threshold 1. The priority report supports a qualified search finding, not an exhaustive priority guarantee. I did not repeat an exhaustive literature search. The AMR catalogue URL returned HTTP 403 during this audit; the directly checked primary manuscript supplies the question independently.

## Reproducibility and artifact checks

- Read the README, citation file, site HTML, metadata/deposit text, both scripts and their documentation, and release builder.
- Exact script: **10/10 passed**. Numerical script: **7,679 checks, zero failures**, using bundled Python 3.12.14 / NumPy 2.3.5, recorded seed, and 101 pairs in dimensions 1, 2, 3, 5, and 8. System Python lacked the documented optional NumPy dependency; this was an environment issue, not a failed mathematical check.
- The exact script retains word order; the numerical derivative uses an independent product-rule expression. Advertised limitations are accurate. Neither diagnostic establishes the all-dimensions or analytic theorem by itself.
- Verified every reproducibility-archive manifest entry and upload-kit checksum: **no mismatch**. Selected archived paper/source/README/site/metadata/scripts match current originals; the kit's PDF and nested archive match as well.
- Local publication copies of the HTML, PDF, metadata, reproducibility archive, and upload kit all match project originals. Nothing was rebuilt or published.
- Rendered and visually inspected all four manuscript pages: no clipped equations, missing symbols, overlaps, or unreadable references. Extracted PDF text agrees with the audited source.

Replay output and rendered pages are confined to `tmp/preprint_round1/`.

## Optional edits only

**C1 — low severity: identify the derivative variable.** At `paper/main.tex:130`, change “The derivative of the resulting angle is” to **“The derivative of the resulting angle with respect to θ is”**. Both t and θ occur nearby, so the added words remove a momentary ambiguity. The existing formula and inference are correct. **Not required for readiness.**

**C2 — low severity: link companion materials from the standalone PDF.** At `paper/main.tex:143`, add: **“Companion materials are available at [the project repository](https://github.com/AlecKriebel/Math/tree/main/gromov_unitary_lipschitz_contraction).”** Use a LaTeX `\href` with that address and short visible label. The current PDF refers to accompanying materials without a direct link. This affects discoverability, not the self-contained proof. **Not required for readiness.**

**C3 — low severity: populate embedded PDF title and author.** `pdfinfo` reports no embedded Title or Author, although both are visibly correct. Add the following to the preamble for indexing and identification:

```tex
\hypersetup{
  pdftitle={A Lipschitz-nonincreasing deformation of small unitary-valued maps},
  pdfauthor={Alec Kriebel}
}
```

**Not required for readiness.** If these optional changes are adopted, rebuild the PDF and existing packages to keep all copies synchronized; these editorial changes do not themselves require new mathematical tests.

## Final checkpoint

**Completion estimate: 100%. Strongest verified result:** the exact theorem and optional S⁰ extension in the hashed manuscript have a sound analytic proof, and the checked publication materials describe them accurately. **Remaining gap for the requested readiness goal:** none identified. Formal certification, external peer review, and established first priority remain outside this audit and are already appropriately disclaimed.
