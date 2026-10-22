# An erasing-witness restriction for the independent-triple problem

## Status and scope

This is an elementary, attributed partial reduction. It does **not** prove or disprove the existence of three independent constant-free equations on three variables with a common nonperiodic solution. No novelty claim is made. In particular, the two-erasure mechanism below occurs in Holub–Žemlička (2015), Lemmas 15–16.

All morphisms are from `{X,Y,Z}*` to a finite-alphabet free **monoid**. Empty images are permitted. Equations have nonempty variable words on both sides and no constants. Independence concerns the entire solution set. A periodic morphism maps all three variables to powers of one word. A deletion witness for an equation satisfies the other equations and fails that equation.

We use the standard two-word fact in its indexed form: for distinct formal letters P,Q and words u,v, the morphism P -> u, Q -> v is injective if and only if uv != vu. Equivalently, this morphism is noninjective if and only if u,v are powers of one common word. This formulation includes empty or equal images; when u,v are distinct and nonempty, it is the usual two-element-code criterion. See Saarela (2024), Lemma 2.1.

## 1. The balanced reduction (prior theory)

An independent system with at least two equations and a common nonperiodic solution contains only balanced equations.

Indeed, let `h` be the common nonperiodic solution. If an equation `E` in the system is unbalanced, Saarela (2024), Lemma 4.4, says that `E` is equivalent to the entire system `Eq(h)`. Every equation in the given system belongs to `Eq(h)`, so `E` alone implies the whole system, contradicting independence.

Consequently every deletion witness for such a system is nonperiodic: every periodic morphism satisfies every balanced equation. This consequence does not redefine independence; it follows from the full-solution-set definition and the prior balanced reduction.

## 2. Nonperiodic erasing morphisms have three equation profiles

Write `pi_A` for the morphism deleting variable `A` and retaining the other two variable letters.

**Lemma 1.** A nonperiodic erasing morphism erases exactly one variable, say `A`. For every equation `(U,V)`, it is a solution if and only if `pi_A(U)=pi_A(V)` as variable words.

**Proof.** Erasing two variables would leave at most one nonempty image, making the morphism periodic. The two retained images do not commute, since otherwise they and the empty image would be powers of a common word. They therefore form a two-word code. Equality after substituting those images is precisely equality of the two retained-variable words. This proves both directions. □

**Lemma 2.** Let `A,B,C` be the three distinct variables. If a nontrivial equation `(U,V)` satisfies both `pi_A(U)=pi_A(V)` and `pi_B(U)=pi_B(V)`, then it is equivalent, over the whole free monoid, to `AB=BA`.

**Proof.** Both deletion equalities preserve every occurrence of `C`. Thus write

`U = u_0 C u_1 C ... C u_r`,

`V = v_0 C v_1 C ... C v_r`,

where each `u_i,v_i` is over `{A,B}`. The two projection equalities imply separately that `u_i,v_i` have the same number of `A` letters and the same number of `B` letters for every index `i`.

Under any morphism, the images of `u_i,v_i` have equal lengths. If the images of `U,V` are equal, their equal-length block boundaries align; cancelling successively gives equality of the images of every pair `u_i,v_i`. Since `U!=V`, at least one such pair is distinct. That pair is a nontrivial relation between the images of `A,B`, forcing those images to commute. Conversely, commuting images make each pair of blocks equal because their letter counts agree, and hence make `U,V` equal. Empty images cause no problem in either argument. □

Lemma 2 is the three-variable form of the argument in Holub–Žemlička (2015), Lemma 16. The present proof uses the two-word code criterion directly, so it does not identify nonperiodicity with a particular linear-rank convention.

## 3. A commutation equation prevents an independent triple

**Proposition 3.** Let `S` be a balanced system in three variables with a common nonperiodic solution. If one member is equivalent to a pairwise commutation equation, then `S` is equivalent to a subsystem with at most two members.

**Proof.** Replace that member temporarily by the equivalent equation `C: YZ=ZY`. This does not change any solution set or independence condition. Every solution of `C` has `y=w^m,z=w^n`, for a word `w` and integers `m,n>=0`. If the morphism is nonperiodic, we can and do choose `w` nonempty, `(m,n)!=(0,0)`, and `x,w` noncommuting. Conversely these conditions describe the nonperiodic solutions of `C` in this form.

