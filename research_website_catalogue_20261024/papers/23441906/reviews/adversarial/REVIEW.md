# Independent adversarial review — Zenodo 23441906

**Verdict: PASS for the full mathematical claim in the published five-page version.** No substantive construction, simplicity, or universal nonpresentation defect was found. This is internal independent AI review, not human peer review, formal certification or a determination of historical priority.

Reviewed: *A simple brace outside asymmetric products of two trivial braces*, Alec Kriebel, v1.0.0, 17 October 2026. Completed 25 October 2026 UTC.

## Exact source and independence

The complete five-page public manuscript was read, including its model, full proofs, attribution, disclosure and references. The public archive has 79 regular files and only one embedded PDF, identical to the main PDF. Both public files, all extracted file bytes, ZIP CRC and all four retained primary PDFs were independently rechecked in `source_binding.json`.

- Main PDF SHA256: `dc8205d726236da7d61870806ed713ba329dbf4cdfdf049e5570d967d6b7e35e`.
- Verification/source ZIP SHA256: `8cc6e65647ff267cb2bd57e5ba5dda4cfc05f72ac11e527517131d9422a8d93d`.
- Main TeX SHA256: `0c1705438710c03f9f3bfba42fcda9b9c83b252394944a06fdfae032d3c1eacc`.

The first page was also rendered and inspected to confirm the precise group exponents and dimension notation displaced by text extraction. The theorem states additive group \(C_5^4\times C_2^5\) and multiplicative group \((C_5^3\rtimes_\tau C_2)\times(C_2^4\rtimes_M C_5)\).

I did not read sibling findings or historical assessment bodies. The paper itself refers to previous audits and bounded novelty investigations; those are incidental assertions, not evidence used here. Supplied programs and numerical expected outputs were inspected only after the independent proof reconstruction and fresh controls had completed. The public replay hashes the frozen historical proof and reads expected mathematical results; it does not require reading historical report prose. The current review does not claim perfectly blinded exposure, and does not adopt those historical verdicts.

## Claim and success criteria

The target is a finite **left** brace, with abelian additive group and the usual lambda action. It must be nontrivial and simple in the full ideal sense, have a metabelian multiplicative group whose Sylow subgroups are abelian, and exclude **every brace-isomorphic presentation** as an asymmetric product of two trivial left braces. A test of a particular factorization would not suffice.

The construction has 20,000 elements. No least possible order, uniqueness/classification of all counterexamples, obstruction to more than two factors, or exclusion of products with nontrivial factors is asserted or verified. The universal obstruction applies to finite two-trivial-factor asymmetric products with abelian multiplicative Sylow subgroups; it does not assert that all asymmetric products have vanishing primary triple stars.

The actual original question, Cedó's Problem9 on printed p.3228 of Oberwolfach Report51/2019, has exactly these hypotheses. They are all retained by the example.

## Universal obstruction: scope attack and reconstruction (pages 1–2)

The cited primary formulation starts with arbitrary normalized symmetric 2-cocycles, not just bilinear forms. I checked the full equations in Bachiller–Cedó–Jespers–Okniński, arXiv:1705.08493v1, Theorem3.1 and its lambda formula (printed p.6), and Cedó–Jespers–Okniński, arXiv:2001.08905v1, Theorem2.2 and surrounding preliminaries (printed pp.2–3). For trivial factors their operations are exactly the paper's
\[
(t,s)+(u,v)=(t+u,s+v+b(t,u)),\qquad
(t,s)\circ(u,v)=(t+\alpha_su,s+v).
\]
These are full primary-source restatements attributed to the original Catino–Colazzo–Stefanelli construction. I did not separately inspect that original 2016 journal article. No missing construction classification is needed: the proof works from the defining displayed operations and brace admissibility itself.

Twisted additive subtraction is
\[
(t,s)-(u,v)=(t-u,s-v-b(t-u,u)),
\]
which follows from the cocycle identity, not an illicit untwisting. Thus
\[
\lambda_{(t,s)}(u,v)=(\alpha_su,v-b(\alpha_su,t)).
\]
Because \((t,0)\circ(u,0)=(t+u,0)\), the brace identity \(\lambda_{a\circ b}=\lambda_a\lambda_b\), evaluated at \((w,0)\), forces
\[
b(w,t+u)=b(w,t)+b(w,u).
\]
Symmetry gives additivity in both arguments. This rules out the attempted escape through nonlinear symmetric cocycles: such cocycles may exist, but when the factors are trivial they are not admissible unless this additional condition holds. The argument does not assume the conclusion by restricting to a bilinear construction family.

For any prime \(p\), biadditivity kills values on mixed primary arguments, while \(b(T_p,T_p)\subseteq S_p\). Hence \(P=T_p\times S_p\) is an additive subgroup of exactly the full p-part order. Its additive law can be a non-split central twist, particularly at2; cardinality, not a direct-product isomorphism, identifies it with the additive Sylow subgroup. The action preserves the characteristic primary subgroup \(T_p\), making the same set a multiplicative subgroup of Sylow order.

