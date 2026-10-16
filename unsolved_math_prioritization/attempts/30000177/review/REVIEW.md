# Independent adversarial review: W₄ with receiver-only LOCC

**Verdict: PASS_COMPLETE_ASYMPTOTIC_CLASS_MEMBERSHIP.** The frozen protocol answers the exact four-qubit W-state question affirmatively in the source's asymptotic unitary-encoding model. Independent rates 9/8 and 9/8 bits per resource copy are achievable, exceeding the two-bit benchmark for the two transmitted qubits. The argument also proves the stated sum-rate supremum lower bound 3/2+h₂(1/4). It does not establish the optimal capacity, a single-copy advantage, or a zero-error code. No mathematical correction is required.

Reviewed independently on 30 September 2026 using GPT-6 Astra at xhigh reasoning effort. The reviewed `CANDIDATE.md` has SHA-256
`fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404`.
Its unchanged bytes are preserved in `author_replay/CANDIDATE.md`. Historical novelty and human peer review remain unestablished.

## 1. Exact task and permitted resources

I read the complete Bruß contribution on printed pp.203–205 of [OWR 4/2005](https://ems.press/journals/owr/articles/785), and inspected the model and final question on rendered pp.204–205. It treats independent information at the senders, fixed transmission assignments to the two receivers, receiver LOCC, and asymptotic capacity. It does not require an orthogonal single-use alphabet or perfect one-shot discrimination.

[Bruß et al., Sections 6–7](https://arxiv.org/abs/quant-ph/0507146v1), provide the detailed model. The sender probabilities factor, their unitaries act separately, and the receivers' spatial split is taken after the prescribed quantum transmissions. Equation (26) requires capacity strictly above the unassisted benchmark; the LOCC-DC shell also excludes LO-DC. The candidate respects both requirements.

For n resource copies, each sender sends exactly n physical qubits to her designated receiver, for a total of 2n. Tensor-product Pauli encodings are a permitted subclass of local unitary block encodings. Joint design of fixed public codebooks in advance is ordinary code design; it does not give the senders a shared message or communication about their actual messages. No encoding depends on measurement outcomes or feedback.

The Bell measurement occurs only after A₁ arrives at B₁, so both measured qubits are at B₁. Its outcome is sent classically to B₂, as the model allows. This internal receiver communication is not a free classical channel from either sender. If both receivers must output the full pair, a final classical message from B₂ to B₁ achieves that without quantum communication.

## 2. Independent state and spectrum audit

I constructed the four-qubit density operator in the original order A₁,A₂,B₁,B₂, applied the two local signed-Pauli permutations, and only then regrouped it into L=A₁B₁ and R=A₂B₂. This independently confirms the candidate's use of symmetry: the regrouping does not move any physical system between receivers beyond the allowed transmissions.

For the identity input, the unnormalized R blocks are the two Bell-outcome blocks of weight 1/4 proportional to |ψ⁺⟩⟨ψ⁺|, one block of weight 1/2 proportional to |00⟩⟨00|, and one zero block. The first sender's Pauli permutes the Bell labels up to global phases; the second conjugates the R blocks. Every input pair therefore has cq spectrum (1/2,1/4,1/4), with remaining eigenvalues zero. All branches are retained, their traces add to one, and their weights are not renormalized after a successful event.

The averaged spectra also check out exactly:

- With X fixed and Y averaged: two eigenvalues 1/4 and eight eigenvalues 1/16, so entropy 3
- With Y fixed and X averaged: eight eigenvalues 1/8, so entropy 3
- With both averaged: each classical-label block is diag(3,1,3,1)/32, so the full spectrum has eight copies each of 3/32 and 1/32, and entropy 5−(3/4)log₂3 = 3+h₂(1/4)

Together with the input-pair entropy 3/2, these give the two conditional information bounds 3/2 and the sum bound 3/2+h₂(1/4). The subscripts on the averaged states are correctly interpreted as the input remaining fixed, rather than physical subsystems. In particular no factor of two or omitted classical-outcome entropy is present.

## 3. Why the coding theorem supplies independent-message achievability

I checked [Winter, Section II and Theorem 9](https://arxiv.org/abs/quant-ph/9807019v3), including the full direct-theorem construction through its successive gentle decoding. Its inputs are separate finite classical alphabets with a product distribution; its code has separate maps from each sender's message set to that sender's input strings. Error is averaged over the uniform product of message sets. The theorem supplies a single output POVM recovering the complete message tuple with vanishing average error under all subset-rate inequalities.

The induced channel here has finite alphabet sizes four and four and finite output algebra consisting of a four-valued classical register and a four-dimensional quantum system. It is memoryless: independent W₄ copies, tensor-product letter encodings, and the same per-copy local Bell measurement give exactly the tensor product of the one-copy cq outputs. Thus all direct-theorem hypotheses are met.

The conditional mutual informations in the region do **not** mean that B₂ is handed either message for free. Winter constructs the decoder from the channel output, with previously decoded records generated internally. As an independent check, the two upper corner points for this particular distribution are

(h₂(1/4), 3/2) and (3/2, h₂(1/4)).

The first coordinate at a successive-decoding corner is the unconditional information S(ω̄)−S(ω_X)=h₂(1/4), followed by the conditional bound 3/2. Time-sharing the two orders gives the symmetric point (3/4+h₂(1/4)/2, 3/4+h₂(1/4)/2). This confirms the feasibility of symmetric rates above 9/8 without relying on a mistaken interpretation of the two conditional bounds in isolation.

The strict gap has an exact certificate:

h₂(1/4) = 2−(3/4)log₂3 > 3/4,

because 27<32. Hence 9/8<3/2 individually and 9/4<3/2+h₂(1/4) jointly. Approaching the sum boundary gives the claimed supremum lower bound; it need not be attained by a finite block code with zero error.

The theorem's limiting rate convention is enough. If exact smaller message-set sizes are desired, they may be selected as Cartesian subcodebooks by averaging: the expected average error of uniformly chosen sender subcodebooks equals the original average error, so some pair has no larger error. This selection is made offline and preserves independent uniform messages.

For the source's accessible-information formulation, the connection is also direct. If the message pair M is uniform and the pair-decoding error tends to zero, Fano's inequality gives H(M|M̂)=o(n) for fixed finite rates. Therefore I(M;M̂) is at least n(r₁+r₂)−o(n). The constructed vanishing-average-error codes consequently certify the required asymptotic dense-coding advantage. No maximal-error or one-copy zero-error conclusion is needed or inferred.

## 4. Why the output POVM remains LOCC

After the preprocessing, B₂ physically possesses Rⁿ and the complete classical record Jⁿ. B₁'s remaining quantum systems are never used by the block decoder. Thus the single-receiver output in the theorem is an actual locally available system, not the original bipartite receiver system treated as if it were colocated.

More explicitly, every output state is block diagonal in Jⁿ. Pinching any candidate output POVM in that register preserves positivity, the sum-to-identity condition, and every measurement probability. In each observed classical block jⁿ, its diagonal blocks form an ordinary POVM on Rⁿ. Reading jⁿ and applying that local POVM is therefore a valid implementation at B₂. This remains true when the POVM processes arbitrarily many of B₂'s own qubits jointly; locality is with respect to the receivers' spatial split.

The protocol has a fixed finite communication pattern: local measurements at B₁, a forward classical record, local block decoding at B₂, and optionally a final classical return of the decoded pair. It uses neither a joint receiver quantum decoder nor extra shared entanglement, sender coordination about the messages, postselection, or receiver-to-sender feedback.

## 5. LOCC-DC shell and the limits of the conclusion

The one-qubit resource marginals have eigenvalues 3/4,1/4. Each relevant two-qubit marginal has eigenvalues 1/2,1/2,0,0. The source's unitary no-communication expression is consequently 2h₂(1/4)<2. Strict inequality follows, for example, from 27>16, which gives log₂3>4/3. If a classical-only fallback is included in the convention, it reaches the threshold two and still gives no strict LO-DC advantage. Combined with the strict achievable LOCC rate above, this places W₄ in the requested LOCC-DC shell.

The source's LOCC upper bound specializes to 1+2h₂(1/4), which exceeds the proved lower bound. It is not assumed to be attainable. The candidate therefore makes no optimal-capacity claim.

I also verified the both-Bell control: for every uniform Pauli input pair, the classical output distribution has four equiprobable outcomes, and the overall output is uniform on sixteen pairs. Its mutual information is exactly two bits. This diagnoses the loss incurred by that particular extra measurement; it is not an upper bound on every single-copy protocol.

[Pradhan–Agrawal–Pati, Section 4.2.3](https://arxiv.org/abs/0705.1917v1), already describes the Bell-measurement pattern for a selected four-state, two-bit W alphabet. Its presentation has one Alice holding the two encoding qubits, rather than proving the present independent-message asymptotic rate region. That prior receiver processing is properly credited. The retrieved 2015 and 2024 two-receiver papers discuss general upper bounds and noisy-state comparisons; none of those bounds is used here as an achievability theorem. Bounded additional primary-source searches did not establish priority for this particular construction. Absence of a matching result is not a novelty certificate.

## 6. Reproduction and recommendation

All six source PDF hashes and byte lengths matched the recorded files. The submitted checker reproduced its receipt byte for byte: **903 exact assertions**.

The independent standard-library checker imports no author code. It works with rational density matrices and Bell projectors, computes exact characteristic polynomials by determinant expansion rather than using the author's conditional-vector and trace-power method, and checks every input pair and conditional block. It also verifies all one- and two-qubit marginals, exact entropy arithmetic, the both-Bell control, and probability-preserving pinching for a genuine sixteen-outcome Hadamard POVM. **All 759 assertions pass.** These finite checks certify the stated channel algebra; asymptotic coding remains the application of the established direct theorem.

Run `python3 independent_checks.py` and `python3 author_replay/verify_channel.py` from this review directory and compare stdout with the corresponding JSON receipts. Preserve the frozen candidate beside the copied author checker, which records its hash.

The package is suitable for publication as a complete candidate affirmative answer in the exact source model, with a separate adversarial AI review passed. Preserve the average-error/asymptotic scope, the two-qubit accounting, the independent-message condition, and the limits on optimality and historical novelty. No source artifact was edited during this review. Source PDFs, rendered pages and caches are excluded from the public review bundle.
