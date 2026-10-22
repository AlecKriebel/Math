## Accepted result: dimension two only

For problem 30001058, the full original OWR Theorem 2 package, including its conditional strict alternation, and the actual lattice-polygon package have exactly the positive-integer feasible pairs
`N >= 4, m > (N+4)/(N-2)`.
The imported unconditional coefficient/root package alone admits
`N >= 3, m > (N+4)/(N-2)`.
For integer m the bound is `m >= floor((N+4)/(N-2)) + 1`.

The full-source least dilation threshold is N=4, requiring m>=5. The smallest possible multiplier m=2 first works at N=9. The nondominated full-source/polygon pairs are (4,5), (5,4), (6,3), (9,2); the unconditional package additionally admits (3,8). There is no simultaneous minimum of both coordinates.

The complete algebraic proof retains the operator derivation, positive coefficients, exact degree two, distinct negative roots, strict log-concavity, ordered root limits, attained coefficient-ratio extremum, conditional hypothesis a+b>c, and strict-boundary witnesses. Constant inputs and the actual unimodular lattice triangle establish sharpness, including the failure of strict alternation at n=3.

- [Publication guide](https://github.com/AlecKriebel/Math/blob/55410fa69d45e1be8510e38c23e1e22fa7ed7a24/unsolved_math_prioritization/attempts/30001058/README.md)
- [Complete proof](https://github.com/AlecKriebel/Math/blob/55410fa69d45e1be8510e38c23e1e22fa7ed7a24/unsolved_math_prioritization/attempts/30001058/PROOF.md)
- [Mathematical audit](https://github.com/AlecKriebel/Math/blob/55410fa69d45e1be8510e38c23e1e22fa7ed7a24/unsolved_math_prioritization/attempts/30001058/AUDIT.md)
- [Exact acceptance scope](https://github.com/AlecKriebel/Math/blob/55410fa69d45e1be8510e38c23e1e22fa7ed7a24/unsolved_math_prioritization/attempts/30001058/ACCEPTANCE.json)

## Source qualifications and review limits

The controlling source is Beck's contribution, joint with Stapledon, in Oberwolfach Report 44/2008, printed pp.2498–2500, especially Theorem 2 and Corollary 3: https://ems.press/content/serial-article-files/46191.

The related Beck–Stapledon PDF title is *On the Log-Concavity of Hilbert Series of Veronese Subrings and Ehrhart Series*, arXiv:0804.3639v3: https://arxiv.org/abs/0804.3639v3. Its normalization h0=1 differs from the controlling report's h0>=1, and its conditional hypothesis is worded differently. Jochemko's later real-rootedness result is contextual and does not replace the full-degree, strict-alternation or ratio arguments: https://arxiv.org/abs/1602.09139v2.

No result in other dimensions, current general-problem status, or novelty is claimed. This authored proof and mathematical audit do not constitute external human peer review or proof-assistant certification.

## Verification and exact publication boundary

Exactly seven sealed authored-report/public-metadata files, totaling 27,015 bytes, are added under `unsolved_math_prioritization/attempts/30001058/`. The accepted proof is byte-identical. The manifest hashes the other six files, and its independently pinned SHA-256 is `491da822eab98ff2722e35f624b764b07d2cc724279b0416e9193498db2f3dba`.

The recorded mathematical checks cover 13 symbolic identities, seven positive-cone certificates, two leading-coefficient limits, 16,200 exact regression cases, 10,915 conditional cases, seven boundary controls and 49 inverse integer-threshold checks. Normal, -O and -OO results agree. Exact finite checks support the written universal proof. Publication integrity was independently rechecked in all three modes before upload.

Source PDFs/text/images, scripts, raw regression tables, datasets and private coordination/control files are excluded. Source pins retain public bibliography, PDF identities and qualified inspection/retrieval history. No source-author code was executed. QUEUE.md and all unrelated content are unchanged.

Base: `5c5d4c9d7a2ea547fdf8a35cf874f604cec27bed`.
Exact proposed head: `55410fa69d45e1be8510e38c23e1e22fa7ed7a24`.
This is an open draft for review; no merge, release, submission or outreach is included. Local verification is distinct from GitHub CI.
