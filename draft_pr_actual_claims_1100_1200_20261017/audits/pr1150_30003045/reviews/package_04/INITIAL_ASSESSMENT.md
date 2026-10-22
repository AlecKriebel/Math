# Sealed initial assessment — package review 04

UTC: 2026-10-18T00:13:46.251040+00:00. Completion: 22% of this whole-package review. Supplied-candidate independent checking, not blind rediscovery. Before this seal I have not read root verdict reports, earlier review reports, sibling review reports, proof/repair history, package runner or builder. The delegation supplied target frozen hashes, substantive checklist topics and descriptions of historical issues; that parent-context exposure limits causal independence. No claim of perfect isolation is made.

## Read order and evidence

1. Created this review folder and wrote `.gitignore` first (private/, sources/, tmp/, rendered/, __pycache__). Read all workspace AGENTS.md and the PDF skill.
2. Read ALL 13,263 bytes of publication/main.tex via complete cat output, from document class through end document.
3. Rendered and personally viewed ALL four frozen paper pages, in order 1–4, at 110 dpi. Text, equations, references and disclosure are legible with no clipping/overlap observed.
4. Independently fetched https://ems.press/content/serial-article-files/46609 (not reused from the package). Extracted text, read Laghribi's complete contribution from printed 248 through 251; rendered and viewed PDF pages 34–37 (printed 248–251), including Question 2 and the projective-quasilinear-quadric definition. Only this contribution is substantively read, not all 52 report pages.
5. Reconstructed and attempted to falsify the supplied claim below, without reading earlier verdicts.

## Exact claim and independent reconstruction

Characteristic two, F=F2(b,z,s,t), four independent variables, L=F(beta), beta^4=b; K=F(theta), theta^2+theta=s^-1; B=<1,t>_b. L/F has degree 4 and exponent 2, K/F is genuine separable quadratic, B_L anisotropic. xi is s^-4 bz^2/(1+bz^2) dlog z. Claim: xi is killed by LK and hence LK(B), while xi is outside the full sum of the L, K and F(B) kernels in H2^2(F). The original question includes binary anisotropic B: its projective quadric is the integral degree-two closed point of P1, and its function field is F(sqrt(t)). The original source gives no exclusion of the binary case. A counterexample at n=1 is an allowed negative answer.

I independently checked the following sequence.

* b has odd b-order, so is nonsquare. In characteristic two X^4-b then has degree-4 purely inseparable minimal polynomial. s^-1 has odd negative s-order; no x^2+x can have that order. t keeps odd t-order in F2(beta,z,s,t), so B_L stays anisotropic. A separable extension cannot introduce its purely inseparable square root.
* In L, f=1+beta^2 z and h=beta^2 z/f give dlog f=h dlog z and h^2=bz^2/(1+bz^2). The logarithmic Artin–Schreier relations identify xi_L with s^-2 h dlog z=[s^-2,f)=[s^-1,f), hence it vanishes over LK. This uses an additive quotient relation, never L-linearity of wp.
* Let gamma^2=t and M=LF(B)=F2(beta,z,s,gamma). Any three-summand decomposition xi=x+y+w restricts to xi_M=y_M because x and w die in M. Subject to verification of the full relative cyclic Brauer-kernel theorem, y=[s^-1,c) for an arbitrary c in F*, so [s^-1,f/c)_M=0 and f/c must be a norm.
* Complete at s: D=k'((s)), k'=F2(beta,z,gamma). The Artin–Schreier extension remains genuine. With pi=theta^-1, pi^2+s pi+s=0 and N(A+B pi)=A^2+sAB+sB^2. For nonzero A,B, writing a=v(A), b'=v(B), 2a and 1+2b' have opposite parity, and 1+a+b' exceeds their minimum. Thus a unit norm has a=0 and b'>=0 and square residue Abar^2. A=0 and B=0 do not provide exceptions. This argument does not import a perfect-residue or defect assumption.
* For every c in F*=k(s)*, including arbitrary rational denominators and negative s-order r, c=s^r c0(1+O(s)), c0 in k*=F2(b,z,t)*. Multiplying f/c by the norm N(pi^r)=s^r produces a unit norm. Therefore f/c0 must lie in k'^2. No restriction to finite samples, polynomial slots or r>=0 appears.
* Put S=k'^2=F2(beta^2,z^2,gamma^2), R=F2(beta^4,z^2,gamma^2). Every c0 in k=R(z) has a unique expression u+vz with u,v in R, rational denominators included. z is outside S because z^2 has odd z^2-order there. If f=q c0 for q in S*, comparison of 1,z gives qu=1 and qv=beta^2. Thus u nonzero and beta^2=v/u in R, contradicting the odd beta^2-order versus even orders in R. v=0 also immediately contradicts qv=beta^2. This rules out every c and includes all three original summands.

## Boundary and source scope checks

For n=0, a separable Artin–Schreier root cannot first appear under purely inseparable extension or a rational-function extension. For anisotropic quasilinear positive dimension d>=2, the projective quadric field is a purely inseparable quadratic extension of a rational field in d-2 variables; this remains so over KL since separable extension preserves quasilinear anisotropy. Roots descend to KL, then to K. Thus the composite kernel is exactly the K kernel, with the other two zero. The stated zero-fold convention is separated and does not form a function field of an empty quadric.

The exponent-one boundary only asserts xi_L=[s^-1,1+uz)_L when b=u^2 in the base and beta^2=u; this suffices for membership in the sum of the L and K kernels. It correctly avoids an unsupported base single-symbol equality, since du may be nonzero. Taking the Pfister slot z instead kills dz, so the independent t slot is essential.

The text expressly credits the ALO generator and makes no firstness/global-openness claim. Its exact ALO identification and the Kato/Brauer/norm dependencies still require primary-source authentication in the post-seal package audit. Paper disclosure of extensive AI, initial parent exposure, no external human review and no formal proof certification is visible. No counterexample or proof gap was found in this independent reconstruction; this is a provisional mathematical pass contingent on the stated standard dependencies, not yet a package verdict.

## Seal inputs

```json
[
  {
    "path": "/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045/publication/main.tex",
    "bytes": 13263,
    "sha256": "739e8dc4654df90d61b4e71d516537f8e3a4211595b53697eacd2075fe0c65e4"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045/publication/output/pdf/mixed-kato-counterexample.pdf",
    "bytes": 71463,
    "sha256": "01ef963f6dbebc0c3aa91bfb10f13d293c983a46238c4465ae53bf4db99f1c96"
  },
  {
    "path": "/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045/reviews/package_04/sources/owr2016-5.pdf",
    "bytes": 514462,
    "sha256": "75a01e6e34988e672e0b6b48a56a3467ef7de59ee7fecc850a71e29110bf748c"
  }
]
```

The seal covers this file's preexisting content plus the three input identities; an external hash receipt is written immediately afterward. Review evidence remains outside the frozen source archive, so this is not circular release attestation.
