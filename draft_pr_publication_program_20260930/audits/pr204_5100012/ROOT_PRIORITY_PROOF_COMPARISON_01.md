# Root comparison with the centered-pedal preprint

UTC checkpoint: 2026-10-16T10:07:50Z. This is a positive-overlap comparison, not an absolute novelty certificate. Root read all five pages of Alper Ferudun, Center-Pedal Area Products in Elliptic Billiards, DOI10.5281/zenodo.23085904, and authenticated the78322-byte current primary PDF SHA2568ba41a5466bc289a9f714b57527f596fbe39b3422bc6bcf0a95d39bbde50c40c. The paper's Theorem1 and conventions cover the same least-period signed origin-pedal claim, including primitive stars and the complete-line construction. Its least-period qualification is explicit. A new-resolution or novel-theorem claim for our present note is therefore unsupported.

## Exact relationship of the trace formulas

To avoid confusing the two papers' alpha/beta conventions, write outer semiaxes a,b, caustic semiaxes alpha_c,beta_c, c^2=a^2-b^2, k=c/alpha_c, k'=beta_c/alpha_c, and v as in the submitted proof. Put W(u)=a^2-c^2 sn(u)^2. Our proof uses S(u)=sum_j dn(u+j delta), delta=2v. Ferudun uses the trace F(u)=sum_j dn(u+j delta)/W(u+j delta), after a real reflection-coordinate telescope for the center-pedal area.

The ordinary dn addition formula and the quarter-period shift give the pointwise meromorphic identity

    dn(u+K-v)+dn(u+K+v)=2ab dn(u)/W(u).

Indeed the addition denominator after shifting u by K is

    dn(u)^2-k^2 cn(u)^2 sn(v)^2
      =cn(v)^2/alpha_c^2 * W(u),

and k' dn(v) alpha_c^2/cn(v)^2=ab. These equalities use a=alpha_c dn(v)/cn(v), b=beta_c/cn(v), and dn(v)^2=1-k^2 sn(v)^2. Summing over a closed delta-orbit reindexes the two shifted dn sums, so

    F(u)=S(u+K+v)/(ab).

Consequently the explicit center-pedal coefficient in Ferudun's Lemma3 implies

    B(u)=C_T S(u+K+v),
    C_T=sqrt(lambda)*sqrt(a^2-lambda)
        *[(a^2+b^2)a^2b^2-lambda(a^4+b^4)]/(2a^3b^3).

This is the same coefficient as our residue expression alpha_c^2 sn(delta)(dn(delta)+k'^2)/(1+dn(delta))^2. Standard Jacobi double-angle identities give the equivalence. Thus an explicitly evaluated coefficient is not a defensible new-formula claim relative to this primary result. The priority family independently checked the pointwise identity, two exact algebraic residuals, and closed-trace diagnostics after receiving Root's comparison.

Our presentation directly computes the pedal foot, cancels its apparent double poles between incident area terms, and compares two-pole functions on a reduced torus. The centered preprint first telescopes real reflection coordinates and then removes complementary poles of the area times its trace. These are different proof organizations of the same theorem within established Jacobi and meromorphic methods. No claim that this organization is historically new, logically independent of all earlier work, or a stronger theorem follows from this comparison. The original PR203/204 sharing of author proof material also remains disclosed.

## Chronology and editorial consequence

The original PR204 server creation time is2026-10-01T05:28:14Z and its frozen HEAD is551a524e2db65fec90684485ef676d0b4179378d. Ferudun's Zenodo record creation is2026-10-01T15:39:54.821511Z and DataCite registration is2026-10-01T15:39:55Z; its manuscript and website bear the date1October2026. These records document contemporaneous October1 manuscripts/submissions. Repository creation/commit dates, a website's stated online date, and DOI registration do not by themselves establish discovery time, earliest worldwide public availability, literal simultaneity, or independence. No such conclusion will be asserted.

Under the user's standing authorization to publish carefully attributed alternative research notes, the appropriate potential package is an alternative proof/exposition with the exact overlap prominent, the documented timeline, necessary least-period qualification, and reproducible verification materials. It must not be framed as the first resolution of a problem still open today. The bounded priority family's final report and Root editorial acceptance are still required before manuscript promotion. This note alone authorizes no publication, PR or tracker mutation.
