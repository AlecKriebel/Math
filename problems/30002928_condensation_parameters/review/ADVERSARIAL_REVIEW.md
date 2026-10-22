# Independent full five-turn review: PASS within the stated scope

Problem30002928 / OWR-13856-004. All five proofs, final result and additive source qualification were read. No mandatory mathematical correction was found beyond the already supplied source qualification. The original all-kernel parameter-selection conjecture remains unsolved5/5. This is AI-assisted review, not formal certification or human peer review.

## Source scope

The official OWR printed2014 was visually inspected: the field is positive, the limiting phase lies on the negative metastable branch, and the short half-line display does not specify its exterior convolution convention. The2011 source explicitly defines reflected Neumann convolution and distinguishes it from endpoint conditions. The2000 definition page was visually inspected and indeed prints monotonicity on the whole real line, inconsistent with a nonconstant even density. SOURCE_QUALIFICATION correctly retracts the earlier extraction-loss assertion and states radial decrease as an explicit working hypothesis/inferred reading. No source-intent or vacuous full-resolution inference is warranted. The constructed smooth compact decreasing kernels still belong to the broader smooth-even-normalized OWR class.

## Turn1: nonlocal identity and necessary bound

The half-line convolution split and symmetrization give the two boundary terms with the stated signs. Compact kernel support, bounded profile, integrable monotone derivative and zero far-field deviation justify the passages from finite intervals. Integration by parts gives I(m,u) as the positive kernel-derivative quadratic form. The strict bound uses positivity propagation and the peak equation to produce a genuine positive-measure deficit; it does not assume strictly decreasing J. The trapezoidal-error sign follows because A'' is odd and strictly increasing. Consequently u<-m and the stated positive-field interval are valid necessary conditions, not existence or uniqueness.

## Turn2: comparison kernel only

The exponential Green kernel converts the bounded full-line equation exactly to the displayed second-order ODE. The energy difference has strictly negative field derivative. Its signs at zero field and the negative spinodal endpoint give one selected field. The turning point lies on the descending potential branch; the quadrature is finite at its peak and diverges logarithmically at the stable negative equilibrium. Thus it defines the unique centered unimodal homoclinic, and bounded Green inversion returns the integral equation. The implicit derivative is negative and the quadratic endpoint coefficient follows from the second peak derivative and nonzero field derivative. This is a complete theorem for the exponential kernel, explicitly outside the smooth compact source class.

## Turn3: functional-analytic persistence

On even C0, convolution by J0 is bounded, and the localized difference from the stable-tail convolution is compact by uniform translation continuity, vanishing tails and Arzela–Ascoli. The stable-tail inverse is a Neumann series, hence the linearization is Fredholm of index zero. A kernel vector gives the scalar Green ODE; its Wronskian with the nonvanishing half-line translation solution vanishes at infinity. Evenness imposes zero derivative at the origin, while the translation solution has nonzero derivative there, removing that mode. This yields a bounded even-space inverse.

The field derivative belongs to C0 because its far-field constant cancels exactly. The bordered peak Schur complement is the nonzero reciprocal of the comparison branch's peak-to-field derivative. The explicit comparison homoclinic varies continuously in C0 using local ODE dependence and uniformly stable exponential tails near a fixed field. The Banach implicit-function theorem therefore applies. Positivity above the limiting phase follows by the global-minimum argument; C0 closeness alone is correctly not used to infer shape.

## Turn4: moving planes

For positive violations, the far-right small-tail bound places both compared profile values in the stable derivative interval, even if the reflected coordinate is not geometrically in the tail. The reflection kernel is nonnegative, strictly positive within interaction range, and has mass at most one. Starting-plane contraction and strict-sign propagation are justified. At a putative nonsymmetric stopping plane, uniform negativity on the central compact interval leaves only a thin strip and far tail. Compact support removes their mutual coupling; the strip smallness and tail contraction separately eliminate positive parts. This closes the continuation step without a false global contraction estimate. Uniqueness of the symmetry center follows from decay, and the moved-plane inequalities give strict unimodality.

## Turn5: uniformity and remaining quantifiers

Compactness of the reference peak interval supplies uniform inverse bounds, derivative control and a single contraction radius. The residual estimate and radius choice give a self-map; local branches agree by uniqueness. Differentiated implicit equations preserve the negative field derivative uniformly. The explicitly normalized smooth compact kernel has L1 error at most twice the unnormalized mass loss, so one kernel works for the whole fixed compact interval. Spatial rescaling preserves the equation and both relevant norms. The physical neighborhood is relative to the stated nonnegative strictly decreasing class.

No endpoint-uniform perturbation size is inferred. The peak identity forces different-field competitors to cross despite ordered limiting phases, so the local branch theorem cannot silently become global uniqueness. General source kernels, distant branches and unspecified half-line continuations remain open exactly as stated.

## Verification

All26 manifest-bound author files, historical turn bindings and eight final source hashes verify. All five author checkers replay byte-identically, totaling23,738 assertions. A separately written checker passes460 exact symbolic/rational controls covering energy boundary identities for exponential mixtures, scalar derivatives and endpoint algebra, and reflected-kernel positivity. These checks supplement the written infinite-dimensional proofs; they do not certify Fredholm theory or moving planes numerically. Both author and independent symbolic scripts require SymPy.

Publish as an unsolved5/5 scoped research checkpoint, preserving every frozen proof and the additive qualification. Prominently separate the solved comparison kernel from the actual compact-kernel local branch. No full original resolution or novelty claim is supported.
