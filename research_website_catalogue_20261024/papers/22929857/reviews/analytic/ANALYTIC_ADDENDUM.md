# Analytic closure after the independent reconstruction seal

The original EARLY_RECONSTRUCTION and its seal remain unchanged. The checks below were completed after that seal and do not use archived/current review opinions.

## Actual monotonicity throughout time

The displayed estimate q_t Lip(Φ) by itself bounds each time against the initial map; a decreasing upper envelope alone would not logically establish pairwise monotonicity of the actual Lipschitz constants. The formula supplies the stronger fact directly.

For r,s∈[0,1), multiplying out the rational expressions gives

F_r(F_s(W))=F_((r+s)/(1+rs))(W).

Indeed the numerator and denominator, after the common (I+sW) inverse cancels, are respectively (1+rs)W+(r+s)I and (1+rs)I+(r+s)W. Only functions of the same W commute here. For0≤s≤t<1, choose r=(t−s)/(1−st)∈[0,1). The normalized image of H_sΦ remains in the semicircle (as checked by the scalar spectral flow), and H_sΦ(p)=A. Consequently H_tΦ=H_r(H_sΦ) and

Lip(H_tΦ)≤q_r Lip(H_sΦ)≤Lip(H_sΦ).

The terminal time t=1 is constant and therefore has Lipschitz constant0. This closes a potential title/interpretation ambiguity: the actual Lipschitz constant is nonincreasing in time, not merely bounded by a decreasing envelope. This corollary is elementary from the same formula; it is not a proposed research follow-up or novelty claim.

## Explicit independent noncommuting input family

Let X and Z be the two real Pauli matrices, so X²=Z²=I, XZ=−ZX. On the unit-round circle put

Φ(s)=exp(i a(s)X) exp(i b(s)Z), a(s)=sin(s)/8, b(s)=(1−cos(s))/8.

It is periodic and Φ(0)=I. Right-trivializing the derivative gives a skew-Hermitian matrix with two orthogonal Pauli components of coefficients a'(s),b'(s). Thus its op speed is sqrt(a'²+b'²)=1/8, and HS speed is√2/8. The intrinsic Lipschitz constants equal these sup speeds because the upper bound comes from shortest source arcs and the lower bound from the local metric derivative. It therefore lies safely inside both actual theorem domains. Its tangent does not generally commute with its value.

The independent controls compare the output differential against q_t times these exact input speeds, and compare actual principal-eigenangle intrinsic distances over every pair in a64point circle grid and seven times. This tests the distinction between matrix chordal and unitary intrinsic distances. The worst floating-point excess is reported, rather than treating numerical nonnegativity as certified. The separate exact Gaussian-rational controls validate the noncommuting tangent congruence and its resolvent factor certificate in175matrix/time cases with875tangent directions, plus explicit wrong-order controls. Neither campaign establishes the universal theorem by enumeration.

## Primary interfaces and provenance

The actual author-hosted Gromov2017 body, printed35–36, contains the specific strict1/2 question with dependence on the entire input and its preceding standard bi-invariant2π normalization. The neighboring Lip<1 discussion is distinct. No application to general sphere fibrations follows from the reviewed theorem. The target specifies the two actual metrics, avoiding the false inference that one shortest-loop normalization determines every bi-invariant metric.

Neretin2011, printed42/physical54, §1.7.9 and Theorem7.5, gives the classical Cayley chart with an i factor converting skew-Hermitian to Hermitian coordinates. Its displayed inverses require the usual chart domain. The target supplies I+W invertibility through ReW≥0, and derives its scaling identity algebraically. It does not import a new cohomology/topology theorem, claim the Cayley chart new, or require an unproved arbitrary-matrix operator-Lipschitz functional-calculus principle.

All four target manuscript pages and its entire TeX were read before the early seal. The only supplied executable bodies subsequently read/replayed are verification/verify_exact.py and verify_numeric.py; both have an explicit output argument directed into this analytic folder. No release/build script or archived audit/current review opinion was read or run. Source exact results agree after removing generation time/Python version; numerical case design/counts agree, and this environment reproduces the reported residual maxima, but no cross-platform floating-byte reproducibility is required or claimed. Their limitations are accurately stated in the manuscript.

No central mathematical defect has been found. Priority and current worldwide openness remain unknown under bounded reading/search. No follow-up is proposed. This remains AI-assisted independent mathematical review, not external human peer review or formal proof-assistant certification.
