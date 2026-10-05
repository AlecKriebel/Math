# FIRST_SOURCE_ONLY — locked before candidate read

Established at UTC: 2026-10-04T21:42:43.855656+00:00
Completion toward operational/theorem audit: 25%.

## Independence
Only repository instructions, the four primary PDFs supplied in source custody, and this audit's own extraction streams have been read. No CANDIDATE, source-manifest author claims, reviews, priority notes, ROOT/sibling conclusions, or candidate proof artifacts have been read. This is the independently established interpretation against which the submitted candidate will be tested.

## Exact target and success criteria
Oberwolfach Report 4/2005, contribution “Distributed quantum dense coding”, printed pp. 203–205 (PDF pp. 19–21), asks on p. 205: “Is the so-called W-state of four qubits in the LOCC dense codeable class?”

The contribution p. 204 defines the LOCC capacity as the asymptotic locally accessible information, maximized over the senders' unitary encodings and probabilities. Two distant receiver laboratories hold A1B1 and A2B2 after A1 sends to B1 and A2 sends to B2; their operations must be LOCC across that laboratory split. Published PRL 93, 210501 (2004), p. 210501-3 states the product probabilities explicitly and the asymptotic convention. Its p. 210501-4 says four-party W is not locally DC but LOCC-DC status unknown. The shell interpretation is visible in the Fig. 1 caption (published p. 210501-3).

The 2005 expansion arXiv:quant-ph/0507146v1, p. 10, Eq. (26), makes the shell definition explicit: CLOCC > sum_j log2 dAj and not LO-DC. For two qubit senders the strict threshold is 2 bits per copy/channel use of the two sender systems. Its p. 7, Eq. (16), defines the one-capacity through actual LOCC accessible information, not the upper bound; p. 8 Eq. (21) extends an additive upper bound to asymptotic use. Pages 5 and 8 allow multiple copies, collective local unitaries on a sender's copies, and asymptotic regularization, while keeping unitary encoding. Achievability must exhibit operations satisfying the laboratory split and surpass 2 strictly, rather than merely compute a Holevo upper bound above 2.

## Operational assumptions from primary sources
- The resource is a specified shared quantum state; capacity is a property of the state, rather than noisy-channel entanglement assistance (OWR p. 203; expansion p. 2).
- Senders encode by local unitary transformations with individual independent message distributions: p_{i} = product_j p_{ij} (PRL p. 3; expansion pp. 5, 7, Eqs. (11),(16)). Arbitrary correlated centralized codeword selection does not automatically meet this condition.
- Sender-to-receiver quantum channels are noiseless; all sender quantum systems are transmitted once. No uncounted auxiliary entangled resources or quantum link between receivers occurs (expansion pp. 2, 12).
- Receivers may exchange classical communication, and act collectively within their own laboratories; the full bipartite block decoder cannot cross the A1B1 : A2B2 split by quantum operations.
- Classical communication between senders and receivers is forbidden (expansion p. 2; PRL p. 2 explanation of excluded preprocessing). Receiver-to-receiver post-transmission communication is allowed.
- A pre-existing state cannot be distilled/filtered using free sender-to-receiver classical preprocessing (PRL p. 2). Any resource discard or postselection must be included in the rate/resource accounting and compatible with unitary encoding.
- Average accessible information and asymptotic regularization are the primary-source language. Reliable independent-message coding gives a sufficient lower bound via Fano's inequality. A demand for maximal error is not stated by these source definitions; it must be separately justified if claimed.

## Boundary and exclusion requirements
The strict >2 condition must be met with an attainable strict-interior code rate. A supremum equal to a number >2 is sufficient if rates arbitrarily close from below are achievable; claiming exact attainment of a capacity boundary is unnecessary. A shell classification also requires CLO <=2. The published PRL explicitly lists W as not locally DC, but a checkable independent reduced-state calculation would be useful rather than accepting this alone.

## Source observations versus deductions
The operational restrictions and shell definition above are direct source observations. Interpreting an independent reliable block code as sufficient for asymptotic accessible information is a deduction, requiring an actual coding theorem and Fano calculation. The PDFs do not provide a generic LOCC achievability theorem. Upper-bound formulas do not prove W membership. None of these sources alone gives the W solution.

## Evidence pins
Full PDF SHA256/length pins are in source_pins.json. Extractor argv, cwd, process IDs, UTC times, exit status and complete streams are under process_evidence/*_extract_retry. Published PRL pp. 3–4 were rendered into prl-definition-3.png and prl-definition-4.png; p. 3 was visually inspected. An initial runner argument-order defect prevented launch in four *_extract records; corrected retries all exited 0 with empty stderr. Those failed metadata are preserved rather than discarded.
