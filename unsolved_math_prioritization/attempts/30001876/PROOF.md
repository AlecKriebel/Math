# GL3 Maass restriction: reconstruction and original normalization audit

Date: 11 October 2026. Problem: 30001876 / OWR-11135-003.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made.

Editorial chronology: this is the complete authored mathematical reconstruction and initial normalization audit. Its earlier hold and requests for independent normalization work are retained as historical mathematical judgments. The later independent challenge in AUDIT.md supplies a Bessel–Mellin–Barnes calculation and narrows that hold; ACCEPTANCE.md records the combined verdict. In the literal Li–Young power convention, 8J=P_plus/D. With the explicitly interchanged Bump exponents, 8J=P_minus/D. Both are conditional on the corrected imported Bessel identity. Neither convention is silently selected. The original displays are still not accepted as simultaneously literal, and no claim that the final restriction theorem is false follows.

## Disposition

**Prior-result scope confirmed; fixed-scale spectral reconstruction accepted with stated standard analytic imports; exact printed gamma-normalization chain held for correction.** This is an audit and reconstruction of existing machinery, not a new restriction theorem, a worldwide novelty search, or acceptance of the whole Li–Young paper. The original introductory question is not evidence of a separate unresolved conjecture. The corrected intended setting is a level-one spherical Hecke–Maass **cusp form**, restricted by an upper **block-diagonal** embedding with a positive scale. It is not an arbitrary upper-triangular subgroup or an arbitrary GL3 automorphic representation.

The spectral expansion, zero constant component, odd-parity vanishing, inverse Mellin reconstruction, and the factors 1/pi and 1/(4 pi^2) in the restriction-norm identity follow independently of the disputed closed gamma normalization. Reading the actual printed proofs reveals that the chain (3.13), (3.18), (3.19), (3.20) is not internally consistent as written. There is also a factor-two issue in literal unfolding with the stated U2. These are not reasons to label the entire theorem false; they are reasons not to issue an unconditional exact-normalization acceptance on the strength of those lines alone.

## 1. Target authentication and source identity

The original supplied evidence inventory had 101 listed members. All listed members were regular files with safe distinct relative paths and matching byte counts and SHA-256 hashes, against the independently supplied manifest digest 4c341f931751ecb0559cab6ee16a926c6a1d9b212c713ac375a37bdc185363d5. That check authenticated the specified membership; it did not claim that a shared screening directory contained no unrelated files. Public verification metadata distinguishes this earlier evidence authentication from the creator’s later closed 60-member package and the independent challenge’s closed 36-member package. No dataset contents are distributed. The geometric interpretation below is taken from the original scholarly report and final article.

OWR source: Xiaoqing Li, joint work with Matt Young, “L2 restriction norm of a GL(3) Maass form,” in The Analytic Theory of Automorphic Forms, Oberwolfach Report 43/2011, DOI 10.4171/OWR/2011/43. The contribution begins on printed 2405 (PDF 9), and the relevant introductory paragraph is printed 2406 (PDF 10). It calls the embedding “upper diagonal” and asks about the inner product with a given SL2(Z) Maass form, followed by “or more generally, we ask for the spectral decomposition.” The very next paragraph describes their restriction-norm result and reduction to averages of GL3 x GL2 L-functions. This is an introductory motivation inside a report of existing joint work, not a separately numbered open problem. The OWR right-invariance notation is O2(Z); the final article says O2(R). The final geometric definition makes the latter unambiguous.

Main source: Xiaoqing Li and Matthew P. Young, The L2 restriction norm of a GL3 Maass form, Compositio Mathematica 148 (2012), 675–717, DOI 10.1112/S0010437X11007366, published online 20 March 2012. The retained publisher PDF is 890,977 bytes, SHA-256 4d9e561254394b453a0bea6bc7de585f6138c82c54949db836fdf6b8669fed7b, 44 PDF pages including cover. Fresh retrieval from the same publisher URL matched these exact bytes. Printed page p corresponds to PDF page p−673. We use final numbering, not the preprint's one-section-shifted numbering.

Public URLs:

