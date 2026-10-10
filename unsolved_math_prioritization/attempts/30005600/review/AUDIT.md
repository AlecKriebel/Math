# Independent mathematical audit of torus problem 30005600

Audit date: 7 October 2026. Problem: OWR-14297736-006, rank 952.

## Verdict

Accept the scoped mathematical partial results after the two scope corrections incorporated in `reading_copy/PROOF.md` and `reading_copy/RESEARCH_LOG.md`. The original problem remains unresolved after five approaches. This is an independent mathematical and reproducibility audit, not formal verification, external peer review, a novelty certification, or a full-resolution claim.

The main one-variable theorem is accepted: for a smooth positive b-periodic factor f(y) with M = max f and F = integral from 0 to b of f satisfying M <= F, the full first strictly positive Dirac eigenvalue is 2π/F. The weighted scalar Rayleigh principle, its kernel projection, the L-infinity-dependent lower bound, the Fourier Ritz matrices, and the harmonic-map comparison are accepted. The covering result is accepted only as an energy obstruction for the pulled-back harmonic map and its associated eigenpair. It is not a lower bound for the first positive eigenvalue of the pullback metric.

Two corrections were needed:

1. Original Approach 4 overstates the implication of the map-energy estimate when it says that the covering counterexample route is closed. Additional lower eigenmodes on the cover are not controlled. All unqualified versions of this conclusion in the proof, its closing checklist, and the research log have been narrowed in the separate reading copy.
2. The original numerical discussion calls concentration at b=2 necessary or known to be needed. What is established is that spherical bubbling supplies a comparison below the flat value. The search failed to capture that comparison. Necessity of concentration and absence of a smooth minimizer were not proved.

These corrections do not alter any displayed proved inequality or the one-variable theorem. No author original, queue, remote repository, or external publication was changed.

## Inputs and integrity

The reviewed archive is `AUTHOR_30005600.zip`, 25,093 bytes, SHA-256:

891e8c125dbb0310074a63f83d4071712cc50bab1584c6153ae829a5d5ed7782

The frozen proof is 20,099 bytes, SHA-256:

c8bebb5be39bab1bbc1f2d28bbe99d021eeaf478499c3f385b1b689d3916c44b

All ten file entries in the author manifest matched both their recorded byte counts and SHA-256 values. All eleven archive members, including the manifest, matched the extracted author files byte for byte. The four locally supplied public-source PDFs also matched the sizes and hashes recorded in SOURCES.json. Hash agreement establishes identity, not mathematical correctness or completeness of retrieval history. The corpus hashes and repository duplicate-search history were not independently rerun as part of this mathematical audit.

The separate patch `SCOPE_CORRECTIONS.patch` specifies the complete textual correction and reading-copy review-status annotation against the frozen proof and research log. The corrected reading copy is governed by this audit. Statements in the historical author research log that review was pending describe the author-freeze state.

## Target and primary-source check

