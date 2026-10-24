# Independent adversarial audit: normal doubles

Reviewer: `/root/p21126_superexp/double_adversary`; completed independently of the author. UTC: 2026-10-24T21:20:45.492500+00:00.

**Outcome: PASS for the explicitly stated partial construction and upper-bound filters.** This is neither a solution of either branch of 21.126 nor an originality certificate. The exact current input is recorded in REVIEWED_INPUTS.json. The virtual-passage clarification added during review was read and verified.

## Reconstructed algebraic injection

Write D=G*_N G. The amalgam normal-form theorem first ensures that N embeds. It is normal in D because both vertex groups normalize it. Its quotient has the universal property of (G/N)*(G/N), so the kernel of the quotient map p:D→Q*Q is exactly N, rather than a larger unidentified normal closure. The fold f is the identity on N. Thus an element killed by both f and p lies in N and is killed by an injective restriction of f, hence is trivial. No splitting, residual finiteness, finite generation, or presentation of N enters this argument.

The proposed RAAG target is an actual target: disjoint union of defining graphs gives a free product of RAAGs, and join gives direct product. The two given embeddings of G and Q therefore give an embedding of D into that product RAAG. The quotient homomorphism G→Q need not be induced by a graph map. For virtual embeddings, intersect the injection with a finite-index RAAG-embeddable subgroup of the ambient product. Replacing both vertex groups separately by a finite-index subgroup does NOT automatically give a finite-index amalgam, and the revised text correctly disclaims that shortcut.

Finite presentability of D uses two finite vertex presentations plus the finitely many identifications of generators of N. Every element of N is a word on those generators, so these finitely many relations identify all of N. Finite presentation of N is not required.

## Quotient reduction and distortion

The graph-product deletion condition gives an inverse pair in any nonempty identity word such that the intervening letters commute with its underlying generator. Choose a pair without an intervening occurrence of that same generator, if necessary. Moving one member through the intervening block and cancelling never increases length. Repeating uses at most m/2 cancellations and at most m^2 commuting swaps. For the free product Q*Q, the defining graph is a disjoint union, so every allowed swap is internal to one factor. Cross-factor commutations are never assumed.

I reconstructed the kernel estimate with a separate bookkeeping form. Let K(n)=n+M n^2 and S_n=1+L+...+L^n. Each original N-letter, and each of at most n^2 quotient-relator corrections of initial N-length at most M, is conjugated by a T-prefix of length at most n. Iterating the finitely many conjugation substitutions costs at most its initial length times S_n and produces at most its initial length times L^n letters. Hence the final N-word has length at most K(n)L^n. All prefixes consist of surviving original T-letters; collecting correction words at the left does not lengthen them. This rules out an unaccounted exponential in the quotient's quadratic area.

The argument works for non-split extensions and for infinitely related N. L≥2 and M≥1 handle empty or trivial families. Trivial N, trivial Q, free Q, and free-abelian Q introduce no exceptional case.

## Intrinsic area reconstruction

For the double, all N-generators are common and there are two copies of T. Each conjugation substitution is a cell of one of the copied finite G presentations, after the finitely many true conjugation and signed commutator relations have been added. There are at most n^2 signed swapping cells. The remaining rewriting area is bounded by K(n)S_n, up to a fixed factor. Thus it is an ordinary exponential in n.

The resulting word W is a word on N-generators with length at most K(n)L^n. Since the original word is null in D, the fold gives W=1 in G. Filling it in the FIRST COPY of G is a legitimate filling inside D, at area δ_G(|W|). That filling may use T-letters internally. There is no attempt to fill W using a finite presentation of N, which is why the absence of finite presentability of N is harmless. Absorbing polynomial factors into an exponential gives exactly the claimed form

    δ_D(n) ≤ C exp(Cn) + C δ_G(exp(Cn)).

For polynomial-Dehn G this is at most an ordinary exponential. For exponential-Dehn G it only permits a double-exponential upper bound and proves no matching lower bound. The note correctly distinguishes these outcomes.

## Attempted falsifications and scope limits

I tested the logical points where a false double argument usually enters: kernel versus normal closure, non-normal amalgamated subgroups, unsplit quotient lifts, illicit cross-factor commutations, unbounded conjugating prefixes, finite presentation of the kernel, and finite-index passage. Under the displayed hypotheses none yields a counterexample. Dropping normality breaks the first injection proof; replacing the RAAG quotient by an arbitrary RAAG subgroup does not preserve its length-nonincreasing quotient reduction in intrinsic generators. These are genuine excluded cases, not proved extensions.

This review audits the explicit elementary proofs, not the entire preliminary literature audit or all Rips construction theorems. No lower bound, exotic Dehn function, new solution, publication readiness, or priority claim is approved.
