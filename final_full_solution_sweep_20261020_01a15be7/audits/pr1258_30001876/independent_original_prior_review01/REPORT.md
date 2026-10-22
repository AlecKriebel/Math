# PR1258 / 30001876: full prior reconstruction, explicitly repaired normalization

Independent review22 October2026 UTC. Exact head a6e7e6f25f9ede706c80d6f7246a065011df501f; base4b27092a448d53b61408355ce44ec38d103a1ce4. All eight added blobs and live PR body were fetched independently and match these pins. No QUEUE or other path changes occur. Overall sweep80%; this review's completion is not completion of global accounting.

## Decision

Accept full coverage of the original introductory inner-product/spectral-decomposition request in its natural level-one spherical Hecke–Maass cuspidal setting, as credited prior work. This is not acceptance of all literal normalization displays, the whole43-page article, a new theorem, a worldwide firstness claim, or the sharp restriction estimate. A proposed exact four-string row with blank B is in ROW_PROPOSAL.json; root must read this report and the complete new derivation before adopting it or taking any service action.

The fixed-scale cusp-plus-Eisenstein expansion and inverse Mellin reconstruction are sound, with the stated foundational spectral, Fourier–Whittaker, reduction/derivative-decay and continuation imports. The coefficients have a genuine unfolded L-series/kernel formula, rather than merely a circular definition as inner products. The contested special-function constant can now be established directly from the printed Jacquet integral. This replaces the earlier challenge's conditional Bessel import with an explicit independent proof of precisely the required identity. It does not retroactively claim that the previous audit read the original Stade or Takhtadzhyan–Vinogradov proofs.

## Original target and publication authentication

