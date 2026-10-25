# A seven-hyperplane counterexample to a generic-initial degree bound

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

15 October 2026; no version declared · Unrefereed preprint · CC BY 4.0

## Original abstract

For the characteristic-zero arrangement defined by Q=xy(x-y)(x-2y)zw(x+z+w), the degree-reverse-lexicographic generic initial ideal of the ambient Jacobian ideal has pure-second-variable cutoff 8 and a degree-7 minimal generator whose largest variable is the third. This explicitly contradicts the second-variable bound of Bigatti–Palezzato–Torielli, also stated in OWR Report 5/2021. We prove the generic sectional dimensions on a nonempty open set of compatible flags, using scalar polar syzygies and Hilbert–Burch, and give exact rational checks. The arrangement is a classical parallel connection; the methods and the valid three-variable arrangement theorem are prior work. Historical novelty and independent discovery are not established. This unrefereed note was developed with extensive AI assistance and has not undergone conventional human peer review.

## In plain language

A generic initial ideal records the monomial structure of polynomial equations after a general linear change of coordinates. This note gives a seven-hyperplane arrangement whose Jacobian ideal violates a proposed bound linking a second-variable exponent to the degrees of generators involving the third variable.

## Main result

Let $K$ be any field of characteristic zero, $S=K[x,y,z,w]$, and $Q=xy(x-y)(x-2y)zw(x+z+w)$. Form the ambient Jacobian ideal $J=(Q_x,Q_y,Q_z,Q_w)$ using all four partial derivatives before taking any section.

For the degree-reverse-lexicographic generic initial ideal $B$ with variable order $x_1>x_2>x_3>x_4$, the pure-second-variable cutoff is $p=\min\{d\ge0:x_2^d\in B\}=8$. The full four-variable ideal $B$ has a degree-seven minimal generator in $K[x_1,x_2,x_3]$ divisible by $x_3$. Its largest variable is therefore $x_3$, and its degree is strictly below $p$.

This contradicts the general-dimensional second-variable bound in Bigatti–Palezzato–Torielli's Conjecture 5.7 and the matching Oberwolfach statement. In the former notation, the proposed threshold is $d_0+1=p$. The theorem holds over every characteristic-zero field, without assuming the field is algebraically closed.

## Why it works

The proof studies compatible binary and ternary linear sections while keeping all four ambient polars. Reducing a linear polar relation modulo each distinct factor turns it into scalar proportionality equations with a trace condition. On the stated open conditions, there are no ternary linear syzygies and exactly one binary linear syzygy.

The binary polars have no common projective zero, so the ideal has height two. The classical Hilbert–Burch theorem forces syzygy coefficient degrees $1,2,3$. The resulting Hilbert values are $H_2(6,7,8)=(3,1,0)$ and $H_3(5,6,7)=(21,24,24)$.

An explicit compatible flag shows that the required conditions hold on a nonempty open set. Intersecting that set with the generic-initial open set justifies the generic sectional values. Favorable ranks in one coordinate system alone would not establish this step.

Strong stability and the reverse-lexicographic section identity give the cutoff eight. Multiplication by $x_3$ in the first-three-variable quotient has kernel dimensions zero at degree six and one at degree seven. A minimal-divisor argument then gives the degree-seven generator and proves its minimality in the full ring: a divisor of a monomial in the first three variables cannot introduce $x_4$.

## Scope and prior work

The ternary section retains four ambient partial derivatives. It differs from the three-generated Jacobian ideal obtained by restricting the arrangement and then differentiating in three variables. The valid three-variable theorem of Marchesi–Palezzato–Torielli remains intact.

The arrangement is a classical parallel connection of $U_{2,4}$ and $U_{3,4}$ along the shared factor $x$, as in Falk–Proudfoot. The logarithmic derivation mechanism, Hilbert–Burch theorem, Galligo generic-initial theory, Conca section identity and sectional counting methods are prior work. Tohaneanu explicitly credits Orlik–Terao for the derivation mechanism.

Migliore–Nagel's applicable family theorem already gives the resolution $0\to S(-7)^3\oplus S(-9)\to S(-6)^5\to J^{\mathrm{top}}\to0$, where $J^{\mathrm{top}}$ is the intersection of the codimension-two primary components of $J$. This is substantive prior information about the family. That five-generated ideal differs from the four-generated ambient Jacobian ideal studied here.

