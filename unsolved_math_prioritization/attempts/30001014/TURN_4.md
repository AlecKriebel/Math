# Turn 4: cones, attachment at a character, and the limit of retract reductions

Substantive author turn **4/5**, for the explicitly infinite-spectrum variant. This turn adds path-connected contractible examples and proves a broad attachment theorem: **every nonempty compact Hausdorff space is a closed retract of a compact spectrum exhibiting the pathology**. The latter is an embedding/retraction result, not realization of the original space itself.

## 1. The exact input property

Let D be a unital MASA in a unital C*-algebra A, with compact spectrum Y. Assume there is a nonzero element

 x in ker(A⊗_max A→A⊗_min A)

which commutes with D⊗D. All pairs certified in turns2–3 have this property. Choose a representation Π of A⊗_max A with Π(x)≠0; such a representation exists because representations separate elements of a C*-algebra. The source pair permits its explicit left/right representation.

This input is stated at the maximal completion. We do not assume that an arbitrary commutant element in an intermediate tensor quotient lifts to a commutant element at the maximal completion. Such a lifting claim would be unjustified. The preceding constructions already provide the maximal witness needed here.

## 2. Unitized cones retain a localized witness

Define

 CA={F in C([0,1],A):F(0) is a scalar multiple of1},
 CD={F in C([0,1],D):F(0) is a scalar multiple of1}.               (1)

The map χ:CA→C taking the scalar endpoint value is a character. Its restriction to CD is evaluation at the cone apex. The ideal of sections vanishing at0 is C0((0,1],A), and it contains the interior ideal J=C0((0,1),A).

The same interior-bump argument as in turn3 proves that CD is a MASA: a commuting section takes values in D at every t>0, and its scalar value at0 already belongs to D. Its spectrum is the ordinary compact cone

                       CY=([0,1]×Y)/({0}×Y).                    (2)

Indeed the continuous functions on this quotient are precisely (1)'s D-valued sections under D=C(Y). Compactness and Hausdorffness follow from collapsing the closed subset {0}×Y in the compact Hausdorff product. The contraction [t,y]↦[(1−r)t,y], 0<=r<=1, is continuous and contracts CY to its apex. Hence CY is contractible and path connected, even when Y is disconnected or nonmetrizable.

The ideal-specific maximal-tensor inclusion proved in turn3 gives

 J⊗_max J=C0((0,1)²,A⊗_max A) → CA⊗_max CA

isometrically. Choose f in C_c((0,1)) with f(1/2)=1 and put X(t,s)=f(t)f(s)x. The same pointwise multiplication proof gives [X,CD⊗CD]=0 and zero image in the minimal completion. Evaluation e at1/2, followed by Π, detects X. Thus

 ||w||_α=max{||w||_min,||Π((e⊙e)(w))||}

is a C*-norm for which X has nonzero image. Every β>=α retains a nonzero minimal-kernel commutant element, so CD⊗CD fails to be a MASA in CA⊗_β CA. The strict positivity of the witness is not needed, and no new norm-injectivity assumption enters.

Taking the fully proved source Y=S, or the Cantor cube examples from turn2, yields explicit path-connected contractible pathological spectra. This does not identify any of these cones with an interval or a ball.

## 3. Attach an arbitrary compact space at the cone character

Let Z be any nonempty compact Hausdorff space and choose z0 in Z. Form the unital pullback

 B={(F,g) in CA⊕C(Z):χ(F)=g(z0)},
 E={(F,g) in CD⊕C(Z):χ(F)=g(z0)}.                               (3)

This is an actual *-algebra pullback along **characters**. It does not use a conditional expectation onto a MASA as though that expectation were multiplicative. Existence of χ is the reason for first taking the cone.

The algebra E is a MASA in B. To see this, suppose (H,h) commutes with E. For every t>0 and d in D, choose a scalar bump supported away from0 and equal to1 at t. The pair consisting of that bump times d and the zero C(Z) function belongs to E. Thus H(t) commutes with D and lies in D. At0 the scalar condition is automatic. Therefore H is in CD, while h already belongs to the abelian C(Z), and the original matching condition proves (H,h) is in E.

The spectrum of E is

                        W=CY union_(apex=z0) Z.                  (4)

Both summands embed as closed subspaces; the finite point-identification in their disjoint union gives a compact Hausdorff space. Functions on the quotient are exactly pairs of continuous functions with matching values, proving the identification without a set-theoretic spectrum shortcut.

The interior ideal J from §2 embeds into B as (F,0), since its endpoint scalar is0. It is a closed ideal. The localized tensor X from §2 therefore embeds isometrically in B⊗_max B by the same ideal lemma. Multiplication by (F,g) on J only sees F, so the same pointwise argument proves that X commutes with E⊗E. The evaluation e_B(F,g)=F(1/2) is a surjective unital *-homomorphism, and Π∘(e_B⊙e_B) detects X. Its image in B⊗_min B is zero. The threshold norm and all larger norms consequently exhibit the required pathology, exactly as in §2.

## 4. A universal closed-retract statement, with its limitation

The map r:W→Z which is the identity on Z and collapses the entire cone CY to z0 is continuous: its two continuous pieces agree at the identified point. It is a retraction onto the closed embedded copy of Z. Since the source seed Y=S is fixed and fully proved, this construction works for **every** nonempty compact Hausdorff Z.

Therefore embedding an arbitrary compact space as a closed subset, a retract, or a continuous image of a pathological spectrum cannot by itself solve the realization question. An additional operator-algebra transfer theorem would be necessary. There is an explicit obstruction to an unrestricted such transfer: take Z to be a singleton. The space W=CS is realized by §2 and retracts onto Z, whereas turn1 proves that Z cannot be realized. Thus realizability is not preserved by arbitrary closed retracts, and likewise is not preserved by arbitrary continuous images or closed subspaces.

This finite target does not refute a hypothetical transfer theorem restricted to suitable **infinite** targets. That restricted transfer remains unproved, and we do not present the singleton as a counterexample to it. The precise positive statement here concerns the larger space W in (4), not its retract Z.

## 5. Scope after four turns

There are now source-supported realized classes including convergent-sequence products, all infinite Cantor cubes, a connected mapping torus, cones of the certified spectra, and the character attachments (4). Cone examples establish path connectedness and contractibility; the prior mapping torus only claimed connectedness. These properties should not be conflated.

Neither the announced interval construction nor realization of every infinite compact Hausdorff space has been reconstructed. The obstruction to a naive quotient/retract proof is explicit, but failure of that proof route is not a counterexample to the infinite realization question. One substantive turn remains within the original five-turn budget. Status for the explicitly infinite variant: **unresolved4/5**.
