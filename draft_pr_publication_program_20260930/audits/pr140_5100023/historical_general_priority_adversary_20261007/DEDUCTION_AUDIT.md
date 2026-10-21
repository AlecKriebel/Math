# PR140: deduction audit of the historical centroid route

This is an independently constructed reviewer deduction, not a located historical proof of k405. The accepted candidate's opposite-edge antipedal identity is an explicit premise. The checks below audit which old theorems can be used after that premise is supplied; they do not rerun the mathematical gate.

## 1. The old transformation really exists

Let D=diag(a,b), let P_i be an elliptic billiard orbit, and let w_i be its outgoing Euclidean unit direction. Set Z_i=D w_i. Gutkin–Tabachnikov, *Billiards in Finsler and Minkowski geometries* (2002), Corollary 7.7, printed p.298, applies with their operator A=D^(-1), boundary M equal to the ellipse and N equal to the unit circle. It gives the transformed phase points

    (Z_i, u'_i) = (D w_i, -D^(-1) P_(i+1)).

Their Theorem 7.1, Proposition 7.3 and Corollary 7.6, pp.296–298, prove the orbit correspondence and periodic length preservation. Their Example 7.8, p.299, attributes this elliptic special case to Veselov (1988/1991). The originals of those two Veselov papers were not read in this family. The 2002 source body was obtained from a PDF linked by Tabachnikov's own publications page, and its relevant rendered pages were read.

Akopyan–Schwartz–Tabachnikov (2020 preprint; 2020 online publication; 2022 volume), Lemma 3.1/Remark 3.2, published pp.1318–1319, explicitly revisit the same skew-hodograph construction. None of these statements describes an antipedal centroid.

The indexing/orientation can also be checked directly. Reflection implies

    w_(i-1)-w_i is a positive multiple of D^(-2) P_i.

Consequently Z_i-Z_(i-1) is directed along -D^(-1) P_i. These vectors have norm one because P_i lies on the ellipse. At Z_i the difference of incoming/outgoing unit directions is proportional to D^(-1)w_i=D^(-2)Z_i, the ellipse's normal. Thus this is an ordinary billiard in the same ellipse, rather than an arbitrary affine image to which Euclidean reflection was silently transferred. The cited orbit isomorphism preserves least period and smoothly maps a family to a family.

The transformed Joachimsthal constant is the same. With the outgoing convention, w_i dot D^(-2) P_i=-J and w_i dot D^(-2) P_(i+1)=J. Therefore

    u'_i dot D^(-2) Z_i = -J,  J=sqrt(lambda)/(ab).

The admissible caustic parameter stays lambda. Length preservation is explicit in the old source and also follows by summing the reflected-direction differences: if delta_i is the reflection angle and H_i the support of the outer ellipse, then the transformed edge length is 2 H_i sin(delta_i). Bialy–Tabachnikov Theorem 2.2, preprint p.3, makes its sum the original L. There is no new length invariant in this deduction.

## 2. What the old pedal theorem says

Bialy–Tabachnikov, *Dan Reznik's identities and more*, Theorem 4.1, published pp.1348–1349 (preprint pp.6–7), fixes an arbitrary point p and takes its perpendicular feet R_i on the **boundary tangents at the orbit vertices**. It proves that the unweighted centroid of these feet is fixed over the billiard family. The source identifies its cases as k302/k306. This is not the antipedal intersection construction of k405.

Applying that theorem to the genuine transformed orbit Z_i is legitimate. Identifying the resulting mean with the desired antipedal mean is the extra step, not part of that theorem.

## 3. Exact additional antipedal-to-pedal lemma

Use the candidate's chord midpoint angle t, C=cos(t), S=sin(t), and

    g=a^2 S^2+b^2 C^2,  w=(-aS,bC)/sqrt(g),
    Z=(-a^2 S,b^2 C)/sqrt(g).

The outward unit normal at Z is n=(-S,C), and its tangent is n dot X=sqrt(g). Choose any fixed nonzero d and p=(d,0). The perpendicular feet onto the tangents at Z and -Z are

    R_+=p+[sqrt(g)-p dot n] n,
    R_-=p-[sqrt(g)+p dot n] n.

Their mean is

    (R_++R_-)/2=(d C^2,d SC).

Put h=+/-sqrt(a^2-b^2), f=(h,0), and K=a^2 b^2-lambda(a^2-b^2). Candidate Eq.(8), divided by two, asserts

    (Q_f(A,B)+Q_f(-A,-B))/2
      =(-h+hK C^2/[a^2(b^2-lambda)],
                       hK SC/[ab(b^2-lambda)]).

Hence the additional bridge is the identity

    mean(Q_f opposite pair) = -h e_x + T_h mean(R opposite pair),

    T_h=diag(hK/[d a^2(b^2-lambda)],
             hK/[d ab(b^2-lambda)]).

Summing antipodal pairs in a primitive even orbit gives

    C_f = -h e_x + T_h C_R.

This proves constancy from the old pedal theorem **after** the focal opposite-edge lemma has been established. The focal lemma requires solving the two antipedal line systems, adding opposite-edge answers, and using h^2=a^2-b^2 plus the confocal tangency relation. It is the candidate's substantive geometric/algebraic step. An arbitrary-pole extension is not being asserted.

I did not locate that complete focal antipedal/skew-pedal bridge in the inspected accessible prior primary literature. The foot-pair calculation above is my deduction; its equality to the antipedal pair uses the candidate's accepted identity. It is not a previously published theorem just because each surrounding dynamical tool is old. Conversely, failing to locate it does not certify novelty.

## 4. The explicit coefficient once that lemma is supplied

For the transformed orbit, the boundary-normal angle is psi=t+pi/2. Bialy–Tabachnikov Corollary 3.2, published p.1346 (preprint pp.4–5), gives

    sum cos(2psi_i)=[L/J-N(a^2+b^2)]/(a^2-b^2),
    sum sin(2psi_i)=0.

Thus the transformed pedal centroid is (d H,0), where

    H=1/2 [1-(L/J-N(a^2+b^2))/(N(a^2-b^2))]
     =a^2/(a^2-b^2) [1-bL/(2a sqrt(lambda) N)].

Combining this with the **extra bridge** recovers exactly the candidate's focal formula. This demonstrates that no new conserved normal tensor is necessary. It does not demonstrate that a historical author had already proved the antipedal coefficient or answered k405.

## 5. Why other classical conic theorems do not close the gap automatically

Conic polarity and the antipedal operation are different. In focus-centered coordinates q=P-f, the antipedal line is

    q dot (Q-f)=|q|^2.

It is the ordinary unit-circle polar of q/|q|^2, not of q. A focus-polar description of the original ellipse has radial form r=p/(1+e cos(theta)). Inverting its vertices first produces rho=(1+e cos(theta))/p, a limaçon, with equation

    [p(X^2+Y^2)-eX]^2=X^2+Y^2.

For e nonzero this is not the ordinary conic-polar construction used in the inspected Poncelet contact-polygon centroid theorems. A separate transformation would have to be supplied.

Tsukerman's *Discrete Conics*, Definition 1.1 and Section 4, imposes equal focal angular steps or equally spaced points on a circle in its relevant negative-pedal results. An elliptic billiard's raw vertices do not meet those hypotheses. Mapping an ellipse to a circle by unequal axial scales does not preserve perpendicular lines. Raw focal rays are also not the outer ellipse's normals: at a=5,b=3,f=(4,0),P=(0,3), their determinant is -4/3.

The ordinary Poncelet centroid theorem of Schwartz–Tabachnikov concerns vertices of a Poncelet polygon; its contact-polygon extension uses an ordinary conic polarity. It does not say that every rationally constructed derived polygon has a fixed centroid. Weill's homothetic-conic contact-centroid theorem also does not apply directly to a noncircular confocal pair: equality of its axial scale ratios would force lambda(a^2-b^2)=0.

## 6. Bounded checks and historical interpretation

The standalone bridge_controls.py independently checks 18 exact identities in normal and optimized Python, using explicit failures rather than assertions. They check the transformed ellipse/normal, foot-pair calculation, affine bridge relative to accepted Eq.(8), H conversion, Joachimsthal signs, and specific hypothesis obstructions. They perform no orbit search, no author-verifier import and no claim that numerical samples prove all periods. The original unsealed control precursor and its receipts were preserved privately before a readability-only cleanup; final receipts bind the final code.

The strongest historical conclusion is: the dynamical transformation, pedal-centroid constancy and normal-harmonic sums are published prior tools; an additional focal antipedal identity is needed for the target and was not located in this bounded primary-source audit. The target's origin case follows from classical central symmetry. Novelty of the focal bridge and full k405 result remains undetermined until the overall priority assessment is completed.

