# Independent adversarial check of #273 communication consequences

Checkpoint 2026-10-06 Pacific; triage confidence/audit completion 90%. This checks implication scope and obvious counterexamples, not the release EPnI proof.

## 1. Wilde–Hayden–Guha dynamic capacity: passes restricted scope

Recommended target remains the quantum dynamic C,Q,E region and the public/private/key region of the **pure-loss channel with eta >= 1/2**, with finite mean input photon number and the established net resource accounting. Vacuum-port #273 gives exactly S(E_eta^tensor-n(rho)) >= n g(eta g^-1(S(rho)/n)), for arbitrary finite-energy n-mode states. This is the multimode constrained output entropy premise; it is stronger than the single-mode theorem proved earlier. The finite-energy restriction is appropriate for energy-constrained block-code inputs, but mixtures/conditioning and finite-dimensional truncation must be recorded.

Primary existing conditional theorem: https://arxiv.org/html/1105.0119 ; https://journals.aps.org/pra/abstract/10.1103/PhysRevA.86.062306 . Independent later statement: Wilde quantum information notes, Theorem 25.5.4, https://www.markwilde.com/qit-notes.pdf . The first bound is C+2Q <= g(lambda N)+g(eta N)-g((1-eta)lambda N); some search/OCR snippets incorrectly duplicate eta N, so use the original equation or textbook.

Novelty exclusions: quantum-limited **amplifier** dynamic/broadcast capacities were already solved in Qi–Wilde PRA95 012339 (2017): https://journals.aps.org/pra/abstract/10.1103/PhysRevA.95.012339 . Ordinary single-resource pure-loss quantum/private capacities already unconditional. General thermal-noise quantum capacity does not follow. The original #273 paper expressly excludes dynamic/wiretap/quantum claims at /Users/alec/Desktop/math/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/06-broadcast.tex:301 .

## 2. Pereg–Ferrara–Bloch confidential broadcast: restrict eta >= 1/2

For eta >= 1/2, Theorem6's entropy premise exactly matches #273's vacuum specialization, so the research path looks strong. Primary source https://arxiv.org/html/2105.04033 , Conjecture1 and Theorem6, SectionIII-C. Fixed preshared key rate R_K >=0 and strong mutual-information secrecy are allowed. For beta in [0,1], target bounds are R0 <= g((1-eta)N)-g((1-eta)beta N), R1 <= min{g(eta beta N),g(eta beta N)-g((1-eta)beta N)+R_K}.

**Actual boundary counterexample to copying the published eta<1/2 formula:** their displayed Theorem6 lower-transmissivity branch still has R0 <= g((1-eta)N)-g((1-eta)beta N). Set eta=0,beta=0,N>0. It permits R0=g(N)>0 and R1=0, while Bob receives vacuum and cannot decode the common message. SectionII-C Remark2 explicitly says the common message is decoded by both Bob and Eve. Thus this branch cannot be cited blindly. Their own thermal inner-bound equation (34) uses eta in that R0 bound and has the correct vacuum limit, suggesting a transcription error in Theorem6. The weak-Bob regime is best excluded from the initial announcement; it may be repaired separately and probably needs no EPnI.

**Operational-scope caveat:** SectionII-C line173 says the bosonic encoder uses a coherent-state protocol and imposes a per-codeword energy constraint. Theorem6's converse then starts with arbitrary input density operators at lines352–354. An announcement about arbitrary entangled codewords should explicitly verify this converse extension and match average-versus-per-codeword constraints, instead of claiming it is verbatim the operational theorem. This is likely a manageable audit, not a new central entropy obstacle. Their security criterion is strong secrecy (mutual information leakage tends to zero), explicitly weaker than semantic security; do not silently upgrade it.

**Excluded three-receiver overreach:** Theorem10 only supplies a displayed inner-bound inclusion despite the prose saying it determines a region. #273 does not automatically provide the absent matching converse.

## 3. Fresh literature boundaries

A search surfaced Pirandola arXiv:2610.06832 (dated 2026-10-05), claiming exact finite-energy two-way pure-loss capacities; this is a different assistance model and not duplication of the dynamic one-way tradeoff. It reinforces excluding two-way capacities as a proposed easy novel target. No independently verified recent unconditional result for the above one-way dynamic/confidential regions was found in this quick check. Priority cannot be guaranteed from the scan.
