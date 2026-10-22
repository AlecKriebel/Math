# Status and five-approach record

Problem 30002888 / OWR-13682-010. Checked 2026-10-06.

**Outcome: honest partial investigation. No full construction or counterexample
has been obtained. No novelty claim is made.** The general statement should
not be marked solved on the basis of this package. The conditional results in
`proof.md` distinguish existence of a coherent triangle functor, perverse
t-exactness, derived Hom comparisons, and Yoneda Ext comparisons.

## Modern literature boundary

Riche's *Mixed modular perverse sheaves on affine flag varieties and Koszul
duality* was published online April 20, 2026, in Revista de la Union Matematica
Argentina 69(1), 373-410; DOI https://doi.org/10.33044/revuma.5035 . Its
Theorem 5.5 constructs a t-exact, Tate-trivialized derived functor with graded
Hom comparison. This concerns Iwahori-unipotent-equivariant etale sheaves on
affine flags of connected reductive G over an algebraically closed field of
positive characteristic, with coefficients in an algebraic closure of F_p,
p different from the geometric characteristic. The body's assumptions
(Section 3.3 and the start of Section 5) require:
- the character lattice modulo roots is free;
- the cocharacter lattice modulo coroots has no p-torsion;
- p strictly exceeds the componentwise bounds
  `A_n:1, B_n:n, C_n:2, D_n:2, E6:3, E7:19, E8:31, F4:3, G2:3`;
- the dual group's Lie algebra has an invariant self-duality;
- an etale central isogeny H to the dual group admits an H-equivariant
  morphism H->Lie(H), taking identity to zero and etale there (Lemma 2.10).

The introduction still identifies the general comparison as unresolved.
These hypotheses do not cover arbitrary complex affine-stratified varieties;
no universal etale-to-analytic transfer is asserted here.

Primary PDF: https://www.inmabb.criba.edu.ar/revuma/pdf/v69n1/v69n1a24.pdf .

Eberhardt and Scholbach's *Integral motivic sheaves and geometric representation
theory*, Advances in Mathematics 412 (2023), 108811, compares reduced
stratified Tate motives with the Achar-Riche category under affine-stratified
resolution assumptions. Its Section 1.6.1 explicitly leaves integral and
modular realization dependent on gluing; the complex-coefficient construction
does not supply an arbitrary-characteristic answer. Equivalence of a mixed
category with another mixed category is not the sought comparison to ordinary
perverse sheaves. Inspected preprint: https://arxiv.org/abs/2202.11477 ;
https://arxiv.org/pdf/2202.11477 .

The older finite-flag construction and the precise original conventions are
recorded in `proof.md`. The report year is 2015; its publisher lists publication
on February 15, 2016. This explains the two dates without changing the problem.

## Bounded investigation: five approaches

1. **Direct totalization of parity complexes.** Tested the chain-level lifting
   issue, rather than assuming a bicomplex exists. Section 5 of `proof.md`
   gives the first coherent-null-homotopy calculation. It does not vanish by
   an argument supplied here. No universal functor results from this route.

2. **Existing finite-flag Koszul duality.** Verified that this is a known
   affirmative special case, not a new solution. It depends on geometric
   structure unavailable for an arbitrary stratified X. Stopped short of
   transferring it outside its hypotheses.

3. **Affine-flag degrading functors.** Checked the current primary theorem
   and its coefficient, characteristic, and group restrictions. This updates
   historical special-case status but does not answer the whole question.
   No second proof of that established result was attempted.

4. **Motivic realization.** Checked the comparison formalism and its expressly
   stated realization gap. A richer six-functor formalism does not by itself
   produce the needed modular realization. No unsupported implication from
the complex-coefficient case was used.

5. **Categorical reduction and local construction.** Proved the generator
   criterion, its carefully conditional passage to Yoneda Ext, the gluing
   t-exactness test, and the elementary one-stratum construction. These
   isolate precisely what is missing: a general coherent extension and the
   relevant compatibility/realization assertions. They are partial results,
   not a replacement for those missing hypotheses.

## Scope of status claims

The literature review is bounded to the primary report, the cited foundational
construction, the 2023 motivic comparison, the 2026 affine-flag paper, and
targeted current searches. It is not an exhaustive theorem of absence.
The 2026 author's own statement supports treating the broad construction as
unresolved in this investigation; unsuccessful search is not evidence of
novelty. No claim is made that all possible negative examples have been ruled
out, or that additional hypotheses are necessary rather than merely sufficient.

This package contains no executable mathematical verifier. Its proofs need
independent mathematical review. Package hashes establish byte identity,
not mathematical truth. No claim of an independent acceptance audit is made.
