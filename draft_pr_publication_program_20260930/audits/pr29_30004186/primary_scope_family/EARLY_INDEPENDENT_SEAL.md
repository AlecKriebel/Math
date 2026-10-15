# Early independent primary-source seal

Sealed UTC: 2026-10-01T23:30:44.601300+00:00
Audit goal completion estimate: 25% (source reconstruction done; candidate/provenance comparison outstanding).

Before sealing I read root AGENTS.md and the PDF skill, independently fetched primary sources, read the literal OWR contribution at printed pages 1940-1942 and inspected its three rendered pages. I have not read candidate files, old original-stage review, code, receipts, or sibling-family results. Original candidate head supplied by parent: 5ac4a57e08dd72a6f16768f2288b9c0349999431; target ID 30004186 / OWR17128-002; claimed candidate SHA256 95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c. These are identification claims pending independent verification.

## Original question reconstructed

[OWR original](https://ems.press/content/serial-article-files/46811), contribution of Anna Geyer (joint work with Dmitry Pelinovsky), pp. 1940-1942, report DOI 10.4171/OWR/2019/32. It treats the quadratic reduced Ostrovsky equation u_t+u u_x=partial_x^(-1)u for periodic zero-mean data. The peak is U_*(z)=(3z^2-pi^2)/18 on [-pi,pi], periodically extended, with speed c_*=pi^2/9. U_* lies in H^s for s<3/2 and is Lipschitz, with a derivative jump at identified endpoints. Nonlinear instability is left open after linear and spectral instability. The stated obstacles are an evolution theory at peak regularity and the mismatch between the weighted L2 generator domain (allowing finite perturbation jumps at the peak) and H1 (continuous perturbations). The final open sentence does not prescribe an instability norm or demand a particular global weak solution concept. Therefore a truthful scoped partial result may be accepted without claiming full resolution; it is not legitimate to invent a stronger fixed H1/L2 target and attribute that definition to OWR.

[EMS metadata](https://ems.press/journals/owr/articles/17128) labels the report 2019, submitted July 14, 2019, and published September 10, 2020. Workshop date and publication date are distinct.

## Published and preprint status

[SIAM 2019 author offprint](https://pelinovsky.mcmaster.ca/PaperBank/PeakedWaveOstrov.pdf), DOI 10.1137/18M117978X: theorem 1 is uniqueness and linear instability, with X1={v in mean-zero L2: (c_*-U_*)v in H1}. Its discussion does not transfer that linear result to nonlinear instability. [Proc. AMS 2020 offprint](https://pelinovsky.mcmaster.ca/PaperBank/PeakedSpectralUnstable.pdf), DOI 10.1090/proc/14937: spectral instability for quadratic and cubic reduced Ostrovsky equations; its introduction again leaves nonlinear instability open.

[arXiv:1804.03788v1](https://arxiv.org/abs/1804.03788v1) has a nonlinear section: definition 4 uses H1 orbital distance to all translates and includes unique global H1 evolution; lemma 10 asserts a smoother perturbation v, local lifetime order delta^(-1), and fixed L2 escape. Its proof uses modulation, the semigroup lower bound, momentum conservation, and a contradiction assuming H1 perturbation size B delta. I read the full actual section, including lemmas 9-10 and remarks 16-18, rather than infer theorem scope from its title. [v2](https://arxiv.org/abs/1804.03788v2) and the published paper remove this nonlinear section/claim. The public version history is a revision, not a formal withdrawal. No inference about authors' motives is justified. Freshly served v1 PDF contains a December 2024 typesetting date, so the 2018 submission date is anchored to arXiv version metadata, not that typesetting date.

## Distinct 2025 model

[Natali-Pelinovsky-Wang arXiv:2503.15071v1](https://arxiv.org/abs/2503.15071) studies 2c eta_tx=(c^2-2 eta)eta_xx-(eta_x)^2+eta, equivalently (2c eta_t-c^2 eta_x+2 eta eta_x)_x=eta+(eta_x)^2. Its mean constraint is integral[eta+(eta_x)^2]=0, unlike zero mean u. It explicitly compares the reduced Ostrovsky equation (v_t+v v_x)_x=v. Theorem 1 is local H1 intersect W1,infinity evolution. Theorem 4 gives, for every delta>0, data with H1 size <=delta^2 and W1,infinity size <=delta, then fixed W1,infinity escape (=1) before maximal local lifetime, from a one-sided peak gradient characteristic inequality. It supplies no H1 escape result. Removing the squared-gradient term would change the model and cannot serve as an exact-equation provenance claim.

## Precommitted falsification criteria

1. Identify equation, peak, mean constraint and periodic topology exactly; reject a different-model theorem as a solution of the target.
2. State solution class, existence/continuation assumptions, phase/orbit convention, initial norm, quantifiers and escape norm. A bounded pointwise derivative or gradient escape alone does not imply L2/H1 orbital escape; phase treatment must be checked.
3. Treat linear/spectral calculations and bounded numeric experiments as partial support, never as the nonlinear evolution theorem.
4. If a same-equation W1,infinity characteristic result is claimed, independently read its existence bridge, one-sided traces, continuation, and fixed-escape quantifier; a truthful partial result is admissible without global weak/H1 resolution.
5. Authenticate exact original-head files, raw pinned dataset and related-group/readiness context independently. Legacy code replays cannot authenticate historical model, query, or prior-absence assertions.
6. A bounded later-literature search records what was checked and cannot certify worldwide absence or novelty.
