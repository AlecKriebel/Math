# Exact source and access audit: 30001080 / OWR-2093-003

Checked 2026-10-01. The imported wording is an open converse about mass-preserving transport kernels. “Invariant random measure” means covariance with the underlying flow; it must not be replaced by assuming its candidate law is stationary.

## Full original report

Last, joint work with Thorisson, *Bernoulli and Cox transports of stationary random measures*, in OWR47/2008, *New Perspectives in Stochastic Geometry*, printed pp.2673–2674, DOI 10.4171/OWR/2008/47. The full contribution was read and p.2673 visually checked. The report is volume5 (2008), while the publisher records publication on September30,2009.

- [Publisher report](https://ems.press/content/serial-article-files/46189)
- [Institutional full reading copy](https://oa.tib.eu/renate/server/api/core/bitstreams/a7d01308-3e21-427a-90c8-65e2f5a1c8f1/content)

The talk introduces a locally compact Abelian group, a random measure ξ, and a possible accompanying random element X. It distinguishes mass-stationarity, preserving allocations, Bernoulli randomization and the Cox process ζ with intensity ξ. The inserted process is ζ⁰=ζ+δ₀. It explicitly discusses the joint pair (ξ,ζ⁰) before posing the converse for the **distribution of ξ** under kernels obtained by applying allocations to this Cox process.

Accordingly the candidate treats two formulations separately: the general abstract ξ-only Markov test theorem, and an explicit Cox-derived matching characterization for the canonical law of ξ. The latter matching uses ξ as background to the Cox process, exactly as specified in its theorem statement. Independent source review must verify that scope; no claim is made for a different rule that forbids observing the original measure.

## Full foundational paper

Last–Thorisson, *Invariant transports of stationary random measures and mass-stationarity*, Annals of Probability37(2) (2009),790–813, DOI10.1214/08-AOP420. [Complete arXiv electronic reprint](https://arxiv.org/pdf/0906.2062v1). Accessed mathematical sections: Section2's flow/Radon/Palm conventions and (2.7); Section3's Markov versus weighted kernel definitions and covariance/balance formulas; Theorem4.1; Definition6.1 and Theorem6.3; all of Section7's discussion and Problems7.3–7.7. Problem7.3 was visually checked on reprint PDFp.23. Numbering refers to the accessed reprint, rather than inventing final journal page locators.

The source explicitly assumes Q(ξ(G)=0)=0 in its question setting. It allows σ-finite Q on an abstract measurable flow. A transport-kernel is Markovian; a weighted transport-kernel need not be. Problem7.3 restricts kernels to σ(ξ)⊗G measurability while testing invariance of the full Q. These details motivate Turn2's argument without disintegration or a countably generated auxiliary state space. Mecke's established identity (2.7) and the Palm/mass-stationarity equivalence are credited inputs.

An older [2007 full preprint](https://publikationen.bibliothek.kit.edu/1000010936/1010653) was also read for continuity. Its question is numbered8.3 and its terminology is “quasi-transport.” It is not used to overwrite the later version's numbering.

## Later characterization results

Last–Thorisson, *Construction and characterization of stationary and mass-stationary random measures on R^d*, SPA125 (2015),4473–4488, DOI10.1016/j.spa.2015.07.006. [Complete arXiv v2](https://arxiv.org/pdf/1405.7566v2), stamped17July2015 with a printed April24,2019 header in the retrieved bytes. No inference about a new theorem or revision date is made from that header. Definitions, Theorems1/6/7/8 and final Section9 were read. [Publisher HTML](https://www.sciencedirect.com/science/article/pii/S0304414915001635) also exposes the final discussion. Its kernels in the concluding characterization are not Markovian, and it explicitly says Problem7.3 remains open. This published result is not passed off as the candidate's converse.

Last–Thorisson, *Characterization of mass-stationarity by Bernoulli and Cox transports*, Communications on Stochastic Analysis5(2) (2011),251–269, DOI10.31390/cosa.5.2.01. [Verified publisher metadata](https://repository.lsu.edu/cosa/vol5/iss2/1/), [KIT catalogue](https://publikationen.bibliothek.kit.edu/1000185535). **Full-text access limitation:** the old author PDF link now redirects to an author homepage. The publisher PDF URL returns403 to direct readers and remained in a Cloudflare security-verification loop in the cloud browser after one ordinary reload. No CAPTCHA was attempted, no access bypass was used, and no full final PDF is claimed read. Indexed snippets suggest the joint background is permitted, but those snippets are not used as a substitute for a complete theorem. Turn2 defines and proves its Cox matching directly against the full original OWR description.

## Metric input and classical tools

Struble, *Metrics in locally compact groups*, Compositio Mathematica28(3) (1974),217–222. [Full primary PDF](https://www.numdam.org/item/CM_1974__28_3_217_0.pdf). The p.217 theorem gives a compatible proper left-invariant metric on every locally compact second countable group; in the Abelian case it is translation-invariant. This is the metric input for compact Cox exclusion balls. We use standard Haar uniqueness on closed subgroups; no measurable family of Haar normalizations is selected. The exact Poisson Campbell–Mecke identity needed for the matching density is derived by its finite Poisson series and compact exhaustion in Turn2's appendix.

## Prior-attempt and source pin

Pin: ulamai/UnsolvedMath revision37e53eabe540fb458758e198be61634bd02ee008. The entire imported statement/background and empty upstream report were read.

- Statement SHA256:37dd11304ad5e150719b65bac9ae7d830125e4e5ca2012804ed9167d67a474c3.
- Sorted JSON [record,report] SHA256:5de82ef1b20a615ee3eed3e1ffe640f84c5ac47704f5f66dcf1ed492f744cb03.
- All-state target/source/mass-stationarity PR searches in AlecKriebel/Math returned no attempt; branch and both possible target commit-path searches were empty.
- Local all-ref history and related-target groups contained no attempt; target row was queued0/5.
- Current exact-phrase and later-literature searches found no verified later solution of the Markov converse. This is not a comprehensive novelty certification.

Reading copies, extracts, screenshots and full imported records are excluded from publication. No external outreach occurred. Two substantive author turns are recorded; source retrieval is not an extra turn.
