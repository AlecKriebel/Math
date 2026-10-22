# Sealed initial assessment — independent candidate audit

UTC seal time: 2026-10-18T00:06:09.225632+00:00

Completion estimate: 20% of the assigned whole-package audit.

## Exposure and read order
1. Received parent instructions containing the candidate's frozen inventory, targeted adversarial concerns, edition history labels, and known credit/access boundaries. This is a supplied-candidate audit, not blind rediscovery. No root, older, or sibling verdict report has been opened before this seal.
2. Read repository AGENTS.md and PDF SKILL.md.
3. Read ALL publication/main.tex (first document evidence).
4. Independently fetched the EMS original from https://ems.press/content/serial-article-files/46609, extracted text, read Laghribi printed 248–251 in full including exact Question 2, and viewed all four source pages.
5. Rendered and viewed ALL four paper pages. Source rendering is the published PDF, not a newly compiled replacement. All text is readable with no clipping or overlap.
6. Wrote this initial assessment before any earlier report, supplement, program, manuscript credit body, or package verdict was read.

The chronological tool transcript supplies the read-order evidence; this signed-by-hash record reports it honestly but cannot cryptographically prove absence of other exposure. Metadata pinning is not reading.

## Exact target
Question 2 uses the projective quadric of B(v,v), with no positive-dimensional restriction. For every finite purely inseparable L/F, separable quadratic K/F, anisotropic bilinear Pfister B staying anisotropic over L, it asks equality of H_2^{n+1} kernels for L K(B) and the sum of the L, K, F(B) kernels. A binary anisotropic B is permitted: its projective quadric is integral and zero-dimensional with function field F(sqrt(t)). The candidate addresses the universal equality by one n=1 negative instance, not every n or every input.

## Independent reconstruction and attempted falsification
Take F=F2(b,z,s,t), beta^4=b, theta^2+theta=s^-1, B=<1,t>_b. b nonsquare implies [L:F]=4 and exponent 2. The odd s-pole proves genuine AS, and t has odd t-valuation over L, so B remains anisotropic, including after separable base extension.

Let f=1+beta^2 z, h=beta^2 z/f. In L, d(beta^2)=0, h dlog z=dlog f and h^2=bz^2/(1+bz^2). Two AS quotient relations give xi_L=[s^-2,f)=[s^-1,f), hence vanishing over LK. These are cohomology equalities, not an L-linear wp assertion.

For a hypothetical full three-summand decomposition, the whole cyclic relative Brauer kernel over K is [s^-1,c) with c in F*. Restrict to M=L(sqrt(t)); the L and Pfister summands both vanish. Thus [s^-1,f/c)_M=0 for every proposed decomposition coefficient c. This step really includes the third summand.

Complete to D=F2(beta,z,gamma)((s)), gamma^2=t. With pi=theta^-1, pi^2+s pi+s=0 and N(A+B pi)=A^2+sAB+sB^2. The pure leading valuations 2a,1+2b are unequal. For a<=b, 1+a+b>2a; for a>=b+1, 1+a+b>1+2b. Thus unit norms have a=0,b>=0 and square residue. Zero A or B gives the same necessity. This covers arbitrary integer valuations, not only polynomial coefficients. Multiplying by N(pi^r)=s^r handles every positive or negative s-order of c; any rational denominator contributes only to its residue c0 in F2(b,z,t)*.

Put S=F2(beta^2,z^2,gamma^2), R=F2(beta^4,z^2,gamma^2). Every c0 in R(z)* is u+vz, u,v in R, even for arbitrary rational denominators. Since z notin S, f=q c0 implies qu=1 and qv=beta^2; u=0 is impossible and v=0 is also impossible. Consequently beta^2=v/u would lie in R, contradicted by its odd valuation at beta^2=0. No counterexample to this necessity was found. The nonsplitting proof uses the norm criterion/general relative-Brauer theorem, whose precise primary-source scope remains to be checked.

At n=0, AS roots descend through purely inseparable extensions and rational fields; the anisotropic quasilinear projective chart is purely inseparable quadratic over a rational field, so the only kernel is K/F. The statement includes binary forms; zero-fold convention is explicitly separate. The exponent-one boundary correctly restricts over L before subtracting the base symbol: it does not claim a base equality d(1+uz)=u dz.

## Initial conclusion and exact gaps
Provisional mathematical PASS for the exact displayed counterexample, universal norm obstruction, full third summand, degree-zero assertion, and stated exponent-one boundary. No mathematical defect identified from the paper/original source alone. Success remains conditional on accurate natural Kato–Brauer/relative cyclic/norm dependencies and exact prior generator credit. Whole-package conclusion is deliberately OPEN: code, archives, replay, metadata, source custody, and history have not yet been audited. No novelty/firstness/global openness conclusion is made.

## Pins read before seal
[
  {
    "path": "publication/main.tex",
    "bytes": 13263,
    "sha256": "739e8dc4654df90d61b4e71d516537f8e3a4211595b53697eacd2075fe0c65e4"
  },
  {
    "path": "publication/output/pdf/mixed-kato-counterexample.pdf",
    "bytes": 71463,
    "sha256": "01ef963f6dbebc0c3aa91bfb10f13d293c983a46238c4465ae53bf4db99f1c96"
  },
  {
    "path": "reviews/package_03/sources/OWR-2016-5.pdf",
    "bytes": 514462,
    "sha256": "75a01e6e34988e672e0b6b48a56a3467ef7de59ee7fecc850a71e29110bf748c"
  }
]
