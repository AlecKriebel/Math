# Independent analytic review — Zenodo 23147866

**Disposition: PASS for the exact stated theorem and operational model.** No substantive mathematical defect or unresolved central proof gap was found. The conclusion is an asymptotic achievable-rate lower bound and the specified historical LOCC-DC classification. It is not an exact unrestricted LOCC capacity, a one-copy result, a maximal-error result, a priority certificate, or human peer review.

## Immutable inputs and independence

Paper: Alec Kriebel, *Asymptotic LOCC dense coding with the symmetric four-qubit W state*, printed October 4, 2026, Zenodo version `1.0`, five PDF pages.

- PDF SHA256: `61140691594c742dff977862eddf215e23b7e7313c9fd6e4d7b3b008827bfe86`.
- TeX SHA256: `21beee795a3d8c4a43cba4ce9494698068bbdfe5e3807e15e1c1b1dde7ab7b32`.
- Published verifier SHA256: `b0b0e1fe9feaf1d9724f18bf38cef1f22f633e820460b362da2c8c1971d7f0cd`.
- All eight published files were checked against the fresh acquisition receipt. There is **no source ZIP**. The source package is a collection of individual files.

I read all five PDF pages, all of the standalone TeX, and the complete published mathematical code. I formed the independent mathematical conclusion before reading the package README. `PRIORITY_AUDIT.md` was hash-verified but deliberately not read; no archived or sibling mathematical opinions were consulted. The published code and recorded result contain a finite-algebra PASS label and historical verifier provenance. That incidental exposure is disclosed: I reproduced the code, then used a separately written density-matrix/eigenspace method and direct analytic reconstruction rather than adopting its verdict. The README's historical provenance was encountered only after the independent conclusion had been logged. A proposed primary-model subtask could not be spawned because the team had reached its agent limit; all primary checks below were done directly.

## Exact theorem and resources

The resource is the symmetric pure state

\[
 |W_4\rangle=(|1000\rangle+|0100\rangle+|0010\rangle+|0001\rangle)/2
\]

in the order `A1,A2,B1,B2`. Each sender initially owns one `Ai`, each receiver one `Bi`. For `n` copies, there are two independent uniform message sets and separate fixed codebooks. Sender `i` performs a local unitary on `Ai^n` and transmits exactly `n` qubits to receiver `i`. After transmission, the receiver cut is `L^n:R^n`, with `L=A1B1` and `R=A2B2`.

Receiver-to-receiver classical communication and collective operations inside each receiver's laboratory are allowed. There is no message disclosure from a sender, no feedback to a sender, no quantum communication between receivers, and no additional shared entanglement. The proposed encoders are only products of one-qubit Paulis, a permitted subclass of the local unitary encoders.

The result is that every nonnegative rate pair satisfying

\[
 R_1<3/2,\qquad R_2<3/2,\qquad
 R_1+R_2<3/2+h_2(1/4)
\]

is achievable with **uniform average message-pair error** tending to zero. Rates are in bits per resource copy, while the physical transmission is two qubits per copy. Receiver classical messages are internal decoder communication allowed by the model; they are not a free sender-to-receiver side channel.

## Analytic reconstruction

### Bell instrument and normalization

Reordering the tensor factors gives

\[
 |W_4\rangle=(|\psi^+\rangle_L|00\rangle_R+
 |00\rangle_L|\psi^+\rangle_R)/\sqrt2.
\]

Contraction with the four Bell bras at `L` produces the unnormalized residual vectors in equation (5). Their squared norms are `1/4,1/4,1/2,0`, which sum to one. The zero branch is kept as a zero block; there is no successful-branch conditioning, postselection, or omitted probability factor. Paulis on `A1` permute the Bell projectors up to scalar phases, and the phases disappear in each branch density operator. Paulis on `A2` act within the retained `R` system.

After receiver 1 forwards its four-valued result `J`, the entire output `JR` is at receiver 2 and has dimension `4×4=16`. Repeating the instrument separately on copies yields an actual finite memoryless classical–quantum multiple-access channel. The source entanglement across the receiver cut does not turn this into an impermissible joint receiver measurement: the first receiver has already made a local measurement, and only its classical outcome travels between laboratories.

### Spectra and entropies

