# Erdős Problem 783: coprime sieving under a reciprocal budget

Target: 2302 / EP-783. Disposition: mixed, with accepted prior asymptotic value, corrected restricted stability, a finite exact counterexample, and an unaccepted general-rigidity proof.

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete substantive ten-section audit and the full authored finite counterexample are retained, including every mathematical set, fraction, inequality, count, correction, dependency and limitation. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks concern one finite witness only; they do not establish an eventual optimizer or the general harmonic-rigidity claim.

## Exact mathematical dispositions

For fixed C>0, minimize the unsieved proportion over pairwise coprime A⊆{2,…,N} satisfying Σ(a∈A)1/a≤C. The sharp leading value is ρ(e^C)+o(1), where ρ is the Dickman function. The general-modulus lower bound is prior work of Terence Tao, using the classical prime-modulus result; a correctly budgeted descending-prime tail supplies the matching upper bound. The complete written reconstruction and all local normalization, truncation and indexing repairs are in AUDIT.md.

- The sharp fixed-C asymptotic value is accepted with the listed repairs and explicit classical dependencies. The union-bound range C≤log 2 and the endpoint are retained.
- Fixed-power-cutoff prime stability is accepted after the small-prime hypothesis and factor-2 corrections. Its compactness parameter u is fixed, with u≥w>2.
- For near-minimizers with C>log 2 and w=e^C, composite reciprocal mass is o(1), recovered by the corrected two-parameter argument. Tightness near logarithmic scale zero does not supply one fixed cutoff with o(1) loss.
- General prime-tail harmonic rigidity is unaccepted from the inspected February 25 proof. Fixed cutoff errors are not shown to vanish, and diagonal cutoffs can make u grow beyond the fixed-u stability theorem. No counterexample to the general theorem, no disproof, and no global-openness certification is claimed.
- The literal all-N exact greedy rule is false: at N=100 and C=1/2, the descending-prime greedy set leaves 62 integers while an admissible prime set leaves 57. PROOF.md retains both full prime sets, every exact reciprocal fraction and signed budget comparison, and the full overlap-free counting argument.
- This one finite witness does not refute a fixed-C eventual exact rule, assert global optimality of the replacement set, or classify exact optimizers. The eventual exact problem and complete classification remain unresolved by this audit.

## Reading order and evidence

1. AUDIT.md preserves the complete ten-section mathematical audit, including the strictness mechanism, fixed-u compactness/equality argument, both Corollary 35 counterexamples, repaired power estimate, composite-mass argument, precise cutoff/uniformity gap and cardinality limitation.
2. PROOF.md is the complete authored finite exact counterexample.
3. ACCEPTANCE.md and ACCEPTANCE.json state the separate accepted and unaccepted claims and bind the two distributed authored documents.
4. SOURCES.json preserves historical PDF/text identities, all inspected page lists, public retrieval history and access limitations. The complete January, February, Tao and Granville–Soundararajan texts were read; only the target page of the 1973 paper was audited.
5. VERIFICATION.json records the single finite witness's historical normal/-O/-OO execution agreement and byte identities without distributing raw outputs or code. MANIFEST.json lists exactly eight files and hashes the other seven; its digest is separately pinned in the publication description.

The primary dependencies include the classical prime-modulus value/equality theory, prime number theorem, Mertens theorem, Dickman asymptotics and Dickman log-concavity. Hildebrand's original long paper and the full dependency closure were not independently re-audited. Granville–Soundararajan's cited machinery and numerical inequalities remain classical inputs; their numerical checks were not rerun as interval certificates. The Dickman continuation calculation checks the mechanism, rather than certifying all Dickman theory independently.

## Attribution and public sources

- Paul Erdős, Problems and results on combinatorial number theory (1973), printed page 135: https://users.renyi.hu/~p_erdos/1973-21.pdf
- Terence Tao, Sieving by coprime numbers, February 22, 2026, third version: https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf
- Chojecki, Extremal coprime coverings under a reciprocal budget and a Dickman-type conjecture, January 23, 2026: https://www.ulam.ai/research/erdos783-final.pdf
- Chojecki, Erdős Problem #783: sharp asymptotic value and a stability program, February 25, 2026: https://www.ulam.ai/research/erdos783-rem.pdf
- Granville and Soundararajan, The number of unsieved integers up to x, arXiv:math/0308009v1 (2003), Acta Arithmetica 115 (2004), 305–328: https://arxiv.org/abs/math/0308009
- Public discussion: https://www.erdosproblems.com/forum/thread/783

The February note explicitly claims the additional general stability theorem; it is not treated as merely a conditional program. Tao's dated February 23 statement that he did not plan journal publication is preserved only as historical intent. Direct forum access failed during the bounded source check, so search-indexed discussion supplied that attributed statement. No exhaustive later-literature, present publication-status or consensus claim is made.
