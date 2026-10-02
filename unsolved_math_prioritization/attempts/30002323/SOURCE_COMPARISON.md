# 30002323: reported prior negative answer, construction not independently verified

**Source gate only; zero substantive author turns.** The later primary report explicitly credits Gábor Tardos with a counterexample. This record verifies that announcement and its relevance to the imported question; it neither supplies nor independently verifies the counterexample itself. Proposed source-based disposition: `already_solved`, 0/5, with this qualification retained prominently.

## Exact source scope and location

1. **Original:** Ehud Friedgut's complete contribution, *Combinatorics and Probability*, Oberwolfach Report 18/2013, printed p. 1118 (PDF p. 32), DOI 10.4171/OWR/2013/18. It asks whether every partition of the symmetric group into cosets fixing prescribed images of t distinct points coarsens to a partition of the same kind with t−1 prescribed images. Its explicit two-point example makes the pointwise stabilizer interpretation unambiguous. No fixed-t/large-n restriction is stated. [Official report](https://publications.mfo.de/bitstream/handle/mfo/3349/OWR_2013_18.pdf?isAllowed=y&sequence=1)
2. **Repeated question:** Ehud Friedgut's separate contribution, *Combinatorics*, Oberwolfach Report 1/2014, printed p. 81 (PDF p. 77), repeats the same unrestricted question. The preceding graph-block problem belongs to Reinhard Diestel; the subsequent Hamilton-circuit problem belongs to Peter Heinig. [Publisher report](https://ems.press/content/serial-article-files/46491)
3. **Later update:** Ehud Friedgut, “Partitioning the symmetric group into cosets,” *Combinatorics and Probability*, Oberwolfach Report 22/2016, printed p. 1217 (PDF p. 29), states the fixed-t, sufficiently-large-n version and immediately reports: “This turns out to be false; a counterexample was found by Gábor Tardos.” [Publisher report](https://ems.press/content/serial-article-files/46627); [official MFO copy](https://publications.mfo.de/bitstream/handle/mfo/3526/OWR_2016_22.pdf?isAllowed=y&sequence=1)

All three entire contributions and their boundaries were extracted and visually checked. The 2016 entry ends immediately after the attribution; Johannes Lengler's next contribution follows. **The entry supplies no construction, numerical parameters, partition list, proof, or bibliographic reference for the counterexample.** The preceding references belong to a different problem. Targeted searches did not locate a separate explicit construction during this bounded gate. This is a retrieval limit, not an assertion that no proof exists elsewhere.

## Logical comparison, not a reconstructed counterexample

Let Q(n,t) mean that every partition of S_n into t-cosets refines some partition into (t−1)-cosets. The 2013 affirmative answer would assert Q(n,t) for every admissible pair (n,t). It therefore implies

    for each fixed t, there exists N(t) such that Q(n,t) holds for all n >= N(t).

This is the 2016 affirmative statement. Its negation implies the negation of the 2013 universal assertion. Thus the reported negative answer in 2016 addresses the earlier target as well. The eventually-in-n affirmative statement is logically weaker, not stronger, than the unrestricted affirmative statement. No particular t, n, infinite family, or explicit partition is inferred as a independently verified construction here. The only mathematical verification in this gate is the elementary implication between the two assertions.

## Imported record and related aliases

The pinned imported record for 30002323 / OWR-12481-012 labels the question open as of its 2026-08-21 triage and says no later resolution was found. The 2016 primary announcement is a reason to correct that source-status assessment. Direct access to the current UnsolvedMath page failed; the pinned data and primary reports were used instead.

ID 30002469 / OWR-12861-020 combines Diestel's graph-block question with Friedgut's separate 2014 coset question. The reported negative answer applies only to its coset subquestion. It establishes nothing about the graph-block question or Heinig's neighboring Hamilton-circuit question; the imported literature note mentioning Hamilton-generation is not evidence for either coset refinement or graph blocks. No other row is changed by this record.

## Prior-attempt gate and limits

Repository PR searches (all states), commit searches for both identifiers, their OWR aliases, coset partition, and Tardos, target-path histories, all 348 live branch names, and commit/path/ref searches across 411 locally mirrored refs found no matching earlier attempt. See PRIOR_GATE.json. These finite checks do not certify inaccessible or deleted history. The dataset's research entry under OWR-12481-012 is null.

## Disposition and credit

No author proof turn was opened. The source gate recommends skipping new research on the basis of the explicit primary report of a prior negative answer, credited to Gábor Tardos. `already_solved` is a source-status category here, not a claim of a new solution or a verified counterexample artifact. The qualification “reported prior negative answer; construction not independently verified” must accompany any queue, PR, or summary disposition. No novelty claim, external researcher contact, paper, or DOI for a new result is made.