Since that multiplicative Sylow is abelian, comparing \((t,0)\circ(0,s)\) with \((0,s)\circ(t,0)\) shows \(\alpha_s(t)=t\) for \(s\in S_p,t\in T_p\). Then for inputs in P,
\[
(t,s)*(u,v)=(0,-b(u,t)).
\]
Every resulting vertical element has identity lambda action on P: its first coordinate is zero, and its S-coordinate belongs to \(S_p\). Therefore \((a*b)*c=0\) for every triple in P. The proof covers arbitrary finite abelian factors, all prime powers, zero factors and different choices of coordinates. If either factor has order1 the same argument simply becomes degenerate; it creates no exception.

Brace isomorphisms preserve additive primary subgroups and both star operations. A nonzero primary triple-star value in the constructed brace therefore excludes every admissible presentation, including one unrelated to the proposed coordinates. Neither simplicity nor metabelianity is secretly needed by this lemma; the abelian-Sylow condition is essential to its proof.

Fresh boundary controls independently checked a valid \(T=S=C_2\), \(b(t,u)=tu\), identity-action product: addition is \(C_4\), multiplication is \(C_2^2\), and all64 triple stars vanish. Thus the proof did not silently assume split characteristic-two addition. A separate normalized symmetric coboundary on \(C_4\) with values in \(C_2\), derived from the function values(0,0,0,1), satisfies all64 cocycle identities but fails the requisite bilinearity/lambda-composition identity. It is not misclassified as an admissible brace. The later public replay additionally checks a genuine order-eight product with nonabelian Sylow and nonzero triple star, so the necessary hypothesis is exercised rather than omitted.

## Construction and group law (pages 2–3)

Let \(R=x\mathbb F_5[x]/(x^5)\). Its multiplication is ordinary truncated commutative polynomial multiplication. The finite formulas
\[
L(r)=r-r^2/2+r^3/3-r^4/4,\qquad
E(t)=t+t^2/2+t^3/6+t^4/24
\]
have only invertible denominators in characteristic5. All total degrees at least5 vanish, so the usual degree-at-most4 formal expansions give the inverse and circle-homomorphism identities without division by5 or an infinite convergence argument. In particular \(L(r+u+ru)=L(r)+L(u)\).

The substitution \(\sigma:x\mapsto-x\) commutes with L and fixes its fourth coefficient \(\eta(r)\), while \(\eta\) is a homomorphism for the ring circle group. The finite verification independently exhausted both inverse compositions for625 inputs and all390,625 circle-homomorphism pairs.

The even-weight binary subspace V has dimension4. Its dot form is alternating and nondegenerate: the annihilator of V in the ambient five-dimensional space is the constant line, and the nonzero constant vector has odd weight, so is not in V. The quadratic function \(Q(v)=\operatorname{wt}(v)/2\bmod2\) satisfies \(Q(v+w)=Q(v)+Q(w)+\beta(v,w)\) by the exact integer overlap formula. A five-cycle M preserves weight, beta and Q; its only fixed vector in V is zero. Hence \(M-I\) is bijective. These facts remain true at all allowed vectors, including zero.

For the displayed product, set \(e=z+Q(v)\), \(s=\eta(r)\), and write \(L(r)=(k_1,k_2,k_3,s)\). The coordinate change
\[
\Psi(r,v,z)=((k,e),(v,s))
\]
is bijective because E recovers r and Q recovers z. The first output logarithm is \(L(r)+\sigma^eL(u)\), giving \(k+\tau^eh\) and \(s+t\). The quadratic identity cancels precisely the beta term in the output e-coordinate, yielding \(e+f\). The remaining coordinate is \(v+M^sw\). Thus the full transformed product, for arbitrary inputs, is the ordinary direct product of the two stated semidirect products. This proves associativity, identity and inverses without relying on sampled associativity tests.

The lambda formula derived by actual additive subtraction is
\[
\lambda_{(r,v,z)}(u,w,Z)=((1+r)\sigma^{z+Q(v)}u, M^{\eta(r)}w, Z+\beta(v,M^{\eta(r)}w)).
\]
The first block is invertible and \(\mathbb F_5\)-linear because \(1+r\) is a unit, and the last two coordinates are an invertible triangular \(\mathbb F_2\)-linear map. There are no cross-primary additive terms. Therefore every lambda map is an additive automorphism, which is exactly the left-brace compatibility once the group law is established.

The derived group of the first semidirect factor is \((\tau-I)\mathbb F_5^3\), rank2; the second is \((M-I)V=V\), rank4. Their product is abelian of order400, and both actions are nontrivial. This establishes nonabelian metabelianity. A Sylow5 subgroup is \(\mathbb F_5^3\times C_5\), order625, and a Sylow2 subgroup is \(C_2\times V\), order32; both are abelian. Sylow conjugacy establishes the assertion for every Sylow subgroup, without incorrectly requiring these displayed subgroups to be normal.

