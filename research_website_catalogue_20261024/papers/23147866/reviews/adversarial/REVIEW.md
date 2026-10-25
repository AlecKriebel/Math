# Independent adversarial review: Zenodo 23147866, v1.0

**Verdict: PASS for the stated mathematical claim.** No substantive error or missing central argument was found in the five-page published note. This is a mathematical review of an unrefereed preprint, not conventional peer review or certification of novelty.

The strongest verified claim is the achievability, with independent messages and vanishing uniform average error, of every nonnegative pair

\[
R_1<3/2,\quad R_2<3/2,\quad R_1+R_2<3/2+h_2(1/4).
\]

The resource is one symmetric four-qubit W state per use; sender i sends its one qubit to receiver i; the receiving laboratories are A1B1 and A2B2. Within this precise model, the asymptotic LOCC sum-capacity is at least 2.311278124459… bits per resource copy, and (9/8,9/8) is achievable. The paper does not prove the optimal capacity or a one-shot advantage.

## Source binding and independence

Actual published PDF: `sources/w4_locc_dense_coding.pdf`, SHA256 `61140691594c742dff977862eddf215e23b7e7313c9fd6e4d7b3b008827bfe86`.

Actual TeX: SHA256 `21beee795a3d8c4a43cba4ce9494698068bbdfe5e3807e15e1c1b1dde7ab7b32`. Published verifier: SHA256 `b0b0e1fe9feaf1d9724f18bf38cef1f22f633e820460b362da2c8c1971d7f0cd`.

All five PDF pages and the full TeX were read; the instrument, spectra, decoding and scope pages were also inspected as rendered pages. The mathematical support code was read and replayed. All seven digests in the published SHA256SUMS match; no ZIP is part of this deposit. `inputs.json` binds all eight published files and acquisition records.

No sibling review or historical review body was consulted. `PRIORITY_AUDIT.md` remained unread: only its bytes were hashed. The manuscript itself declares prior AI reviews. After the first independent proof pass and 429 exact controls, the published verifier and README were read; their incidental provenance text includes a historical `claimed_solved` label and prior review identifiers. These assessments were not used as evidence. The fresh script imports no archived implementation. Its final 537 checks include additional direct branch-permutation and majorization controls added after the published replay.

## Attack on the physical model

The original computational order A1,A2,B1,B2 matters. Reordering into A1B1:A2B2 gives the displayed two-term Schmidt decomposition. The two sender actions really act on different qubits and commute. Each codeword is a tensor product of single-qubit Paulis, so even the smaller class of product encoders supplies the claimed inner region; no joint sender operation or knowledge of the other sender's message is hidden in the construction.

Receiver 1's Bell measurement acts jointly only on A1B1, after A1 has arrived. It is a complete local measurement, including its zero-probability branch where appropriate. All outcomes are forwarded. The residual vectors have squared norms 1/4,1/4,1/2,0 before encoding. Consequently the protocol is trace preserving, not a success-conditioned filter. The first receiver retains no quantum system needed by the decoder. Receiver 2 holds the received A2 and original B2 plus the classical report J.

The accounted resources are n copies of W4, n transmitted qubits from each sender, and permitted receiver-to-receiver classical communication. The proof uses neither receiver quantum communication, extra entangled pairs, catalysis, a sender feedback channel, nor a successful-branch probability omitted from the rate. The W copies are consumed; preparation cost is not claimed to be free in a resource-independent sense. The comparison to two classical bits is per two transmitted qubits with the stipulated entangled resource supplied.

## Finite algebra and falsification controls

The fresh exact implementation constructs the literal 16-component W vector and four-qubit Pauli matrices, projects the first and third bits onto unnormalized Bell vectors, and divides their outer products by two. This differs from the published sparse Fraction implementation and its power-sum spectrum certification. SymPy rational matrices and exact eigenvalues certify all 64 blocks, normalization, positivity, and ranks, as well as the averaged spectra:

| State | Positive eigenvalues | Entropy |
|---|---|---|
| Conditional output | 1/2, 1/4, 1/4 | 3/2 |
| First input fixed, second averaged | 1/4 twice; 1/16 eight times | 3 |
| Second input fixed, first averaged | 1/8 eight times | 3 |
| Both averaged | 3/32 eight times; 1/32 eight times | 5 − (3/4) log₂3 |

This reproduces both conditional Holevo values 3/2 and the sum value 7/2 − (3/4)log₂3. The actual branch matrices, not just their spectra, agree with the Bell-permutation formula in equation (6). All four single-qubit marginals and all six two-qubit marginals have the stated spectra. Majorization checks are consistent with increased entropy under the partial and complete Pauli averages. The single-qubit marginal is strictly nonuniform, so h₂(1/4)<1.

Controls designed to lose the claimed advantage behave as expected. Measuring both receiving pairs in the Bell basis yields exactly four conditional outcomes of probability 1/4 and a uniform average over 16 outcomes: mutual information is exactly two bits. Erasing J eliminates every dependence of receiver 2's state on sender 1, and the joint Holevo value drops to h₂(1/4). Keeping only the original Ψ+ branch leaves trace 1/2, exposing the cost that an illicit postselection would omit. An explicit POVM with off-diagonal classical-register blocks gives exactly the same outcome probabilities after pinching for every input pair. Positivity and completeness of its pinched effects are checked. These controls validate mechanisms, not a capacity converse.

