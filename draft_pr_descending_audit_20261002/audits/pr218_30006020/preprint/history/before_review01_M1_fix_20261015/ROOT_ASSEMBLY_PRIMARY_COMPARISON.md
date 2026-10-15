# Root direct verification of classical probability and announcement coverage

Evidence cutoff: 2026-10-15 UTC. This supplements, and does not reseal, the earlier root-priority report. The exact submitted candidate remains frozen at SHA-256 f1d43a7f4ae54e6c3ac8318cac8f2106b937d4657101bdd3a9b91523e0e5de4b.

## Positive older probability coverage

The root independently downloaded the full final Arratia–Barbour–Tavaré (2000) and Arratia–Tavaré (1994) papers. Their hashes match the independent assembly family's copies; ASSEMBLY_PRIMARY_RETRIEVAL.json records the actual bytes. A cleaner author-uploaded facsimile of AT1994 was also downloaded. The root read ABT's conditioning relation, uniform logarithmic condition, Theorem 3.1 and its proof, and the supporting estimates; it read AT's Lemma 5, equation (126), and complete proof. It actually inspected rendered ABT printed p.1630 and AT equation (126).

Put a_j=ζ(2j)/(2j), and let Z_j be independent Poisson variables of means a_j. The candidate's component counts are exactly their law conditioned on ΣjZ_j=n. This is the old DGZZ weighted permutation law, equations (1.7)–(1.8) and Lemma 3.6, not a newly defined probabilistic model in a priority sense.

ABT's parameter is θ=1/2. If A=ζ(2)/2, then j E Z_j=ζ(2j)/2→1/2; j P(Z_j=1)=1/2+O(1/j); and, for ℓ≥2, j P(Z_j=ℓ)≤A^ℓ/(ℓ! j). The ULC follows with e(j)=C/j and factorially summable constants c_ℓ. ABT Theorem 3.1 therefore covers the complete vector of counts with j≤b_n for every b_n=o(n) in total variation. For a compact q_n-scale window with q_n→∞, q_n=o(n), choose b_n a fixed multiple of q_n. The corresponding independent Poisson mean tends to (1/2)log(b/a), and disjoint windows are independent. Thus the candidate's unmarked all-rate mesoscopic Poisson conclusion is an older-theorem corollary, including arbitrarily slowly diverging q_n.

AT's factorial identity specializes to

E ∏_j(C_j)_{r_j} = (h_{n−Σjr_j}/h_n) ∏_j a_j^{r_j}.

In its assembly notation take m_j/j!=a_j, tilt x=1, and p(n)=n!h_n. Positive real weights are justified by the proof's conditional-Poisson algebra, without claiming the existence of an integer-sized combinatorial class with these m_j. Direct deletion of selected components gives the same identity. A self-contained proof is useful but does not remove the earlier attribution.

The root also read NSZ2013 Theorem 3.3, its full hypothesis (3.7), and the adjoining application statements. Its growing-set coefficient estimate assumes C log n−n/d_n→−∞ for every fixed C. It covers q_n of order √n, but not every q_n=o(n); for example d_n=n/√log n fails that hypothesis. ABT supplies the genuinely unrestricted unmarked range. Neither paper alone states the same geometric cylinder-area theorem.

## Marking and normalization: deduction, not a located earlier theorem

Independent Gamma(2j,1) marks on independent Poisson components form a Poisson point process with intensity

ρ(y)=e^(−y)/y Σ_{j≥1} ζ(2j)y^(2j)/(2j)! = e^(−y)/y Σ_{m≥1}(cosh(y/m)−1).

The m=1 term is 1/(2y)+O(e^(−y)/y); for m≥2 use cosh t−1≤(t²/2)e^t and Σm^(−2)<∞, giving O(y e^(−y/2)). Hence 2qρ(2qx)→1/(2x) locally uniformly away from zero as q→∞. Combining ABT with b_n=⌊√(nq_n)⌋, a common marking kernel, Gamma lower-tail bounds for j>b_n, AT's identity for moments, and concentration of the Gamma(2n,1) total gives a short route to the analytic marked conclusion. This paragraph is a checked auditor deduction, not a claim that an older source contains the marked or geometric theorem. The submitted elementary proof is separately accepted.

## Prior microscopic announcements and current public leads

The root read Liu's 2022 thesis Remark 1.5.9, printed p.22, and actually inspected its rendered full page. It explicitly describes work in progress with Delecroix, gives the all-multiplicity intensity ρ, and states fixed intervals [a/(6g−6),b/(6g−6)]. It also gives the generalized Ewens weights. The root inspected Durham 2025 slides 26 and 195: slide 26 specifies primitive multigeodesics, and slide 195 labels the fixed microscopic law a conjecture with the different primitive density e^(−x)(cosh x−1)/x and its 1/(2x) tail. These are credited prior announcements. The root does not claim that either public passage proves growing-window uniformity.

The exact DL Gamma total is 6g−6, consistent with the thesis. OWR's separate microscopic summary prints 4g−4. Those two fixed microscopic normalizations are not identified or repaired here. No new microscopic theorem is proposed; the mesoscopic result uses neither the literal OWR formula nor an interchange of endpoint limits.

The newly observed IPAM talk lead was resolved through the actual official publisher video description (https://www.youtube.com/watch?v=lvALmZQfmjs) and its MathInstitutes entry (https://mathinstitutes.org/videos/24204). The 26 January 2026 talk concerns short geodesics on random hyperbolic surfaces and random metric maps, joint with Barazer and Giacchetto. This identifies its public abstract with an adjacent ensemble already compared; the video itself was not watched, and no inference about every claim in its contents is made. The September 2026 Rennes CV talk could not be resolved to a same-target primary statement. Raw follow-up searches and descriptions remain private.

## Root decision

No inspected primary passage positively covers the same geometric moving-window theorem. The unavailable announced Small components manuscript remains a specific priority uncertainty. Negative searches do not certify novelty, but possible private overlap is not proof of earlier coverage. Together with the fresh final adversarial synthesis, this supports preparing an explicitly credited consequence note answering the written OWR intermediate-area question. It does not certify universal first priority or authorize release of the undercredited frozen candidate. Exact DGZZ/ABT/AT credit, announcement credit, precise ensemble and limit order, the microscopic reservation, extensive AI disclosure and unrefereed status are mandatory globally. Fresh sequential adversarial manuscript reviews remain required before publication.
