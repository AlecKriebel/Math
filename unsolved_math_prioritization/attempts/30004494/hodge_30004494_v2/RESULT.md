# 30004494: original target remains unresolved

## Verdict

Five substantive approaches were completed. No proof or counterexample to the full boundary-corrected ampleness conjecture was obtained. The retained results are rigorous algebraic controls and a reconstruction of a known surface mechanism. They carry no novelty claim. Status for the original target: **unsolved after 5/5 attempts** (workflow state: exhausted). The v1 mathematical partials passed independent audit; this v2 corrects its one mandatory literature-scope issue and awaits delta acceptance. AI-assisted, unrefereed.

## Exact target and conventions

Write X for the smooth projective compactification and U=X minus Z, where Z=union Z_i is a reduced simple-normal-crossing divisor. A pure polarized variation of Hodge structure of effective weight n>=1 on U has period map Phi:U->Gamma\D, fixed Hodge numbers, polarization Q, Hodge filtration F^p and Deligne extensions F_e^p. In the integral setup, Gamma is the image of the monodromy representation of pi_1(U) in Aut(V_Z,Q); it need not equal an arithmetic group. The unipotent-monodromy setup is the one used for the clean tensor identities and quoted modern semiampleness theorem here. Quasi-unipotent reductions require care with ramification and extension conventions, and are not silently substituted.

The 2021 precise source uses the augmented line bundle

L = tensor product, for p=ceil((n+1)/2),...,n, of det(F_e^p).

The logarithmic Gauss-Manin differential is a bundle map

Psi:T_X(-log Z) -> Gr^(-1)_F End(E_e), where E_e=direct sum Gr^p_F(V_e).

The target assumes fibrewise injectivity of this map everywhere. It asks for one vector of nonnegative integers (a_i), independent of m, and an integer m_0, with

mL - sum a_i Z_i ample on the original X for every integer m>=m_0.

The source report uses suitable local Torelli assumptions and identifies this logarithmic condition. Its primary location is Robles's contribution, printed pp.1306-1308 of [OWR24/2020](https://publications.mfo.de/bitstream/handle/mfo/3797/OWR_2020_24.pdf). The displayed bundle definition and formal conjecture are in [GGR 2021, (1.2), Conjecture 1.10(b), Remark 1.13](https://arxiv.org/abs/2102.06310). We do not replace the target by generic immersion, by semiampleness, by ampleness only on a quotient, or by a result after changing X.

## What is retained

See [PROOFS.md](PROOFS.md) for complete arguments:

- An exact criterion: the correction E must be negative on every nonzero class in the entire closed L-null face. Compactness gives a uniform threshold once that condition is known.
- A proof that real, rational and fixed integral correction coefficients are equivalent for the ample-existence problem when L is nef.
- A constructive surface theorem with rational coefficients computed by -A^(-1)1, including disconnected intersection matrices and a single threshold for all curves.
- An actual blowup construction showing why generic immersion is insufficient, explicitly outside the original fibrewise-injective hypotheses; and stability of a successful correction under boundary blowups.
- A finite rational-polyhedral feasibility criterion, a dual impossibility certificate, and exact arithmetic controls showing why independently successful local choices need not be globally compatible.

## Literature update that changes the interpretation

[BFMT, arXiv:2508.19215v2](https://arxiv.org/abs/2508.19215v2), Corollary 1.3, proves semiampleness for the **full Griffiths bundle** with unipotent local monodromy. Theorem 1.2 identifies an ample bundle on the new period-image compactification and its pullback. This is important progress but does not itself supply an effective boundary correction on X. Moreover the full product and the earlier upper-half augmented product are different in odd weight. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) gives the exact comparison.

Two historical hazards were checked: [arXiv:2106.04691](https://arxiv.org/abs/2106.04691) is withdrawn because its Theorem 1.7 proof is incomplete; [arXiv:2010.06720v6](https://arxiv.org/abs/2010.06720v6) corrects previous determinant-descent assertions and exhibits an odd-weight failure of descent. Neither is used as an unconditional completion theorem. The 2025 generalized toroidal construction allows a base modification in general, but Theorem 2.11 retains the original compactification under its simplicial condition. In the integral/unipotent framework here, logarithmic local Torelli implies independent local monodromy logarithms, which satisfy that condition. Thus a base change is not a necessary obstacle for this input. Projectivity of the generalized toroidal target remains Conjecture 2.12, and the construction does not supply the required fixed effective boundary correction.

## Sharp remaining gap

No common nonnegative boundary coefficient vector has been proved to make -E positive on the complete closed L-null face in arbitrary dimension. Fibrewise theta identities, projective period images, and semiampleness do not by themselves establish it. The five approaches stop at this gap. Further numerical examples cannot resolve the missing Hodge-geometric compatibility statement.

## Reproducibility and scope

Run `python3 verify.py` from this folder. It uses only the Python standard library and performs exact rational arithmetic; it neither downloads sources nor writes remote state. `VERIFICATION.json` records its reproducible result. `SOURCE_MANIFEST.json` records public source URLs, PDF hashes/sizes and inspection scope. Source PDFs, extracted text, images, raw datasets and private coordination files are excluded from this packet. No remote write was made by the author.
