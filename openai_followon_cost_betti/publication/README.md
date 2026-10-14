# L2-acyclicity and cost for a rank-100 amalgam

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X.
Date: October 6, 2026. License for this original note, code and audit text: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/.

This is an expanded consequence and verification note for OpenAI's *A group without fixed price*, family 259, pinned to `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The group and positive Bernoulli cost bound are due to OpenAI. Gaboriau supplies cost--Betti comparison and action invariance; the general connection with fixed price was already explicit in Popa--Shlyakhtenko--Vaes by 2018. The earlier conditional limit argument was already public in our preliminary triage (commit `387962dc519c86b1d1833cb0a41bd3fbddd2b446`). This note adds a self-contained direct cellular calculation, a proof of asphericity and all-degree L2-Betti vanishing, and a checked dependency record. It makes no assertion of being first or of an independent fixed-price discovery.

## Exact resolved scope

Let A=F(a,b_1,...,b_99), w=ab_1ab_2...ab_99a, J=<b_1,...,b_99,w>, and Gamma=A*_J(J x <t>). Equivalently Gamma has 101 generators and 100 commutation relators [t,b_i], [t,w]. Its displayed presentation complex is a finite two-dimensional K(Gamma,1). Every L2-Betti number of Gamma is zero by the direct proof, independently of both cost estimates.

The conull free part X of the product-Lebesgue Bernoulli shift [0,1]^Gamma is free, ergodic and p.m.p. Its orbit relation has every L2-Betti number zero and Cost(R_X)>=1+1/(100*2^61), using the explicitly cited OpenAI positive cost input. This gives strictness in Cost(R)-1>=beta_1(R)-beta_0(R). The group infimum cost is one and satisfies Cost_*(Gamma)=1+beta_1(Gamma). The zeroth correction remains necessary for finite classes.

The Bernoulli positive cost gap is inherited from the full compression/deployment/finite-model/rank/planar argument; it is not proved by the invariant calculation. The source warns that its input was intermediate and not established to be the final revision. The exact source proof was read and independently challenged; scoped proof audits accompany the package. No relevant Lean proof was identified, no machine formalization is claimed, and numerical or finite-case checks are not substitutes for the mathematical proofs.

## Contents and reproduction

`main.tex` is a single self-contained source with inline bibliography. `paper.pdf` is the exported paper. `cost-betti-source-and-verification.zip` contains the source and verification materials. Inside that archive, run:

```sh
python3 verification/verify_exact.py
python3 verification/finite_boundary_check.py
python3 verification/check_fox.py
python3 verification/verify_constants.py
tectonic main.tex
```

Alternatively compile `main.tex` twice with an existing pdfLaTeX installation. The verification scripts use only Python's standard library. The second check covers 329,027 finite contraction cases; it does not prove the Borel or infinite-class arguments. Software versions and clean-build output are recorded under `reproducibility/`. Exact inspected upstream file hashes are in `upstream/UPSTREAM_MANIFEST.json`; original third-party PDFs and TeX are cited, not bundled. The additional Fox checker reproduces the independent algebraic checks for ranks 0, 1, 2 and 99, and the constants checker independently reproduces the exact rational inequalities. The original upstream TeX was separately rebuilt in an isolated copy after three engine-specific metadata primitives were guarded for Tectonic; mathematical text was unmodified.

`proof-audits/` gives source pointers, exact mathematical checks, limitations and reviewed versions. `priority/` preserves the dated audit and its corrections/addenda. Historic provisional reports describe the scope and status of their own check, not a claim that later package review has been completed. The final exact upload set and completed fresh reviews are identified by the external frozen-package/review records in the [public project folder](https://github.com/AlecKriebel/Math/tree/main/openai_followon_cost_betti), under `receipts/` and `reviews/`; archive contents are fixed before those complete-package reviews.

AI tools were used extensively in research, drafting and verification. This preprint has not undergone conventional human peer review/refereeing at publication. Automated adversarial reviews are evidence rather than formal proof certificates or human refereeing. No affiliation or coauthor is asserted. No individual was contacted.

