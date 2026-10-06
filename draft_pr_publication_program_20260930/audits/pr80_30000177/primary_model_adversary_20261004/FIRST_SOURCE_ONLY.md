# FIRST_SOURCE_ONLY: historical model audit for problem 30000177 / OWR-785-003

First independent source conclusions. Created and fixed before any candidate, readiness assessment, author proof, old triage, sibling mathematical conclusion, priority assessment, or review was inspected. This audit reconstructs a historical question; it does not answer it or establish novelty.

## Source result

The original question is whether the fixed, symmetric four-qubit W resource has **asymptotic LOCC dense-coding capacity strictly greater than 2 bits per use**, with **two separately encoded sender messages**, one qubit transmitted from each sender to its respective receiver, and **LOCC decoding across the two receivers' laboratories**. A common-message encoder, one-shot zero-error requirement, or resource-conversion protocol with sender-to-receiver classical communication is a different contract.

The exact target appears in the Bruß contribution, printed OWR p. 205 (PDF page 21): “Is the so-called W-state of four qubits in the LOCC dense codeable class?” The surrounding protocol is on printed pp. 203–204. [Original OWR report, DOI 10.4171/OWR/2005/04](https://ems.press/content/serial-article-files/45978).

## Independently reconstructed contract

1. **State and placement.** Write the four original tensor factors as `A1 A2 B1 B2`. The fixed resource is
   `|W4> = (|0001> + |0010> + |0100> + |1000>)/2`.
   OWR and PRL name the state rather than printing this ket. The PRL's reference [23], Dür–Vidal–Cirac, explicitly supplies this four-qubit ket in Sec. V.B, Eq. (30), arXiv PDF p. 8. Its permutation symmetry makes the particular relabeling of four single-qubit parties immaterial. [Cited W-state primary paper](https://arxiv.org/pdf/quant-ph/0005115v2).

2. **Separate messages and local encoding.** The explicit PRL two-receiver family is
   `P(i1,i2)=p1(i1)p2(i2)`,
   `rho_i1i2=(U_i1^A1 ⊗ V_i2^A2 ⊗ I_B1 ⊗ I_B2) rho (...)†`.
   Each sender's unitary is indexed by her own message. The objective concerns information about the message tuple. This is stronger model evidence than the informal statement that messages may differ: the prior and unitary family are explicitly factorized. Shared deterministic code design is consistent with this family. Allowing one encoder to depend on both message indices is not justified by this displayed model. Source: PRL 210501-2, final paragraphs; 210501-3, left column; arXiv 0407037v3 pp. 2–3. [Published PRL primary PDF](https://wordpress.qubit.it/wp-content/uploads/publications-dariano/PhysRevLett_93_210501.pdf).

3. **Transmission and decoding cut.** `A1 -> B1` and `A2 -> B2` over noiseless quantum channels. After transmission, receiver 1 owns `A1 B1`, receiver 2 owns `A2 B2`. “Local” therefore refers to `A1 B1 : A2 B2`, not to four permanently separated one-qubit laboratories. Each receiver may perform joint operations on everything within her laboratory. Receiver-to-receiver classical communication is allowed in LOCC decoding; receiver-to-receiver quantum communication or a measurement spanning both laboratories changes the scenario to global decoding. Source: OWR p. 204; PRL 210501-3, left column.

4. **Fixed resource and encoders.** The source optimizes the unitaries and their probabilities for the given state. It does not optimize an initial state conversion. PRL 210501-2 explicitly refuses classical communication between a sender and receiver to change the shared state, discussing filtering as an example. Thus distillation/filtering with such communication is outside the stated resource task. The later primary expansion makes the unitary-only restriction explicit in both bipartite and multipartite settings: arXiv 0507146v1 p. 5, after Eq. (10), and p. 12, discussion. Receiver-side local operations after transmission are part of decoding; that does not authorize an earlier sender–receiver resource-conversion stage. [Later primary expansion](https://arxiv.org/pdf/quant-ph/0507146v1).

5. **Asymptotic success criterion.** PRL 210501-1 discusses asymptotic attainability using the coding theorems cited as [11]; 210501-2 states that product encodings of signal states suffice in the one-receiver case. PRL 210501-3 defines the two-receiver capacity through the asymptotic version of LOCC accessible information, optimized over the sender unitaries/probabilities. OWR p. 204 uses the same asymptotic language. A perfect single-copy discrimination protocol is a sufficient special case, not the required definition. Positive one-copy accessible information is not itself a declaration of a zero-error code. A finite-block lower bound needs a valid coding/normalization bridge to a capacity claim.

6. **Benchmark and membership.** The strict benchmark is `log2 dA1 + log2 dA2 = 2`; equality does not establish dense codeability. This is a sum benchmark, not a requirement that each sender separately exceed one bit. PRL 210501-3 gives the strict dimension inequality; 210501-4 states that W is not locally dense-codeable and leaves LOCC usefulness open. The expansion's Eq. (26), p. 10, defines the LOCC-DC shell using `C_LOCC > sum_j log2 dAj` and excludes LO-DC. For the specified W state, the source's existing non-LO-DC statement makes the unresolved issue the strict LOCC advantage.

## Source ambiguities and necessary qualifications

- **The original is not a fully specified modern capacity theorem.** It does not spell out a full multiple-access rate region, an explicit error limit, a limsup/supremum convention, or the exact class of block encoders in its two-receiver definition. The asymptotic claim and cited coding context support ordinary long-block communication, with vanishing decoding error as a standard operational reconstruction. They do not support silently changing the question to one-shot zero error. A later argument should state its coding bridge rather than rely on the word “capacity.”

- **Blocks versus one use.** The expansion pp. 3–5 distinguishes a one-use unitary-encoding Holevo quantity from capacity and permits a sender's unitary to act across several copies of her own subsystem. It then states the two-receiver upper bound applies asymptotically, p. 8, Eq. (21). Consequently an impossibility argument confined to single-copy product measurements or unitary products across copies cannot settle the stated asymptotic question without an additional argument. This is a scope consequence, not a newly proved capacity result. The original short article itself provides less formal detail here.

- **Sender communication is not uniformly forbidden by the prose.** PRL 210501-1 lists sender/receiver interaction scenarios; the expansion p. 2 expressly allows classical communication within the sender group and within the receiver group, while forbidding it across sender–receiver groups. Yet the two-receiver calculation uses a product message prior and product own-message-indexed encoder (expansion p. 7). The conservative historical formal family is the displayed independent-message family. One should not turn the introductory permission into a common-message or cross-message encoder without explaining the model extension.

- **Resource accounting is implicit beyond the given state.** The fixed dimensions and given resource provide no permission for additional shared entanglement between receivers, extra transmitted systems, or uncounted classical sender–receiver side channels. Treating those as unavailable is an inference from the resource task and LOCC scenario, not a separately enumerated ancilla theorem in the sources. Standard local decoder ancillas do not change the receiver partition. Stochastic success branches must be averaged/accounted for; discarding failures for free would change the reported information rate.

- **The bound is not the capacity.** The optimal orthogonal-unitary encoding discussed with the entropic expression optimizes the displayed upper bound. It does not prove the LOCC bound achievable for all states. PRL 210501-4 explicitly identifies looseness of Eq. (4); expansion p. 6 gives an ensemble for which the local bound exceeds the global Holevo bound. OWR p. 203's use of `Iacc` for the Holevo expression and p. 204's shorthand about an “asymptotic version” must be read alongside this distinction. A bound greater than 2 alone does not prove the W target.

- **A real printed partition-index typo.** OWR p. 204 and published PRL 210501-3 print the second marginal as a trace over `A1 ... A_(k+1) B1`. This removes one of the systems that the protocol assigns to receiver 2. The declared cut on the same PRL page is `A1 ... Ak B1 : A_(k+1) ... A_(N-1) B2`. The correct complementary trace for that declared cut is over `A1 ... Ak B1`. The later expansion p. 7, Eq. (19), prints the consistent definition. This report follows the declared laboratory cut and flags the typo rather than silently treating the erroneous marginal as a new operational model. Both original printed pages were visually inspected.

## Exact claim for subsequent comparison

A purported positive resolution must establish `C_LOCC(|W4><W4|) > 2` with the stipulated sender independence, unitary encoders, noiseless one-qubit transmissions to different receivers, fixed resource accounting, and valid asymptotic LOCC decoding across `A1B1:A2B2`. A negative resolution must cover that asymptotic class; failure of one selected alphabet, one decoder, one copy, or one zero-error codebook is insufficient. No candidate was examined here.

The strongest verified result of this audit is the source-model reconstruction above. The truth of the W capacity inequality, novelty, candidate correctness, and publication readiness remain unassessed. Source-model completeness: **100% for the inspected primary sources, with the formal gaps explicitly retained**.

## Source pins and execution custody

`SOURCE_PINS.json` records URLs, byte counts, SHA-256 values, and local copies. The source-only originals were:
- OWR 2005: 830743 bytes; SHA-256 `3afdcbb43f08c385bc603cb650616c5f0746b3695964588d694ff68831321904`.
- Published PRL author-hosted PDF: 114577 bytes; SHA-256 `1727ffc1169ce642969664a5bc8fbb01bdd5d71476c911820fb81b88ce1c74d3`.
- arXiv 0407037v3 and IAS author version: each 119655 bytes, identical; SHA-256 `f350a00d92fb419fef5dbec74f7d43ccdd3388ea52ad1bba3259ee97f50895b4`.
- arXiv 0507146v1: 181867 bytes; SHA-256 `2ee0d3ec39bd0befd2df1d00b020fd7eb55df14767009e7b7a32ca3c1c0d83ce`.
- Cited Dür–Vidal–Cirac arXiv 0005115v2: 244428 bytes; SHA-256 `98bdc1f9c3d9b87652d46b54229e7791cd940e0a861d825bc8da4004604a9cd3`.

Every successfully launched subprocess check has its actual cwd, argv, child PID, UTC start/end, exit code, and full stdout/stderr bytes under `process_evidence/<check>/`. One attempted rg search used an unavailable absolute executable: no source-check process ran. Its launch-failure record explicitly retains the missing original wrapper PID/time instead of inventing them; the retry has a complete receipt. Web-tool and image-view operations are provider calls, not local subprocesses, so no local argv/PID exists for them.

The relevant OWR contribution and all four pages of both 2004 representations were read; the complete fourteen-page later expansion was read; the cited W ket was checked at its defining primary-source section. Source extraction includes adjacent printed page material but no conclusions about neighboring research were used. No Git command, index/status operation, shared tracked-file edit, PR action, external message, upload, or outreach was performed.