The matching-product theorem in Bachiller arXiv:1511.08477v3, Definition4.1/Theorem4.2 and Example4.6, provides the acknowledged general framework. Its direct-sum/left-ideal scope matches this decomposition. It is not used as a substitute for the directly checked operation law or simplicity. For example, the cross-actions are \(\alpha_{(v,z)}=\sigma^{z+Q(v)}\) on R and \(\beta_r(w,Z)=(M^{\eta(r)}w,Z)\) on the binary brace; the general formula recovers the displayed lambda map. The manuscript does not claim a new general construction formalism.

## Simplicity: all ideals, not only selected subgroups (page 4)

If I is a full ideal, the permitted implications are \(\lambda_g(i)-i\in I\) and \(i*g\in I\). The second uses normality/quotient-brace structure and is not valid merely from an arbitrary left-ideal hypothesis. The primary preliminaries explicitly justify the quotient and this ideal lemma; the manuscript uses the correct stronger notion.

For a nonzero element with ring part r, the additive sixfold multiple retains r modulo5 and kills its binary coordinates. If its lowest nonzero term is \(cx^j\), the lambda difference with actor \(x^{4-j}\), for j<4, leaves exactly \(cx^4\), since higher terms vanish. For j=4 it already has this form. Rescaling yields \(a=(x^4,0,0)\).

For a nonzero purely binary element, either it is \(b=(0,0,1)\), or nondegeneracy supplies w with \(\beta(w,v)=1\), and the specified lambda difference produces b. The possibly nonzero Q(w) does not invalidate this calculation because the input has ring coordinate zero.

From b, the literal star with x is \(3x\ne0\); scalar2 recovers x and the preceding argument yields a. From a, because \(\eta(x^4)=1\), the star with a pure binary vector is exactly \((0,(M-I)w,0)\). Bijectivity supplies the whole V part, and a beta lambda difference supplies b. Thus either starting type gives both binary generators and x. Repeated lambda differences with actor x give \(x^2,x^3,x^4\). These are all nine additive generators of B, so I=B.

This is a universal finite-dimensional argument for every nonzero ideal, not a normal-subgroup search or a simulation. The fresh implementation separately derived all nine generators from each of the19,999 nonzero elements using only those permitted implications. The 31 purely binary seeds and19,968 seeds with nonzero ring part cover the entire nonzero set. Its deterministic derivation-stream hash is retained and reproducible by the script.

On the actual additive5-part, star multiplication is exactly the ring product. Consequently \(x*x=x^2\ne0\), so the brace is nontrivial, and \((x*x)*x=x^3\ne0\). Together with the universal obstruction this proves the claimed full negative answer, not just failure of the displayed coordinates to be an asymmetric product.

## Checks and custody

`fresh_controls.py` was authored from the manuscript before any submitted helper was read; it imports only the standard library. Its952,652 explicit guards passed. They include all ring-pair log identities, binary identities, the20,000-element coordinate bijection,360,000 two-sided generator product probes, all19,999 seed derivations, and the cocycle boundary controls. Generator probes alone are not claimed to establish the full group law; the arbitrary-input transformed-product proof does that. Likewise finite cocycle examples do not prove the universal exclusion.

After fresh controls, I inspected all four called public programs and the runner. The isolated, unmodified `verification/verify_all.py` replay completed with exit0 under Python3.12.14. It ran construction, obstruction, finite and symbolic programs in normal and optimized modes: eight runs. Expected mathematical results matched, including exact regenerated ideal-seed and sample-trace certificate bytes. Explicit failure guards remain active under optimization. The programs carry out factored universal polynomial identities, exact finite checks and deliberately broken controls; no enumeration of all \(20,000^3\) triples is represented as performed.

`published_replay.json` and `published_replay_receipt.json` retain the complete runner result, code hash and runtime. Separate inventories confirm original source bytes and the outer isolated mirror were unchanged; inner temporary products were disposable. No executable submitted code ran in the shared source directory. Original proof/report bytes used only for fingerprints were not treated as trusted conclusions.

One initial reviewer archive-rehash command assumed the archive names included the extraction-directory prefix; it failed to find the first file. The mapping was corrected to the actual supplied extraction root, and all79 regular files then matched exactly. This was reviewer tooling, not a manuscript/source defect. No mathematical-control failure occurred, and no published source was repaired.

## Remaining limits and strongest verified result

The strongest verified result is the full stated counterexample: the explicit order20,000 nontrivial simple left brace has the claimed groups, metabelian multiplicative group with abelian Sylow subgroups, and no isomorphic presentation as an asymmetric product of two trivial left braces under the full admissible symmetric-cocycle definition.

No substantive gap remains in that mathematical argument on this review. Basic group/brace facts and the checked primary definition interfaces remain standard background. The original2016 construction paper was checked through exact later primary restatements, not represented as separately read. No classification beyond the two-trivial-factor class, least-order theorem, exhaustive novelty determination, inaccessible recent literature implication, journal acceptance, human review or formal proof certificate is asserted. Follow-up proposal: none added.
