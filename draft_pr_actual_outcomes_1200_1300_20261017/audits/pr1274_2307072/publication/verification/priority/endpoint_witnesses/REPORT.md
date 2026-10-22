# Independent initial audit: endpoint witnesses and mathematical ancestry

## Finding and recommendation

The single witness and its primitive are classical in exactly the submitted normalization. Tadeusz Iwaniec's 1986 journal paper prints

\[
\rho(z)=(z/|z|)^2\mathbf1_D(z),\qquad
T\rho=(1+\log|z|^2)\mathbf1_D,
\qquad w=(z\log|z|^2)\mathbf1_D.
\]

These are equations (6)--(7) and the sentence immediately following them on printed p.388. The kernel on p.387 is precisely \(-1/\pi\operatorname{pv}(z-t)^{-2}\), and equation (1) is \(T\bar\partial w=\partial w\). The exact witness, exact transform, and exact primitive therefore cannot be presented as new. The primary journal scan, rather than a search excerpt or a later attribution, was freshly downloaded and visually inspected. [Iwaniec, 1986](https://doi.org/10.1307/mmj/1029003418).

James T. Gill's 2010 Theorem 1 also publishes the entire positive-angular-mode formula needed for the proposed polynomial family. Consequently, the polynomial calculation is an elementary explicit consequence of published operator formulas. This audit did not locate the particular sequence \(v_m\) or the exact norm \(H_m\) printed in an earlier inspected body. That is a narrowly stated remaining bibliographic gap, not evidence of firstness or of a new solution mechanism. [Gill, 2010](https://doi.org/10.1307/mmj/1281531461).

Recommended framing: an explicit polynomial illustration or expository verification of classical Beurling formulas, with direct credit to Iwaniec and Gill. Do not promote the packet as a newly discovered logarithmic counterexample or a novel resolution of the qualitative endpoint issue. Whether an earlier source explicitly states both clauses in the precise wording of Problem 7.72 remains separate from whether those clauses already follow from classical mathematics.

The submitted packet already explicitly disclaims novelty and historical priority. This finding strengthens its incomplete historical account; it is not an allegation that the submitted text asserted firstness.

## Exact target and audit scope

The input is the PASS claim pinned by `../../MATH_GATE.json`, read together with all six files in the original submitted packet. The mathematical proof and submitted source-verification record were read before the independent searches; the remaining packaging files were read after the substantive findings. Here

\[
N=\{v\in L^\infty(D):\int_D v\phi\,dA=0\text{ for every holomorphic }\phi\in L^1(D)\},
\]

with a bilinear pairing, zero extension outside the unit disc, and the negative Beurling kernel. The checked assertions are failure of mapping all of \(N\) into \(L^\infty(D)\), failure of a common norm bound, and failure of such a bound even for \(N\cap\mathbb C[z,\bar z]\). Each fixed polynomial still has a bounded transform. Pointwise divergence at the origin alone is insufficient for the first assertion; positive-area level sets or an essential-supremum argument are required.

This family pursued explicit witnesses, angular-mode/Hardy formulas, endpoint differential inequalities, and Bergman-annihilator representations. It did not read another priority family's report or the root's new priority query material before this seal. The source-only/PDE reviews were not needed. No external individual was contacted. No Git mutation, push, release, or publication occurred.

## Dated positive evidence

| Date | Primary evidence actually inspected | What it establishes | Exact limit |
|---|---|---|---|
| March 1964 | de Leeuw--Mirkil, pp.113--114, Proposition 2 and corollary | Homogeneous differential operators of the same order admit a uniform sup-norm domination only when the target symbol belongs to the linear span of the controlling symbols. | This directly rules out \(\|\partial u\|_\infty\le C\|\bar\partial u\|_\infty\) on smooth compactly supported complex functions. The passage to the printed problem is assembled below, not claimed as a quotation from this paper. |
| 1986 | Iwaniec, pp.387--390 and 393; all eight pages read in OCR, critical pages visually checked | Exact logarithmic witness, transform, zero-boundary primitive, and derivative identity under the submitted sign convention. | No explicit formulation of the full analytic-area-\(L^1\) annihilator or proposed polynomial sequence was found in this inspected article. |
| August 2009 | Bañuelos--Janakiraman, final journal pp.459--463; author manuscript pp.1--5; relevant references | Repeats the exact logarithmic pair, explicitly attributing it to Iwaniec's 1986 article, in Remark 2.1 on final p.461. | The paper's displayed positive kernel conflicts with the positive logarithmic output copied into that remark. The 1986 original resolves the target convention. Author and final PDFs are different bodies. |
| August 2010 | Gill, journal pp.353--356, especially Theorem 1 and its complete proof | Full transform formula on \((z/\bar z)f(|z|^2)\); explicitly reprints the logarithmic pair in (4), pp.355--356, crediting Iwaniec. | Neither the particular \(v_m\) nor an explicit assertion for all analytic \(L^1\) annihilator tests was found in the inspected passage. |
| January 2011 manuscript; online December 2011; 2012 issue | Breit--Diening, Saarland preprint 290, printed pp.4--7, especially p.6; primary publisher metadata | Explicit endpoint Korn example \(v(x)=Qx\log|x|\), with bounded symmetric gradient and unbounded full gradient; also smooth compactly supported approximating examples. | The author preprint is the inspected mathematical body. The subscription-only final body was not inspected or presumed byte-identical. |
| March 2014 | Bañuelos--Osękowski, final journal pp.213--215, particularly p.214 | Repeats the Hardy-adjoint positive-angular-mode identity and credits Gill for the adjoint result. | Its weak-type main theorem is a different conclusion. It supplies ancestry of the formula, not direct publication of the proposed \(H_m\) statement. |
| 1980 article; received August 1979 | Burbea, pp.207--209 and 220--221, Proposition 4 and proof | Finite-\(p\) Bergman-annihilator/zero-boundary Sobolev identification; backward references to Havin 1968 and Schiffer 1963. | The paper expressly restricts its operator theory to \(1<p<\infty\). Its theorem must not be silently extended to the \(p=\infty,q=1\) target. |

Sources: [de Leeuw--Mirkil](https://doi.org/10.1215/ijm/1256067459), [Iwaniec](https://doi.org/10.1307/mmj/1029003418), [Bañuelos--Janakiraman](https://doi.org/10.1307/mmj/1250169072), [Gill](https://doi.org/10.1307/mmj/1281531461), [Breit--Diening preprint](https://www.math.uni-sb.de/preprints/preprint290.pdf) and [publisher metadata](https://doi.org/10.1007/s00021-011-0082-x), [Bañuelos--Osękowski](https://doi.org/10.1307/mmj/1395234366), [Burbea journal-body archive](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7338-11512_2006_Article_BF02384691.pdf).

## What the older angular-mode theorem gives here

This subsection is the auditor's mathematical comparison, not a claim that the following problem-specific derivation was printed by those authors.

Gill defines

\[
\Lambda^*a(t)=\int_t^\infty\frac{a(s)}s\,ds-a(t)
\]

and proves, for real \(a\in L^p(\mathbb R_+)\), \(1\le p<\infty\),

\[
B\big[(z/\bar z)a(|z|^2)\big](z)=-\Lambda^*a(|z|^2).
\tag{A}
\]

The sign in (A) matches the negative kernel. Its proof occupies the bottom of printed p.355 and the upper part of p.356, using the dilated logarithmic pair and density of finite radial step functions. This is a published full formula, not merely generic \(L^\infty\to\mathrm{BMO}\) unboundedness.

For \(a=\mathbf1_{(0,1)}\), (A) gives the exact submitted logarithm. For

\[
a_m(t)=\big[1-(1-t)^m\big]\mathbf1_{(0,1)}(t),
\]

the input in (A), restricted to \(D\), equals

\[
e^{2i\theta}a_m(r^2)
=z^2\sum_{j=0}^{m-1}(1-|z|^2)^j=v_m(z).
\]

This follows from \(1-(1-t)^m=t\sum_{j=0}^{m-1}(1-t)^j\). Thus Gill's theorem yields, for \(t=|z|^2\in(0,1)\),

\[
Bv_m=1-(1-t)^m-\sum_{k=1}^{m}\frac{(1-t)^k}{k}=G_m(t).
\tag{B}
\]

The remaining exact-norm calculation is elementary: \(0\le a_m\le1\), with supremum one; \(G_m(0)=-H_m\), \(G_m(1)=1\), and

\[
G'_m(t)=\sum_{j=0}^{m-1}(1-t)^j+m(1-t)^{m-1}>0.
\]

Continuity at zero makes the lower endpoint control the essential supremum on a positive-area disc. Hence \(\|v_m\|_\infty=1\) and \(\|Bv_m\|_\infty=H_m\). The exact norm does not follow just by evaluating a single point; this continuity step is needed. The submitted polynomial primitive is the termwise antiderivative of (B), while the limiting primitive already appears explicitly in Iwaniec.

The full annihilator test class also presents no new obstruction for these inputs. If \(a\) is bounded on \((0,1)\), \(f_a(re^{i\theta})=e^{2i\theta}a(r^2)\), and \(\phi\) is holomorphic and area-integrable, then \(f_a\phi\) is absolutely integrable. For each \(r<1\), the uniformly convergent Taylor series of \(\phi\) on that circle has nonnegative angular modes. Its product with \(e^{2i\theta}\) has zero angular integral. Fubini gives \(\int_D f_a\phi\,dA=0\). This proves membership in the literal bilinear \(N\), for both the older single witness and every \(v_m\).

Accordingly, the first negative answer is a direct problem-specific consequence of Iwaniec's exact old example; the exact polynomial formula is a direct specialization of Gill's old theorem plus the displayed finite-sum calculation. It would be misleading to describe these as requiring a newly discovered endpoint mechanism. The additional work can still provide a clear, useful exposition with correct conventions and boundary details.

## Distinct endpoint route: a precise classical equivalent

The de Leeuw--Mirkil corollary concerns actual homogeneous differential operators, not an arbitrary unconstrained singular integral. Apply it with \(A=\bar\partial\) and \(B=\partial\) in two real variables. Their degree-one complex symbols are not scalar multiples. Therefore the uniform inequality

\[
\|\partial u\|_\infty\le C\|\bar\partial u\|_\infty,
\qquad u\in C_c^\infty(\mathbb C;\mathbb C),
\tag{C}
\]

is impossible. Dilation and translation place any counterexample's support strictly inside \(D\) without changing the derivative ratio. The following transfer is assembled here from this classical theorem:

1. For \(u\in C_c^\infty(D)\), \(v=\bar\partial u\) belongs to \(N\): integration by parts is legitimate for every analytic \(L^1\) test because the support is interior. The full-plane identity gives \(Bv=\partial u\). A common bound on \(N\) would imply (C).
2. Mapping every member of \(N\) into \(L^\infty(D)\) would itself imply a common bound by the closed graph theorem. Indeed, \(N\) is closed in \(L^\infty(D)\), zero extension is continuous into \(L^2(\mathbb C)\), and \(B\) is \(L^2\)-continuous. These facts make the graph of the alleged map \(N\to L^\infty(D)\) closed. Thus the 1964 endpoint theorem already implies qualitative failure of the all-members assertion after this transfer.
3. The polynomial restriction also cannot rescue a common bound. For fixed \(u\in C_c^\infty(D)\), put \(h=u/(1-|z|^2)\), extended smoothly across a neighborhood of \(\overline D\) by zero near its boundary. Approximate \(h\) in \(C^1(\overline D)\) by polynomials \(q_n(x,y)\), and let \(u_n=(1-|z|^2)q_n\). Their zero extensions are continuous, piecewise smooth, and have no boundary measure in their first derivatives. Then \(v_n=\bar\partial u_n\) is a polynomial on \(D\), \(Bv_n=\partial u_n\) there, and \(v_n\in N\). For the last statement, integrate against \(\phi_r(z)=\phi(rz)\), then use \(\phi_r\to\phi\) in area \(L^1\). Passing a presumed polynomial inequality to the \(C^1\) limit would imply (C), a contradiction.

This supplies a classical equivalent-operator route to both qualitative target failures. It is not claimed that de Leeuw--Mirkil published the named disc-annihilator problem or this polynomial approximation argument. The exact \(H_m\) family does not come from their qualitative theorem alone.

The independent Korn lineage corroborates how familiar the logarithmic primitive is. For planar rotation \(Q(x,y)=(-y,x)\), Breit--Diening's \(Qx\log|x|\) corresponds to \(i z\log|z|\), a scalar multiple of the submitted \(z\log|z|^2\). Its \(\bar\partial\) derivative is bounded and its \(\partial\) derivative is logarithmic. Their explicit zero-boundary example therefore uses the same local mechanism. One need not appeal to Ornstein's harder \(L^1\) theorem to establish the present \(L^\infty\) failure.

## Citation tracing and routes that do not settle priority

The positive formula chain was followed in both directions: the 2009 paper's Remark 2.1 led back to the 1986 original; Gill 2010 explicitly identifies the same pair and proves its general angular-mode extension; the 2014 paper repeats the extension. Strzelecki's 2017 journal paper cites all three radial/adjoint papers and identifies their finite-\(p\) norm setting. The report does not equate such finite-\(p\) results with the target endpoint conclusion.

The endpoint chain was independently followed backward from Breit--Diening's explicit logarithmic example and reference [LM] to the 1964 de Leeuw--Mirkil primary theorem. Its Proposition 1, Proposition 2, proof, and corollary were read together and pp.113--114 inspected visually. This avoids assuming that generic unboundedness on all of \(L^\infty\) automatically persists on \(N\).

The Bergman route led to Burbea's complete Proposition 4 and proof, pp.220--221. Its Hermitian annihilator convention requires conjugation when translated to the present bilinear pairing. Its finite-\(p\) hypothesis is substantive; extrapolating that representation to the endpoint would transfer the very regularity difficulty under investigation. Therefore this route is contextual ancestry, not a standalone proof of the target at \(p=\infty\). Havin 1968 and Schiffer 1963 were identified through Burbea's primary bibliography but their bodies were not inspected here; no result is attributed directly to those bodies on that basis.

The 2008 Bañuelos--Janakiraman author PDF cited in the submitted verification record is a different article from their 2009 weak-type paper. The former concerns finite-\(p\) norm bounds. Its introduction and theorem statements were freshly read; it is not used as direct evidence for the exact witnesses. The 1982 Iwaniec paper was also acquired from EMS Press; its operator identity and finite-\(p\) radial examples provide context, while the exact logarithm is directly verified in the 1986 paper. Volberg's arXiv:1203.2291v1 is about finite-\(p\) radial/stretch/twist inequalities; its 2012 public submission and its internal assertion of February 2009 composition are different dates. It does not, in the inspected body, establish the claimed direct Volberg attribution for this precise problem. That question belongs to the independent direct problem-edition audit.

No conclusion here depends on a present-day claim that the finite-\(p\) Iwaniec conjecture is open or solved. It is a different question, and historical articles' descriptions of its status are not promoted to current-status statements.

## Exact remaining gaps and falsification checks

| Route | Status | Exact gap or limitation |
|---|---|---|
| Exact single witness, output, primitive | Verified prior publication, 1986 | No priority claim for this witness is defensible. Earlier than 1986 was not exhaustively ruled out. |
| General formula encompassing the polynomial family | Verified prior publication, 2010 | Particular family and exact \(H_m\) claim are audit deductions unless an earlier printed occurrence is supplied. |
| Earlier source explicitly states both full target clauses | Not established in this family | The inspected articles need not use the named problem's precise \(N\), all analytic \(L^1\) tests, and polynomial wording together. This is a publication-history gap, not a mathematical gap. |
| Qualitative constrained endpoint via differential operators | Verified theorem plus transparent transfer | Problem-specific transfer and polynomial approximation are assembled here; do not retroactively attribute them as printed claims. |
| Endpoint Bergman-annihilator isomorphism | Blocked as a shortcut | Available source is finite \(p\). Replacing its missing endpoint theorem by assumption would be circular. |
| Generic full-plane \(L^\infty\to\mathrm{BMO}\) unboundedness | Rejected as sufficient alone | Does not identify \(N\) or the polynomial class. Exact old witnesses and the derivative route do. |
| Exact polynomial norm as a novelty claim | Unresolved, with weak novelty prospects from this evidence | Lack of a located prior printed \(H_m\) is not clearance; the entire operator computation is an elementary substitution into an established theorem. |

Checks against hidden mismatches: Iwaniec uses the same negative kernel and planar Lebesgue measure; \((z/|z|)^2=z/\bar z\) away from zero; its old primitive vanishes on the unit circle; positive-area level sets give essential unboundedness; Gill's radial coefficient is supported in \((0,1)\), hence has zero transform outside the disc under (A); the angular cancellation uses the literal bilinear pairing; \(m\) is a positive integer; \(H_1=1\) poses no exceptional case; fixed polynomial transforms remain bounded. No unverified change of convention or endpoint extrapolation is needed.

## Acquisition, access, and seal limits

Raw responses, HTML (including failed responses), PDFs, text extractions, OCR, and page PNGs are confined to this family's ignored `_local/` directory. The public query ledger contains only literal queries, URLs, and authored status descriptions. The source ledger records body byte counts, SHA-256 hashes, timestamps, relevant complete passages, visual checks, and version/access limitations. The manifest has an explicit list of authored files and excludes itself; source inputs and `_local` evidence are not manifest members.

Warsaw's author-PDF endpoint returned HTTP 403. Several automated Project Euclid requests returned challenge HTML. The ordinary browser landing pages displayed Open Access and a public DOWNLOAD PDF link; documented browser downloads obtained the genuine journal PDFs without authentication, CAPTCHA, or access-control manipulation. These successful primary bodies supersede the earlier access limitation for the cited articles. The subscription-only Breit--Diening final article was not downloaded. One guessed DOI resolved to an unrelated article and was discarded; one guessed arXiv URL was unrelated and discarded; the crossref metadata endpoint eventually returned HTTP 429 and was not retried. Such attempts remain in the private retrieval trail and carry no evidentiary weight.

This is the sealed initial independent-family report. It is not publication clearance, a firstness certificate, an exhaustive proof of literature absence, or external human review. Any cross-family challenge must be recorded in a new folder without changing this seal.