The published standard-library verifier was separately executed without optimization. Its 551 checks pass, and its output matches `verification_results.json` exactly. Those checks establish finite algebra; neither their count nor the independent finite controls supplies the asymptotic theorem.

## The coding-theorem interface and quantifiers

[Winter, arXiv:quant-ph/9807019v3](https://arxiv.org/abs/quant-ph/9807019v3), §II and Theorem 9, is the essential imported theorem. It treats finite classical input alphabets, product input distributions, density-operator outputs, separate message-to-codeword maps, and uniform average decoding error. Its direct theorem gives the subset rate constraints for one quantum-output receiver. This applies after the Bell instrument: J and R are both at receiver 2, so the theorem is not being applied to a forbidden joint measurement across the original laboratory cut. Conditional on any pair of codewords, the output is a product over independent W copies; selected codewords need not themselves be independently drawn on every use after the deterministic codebooks are fixed.

The classical-register pinching argument is sound for every blocklength, not merely the sample POVM tested computationally. Positivity and the identity sum survive the pinching map. Each diagonal J-string block sums to the identity on R^n and is a local POVM there. Because all output states are diagonal in J^n, pinching preserves every decoding probability. Thus the abstract decoder is physically realizable by receiver 1's copywise measurements followed by a conditional collective measurement wholly inside receiver 2's laboratory. Reporting the decoded labels back is allowed classical communication.

There is no step from one-shot Holevo information to operational capacity without a coding theorem. The proof explicitly invokes that theorem. Its rates approach the sum face as a supremum; it makes no finite-block equality assertion. The exact inequality 27<32 establishes the strict (9/8,9/8) example. Zero-rate users cause no issue: singleton message sets are permitted. Fano's inequality is applied to the pair of independent uniform messages; dividing by n makes its penalty vanish when average error tends to zero and rates converge. The sole-message case is separately addressed. No expurgation to maximal error, zero-error result, or finite error exponent is inferred.

## Classification and primary-source comparisons

[Bruß et al., quant-ph/0507146v1](https://arxiv.org/abs/quant-ph/0507146v1), §§6–7, explicitly uses product message probabilities, local unitary encoders, the post-transmission receiver cut, and an asymptotic LOCC capacity. Its LO expression and classification conditions give 2h₂(1/4)<2 for this resource. The local entropy bound remains additive for collective unitary encoding on copies: each conditional local state has entropy n and the averaged local state's entropy is at most n+n h₂(1/4). Allowing the classical fallback does not produce a strict LO advantage. Achieved LOCC advantage therefore puts W4 in the claimed source convention's LOCC-DC shell.

The specific W-state question is present in the conclusion of [Bruß et al. 2004](https://arxiv.org/abs/quant-ph/0407037v3) and on printed page 205 of the [Oberwolfach 2005 report](https://ems.press/content/serial-article-files/45978). This checks the historical target, not continuing worldwide openness through 2026.

[Pradhan–Agrawal–Pati, 0705.1917v1](https://arxiv.org/abs/0705.1917v1), §4.2.3, does contain the Bell-measurement/forwarding/Bell-measurement construction and a two-bit result. It is not an asymptotic converse for the retained-quantum-output protocol here. [Huang–Zhang–Hou, quant-ph/9911120v5](https://arxiv.org/abs/quant-ph/9911120v5), §6, already applies multiple-access coding to independent dense-coding encoders; the present note appropriately does not claim this general framework.

[Das et al., 1412.6247v1](https://arxiv.org/abs/1412.6247v1), §II and equation (4), and [Muhuri et al., 2211.13057v2](https://arxiv.org/abs/2211.13057v2), equations (6)–(7), supply upper bounds in the split-receiver setting. Neither cited bound above two is an achieved rate. The noiseless bound here is 1+2h₂(1/4), larger than the achieved lower bound, so no conflict occurs. [Hayashi–Wang, 2109.12518](https://arxiv.org/abs/2109.12518), §III, starts with one encoding party holding A, a helper holding F, and transmission of A to one message receiver. Its local cut separates the whole transmitted system from F; it cannot simply replace A1B1:A2B2 with A1A2:B1B2. It is not the theorem used in this proof.

Cao–Song's DOI and four-qubit-W abstract were found, but full publisher text was not retrieved because access was denied. I therefore do not certify the precise historical location of that decomposition. Its identity is independently established directly from the four-term state, and no security theorem or operational claim from that paper is imported. Reference receipts record the nine downloaded primary documents and hashes.

## Remaining limits and disposition

There is **no identified mathematical gap in the stated achieved region or classification**. Exact optimal LOCC capacity, an improved converse, one-copy accessibility, efficient finite-block codes, robustness to noise, maximal-error communication, and worldwide priority remain outside this review and outside the proved theorem. The coding existence result is nonconstructive in the operational sense stated in the manuscript. The finite checker is not a replacement for it.

The paper can pass this adversarial mathematical gate with its existing scope qualifications. No source, website, spreadsheet, Git state, Zenodo record, or external communication was changed. Downloaded references and rendered pages are ignored cache files; durable independent checks and hash-bound records remain in this review directory.
