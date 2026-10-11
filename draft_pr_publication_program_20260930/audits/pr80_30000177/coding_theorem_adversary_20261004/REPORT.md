# Operational coding theorem adversarial report

Audit target: PR80 / 30000177 / OWR-785-003, immutable submitted head
`dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3`. Audit family: asymptotic operational
coding, independent messages, local decoding, primary theorem dependencies.
Completion estimate: 100% for this family. Novelty and priority are outside scope.

**Verdict: PASS.** No central correctness gap or necessary mathematical repair
was found. The submitted candidate establishes a strict asymptotic LOCC advantage
under the original source's unitary encoding model, and the not-LO-DC condition
needed for the LOCC-DC shell. The achievable sum rate 9/4 exceeds the two-bit
benchmark. The larger lower bound 3/2 + h2(1/4) is a supremum of achievable sum
rates. It is not a claim of optimal capacity or one-copy attainability.

## Independence and source definition

`FIRST_SOURCE_ONLY.md` and its hash pin were saved before reading CANDIDATE.md.
They derive the exact question and model from the primary OWR contribution,
published PRL, and 2005 expansion. `FIRST_CANDIDATE_VERDICT.md` fixes the first
candidate verdict after primary theorem reading and checker replay. No author
review, SOURCES.md, priority assessment, ROOT conclusion, or sibling conclusion
was read at any point. The audit inspects the complete submitted candidate,
not a new route to a weaker question.

