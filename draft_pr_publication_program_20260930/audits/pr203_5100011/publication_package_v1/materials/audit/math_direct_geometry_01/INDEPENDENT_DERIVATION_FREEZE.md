# Independent direct-geometry derivation freeze

Frozen at 2026-10-16T07:33:09.205703+00:00, before reading original proof or favorable verdict.

## Universal signed pedal-area identity

Let the ordered original side lines be L_i: n_i dot X=h_i, |n_i|=1, cyclic indices. Either normal orientation is allowed independently. The perpendicular foot from M is Q_i=M+(h_i-n_i dot M)n_i. Write d_i=n_i cross n_(i+1) and s_i=n_i dot n_(i+1). Translation invariance of cyclic signed shoelace area gives

B(M)=1/2 sum d_i (h_i-n_i dot M)(h_(i+1)-n_(i+1) dot M).

Consequently

B(M)=B(0)+ell dot M+C |M|^2,
B(0)=1/2 sum d_i h_i h_(i+1),
ell=-1/2 sum d_i [h_i n_(i+1)+h_(i+1)n_i],
C=1/4 sum d_i s_i=1/8 sum sin(2 delta_i).

Proof of isotropy: put M=(r,0) by rotating coordinates and n_i=(cos alpha_i,sin alpha_i). Each quadratic summand obeys

sin(alpha_(i+1)-alpha_i) cos alpha_i cos alpha_(i+1)
 =1/4[sin(2alpha_(i+1))-sin(2alpha_i)+sin(2alpha_(i+1)-2alpha_i)].

The first two terms telescope. This is valid for arbitrary side-line lists, including stars and repeated lists, without billiard or central-symmetry assumptions. It makes no division by B, A, C, or |M| and therefore includes zero pedal area and C=0.

If P_(i+m)=-P_i and the normals are chosen n_(i+m)=-n_i, then h_(i+m)=h_i, d_(i+m)=d_i, s_(i+m)=s_i, and ell=0. Thus B(M)=B(0)+C|M|^2 for a centrally paired polygon. Under reversal all of A,B(0),C change sign; A B(M), A B(0), AC are unchanged. Scaling all lengths and M by t scales A,B by t^2 and their product by t^4; C is dimensionless.

## Precise remaining billiard task

Assuming central pairing is justified for every primitive even periodic trajectory with an elliptical caustic, all-M phase independence is equivalent to both scalar quantities A B(0) and AC being phase-independent. Necessity follows by evaluating M=0 and one nonzero fixed M, sufficiency by the displayed identity. This equivalence remains valid at zero pedal area and does not assume A nonzero. If A=0 at an exceptional phase, all products at that phase vanish, which is a substantive constraint rather than grounds for division.

Central pairing is not proved here. Neither scalar invariant is proved here. In particular, identifying a Steiner curvature center at the origin alone proves only radiality, not phase independence. Promoting either scalar invariant without a checkable proof transfers the central difficulty and is BLOCKED.

## Primary scope intake, after independent plan

Read direct local arXiv v11 PDF pp.1-7 and separate journal PDF pp.341-346. The v11 Section 3.3 p.4 defines feet from M onto original trajectory sides; Eq.(1) p.3 defines signed cross-product area. Table 3 p.6 row k203,a prints A A_m, N=0 mod 4, M=all, value=?, proven=?. Journal Section 3.3 p.344, Eq.(1) p.343, Table 3 p.346 give the matching claim. Neither row prints 'primitive'. Both papers' introduction defines physical reflection by normals to the outer ellipse and the pair as confocal ellipses. No stronger novelty or verification claim is inferred from the question marks.

Completion toward this family's universal direct proof: 20%; strongest verified result is the arbitrary-polygon radial quadratic and exact two-scalar reduction conditional on central pairing. Original proof has not yet been read.
