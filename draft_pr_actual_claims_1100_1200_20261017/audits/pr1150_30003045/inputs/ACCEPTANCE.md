# Acceptance of the mixed Kato kernel counterexample

## Decision and review status

ACCEPT: the arbitrary-exponent three-summand equality in the original Question 2 is false at its allowed index n = 1. No mathematical correction to the submitted counterexample was required by the independent internal AI audit. The original n = 0 equality is valid under the stated bilinear Pfister convention with dimension at least two.

The accepted proof has 12,061 bytes and SHA-256 b1533a032e031d82a0d124cdb410e86e5ee59af477dd711d2157a5d72f36e2ca. COUNTEREXAMPLE.md preserves those exact bytes. AUDIT_REPORT.md preserves all 9,966 bytes of the independent mathematical audit, including its alternate explicit norm computation and all-parameter residue exclusion.

This is an AI-assisted authored proof and independent internal AI mathematical/source review. It is unrefereed. No external human peer review, journal acceptance of these documents, formal proof-assistant certification, novelty, or priority is claimed. Acceptance is specific to the audited argument and its stated standard-theorem dependencies.

## Accepted content

The base field is F = F_2(b,z,s,t). The extensions satisfy beta^4 = b and theta^2 + theta = s^(-1), and the bilinear Pfister form is <1,t>_b. The degree-four inseparable extension has exponent two; the quadratic Artin–Schreier extension is genuine; and the form remains anisotropic over the inseparable extension.

For the binary projective quasilinear quadric, the function field is F(sqrt(t)). Its zero-dimensionality causes no exception to the stated convention. The class represented by s^(-4) b z^2/(1+b z^2) dlog z becomes [s^(-1),1+beta^2 z) over L and dies over LK.

To exclude the complete three-summand sum, restrict to M = L F(B). This kills both the purely inseparable and the Pfister summands. Every remaining quadratic-kernel class has the fixed first slot s^(-1). Completion at s and the cyclic norm criterion would force (1+beta^2 z)/c_0 to be a square in the residue field for some c_0 in F_2(b,z,t)^*. The square-field coefficient comparison makes that impossible for every c_0. Thus the additional Pfister summand is included in the exclusion, rather than silently discarded.

The original index n = 0 is addressed separately by the impossibility of gaining Artin–Schreier roots through purely inseparable or rational extensions and the associated quasilinear-quadric function field. The example does not contradict exponent-one results. Replacing the independent Pfister slot t by z absorbs the class, as the proof and audit explicitly explain.

## Credit and inspection limits

The mixed-generator mechanism is already present in Aravire, Laghribi and O'Ryan, Cohomological kernels of mixed extensions in characteristic 2, Journal of Algebra 542 (2020), 249–276, DOI https://doi.org/10.1016/j.jalgebra.2019.09.012. The inspected author manuscript is dated 15 August 2019. Its generator correspondence is credited; it is not used as a substitute for excluding the extra Pfister summand.

The complete author and independent source reports retain their inspection limits. Four freshly downloaded PDF files matched the supplied bytes. Milne was inspected as web text only, with no local PDF hash or visual inspection. Voight was inspected through publisher HTML. No byte comparison to the mixed-kernel paper's published typeset PDF or exhaustive later-literature survey is claimed. Preparation of this edition adds no new source inspection.

## Verification and editorial scope

The author's 13 exact algebra diagnostics and the independent audit's 25 finite checks passed in ordinary Python, Python -O and Python -OO. The independent deliberately incorrect expectation was rejected in all three modes. These finite diagnostics and integrity checks are not a substitute for the mathematical argument.

The proof, independent mathematical audit, independent source report and independent verification report are preserved byte for byte. Only the author's obsolete awaiting-audit status and related public-edition wording are updated; their mathematical and source-inspection substance is retained. The acceptance, reading guide, manifest and selected public retrieval metadata are edition framing.
