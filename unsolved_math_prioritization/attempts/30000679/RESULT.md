# Rank-two NIP groups: a credited prior resolution

## Disposition

Both assertions in problem 30000679 / OWR-1453-013 have affirmative answers in the intended superrosy setting. This is an application of existing work by Clifton Ealy, Krzysztof Krupiński and Anand Pillay, not a new solution. One substantive investigation was used; it stopped when the exact prior resolution was verified. Independent review is pending for this frozen author packet.

## Exact scope

Let G be a definable group in the rosy model-theoretic setting of the original report. Assume that the ambient theory has NIP, every definable subgroup of G has finitely satisfiable generics (hereditary fsg), and its thorn U-rank is 2. The two questions are:

1. Does G contain a solvable subgroup of finite index?
2. If, additionally, G=G^00, is G itself solvable?

Here G^00 is the smallest type-definable subgroup of bounded index in the sufficiently saturated ambient model. Definability allows parameters, as in the cited paper. Rank means thorn U-rank, not dp-rank, Morley rank in an arbitrary theory, or the rank of a finitely generated abstract group.

## Existing theorem and application

Ealy–Krupiński–Pillay, *Superrosy dependent groups having finitely satisfiable generics*, Annals of Pure and Applied Logic 151(1) (2008), 1–21, DOI [10.1016/j.apal.2007.09.004](https://doi.org/10.1016/j.apal.2007.09.004), prove the first assertion as Theorem 2. The accessible [arXiv version](https://arxiv.org/abs/0706.0486) was submitted on June 4, 2007; its Theorem 2 appears on pp.2 and 19. Its complete rank-two argument is Theorem 3.1, pp.18–25. Crucially, Remark 3.3 on p.25 says the finite-index solvable subgroup can be chosen definable.

Consequently, choose a definable solvable H≤G with [G:H]<∞. This answers question 1. If G=G^00, finite index is bounded, and a definable subgroup is type-definable. The defining minimality of G^00 therefore gives

G = G^00 ≤ H ≤ G.

Thus H=G and G is solvable. This answers question 2. The use of definability here is essential: mere abstract finite index is not enough to invoke the definition of G^00.

If “solvable-by-finite” is defined using a normal solvable subgroup, there is no convention gap. Let N be the kernel of the left action of G on G/H. Equivalently, N is the intersection of the conjugates of H. The action has finite image, so [G:N] is finite; N≤H is solvable, N is normal, and only finitely many conjugates are distinct. Accordingly N is definable as a finite intersection of definable subgroups. Either convention yields the same conclusion.

## A direct check on the definability point

The main proof explicitly produces a definable witness, so no assumption that every abstract subgroup is definable is made. The core construction above also preserves this property. In the saturated setting, N remains a type-definable bounded-index subgroup, hence contains G^00. If G=G^00, N=G. In particular no step identifies the ordinary connected component G^0 with G^00 in general.

Without connectedness, the implication from solvable-by-finite to solvable is false: any finite group has the trivial solvable subgroup of finite index, whereas A5 is not solvable. The executable finite-group control tests precisely this logical pitfall; it is not a counterexample to the stated rank-two theorem.

## Limits of this result

No result is asserted after dropping hereditary fsg, replacing it by definable amenability, changing thorn rank to dp-rank, or using an unspecified abstract notion of rank. The source paper's later definable-amenability conjecture is a different problem. There is no novelty claim, formal-verification claim, or claim that this packet has received human peer review. The substantial rank-two theorem is credited to the published authors; the short implication from its definable witness to question 2 is written out above.