I derived the conditional spectrum from the three nonzero rank-one blocks. Averaging the `A2` Pauli conjugations implements the depolarizing twirl on `A2` while preserving the `B2` marginal. Averaging `A1` distributes the residual branches evenly among the classical labels. These operations give:

| Output state | Positive eigenvalues | Entropy |
|---|---|---|
| Fixed input pair | `1/2,1/4,1/4` | `3/2` |
| Fixed `x`, averaged `y` | `1/4` twice; `1/16` eight times | `3` |
| Fixed `y`, averaged `x` | `1/8` eight times | `3` |
| Averaged `x,y` | `3/32` eight times; `1/32` eight times | `3+h2(1/4)` |

Every row has total trace one and fills the 16-dimensional space after zero eigenvalues are included. The last row follows also from each `J` block being `I_A2/8 ⊗ diag(3/4,1/4)`. Therefore both conditional Holevo quantities are `3/2`, and the joint quantity is `3/2+h2(1/4)`.

The equal entropies of the two conditional averages do not mean their spectra coincide or have a fixed majorization ordering. The independent checks verify that these two spectra are incomparable. Both are nevertheless majorized by the conditional spectrum and majorize the overall average, consistent with the respective mixture operations.

### Coding theorem and the decoder's locality

The load-bearing achievability input is [Winter's exact cited preprint, quant-ph/9807019v3](https://arxiv.org/pdf/quant-ph/9807019v3). Its definitions on PDF p. 2 use finite alphabets, a finite-dimensional memoryless output, independent message encoders and uniform average error. Theorem 9 on pp. 4–5 supplies rates subject to all subset conditional-information constraints; its proof yields deterministic codebooks and a joint output POVM. The current two-user application has precisely the two individual constraints and one sum constraint. No theorem for separated quantum outputs is being invoked: `JR` is already entirely local. The theorem is an accepted external result; this review checks its hypotheses and conclusion rather than re-proving quantum coding theory.

Dephasing each decoding POVM element in `J^n` is a positive unital block projection. It preserves positivity and the sum of the POVM elements, and its adjoint fixes every channel output. Thus it preserves all decoding probabilities. Each diagonal block is a valid POVM on `R^n`, selected by the received classical string. Receiver 1 needs only its copywise Bell measurements and a classical message; receiver 2 performs the required collective quantum decoding locally. If both receivers must know the answer, receiver 2 can report the decoded labels through the allowed classical link.

The argument does not presume that the Holevo quantity of a single noncommuting ensemble is already a one-copy accessible-information rate. The retained output family is indeed noncommuting: a checked pair has squared Frobenius commutator norm `1/64`.

### Rate accounting and limiting arguments

The sum bound is a supremum lower bound. Interior rates can approach the sum face, so no finite code exactly attaining that face is required. The symmetric boundary rate is approximately `1.155639` per sender, while `9/8=1.125` lies strictly below it and below each individual bound. The strict inequality reduces exactly to `27<32`; it does not depend on rounding the displayed decimal entropy.

The two individual bounds cannot be added as if the sum bound were absent: `(3/2,3/2)` violates the joint constraint. Time sharing between the two coding corner orders is compatible with fixed separate codebooks and requires no message-dependent coordination. Zero rates are permitted: a sender can have a singleton message set, and `(0,0)` is trivial. The coding theorem's nonnegative-rate statement and standard limiting choice of code sequences cover these boundary cases.

Fano's inequality is applied to the uniform **pair** of messages and the decoded pair. Because the logarithm of the number of message pairs is linear in blocklength and average error vanishes, the information loss per copy tends to zero. This establishes the bridge to the historical asymptotic accessible-information formulation. The manuscript explicitly handles the singleton joint message set. There is no unjustified conversion from average error to maximal error, no zero-error claim, and no supplied finite-blocklength error exponent.

## Original model, LO classification and converse boundaries

The historical model checks used original primary sources rather than the packaged priority discussion:

- [Bruß et al., quant-ph/0407037v3](https://arxiv.org/pdf/quant-ph/0407037v3), pp. 1–4: local unitary senders, split routing, receiver LOCC and the four-qubit W classification question are present. The paper distinguishes a global receiver from separated receivers.
- [Bruß et al., quant-ph/0507146v1](https://arxiv.org/pdf/quant-ph/0507146v1), pp. 3–5 and 7–10: the treatment is asymptotic and unitary-encoding; Section 6 uses product sender probabilities and the same routed receiver cut. Equations (21)–(23), (25)–(26) distinguish the LOCC upper bound, the no-communication expression, and the strict LOCC-DC shell. These are a model match, not evidence that the question remained open in 2026.
- [Original OWR 4/2005 PDF](https://ems.press/content/serial-article-files/45978?nt=1), printed pp. 203–205: Bruß's contribution explicitly discusses the asymptotic LOCC capacity and asks the four-qubit W classification question.

Independently, each one-qubit marginal of the symmetric resource has spectrum `(3/4,1/4)`, and each two-qubit marginal has spectrum `(1/2,1/2,0,0)`. For a block of `n` copies, a local sender unitary preserves the joint sender/receiver marginal entropy `n`, while its average entropy is at most `n[1+h2(1/4)]` by the fixed receiver marginal and dimension of the transmitted subsystem. Thus the raw local-unitary expression per link is `h2(1/4)` even if the sender uses unitaries across copies. The two no-communication expressions sum to `2h2(1/4)<2`. Comparing with the two-bit unassisted classical fallback does not create a strict LO advantage. This is the claimed classification convention; the fallback is not asserted to be a unitary-only reinitialization of the fixed W resource.

The achieved rate exceeds two while staying below the source's general LOCC upper bound `1+2h2(1/4)≈2.622556` and the global-receiver value `3`. These checks are consistent with a lower bound. They do not show optimality or close the remaining interval for unrestricted LOCC decoding.

The particular both-Bell measurement has four equiprobable output pairs conditional on every Pauli input pair, and a uniform 16-outcome average under the stated uniform input distribution. Its information is exactly `4−2=2` bits. This is a calculation for that instrument, not a converse for all one-copy LOCC measurements or all block protocols. [Pradhan–Agrawal–Pati, arXiv:0705.1917v1](https://arxiv.org/pdf/0705.1917v1), Section 4.2.3, PDF p. 36, describes Bell forwarding followed by a Bell measurement in its single-sender two-qubit discussion. It does not supply an asymptotic converse to the present independent-message retained-output construction.

## Reproduction and independent controls

The complete published verifier was inspected and run without optimization. Its JSON output reproduced the published result exactly, including **551 assertions**. It verifies finite channel algebra; it does not independently establish the coding theorem or priority.

The new `independent_checks.py` does not import that verifier. It uses full `16×16` density-operator conjugation by Kronecker matrices, explicit tensor-factor reordering and Bell contraction. It establishes the spectra by exact rational eigenspace nullities rather than the published power-sum method. Its **248 assertions** include:

- all 16 encoded input pairs and 64 unnormalized instrument blocks, trace preservation and eigenvalue multiplicities;
- no-signalling checks: `R` alone is independent of sender 1, and `J` alone is independent of sender 2;
- majorization checks and the incomparable equal-entropy conditional spectra;
- noncommutativity of the retained outputs;
- the both-Bell comparison, exact strict rate inequality and rate/upper-bound consistency;
- negative controls against adding the two individual maxima or treating the both-Bell calculation as the retained-output channel.

Finite matrix checks use exact fractions. Decimal entropy/rate values and their consistency comparisons are numerical diagnostics, while the strict advantage is proved by the exact integer inequality and the analytic entropy formulas. No numerical diagonalization, tolerance-sensitive eigenvalue truncation, or simulation is used as proof of achievability. Run `python3 independent_checks.py`; its saved result is `independent-checks.json`.

## Scope of the disposition

The theorem's channel calculation, decoder locality, resource accounting, coding-theorem application, asymptotic rate inference and stated classification all pass this review. There is no central defect to record for repair.

This verdict does not establish an optimal LOCC capacity, a one-copy advantage or impossibility, zero-error or maximal-error rates, a constructive blocklength bound, noise robustness, experiment feasibility, or a new coding theorem. It does not certify worldwide firstness or independently audit the complete historical literature. The contextual references not used as theorem inputs are not substitutes for a novelty search. The source's existing AI/unrefereed disclosure remains accurate. No changes to publication assets, website, spreadsheet, Git, Zenodo or external communications were made.
