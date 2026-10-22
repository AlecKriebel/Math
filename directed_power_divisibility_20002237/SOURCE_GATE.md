# Source and problem-identity audit

Checked 3 October 2026.

## Original target

The original is **AIM, Definability and decidability problems in number theory, §3, Problem 3.5**, attributed to Thanasis Pheidas. The [10 December 2019 archived original](https://web.archive.org/web/20191210085514id_/http://aimpl.org/definedecide/3/) was inspected directly and agrees with the recorded statement: fixed prime p, directed relation y=p^s x, and existential decidability over Z in the language +, R_p, 0, 1.

The [live AIM page](http://aimpl.org/definedecide/3/) currently failed with a certificate-hostname error in the research browser. The exact [UnsolvedMath target](https://www.unsolvedmath.com/problems/20002237) returned HTTP 403 there. No access restriction was bypassed. The problem identity and wording were independently recovered from the archived AIM primary source; freshness of the live problem page was not verified.

The existing UnsolvedMath machine-generated report is treated as prior partial work, not as a proof of the full target. Its one-positive-atom positive-existential decision argument is credited in Attempt 2. Its prior research effort is not counted among the five new attempts here.

## Primary literature checked and distinctions retained

1. **Thanases Pheidas (1987),** An undecidability result for power series rings of positive characteristic. II, Proceedings of the AMS 100(3), 526–530. [DOI](https://doi.org/10.1090/S0002-9939-1987-0891158-2). The publisher PDF was inaccessible during this research; its relevant natural-number-domain theorem was checked through the following primary exposition, rather than falsely claimed read in the original.
2. **Leo Gitin (2024),** Undecidability of expansions of Laurent series fields by cyclic discrete subgroups. [arXiv:2408.13900v1](https://arxiv.org/html/2408.13900v1), section “Pheidas' work.” It explicitly treats (N,0,1,+,R_p). It supplies no existential definition of the nonnegative cone in the present Z-domain structure.
3. **Philipp Hieronymi, Michael Reitmeir and Xiaoduo Wang (2026),** Axiomatizations of Presburger Arithmetic With Predicates For Powers. [arXiv:2602.19602v1](https://arxiv.org/html/2602.19602v1). The predicates are unary sets of powers. Their decidability results do not define the binary variable-scaling relation R_p.
4. **Antonia Lechner, Joël Ouaknine and James Worrell,** On the Complexity of Linear Arithmetic with Divisibility. [Author-hosted paper](https://people.mpi-sws.org/~joel/publications/epad15.pdf). This is a primary complexity treatment of existential ordered additive arithmetic with ordinary divisibility. It supports the distinction that interpreting exponent addition and ordinary divisibility does not itself establish existential undecidability.
5. **Alexander Rybalov (2026),** On the Diophantine problem related to power circuits, Groups, Complexity, Cryptology 18(1), article 2, published 1 April 2026. [Paper](https://gcc.episciences.org/17806/pdf), [DOI](https://doi.org/10.46298/jgcc.2026.18.1.17270). This concerns positive integers with order and the operation (x,y)↦x·2^y. It has an explicit integer exponent input and is a different structure from the AIM target.

Targeted searches located no full resolution of the exact Z-domain directed-relation question. This is a bounded literature finding, not a claim to exhaustive coverage. The work makes no priority or global-novelty assertion for its partial lemmas.

## Not interchangeable

- Z versus N as the domain of quantified arithmetic variables.
- Directed y=p^s x versus allowing either direction, or a sign change.
- A binary scaling relation versus a unary power predicate.
- A named multiplier U=p^s versus a named exponent s connected by an exponential graph.
- Full first-order undecidability versus undecidability of the existential fragment.
- Existential formulas versus the initially positive-only one-atom fragment.

The mathematical arguments explicitly preserve all of these distinctions.
