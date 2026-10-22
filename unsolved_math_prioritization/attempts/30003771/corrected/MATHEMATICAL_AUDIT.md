# Mathematical scope and obstruction audit

## 1. What the original question actually asks

In the source report, X is proper, finite type, geometrically connected and geometrically reduced over a field k; D is a simple normal-crossings divisor, with a positive-integer multi-index r. The theorem compares existence of a finite abelian group scheme and a ramified torsor with data (D,r) against occurrence of every allowed local multiweight in essentially finite parabolic bundles having abelian monodromy. The group is existentially quantified. No rational point of X is required. The nonabelian question follows Theorem 1 on printed page 1070. The workshop occurred 15–21 April 2018; the catalog's parenthetical “2019” should not replace that event date. [S1]

The local ramification model is a Kummer cover induced along an injection of the product of roots-of-unity group schemes into G, after a field extension and an fppf neighborhood of the base point. This is more restrictive than merely naming a torsor on the associated stack. [S1]

Source-version qualification: the 2018 report uses an earlier diagonal-step definition of a weight. This audit uses the corrected joint-weight definition in the final manuscript, Definition 2.5: the sum of the coordinate-step images in E_(l/r) must have nonzero cokernel at x. The final manuscript explicitly credits Ahlqvist for correcting the earlier definition. At a crossing, a simultaneous diagonal step is not a substitute for that sum. Thus “the original question” here preserves its proper-base existence quantifiers and Kummer-local torsor requirement, while adopting the published correction to its weight terminology. [S1, p. 1070; S2, Definition 2.5 and footnote 1]

## 2. A precise partial endpoint of the proposed strategy

Let S be the root stack associated with (X,D,r). Its geometric inertia at a point on several divisor components is H = product(mu_{r_i}) over those components. Denominators are bounded by r componentwise. At a crossing, keeping only separate one-divisor weight lists loses joint-character information.

The relevant existing uniformization theorem applies to an inflexible, pseudo-proper, finite-type stack with finite inertia. It says that a finite-group-scheme torsor with algebraic-space total space exists exactly when every representation of each closed residual gerbe is a subquotient of the restriction of an essentially finite bundle. This is already nonabelian. It uses the Nori gerbe and does not need a chosen rational point. [S3, Theorem 4.11 and Proposition 4.5]

A dependency qualification is essential: S2, Remark 3.21 corrects the terminology of S3 for nonalgebraic fundamental gerbes. The relevant morphism to the profinite Nori gerbe must be faithful (injective on automorphism sheaves); it is not asserted representable by algebraic spaces. S2, Lemma 3.20 passes from faithfulness at the limit to a finite gerbe stage. At that algebraic stage representability is appropriate, and S3, Proposition 4.5 supplies a finite-group-scheme torsor. The residual-representation uniformization criterion remains valid with this correction.

Here is the elementary character step behind the reduction. A representation of the diagonalizable group H is a finite direct sum of its character spaces, in any characteristic. If every character occurs in some restricted bundle, a direct sum of finitely many such bundles, with repetitions, contains any chosen finite-dimensional H-representation as a subrepresentation. Conversely, if every H-representation is a subquotient, apply this to a single character: graded subquotients cannot acquire a character absent from the original representation. Thus all-character detection, with the correct joint weights, matches the residual-representation test.

Subject to checking the stated stack hypotheses, that argument reaches uniformization of S. It does not show that the composite cover of X has the prescribed fppf-local Kummer induction form. Those are two distinct assertions. Replacing the latter assertion by the former would change the problem.

There is a second distinction: for a fixed group G, torsor reconstruction requires an exact strong symmetric monoidal functor from Rep_k(G), including its unit, tensor, associativity and symmetry compatibility. A single essentially finite object, an unstructured list of representations, or a collection of independently chosen weight spaces is not that data. A pointed classification additionally requires a specified fiber identification at the base point. An unpointed statement must retain its groupoid/gerbe formulation.

## 3. Verified prior failure of the local step

