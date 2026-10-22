# Independent exact-target finding (sealed before proof exposure)

UTC checkpoint: 2026-10-17T23:15:53.473164+00:00. Completion estimate: 30%.

No PROOF.md, old AUDIT, status, acceptance, root finding, or concurrent review has been read.

Original question: OWR 33/2012, Colbois talk, printed 2034–2036 (PDF pages 22–24), Theorem 3 and final open question. For every dimension m≥2, does there exist a pair of constants A_m,B_m depending only on m, such that every bounded smooth Euclidean domain Ω⊂R^{m+1}, and every integer k≥1, satisfy

λ_k(∂Ω)|∂Ω|^{2/m} ≤ A_m I(Ω)^{1+2/m}+B_m k^{2/m},
I(Ω)=|∂Ω|/|Ω|^{m/(m+1)}?

Operator: intrinsic scalar Laplace–Beltrami on the entire induced boundary; not the Dirichlet spectrum inside Ω and not Steklov. The talk says spectrum of the Laplacian on compact Riemannian manifolds; its CEG reference supplies the Laplace–Beltrami and indexing definitions.

Boundary connectedness: no requirement survives the standing conventions check. This is supported positively, not just by omission: the same CEG paper, Example 3.1 on page 14, explicitly uses Ω_i=N_i×(−L_i,L_i), its two boundary components, λ_1=λ_2=0 and λ_3=λ_2(N_i)>C. The main theorem and general result impose bounded smooth domain hypotheses without a separate global connected-boundary convention. The generic introductory description of λ_2 as first positive is not a universally enforced connected-boundary assumption, since Example 3.1 explicitly handles extra zeros. The all-eigenvalue min-max formula uses k-dimensional subspaces of H¹(Σ), so repeated eigenvalues, including every zero, are counted.

Domain connectedness: the source uses domain without a separately stated definition. The standard connected-open-set interpretation is the conservative admissible class; constructing connected Ω suffices under either convention. No genus or sphere-topology restriction is imposed in Theorem 3 or its open question. CEG dimension is n≥2; OWR uses m. The targeted full negative statement m≥2 therefore matches the dimensional scope. A disconnected-boundary construction would not answer a separate stronger question restricted to connected boundaries, but it can answer the actual stated question.

Primary source versions: EMS PDF DOI 10.4171/OWR/2012/33, 64 pages; arXiv PDF 1007.0826v2, margin date 2 October 2011 and embedded compilation date May 25, 2022, 19 pages. Local independent bytes and rendered page artifacts are in sources/. Full Colbois talk rendered pages visually inspected; CEG text inspected for standing definitions and all main statements, min-max, proofs, examples, and references; rendered pages 1,2,14 visually inspected so far.

Core conclusion: target scope permits the claimed two-component boundary. No target mismatch found.