The original target is the infimum of the first strictly positive Dirac eigenvalue times square-root area, within a fixed torus conformal class and the trivial spin structure. Zero modes are omitted. The OWR split is b>π versus b<=π, with matching expressions at π. [OWR Conjecture 3](https://ems.press/content/serial-article-files/47475).

KMP Theorem 1.7 establishes b>2π; Remark 3.7 plus the flat comparison gives the value at b=2π. Its Theorem 1.1 provides the sub-spherical minimizer, and Sections 3.1–3.2 provide the map correspondence and normalizations used here. Endpoint uniqueness is not inferred. [Published KMP article](https://academic.oup.com/imrn/article/2024/21/13758/7810213).

FLPP Corollary 6.6 has the strict threshold E<4π. [FLPP paper](https://arxiv.org/pdf/math/0012238).

Martynyuk's April 2026 manuscript concerns higher-eigenvalue existence and the sphere conformal spectrum; it does not supply this torus threshold. [Martynyuk v1](https://arxiv.org/html/2604.14840v1).

The bounded current-source check found no full-resolution source. This is not an exhaustive proof of worldwide open status. No novelty judgment is made for the elementary partials.

## Approach 1 accepted with the stated remaining gap

### Flat spectrum

The lattice is Γ = Z(1,0) + Z(a,b), with b>0, |a|<=1/2 and a²+b²>=1. Trivial-spin sections are periodic C²-valued functions. Their Fourier frequencies are exactly

η(m,n) = (m,(n-am)/b), with integers m,n.

The symbol of D0 = -i(σ1 ∂x + σ2 ∂y) at η is 2π(σ1 ηx + σ2 ηy), whose eigenvalues are ±2π|η|. The zero frequency contributes the two-complex-dimensional kernel. Completeness of the torus Fourier basis accounts for the whole spectrum.

The proof of the shortest nonzero dual length is correct. Multiplying its squared length by b² gives b²m²+(n-am)². For m=0 and n nonzero this is at least 1, with equality at n=±1. For |m|>=2, b²>=3/4 gives a bound of at least 3. For |m|=1, nearest-integer distance is |a|, so the expression is at least a²+b²>=1. Thus μ1(g0)=2π/b, and area b gives normalized value 2π/sqrt(b).

### Harmonic maps and parity

The required minimizer argument is used only after assuming a strict sub-spherical value. On a genus-one surface the possible singularity count is zero, so the resulting minimizer is smooth. The admissible harmonic map belongs to the correct induced-spin class; a general harmonic map cannot silently replace that condition.

With the unit-sphere convention E=(1/2) integral |dΨ|², the degree-zero minimizing map has E=2Λ². For nonzero degree, the holomorphic case cannot represent a nonzero Dirac eigenvalue; the antiholomorphic case has absolute degree at least two and cannot lie below the relevant energy threshold. The factor two in E=2Λ² is retained throughout.

A nonconstant equatorial map has phase 2π<ξ,z> for ξ in Γ*. Harmonicity of its phase on the universal cover, followed by subtracting its linear periods, leaves a periodic harmonic function and hence a constant. Its energy is 2π²b|ξ|². A spinor lift has half-phase monodromy (-1) to the power ξ(γ). Thus trivial spin requires ξ in 2Γ*, and its energy is at least 8π²/b. This agrees with the projectivization of a periodic eigenspinor of frequency η, whose phase frequency is 2η. Constant maps are excluded by the positive eigenvalue.

Assuming Λ<min(2π/sqrt(b),sqrt(2π)) yields E<4π. The circle theorem and parity estimate contradict that assumption. Therefore the two-sided comparison displayed as (1) is valid. At b=2π the lower and upper bounds coincide at sqrt(2π). The strict rigidity theorem does not classify all minimizers at E=4π, so no endpoint-uniqueness claim is justified.

The missing spin-sensitive energy lower bound in the interval [4π,8π) remains genuinely unproved. Nothing in this audit promotes the 4π rigidity theorem to an 8π theorem. The degree and even-zero admissibility restrictions on maps must remain in any attempted sharp reformulation.

## Approach 2 accepted with exact domains and kernel

For smooth f>0 on the compact torus, f, f inverse, and their required derivatives are bounded. Conformal covariance and the unitary identification of geometric L² with flat L² give

Af = f^(-1/2) D0 f^(-1/2).

Its self-adjoint operator domain is H¹(T,C²). It has compact resolvent. Its kernel is f^(1/2) times the constant spinors. Multiplication by f^(1/2) is an isomorphism of H¹, so writing u=f^(1/2)v gives

||Af u||² / ||u||² = (integral |D0v|²/f) / (integral f|v|²).

Orthogonality to every kernel spinor is exactly integral f v=0, componentwise. It is not unweighted mean zero. The Rayleigh formula is the closed quadratic-form formula for Af² on the kernel complement, with form domain H¹; it does not require every test function to lie in the operator domain of Af².

Chirality anticommutes with Af, and Af² preserves the two scalar summands. Complex conjugation takes the form for ∂x+i∂y to the form for ∂x-i∂y, preserving the weighted norm and mean constraint. The two scalar infima therefore agree. This verifies the precise scalar formula (2), including its strictly positive spectral interpretation. Smooth constrained tests are dense: approximate in H¹ and subtract the weighted mean.

For v=w+c with unweighted mean of w zero, the weighted constraint fixes c=-(integral fw)/(integral f). Expanding the squared norm yields exactly

integral f|v|² = integral f|w|² - |integral fw|²/(integral f).

The denominator is at most M integral |w|², while the numerator is at least M^(-1) integral |Lw|². Fourier Parseval yields integral |Lw|² >= (2π/b)² integral |w|². This proves (3), with both factors of M in the denominator. For constant f it agrees with the exact flat spectrum and scaling.

The bound degenerates under concentration and does not solve the uniform conformal problem. The proposed sharp inequality (4) is a correct reformulation, but remains an unproved universal inequality. No reversal of the L²/L-infinity comparison is accepted.

## Approach 3 accepted as a full-spectrum theorem

The function f(y) is well-defined on the skew torus precisely because it is b-periodic. Horizontal translation is a unitary circle action commuting with Af and with the weighted generalized equation D0v=λfv. The x-Fourier sectors are indexed by n in Z and have the form exp(2πinx)w(y), with

w(y+b)=exp(-2πina)w(y).

The sector domain is H¹ functions with this unitary quasiperiodic boundary condition. The derivative and Dirac operators have the corresponding self-adjoint boundary realization. Smooth eigenfunctions satisfy the induced derivative matching automatically.

In the n=0 sector, diagonalizing σ2 gives the exact solutions exp(±iλ integral from 0 to y of f). Periodicity requires λF in 2πZ. Thus the full n=0 spectrum is (2π/F)Z, with the appropriate two spinor components; zero consists exactly of constants in the generalized representation.

For n nonzero, Dn=2πnσ1-iσ2 d/dy. Pauli anticommutation and cancellation of the quasiperiodic boundary terms give

||Dn w||² = (2πn)²||w||² + ||w'||².

For an eigensection Dn w=λfw this implies |λ|>=2π|n|/M. With M<=F every such nonzero sector has |λ|>=2π/F. This estimate is for actual eigenfunctions and does not pretend that squaring the generalized equation commutes with f. Since the full compact-resolvent operator decomposes into these invariant sectors, no omitted mode can undercut the explicit n=0 branch.

Area is Q=integral from 0 to b of f², because the horizontal period is one and the strip fundamental domain has unit horizontal width. Cauchy–Schwarz gives F²<=bQ, with equality precisely for constant smooth f. The normalized result (5) follows. Every quantity has the expected homothetic scaling.

The cosine family has F=b, Q=b(1+ε²/2), and M=1+|ε|. Its smooth positivity and hypothesis are exactly |ε|<1 and 1+|ε|<=b. The assertions about no examples at b<1 and only constant factors at b=1 are correct. For M>F the proof gives only the n=0 branch; no global first-eigenvalue conclusion is accepted there.

## Approach 4 accepted only after scope correction

For a nonzero character χ:Γ→Z/2, any subgroup trivializing it lies in ker χ and therefore has index d>=2. Restriction of monodromy does trivialize the pulled-back spin structure. A conformal unbranched cover preserves harmonicity and multiplies total energy by d. A non-equatorial base harmonic map has E>=4π, hence its lifted map has E>=8π. If the degree is zero, its antiholomorphic energy is at least 4π. These are valid map-energy conclusions.

The associated Dirac eigenvalue λ satisfies λ²Area=E^(0,1), but it need not be μ1 on the cover. The inequality μ1<=|λ| points in the wrong direction to deduce a lower bound for μ1. In particular, neither literal pullback of the metric nor the existence of additional eigenmodes has been excluded by the energy estimate.

This distinction can be checked without using a conjectural example. Start with any smooth positive periodic f on a trivial-spin torus T0 with basis γ1,γ2. Pass to the N-fold cover with basis Nγ1,γ2. Choose a dual covector η with η(γ1)=1 and η(γ2)=0, and set vN=exp(2πi<η,z>/N). Its f-weighted mean over the cover vanishes by summing the N roots of unity. Formula (2) gives

μ1² Area <= [(2π|η|)² Q0 (integral on T0 of 1/f)/(integral on T0 of f)] / N,

where Q0=integral on T0 of f². Thus the normalized first positive eigenvalue of these literal lifted metrics tends to zero on the tower, while the energy of any fixed pulled-back harmonic map grows with the covering degree. Starting after a spin-trivializing cover gives the same observation for the mechanism under review. This is not a counterexample to the original conjecture, whose flat comparison also changes with the cover. It demonstrates why a map-energy lower bound is not a first-eigenvalue lower bound.

The corrected packet now excludes only the associated low-energy map witness. Lower eigenmodes of cover metrics, intrinsically trivial-spin maps, and deformations remain open to further analysis.

## Approach 5 accepted as an uncertified search and exact formulation

In u=x-ay/b and t=y/b coordinates, the Fourier wave exp(2πi(mu+nt)) has

L e_k = 2πi q_k e_k, with q_k=m+i(n-am)/b.

Consequently the derivative Gram matrix is Aij=4π² conjugate(qi) qj times the (i-j) Fourier coefficient of 1/f. Eliminating the constant mode using weighted mean zero gives exactly the stated covariance matrix Bij. The conjugation and Fourier-coefficient indices in both the mathematics and implementation are correct, including for sine-containing factors. The area factor b cancels from the generalized eigenproblem and returns as b times mean(f²) in area normalization.

For exact integrals both Gram matrices are positive definite on any finite set of distinct nonzero frequencies. A is positive because a nonconstant Fourier polynomial cannot have L derivative zero on the torus. B is positive because the weighted-mean-adjusted polynomial can vanish identically only if its nonconstant coefficients all vanish. Exact finite-dimensional minima are upper bounds for μ1². They are not lower bounds.

The actual script computes grid quadrature with floating-point FFTs and a floating-point generalized eigensolver. The discrete weighted-mean constraint is not an exactly certified continuous constraint. Symmetrization and the square-root clamp do not supply certified interval error bounds. Thus the output itself is neither a rigorous continuous upper-bound enclosure nor a lower-bound certificate. The larger-cutoff evaluations also change quadrature size, so their observed downward movement is not a proved continuous spectral convergence result.

The recorded search covers a six-parameter exponential family, bounded optimizer boxes, finitely many starts and seven conformal classes. It is nonexhaustive in both parameters and the space of all smooth factors. Convergence flags do not prove mathematical minimality. The evidence supports only that this specified computation produced no strict candidate below the conjectured target.

## Reproduction and independent computational cross-check

All original files were preserved. The numerical script was replayed from a separate directory.

- Normal Python exact checker: PASS, byte-identical to EXACT_CHECKS.json.
- Optimized Python exact checker: PASS, byte-identical to the same reference.
- Counts: 5,600 dual-lattice modes; 729 weighted-variance cases; 34 cosine parameters; all three nonzero parity characters; three rejected-shortcut controls.
- Complete numerical replay: exit code 0; output JSON byte-identical to SEARCH_RESULTS.json.
- Replay output SHA-256: d4bd15167fe3881a4d7939b7221d7fefcfd6edebd54cd8a6cb8fc551b179900e.
- Runtime: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, with single-thread BLAS settings.
- Search totals: 287 initial factors, 14 optimizations, 1,666 optimizer objective calls, plus controls and refinements.

The six flat and three one-variable numerical controls passed. A nonblocking source-code comment says that the one-variable control uses N=10; the actual code uses N=8. The actual N=8 run is what passed. This comment has no effect on the calculation and is not silently represented as an N=10 test.

At cutoff 6 the best square and equilateral evaluations were respectively 4.92499227573857 and 4.964147914012294. The other five best factors were flat. At (a,b)=(1/4,2), the reported value 4.442882938158366 is above the known spherical comparison 3.544907701811032. This is a failure to capture an established improvement below flat, not lower-bound evidence and not proof that every improving or minimizing sequence must concentrate.

An additional independent direct-grid assembly, using complex Fourier basis functions and explicit weighted-mean subtraction rather than FFT lookup, tested a skew class a=0.37,b=2.3 with sine and cosine coefficients. Against the FFT matrices, maximum differences were 8.53e-14 for A and 2.23e-16 for B. The weighted means were at most 5.60e-17, the smallest generalized-eigenvalue difference was 5.16e-14, and rescaling f by 7 changed the normalized output by at most 3.11e-14. These checks are recorded in INDEPENDENT_GRID_CHECK.json. They test implementation conventions; they do not certify integrals or infinite-dimensional spectral bounds.

## Remaining problem and acceptance limits

The accepted known comparison settles the value for b>=2π, with its published provenance retained. The flat-value lower bound for π<b<2π and the spherical-value lower bound for b<=π, including b=π, remain unproved here.

Accepted deliverables are the complete one-variable theorem under its stated condition, the exact kernel-corrected variational reduction and elementary weighted bound, the credited harmonic-map comparison with its explicit gap, the carefully restricted covering energy obstruction, and the reproducible but uncertified negative search. No full solution, counterexample, novelty claim, global optimizer certificate, endpoint-uniqueness theorem, or metric-level covering obstruction is accepted.
