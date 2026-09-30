# Independent review: three pseudo-Anosov braid-related maps

**Verdict: PASS_COMPLETE_LITERAL_EXISTENTIAL_ANSWER.** The candidate gives three distinct, pairwise noncommuting, orientation-preserving Anosov diffeomorphisms of the closed torus whose three pairwise Artin relations have length three. This answers the literal question under the source's explicit torus convention. No mandatory correction is required. Recommended status: **claimed_solved, 1/5**. Historical priority remains unconfirmed; this is adversarial AI review, not human peer review.

The frozen `CANDIDATE.md` has SHA-256 `3808eff0561ba45d9ec32e02d86524133bf06e1abb08871b95fd5f16856d50b5`. All 311 submitted assertions replay with the identical receipt, and 3,156 independently written exact controls pass. The complete argument is short enough to check directly; the finite tests are supplementary.

## 1. Exact source scope

I independently inspected the rendered manuscript pages 122–124 of Wajnryb's chapter. Page 122 permits compact surfaces, possibly with boundary, and uses orientation-preserving maps in the oriented case. Page 123 defines alternating Artin relations. Page 124 separately discusses embeddings, then noncommuting braid-related pairs, then the existence of a set of at least three pseudo-Anosov maps with pairwise braid relations. Its immediately following paragraph explicitly discusses Anosov matrices on the torus. Thus this question does not silently impose genus at least two or exclude nonsingular torus foliations. [Primary source, Chapter 8, manuscript pp.122–124](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

The manuscript pagination differs from the published chapter pagination; the candidate's page 124 accurately identifies the linked copy. I also compared the complete pinned problem statement: it includes the same torus paragraph and adds no genus, independence, or faithfulness condition.

The set must contain distinct maps. The candidate meets this, and even makes their mapping classes distinct and noncommuting. The source does not require them to be nonconjugate or to be a minimal generating set. A faithful representation of a three-generator Artin group would be a stronger requirement and is not established here. Nor is there a claim for every prescribed surface or a torus with boundary fixed pointwise.

## 2. Universal group argument

Suppose a and b are distinct group elements satisfying aba=bab, and put c=aba^{-1}. Multiplying the braid relation on the left by b^{-1} and on the right by a^{-1} gives c=b^{-1}ab. Conjugating the original relation by a therefore gives aca=cac; conjugating it by b^{-1} gives cbc=bcb. These are the two additional pairwise relations.

If c=a, cancellation gives b=a. If c=b, then a and b commute. But commuting elements x,y with xyx=yxy satisfy x²y=xy², hence x=y by cancellation. This rules out c=b and also proves noncommutation for every pair of the triple. No assumption of torsion-freeness, faithfulness, or special geometry enters this lemma.

Conjugacy preserves the pseudo-Anosov property, so a distinct length-three braid pair in that class yields a triple. This is an elementary deduction from the pair mechanism already discussed in the source. It is not evidence of a new mapping-class-group construction of independent generators.

## 3. Recalculation of the actual torus maps

Using column-vector composition, I recalculated

\[
A=\begin{pmatrix}3&1\\2&1\end{pmatrix},\quad
B=\begin{pmatrix}1&-2\\-1&3\end{pmatrix},\quad
C=\begin{pmatrix}8&-11\\3&-4\end{pmatrix}.
\]

Each determinant is one and each trace is four. Direct multiplication gives

\[
ABA=BAB=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
C=ABA^{-1}=B^{-1}AB,
\]

\[
ACA=CAC=\begin{pmatrix}7&-10\\5&-7\end{pmatrix},\qquad
BCB=CBC=\begin{pmatrix}5&-13\\2&-5\end{pmatrix}.
\]

The integral inverse of each matrix makes its action on R²/Z² a genuine diffeomorphism. The determinant gives orientation preservation. Composition of these linear maps is matrix multiplication exactly, without an isotopy error or a translation term. Their distinct integral homology actions make them distinct mapping classes as well as distinct maps. Their pairwise products fail to commute, so neither a length-one nor a length-two Artin relation is being used.

Independently, the matrices fit the source's credited referee construction. Set

\[
X=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}-2&-1\\3&1\end{pmatrix}.
\]

Then X²=−I, Y³=I, A=XY and B=YX. The central −I causes no problem: both ABA and BAB equal −X. This explicitly matches the source's torus variant, rather than incorrectly demanding an order-two noncentral X in SL2(Z). The source's pair mechanism must remain credited.

## 4. Dynamics and measured foliations

For each matrix M the characteristic polynomial is t²−4t+1, so its eigenvalues are 2+sqrt(3) and 2−sqrt(3). The first exceeds one, the second lies strictly between zero and one, and they are reciprocal. The two constant eigendirections descend to transverse invariant line foliations on the torus. The derivative is M at every point, giving uniform expansion and contraction. Thus these are Anosov maps directly, not merely mapping classes known to have some suitable representative.

If a constant covector annihilates the contracting eigenline, its pullback by M is multiplied by 2+sqrt(3); the covector annihilating the expanding line is multiplied by 2−sqrt(3). Absolute-value integration supplies the transverse measures, invariant under deck translations. This proves the required reciprocal measured-foliation scaling. An integral matrix cannot have a rational eigenline with either of these irrational eigenvalues, so the line slopes are irrational. The foliations are nonsingular, exactly as allowed by the torus discussion in the source. A convention reserving the word pseudo-Anosov for negative-Euler-characteristic surfaces would change the terminology, but is not the convention used by the target's explicit example paragraph.

These facts establish the complete claimed existential answer. They do not rely on finite-coordinate samples to establish a global dynamical statement.

## 5. Independent controls and publication limits

The independent program recomputes the integer identities, the referee-pair factorization, and exact spectral projectors over Q(sqrt(3)). The projector checks certify rank one, idempotence, transversality, and eigenvalue scaling using rational arithmetic. It also tests the abstract lemma on all distinct braid-related pairs in symmetric groups of degrees two through five, finding 279 unordered pairs, and tests the induced maps on finite torus grids of moduli two through nine. The total is 3,156 assertions. The universal group proof above, not a finite-group enumeration, proves the lemma in arbitrary groups.

Reproduction:

```
python author_replay/verify.py
python independent_checks.py
```

All 311 submitted assertions reproduce the frozen receipt. No historical priority follows from these computations or from a bounded literature search. Publish the explicit answer and its elementary dependence on the source's already known pair construction, retaining the distinction from faithful Artin embeddings, prescribed higher genus, and boundary-fixed torus questions.