In the final manuscript, Remark 2.9(3) warns that the naive nonabelian existence statement is doubtful with Definition 2.2 unchanged. Proposition 3.13 asserts that agreement of two abelian torsors on a closed residual gerbe extends after an fppf neighborhood of the coarse point. Appendix B disproves its nonabelian analogue. Its first family uses characteristic p, root index p and G = alpha_p semidirect mu_p. Its second uses odd characteristic, root index 2 and G = mu_p semidirect C_2, with inversion action. The latter is already a Deligne–Mumford root stack. Both groups are finite nonconstant group schemes. [S2, Remark 2.9(3), Proposition 3.13, Appendix B]

In particular, imposing prime-to-characteristic root denominators alone does not remove the documented obstruction. It does not turn a nonreduced structure group into a finite étale group. Conversely, no counterexample for finite constant groups in characteristic zero is inferred here.

## 4. Explicit algebraic checks

The following elementary checks explain why the obstruction survives the base-neighborhood operation. They verify part of the cited construction, not the full global existence question.

### Lemma 1: additive obstruction

Let k have characteristic p > 0 and R = k[u,v] localized at (u,v). If R -> B is a faithfully flat algebra, then

v is not in uB, and therefore v is not of the form u b^p for b in B.

Proof. Faithful flatness makes R/(u) -> B/uB injective. The class of v in R/(u), which is k[v] localized at (v), is nonzero. Therefore its image in B/uB cannot vanish. This proves both statements. At the closed point (u,v), by contrast, the specialization of v is zero. The same argument applies to an arbitrary fppf neighborhood containing a point above (u,v), after localization at that point, because a flat local homomorphism of local rings is faithfully flat. QED.

Thus an obstruction represented by v modulo the image of b -> u b^p cannot be killed by such a neighborhood, although its specialization vanishes. No computation or finite sample is being used.

### Lemma 2: prime-to-characteristic root-index obstruction

Assume p is odd. Put

R = (k[u,v,a]/(a^2 - 1 - uv^2)) localized at (u,v,a-1),

C = R[t]/(t^2-u), and e = a+vt.

The polynomial defining C is monic, so 1,t is an R-basis. The involution t -> -t gives e norm one since (a+vt)(a-vt)=a^2-uv^2=1. Modulo u, the relation for a becomes (a-1)(a+1)=0. Since a+1 is a unit at the chosen point, R/(u) is k[v] localized at (v). In particular, v is nonzero modulo u.

For any faithfully flat R-algebra B, e cannot be the p-th power of an element of C tensor_R B. Indeed, write such an element c+dt in its unique basis expansion. Characteristic p and t^2=u give

(c+dt)^p = c^p + d^p u^((p-1)/2)t.

Equality to e would require v = d^p u^((p-1)/2), contradicting Lemma 1's ideal-contraction argument because (p-1)/2 >= 1. This rules out a p-th root even before imposing any norm-one constraint on c+dt. Specialization at the chosen closed point sends e to 1. QED.

This is an essentially finite-type local algebraic realization of the relevant norm-one obstruction. It proves an explicit algebra statement only. Passing from it to a complete torsor construction requires the twisted Kummer sequence and lifting identification of the cited source; those results are not being silently treated as a new proof.

## 5. Scope checks and stopping point

- Characteristic is unrestricted in the original question. Positive-characteristic finite group schemes cannot be replaced by abstract finite groups.
- “Tame stack” does not itself mean that every root index is invertible in k. A diagonalizable group scheme has a character grading even when it is nonreduced. Prime-to-characteristic indices do make the displayed root inertia étale, but Lemma 2 shows why that restriction alone is insufficient for the proposed local step.
- Prescribed ramification requires faithful full inertia, including at intersections. Noncommutativity of global monodromy does not make the product of local root inertia noncommutative.
- Basepoints and neutrality are additional data. The original unpointed gerbe method avoids assuming them.
- A failure for particular local torsors does not prove that every possible global torsor with the same ramification fails. The global criterion allows changing G. The displayed affine/local examples do not satisfy the original proper-base hypothesis.
- Ahlqvist's 2024 paper broadens building data and the ramified-cover setup, but its Theorem 9.18 and Definition 9.8 retain finite abelian G. It does not supply the missing nonabelian theorem. [S4]

**Final mathematical status:** a known, explicitly checked obstruction defeats the straightforward abelian-proof extension. A proof or counterexample for the original proper-base nonabelian existence criterion, with its original local torsor definition, has not been established here. No novelty claim is made.
