# A checkable prior-component deduction of k404

Audit author: independent recent-priority adversary for PR255. This is an audit derivation, not a new discovery claim.

Fix a>b>0 and 0<lambda<b². Let P be any primitive billiard family with strict confocal elliptical caustic and least period N congruent to 2 modulo 4. All areas are ordered signed shoelace areas. Let A be the original orbit area, p_F its original-side pedal area at either boundary-ellipse focus, and q_F its original-vertex antipedal area. Write c²=a²-b².

The authenticated original Ferudun archive, DOI 10.5281/zenodo.23079799, Lemma 4, gives q_F=R A for any centrally paired elliptic-caustic trajectory, where

    R = [a²b²(3b²-a²)+lambda(a²-b²)²]
        /[2a²b²(b²-lambda)].

The denominator in R is strictly positive. The lemma's own proof pairs opposite edges and telescopes an endpoint difference. It does not use the main theorem's quarter-period permutation, and therefore is not confined to N divisible by four.

The immutable original PR250 proof, SHA256 ac486431077ab33493c78dc83ce3940648a7121e72015da8563e4dc6fea7d124, Sections 1 and5, gives

    p_M=(c0+c2|M|²) A,

for all fixed real M and all primitive coprime stars of least period N congruent to 2 modulo 4 in this same strict domain. The proof establishes A>0 in positive winding orientation. Thus, at either focus,

    p_F=c_F A,       c_F=c0+c2 c².

The components already imply q_F/p_F=R/c_F wherever p_F is nonzero. The remaining domain check is elementary and independent of any claimed invariant:

Scale the caustic semiaxes to alpha>beta>0. In the credited Stachel parametrization let its contact normals be n(u)=(-sn(u)/alpha,cn(u)/beta), with modulus k satisfying k²=1-beta²/alpha². The primitive step delta=4K tau/N lies strictly between 0 and 2K. Direct differentiation gives det(n,n')=dn(u)/(alpha beta)>0, and n(u+2K)=-n(u). Therefore its lifted unit-normal angle psi increases strictly by pi in 2K, and

    0<psi(u+delta)-psi(u)<pi

for every real u. Both foci lie inside the caustic, because a²-lambda-c²=b²-lambda>0. The foot on a caustic tangent from such an interior focus has

    q_F(u)-F=rho(u) n_hat(u),      rho(u)>0.

Consequently every consecutive determinant of the translated feet is positive:

    det(q_F(u)-F,q_F(u+delta)-F)
      =rho(u)rho(u+delta)sin(psi(u+delta)-psi(u))>0.

Closure treats the final edge with the same lifted angle; no simplicity or winding-one hypothesis is used. Hence p_F>0 for every real phase and c_F>0. The antipedal intersections are finite: any dependent consecutive focal rays would make an actual caustic-tangent chord pass through its strictly interior focus, which is impossible.

It follows throughout the whole target domain that

    q_F/p_F=R/[c0+c2(a²-b²)],

a real phase-independent constant, equal at the two foci. R may be zero or negative. Reversing traversal negates both areas; repetitions of already admissible primitive cycles preserve the ratio. Neither padded odd cycles nor hyperbolic or degenerate caustics are included.

This establishes exact mathematical coverage by a combination of earlier components, with the harmless focal denominator check explicitly supplied. It does not show that a single earlier publication named k404, that anyone previously wrote this particular combination, or that the underlying proofs are globally first.

Primary links:

- [Ferudun original archived source](https://zenodo.org/records/23079799/files/arxiv_source.zip)
- [Ferudun reading copy](https://eulersolve.org/papers/amr-050-0021/paper.pdf)
- [Immutable PR250 full proof](https://github.com/AlecKriebel/Math/blob/ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3/unsolved_math_prioritization/attempts/5100013/PROOF.md)
