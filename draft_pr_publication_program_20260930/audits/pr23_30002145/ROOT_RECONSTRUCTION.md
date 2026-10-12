# Root reconstruction and exact validation criteria: symmetric-gradient line

Exact target: the imported question leaves domain and regularity unspecified. Original OWR36/2012 Rindler pp2247–49 explains published lower-semicontinuity/blow-up work; p2248 asks for structural information in an explanatory paragraph, then explains why a second blow-up gives the good separated form. It does not label a new conjecture. The literal imported complete-classification deficit must be checked against the full2020 theorem, and any arbitrary-domain globalization excluded explicitly.

## Universal smooth necessity and sufficiency

Use Eu=(Du+Du^T)/2 and a odot b=(ab^T+ba^T)/2. Distributionally, partial_k(Wu)_ij=partial_j(Eu)_ik−partial_i(Eu)_kj. Eu=0 implies all derivatives of Wu vanish, then Du is constant and u=Rx+c with R skew. This kernel fact is local on connected open sets and global on R^d; it does not require simple connectivity once the symmetric gradient is zero.

For independent a,b choose the first two spatial coordinate columns dual to a,b within their span and the remaining columns an orthonormal basis of its orthogonal complement. Let A be that invertible matrix. Then y=A^(-1)x, v(y)=A^T u(Ay) has E_yv=A^T E_xu(Ay)A, with A^Ta=e1 and A^Tb=e2. This is the correct congruence/displacement transformation; transforming only the spatial argument would be wrong. A^(-T)e1=a, A^(-T)e2=b, and transverse basis vectors are unchanged. Rigid motions transform to rigid motions under this congruence. Thus orthogonality of the original a,b is unnecessary.

For canonical independent Eu=(e1 odot e2)gamma, the identity for W12 gives partial_12 gamma=0 and transverse partial_1alpha gamma=partial_2alpha gamma=0. W1alpha has only its2-derivative proportional to partial_alpha gamma; W2alpha has only its1-derivative proportional to the same quantity. Their curl identities force every transverse partial_alpha gamma to be constant. Consequently gamma=h1(x2)+h2(x1)+2x·w, where w is constant transverse. This deduction holds on the whole space, or on an adapted rectangular neighborhood; it does not identify unrelated branches on disconnected slices of a nonconvex domain. Integrate H1'=h1,H2'=h2. The explicit field

    e1[H1(x2)+x2(x·w)] + e2[H2(x1)+x1(x·w)] − w x1 x2

has exactly that symmetric gradient: all e1/w and e2/w mixed quadratic terms cancel, leaving 2x·w times the symmetric product. Subtracting this field from any solution leaves a rigid motion. Transforming back by A gives precisely the displayed nonorthogonal candidate formula with w perpendicular to span{a,b}. This checks necessity as well as the easy differentiation direction.

For the canonical parallel case Eu=(e1 odot e1)gamma, Saint-Venant compatibility gives every transverse second derivative partial_alpha beta gamma=0. Hence gamma=h(s)+sum t_j k_j(s), s=x1. Integrating H'=h and P_j''=k_j gives

    e1[H(s)+sum t_j P_j'(s)] − sum e_j P_j(s),

whose mixed symmetric terms cancel. Subtraction is rigid. General nonzero parallel a,b span exactly the same matrix line as e odot e for a unit e; any scalar/sign can be absorbed in the signed coefficient. The candidate's explicit independent/parallel split avoids a naive reading of the source's printed a!=±b without normalization. If either vector is zero, Eu=0; in dimension1 the nonzero matrix line is all scalars and every smooth one-variable field is allowed.

## Signed-measure and regularity scope

The full DePhilippis–Rindler arXiv1911.01356v2 Theorem2.10 pp12–14 explicitly assumes u in BDloc(R^d) and a signed Radon measure nu, not only positive tangent measures. Its(i)/(ii) are the two product cases, with BVloc one-dimensional profiles and, in the parallel case, P_j locally Lipschitz with BVloc derivative. Full proof of these two clauses uses the same W identity and regularization; clause(iii) is a different ellipticity claim and not the target. The source's normalization wording should not be overread as making unnormalized collinear vectors independent. The independently derived smooth formulas avoid that ambiguity. A smooth u lies in BDloc automatically, so the actual queried sufficiently-regular whole-space case is a direct typed specialization.

For the stronger rough profile assertion, the compatibility identities remain distributional. Canonical independent coefficient distributions decompose into two one-dimensional distributions tensored with transverse Lebesgue measure plus a transverse linear density. A locally finite Radon coefficient implies the one-variable derivative components are locally finite Radon measures by testing against compact transverse functions of unit integral; integrating produces BVloc H_i. In the parallel case the transverse-affine distribution decomposes into h(s) and k_j(s); compact test functions with prescribed mass/first moments extract each Radon coefficient, yielding BV H and twice-integrated k_j with BV first derivatives. Subtracting the resulting L1loc field has zero Eu and is rigid. Separate signed-measure family must independently check this closure/extraction and the published source version before promotion. Positivity is unnecessary for these linear distributional arguments.

The2011 Rindler body gives the two-dimensional LD classification in Propositions4.7/4.9 and Example4.8; its good-blow-up theorem has more restrictive tangent/positive-measure hypotheses and is not substituted for2020 signed classification. The polynomial transverse cubic and parallel quartic examples verify why simpler guesses fail, not new counterexamples to an open problem. Local box normal forms follow the same compatibility integration; no global nonconvex-domain profile claim is justified.

## Falsifiable acceptance boundaries

Require actual published theorem/source compatibility, arbitrary scaling and nonorthogonal matrices, signed rather than positive measures, factors1/2 and transverse2, d1/zero/parallel edges, rigid-kernel statement, exact records and original0/5 source-triage budget. The old no-shared-queue claim must be dated/qualified because the exact head edits its queue row. Imported source_record cleanup self-contained/typography-only assurances must be treated as historical and qualified by the original missing domain. No false current global-domain claim, new discovery or paper/DOI. Reproduce both original diagnostic receipts in ignored copies; finite exact examples supplement the universal classification.

## Root independence record

Root read frozen SOURCE_STATUS and source_record, independently downloaded/read full original OWR passage,2020 theorem/proof and kernel lemma, and2011 relevant propositions before historical reviews or author code. The universal derivation above was developed before a signed-measure family's initial scope report arrived, but this file was persistently sealed afterward. Therefore this root artifact is NOT advertised as a strictly blind independent certificate. The three distinct family seals carry early independence; their conclusions are hypotheses until checked. No old author/historical diagnostic script or review has been read by root at this seal.