I independently fetched the [EMS report](https://ems.press/content/serial-article-files/46359), read Li's contribution on printed2405–2406/PDF9–10, and visually checked the controlling p.2406. It describes joint work with Matt Young, a codimension-two GL3 restriction through an upper block GL2 embedding, its inner products with SL2 Maass forms, and the more general spectral decomposition. The next paragraph reports their restriction result. It is introductory motivation in a report of existing work, not a separately numbered unsolved conjecture. The wording O2(Z) is clarified to O2(R) in the final paper. The final geometry is upper block diagonal with a positive scale, not an arbitrary upper triangular subgroup.

The authenticated prior source is Xiaoqing Li and Matthew P. Young, [The L2 restriction norm of a GL3 Maass form](https://doi.org/10.1112/S0010437X11007366), Compositio Mathematica148(3)(2012),675–717, online20 March2012. Fresh DOI resolution returned200; Crossref, publisher landing page and actual publisher PDF agree on title, authors, journal, volume, pages and DOI. The890,977-byte final PDF has SHA2564d9e561254394b453a0bea6bc7de585f6138c82c54949db836fdf6b8669fed7b. The correct same-paper preprint is [arXiv:1102.0195v1](https://arxiv.org/abs/1102.0195), whose primary metadata explicitly carries the same journal DOI. It is531,373bytes with SHA2564041d355d80156972023a0c97342359e8334f8e1903820b2c4e00c8ff5b81b7b.

The root task's1012.1356 lead is an unrelated physics paper, independently authenticated as such. It is not an alias or a defect in the PR, which correctly cites1102.0195. DOI10.4171/OWR/2011/43 identifies the original question-containing report, not the result DOI proposed for C.

The final article itself separates Sections2–4, which give standard automorphic background, period formulas and the spectral identity, from the later sharp-bound argument. I read the relevant actual definitions, full Proposition3.3 proof, full Proposition3.4 proof, Proposition3.5 statement and Corollary3.6, and the full Theorem4.1 proof. Proposition3.5 has no written proof in the source; its Eisenstein unfolding is reconstructed here, not counted as an inspected omitted proof. Sections5–10 are not mathematical premises for the scoped reconstruction and were not proof-audited. Reading the introduction's outline is not reading their proof bodies.

## Findings retained from the PR

The four-equation incompatibility is real. Write W*=D W for the completion(3.13), I for the common local integration functional and P− for the printed six-gamma numerator. The printed equations say G=4I(W), G=P−/D and I(W*)=P−/(4D). Linearity instead makes their first and third statements imply G=P−/D². Generic D is neither1 nor0. This cannot be repaired by a later spectral measure or by changing a Fourier index. I visually checked printed683–684, including the actual D denominator in(3.20). The older preprint repeats the problem and supplies no independent correction.

The literal U2 stabilizer factor2 is also real. The source defines U2 with diagonal entries1, so −I is absent; yet ±γ give equal spherical Whittaker seeds on the upper-block restriction. The source's Eisenstein normalization itself inserts1/2 for this same quotient. Under ordinary hyperbolic measure, unfolding to the effective strip thus contributes2. Combining it with the GL2 Fourier K factor2 and the even sign-pair factor2 gives8J, not4J. Changing only the coset notation while leaving all Fourier coefficients unchanged would alter the Fourier expansion.

No factor-two-only erratum is asserted: those two intermediate factor errors can compensate in a specified convention. The different power-function orientation also matters. Blomer's actual raw definition and power function on preprintpp.6–7, with notes3–5, independently confirm the convention mapping and historical8-versus4 warning. I use neither his following modified-W display nor a repeated-argument display in another paper to choose constants.

## New independent repair of the essential local identity

The complete proof is in INDEPENDENT_DERIVATION.md, Sections1–5. Starting from the literal source(2.1)–(2.3), it computes the bottom-row and wedge norms of wu diag(ab,a,1). The two denominator quadratics are

R=a²b²+a²y²+z², Q=a²b²+b²x²+(z−xy)².

Gamma-Laplace representations, an elementary z Gaussian integral, and t=h(1−v),s=hv reduce the remaining expression to the product

(a²+(1−v)x²)(b²+vy²).

Two elementary Fourier-Laplace evaluations then give the complete double-Bessel formula. Its prefactor is4 after completion, followed by2 from v=u²/(1+u²), hence8. The starting domain Re(3ν1/2),Re(3ν2/2)>1/2 justifies Fubini absolutely; the standard Jacquet continuation extends it. This is a fresh proof of the central disputed GL3 normalization, not an appeal to a historical constant or to numerical agreement.

The subsequent Bessel Mellin and beta integrals give the exact double Mellin constant1/4. A final K Mellin inversion contributes1/4 and z=2w contributes2; Barnes' second lemma gives the completed GL3×GL2 integral P/8. The full five-gamma/one-denominator version and its pole separation are stated in the derivation. Barnes' lemma remains a standard foundational import, also checked against Dufresne's actual primary web-extracted statement and Theorem4.3 proof on PDF10–12. Dufresne's full36-page paper and earlier probabilistic foundation are not claimed re-proved or byte-pinned here. NIST10.43.19 confirms the Bessel Mellin normalization; NIST5.13.3 is only Barnes' first lemma and is not misidentified as the second lemma.

For A=1−ν1−2ν2,B=−ν1+ν2,C=2ν1+ν2−1 and P± the six-gamma products with signs±{A,B,C}, the result is:

- Literal printed Jacquet power function: H=8J=P+/D.
- Explicitly interchanged Bump power function, with matching raw Jacquet function/Fourier convention: H_Bump=8J_Bump=P−/D.

These identities no longer need the earlier unverified Whittaker Bessel import: it has been supplied directly. They do continue to use the explicitly stated elementary/special-function foundations. They are not the same expression for a fixed convention, and no identification of F with its contragredient or of Fourier coefficients across changed conventions is made. In the literal convention, keeping G_int=4J makes its corrected closed expression P+/(2D), and the period is2 conjugate(ρ(1))L G_int. Introducing H=8J avoids overloading the conflicting symbol G. The simultaneous printed-consistency hold therefore remains; an explicit repaired normalization does not make the old four assertions all true.

## Why this covers the original reconstruction request

For f_r(z)=F(diag(rg_z,1)), the unfolded even period is Λ_j(s)=conjugate(ρ_j(1))L_j(s)H_tj(s), with L_j(s)=ΣA_F(m,n)λ_j(n)/(m²n)^s. The continuous term has the identical unfolding with the Eisenstein Fourier coefficient; its constant Fourier terms disappear against nonzero Whittaker characters. F and A_F are not silently normalized: multiplying F by c multiplies both Λ and this L-series by c. The conjugation ofρ is required by the chosen inner product and is checked by a phase control.

At every r, group symmetry kills odd cusp coefficients and unfolding kills the global constant component. This does not kill the full GL2 continuous spectrum. With Λ(s)=∫c(r)r^(2s−1)dr/r, inversion is c(r)=(1/π)∫Λ(1/2+it)r^(−2it)dt; a single central L-value is not a fixed-r coefficient. GL2 spectral density is1/(4π); combined with Mellin Plancherel it gives norm factors1/π and1/(4π²), exactly as in the integral-defined Theorem4.1 proof.

The derivation explicitly checks decay at both scale ends using short row-lattice vectors of the determinant-one representative, then invokes the standard cusp-form derivative-decay/reduction theorem. This supplies finiteness and fixed-coefficient Schwartz behavior without assuming the sharp restriction bound. L2 inversion and expansion are sufficient for spectral decomposition; smooth pointwise/local-uniform conclusions use their stated extra estimates. No global interchange of the entire spectral/Mellin family is assumed. The source's cuspidal setting is not replaced by arbitrary noncuspidal representations, other levels, K-types or embeddings.

Thus the exact integral-defined reconstruction is complete within the actual source's intended setting, and an explicit normalization repair is available. Treating unread Sections5–10 as a missing premise would demand a different claim. The natural setting is obtained from the original joint-work context and the final article's geometry and Fourier expansion, not manufactured to save an unrelated partial result.

## Independent controls and limits

The read-only reviewer checker binds the eight PR blobs, nested manifest, ledger capture and source receipts. Sixteen exact rational cases verify row/wedge quadratics, Gaussian factorization, power/completion exponents and parameter mappings. Four independently computed Barnes contour integrals use opposite nonsymmetric triples and two cutoffs/grids; relative errors are below8×10^(−15). The opposite triples differ by about0.13 relatively, so sign errors cannot hide in a self-dual test. Gaussian inversion tests frequency2t and1/π. Deliberate invalid factor, sign, stabilizer, phase and provenance variants are rejected. Normal,-O,-OO results agree. These finite floating-point diagnostics support transcription and falsification; the written proof establishes the identity. No interval-validation, formal automorphic theorem certificate or author-code execution is claimed.

The original Stade1990 URL again returned an HTML bot-block body, not a PDF; its proof remains unread. Direct Dufresne download returned403, but its public primary web extraction supplied the specified lemma/proof passage. No complete source reading is inferred from whole-file retrieval. Raw source/ledger/PR bodies and page images stay private; public files contain authored reasoning, proposed cells and receipts. The final seal covers every actual recursive member except the exact seal itself, including the private-body seal and nested PR manifest. This AI-assisted review is unrefereed; no authors' AI use, official erratum, paper-wide acceptance, worldwide firstness or publication-accounting completion is asserted. No service, Git, CASE, cursor or credential inspection/mutation occurred.
