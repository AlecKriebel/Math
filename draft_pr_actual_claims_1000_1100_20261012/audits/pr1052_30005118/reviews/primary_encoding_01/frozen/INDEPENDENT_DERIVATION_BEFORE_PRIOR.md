# Independent frozen source-interface derivation

This document was written after reading only the mathematical certificate and pin manifest, before reading submitted verdicts, SOURCE_LEDGER, or prior audits. Source claims remain obligations until freshly checked. The mechanism below is my independently reconstructed argument.

## Exact hypothesis to test

For unbounded positive n supplied with an explicit subset B of C_n, ordinary self-sum recognition asks whether there exists A subset of the same C_n with A+A=B, repeated summands included. Two distinct decision languages are considered: the n-bit membership-vector language, and the binary-n/binary-residue-list language. The intended theorem is NP-completeness of each, also under odd n, nonempty B containing 0, and representatives less than n/2. The original 'efficient' question must remain qualified unless its representation and complexity measure are specified.

## Reconstructed transfer

Let nonempty integer S have minimum t. If S=R+R, fix r in R to see R finite (translation injects into finite S). Then min S=2 min R. An odd t is impossible. For even t, translating S by -t translates any root by -t/2 and is an exact integer equivalence; this works for negative t. Write B=S-t and M=max S-t. Any integer root T of B has min T=0 and max T=M/2, including 0 and lying in [0,M]. If M odd there is no such root.

Now fix odd n>2M and suppose cyclic A+A=B, with 0 in B subset [0,M]. A pair a,c in A gives a+c=0. Their doubles are mutually inverse members of B. Their representative sum is a nonnegative multiple of n smaller than n, so both doubles are 0. Odd n implies a=c=0. Thus A contains 0 and A subset B. Its canonical lifts lie in [0,M], and every lifted pair sum lies in [0,2M] strictly below n. Equality modulo n now becomes equality over integers in both inclusion directions. Conversely an integer root projects to a cyclic root. This proves the claimed equivalence and the stronger statement that every cyclic root lifts to an integer root.

The dependence on repeated summands is essential in using 2a and 2c. Oddness is essential for the asserted every-root anchor; for even n a root {n/2} of {0} is unanchored. Absence of normalization fails even for odd n: integer {1} is NO while it has singleton cyclic root in C_5.

A total map returns (3,empty) on empty S, (5,{0,1}) when min S is odd, otherwise n=max(3,2M+1), B=S-min S. The odd-minimum output is NO by the transfer: an integer root of {0,1} would contain 0, would need 1 to represent 1, and would then sum 1+1=2. Empty and diameter-zero outputs are correctly YES. For an everywhere nonempty, zero-containing target sublanguage, replace the empty-S YES output with (3,{0}); empty source remains YES. All three nonempty restricted outputs have odd n and B representatives <n/2.

## Encoding obligations and NP proof

Sparse input: let L be the total signed binary integer input length. Subtractions of L-bit integers and n=2M+1 use O(L) bits; at most |S| residues are written. Thus the transfer is polynomial in L irrespective of M's numerical magnitude. The external source theorem must actually be about finite integer sets with an unrestricted integer root, or another domain exactly equivalent to this one. Binary polynomial reducibility alone suffices for sparse hardness.

Dense input: polynomial bit length of M does not suffice. Need a source reduction from ordinary 3-SAT with N=v+c to explicitly computable S subset [0,C N^d], with fixed C,d, and formula SAT iff an unrestricted integer root exists. Then n<=max(3,2C N^d+1) is polynomial in N and the n-bit target is constructible in polynomial time. The submitted constant 2^57 and exponent 4 must be traced through the full reduction chain, not inferred from an abstract or a finite-universe definition. Root normalization of an intermediate lemma cannot be used to assume the final S contains 0.

NP: dense certificate is n bits, polynomial in dense input, and enumeration of all n^2 modular pairs is polynomial. Sparse certificate requires cardinality control: for any nonempty A fix a0, so a->a+a0 is injective into B; |A|<=|B| for every n, including n=1 and even n. A list of at most |B| canonical residues has O(|B| log(n+1)) bits. Verification forms all pairs including diagonal, sorts/deduplicates, and compares the exact target in polynomial bit time. B empty admits A empty; any nonempty A gives a nonempty pair sum and fails. Duplicates or invalid encodings can be normalized/rejected without altering the decision language.

Only unbounded n creates an asymptotic hardness claim. Each individually fixed n has finitely many B and trivial constant-table decision complexity; no uniform polynomial family follows. Exponential n in a sparse encoding is allowed and does not make dense algorithms polynomial in sparse length. The usual P iff NP conclusion follows only for deterministic polynomial-time exact decision in either explicit model, once that language is NP-complete. Search, randomized, oracle, succinct-circuit, distinct-summand, average-case, and prime-modulus claims do not follow automatically.

## Fresh primary-source obligations

1. Original printed Problem 15 must quantify both B and A inside the same cyclic group, be ordinary A+A, identify Campos/Alon/Granville, and leave efficiency definition unspecified. Inspect the complete original page and surrounding definitions, including exact symbol C_n/Z_n and attribution.
2. Pin AFWS arXiv v2 date and theorem numbering. Check integer-root domain and actual input representation from controlling body, not merely Definition 1.1's introductory notation. Confirm theorem is self-sum and not A+B.
3. Trace integer hardness through positioning, masking/skeleton, SAT gadget, and final parameter chain. Confirm polynomial constructibility and the numerical [0,2^57(v+c)^4] bound on manuscript p23 and O((v+c)^4) p2. Record which assertions are externally established rather than fully independently reproved.
4. Fixed-characteristic vector groups from Theorem 1.3 are unnecessary and do not automatically give cyclic-group hardness. Inspect only sufficiently to avoid conflation.
5. Independently inspect published SODA metadata/DOI. A failed retrieval is not evidence against a theorem. Distinguish the inspected v2 body from the published version.
6. Search controlling body for an explicit cyclic corollary and record comparative overlap, but do not infer exhaustive priority or originality from absence.

No prior audit/source-ledger conclusions have yet been read. Success requires all source obligations plus this transfer to check. A source-domain or dense-universe failure would block the corresponding theorem even if the elementary transfer is correct.