For a balanced equation `B`, both sides have the same number `r` of `X` letters. Split them at these occurrences into blocks over `{Y,Z}`. For block `i`, let `(p_i,q_i)` be the number of `Y` and `Z` letters on the left minus those on the right. Upon substituting `y=w^m,z=w^n`, the corresponding blocks become powers of `w`. Since `x,w` form a code, a nonperiodic solution of `C` solves `B` if and only if

`p_i m + q_i n = 0` for every block `i`.

Let `D_B` be the matrix of these two-column rows. The fixed common nonperiodic solution provides a nonzero vector `(m_0,n_0)` in the kernel of every `D_B`. Therefore each matrix is zero or has rank one. Every nonzero matrix has the same kernel, namely the line spanned by `(m_0,n_0)`.

If `D_B=0`, every nonperiodic solution of `C` satisfies `B`. If `D_B!=0`, the nonperiodic solutions of `C` satisfying `B` are exactly those whose exponent vector lies on that common line. Periodic solutions satisfy all the equations automatically, since all are balanced. Thus either `C` implies all of `S`, or `C` together with any one member having nonzero matrix implies all of `S`. Replacing `C` back by its equivalent original member gives the asserted subsystem. □

This is a direct restricted-class argument. It does not infer that a finite subsystem is redundant merely because an entire system has a one-equation presentation.

## 4. Consequences for the exact target

**Theorem 4.** Suppose `S={E_1,E_2,E_3}` is an independent system with a common nonperiodic solution.

1. At most one of the three equations admits an erasing deletion witness.
2. If the system has any common erasing nonperiodic solution, none of its three equations admits an erasing deletion witness.

**Proof of 1.** Assume erasing deletion witnesses exist for two different equations. They are nonperiodic by Section 1. They cannot erase the same variable, because Lemma 1 would give them identical equation profiles, whereas their satisfied/failed equations differ. They therefore erase distinct variables `A,B`. The third equation is satisfied by both witnesses, so its two deletion projections are identities. It is nontrivial, since the system is independent. By Lemma 2 it is equivalent to `AB=BA`. Proposition 3 contradicts independence. □

**Proof of 2.** Let a common nonperiodic solution erase `A`, and assume a deletion witness for `E_i` erases `B`. Lemma 1 forces `A!=B`, since the common solution satisfies `E_i` and the witness fails it. Choose any other equation `E_j`. Both morphisms satisfy `E_j`, so Lemma 2 makes that nontrivial equation equivalent to `AB=BA`. Proposition 3 again contradicts independence. □

These restrictions eliminate certificates that rely too heavily on erasing witnesses. They do not remove erasing common solutions from the problem. A remaining candidate may have such a common solution and three nonerasing deletion witnesses, or may have a nonerasing common solution and at most one erasing deletion witness.

## References

- Juhani Karhumäki, contribution to *Mini-Workshop: Combinatorics on Words*, Oberwolfach Report 37/2010, printed pp. 2215–2219; exact question at p. 2217. [Publisher PDF](https://ems.press/content/serial-article-files/46296).
- Dirk Nowotka and Aleksi Saarela, *An Optimal Bound on the Solution Sets of One-Variable Word Equations and its Consequences*, SIAM J. Comput. 51(1) (2022), 1–18. [DOI](https://doi.org/10.1137/20M1310448), [author PDF](https://amsaar.gitlab.io/articles/nosa22sicomp.pdf).
- Aleksi Saarela, *On the Solution Sets of Three-Variable Word Equations*, Theory Comput. Syst. 68 (2024), 1556–1571. Lemmas 2.1 and 4.4. [DOI](https://doi.org/10.1007/s00224-024-10193-9), [author PDF](https://amsaar.gitlab.io/articles/sa24tocs.pdf).
- Štěpán Holub and Jan Žemlička, *Algebraic properties of word equations*, J. Algebra 434 (2015), 283–301. Lemmas 15–16 and Theorem 24. [DOI](https://doi.org/10.1016/j.jalgebra.2015.03.021), [author-hosted PDF](https://www.karlin.mff.cuni.cz/~holub/soubory/AlgebraicProperties.pdf).
