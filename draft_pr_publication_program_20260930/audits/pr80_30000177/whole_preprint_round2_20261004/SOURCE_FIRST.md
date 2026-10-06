# Frozen original-source model

Frozen 2026-10-04T23:44 UTC, before opening the manuscript, priority supplement, or substantive prior/sibling assessment. Administrative pin metadata has been read; its conclusions are not adopted.

The exact Oberwolfach question on printed p. 205 is: “Is the so-called W-state of four qubits in the LOCC dense codeable class?” The relevant Bruß et al. PRL 93, 210501 (2004), pp. 2–4, and arXiv quant-ph/0407037v3 agree: the four-party W state is outside the historical local dense-codeability class, while LOCC usefulness is posed as unknown. The 2005 expanded source, sections 3.1, 4, 6, 7 (printed pp. 4–11), specifies asymptotic unitary encoding and the classification shells.

The resource to test is the normalized symmetric one-excitation state

\[
|W_4\rangle_{A_1A_2B_1B_2}=\tfrac12(|1000\rangle+|0100\rangle+|0010\rangle+|0001\rangle),
\]

used as independently prepared copies. Each sender initially holds one qubit and one independent classical message. Sender choices have product probabilities, not a cooperative joint message alphabet. Each sender applies a unitary on her own subsystem; arbitrary block unitaries within that sender's copies remain local. No communication of sender messages or sender-to-receiver free classical side channel is part of this model. Transmission is noiseless: A1's encoded qubits go to B1, and A2's encoded qubits go to B2. After transmission the allowed LOCC cut is (A1 B1):(A2 B2), not A1 A2:B1 B2. Receiver-local operations can act jointly on all qubits in that receiver's lab, and classical communication between receiver labs is allowed.

The original objective is asymptotic accessible information per shared-state copy strictly above the two transmitted-qubit classical baseline of 2 bits. The original papers separate one-copy locally accessible information from asymptotic capacity. A sufficient stronger operational certificate is a sequence of independent-message codes on n copies, M1,n × M2,n codewords implemented by allowed sender-local unitary blocks, with uniform independent messages, sum rate liminf n^-1 log2(M1,n M2,n)>2, and vanishing average decoding error for an LOCC receiver protocol. Fano then relates decoded-message information to the original criterion. A one-copy success branch, global Holevo bound alone, postselection with omitted cost, or a cooperative code with correlated sender indices does not establish this objective.

The 2005 classification uses shells: LO-DC means CLO>2; LOCC-DC requires CLOCC>2 while not LO-DC; G-DC excludes LOCC-DC. The historical CLO is the sum of the two individual receiver dense-coding quantities. This is not a claim that every possible modern formulation allowing unrestricted offline pooling of separated measurement records has exactly the same noncommunication capacity.

Boundary checks fixed before seeing the proposed proof: all measurement outcomes must be retained; transmitted-qubit count remains 2 per resource copy; block operations must stay within receiver labs; input independence and both individual rate inequalities must survive coding; rate points with zero coordinates need singleton message sets; Fano must treat a singleton joint message separately; asymptotic average error is not zero error, maximum error, or an explicit finite-blocklength construction; an achievable region is not the full optimal region. A sum-face supremum is permitted for strict-interior achievability, but attainment needs separate justification.

Reading scope: entire relevant Bruß 2004 PRL body, relevant original-target paragraph plus preceding model in Oberwolfach pp. 203–205, Bruß arXiv v3 model and target passages, and Bruß 2005 sections 3.1/4/5/6/7 plus discussion. Original-source bytes are pinned in INPUT_MANIFEST.json; local extracts and actual extraction process records are private. The workshop's other contributions and unrelated bibliography entries are not claimed read.
