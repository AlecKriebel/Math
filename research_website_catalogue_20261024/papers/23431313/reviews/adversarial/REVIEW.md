# Independent adversarial review — Zenodo 23431313

**Verdict: PASS for the full stated smooth compact-support classification.** No substantive mathematical defect was identified in either constructive sufficiency or necessity. This is an independent internal AI review, not human peer review, formal verification, a priority certificate, or approval of every stronger theorem discussed in the references.

Reviewed manuscript: *A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators*, Alec Kriebel, version1.0, 15 October2026. Review completed25 October2026 UTC.

## Source binding and independence

All five published pages were read, including the complete proofs, limitations, comparisons and references. The sole outer embedded PDF and the PDF inside the historical nested ZIP are byte-identical to the public reader; no additional edition remains unread. The page2 formula and Jordan convention were also visually inspected.

- Main PDF SHA256: `a1e2da77dd739bcc7ddc4dd8ba916c99010450e4224ae7a52d01d34c98960e72`.
- Public ZIP SHA256: `21de02dcdc08c6cd804ccf6345ede97edbfe734469dcdd83ff3b7a65c3c20f02`.
- Main TeX SHA256: `00cdda5b1c519407d834868b00a4f8fb20acbe22d21864f94af624c8ce9092cd`.

`source_binding.json` records independently rechecked public sizes/MD5/SHA256, all129 outer file bytes against their archive members, recursive ZIP CRC and reader-PDF hashes, and seven retained primary PDF hashes/URLs. Six relevant primary bodies were inspected at the interfaces described below; the separate GeometryIII online-first copy was retained/rehashed, while the actual issue PDF supplied the journal-body comparison.

Universal reconstruction and fresh controls preceded supplied-program reading. No sibling conclusions or dedicated historical assessment bodies were read. The manuscript contains audit and priority disclosures, and the required replay-interface inspection exposed historical terminal-status literals in `verify_kit.py`. Those incidental statements are not adopted as mathematical evidence. The mathematical replay hashes historical payloads opaquely. This is independent derivation with disclosed exposure, not a claim of perfect blindness.

## Exact claim and model boundaries

For every dimension \(n\ge1\) and every prescribed numerical real Jordan matrix J whose eigenvalues are all real, there is a globally \(C^\infty\), compactly supported real tangent-bundle endomorphism L on \(\mathbb R^n\) with vanishing Nijenhuis torsion, whose matrix equals J in a smooth commuting local frame on a nonempty open domain. Conversely, every eigenvalue at every point of any such compactly supported smooth real Nijenhuis operator is real.

The claim permits arbitrary block sizes, repeated eigenvalues, zero eigenvalues and the zero matrix. It does not prescribe the ambient Cartesian-frame matrix, retain a single Jordan type globally, require global algebraic regularity, or assert nonzero real-analytic compact support. Type, eigenvalues and rank may change outside the realization domain. These are explicit theorem limits rather than repairs imposed by this review.

The original problem was checked directly: author-v2 of arXiv:1804.03737 asks in Problem5.11 (printed p.29) for compact support and a prescribed unchanged Segre type on a domain, and then asks for necessary and sufficient conditions. Author-v1 labels the counterpart Problem4.10 (printed p.37). Both already credit real semisimple and two-dimensional Jordan examples and the nonreal obstruction. The paper correctly separates that historical target from any claim that it remained open worldwide in2026.

## Collar identity: order and unconstrained terms (page2)

