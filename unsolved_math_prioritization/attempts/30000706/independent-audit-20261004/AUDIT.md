# Independent adversarial audit: rank 606 / problem 30000706

## Verdict

**PASS as an explicitly incomplete, bounded partial investigation.** No substantive mathematical error or required correction was found in Propositions 1–8 or the example calculations. This is not a solution certificate, formal verification, novelty endorsement, or expert peer review. The appropriate status remains **unsolved, 5/5**.

The audit independently reconstructed the arguments, checked the potentially fragile degree-two fiber classification, verified the stated source hypotheses, reran the author verifier in an isolated copy, and added a separate diagnostic implementation. All seven frozen payloads match their manifest. The manifest itself has SHA-256:

`cb3fd99d35566ff256249f4eb19f0aa8036bab8892d7575899cb5218400d0bc1`

The author replay passes **165/165**, and its output receipt is byte-identical to the frozen receipt. The separate audit script passes **280/280** checks. These counts describe bounded diagnostics, not 445 independently proved mathematical theorems.

Audit date: 2026-10-04 UTC. The frozen public directory was not edited. No repository, branch, queue, or other remote write was performed. Source PDFs and rendered source pages remain private and are excluded from the audit publication files.

## 1. Scope and source fidelity

The pinned target record and the original problem agree: classify plane meromorphic pairs sharing four distinct values, one of them infinity, with the stated Mues function equal to one. The record hash matches the source-provenance file. The primary source was inspected as extracted text and independently rendered at PDF page 55, printed page 541. The author accurately treats its proposed exhaustion by known examples as a presumption rather than a theorem. The finite shared values, nonconstant functions, distinct functions, and entire-plane domain used in the report are appropriate. Nonconstant and distinct are also forced by the nonzero differential identity wherever it is defined.

