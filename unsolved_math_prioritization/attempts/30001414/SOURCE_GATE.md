# Source gate: boundary conditions and optimal Hardy–Sobolev constants

Checked 2026-10-21. Problem 30001414 / OWR-4209-004; ordered queue row 1878.

## Verdict

SOURCE VERIFIED; OPEN-CLASSIFICATION NOT RESOLVED. The corpus question is genuine, but omits essential hypotheses and the homogeneous energy. No general classification or complete solution was located in the searches below. This is a bounded search result, not proof that no solution exists. No mathematical solution should be claimed from Navier equality, fractional Navier extensions, or elementary intermediate-space examples alone.

## Original scope

Filippo Gazzola's contribution, “Higher order Sobolev-Hardy inequalities with remainder terms,” in Oberwolfach Report 08/2010, pp.351–354, asks the boundary-condition question on p.352, after Theorem 1. The setting is integer m≥1, 1<p<∞, mp<n, bounded C^m domains. The energy is ||Δ^k u||_p^p for m=2k and ||∇Δ^k u||_p^p for m=2k+1. The two target denominators are ∫|u|^p/|x|^{mp} and ||u||_{np/(n-mp)}^p. The comparison constants are those of the whole space. Navier means trace Δ^j u=0 for 0≤j<m/2. The report has the origin-in-domain case in mind for Hardy sharpness. Its next open problem concerns remainder terms and is distinct.

Primary report: https://ems.press/journals/owr/articles/4209
PDF: https://ems.press/content/serial-article-files/46265
DOI: https://doi.org/10.4171/OWR/2010/08

## Established literature and exclusions

1. Gazzola, Grunau and Sweers, “Optimal Sobolev and Hardy-Rellich constants under Navier boundary conditions,” Ann. Mat. Pura Appl. 189 (2010), 475–486, DOI https://doi.org/10.1007/s10231-009-0118-5. Theorems 1–2 establish the Navier equalities; their proofs use rearrangement and extensions of radial functions. This is the baseline already known to the 2010 question, not its resolution. Author PDF inspected: https://gazzola.faculty.polimi.it/bestconstant.pdf
2. Musina and Nazarov, “On the Sobolev and Hardy constants for the fractional Navier Laplacian,” Nonlinear Analysis 121 (2015), 123–129, https://doi.org/10.1016/j.na.2014.09.021, https://arxiv.org/abs/1408.3946. Publisher text and abstract checked. Their extension compares fractional Dirichlet and Navier operators in the Hilbert setting; it does not classify other boundary conditions in the integer-order general-p question.
3. Do Ò, Furtado, Medeiros and Ratzkin, “Weighted Hardy-Sobolev type inequalities with boundary terms,” https://arxiv.org/abs/2602.08702 (submitted February 2026). Abstract checked only. Weighted inequalities with boundary terms on unbounded domains do not, on the inspected evidence, resolve preservation of both original bounded-domain homogeneous constants. No full-text verification of this paper is claimed.

## Authored mathematical guardrails

For a linear space X with W_0^{m,p}(Ω)⊆X⊆W_ϑ^{m,p}(Ω), both sharp constants equal the common endpoint constants by monotonicity of infima, provided the endpoint Hardy equality applies, for example 0∈Ω. This supplies many additional constraints but is an immediate corollary, not an exhaustive answer. Requiring more traces on part of the boundary while retaining all Navier traces produces examples in this sandwich; any claimed novelty must exclude these inherited examples.

Conversely, a boundary condition allowing a nonzero constant cannot preserve a positive constant for either displayed homogeneous quotient: the energy is zero and both denominators are positive (the Hardy integral is finite when mp<n). This excludes unrestricted and ordinary pure Neumann spaces in the formulation that admits constants. Adding a mean-zero constraint, a boundary energy, or a lower-order norm changes the problem and requires separate analysis.

Do not assert Hardy sharpness for arbitrary domains avoiding the origin merely because the universal inequality holds. For instance, in the m=1,p=2 case, a tiny ball far from the origin has weighted quotient bounded below by dist(0,Ω)^2 times its Dirichlet first eigenvalue, which can exceed the whole-space Hardy constant. Explicitly put 0∈Ω in a sharpness formulation.

## Replay and duplicate check

Searched all 15,458 problem records and all 6,701 research-result entries using target ID, source code, distinctive title, boundary-question phrase, primary-paper DOI/title and Navier/Hardy–Sobolev terms. No direct research-result record for OWR-4209-004 and no exact problem duplicate found. Neighboring records from the same report concern hinged-plate positivity, p-Laplacian nodal geometry, extension domains and Korn–Sobolev questions, not this classification. Broad Navier matching produces numerous unrelated Navier–Stokes records; these are not duplicates.

Current web searches used exact question and paper titles, author/Hardy/Sobolev/boundary combinations, mixed-boundary and Robin terms, and 2024–2026 qualifiers. They found relevant extensions but no verified classification. One mixed-boundary publisher page returned 403; no conclusions rely on its inaccessible full text.

## Next admissible work

Specify a nontrivial class of local boundary operators beyond nested Navier subspaces, then test both quotient infima with identical energy and hypotheses. The source does not prescribe such a class, so a candidate-family theorem is partial progress, not a complete classification. No publication or queue changes were made.