On \(\mathbb T^m\times(-1,1)\), with \(m=n-1\), the invariant angular fields \(e_i\) and \(v=\partial_t\) form a global commuting frame. The angular coordinate *functions* are only local, but the fields and dual one-forms are global, which is enough to define the tensor. Write
\[
Le_i=A(t)e_i,\qquad Lv=b(t)+\lambda(t)v.
\]
All coefficients depend only on t. Direct bracket evaluation yields
\[
[Le_i,Lv]=-\lambda A'e_i,\quad [Le_i,v]=-A'e_i,\quad [e_i,Lv]=[e_i,v]=0,
\]
and hence
\[
N_L(e_i,v)=(A-\lambda I)A'e_i.
\]
All angular-pair components vanish. Tensoriality and skew symmetry cover every component. There are no missing b', lambda' or rank conditions: those terms cannot arise in these brackets. The matrix order is genuinely \((A-\lambda I)A'\), not its reversal.

Fresh symbolic first-jet contraction from the coordinate definition verified85 complete tensor components in dimensions2–5, keeping every entry of A, A', b, b', lambda and lambda' algebraically independent. Separate exact controls reject reverse arrow order and the reversed product, including a valid stage with \(AA'=0\) but \(A'A\ne0\). These corroborate, rather than replace, the general bracket derivation.

## Arbitrary real Jordan data and the finite path (pages2–3)

Using the upper-superdiagonal convention, move one complete Jordan block last and designate its terminal vector as transverse. Its preceding vectors, together with all other blocks, span an invariant hyperplane. Thus the initial full matrix is \(\begin{psmallmatrix}A_0&b_0\\0&\lambda_0\end{psmallmatrix}\), including the terminal arrow in b0. No arrow is silently discarded from the initial matrix. A size-one chosen block simply contributes no shortened angular block.

First turn b0 off while A and lambda stay fixed. This is permitted by the exact collar equation. For each angular block \(\mu I+K\), move lambda to the real number mu while A is fixed. Keep all other blocks fixed. If
\[
K=\sum_{j=1}^{r-1}a_jE_{j,j+1},\qquad KK'=\sum_{j=1}^{r-2}a_ja'_{j+1}E_{j,j+2},
\]
turn off a1 first, then a2, and so on. At a stage changing \(a_{j+1}\), its predecessor \(a_j\) is already identically zero; the first arrow has no predecessor. Thus \(KK'=0\). Other matrix blocks contribute no derivative. Repeated eigenvalues, crossings with inactive blocks and zero mu cause no denominator or spectral-choice problem.

After the arrows vanish, change the scalar block value c from mu to zero while setting lambda=c on that stage. The derivative is supported only on that block, where \(A-\lambda I=0\). Repeat until all angular blocks, b and lambda are zero. Singleton blocks have no arrow stages; zero-eigenvalue scalar stages may be constant. Since \(n\ge2\), the angular space is nonempty. The n=1 case is treated separately, correctly.

Concatenate the finitely many stages using switches with actual open endpoint plateaus. For the stated \(H(u)=e^{-1/u}\) on u>0 and zero otherwise, every right derivative at0 is a polynomial in1/u times the exponential and tends to zero. Therefore the stated switch is globally smooth. An affine reparametrization such as an argument crossing from below0 to above1 yields the required genuine endpoint plateaus. Equal stage values then glue with all derivatives zero. Reparametrization multiplies A' by a scalar and preserves the ordered constraint.

The even composition \(q(t)=S(2(t^2-1/16))\) is zero for \(|t|\le1/4\) and one for \(|t|\ge3/4\). The exact threshold arguments are0 and1, respectively; no absolute-value corner is introduced. The chain rule preserves the constraint even on the negative-t side. The tensor is exactly J on the central band and exactly zero on both end bands. A constant frame permutation restores the initially specified block order and preserves commutation.

An arbitrary scalar cutoff of J would not suffice; the paper does not use one. Independent controls explicitly reject both a nilpotent cutoff with \(J^2\ne0\) and scalar drift without lambda tracking. The published checks additionally reject a common cutoff of distinct eigenvalues.

## Same-dimensional embedding and global smoothness (page3)

The induction proving \(\mathbb T^d\) embeds two-sided in \(\mathbb R^{d+1}\) is valid. Starting with the circle, suppose f embeds \(\mathbb T^{d-1}\) as a two-sided hypersurface in \(\mathbb R^d\), with global unit normal nu. In the extra ambient dimension, its normal bundle has the explicit orthonormal frame \((\nu,0),(0,1)\). Compactness permits a uniform embedded tubular disk radius. The boundary of that disk bundle is \(\mathbb T^{d-1}\times S^1\), with the displayed parametrization.

The tubular embedding guarantees injection and immersion. The claimed new normal \((\cos\phi\,\nu,\sin\phi)\) has length1, is orthogonal to the circle derivative, and is orthogonal to derivatives in p because \(\nu\cdot df=\nu\cdot d\nu=0\). Thus the next induction step is again two-sided. This is an all-dimensional geometric argument, not an inference from low-dimensional drawings or numerical embeddings. The standard smooth tubular-neighborhood theorem is the imported background fact.

For \(n\ge2\), the resulting normal collar is an open n-dimensional subset of \(\mathbb R^n\), diffeomorphic to \(\mathbb T^{n-1}\times(-1,1)\). Pushforward preserves Lie brackets and Nijenhuis torsion. Its support is contained in the image of the compact set \(\mathbb T^{n-1}\times[-3/4,3/4]\), which lies strictly inside that open collar. Consequently every collar-boundary point has an ambient neighborhood disjoint from this compact support. Zero extension is genuinely smooth there and torsion vanishes by locality. No angular frame or coordinates have to extend beyond the collar.

The central band is open and nonempty; a connected coordinate box inside it gives the requested realization domain. On that box the pushed frame remains commuting. For n=1 any scalar plateau bump times the identity is Nijenhuis because vector-valued alternating two-forms vanish identically; the zero tensor covers J=0 in all dimensions. These cover the dimensional and zero boundary cases.

## Necessity and the exact imported theorems (pages3–4)

I inspected arXiv:1903.04603v2 Theorem3.1, the surrounding admissible-factor discussion and proof, and Proposition3.2/Theorem3.3 with their proofs. The splitting theorem explicitly permits algebraically singular points. Equal roots and conjugate roots must remain grouped, but an isolated nonreal root with its conjugate can be separated from the remaining spectrum. It yields block dependence on separate local coordinates. The no-real-eigenvalue block has a smooth canonical complex structure and becomes a holomorphic complex tensor, with its complex eigenvalues in the upper half-plane. No real-analyticity or generic regularity assumption is being smuggled into the smooth argument. Standard analytic-functional-calculus/integrability background used by those published results is accepted, not re-proved here.

The paper's weaker zero-point rigidity lemma is sufficient and its maximum-principle proof is valid:

1. On a closed connected manifold, the maximum positive imaginary part mu(x), with zero assigned to an all-real spectrum, is continuous by continuity of polynomial roots. If any nonreal eigenvalue exists, compactness gives a positive global maximum mu0.
2. Among roots on that maximal line, choose maximal algebraic multiplicity m0. The locus E containing such a root is nonempty and closed. Along a convergent sequence, roots admit a convergent subsequence locally; vanishing characteristic-polynomial derivatives gives multiplicity at least m0, and maximality gives equality. No continuous labeling of all roots is needed.
3. Near p in E, isolate the chosen root and conjugate with the splitting theorem. The real block has complex rank m0. Its monic complex characteristic factor P is holomorphic in block coordinates and independent of complementary coordinates, with \(P(z)=(z-\lambda_0)^{m_0}\) at p.
4. All nearby roots have imaginary part at most mu0. Therefore minus the imaginary part of the linear coefficient a1 is bounded above by m0*mu0 and attains that value at p. The holomorphic maximum principle makes a1 locally constant. Equality of the sum forces every root in that factor to have imaginary part mu0.
5. The shifted polynomial \(P(w+i\mu_0)\) then has only real roots, so all its coefficients are real-valued holomorphic functions and hence constant. It equals the original power locally. This avoids assuming individual repeated roots are holomorphic. Splitting gives independence of complementary coordinates, so E is open in the whole manifold, including the case of an empty complementary block.
6. Connectedness makes E the whole manifold, contradicting a point where L=0.

Compact support on \(\mathbb R^n\) allows identification with a standard chart of \(S^n\), followed by zero extension on a neighborhood of infinity. The support image is compact away from the omitted point, so this extension is smooth and remains Nijenhuis. The closed connected zero-point lemma therefore applies in every stated dimension.

The source's stronger Theorem6.1 and its proof on pp.41–43 were inspected. The literal later assertion that applying \((L-\lambda_0I)(L-\overline{\lambda_0}I)\) removes only one nonreal pair is imprecise: the listed spectra \(\{\pm i,\pm i/2\}\) become \(\{0,3/4\}\) under \(z^2+1\). That observation does not refute spectral rigidity. The current paper explicitly avoids depending on that reduction sentence and supplies the sufficient maximum argument above. I therefore do not adopt or certify every step of the stronger global persistence proof, and do not identify the unread *Advances in Mathematics* publisher body with these author-version bytes.

## Prior-result comparisons

Theorem4.5 and its p.28 remark in BKM author-v2 give arbitrary algebraic types at points using independent characteristic-coefficient coordinates; generic nearby points have distinct eigenvalues. That does not by itself give a fixed repeated-block type on an open domain with a compact zero transition.

The actual GeometryIII issue PDF has Theorem1.10 (printed p.161), while author-v1 labels its counterpart Theorem1.4. I checked both statements and the issue proof around pp.172–173. The regular-layer condition allows one block per eigenvalue, starts at a nonzero nilpotent Jordan block for n>1, and states local membership in the layer closure. It does not itself supply the unrestricted repeated-block compact-support construction. The different publication numberings are correctly distinguished.

GeometryIV author-v1 Theorem1.4 and the nilpotent compatibility equations in its proof were read. The framework permits singular/zero output symmetries, but coefficients obey differential compatibility; it is not legitimate simply to multiply every term by a bump. In size3, the displayed Toeplitz functional-calculus formula contains a term of the form \(f'_2(u^3)u^2\) when the output is nilpotent. Treating u2 as an angle prevents naive periodization unless that coefficient vanishes. This supports the paper's narrow comparison; it does not rule out a different use of that framework. No comprehensive implication or worldwide-priority exclusion follows from this bounded source review.

## Fresh checks and unmodified replay

`fresh_controls.py` imports no supplied helper. It passed50,001 explicit guards, including85 symbolic generic first-jet components,45,816 exact polynomial stage checks and4,092 exact-zero endpoint checks. The4,092 schedule paths cover all ordered size compositions through dimension8, four zero/repeated/signed spectrum assignments and every distinguished block. It also checks invalid order/cutoff/scalar variants, plateau thresholds, evenness, the dimension-one boundary and the polynomial-pair-count example. Arbitrary real eigenvalues and unbounded dimension are established by the written argument, not extrapolated from these finite paths.

I corrected only reviewer bookkeeping that initially included the path-total counter in the reported number of guarded assertions. The final50,001 figure counts actual guards; the mathematical checks were unchanged and re-executed. No manuscript or published helper was repaired.

After reading `scripts/run_checks.py` and `safety.py`, the unmodified portable mathematical entry was run in an isolated copy under normal, `-O` and `-OO` Python3.12.14. All three outputs were identical and passed:576 schedule families,4,778 stages,515 direct bracket stages,1,575 first-jet scalar components, and five rejected deliberate faults per run. Payload verification runs first and checks the complete128-file manifest plus its own manifest. Original and isolated source inventories remained byte-identical.

The published controls explicitly say they are newly distributed controls, not replays of historical omitted programs. I preserve that distinction. `verify_kit.py` contains historical administrative-status validation; its code was inspected for interface understanding, but its terminal-adoption verdict machinery was not used as mathematical evidence or represented as a new review. No PDF build, source rewrite or external action was performed.

## Final scope and remaining gap

The strongest verified result is the full stated if-and-only-if classification: all numerical real Jordan matrices occur in a commuting smooth local frame on an open domain of a compactly supported global smooth Nijenhuis tensor in the same dimension, and any such compactly supported tensor has entirely real spectrum everywhere. No mathematical gap remains identified within that scope.

Standard splitting/holomorphic and tubular-neighborhood inputs remain accepted background with checked interfaces. The theorem does not prescribe a Cartesian-frame matrix or global Jordan type, and does not establish analytic compact support, full-result priority, mechanism priority or worldwide preexisting openness. No follow-up question is added merely because the paper mentions limitations.
