# Source-scope and prior-art adjudication: canonical tightening of wavelet frames

Date: 14 October 2026 UTC. Target: Michael Frank's question in OWR 10/2004; problem 30000043 / OWR-720-011.

## Decision

**The accepted Haar-perturbation proof supplies a negative answer to the source question under its usual indexed, single-generator meaning.** It is not merely a counterexample to an arbitrarily selected unrelated variant. The natural interpretation preserves the dilation, translation lattice, generator count, and indexing of the canonical family. That reading is supported by the source's surrounding unitary-system discussion and the precise later canonical-Parseval formulation of Bownik–Jasper–Speegle.

No claim is made about representing the resulting unordered collection after an arbitrary permutation, changing the lattice or dilation, or changing the number of generators. Those are stronger or different questions; their exclusion is not required to refute the usual indexed preservation claim. No historical novelty or literature-wide present-day openness claim is certified.

This document adjudicates source match and prior credit. Mathematical acceptance is supplied by the separately pinned proof and independent audits below; this adjudication adds no new mathematical construction or proof pass.

## 1. Original source and standard scope

Michael Frank, *Approximation of Frames by Normalized Tight Ones*, in *Mini-Workshop: Wavelets and Frames*, Oberwolfach Reports 1 (2004), report 10, contribution beginning on printed p.529; question on p.531 immediately before Theorem 5. [Publisher](https://ems.press/journals/owr/articles/720); [official report PDF](https://ems.press/content/serial-article-files/45879); [DOI](https://doi.org/10.4171/OWR/2004/10).

Frank uses S=(θ*θ)^−1. The questioned family S^(1/2)x_i is therefore F^(−1/2)x_i for the ordinary frame operator F=θ*θ, not the canonical dual F^(−1)x_i. The source discusses a fixed unitary system and its generating vectors, then states the positive semi-orthogonal case for one generator with atoms |det M|^(j/2)φ(M^j x−k). It credits Deguang Han, *Approximations for Gabor and wavelet frames*, Trans. AMS 355 (2003), 3329–3342, [DOI](https://doi.org/10.1090/S0002-9947-03-03047-2).

The short question is informal about alternative reindexings. The indexed interpretation is source-supported, without claiming the sentence expressly excludes every possible convention. A full-space one-dimensional dyadic counterexample lies within the ordinary wavelet setting and avoids subspace and multiple-generator ambiguities.

## 2. Indexed preservation is established literature terminology

Bownik, Jasper and Speegle, *Orthonormal dilations of non-tight frames*, Proc. AMS 139 (2011), 3247–3256, [published author-hosted PDF](https://pages.uoregon.edu/mbownik/papers/44.pdf), [DOI](https://doi.org/10.1090/S0002-9939-2011-10887-6), Theorem 4.1, equation (4.3), and Remark 4.1 on p.3255 express the property as local commutation:

    F^(−1/2) D^j T^k φ = D^j T^k η for every j,k;
    η = F^(−1/2)φ.

Their remark identifies this with the canonical Parseval family remaining affine. Their dilation theorem assumes the condition and proves it necessary for the stated conclusion. The introduction describes a proper subclass of non-tight frame wavelets. Thus this formulation and distinction are prior context. The inspected paper does not exhibit the present classical example or its inverse-square-root calculation.

Their convention is DTD^−1=T². For the expanding physical dilation Δf(x)=√2f(2x), take D=Δ^−1; the relation then holds. Since j runs over all integers, j↦−j aligns the scale conventions. This is not arbitrary reindexing of the target family.

Bownik–Lemvig, *The canonical and alternate duals of a wavelet frame*, ACHA 23 (2007), 263–272, [published PDF](https://pages.uoregon.edu/mbownik/papers/29.pdf), [DOI](https://doi.org/10.1016/j.acha.2007.04.004), pp.264–265, separately defines preservation using the same generator count and an indexed translation/local-commutant relation. Its operator is F^−1; it corroborates terminology but does not prove canonical-tight failure.

## 3. Exact match of the accepted witness

Let h=1_[0,1/2)−1_[1/2,1), Δf(x)=√2f(2x), T_kf(x)=f(x−k), and φ=h+(1/100)Δh.

The pinned proof establishes that {Δ^jT_kφ : j,k∈Z} is a Riesz basis for all L²(R), with valid frame bounds 9801/10000 and 10201/10000. Its ordinary frame operator is exactly F=AA*, where A=I+(1/100)V and V maps the Haar basis vector e_(j,k) to e_(j+1,2k).

A norm-convergent functional-calculus series for the actual inverse square root gives

    ||F^(−1/2)T_1φ − T_1F^(−1/2)φ|| > 1/1000.

The independent acceptance audit verifies this obstruction and strengthens the lower bound to 19/5000. Any same-index affine generator is forced by (0,0) to equal F^(−1/2)φ; failure at (0,1) rules it out. This refutes the universal classical single-generator assertion. Neither a canonical-dual substitution nor numerical truncation is involved.

## 4. Prior credit: the perturbation family and coordinate mechanism are classical

The generator family must not be presented as newly discovered. Daubechies and Bin Han, *The canonical dual frame of a wavelet frame*, ACHA 12 (2002), 269–285, [author-hosted published PDF](https://sites.math.duke.edu/~ingrid/publications/ACHA_12_2002.pdf), [DOI](https://doi.org/10.1006/acha.2002.0381), p.271 equation (1.6), gives ψ=η+ε√2η(2·), 0<ε<1, for any orthonormal wavelet η. This includes η=h and ε=1/100. It credits Daubechies (1990) and Chui–Shi (1993) for canonical-dual counterexamples in this family.

Daubechies, *The wavelet transform, time-frequency localization and signal analysis*, IEEE Trans. Information Theory 36 (1990), 961–1005, [published author-hosted PDF](https://sites.math.duke.edu/~ingrid/publications/ieee36-1990.pdf), [DOI](https://doi.org/10.1109/18.57199), pp.988–989, attributes the perturbation to P.-G. Lemarié, communicated by Y. Meyer. Its p.989 construction uses a scaled-wavelet perturbation and a basis-index partial isometry with an even/odd adjoint action, studying canonical duals and their regularity. Thus both family and basic coordinate mechanism have prior provenance. No unverified printed sign or frame-bound formula from that scan is imported into the accepted proof.

Chui and Shi, *Inequalities of Littlewood–Paley Type for Frames and Wavelets*, SIAM J. Math. Anal. 24 (1993), 263–277, [publisher/DOI](https://epubs.siam.org/doi/10.1137/0524017), is credited through the explicit 2002 attribution; its full text was not inspected here.

Bownik–Lemvig (2007) corrects the 2002 paper's later argument about canonical-dual failure despite existence of alternate wavelet duals. That correction does not invalidate every statement of the 2002 paper. Here its p.271 formula supplies observed provenance; the current inverse-square-root proof is independent.

The honest description is **a direct, quantitatively audited canonical-tight analysis of a classical wavelet perturbation family**. The checked sources do not determine whether that inverse-square-root argument or conclusion was previously published. Do not advertise novelty or priority.

## 5. Mathematical evidence pins

The following authored artifacts were inspected at these exact bytes. Names are artifact names, not third-party source attachments.

- Proof, *An explicit dyadic Riesz wavelet whose canonical tightening loses its natural affine indexing*, COUNTEREXAMPLE.md: 7,499 bytes; SHA-256 8c943a270c9b35d0cf3ddef2b94de5ec8bbbcb4ec45deca81d28fd2228e522a1.
- Independent acceptance, *Independent audit of the Haar perturbation counterexample*, ACCEPTED_AUDIT.md: 7,735 bytes; SHA-256 1fc355da72d93121de4db00658e4a2c130c94eb03831a24925d3752bf52cc964.
- Separate check, INDEPENDENT_HAAR_CHECK.md: 2,293 bytes; SHA-256 58ed145c605d3568b6592474a9566fe5c05d31cbac535db59395feb38f214c1f.

These pins bind the adjudication to accepted mathematical versions, without claiming later editorial versions have identical bytes.

## 6. Recommended disposition

For queue row 1781 / problem 30000043, after acceptance of the pinned proof and audits:

- Status: **solved**, qualified as **negative answer under the usual indexed single-generator interpretation**.
- Turns: **1/5**, denoting the one shared mathematical pass producing this proof, not certified lifetime history.
- Suggested Findings: “Explicit full-L²(R) dyadic Riesz-wavelet counterexample φ=h+0.01Dh: canonical F^−1/2 translation defect at (0,1) is >0.001; independently audited. Resolves usual same-index, same-lattice, one-generator preservation. Classical perturbation family credited to Lemarié/Daubechies and Chui–Shi; Bownik–Jasper–Speegle local-commutant formulation credited. Arbitrary reindexing and historical novelty not claimed.”

Do not classify this as a verified prior-solved literature result: the earlier sources verified here concern the classical perturbation, canonical duals, or a conditional characterization. Canonical-tight failure rests on the accepted explicit proof. Conversely, do not leave the standard claim unsolved solely because arbitrary permutation has not been excluded.

## 7. Bounded search and distribution limits

The search covered the source and neighboring theorem; Bownik–Jasper–Speegle; canonical-tight, canonical-Parseval, canonical-orthonormalization and symmetric-orthogonalization phrases; Haar perturbation/Riesz-wavelet phrases; canonical-dual literature; and primary author/publisher pages. It located and inspected the classical formula rather than relying on absence of search hits. Canonical filters, Gabor windows, discrete transforms, quasi-affine systems, and unrelated tight-wavelet constructions were not treated as answers. This is not an exhaustive bibliography.

Only authored analysis and public bibliographic/verification metadata belong to this packet. No third-party source text, PDFs, dataset contents, or private coordination material is included.