Primary source: [Oberwolfach report](https://ems.press/journals/owr/articles/1460), DOI 10.4171/OWR/2007/09; [PDF](https://ems.press/content/serial-article-files/46093).

The catalogue itself was not independently made accessible. The author's saved response records HTTP 403. The audit checked the complete pinned record against the original source rather than interpreting the inaccessible web page as evidence.

The chronology correction is sound. The publisher identifies Huang–Du's paper as volume 24, issue 4, October **2004**, pp. 529–535. The frozen official Crossref record agrees, including its exact byte count and hash. This citation cannot honestly be called post-2007 work merely because its DOI contains “17.” [Publisher record](https://www.sciencedirect.com/science/article/pii/S0252960217302345).

The audit checked the frozen primary papers and all six listed source hashes/byte counts. The 2011 survey's cited 2012 publication details also agree with the author's bibliography in the 2025 paper. Some direct web opens failed; the audit does not turn those failures into claims about the mathematics or availability of the local PDFs.

## 2. Local multiplicities and coefficients: Propositions 1–2

**Accepted.** Put D=P'(a). For a finite shared value, the derivative-product and denominator exponents cancel to leave the exponent contributed by the difference, less two. If p<q, the result is

psi = (p q A^2 / D^2) t^(2p−2)(1+O(t)).

If q<p, replace A,p by B,q as appropriate. If p=q with unequal leading coefficients, the leading coefficient is p^2(A−B)^2/D^2 and the exponent is 2p−2. With equal leading coefficients and first differing order k>p, the exponent becomes 2k−2. Thus a nonzero constant forces exactly the cases and coefficient equations in Proposition 1; an identically zero difference germ is excluded by the identity theorem.

The finite U formulas are also correct, including their signs: A/D for (1,q), −pB/D for (p,1), and (A−B)/D for (1,1). Consequently U^2=p/q and both factors are removable, finite, and nonzero at each finite shared point.

At a common pole with p<q, the denominator contributes t^(−3p−3q), the two derivatives t^(−p−q−2), and the squared difference t^(−2q). The resulting expression is p q A^(−2)t^(2p−2). The equal-order coefficient and residue equation in the report follow in the same way. If the pole principal parts cancel to difference order at least −p+1, the Mues expression has order at least 2p, precluding a nonzero constant.

After excluding this cancellation, ord(U)=2p−max(p,q)−1 is correct. This gives zeros or poles only at unequal common poles. Away from the four shared fibers the factors are holomorphic, and psi=1 prohibits a zero derivative or a coincidence. In particular, the report correctly rejects the tempting but false assertion that U and V must always be entire. Gundersen's U=1−t and V=8/(1−t) exhibit the failure directly.

The new endpoint and cancellation diagnostics cover 128 generic endpoint models and 24 leading-cancellation models. These supplement the unrestricted exponent argument; they do not replace it.

## 3. Rational obstruction and Möbius subclass: Propositions 3–4

**Accepted.** The rational obstruction considers all possible values of a rational h at infinity. If h approaches a root of P, h'/P(h)=O(1/z), with h^k bounded. If h approaches any other finite value, h'=O(1/z^2). If h has a pole of order m at infinity, h^k h'/P(h) has order O(z^(m(k−2)−1)), hence O(1/z) for k=0,1,2. The expansion of (f−g)^2 then gives psi=O(1/z^2), contradicting psi=1. No sharing hypothesis is used or smuggled into this proof.

The target transformation factors are correct. An affine target map contributes alpha^(−2). Inversion centered at a finite shared root a contributes P'(a)^2. Combining these with the chain rule gives precisely the constants c_T in Proposition 4, including the factor four for inversion centered at a base root ±1. The audit directly checked normalized transformed exponential pairs for each of the four possible locations of the target pole, independently of the author's symbolic transformation-ratio check.

The omission argument is complete. Every nonfixed shared value of M is omitted by f, and its inverse image under M is omitted too. There must be at least two nonfixed shared values because a nonidentity Möbius map has at most two fixed values. Picard allows at most two omitted values. Therefore there are exactly two omitted shared values and two fixed shared values. The inverse image condition forces the omitted pair to be invariant; because neither is fixed, M exchanges them. After normalization M(w)=1/w and the fixed points are ±1.

The normalized f is holomorphic, zero-free, and therefore exp(h) for an entire h; g=exp(−h). Its Mues expression is h'^2. The correctly transformed identity forces h'^2 to be a nonzero constant, hence h'=lambda and h=lambda z+b. The converse follows by direct substitution and the shared fibers of ±1, with 0 and infinity omitted. This proves the complete claimed subclass without presuming general Möbius dependence.

The separate observation about arbitrary entire precomposition is likewise correct for a base pair with nonzero constant psi. It cannot establish exhaustion of all pairs, and the report does not use it for that purpose.

## 4. Rational-exponential endpoint and degree analysis: Proposition 5

**Accepted.** A possible concern was the compactly stated endpoint expansion. It can be made explicit as follows. For

E = R'S'(R−S)^2 / [P(R)P(S)],

the relevant orders at a puncture are:

- Distinct finite roots of P: −2.
- One finite root and one ordinary finite value of local degree q: q−2, at least −1.
- Distinct ordinary finite values with local degrees p,q: p+q−2, at least zero.
- One pole and one finite root: −2.
- One pole and one ordinary finite value of local degree q: q−2, at least −1.
- Equal finite shared root or equal poles: at least 2 min(p,q)−2, hence nonnegative, and cancellation only increases the order.
- Equal ordinary finite value: positive order.

Thus the required double pole of E at t=0 occurs only when the two endpoint images are distinct members of B. At infinity, passing to s=1/t transforms the identity into lambda^2 s^2 times the same derivative expression in s, so the identical argument applies. This explicitly includes endpoints at infinity and equal leading terms.

On C*, the exponential parameter has nonzero derivative. Hence all rational-map ramification there lies over B. Counting the union of four fibers and adding ramification at both punctures gives

(4d−e0−e∞−n)+(e0+e∞−2)=2d−2,

so n=2d. Since the shared union on C* is the same for R and S, their degrees are equal. No unproved degree bound is introduced.

## 5. Degree-two completeness: Proposition 6

**Accepted, conditional only on the explicitly credited established 2CM+2IM theorem.** This was the main adversarial focus.

If a value is omitted on C*, the full degree-two fiber of R must be supported at one puncture and that of S at the opposite puncture. Both local degrees there are two: neither map can also take that value at the other puncture, because the other map already takes it there and the two endpoint images must differ. Each map therefore has at most one remaining critical point. Of the four shared points on C*, at least two are simple for both maps. Any value with such a point is shared CM: a second C* preimage, if present for either map, must be common and must consume the remaining degree one for both maps. Thus there is an attained CM value in addition to the omitted CM value. The corrected Gundersen 2CM+2IM theorem gives Möbius dependence and excludes this branch of the non-Möbius subclass. The accepted theorem, its corrected status, and its conclusion are stated in [Steinmetz 2011, §§2–3](https://arxiv.org/html/1102.3383v1).

If no value is omitted, four shared points over four values means exactly one point for each value. A (1,1) point would require one residual preimage at a puncture for each map, and the punctures must be opposite. Only two endpoint images would then remain for the other three values; at least one of those values would have its full degree-two fiber at its sole shared point for both maps, giving forbidden multiplicities (2,2). Consequently every shared point is (1,2) or (2,1). If k points are double for R, its puncture degrees total 4−k, while those for S total k. Each total is at least two; therefore k=2 and every puncture is unramified for both maps.

The audit also enumerated all finite fiber-data possibilities after these proved degree and local-order constraints. With the four C* labels sorted and punctures ordered, there are exactly 84 admissible signatures: 12 with two omitted and two attained CM values; 48 with one omitted and one attained CM value; and 24 with no omitted and no CM values. All nonomitted signatures have exactly the reported complementary multiplicities and unramified punctures. This enumeration is a finite combinatorial cross-check, not an existence classification of rational maps.

The normalization and elimination are sound. Sending the two infinity-endpoint values to 0 and infinity and scaling the sole common pole to t=1 forces

R=alpha(t−r)/(t−1)^2,  S=beta(t−r)^2/(t−1).

Here r is finite, nonzero, and different from one. The remaining critical points are 2r−1 and 2−r, and neither is a puncture. Their simple counterpart fibers must use t=0 as the second preimage, giving the two displayed equations. Their only common root is r=−1. Equality at t=−3 gives beta=alpha/8, and t=3 gives the same condition. Degree-degenerate and puncture-critical values are excluded by the preceding fiber structure rather than silently discarded during polynomial cancellation.

The stated equivalence does not accidentally omit parameter inversion or exchange of f,g. Exact audit checks give, with J(w)=(w−1)/(8w+1),

J(R0(1/t))=−R0(−3t),  J(S0(1/t))=−S0(−3t),

and applying w↦−1/(8w) to R0(−t),S0(−t) exchanges the pair. Thus those operations are already absorbed by the allowed common target map and nonzero scalar parameter change.

The Gundersen fiber factorizations, psi=8, and normalization by z/sqrt(8) all check. The four shared sets on C* are exactly the stated singleton fibers; zeros introduced at t=0 do not add plane preimages. No conclusion for degree greater than two follows, and none is asserted.

## 6. Elliptic reduction and Reinders example: Proposition 7

**Accepted.** For two nonconstant elliptic functions on one common torus, four-value sharing makes the Mues expression holomorphic at every potential pole by the same local order calculations, whether or not it was normalized beforehand. A holomorphic function on the compact torus is constant. The constant is nonzero because the meromorphic factors f', g', and f−g are all nonzero as functions. Domain scaling can therefore normalize it to one.

There is no ramification away from the shared fibers after normalization. Riemann–Hurwitz on the torus gives ramification 2d and hence 2d points in the shared fiber union. Applying this to both maps proves equal degrees. Adding their fiber multiplicities yields sum(1+m_j)=8d, and therefore sum m_j=6d. The uniform and mixed-pattern observations follow exactly. In particular, the balance allows mixed patterns and does not exclude Steinmetz's established (1,1)/(1,4) examples.

For Reinders's example, the cubic has three distinct roots, so its smooth compactification is elliptic; du/v is a holomorphic nonvanishing differential and gives the required uniformizing coordinate. The two rational functions on this curve define globally meromorphic elliptic functions. They are distinct. Their zero and pole divisors give degree four for each map: orders (3,1) at u=0, (1,3) at u=−4, (−1,−3) at u=−1, and (−3,−1) at the elliptic point at infinity. At the finite branch points, u−u0 is a unit times a square of a local parameter and v is a unit times that parameter; at infinity u and v have pole orders two and three. The verifier's simpler substitutions test valuations only and should not be mistaken for exact curve parameterizations.

The squared-fiber factorizations and G/F=1 at u=±2 establish actual agreement of the signs of ±1, not merely squared equality. At both u values, v is nonzero, so u is an unramified local coordinate. The opposite simple/triple orders follow from the factorization and account for all those fibers.

The audit independently computed derivatives by writing F=A(u)v and G=B(u)v, so F'=A'Q+A Q'/2 and G'=B'Q+B Q'/2 for Q=12u(u+1)(u+4). This avoids the author's quotient-field reduction implementation. It reproduces U=12sqrt(3)/(u+1), V=4sqrt(3)(u+1), psi=144, and the z/12 normalization. The finite local identities U_normalized^2=p/q also hold at all four relevant u coordinates. The construction is known and properly credited.

The 2025 paper's main hypothesis is explicitly four finite shared pairs plus a fifth CM pair at infinity, excluding Möbius-related pairs. Its genus-zero theorem cannot be transferred to the four-value target. The audit checked hypothesis (H) and Theorem 1 in the published PDF, rather than reading only the abstract. [Published paper](https://afm.journal.fi/article/download/157535/102512).

## 7. Differential system and rescaling: Proposition 8

**Accepted.** The two first-order equations are equivalent to the definitions on the ordinary locus; they do not authorize arbitrary global choices of U. If infinity is CM, Proposition 2 forces all common poles to be simple and U,V have no zero or pole there; the earlier local statements then show that both are entire and zero-free. The report correctly restricts this conclusion.

The local ODE example is a valid analytic existence argument near (z,g)=(2,3), and the derivative is 144. A local solution neither proves global meromorphic continuation nor four-value sharing. Its role as a boundary on the attempted method is appropriate.

For shrinking rescalings, psi_n=rho_n^2. If the nonconstant limits were distinct, one could choose a small disk avoiding the poles, finite shared values, derivative zeros, and coincidences of the two limit functions. These excluded sets are discrete. Spherical locally uniform convergence to finite holomorphic limits there is ordinary locally uniform holomorphic convergence for sufficiently large n; derivatives converge as well. Passing to the differential identity gives zero for a quotient whose numerator and denominator are nonzero. This contradiction proves F=G. The proposition is conditional on both nonconstant limits existing and does not claim that such rescalings exist for every target pair.

This is a legitimate obstruction to preserving distinctness in the proposed shrinking-rescaling route, not a nonexistence proof for the original pair. The report keeps that distinction.

## 8. Recent-source caution and release limitations

The Li–Zhai–Yi v8 theorem statement was independently inspected in the dated PDF and on rendered printed page 4. It requires one finite-order function and a shared CM value. Neither is a supplied general hypothesis of the target. No result in the frozen packet uses this theorem: the degree-two argument uses the older corrected 2CM+2IM theorem instead. The attribution as a claim, the fixed v8 date, and the disclaimer about its full proof are accurate. [Versioned source](https://arxiv.org/abs/2402.03248v8).

The author's log mentions a concern communicated from the neighboring rank607 investigation. This audit does **not** certify that neighboring proof objection or audit the 39-page proof. It independently checks the statement, the missing hypotheses, and the complete lack of dependence of this packet on the recent theorem. The shared warning must not be relabeled as a fresh independent refutation on the strength of this audit.

The five approach families are materially distinct and their failure gaps are stated. All claims of global exhaustion, finite order, bounded spherical derivative, algebraic dependence, or bounded primitive degree are correctly withheld. The subjective progress estimates in the log are explicitly bookkeeping judgments and are not evidentiary confidence levels.

The bounded literature statement is permissible: no full classification was found in the described search. This audit has not proved the absence of a result anywhere in the literature. It also has not repeated the entire repository-history/queue duplication gate; the mathematical audit is not a substitute for a current release gate.

## 9. Corrections and reproducibility

**Required corrections: none.** Optional exposition improvements are recorded separately and do not block release as an unsolved partial packet:

1. Proposition 5 could display the endpoint order table, especially the pole/ordinary-value and equal-image cases.
2. Proposition 6 could insert the two-line count k=2 proving that all punctures are unramified.
3. If the auxiliary local-order checks are discussed in greater detail, distinguish valuation-preserving substitutions from exact elliptic-curve uniformizers.

The audit intentionally made none of these edits to the frozen report.

Reproduce from this audit directory with `python3 replay/check.py`, then `python3 independent_checks.py`. The latter verifies the frozen manifest, payloads, source file hashes, isolated replay equality, endpoint models, exhaustive degree-two fiber data, coefficient reconstruction, Möbius normalization, and an independently implemented elliptic calculation. It writes only `independent-results.json`. The scripts require Python and SymPy; they require no network. The source integrity checks require the private source files to remain locally available and do not redistribute them.

A final hash check after writing the audit confirmed that all seven public payloads and the author manifest were unchanged. The audit's own authored outputs have a separate SHA256SUMS. This PASS authorizes no remote action by itself; any publication remains subject to the parent's applicable release scope and current repository checks.
