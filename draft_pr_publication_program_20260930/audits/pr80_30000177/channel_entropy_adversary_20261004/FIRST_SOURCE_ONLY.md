# FIRST: source-only model and calibration

Frozen on 2026-10-04 before opening candidate or author code. No author review, SOURCES, priority judgment, sibling conclusion, or ROOT mathematical conclusion was read. Audit completion estimate: 20%.

## Target and byte identity

Target supplied by ROOT: OWR-785-003, problem30000177, whether the four-qubit W state belongs to the LOCC dense-codeable class. Original/current submitted head: dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3. The supplied historical ledger is literally claimed_solved, 1/5; it is outside this audit's mutation scope.

Primary PDFs are independently byte pinned in SOURCE_PINS.json and extracted with subprocess receipts. The report: 830743 bytes, SHA256 3afdcbb43f08c385bc603cb650616c5f0746b3695964588d694ff68831321904. Bruß PRL 93, 210501 (2004): 114577 bytes, SHA256 1727ffc1169ce642969664a5bc8fbb01bdd5d71476c911820fb81b88ce1c74d3. Its arXiv v3: 119655 bytes, SHA256 f350a00d92fb419fef5dbec74f7d43ccdd3388ea52ad1bba3259ee97f50895b4. Bruß arXiv quant-ph/0507146v1 (2005): 181867 bytes, SHA256 2ee0d3ec39bd0befd2df1d00b020fd7eb55df14767009e7b7a32ca3c1c0d83ce. The 2005 PDF's later typesetting timestamp is not treated as its publication date; the arXiv version/date is on p.1.

Report printed pp.203-205 (PDF pages 19-21), PRL pages 3-4, and Bruß2005 classification pages 9-10 were rendered and visually inspected. The exact target is present on printed p.205. The report gives general routing/asymptotic capacity on p.204. PRL p.4 identifies the four-party W state and says it is not locally dense codeable. Bruß2005 Secs.6-7 explicitly describe routing and shell distinctions.

These sources name W rather than printing its normalized four-qubit vector. PRL reference [23] identifies Dür, Vidal, Cirac, PRA 62, 062314 (2000). I independently fetched their primary arXiv quant-ph/0005115v2 (unversioned URL returned v2): 244428 bytes, SHA256 98bdc1f9c3d9b87652d46b54229e7791cd940e0a861d825bc8da4004604a9cd3. Sec.V.B, Eqs.(29)-(31), explicitly defines the symmetric N-qubit single-excitation W family and four-qubit member. An initially attempted v3 fetch failed; its failed receipt is preserved and contributed no source content. Primary links: https://doi.org/10.1103/PhysRevLett.93.210501 ; https://arxiv.org/abs/quant-ph/0507146 ; https://arxiv.org/abs/quant-ph/0005115 .

## Exact model established from primary sources

Tensor order A1,A2,B1,B2. The normalized pure resource is

    |W4> = (|1000> + |0100> + |0010> + |0001>)/2.

Two distant senders apply local unitaries to A1 and A2, encoding independent classical indices with product probabilities. Each sends exactly its one-qubit share noiselessly: A1 to B1 and A2 to B2. After transmission, receiver bipartition is L=A1B1 and R=A2B2. Local decoding within L and within R, plus classical communication between receivers, is permitted. Sender-to-receiver classical communication and sender/receiver preprocessing communication are excluded because they transmit the measured commodity. No extra entanglement or receiver-to-receiver quantum communication is supplied.

Capacity is an asymptotic number of classical bits per shared state, equivalently per pair of sent qubits here. The source permits product encoding across copies and collective receiver decoding. A one-copy cq Holevo value does not itself certify one-shot accessible information. Independent messages must satisfy the classical-to-quantum multiple-access coding rate constraints; replacing them with an unconstrained common encoder needs justification.

The strict usefulness threshold is 2 bits, not 1 bit or a conditional successful-branch threshold. In the source shell convention, LOCC-DC means C_LOCC>2 and absence of LO-DC. An advantage over an arbitrary weak measurement is insufficient. Bruß2005 Eq.(26) excludes LO-DC from this shell. Eq.(22) defines the no-communication rate as the sum of two local resource capacities; Eq.(23) gives the global upper bound. Eq.(21) is an LOCC upper bound, not a general achievability theorem.

## Independent exact marginal calculation

Define h(p)=-p log2(p)-(1-p)log2(1-p). Every one-qubit marginal is diag(3/4,1/4), entropy h(1/4). Every two-qubit marginal is (1/2)|00><00|+(1/2)|psi+><psi+|, where |psi+>=(|01>+|10>)/sqrt(2). Its spectrum in dimension 4 is (1/2,1/2,0,0), entropy 1. Direct tracing proves this: excitations outside the retained pair give |00> weight 1/2; retained excitations add coherently. Thus L and R marginals have that spectrum. The full state is rank one, entropy zero; B1B2 has entropy 1.

In the original unitary resource convention:

    C_LO = 2+2h(1/4)-2 = 1.6225562489182659 < 2,
    C_G = 2+S(B1B2)-S(W) = 3,
    B_LOCC = 2+2h(1/4)-1 = 2.622556248918266.

If a classical fallback that discards the resource is included, its rate is 2 and still not strictly greater than 2. The original papers name resource capacities without that max-with-classical convention; this distinction must be preserved.

source_calibration.py is an independently authored exact rational checker. It verifies normalization, idempotence, all four single marginals, all six pair marginals, eigenvectors including zeros, and all 24 tensor permutations. Its actual execution is preserved under process_evidence/source_calibration, using -E -B, active assertions, full stdout/stderr, PID, UTC, argv, cwd, and prelaunch source snapshots.

## Falsifiable audit criteria fixed before candidate exposure

A successful candidate must define a complete physical local instrument, count every branch with correct probability/normalized state, preserve routing, and obtain a strict asymptotic rate above 2 with product local sender encodings. It must justify entropy dimension/multiplicity, handle zero blocks without spurious logarithms, and identify receiver-to-receiver classical outcome communication. It must explain n-copy tensor extension and the coding theorem. Postselection, joint receiver quantum operations, extra entanglement, or turning an entropy upper bound into capacity without justification would fail. LO exclusion is separately calibrated above. No fresh proof search is authorized.
