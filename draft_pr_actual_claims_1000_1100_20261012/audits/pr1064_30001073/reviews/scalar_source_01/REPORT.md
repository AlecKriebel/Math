# Independent adversarial report: PR 1064 / problem 30001073

## Verdict

PASS for the submitted analytic theorem at head `bdefe31b9d226c8f27008d13f57775d5de8df3d7`. No mathematical correction is required within this review family's scope. The exact asymptotic question in official OWR 44/2008, problem 9, is answered by the submitted upper bound together with the source's known van der Waerden lower bound. The stronger row-stochastic upper bound is valid. This verdict certifies neither novelty/priority nor present worldwide open status, an optimal exponent, external human review, or formal proof-assistant verification.

Severity findings: **P0 none; P1 none; P2 none; P3 none.** The limitations below are evidence boundaries, not submitted defects.

## Scope, independence, and custody

This family independently attacked the scalar variational absorption and input-Frobenius conversion, and checked the full entropy interface rather than importing it under an acceptance label. The submitted PROOF was read before the other eight result files. Its opening status language was not evidence. A full analytic derivation and source applicability analysis were frozen in `FROZEN_INDEPENDENT_DERIVATION.md` at the timestamp and SHA-256 in `INDEPENDENCE_FREEZE.json`, before reading older acceptance/audit/source/status/provenance documents. The later consistency receipt lists all eight subsequent reads.

The submitted target tree is `ba39666fe79a2b127672cac03e02867713e6cd76`. All nine Git blobs were obtained directly from the specified commit and matched the root captured submitted copies. `INPUT_CUSTODY.json` records each blob OID, SHA-256, byte count and mode. The full Git tree, submitted commit object, and target tree object/list were preserved independently in this review directory. `SUBMITTED_PINS.captured.json` captures the root pin record. `PRESERVATION_CHECKS.json` verifies all original root/review/Git bytes and the frozen independent derivation still match.

No branch/index/service/PR/publication operation, external contact, original-file repair, sibling review consumption, or further subagent delegation occurred. Initial discovery printed unrelated filenames, not sibling review content; this is disclosed in custody. This review writes only within its assigned directory. Root records and submitted originals remain intact.

## Mathematical result and exact assumptions

For every positive integer n and nonnegative row-stochastic n-by-n A, S=sum a_ij^2, the proof establishes

    per(A) <= exp(-n + exp(4) sum a_ij^2 log(e/a_ij))
           <= exp(-n + exp(4) S(1+log n)).

Zero summands have their continuous values. The proof disposes of per(A)=0 before defining its Gibbs law. For per(A)>0, the Gibbs marginal B is doubly stochastic and b_ij>0 forces a_ij>0. Row stochasticity, not column stochasticity of A, supplies entry bounds [0,1] and total mass n.

The scalar inequality holds for all a,b in [0,1], with a=0 allowed only at b=0:

    g(b)-d(b,a) <= exp(4) a^2 log(e/a),
    g(b)=-b^2 log b/(1-b), g(0)=0, g(1)=1,
    d(b,a)=b log(b/a)-b+a.

I verified both comparisons g(b)<=b and g(b)<=h(b)=b^2 log(e/b), h's increasing derivative on [0,1], and the split b>=exp(2)a versus b<exp(2)a. The latter is correctly split again at b<=a; it does not wrongly evaluate increasing h beyond 1. The divergence is kept until the input-entry absorption step, so concentrated Gibbs marginals cause no unsupported substitution of Frobenius control from A to B. Every zero/unit limit is valid. The full proof is preserved in the frozen derivation.

The entropy interface was independently expanded using conditional KL against the marginal row restricted to available columns. Only positive-probability histories are consumed, on which its reference normalizer is positive. Priorities remain independent when conditioning on a full supported permutation and a row priority. Log Jensen is in the upper-bound direction; its integral is -1-b log b/(1-b). Weighting by the sampled marginal contributes the second factor b in g. The exact Gibbs entropy identity and sum(-b+a)=0 then justify summing nonnegative scalar d over all entries, including d(0,a)=a. The deterministic-permutation entropy case has equality and verifies g(1)=1.

Cauchy-Schwarz gives S>=1. The probability weights p_ij=a_ij^2/S obey H(p)<=2log n, and the exact identity

    sum a_ij^2 log(1/a_ij)=(S/2)(H(p)-log S)

gives the required entry sum <=S log n. This step and the log S sign were checked directly; zero terms are harmless. Under S<=gamma, the all-n bound is exp(exp(4)gamma)n^(exp(4)gamma)exp(-n). The pure-power n^(3exp(4)gamma)exp(-n) is asserted only for n>=2. At n=1 the prefactor-free form is false, and all submitted summaries correctly retain that caveat.

The block family with fixed integer k and n=km has S=k and permanent (m!/m^m)^k, asymptotic to (2pi/k)^(k/2)n^(k/2)exp(-n). This proves polynomial loss is necessary at gamma=k; it does not make the displayed exponent sharp.

## Fresh primary-source verification and boundary

