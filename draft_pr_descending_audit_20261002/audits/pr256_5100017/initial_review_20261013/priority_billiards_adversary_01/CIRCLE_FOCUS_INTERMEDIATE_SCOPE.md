# Scope check of the doubled-normal circle/focus intermediate

Checkpoint: 2026-10-13T03:41:50.694315Z. This adds a mathematical comparison mechanism to the bounded literature audit. It does not certify novelty of the intermediate lemma and does not substitute for the mixed-support k307 calculation.

The candidate's Eq.(7) has unit-circle vertices Z_i=e^(i phi_i) satisfying

\[
 \cos(\phi_{i+1}-\phi_i)=u+v(X_i+X_{i+1}).
\]

Put m=(phi_i+phi_(i+1))/2 and k=cos((phi_(i+1)-phi_i)/2). The chord line is n(m) dot x=k. Since X_i+X_(i+1)=2k cos m and cos(phi_(i+1)-phi_i)=2k^2-1, its signed support equation is

\[
 k^2-v k\cos m=\frac{1+u}{2}. \tag{A}
\]

This is the tangent-line support equation of an axis-aligned ellipse centered at c=v/2 with semiminor B and semimajor A satisfying

\[
 B^2=(1+u)/2,\qquad A^2=B^2+c^2.
\]

Its two foci are 0 and (v,0). For negative k, reverse the line normal and support together; (A) is unchanged. Thus the usual unoriented tangency identification is valid on both signs.

For the candidate parameters d nonzero, D=F/d, H=(a^2+b^2)/2 and e=(a^2-b^2)/2, this gives

\[
 B^2=\frac{H^2-e^2}{D^2-e^2}>0,\quad
 c=\frac{e(H-D)}{D^2-e^2},\quad
 A=\frac{|HD-e^2|}{D^2-e^2}.
\]

The ellipse is strictly inside the unit circle. If d>0, then D=H+2lambda/d>H and

\[
 A+|c|=\frac{a^2}{D+e}<1.
\]

If d<0, then 1/(a^-2+b^-2)<lambda<b^2. The function D(lambda)=H+2lambda/(1-lambda(a^-2+b^-2)) increases from minus infinity to H-2a^2=-(H+2e) at the excluded upper endpoint, so D<-(H+2e), and

\[
 A+|c|=\frac{a^2}{-D-e}<1.
\]

The doubled-normal ordered vertices therefore belong to a unit-circle/focus-ellipse Poncelet configuration (with the repeated traversal inherited from antipodal pairing). The candidate telescope yields T_Z=2v S_Z, so its signed area centroid is v/3, or two-thirds of the caustic center.

This makes the intermediate a natural specialized circle/focus Poncelet centroid statement, in the same general circle-normalization territory as the classical Poncelet-centroid literature. The [Schwartz–Tabachnikov theorem and proof](https://arxiv.org/pdf/1607.04766) inspected in the priority audit establish a general conic locus, not an explicit identification of this stationary specialization in their stated theorem. This audit did not locate a separately stated historical fixed-CM2 theorem for this exact circle/focus configuration. Its priority is consequently unestablished, and no novelty claim should be made for the cyclic telescope or focus specialization.

Even if this circle/focus area-centroid specialization is already known, it gives only the pure doubled-normal moment. The target outer-side pedal has Q_i=z/2+h_i n_i-(bar(z)/2) n_i^2. Its area centroid requires the mixed cubic terms involving h_i n_i and n_i^2, and their combination with the signed pedal area. That remaining reconstruction is precisely the substantive calculation in candidate Section5. The intermediate alone is not a pre-existing proof of all-even arbitrary-M k307.

Rejected exploratory identification: an initial root message wrote k^2-2v cos(m)k=(1+u)/2 and center v. This missed the division by two in 2k^2-1=u+2vk cos(m). The corrected coefficient is v, center v/2, other focus v, and signed centroid v/3. The root acknowledged the factor error before using this comparison.
