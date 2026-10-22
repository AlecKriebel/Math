# Acceptance: exact threefold Feige baselines

Problem 30006570 / OWR-14299906-007. Public prose edition, 11 October 2026.

## Review and edition status

This is an AI-assisted, unrefereed mathematical proof and audit edition. Its acceptance records an internal AI mathematical audit; it is not external human peer review or formal proof-assistant certification. No novelty is claimed. The exact classical and nonsignalling baseline values were already stated in the cited primary literature. The original quantum-comparison problem remains unresolved by this work.

This is a prose proof/audit edition, not a computational reproduction package. The complete elementary arguments and compact symbolic strategies are provided here. Executable programs, raw outputs, expanded event lists, copied source documents and private coordination material are not distributed. Historical computational checks are described with their scope and limits; they are not represented as new executions during edition preparation. The hand proofs do not depend on those omitted materials.

## Accepted result

For independent uniform three-bit questions and the two-party all-coordinates-win Feige predicate, the exact classical value is 5/16 and the exact nonsignalling value is 1/3. Consequently the finite-dimensional tensor-product quantum supremum lies in [5/16, 1/3]. These baseline values are credited to Schmidt, Storgaard, Walter and Zhao, arXiv:2510.08484v3, Section 6.3: https://arxiv.org/abs/2510.08484v3 . The original question is recorded in Oberwolfach Reports 4/2026, printed p. 241: https://ems.press/journals/owr/articles/14299906 .

PROOF.md gives the full integer vertex-cost argument for the classical upper bound, the credited Boolean strategy and five-case active-bit count, the marginal-mass nonsignalling upper bound, and the three-event symbolic nonsignalling witness. AUDIT.md preserves the independent mathematical checks of these arguments.

## Exact acceptance boundary

- Local responses and POVMs may depend jointly on the entire local input vector. No product, sequential, synchronous, fixed-pattern, restricted-orbit or fixed-dimensional model replaces the original game.
- Classical randomization reduces to deterministic table pairs by convexity. Deterministic strategies are realizable quantumly in dimension one; general shared-randomness correlations need finite dimensions and are not claimed to be dimension-one correlations.
- The quantum value is a supremum over all finite-dimensional tensor-product states and unrestricted full-vector POVMs. The integer ceiling argument cannot be applied to fractional quantum or nonsignalling masses.
- The 1/3 witness is nonsignalling; no quantum realization is asserted. No strict quantum advantage, exact quantum optimum, attainment claim or negative quantum result is established.
- The source's event-order exposition is clarified, not refuted. Its stated probability and classical value are correct.
- Restricted floating-point searches found no certified improvement and failed a known one-copy calibration. This is an honest search limitation, not an upper bound in any dimension and not evidence that quantum advantage is absent. Those searches are outside the mathematical acceptance.

The original quantum-versus-classical question remains UNRESOLVED; the overall result is PARTIAL. Internal acceptance is limited to the two exact baselines and their interval consequence, with no novelty claim, blanket manuscript endorsement, external human review or formal certification.

## Verification meaning

Historical exact checks used three distinct implementations and ran under normal Python, -O and -OO. Sixteen malformed-certificate cases produced 41 scoped rejections per mode. The first two implementations were mathematical checkers rather than complete schema validators; the third covered the fuller schema. The public edition retains the hand proofs and coverage explanation, while VERIFICATION.json records only verification metadata. No omitted code, raw event list, dataset or copied source document is needed to read the proof. Hashes bind this edition to its reviewed inputs; they do not establish theorems independently.
