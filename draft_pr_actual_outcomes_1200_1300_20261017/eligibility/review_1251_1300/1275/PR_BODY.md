## Accepted source-scoped result

This is an AI-assisted audit of Boon Suan Ho's existing Theorem 1.6 in [arXiv:2604.18535v2](https://arxiv.org/abs/2604.18535v2), *Counterexamples for lacunary dilates via dyadic spike blocks* (21 April 2026). The counterexample is credited to Ho. No new disproof, novelty, journal acceptance or refereeing is claimed.

For each fixed finite real p >= 2, the accepted construction provides a real mean-zero f in L^p(T) and one deterministic sparse dyadic sequence n_j = 2^{m_j}, with successive ratios at least 2. On one full-measure set, the limsup of the partial sum divided by N (log N)^{1/p - epsilon} is positive infinity for every epsilon > 0. The function and sequence may depend on p, but not on x or the later choice of epsilon. N counts the selected samples.

At p = 2 this gives the negative answer to the proposed modern universal o(N sqrt(log log N)) bound in Erdős 995.

## Attribution and precise boundaries

The original [Erdős 1964 paper](https://users.renyi.hu/~p_erdos/1964-24.pdf) displays lower examples at N (log log N)^{1/2 - epsilon} and a general upper scale N (log N)^{1/2 + epsilon}. The exact modern little-o wording is not literally displayed on the inspected original page. The audit preserves this distinction.

No epsilon-free endpoint, optimal secondary logarithm, consecutive-dyadic statement, or bounded-exponent-gap result is claimed. The audit does not independently accept the Fourier-tail theorems, Erdős 996 consequences, or other sections outside Theorem 1.6's stated dependency chain.

This audit has had no external human review and no formal proof certification. “Acceptance” records the scoped mathematical assessment. The 11 October 2026 abstract-page inspection found no journal-reference field; it does not establish the absence of later publication.

## Complete audit and verification record

The complete authored AUDIT.md is preserved byte-for-byte. The proof covers the real-p binomial moment estimate, geometric Lp budget and Minkowski argument, deterministic lower floors, binary-digit independence, trial amplification, recursive stage counts, shielding of other blocks, and the common full-measure set.

The recorded finite regressions cover 976 convolution cases, 36 block-parameter cases and 18 stage-recursion cases, with identical normal/-O/-OO outputs. These are supporting checks, not the theorem proof. The publication step did not rerun the mathematical test programs; the recorded preparation receipt reports reproduction of the finite checks. No source-author code was executed. Historical assessment fields retain their audit-stage meaning.

Exactly five files, totaling 37,886 bytes, are added under unsolved_math_prioritization/attempts/2430. They contain authored exposition and public verification metadata. Source PDFs, extracted source text or images, datasets, raw numerical tables, executable scripts and private coordination material are excluded. QUEUE.md and every unrelated tree remain unchanged.

## Exact public-file identities

- ACCEPTANCE.json: 4,808 bytes; SHA-256 62b3f21a235573c10470bf666206504671c0a60202dd0b3527ceaf440be22e17.
- ARTIFACT_MANIFEST.json: 1,572 bytes; SHA-256 9d036ca1335607bfad4a30e55493cba4e3c47c26209a427a8fd4f777605db8eb.
- AUDIT.md: 23,862 bytes; SHA-256 d1918afe66643d0fe05faf85a18286884c4f4d5c3aeb38f7fef302ccab7107c9.
- README.md: 3,277 bytes; SHA-256 b4254293bda625eda5155a4cb2a872a9d6e9b5b4d96f3437de3c5ca4324c6704.
- SOURCES.json: 4,367 bytes; SHA-256 47c21db715eff1a3765add998173f1e6108afa7a2924f6d27fa89abe9dbedf8f.

ARTIFACT_MANIFEST.json lists all five members and hashes the other four. Its own digest is independently pinned above. Local integrity/preservation validation passed in normal, -O and -OO modes; remote blob contents were read back and matched exact UTF-8 bytes, byte counts, SHA-256 and Git blob IDs.

The ten existing workflow definitions are path-filtered to unrelated projects. Exact-head CI is checked separately; zero registered jobs is NOT_RUN, not a pass. Draft only; no merge, release or outreach.