The exact target is the four-qubit W question on printed p. 205 of
[OWR 4/2005](https://ems.press/journals/owr/articles/785). Its p. 204 expressly
uses asymptotic accessible information. The published
[PRL 93, 210501](https://doi.org/10.1103/PhysRevLett.93.210501), pp. 3–4,
defines product sender distributions and the receivers' laboratory split, and
states that W is not locally DC. The
[2005 expansion](https://arxiv.org/abs/quant-ph/0507146v1), Sections 3, 6–7,
Eqs. (16),(21),(25),(26), specifies unitary block encoding, actual locally
accessible information, its asymptotic version, strict advantage, and the shell
exclusion of LO-DC. Its p. 2 forbids classical communication between senders and
receivers and permits it among receivers. These are source observations.

For A1->B1 and A2->B2, the post-transmission cut is A1B1 : A2B2. Arbitrary block
operations within either laboratory are allowed. A protocol must exceed 2 bits
per original W copy/pair of transmitted qubits and cannot claim attainability
merely because a Holevo upper bound exceeds 2. Symmetry of W makes the indicated
equal sender/receiver assignment consistent with the target.

## Primary coding theorem verification

Freshly fetched primary
[Winter, quant-ph/9807019v3](https://arxiv.org/pdf/quant-ph/9807019v3), Section II,
defines separate encoder maps, independent uniform-message average error,
finite alphabets/output, memoryless tensor outputs, block POVMs, and limiting
achievability. Theorem 9, pp. 4–5, gives every subset rate constraint under a
product input prior. For two senders these are the two conditional mutual
informations and their joint sum bound. Its proof draws individual codebooks
independently, fixes a deterministic collection with small total average error,
successively decodes, and time-shares corners. Page 6 explicitly turns the final
classical-output operation into a POVM. Earlier messages in the successive
decoder are decoded internally; they are not provided by free sender feedback.

The citation to Theorem 9 is therefore precise and sufficient. It does not require
a later simultaneous quantum decoder theorem. Theorem 10 supplies the global
capacity-region characterization, but its converse is not needed here.

For dependency corroboration, fresh primary
[Holevo, quant-ph/9611023v1](https://arxiv.org/pdf/quant-ph/9611023v1), pp. 2–3, 6,
allows mixed output states and product codewords; Eq. (18) gives the expected
average-error bound for independently drawn words under a fixed prior and a
block POVM. This supports the single-user coding step in Winter's proof.
[Winter's original 1999 coding paper, author upload](https://arxiv.org/pdf/1409.2536v1),
Lemma 9, proves the gentle-measurement bound used for successive decoding.
No indispensable later coding dependency or pure-state-only restriction was
found. The mixed JR channel is within the primary theorem's domain.

## Applying the theorem to the submitted protocol

These are deductions from the verified theorem and the specified protocol.

1. Each sender's alphabet has four Pauli letters. The mathematical output is
   JR, with dimensions dim J=4 and dim R=4, hence dim(JR)=16. Each output is a
   normalized density operator, including zero-probability Bell branches.
   The resource copies, product encoder letters, and independent per-copy Bell
   measurement imply exactly the memoryless tensor channel required by Winter.
2. A uniform product single-letter prior produces bounds r1<=3/2, r2<=3/2,
   r1+r2<=3/2+h2(1/4). The computed entropy identities are correct. Independent
   deterministic encoder maps produce independent message-codeword ensembles
   even if letters within a selected codeword are correlated over time. Source
   block encoding permits this; single-letter independence over time need not
   hold for the final uniform message ensemble.
3. The candidate's r1=r2=9/8 has positive individual slack and positive sum
   slack, since h2(1/4)>3/4 follows from 27<32. Both constraints must hold;
   using only the joint Holevo quantity would have been insufficient.
4. Time-sharing uses predetermined disjoint blocks and independent component
   messages. Each sender's combined message set is its own Cartesian product.
   It needs no shared message, communication between encoders, encoder feedback,
   or shared randomness at execution. Random code selection in the existence
   proof is fixed before the protocol is used.
5. The theorem's <= boundary language is limiting achievability with arbitrary
   rate deficit, not finite-block equality. Balanced rates approaching half the
   sum bound remain below 3/2 individually. Thus the capacity supremum lower
   bound is justified. The strict interior point alone answers the question.

## LOCC decoding and exact resource accounting

B1's Bell measurement occurs only after receiving A1. It is local on its own
four-dimensional A1B1 system. Its classical outcome J is sent B1->B2. B2 already
holds A2B2=R; it can store J in orthogonal local pointer states without any quantum
transmission. For n copies it holds J^n (4^n classical labels) and R^n (dimension
4^n), enough to implement the theorem's output POVM on dimension 16^n.

Let E_m be any theorem POVM and P_j=|j><j| tensor I_R on the block output.
The state is diagonal in J, so E'_m=sum_j P_j E_m P_j has exactly the same
probabilities for every input pair. Define F_{m|j}=<j|E_m|j>. Positivity of E_m
implies positivity of F_{m|j}, and sum_m F_{m|j}=I_R. Thus B2 reads J and
performs the conditional POVM F on R. This is an actual locally implementable
measurement with classical outcomes. Arbitrarily large local ancillas/collective
local processing do not join the laboratories.

B2 can report its decoded pair to B1 by a final classical message if both must
know both messages. The complete direction/timing is A1->B1 and A2->B2 quantum
transmission, then B1->B2 classical Bell outcomes, then optional B2->B1 classical
decoded messages. No sender receives a message; no receiver quantum register is
transferred. Every W copy and both transmitted sender qubits are counted; all
Bell branches are retained. Discarding B1's postmeasurement system is a decoder
operation, not free sender preprocessing or a success-only resource selection.
No extra entanglement, sender filtering, resource distillation or postselection
is used. Receiver communication is permitted by the original model and carries
information extracted from the prescribed resource rather than externally
supplied sender messages.

## Average error, trimming and accessible information

The theorem and candidate claim average error, not maximal error. Multiple-access
average-to-maximal expurgation can fail to preserve independent message sets;
no such inference is made or needed by the source's accessible-information
capacity. This is a scope limit, not a gap in the submitted claim.

Optional trimming in the candidate can preserve independence. For a code with
error matrix e_{ab} and desired smaller sizes k1,k2, choose independently uniform
k1- and k2-subsets of the two message sets. The expected new average is

E[(1/(k1 k2)) sum_{a in S1,b in S2} e_{ab}]
= (1/(N1 N2)) sum_{a,b} e_{ab}.

Consequently some deterministic product pair has average error at most the old
average. Keep the corresponding individual encoder maps and original decoder;
outcomes outside S1 x S2 can be combined into an error/failure outcome. The
messages remain independent uniform variables on S1,S2. Applying the theorem
first at a slightly larger strict-interior pair supplies sufficient cardinality
for floor(2^(9n/8)) sets. This fills an omitted elementary detail, without
changing the candidate or requiring a new coding mechanism. Trimming is not
necessary to establish any strict sum advantage.

For the actual decoded message pair Mhat and independent uniform message M,
with pair-error e_n, Fano gives

I(M;Mhat) >= log2(N1 N2) - h2(e_n) - e_n log2(N1 N2-1).

For trimmed rates tending to 9/8 per sender and e_n->0, dividing by n yields
an accessible-information limit at least 9/4. The POVM just verified is LOCC,
and the message ensemble is a product of allowed unitary block encodings.
Therefore this operational code is a lower bound for the original source's
regularized accessible-information quantity, closing the potential definition
mismatch. This deduction does not conflate a Holevo upper bound with information
obtainable by measurement.

## Finite-channel evidence and shell exclusion

The submitted checker was inspected in full and replayed as `python3 -E -B`
under the evidence runner, with assertions active. It exited 0, empty stderr,
903 exact assertions, all 16 input pairs and 64 conditional blocks. Rational
power sums through the matrix dimension fix each real-symmetric spectrum by
Newton identities; Hermiticity and nonnegative claimed spectra are checked.
This validates the finite algebra, not the asymptotic theorem by simulation.

The Bell contraction has base branch weights 1/2,1/4,1/4,0 and rank-one states;
Pauli action permutes the Bell outcomes and conjugates R. Averaging yields
S(omega_xy)=3/2, S(omega_x)=S(omega_y)=3, and S(bar omega)=3+h2(1/4). Hand
checking these mechanisms agrees with the exact checker, so no entropy or
dimension mismatch was found.

W's one-qubit marginal spectrum is (3/4,1/4), and each laboratory's initial
two-qubit marginal has spectrum (1/2,1/2,0,0). The source's no-communication
formula gives CLO=2h2(1/4)<2. This independently reproduces the published W
non-LO-DC observation and supplies the shell exclusion. The optional classical
fallback sentence is a comparison convention outside strict unitary encoding;
it is unnecessary to the main result and does not add strict LO advantage.

The source's LOCC upper bound is 1+2h2(1/4), greater than this achieved lower
bound. No optimality follows. The both-Bell negative control obtains exactly
2 bits for its specified uniform Pauli ensemble and fixed measurement; it is
not a converse for alternative measurements, as the candidate explicitly says.

## Gaps, repairs, limitations and evidence custody

Central correctness gaps: none found in this family. Required candidate repairs:
none. Useful exposition additions: state Fano's bound and product-subset trimming
argument explicitly; these elementary deductions are supplied above. They do
not turn an unfinished proof into a new proof search.

This audit does not assert novelty, priority, code efficiency, explicit finite
blocklength, maximal-error achievability, experimental feasibility, one-copy
advantage, or optimal capacity. Exact asymptotic theorem application, rather
than a finite channel calculation alone, is the strongest verified result.

Source PDF hashes, lengths and immutable candidate hash/blob are pinned locally.
Every substantive extraction, download and checker replay has actual argv,
cwd, process IDs, UTC launch/end times, exit status, complete raw stdout/stderr,
and prelaunch source pins under `process_evidence`. Initial runner launches
failed before a child process because of an argument-parser defect; they are
preserved and excluded from successful-check evidence. No artifact is claimed
from those failed launches. The corrected retries all exited 0.

Filesystem exhaustion prevented two first-verdict writes. Only this audit's
own reproducible PRL render PNGs were removed after recording hashes; primary
PDFs and extraction streams remain. Render p. 3 was visually inspected. PNG
hashes: p. 3 `2d9bc92c4bc2fcd025ef9a7969cbc09471f252cac2630e882e5ee597e26ad61d`
(723622 bytes), p. 4 `bc49f39336d407f51e31e5389920ab6a3bc512138da92b7fe0e16e515da8cfef`
(770652 bytes). Their successful render argv remains in its process receipt.
No native app, queue/status/turn, original/tracked file, Git/index/branch,
publication or outreach action was performed. Instructions prohibiting external
communication were obeyed; no outside input was sought.
