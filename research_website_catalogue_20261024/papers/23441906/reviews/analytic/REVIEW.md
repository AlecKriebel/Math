# Independent analytic review — Zenodo 23441906

**Verdict: PASS for the exact mathematical theorem.** The published construction satisfies every hypothesis of Cedó’s stated question, and its primary triple-star invariant excludes every admissible asymmetric product of two trivial left braces, up to brace isomorphism. No substantive mathematical defect was found. This is an AI review, not human peer review, a formal proof certificate, a priority certificate or publication authorization.

## Reviewed object and independence

The complete five-page published PDF, its complete `main.tex`, the original mathematical support `audit/inputs/PROOF.md`, and all four mathematical verification programs plus their runner were read. All five rendered PDF pages were inspected. The public PDF has SHA256 `dc8205d726236da7d61870806ed713ba329dbf4cdfdf049e5570d967d6b7e35e`; the source ZIP has SHA256 `8cc6e65647ff267cb2bd57e5ba5dda4cfc05f72ac11e527517131d9422a8d93d`. The ZIP has 79 regular files and a byte-identical embedded main PDF, with no other reader PDF.

The exact theorem constructs a finite, nontrivial, simple **left brace** of order 20,000, with additive group \(C_5^4\times C_2^5\) and multiplicative group
\[
(C_5^3\rtimes_\tau C_2)\times(C_2^4\rtimes_M C_5).
\]
Its multiplicative group is metabelian and all its multiplicative Sylow subgroups are abelian. The conclusion excludes asymmetric products with **two trivial factors**, not arbitrary matched products, products with nontrivial factors, or every conceivable extension construction. No minimum-order assertion or classification of all counterexamples is proved.

I reconstructed the main arguments and completed fresh controls before reading the packaged mathematical helpers. The fresh simplicity control uses 187 prime-projective directions and a span-closure algorithm rather than the submitted 19,999-seed propagation scripts. It uses explicit coefficient expressions for logarithm/exponential and a four-bit chart for the even-weight space. No sibling report or dedicated historical assessment body was read. The manuscript and necessary original proof contain previous audit/acceptance assertions; those were unavoidable incidental exposure and were not used as evidence. Linked historical assessment files were not opened. Reproduction compares numeric computation outputs and certificate bytes, not scholarly verdicts.

## Original problem and the exact product definition

