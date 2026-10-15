# First source only: model and historical target

This assessment was fixed before reading the immutable candidate, author SOURCES, prior reviews, ROOT results, or sibling conclusions. Inputs are only the four full primary PDFs in PRIMARY_INPUT_MANIFEST.json. The PRL author PDF and arXiv v3 bodies were read; the entire 2005 companion was read across extraction segments; the complete OWR contribution on printed pp. 203-205 was read. Selected decisive PDF pages were rendered and inspected.

## Exact model

The original question is unitary-encoding distributed dense coding using a given shared state and noiseless transmission. Two independent senders apply local unitaries to A1 and A2 with product prior message probabilities, transmit A1 to B1 and A2 to B2, and receivers decode using LOCC across A1B1:A2B2. Classical sender-to-receiver communication is excluded. Capacity is asymptotic accessible classical information per copy of the resource, with two qubits transmitted per copy. The target is a rate strictly above 2 bits, while the state remains outside LO-DC. It is not sufficient to show a global receiver rate, centralized-sender rate, probabilistic filtering with message leakage, or one-copy orthogonal-state distinguishability alone.

The standard symmetric state is |W4> = (|1000>+|0100>+|0010>+|0001>)/2 in A1,A2,B1,B2 order. The primary texts name the four-party W state without rewriting its amplitude definition; the standard symmetric interpretation is the scope used here. Under their formulas, S(B1)=S(B2)=h2(1/4), S(A1B1)=S(A2B2)=1, S(B1B2)=1, and S(W4)=0. Therefore the independent local unitary rates sum to 2h2(1/4) < 2; the classical fallback gives 2 but does not enter LO-DC. The global decoding capacity is 3. The published receiver-LOCC upper bound is 1+2h2(1/4) approximately 2.622556, which does not decide strict advantage. These entropy substitutions are deductions from the source formulas, not source claims of an achievable rate.

## Historical priority evidence

Bruß et al., *Distributed Quantum Dense Coding*, Physical Review Letters 93, 210501 (published 19 November 2004), p. 210501-4, explicitly state that four-party W is outside LO-DC and leave its LOCC-DC classification unknown. The same open statement appears in arXiv:quant-ph/0407037v3, posted 8 December 2004, p. 4. This is direct primary evidence of historical openness, not an inference from a failed search.

The OWR contribution asks: "Is the so-called W-state of four qubits in the LOCC dense codeable class?" Its preceding page fixes the asymptotic two-receiver setting, and reference [5] points to the above PRL. Source: Dagmar Bruß, *Distributed quantum dense coding*, Oberwolfach Reports 4/2005, printed pp. 203-205, DOI 10.4171/OWR/2005/04.

The July 2005 companion, arXiv:quant-ph/0507146v1, *Dense coding with multipartite quantum states*, Secs. 3.1, 6-7, distinguishes asymptotic capacities, gives receiver-LOCC only an upper bound, and defines LOCC-DC as the shell excluding LO-DC. It expands the four-qubit GHZ protocol and proves its rate is 3; it supplies no W4 affirmative theorem. The PDF carries a generated 2018 running header, which is not a new scientific version/date: its arXiv identifier is v1, 15 July 2005.

## Limits of this checkpoint

The original target is historically authentic and was open in 2004/2005. No conclusion about present priority or novelty follows yet. Current primary-literature descendants must be searched and read before a priority finding is fixed.

Primary links: https://doi.org/10.1103/PhysRevLett.93.210501 ; https://arxiv.org/abs/quant-ph/0407037v3 ; https://doi.org/10.4171/OWR/2005/04 ; https://arxiv.org/abs/quant-ph/0507146v1 .