- https://ems.press/content/serial-article-files/46359
- https://doi.org/10.1112/S0010437X11007366
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/957D21B10686FBDDD2E7537C8D9B19D2/S0010437X11007366a.pdf/the-l2-restriction-norm-of-a-gl3-maass-form.pdf

## 2. Geometry and measures

Put X = SL2(Z)\H and write z=x+iv, v>0. Use the determinant-one representative

g_z = [[sqrt(v), x/sqrt(v)], [0,1/sqrt(v)] = n(x) diag(v,1) v^(−1/2).

For r>0 define iota_r(z)=diag(r g_z,1) as a point of H3=GL3(R)/(O3(R) R^x), and f_r(z)=F(iota_r(z)). The equivalent determinant-one GL3 representative is r^(−2/3)iota_r(z). Left multiplication by diag(gamma,1), gamma in SL2(Z), proves automorphy on X. The original upper block has real dimension three after its right orthogonal quotient: two z-coordinates and the scale r. H3 has dimension five, so this is the claimed codimension-two submanifold. Fixing r alone gives a two-dimensional slice, not the whole codimension-two object.

The conventions used here are

dmu(z)=dx dv/v^2,  <f,h>=integral_X f(z) conjugate(h(z)) dmu(z),

and scale measure dr/r. The modular surface has its ordinary hyperbolic measure (volume pi/3), not probability measure. The spectral constant eigenfunction is u0=sqrt(3/pi). The cusp basis {u_j}_{j>=1} is orthonormal for this measure. Rescaling this measure changes Fourier coefficients and the spectral density and must not be done silently.

The paper's E(z,w) is (1/2) sum over U2(Z)\SL2(Z) Im(gamma z)^w, with U2 the upper unipotent matrices of diagonal entries 1. Equivalently it is the sum over Gamma_infinity\SL2(Z), where Gamma_infinity=±U2. The continuous spectral measure is d tau/(4 pi), with E_tau=E(z,1/2+i tau). It is not an L2-normalized cusp vector, but pairing against rapidly decreasing f_r is ordinary absolutely convergent integration.

The GL2 Fourier conventions are

u_j(z)=sum_{n!=0} rho_j(n) 2 sqrt(|n|v) K_{it_j}(2 pi |n|v) exp(2 pi i n x),

rho_j(±n)=rho_j(±1) lambda_j(n)n^(−1/2), n>=1, lambda_j(1)=1.

At level one the Hecke eigenvalues lambda_j(n) are real. A phase of u_j still changes rho_j(1); the conjugate of rho_j(1), not rho_j(1), occurs for the chosen inner product. For the Eisenstein series,

rho(1,w)=pi^w/[Gamma(w) zeta(2w)],

lambda(n,1/2+i tau)=sum_{ad=n}(a/d)^(i tau), which is real for real tau. Values at removable singularities are interpreted by continuation.

F has exactly the Jacquet–Whittaker and A_F(m,n) normalization in (2.1)–(2.8). In particular A_F(1,1) is not silently set to 1. The paper's Dirichlet series (3.23) and (3.30) use A_F rather than normalized Hecke eigenvalues, and therefore scale with F. Multiplying F by c multiplies the period and these series by c and N(F) by |c|^2.

## 3. The fixed-scale quantities and the Mellin periods

Define

c_j(r)=<f_r,u_j>,  c_tau(r)=<f_r,E_tau>,  c_0(r)=<f_r,u0>.

Use a separate symbol for their transforms:

Lambda_j(s)=integral_0^infinity c_j(r) r^(2s−1) dr/r,

Lambda_tau(s)=integral_0^infinity c_tau(r) r^(2s−1) dr/r.

These are the integral-defined quantities denoted by calligraphic L in (3.21) and (3.28). The ordinary L in (3.23)/(3.30) is a Dirichlet series. Neither that series nor its product with an Archimedean factor is a fixed-r coefficient: r has been integrated out. At r=1 the fixed coefficient still involves an inverse integral over the Mellin frequency, not one special value.

For an even u_j, Proposition 3.4 prints Lambda_j(s)=conjugate(rho_j(1)) L_j(s) G_{t_j}(s), where

L_j(s)=sum_{m,n>=1} A_F(m,n) lambda_j(n)/(m^2 n)^s.

Proposition 3.5 prints the analogous formula with conjugate(rho(1,1/2+i tau)) and lambda(n,1/2+i tau). Its proof is explicitly omitted in the article; this audit reconstructs the unfolding rather than claiming to have read an omitted proof. The statements require the normalization qualification in section 5 below.

## 4. Reconstruction of the local unfolding

To avoid the repeated y1 notation, keep r for the scale and put a=r/sqrt(v), b=v after unfolding in z. Then

iota_r(z)=n_12(x) diag(ab,a,1), r=a sqrt(b), dr/r=da/a,

r^(2s−1)=(a^2 b)^(s−1/2).

The Whittaker character produces exp(2 pi i n x). The x integral selects the same Fourier index in conjugate(u_j), producing the factor 2 sqrt(|n|b) K_{it_j}(2 pi |n|b) conjugate(rho_j(n)). Next put a=A/m, b=B/|n|. The factor m^(−1) in (2.8), the scale exponent, and the measure give m^(−2s). For n, the initial n^(−1/2), the (a^2b) exponent, the sqrt(b), the measure db/b^2, and the n^(−1/2) in rho_j(n) give n^(−s). No extra power of r or b is left over.

Set

J_tau(s)=integral_{a,b>0} K_{i tau}(2 pi b) W_J(diag(ab,a,1),nu,psi_1,1)
              (a^2 b)^(s−1/2) b^(1/2) (db/b^2)(da/a).

Equivalently its measure-weight is (a^2 b)^s da db/(a^2 b^2). Definition (3.18) is G_int,tau(s)=4 J_tau(s). We deliberately label this integral-defined G separately from the expression printed in (3.19).

There is a stabilizer point that must be retained. Under the **literal** U2 in (2.8), −I is not in U2 but acts trivially on H. On the restriction, replacing gamma by −gamma multiplies the matrix on the right by diag(−1,−1,1), an orthogonal matrix. Thus the seed is unchanged and the two U2-cosets above each Gamma_infinity-coset contribute equally. Unfolding the ordinary modular fundamental domain therefore gives 2 times the strip integral. In the literal convention the even period obtained from (2.8) is

Lambda_j(s)=8 conjugate(rho_j(1)) L_j(s) J_{t_j}(s)
           =2 conjugate(rho_j(1)) L_j(s) G_int,t_j(s).

The factors in 8 are: 2 for this stabilizer, 2 for the K-Bessel Fourier normalization, and 2 for the ±n pairing. The same formula holds for Lambda_tau with the Eisenstein coefficient and series. Its constant Fourier terms disappear in the x integral because n is nonzero. The calculation begins in a common right half-plane of absolute convergence; analytic continuation then uses the integral-defined period and the standard Rankin–Selberg continuation imported in Corollary 3.6.

**Status of the 8J expression:** this is an auditor-authored reconstruction conditional on reading the supplied Fourier expansion, U2, quotient measure, and A_F conventions literally. It is not certified agreement with the authors' intended normalized L-factor convention, an official erratum, or a publication-ready correction. The factor-two observation and the W* chain below are local consistency findings pending an independent reconciliation of all underlying source conventions.

If instead a Fourier formula is written using Gamma_infinity-cosets, its seed coefficients must be doubled on this restriction; that alternative yields the same period. Replacing U2 by Gamma_infinity without adjusting coefficients is not a reconciliation. Similarly, a half-volume convention would require changing the stated GL2 spectral density and normalization. The paper's (3.24) does not display the stabilizer factor. This audit does not certify an unmentioned measure convention that makes all its displayed lines simultaneously literal.

### Parity and the constant component

The level-one spherical symmetry A_F(m,−n)=A_F(m,n), stated in the proof, pairs the signs. An odd u_j has rho_j(−1)=−rho_j(1), so its transformed period vanishes. More directly, diag(−1,1,−1) belongs to SL3(Z), and its left/right action sends the restriction at x to that at −x. Hence f_r(−x+iv)=f_r(x+iv), and c_j(r)=0 for every r when u_j is odd. This avoids inferring pointwise vanishing solely from a transformed statement.

Pairing against u0 and unfolding leaves integral_0^1 exp(2 pi i n x) dx=0 for every n!=0. Therefore c0(r)=0 for each r. The rapid decrease and convergent Fourier expansion needed for this unfolding are standard cusp-form imports. The result is absence of the **global constant eigenfunction component**. It does not assert that f_r is a GL2 cusp form, or that the x-constant term at the GL2 cusp vanishes; the continuous spectrum generally remains.

## 5. Exact gamma-factor acceptance hold

Write A=i alpha, B=i beta, C=i gamma, with A+B+C=0 and the paper's definitions (2.5)–(2.7). Equation (3.13) gives W_J^*=D(nu) W_J, where

D(nu)=pi^(1/2−3nu1−3nu2) Gamma(3nu1/2) Gamma(3nu2/2) Gamma((3nu1+3nu2−1)/2)
     =pi^(−3/2+i alpha−i gamma) Gamma((1+i gamma−i beta)/2)
       Gamma((1+i beta−i alpha)/2) Gamma((1+i gamma−i alpha)/2).

Let P_tau(s)=pi^(−3s) product over q in {alpha,beta,gamma} and signs ± of Gamma((s±i tau−i q)/2).

The three printed assertions then read:

- (3.18): G=4 I(W_J), where I has the weight just specified
- (3.19): G=P/D
- (3.20): I(W_J^*)=P/(4D)

But linearity and (3.13) give I(W_J^*)=D I(W_J). The first and third assertions consequently give G=P/D^2, not P/D. D is not identically 1. This is an algebraic incompatibility, unaffected by Mellin inversion, parity, or any later spectral measure. It was checked from rendered printed pages 683–684, not merely OCR. The exact same incompatibility is present in the retained arXiv v1 at (4.13), (4.18)–(4.20); that older version cannot serve as an independent repair.

The scale omission in (3.25) is different: r=a sqrt(b) repairs the subsequent proof with the correct Jacobian and exponents, so it is a variable-reuse/exposition issue. No such change accounts for the extra D in (3.20).

A further primary-source warning was found: Blomer–Buttcane–Raulf, A Sato–Tate law for GL(3), Comment. Math. Helv. 89 (2014), 895–919, printed p. 905 footnote 4, explicitly says the leading constant in Goldfeld (6.1.3) should be 8 rather than 4. Li–Young's proof of Proposition 3.3 and its earlier comparison (3.12) both refer to this exact Goldfeld formula. This is relevant evidence requiring a fresh normalization derivation, not automatic permission to transplant a constant: parameter shifts, variable reversal, and the GL2 stabilizer must all be matched. The displayed BBR Bessel formula itself repeats y2 in both Bessel arguments, reinforcing the need not to treat every surrounding display as error-free. Only its stated correction and normalization warning are used here.

Stade 1990, DOI 10.1215/S0012-7094-90-06013-2, was identified from Crossref. Its publisher download returned a 1,160-byte HTML bot-block page rather than a PDF; the DOI web tool also failed. Goldfeld 2006's located university-hosted copy returned HTTP 502. Neither source's underlying proof was inspected in this audit. We do **not** certify the exact replacement for (3.20), the constant in (3.12), or the numerical gamma factor independently of those imports. The integral-normalized expression 8J obtained above remains usable under the literal Fourier/measure conventions. A proposed repair which removes the denominator from (3.20) repairs one algebraic implication but does not by itself reconcile the separate stabilizer and normalization issue.

Thus the audit acceptance boundary is explicit: calligraphic periods defined by (3.21)/(3.28), and their spectral/Plancherel use, are accepted; the printed identification of all of (3.18)–(3.20) and (3.24) with a single exact constant is **not** accepted. This is not a claim that the final L-value formula or the restriction bound is false. It is a concrete obstacle to blanket exact-constant acceptance, with a reproducible local chain and the specific primary import still to check.

## 6. Fixed-scale inversion, with the frequency factor made explicit

For c=c_j or c_tau let M_c(w)=integral c(r)r^w dr/r. Then M_c(w)=Lambda((w+1)/2). Ordinary Mellin inversion gives

c(r)=(1/(pi i)) integral_{Re(s)=sigma} Lambda(s) r^(1−2s) ds.

On the central line this is

c(r)=(1/pi) integral_R Lambda(1/2+it) r^(−2it) dt.

The factor is 1/pi, not 1/(2pi), because the Fourier frequency for x=log r is 2t. An even cusp coefficient can therefore be reconstructed, in the literal integral-normalized convention of section 4, as

c_j(r)=(8 conjugate(rho_j(1))/pi) integral_R
            L_j(1/2+it) J_{t_j}(1/2+it) r^(−2it) dt.

Replace j by tau and rho_j by rho(1,1/2+i tau) for the continuous coefficient. If a separately validated corrected gamma factor H_tau=8J_tau is supplied, it can replace 8J in these formulas. Simply inserting the symbol G without settling which of (3.18) and (3.19) it denotes loses an exact factor.

### Analytic meaning and convergence

There are two sound levels of assertion.

1. Hilbert-space level: N(F)<infinity implies c_j lies in L2(dr/r) and c_tau does so for almost every tau. Mellin Plancherel then gives inversion in L2. It does not by itself justify evaluating an unregularized inverse integral at every r.
2. For this smooth cuspidal restriction, standard rapid-decrease estimates for a cusp form and its derivatives, together with reduction theory and polynomial growth of a fixed GL2 Eisenstein series, give continuous coefficient functions with rapid decay as r tends to 0 or infinity. With the analogous differentiated estimates, the functions of log r are Schwartz. Fourier inversion is then pointwise and the inverse integral absolutely convergent for each fixed j or tau.

For clarity about the latter import, a determinant-one restriction representative has rows including (0,r^(1/3)/sqrt(v),0) and (0,0,r^(−2/3)). Its shortest nonzero row-lattice vector is therefore at most min(r^(1/3)/sqrt(v),r^(−2/3)). Quantitative reduction and cuspidal rapid decrease turn this into arbitrary inverse-power decay. For r>=1 the geometric mean is r^(−1/6)v^(−1/4); for r<=1 the first bound is r^(1/3)v^(−1/2). Arbitrarily high powers give an integrable majorant for all polynomial v-growth of a fixed E_tau and for log-r derivatives. This explains why both scale ends, including the mixed region of large v, are covered. We import the standard reduction/rapid-decrease theorem for derivatives; we do not pretend the sentence “F has rapid decay” by itself proves the uniform estimate. Goldfeld–Thillainatesan 2006, Theorem 2.5 and its proof on pp. 611–613, also explicitly treats the two scale ends through the contragredient, but is not used as a substitute for checking uniformity under the z integral.

If one wants to use only the Hilbert-space input and continuity, a safe pointwise expression is the Fejer-regularized inverse:

c(r)=lim_{T→infinity} (1/pi) integral_{−T}^T (1−|t|/T) Lambda(1/2+it)r^(−2it)dt.

This is the positive Fourier approximate identity in log r. At the L2 level it converges in norm; at continuous points it gives the pointwise value. This states explicitly the convergence mode and avoids equating an L2 identity with an unqualified pointwise integral.

## 7. Spectral expansion and norm identity

For each r>0, ordinary GL2 spectral theory gives in L2(X)

f_r(z)=sum_{j>=1, even} c_j(r)u_j(z)
         +(1/(4pi)) integral_R c_tau(r)E(z,1/2+i tau) d tau.

The constant component has been removed by its proved vanishing, and odd cusp components vanish. This is exactly the content of (4.2) after those simplifications. Smooth rapidly decreasing f_r has bounded derivatives of all orders. The pointwise, locally uniform form follows from the smooth spectral expansion statement in Theorem 2.2 and the usual Sobolev/spectral estimates. Those foundational estimates, the Fourier–Whittaker expansion, and rapid decay are standard imports, not reproved representation theory. For complete caution, the L2 formulation alone is already the spectral decomposition; no global uniform convergence on the noncompact cusp is claimed. We do not interchange the entire j, t, tau family of inverse integrals without an additional majorant.

Parseval at fixed r is

||f_r||_2^2=sum_{j>=1}|c_j(r)|^2+(1/(4pi)) integral_R |c_tau(r)|^2 d tau.

Writing x=log r and Fourier frequency omega=2t proves

integral_0^infinity |c(r)|^2 dr/r=(1/pi) integral_R |Lambda(1/2+it)|^2 dt.

Integrate fixed-r Parseval with dr/r and apply Tonelli to its nonnegative terms. This gives

N(F)=(1/pi) sum_{j>=1} integral_R |Lambda_j(1/2+it)|^2 dt
      +(1/(4pi^2)) integral_R integral_R |Lambda_tau(1/2+it)|^2 dt d tau.

This verifies the factor and measure logic of (4.1) and all steps (4.2)–(4.8) in terms of the **integral-defined** periods. No closed gamma evaluation is needed. Tonelli, rather than a formal unproved exchange of conditionally convergent complex integrals, is the reason the integrated spectral identity is sound. The recorded Gaussian control independently checks the 2t frequency and inverse factor; it is a normalization diagnostic, not a proof of the automorphic theorem.

## 8. Coverage and exclusions

Covered: the specific level-one spherical Hecke cuspidal setting of the final article; the upper block-diagonal GL2 restriction with positive scale; its fixed-scale inner products reconstructed from transformed periods; zero constant component; odd/even selection; cusp-plus-Eisenstein decomposition; scale-integrated Parseval. The elementary reconstruction answers what the OWR introductory sentence is asking within its intended setting. It does not establish that a corpus sentence without hypotheses is a theorem for all objects called GL3 Maass forms.

Not covered: arbitrary levels or characters, other K-types, general cuspidal representations without matching local vectors, GL3 Eisenstein/residual forms, regularized periods, arbitrary embeddings, or a canonical decomposition into all GL3 branching representations. Noncuspidal F can invalidate the decay and ordinary integrability used here, can create nonzero constant contributions, and can need regularization. The theorem's strong eigenvalue-aspect bound is separate: Theorem 1.1 assumes tempered F with L2 norm one and retains |A_F(1,1)|^2; the self-dual corollary has its additional imported Fourier-coefficient bound. Sections 5–10, which prove the sharp bound, have not been proof-audited here. Neither sharpness nor an asymptotic is inferred from the spectral identity.

Outstanding exact-formula work is bounded and identifiable: independently match the Jacquet definition (2.1), completed W* (3.13), corrected Goldfeld Bessel formula, Stade 1990's original integral, its parameter/order conventions, and the ineffective SL2 stabilizer, then state a single repaired gamma-period formula. No author mathematical code was downloaded or run. No claim of an official erratum was found or made. These original outstanding questions are preserved as history; AUDIT.md supplies the subsequent two-convention calculation. A byte-integrity check by itself never establishes mathematical correctness or a right to distribute source material.

## 9. Actual inspection and integrity limits

Actual text inspection: OWR printed 2405–2406; Li–Young introduction and definitions on 676–680, normalization passage 683, full Proposition 3.3 proof on 684, full Proposition 3.4 proof on 685–686, Proposition 3.5 and Corollary 3.6 on 686, full Theorem 4.1 proof on 686–687; arXiv v1 corresponding normalization passages; Goldfeld–Thillainatesan definition and selected rank-lowering proof passages, especially 611–613; BBR printed 905 and its footnote. Actual rendered-page inspection: Li–Young PDF 10–14 (printed 683–687), OWR PDF 10 (2406), BBR PDF 11 (905). OWR PDF 9 was rendered but not visually inspected. Retrieved whole PDF does not mean read whole PDF; source-author cited proofs not obtained are not counted as inspected.

The original sealed evidence inventory covers the authored report, inputs, source bytes, extraction files, source-retrieval evidence, rendered pages, and authored validation scripts/results. Its verifier rejects missing, extra, altered, unsafe-path, duplicate-member and symlink cases. Actual negative controls were conducted on disposable copies, never on original sources. SHA-256 validation proves retained byte identity and closed membership, not correctness of a mathematical proof, a source’s historical authority, or the truth of a paper. Authentication of the earlier 101-member evidence inventory likewise does not convert inherited scholarly claims into checked proofs. This prose edition distributes only authored mathematical reports and public source/verification metadata; copied source bodies, images, extracts, datasets, executable code, raw outputs and private coordination material are excluded.
