# Independent audit of cyclic sumset recognition

Date: 2026-10-09. Problem: 30005118 / OWR-10252930-031.

## Verdict

**ACCEPT.** The certificate establishes that same-group cyclic self-sumset recognition is NP-complete in both the explicit sparse binary encoding and the dense characteristic-vector encoding. This is a rigorous consequence of the published integer hardness theorem and the certificate's elementary transfer. It does not establish an unconditional impossibility of polynomial-time recognition: such recognition exists if and only if P=NP.

This standalone edition retains the full mathematical audit. ACCEPTANCE.md identifies the exact certificate and audit editions included here.

The entire original certificate was read for the independent review. No mathematical correction is required. This report independently checks the transfer and its complexity accounting; it does not independently reprove the cited paper's complete gadget construction or certify novelty.

## Target and source verification

The original target was checked against the actual OWR PDF, with independent page extraction and rendering of PDF page 64, printed page 1228. Problem 15 asks about B=A+A with both sets in the same group Z/nZ. Marcelo Campos communicates the question, attributing it to Alon and Granville. The report does not fix an encoding or define the word efficient. Its ordinary self-sumset notation permits repeated summands. The neighboring graph conjecture is unrelated and is not part of this target. [Official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3964/OWR_2022_22.pdf?isAllowed=y&sequence=4)

The mathematical dependency is Theorem 1.2 of Abboud, Fischer, Safier, and Wallheimer, *Recognizing Sumsets is NP-Complete*. Theorem 1.2 on manuscript page 2 establishes integer NP-completeness; its final reduction on page 23 constructs S in [0,2^57(v+c)^4] from 3-SAT with v variables and c clauses, preserving satisfiability. The exponent 57 was checked visually, avoiding the flattened text extraction's ambiguous appearance. Page 8's intermediate normalization was also inspected; it need not imply that the final source output has minimum zero. The certificate correctly supplies its own normalization. The inspected manuscript is arXiv v2, dated 26 October 2024. [Pinned manuscript](https://arxiv.org/abs/2410.18661v2)

The publisher independently confirms SODA 2025, pages 4484-4506, DOI 10.1137/1.9781611978322.153, published online on 7 January 2025. The older arXiv comment describing the paper as forthcoming does not override that published record. The arXiv version supplies the inspected proof text; a separate page-by-page audit of the publisher's typeset full text was not performed. [SIAM publication record](https://epubs.siam.org/doi/10.1137/1.9781611978322.153)

## Mathematical checks

1. **Integer normalization is exact.** For a nonempty finite S=R+R, finiteness of R follows by injecting a translate of R into S, and min S=2 min R. Odd minima are therefore impossible. For even t=min S, translation of the root by -t/2 gives an exact equivalence between S and B=S-t. This works with negative minima. Any integer root of normalized B has minimum zero and maximum M/2, where M=max B.

2. **The zero-anchor converse is sound.** Suppose B contains zero, lies in [0,M], n is odd, and n>2M. A cyclic root contains a and -a because it represents zero. The canonical representatives of 2a and -2a both lie in B. Their sum is divisible by n but lies in [0,2M], so both representatives are zero. Oddness forces a=0. Thus the root contains zero and is a subset of B. All its ordinary pair sums are smaller than n, so its cyclic sumset equality is an integer equality. This checks both directions, not only the easier forward reduction.

3. **Every reduction branch is valid.** Empty S maps to a fixed YES instance. Odd min S maps to {0,1} in Z/5Z, a NO instance: the anchor lemma would put any root inside {0,1}, while representing 1 would force 1 into the root and hence force the absent sum 2. An even minimum uses n=max(3,2M+1), which is always odd and greater than 2M. M=0 gives {0} in Z/3Z. The construction needs no prime search or factorization.

4. **The stated restricted hardness is supported.** The usual normalized outputs have odd n, contain zero, and lie strictly below n/2. To require these restrictions for every output, replace the empty-source YES output by (3,{0}), as explicitly allowed in the certificate. That substitution preserves YES/NO status. The fixed NO output also satisfies all restrictions. Thus the empty branch does not invalidate the certificate's opening restricted-hardness claim.

5. **No unsupported group substitution occurs.** Fixed-characteristic vector groups need not be cyclic. The certificate does not use that mistaken implication. Its same-group cyclic conclusion follows from the integer theorem and the proved lemma.

## Encoding and complexity checks

For sparse input, n and the explicitly listed residues are binary integers. Subtraction, parity, and forming 2M+1 increase the source bit length by only a polynomial amount. At most the original number of listed elements is output. This gives a polynomial many-one reduction from the sparse integer problem.

For dense input, expanding a general binary integer range into a characteristic vector is not necessarily polynomial. The certificate correctly avoids that argument. It composes the transfer directly with the 3-SAT construction's numerical bound U=2^57(v+c)^4. Here M<=U and n<=max(3,2U+1), so writing n bits is polynomial in formula size. Constant branches and the empty formula are handled separately.

Sparse NP membership is also justified independently. When B is nonempty, a root A has size at most |B|, since a fixed translate of A injects into B. A certificate thus uses O(|B| log(n+1)) bits, and the verifier can compute and compare all at most |B|^2 modular sums in polynomial bit time. For empty B it accepts the empty root. Dense membership follows from an n-bit root and polynomial pair checking. These verifiers work for every positive n, including even n and n=1.

Together, these facts prove the two NP-completeness conclusions and the corresponding equivalences with P=NP. The proof concerns unbounded input n. It makes no claim about restricted summands, two independently chosen summand sets, circuit or oracle descriptions of B, randomized algorithms, average-case complexity, or new hardness gadgets.

## Source integrity

- OWR source PDF: 655,364 bytes; SHA-256 `a0622a6a42add0931f7b1d005157fb499122b8934ce0591f7c9cad684cd5f9ea`.
- Hardness manuscript PDF: 616,293 bytes; SHA-256 `89e6d1eb1b539ea58d463ba1b83cc5d71519055de36cc079398bdb918441a808`.

The exact editorial scope is documented in PROVENANCE.md. Acceptance concerns the retained universal argument and its stated mathematical dependency. No third-party source bodies are distributed.
