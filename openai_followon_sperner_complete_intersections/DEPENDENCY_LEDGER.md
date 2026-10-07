# Dependency ledger

| ID | Precise needed assertion | Source and validation basis | Current status / gap |
|---|---|---|---|
| D1 | Hilb A=∏(1+t+⋯+t^{d_i−1}); A is Gorenstein with symmetric unimodal Hilbert function | Regular-sequence exact sequences; standard CI duality; bounded-product chains | Formula checked; full note proof pending |
| D2 | For any homogeneous ideal containing a full regular sequence of degrees ≥2 over C, a homogeneous ideal containing the corresponding pure powers has the same Hilbert function | OpenAI, Commuting Division-Coefficient Forms…, Corollary 1.2, via Theorem 1.1; LPP Theorem 1.1 HF portion | Central audit in progress, no formalization claim |
| D3 | D2 extends to any characteristic-zero field via a common finitely generated coefficient field embedded in C and flat base change | Upstream 09-consequences and LPP 08-characteristic-zero | Exact descent under check; no embedding of arbitrary k into C required |
| D4 | EGH for every containing homogeneous ideal of a given standard graded Artinian CI implies its Sperner property | Harima–Wachi–Watanabe, arXiv:1601.06928, Theorem 11; DOI 10.1090/proc/13347 | Primary text read; independent reproduction in progress |
| D5 | μ(I)≤μ(in_m I) for arbitrary ideals; linear elimination and field extension preserve generator/Hilbert dimensions | Associated graded inclusion in_m(mI)⊃m in_m(I); graded isomorphism; faithful flatness | Self-contained proofs in progress |

Only full-length EGH Hilbert-function strength is needed. LPP Betti domination, arbitrary regular-sequence length, and local cohomology consequences are outside the necessary dependency chain. No applicable lean/docs/200.md or family-200 entry was found; unrelated Lean filenames containing “200” are not verification.