Three complete primary PDFs were freshly retrieved during this review, not reused from an older audit. `SOURCE_FETCH_RECEIPT.json` records URLs, effective URLs, UTC retrieval times, HTTP metadata, full PDF hashes/bytes, and extracted-text hashes. The exact original and required prior pages were read as full pages and rendered to images for formula inspection. All third-party PDFs, text and renders are private under ignored `sources/raw/`; only authored receipts, locators and analysis belong to this review's deliverables.

[Official EMS report](https://ems.press/content/serial-article-files/46191), printed pp. 2549-2550, PDF pp. 73-74, fixes gamma>=1 and bounds the **unnormalized** sum of squares. Its preceding lower bound is known van der Waerden; its following entrywise gamma/n hypothesis is expressly stronger. The submitted row-stochastic upper theorem thus covers the stated doubly stochastic Frobenius class. For a concrete distinction, (1-t)J_n/n+tI_n with t^2=(gamma-1)/(n-1) has S=gamma and diagonal entries of order n^(-1/2), eventually exceeding gamma/n for fixed gamma>1.

[Anari-Rezaei v2](https://arxiv.org/pdf/1811.02933v2), §1.4 pp. 5-6 and full §4 pp. 10-13, including the complete calculation through Eq. (6) p. 12, confirms the credited Gibbs-marginal/random-order comparison. Conditional Jensen supplies the submitted scalar correction. Its later sharp row-maximization theorem and computer certificate are not needed for this argument. For sparse matrices, defining a greedy sampler on all possible greedy histories needs an extra failure state or equivalent convention; the submitted conditional proof avoids that support issue entirely.

[Anari v2](https://arxiv.org/pdf/2608.28031v2), §4 Lemma 7 pp. 9-10 and its full proof, keeps the same sequential KL comparison exactly for positive A. Its vector g differs from the submitted scalar g. This identity supports the mechanism but proves neither the input-Frobenius absorption nor novelty. Fresh complete-text literal Frobenius searches found three numerical optimization contexts on pp. 29-31 and none in the older paper; locators are recorded. Absence from those bounded checks is not absence of the theorem or its consequences from the literature.

Fresh PDF identities match the corresponding current submitted bibliographic hashes: EMS `3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35` (731001 bytes), Anari-Rezaei `c6d22620c7963ead242068941ef05562c8c72c40accea40cd3304705d546b405` (248293 bytes), Anari `e166fb3d448e33307396df4eb6d00bef8b804c6387d8aba56c959ea7ff942927` (349123 bytes). The PDF title pages identify the versioned arXiv releases. The submitted record's previous source inspections, failed downloads, edition preparation history, Gurvits-Samorodnitsky read, and Radhakrishnan provenance are historical assertions; this review does not claim to replay them or import any uninspected theorem from them.

## Fresh adversarial diagnostics

`check_fresh.py` and `FRESH_CHECKS.json` are newly authored and executed controls, not the omitted historical diagnostic code. The proof remains analytic. Exact rational inputs are used for permanents, marginal probabilities, support and S; Python Decimal supplies 224/384/256-digit transcendental diagnostics, not interval certification.

The scalar sweep checks 2484 pairs at each of 224 and 384 digits, with a as small as 10^-1000, b within 10^-120 of one, exact zero/one endpoints, both sides of exp(2)a at 10^-100 relative distance, and all three nonzero branches. The sampled maximum (g-d)/h(a) is approximately 2.50506 at (a,b)=(0.275,1), far below exp(4); this is a sample maximum, not a global optimization result.

Six arbitrary permutation laws verify the complete conditional-chain interface across positive histories, including deterministic n=1, uniform n=2 through n=5, and a sparse two-matching law. Six exact-rational matrices cover n=1, row-stochastic but non-column-stochastic inputs, sparse greedy traps, non-matching positive entries, irregular doubly stochastic inputs, and zero permanents. Controls check Gibbs identities, total-mass KL cancellation and Frobenius entropy conversion. Twenty block parameter pairs check the required exponent's stated n>=2 range, with n=1 explicitly skipped there.

Five deliberate faulty variants are detected: omission of scalar divergence; extending the pure-power bound to n=1; setting g(1)=0; claiming every sparse greedy marginal history has positive remaining reference mass; and replacing Frobenius control by entrywise gamma/n control. The sparse trap is a source-interface stress test, not a counterexample to the submitted conditional proof.

## Nine-file consistency and remaining limits

All nine submitted members were read. `CONSISTENCY_CHECKS.json` validates every MANIFEST entry, all audit_manifest bindings, exact membership and byte counts. README, PROOF, AUDIT, ACCEPTANCE, STATUS and the provenance/source documents agree on the theorem, n=1 restriction, lower-bound credit, row-stochastic extension, stronger-entrywise distinction, polynomial-loss example and non-novelty boundary. No current-binding conflict was found.

The assertions about pre-edition byte identity and exact old editorial differences cannot be independently established from the distributed nine files alone. The omitted diagnostic scripts/results are not distributed and were not replayed. This review establishes current mathematical correctness and current bindings with fresh evidence; it does not certify excluded historical artifacts. It requires no repair to original or root records.

The strongest verified result is the complete submitted upper theorem and its exact original asymptotic consequence. No gap remains in this review's mathematical route. Priority, optimal exponent and exhaustive literature status remain outside its certified scope.