The full text of Ilardi's 2018 article was unavailable for the priority comparison, so a relevant earlier theorem or family is not excluded. Historical parameter families and code were not exhausted. Firstness, independent discovery, a new arrangement or general method, and present worldwide open status are not established.

The result does not compute the full generic initial ideal, specify an exponent vector for the degree-seven generator, prove a positive-characteristic extension, or claim the smallest possible number of hyperplanes. Exact checks at specified rational coordinates supplement the open-set proof; they are not full-generic-initial or priority certificates.

## References

[A. M. Bigatti, E. Palezzato and M. Torielli, New characterizations of freeness for hyperplane arrangements (2020)](https://doi.org/10.1007/s10801-019-00876-9) Conjecture 5.7 is the second-variable bound; generic-initial and sectional interfaces are classical inputs.

[E. Palezzato, joint work with M. Torielli, Hyperplane arrangements and k-Lefschetz properties, OWR Report 5/2021, pp. 233–235](https://doi.org/10.4171/OWR/2021/5) Conjecture 7 on page 234 states the matching bound using the pure-second-variable cutoff.

[E. Palezzato and M. Torielli, Lefschetz properties and hyperplane arrangements (2020)](https://doi.org/10.1016/j.jalgebra.2020.02.039) Conjecture 7.9 gives another statement of the same second-variable bound.

[E. Palezzato and M. Torielli, k-Lefschetz properties, sectional matrices and hyperplane arrangements (2022)](https://doi.org/10.1016/j.jalgebra.2021.10.014) Conjecture 7.9 and sectional methods provide the established context.

[S. Marchesi, E. Palezzato and M. Torielli, Lefschetz properties and the Jacobian algebra of 3-dimensional hyperplane arrangements (2026)](https://doi.org/10.4171/PM/2155) Theorem 4.7 treats actual three-variable Jacobian ideals, a different ideal from four ambient polars restricted to a ternary section.

[M. J. Falk and N. J. Proudfoot, Parallel connections and bundles of arrangements (2002)](https://arxiv.org/abs/math/0002094) Section 4 and Theorem 4.1 describe the classical parallel-connection construction.

[S. O. Tohaneanu, Projective duality of arrangements with quadratic logarithmic vector fields (2015)](https://arxiv.org/abs/1405.2122v2) Section 2.1 explains the classical scalar/logarithmic mechanism and credits Orlik–Terao.

[P. Orlik and H. Terao, Arrangements of Hyperplanes (1992)](https://doi.org/10.1007/978-3-662-02772-1) Proposition 4.29(3) is the credited antecedent for the decomposition mechanism.

[L. Burch, On ideals of finite homological dimension in local rings (1968)](https://doi.org/10.1017/S0305004100043620) The classical Hilbert–Burch theorem supplies the binary resolution interface.

[A. Galligo, À propos du théorème de préparation de Weierstrass (1974)](https://doi.org/10.1007/BFb0068121) Characteristic-zero generic-initial theory supplies the nonempty generic open and strong stability.

[A. Conca, Reduction numbers and initial ideals (2003)](https://arxiv.org/abs/math/0210064) Lemma 1.2 relates generic linear sections to the reverse-lexicographic generic initial ideal.

[J. C. Migliore and U. Nagel, Jacobian Ideals of Hyperplane Arrangements and their Graded Betti Numbers (2025)](https://arxiv.org/abs/2508.12113v1) Theorem 8.11 and Corollary 8.12 give substantive prior family information for the distinct ideal Jtop.

[G. Ilardi, Jacobian ideals, arrangements and the Lefschetz properties (2018)](https://doi.org/10.1016/j.jalgebra.2018.04.029) The full body was unavailable; possible relevant overlap is not excluded.

## Research status

AI tools were used extensively in developing and checking this note. It is unrefereed, without conventional human peer review or formal proof-assistant certification.

## Contributions

Substantive proof checks, counterexamples, and precise comparisons with earlier arrangement results are welcome. Authorship and acknowledgments depend on actual research contributions and mutual agreement.

## Paper and source

The complete 6-page deposited paper is available below.

Download the paper, complete verification archive, and the separately published TeX source from [the selected Zenodo edition](https://zenodo.org/records/23395703).