Cedó’s contribution to Oberwolfach Report 51/2019, printed pages 3226–3228, defines the standard left-brace notions and asks Problem 9 with exactly the finite, nontrivial, simple, metabelian and abelian-Sylow hypotheses used here. The question is about two trivial **left** braces. The theorem does not answer a weakened version with fewer group hypotheses. [Original problem](https://ems.press/content/serial-article-files/46831)

The full symmetric-cocycle asymmetric-product operations and admissibility condition were checked in Bachiller–Cedó–Jespers–Okniński, Theorem 3.1 and equation (2), and independently in Cedó–Jespers–Okniński, Theorem 2.2. With both factors trivial, the operations are exactly the paper’s equations (1)–(2). These primary bodies also distinguish the general symmetric cocycle from the special biadditive case. Thus the exclusion is not silently limited to a preferred family of bilinear examples. [2017 primary formulation](https://arxiv.org/pdf/1705.08493v1), [2020 primary formulation](https://arxiv.org/pdf/2001.08905v1)

The ideal definition, quotient-ideal implication, and lambda-map conventions agree with these primary sources and Bachiller’s definitions. The latter’s matched-product Theorem 4.2 is background: the published direct group-law argument does not depend on importing a simplicity or existence theorem for a matched-product family. I inspected its statement and relevant definitions rather than treating that citation as a proof of the present result. [Bachiller, inspected edition](https://arxiv.org/pdf/1511.08477v3)

## Universal obstruction reconstructed

For a normalized symmetric cocycle, the twisted additive subtraction formula follows directly by adding the proposed difference to the subtrahend. It gives
\[
\lambda_{(t,s)}(u,v)=(\alpha_su,v-b(\alpha_su,t)).
\]
Because the multiplication of \((t,0)\) and \((u,0)\) is \((t+u,0)\), lambda composition applied to \((w,0)\) gives
\[
b(w,t+u)=b(w,t)+b(w,u).
\]
Symmetry then supplies biadditivity in the other argument. This uses actual brace admissibility, not just the cocycle identities. A symmetric nonbilinear cocycle can define an abelian additive extension while failing the brace condition; the fresh carry-cocycle control exhibits exactly that boundary.

For finite abelian factors, bilinearity kills mixed-primary values and sends \(T_p\times T_p\) into \(S_p\). Consequently \(P=T_p\times S_p\) is closed under the twisted addition and has the full p-part of the total order. It is therefore the unique additive p-primary subgroup. This argument does not identify its addition with a direct product: at p=2 the addition can have higher exponent. The same set is closed under the semidirect multiplication and is a multiplicative Sylow subgroup. Finite factors are automatic if their Cartesian product is finite.

Commutativity of this multiplicative Sylow subgroup forces \(\alpha_s(t)=t\) for \(s\in S_p,t\in T_p\). Thus, using twisted subtraction rather than coordinate subtraction,
\[
(t,s)*(u,v)=(0,-b(u,t))\quad\text{on }P.
\]
Every element of \(\{0\}\times S_p\) has identity lambda action on P, proving \((a*b)*c=0\) there. Simplicity and metabelianity are unnecessary for this lemma. They are separately required by the original problem and separately verified for the example.

A brace isomorphism is an isomorphism of the additive groups and preserves the star operation. It must carry each unique additive p-primary subgroup to the corresponding subgroup. A nonzero primary triple star therefore obstructs **all** such presentations and all possible alternative choices of factors and coordinates; checking a list of proposed decompositions would have been inadequate.

## Construction and the two groups

The nilpotent ring \(R=x\mathbb F_5[x]/(x^5)\) has four coefficients. Its logarithm and exponential terminate in degree four; every required denominator is invertible modulo five. There is no fifth-degree denominator or convergence assumption. Expanding gives, for \(r=ax+bx^2+cx^3+dx^4\),
\[
L(r)=(a,\ b+2a^2,\ c+4ab+2a^3,\ d+4ac+2b^2+a^2b+a^4).
\]
The inverse expansion is
\[
E(r)=(a,\ b+3a^2,\ c+ab+a^3,\ d+ac+3b^2+3a^2b+4a^4).
\]
These expressions and all 625 squared ring pairs were checked independently. The universal truncated formal identities imply that L carries \(r+u+ru\) to \(L(r)+L(u)\). Substitution \(x\mapsto-x\) commutes with L and preserves its fourth coefficient \(\eta\).

The even-weight subspace of \(\mathbb F_2^5\) has dimension four. Its dot form is nondegenerate because its orthogonal complement in the full five-space is the constant line, whose nonzero vector has odd weight. The half-weight quadratic function has polar form beta by the integer weight identity. The five-cycle preserves both, and its only fixed vector in this subspace is zero. Thus \(M-I\) is invertible.

The map \(\Psi\) built from the first three logarithm coefficients, \(e=z+Q(v)\), v and the fourth logarithm coefficient is bijective. Under the paper’s multiplication, the logarithm of the ring coordinate becomes \(L(r)+\sigma^eL(u)\), the new e-coordinate is \(e+f\), and the V-coordinate is \(v+M^sw\). These are exactly two ordinary semidirect-product laws, proving associativity and inverses for all inputs. It would be invalid to infer associativity from generator-pair tests alone; here the symbolic identity supplies the universal argument.

The lambda map then has an invertible linear ring block \((1+r)\sigma^e\) over \(\mathbb F_5\) and an invertible triangular binary block over \(\mathbb F_2\). The inverse of \(1+r\) is the finite geometric expression \(1-r+r^2-r^3+r^4\). Hence every lambda map is an additive automorphism, proving the left-brace identity.

The commutator subgroup of a semidirect product of two abelian groups is the image of the action differences. Here \(\tau-I\) has rank two and \(M-I\) has rank four, giving derived group \(C_5^2\times C_2^4\) of order 400. It is abelian and nonzero, so the group is nonabelian and metabelian. Taking \(C_5^3\times C_5\) and \(C_2\times C_2^4\) across the two direct factors gives Sylow subgroups of orders 625 and 32; both are abelian. Sylow conjugacy supplies the assertion for every Sylow subgroup. Neither subgroup is assumed normal.

## All-ideal simplicity and the decisive triple

Both closure rules in the proof are justified for an ideal I. Lambda invariance gives \(\lambda_g(i)-i\in I\). Normality gives the second rule directly: put \(j=g^{-1}\circ i\circ g\in I\), so \(i\circ g=g\circ j=g+\lambda_g(j)\), and therefore
\[
i*g=\lambda_g(j)-i\in I.
\]
This verifies the quotient-brace inference without assuming that an arbitrary left ideal has the same property.

For a nonzero ring component, multiplying the additive element by six isolates that component unchanged. Multiplication by the complementary ring monomial via a lambda difference then isolates its lowest nonzero coefficient in degree four; rescaling produces \(a=(x^4,0,0)\). If only a binary component remains, nondegeneracy of beta produces \(b=(0,0,1)\), including the separate case v=0.

The two bridges are valid: \(b*(x,0,0)=(3x,0,0)\) produces a nonzero ring element, while \(a*(0,w,0)=(0,(M-I)w,0)\) produces every V-vector. A binary lambda difference gives b, and successive lambda differences using x produce \(x^2,x^3,x^4\). Thus every nonzero ideal contains all nine additive generators. This covers non-coordinate and mixed-primary ideals, not merely selected subspaces.

On \(P_5\), star is ring multiplication. The square x*x is nonzero, showing nontriviality, and the left-associated triple \((x*x)*x=x^3\ne0\) contradicts the universal product lemma. No associativity of star is assumed outside this ring subbrace.

## Additional mathematical support

The original `PROOF.md` includes redundant fixed-set, multiplicative-center and derived-star checks. They are not needed for the five-page theorem, but I checked their actual scope independently rather than reading their linked archived audit.

For a nontrivial simple two-trivial-factor product, \(\ker\alpha=0\) and the radical of b is zero: each otherwise supplies a proper nonzero ideal. Let \(C=\sum_s(\alpha_s-I)T\). The map to the trivial brace T/C has kernel C times S, so simplicity forces C=T. Consequently the multiplicative derived subgroup is T times zero and the globally lambda-fixed set is zero times S, a complement. Invariance of b then gives \(T^\alpha=0\), since a fixed t is orthogonal to C=T. The multiplicative center is therefore trivial in this specific class. These conclusions are not claimed for all simple braces.

For the proposed B, the global lambda-fixed set is \(\mathbb F_5x^4\times\{0\}\times\mathbb F_2\), of order ten, whereas the multiplicative abelianization has order fifty. Its center has order five, represented by \(E(cx^2)\); in particular \(x^2+3x^4\) is central. The stated commutator has logarithm x and equals \(E(x)\), and its two successive ring-star products are \(x^2+3x^3+x^4\) and \(x^3+3x^4\). The submitted replay also checks these exact witnesses. These are consistent redundant obstructions, not missing repairs to the main proof.

## Fresh controls and replay

`fresh_controls.py` and its JSON outputs preserve the independent controls:

- All 625 ring inputs and 390,625 ring pairs check log/exp and the ring homomorphism; all 16 V elements check the binary ingredients. All 20,000 elements check the coordinate bijection and both-sided inverses; 180,000 generator-pair transports are supplemental.
- Any nonzero ideal contains a nonzero prime-primary line. There are 156 lines in \(\mathbb F_5^4\) and 31 in \(\mathbb F_2^5\). A separate linear-span closure from each of these 187 directions, using only valid ideal consequences, reaches ranks (4,5). Receipts retain every direction and its rank-growth events.
- The non-split C4 additive extension satisfies the triple-zero invariant. An order-eight asymmetric product using an alternating binary form and a unipotent action is a genuine brace with nonabelian multiplicative Sylow subgroup and a nonzero triple; this confirms the importance of that hypothesis. A C3 carry cocycle passes the additive-extension test but fails the brace identity, checking the admissibility boundary.
- Removing the sign action strands the binary scalar line; removing the rotation strands the ring part. These deliberately broken controls fail the full-rank propagation conclusion.

The fresh script initially encountered a Python3.9 missing `bit_count` method, corrected with an exact bit count. Its first expectation for the no-sign mutation predicted the whole binary part; the actual closure is the smaller scalar line, still a proper ideal. Neither was a counterexample to the published construction. Both corrections are disclosed in the log.

After these controls, all four packaged mathematical programs and the runner were read in full. The unmodified runner passed all four programs in ordinary and optimized modes under Python3.12.14: eight runs total, in isolated copies. Numeric results matched; the regenerated 19,999-seed certificate and sample-trace files matched the published byte hashes. The runner checks for optimization-sensitive assertions, and the submitted programs use explicit failure guards. All 79 source files remain unchanged.

No computation enumerates all 20,000 cubed brace-law triples or all possible product presentations. Factored exhaustive identities, exact seed derivations and boundary examples supplement the universal proofs. Historical expected PASS fields are not a substitute for the new run or the mathematical reading.

## Exact remaining limits

No substantive proof gap was found for Theorem 1 or its all-admissible-two-trivial-factor scope. The core proof is elementary and direct once the correct product definition is fixed; it does not rest on an unavailable classification theorem.

Primary-reading coverage is deliberately bounded: the original OWR problem and full relevant generalized product interfaces were checked, plus basic/matched-product interfaces in Bachiller. I did not independently audit the entire Catino–Colazzo–Stefanelli journal body, all later construction papers, the cited 2026 literature, every final journal edition or the manuscript’s historical novelty search. Those are not imports needed for the displayed proof. No first-priority claim, minimum-size claim, human-referee assessment or proof-assistant certification follows from this PASS.

**Strongest supported result:** the explicit order-20,000 brace answers the precise original question negatively, including exclusion under every brace-isomorphic admissible two-trivial-factor presentation. This analytic assignment is 100% complete.
