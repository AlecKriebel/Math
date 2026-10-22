# Root independent pre-artifact mathematical mechanism freeze

UTC: 2026-10-17T21:17:42.406056+00:00. Source/criteria preparation 100%; submitted mathematics acceptance 0%; case workflow 5%. This is a proposed exact verification route derived before Root reads either submitted proof or script. It is not an assertion that the submitted implementation supplies these certificates. Native artifact-custody acceptance is still pending. This freeze uses the original queue's public K4,4 target and the independently read source definitions.

The model is the ordinary K4,4 concentration space, admissible as a colored model with singleton vertex and edge classes. Write data X=[Y;Z] with four rows in each block and n columns. Measured statistics are the eight row squared norms and all sixteen entries of Y Z^T. Work with known mean and unnormalized Gram data XX^T. Scaling by sample count does not change cone membership.

## Proposed WMLT certificate

At n=2 take every Y row (1,0) and every Z row (0,1). All measured diagonal entries are 1 and every measured cross entry is 0, matching I8. A linear statistic right inverse corrects I8 continuously for nearby data, preserving PD. Thus this is a nonempty open good-data set, of positive probability under every nondegenerate Gaussian covariance. At n=1 each specified edge has a zero 2-by-2 principal determinant, precluding every PD completion; this includes zero row boundary cases. These two facts would establish WMLT=2.

## Proposed exact ideal transition and almost-sure upper bound

At n=3, the nonzero formal polynomial det(B) of the 4-by-4 measured cross block vanishes on all rank-at-most-3 symmetric matrices; it is one of the specified 4-minors itself, so membership in the elimination ideal does not need a generic vanishing-ideal equivalence.

At n=4 take Y=I4 and let Z have rows (1,1,0,0), (1,0,1,0), (1,0,0,1), (0,1,1,0). The 24-by-32 measured-Gram Jacobian should have row rank24. Mechanism: diagonal variations of Y set the four left diagonals; variations of Z set the sixteen cross entries. Keeping these fixed leaves diagonal-zero deltaY and deltaZ=-Z deltaY^T. The four right-diagonal variations are independent through symmetric off-diagonal coordinates12,13,14,23, respectively, because these are the distinct pairs in the four Z rows. The exact rank and a nonzero24-square minor will be computed independently after custody acceptance.

A full-row-rank Jacobian gives a Euclidean open statistic image, so every elimination polynomial vanishes identically and I4=0. Its nonzero minor is a polynomial in data entries, so that same rank holds outside a measure-zero algebraic set. Since the adjoint Jacobian sends a concentration matrix K to2KX, full row rank excludes every nonzero concentration K annihilating X, including PSD stresses. This supplies almost-sure MLE existence at4 without treating nonzeroI3 as a statistical lower bound.

## Proposed positive-measure failure at n=3

Let Y0 have tetrahedral rows (1,1,1)/2, (1,-1,-1)/2, (-1,1,-1)/2, (-1,-1,1)/2, and Z0 have rows e1,e2,e3,0. Then Y0^T Y0=Z0^T Z0=I3.

Seek positive weights a_i,b_j satisfying
  Y^T diag(a)Y = Z^T diag(b)Z = G.
At the witness all eight weights are1. The linear map from weights to the six symmetric coordinates of their difference has rank6: the four tetrahedral projectors span the common diagonal plus all three off-diagonal coordinates, and the first two coordinate-axis projectors supply the two missing diagonal directions. A six-square minor, using all four a and b1,b2, will be checked exactly. Hold b3=b4=1 and solve this six-square system continuously near the witness. All weights remain positive and G remains PD.

Define
 K = [[D_a, -D_a Y G^-1 Z^T D_b],
      [-D_b Z G^-1 Y^T D_a, D_b]].
Then KX=0. With U=D_a^(1/2)Y G^(-1/2), V=D_b^(1/2)Z G^(-1/2), both U and V have orthonormal columns; the normalized off-diagonal block U V^T has norm<=1. Therefore K is PSD by congruence from [[I,-UV^T],[-VU^T,I]]. Its positive diagonal makes it nonzero, and its within-part off-diagonal entries are zero, so it belongs to the K4,4 concentration space. This holds on a whole neighborhood of data, not only at the displayed point.

A PD completion S would give tr(KS)>0 but also tr(KS)=tr(KXX^T)=0, contradiction. The open bad-data neighborhood has positive Gaussian probability. Adding data columns preserves an existing PD completion, so almost-sure existence at a smaller n would imply it at3. Together with the n=4 upper certificate this would prove MLT=4.

## Scope and unverified obligations

If all proposed certificates pass exact checks, the example has I4=0, I3 nonzero, WMLT=2, MLT=4. It contradicts the source's literal second numerical conclusion WMLT=3, while the second algebraic/cone antecedent is actually satisfied. It does not refute Boolean SOS-or-intersection exhaustiveness, a four-cycle-only intended question, or a variant imposing an extra condition absent from the displayed proposition. No priority or novelty claim is made. Source theorem definitions, submitted proof scope, all lower/upper bounds, and computations still require actual audit.
