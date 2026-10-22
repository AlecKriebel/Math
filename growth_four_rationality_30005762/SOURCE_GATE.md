# Source gate: Rationality Below Growth Rate Four

Audit date: 2026-10-21 UTC. Ordered row 1854; ID 30005762; source key OWR-14298158-007.

## Decision

**SOURCE GATE PASSED; general conjecture remains open in the primary literature located.** There is substantive newer partial progress: Brignall–Opler announced rationality for finitely based classes of upper growth rate strictly below (3+sqrt(5))/2 at Permutation Patterns 2025. This audit does not claim a proof of the full below-four conjecture, and does not promote a conference announcement into a verified published proof.

## Exact target

Robert Brignall's item 6 in the open-problem session of [Mini-Workshop: Permutation Patterns, OWR 6/2024](https://doi.org/10.4171/owr/2024/6), printed p.286, asks whether every finitely based permutation class with growth rate strictly less than 4 has a rational ordinary length generating function. The source page was visually inspected. The 2025 conference abstract dates the conjecture to Permutation Patterns 2023, so 2024 is the report year, not necessarily first formulation.

Here C is a downset under classical permutation-pattern containment, C=Av(B) with finite basis B. Its counting series is F_C(x)=sum(n>=0)|C_n|x^n. “Rational” means F_C(x) belongs to Q(x), not that its exponential growth constant is rational. Heredity under taking patterns is part of the definition; an arbitrary set of permutations is not sufficient.

The report uses “growth rate” without a local formal definition in item 6. To avoid silently assuming a limit exists for every finitely based class, the robust formulation uses upper growth limsup(n→infinity)|C_n|^(1/n)<4; if the proper growth limit exists, it agrees. The 2025 theorem explicitly uses upper growth. The general existence-of-growth-rate question must not be smuggled in as a theorem.

No sum-closure, skew-closure, substitution-closure, well-quasi-ordering, finite number of simple permutations, or restriction to separable permutations is assumed. Sum-closed and skew-sum-closed auxiliary classes occur in the 2025 proof outline, not as hypotheses on C.

## Strict boundary and finite-basis safeguards

The threshold is strictly below 4, not at most 4. The finitely based class Av(132) has Catalan series (1-sqrt(1-4x))/(2x), is nonrational, and has growth 4. Thus the non-strict variant is false even in the separable, finite-simple setting. This example is a boundary check, not a counterexample to the conjecture.

Finite basing cannot simply be discarded: [Albert–Ruškuc–Vatter, Inflations of geometric grid classes of permutations](https://arxiv.org/abs/1202.1833), Theorem 8.5, proves rationality for every class below kappa≈2.20557 and explains that the unrestricted threshold is sharp: nonrational classes already occur at kappa. Kappa is the positive root of x^3-2x^2-1. The published paper is [Israel Journal of Mathematics 205 (2015), 73–108](https://doi.org/10.1007/s11856-014-1098-8). The strict sub-kappa theorem is not a solution to the finitely based sub-four conjecture.

Finite simple permutations imply algebraicity, not rationality in general; Catalan classes already demonstrate the difference. Well-quasi-ordering is likewise not a general rationality criterion. [Brignall–Vatter, Uncountably many enumerations of well-quasi-ordered permutation classes](https://arxiv.org/abs/2211.12397), revised September 2025 and published in 2026, disproves a separate general wqo/algebraicity expectation. It does not remove finite basing from this conjecture.

## Verified partial results and source correction

1. Separable classes: [Albert–Atkinson–Vatter, Subclasses of the separable permutations](https://arxiv.org/abs/1007.1014), Theorem 4.1, gives strong rationality if C⊆Av(2413,3142) contains none of Av(132), Av(213), Av(231), Av(312). Every separable class of upper growth <4 necessarily meets that condition, since each excluded subclass has growth 4. Thus the separable below-four case is already established.
2. Monotone length-three avoidance: [Albert–Brignall–Ruškuc–Vatter, Rationality for subclasses of 321-avoiding permutations](https://arxiv.org/abs/1602.00672), Theorem 1.1, proves rationality for every **proper** subclass of Av(321) that is finitely based **or** well-quasi-ordered. Reversal transfers this to Av(123). The OWR evidence bullet on p.287 omits “proper”; that omission must be corrected, since Av(123) itself is finitely based and Catalan/nonrational. Below 4, properness is automatic for a subclass of Av(123).
3. General finite-basis advance: Brignall's [official PP2025 abstract, printed p.35](https://sites.cs.st-andrews.ac.uk/pp25/program/booklet-pp25.pdf), announces joint work with Michal Opler establishing rationality when upper growth is strictly below Phi=(3+sqrt(5))/2≈2.618034. It explicitly states that the below-four conjecture is still open and explains that parts of the method do not extend beyond Phi. The [7 July 2025 slides](https://www.rbrignall.org.uk/talks/2025-07-07-PP25.pdf) also state the result and label the underlying work “2025+”. The proof outline uses concentrated cell classes, gridding, and formal-language/MSO methods. Only the announcement and slides were located; no full corresponding manuscript or journal publication was identified on the checked author pages/searches. Consequently this is recorded as an announced theorem, not an independently audited proof.
4. Latest nearby result: [Markström–Räty, Logical isomorphism and logical limit laws for small permutation classes and regular languages](https://arxiv.org/abs/2610.22218), v2 of 19 October 2026, was checked in full-text introduction. Its “small” means upper growth below kappa (printed p.4), not below 4. It does not resolve the remaining interval.

## Nonduplication with row 1848

Row 1848 concerns the converse phenomenon inside separables: whether a class containing one of the four nonmonotone Catalan avoidance classes must be nonrational. Such a class has growth at least 4. The present target concerns finite-basis classes below 4, including nonseparables. Their unresolved domains are therefore disjoint in growth. The overlap is only an established supporting theorem (the rational side of the separable classification), not the same open theorem to process twice. Neither rationality of a superclass nor nonrationality of a subclass is generally inherited in the reverse direction.

## Correction and search limits

Av(132) is not sum-closed: 1 and 21 avoid 132, but their direct sum is 132. The inherited source gate incorrectly included a sum-closure qualifier; it is removed here. Av(231) supplies a sum-closed Catalan example instead. This correction was accepted by the research audit and does not change the strict-boundary conclusion.

Literature searches were bounded to the sources described above and do not establish that unindexed or unpublished work does not exist. The PP2025 theorem is announced; a complete proof was not recovered or independently inspected.
