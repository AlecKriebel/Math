# Independent original-scope, canonical-tight and priority audit: PR1345 /30000043

Target: `6455aec3553e2f16ab001c8f8996583ce73aba13`, all27 changed blobs bound in `PINNED_MEMBER_HASHES.json`. This audit treats earlier acceptances and execution receipts as claims. It does not claim human or formal verification. Assigned audit100%; parent sweep80%.

## Verdict

The explicit real Haar counterexample is correct for the full classical indexed single-generator question. No fatal operator, all-space, field, functional-calculus, constant, or indexing gap was found. It proves failure of the actual inverse square root, rather than substituting a canonical-dual result. The usual indexed interpretation is supported by the recovered original question and established local-commutant terminology. Lack of an arbitrary-permutation theorem is not a defect in this stated result.

**New material priority finding:** a public full-target negative preprint is now available: Alper Ferudun, *The Canonical Normalized Tight Frame of a Wavelet Frame Need Not Have Wavelet Structure: An Explicit Riesz Wavelet for a Question of Han and Frank*,17October2026, [DOI10.5281/zenodo.23438995](https://doi.org/10.5281/zenodo.23438995). Its actual indexed proof was checked, not merely its abstract. DataCite independently confirms the exact title/author, findable active DOI and registration on17October2026. Thus the pinned sentence saying no prior tight resolution had been verified needs a dated update for the current audit. This is an unrefereed public preprint, not a peer-reviewed resolution or proof of first discovery. The PR proof is internally dated14October2026, earlier than that public record; this audit does not decide precedence between private manuscripts or establish global priority.

The prior2011 Bownik–Jasper–Speegle paper already asserts a proper subclass and gives the exact preservation criterion. Its inspected theorem does not itself supply the missing classical counterexample proof. The1990/2002 classical family and2007 dual results remain credited background, rather than being mislabeled as full canonical-tight answers.

No row, PR, provider, Git index/ref, publication, or shared audit was modified.

## 1. Original question and precise target

I freshly recovered Michael Frank's *Approximation of Frames by Normalized Tight Ones*, OWR10/2004, printedpp529–531, and visually inspected529 and531. His convention is S=(θ*θ)^−1, so the questioned S^(1/2) family is the ordinary F^(−1/2) canonical tightening, where F=θ*θ. Reading his S as the ordinary F reverses the operator. The question appears immediately before Theorem5, after a discussion of fixed unitary systems and frame vectors. The theorem states a positive semi-orthogonal single-generator case using the standard classical affine atoms.

The natural indexed question therefore includes the following special case. For Df(x)=√2f(2x), T_kf(x)=f(x−k), suppose x_(j,k)=D^jT_kφ, j,k∈Z, is a frame of all L²(R). Must its canonical atoms F^(−1/2)x_(j,k) equal D^jT_kη for one η, at every original pair(j,k)? Index(0,0) forces η=F^(−1/2)φ. A failure at one other index refutes the universal assertion.

The original short sentence does not spell out every reindexing convention. Bownik–Jasper–Speegle2011 Theorem4.1,equation4.3 and Remark4.1 explicitly use this indexed identity to define preservation of affine structure. Their abstract dilation D obeys DTD^−1=T²; taking it to be the inverse of the expanding physical dilation above aligns the conventions, with all integer scales still present. No arbitrary permutation is smuggled into this alignment.

The result below retains the same dilation, integer lattice, one generator and complete L²(R). It need not disprove changed-lattice, additional-generator or unordered variants to answer this indexed universal question. It also does not classify all frames for which tightening succeeds.

## 2. Independent full-space realization

Let h=1_[0,1/2)−1_[1/2,1), e_(j,k)=D^jT_kh, ε=1/100, φ=h+εDh. Each e_(j,k) has norm1, integral0 and support[k2^−j,(k+1)2^−j). Dyadic supports are disjoint or nested; a coarser Haar function is constant on the support of a strictly finer one, proving orthogonality.

For completeness, let f∈L²(R) be orthogonal to every Haar vector. The integrals over the two halves of any finite dyadic interval are equal, so its average equals that of each successive dyadic ancestor. Ancestor lengths tend to infinity, and the absolute average is bounded by ||f||₂/√length, hence tends to zero. All finite dyadic interval integrals vanish. Dyadic step functions approximate compactly supported continuous functions in L², and these are dense. Thus f=0. This is completeness on all L²(R), not merely a proper multiresolution subspace; the fact that some ancestors remain on one side of the origin does not affect the estimate.

Define V e_(j,k)=e_(j+1,2k). The index map is injective, so V extends to an isometry, with adjoint

    V*e_(j,k)=e_(j−1,k/2) if k is even, and0 if k is odd.

In particular V*h=e_(−1,0), while V*e_(0,1)=0. The physical identity T_kD=DT_(2k) gives at every positive or negative scale

    D^jT_kφ=e_(j,k)+εe_(j+1,2k)=Ae_(j,k), A=I+εV.

The Neumann series makes A boundedly invertible because ε<1. Consequently this is a Riesz basis of all L²(R). The frame sum is exactly ||A*f||², giving valid lower/upper bounds(1−ε)²=9801/10000 and(1+ε)²=10201/10000. Optimality is not required.

The ordinary frame operator is

    F=AA*=I+ε(V+V*)+ε²VV*.

It is not A*A: VV* has a missing unilateral-root direction, whereas V*V=I. The independent controls explicitly detect that difference. There is no finite-scale or translation truncation in this realization.

## 3. Actual inverse square root and certified remainder

Put X=F−I and q=2ε+ε²=201/10000. Then X is self-adjoint and ||X||≤q<1. The binomial series with c_n=(−1)^n binom(2n,n)/4^n converges in operator norm and, by continuous functional calculus on[−q,q], equals the positive inverse square root of I+X. Thus

    F^(−1/2)=I−X/2+R, ||R||≤q²/(1−q).

The original proof's looser steps q<3ε and q<1/2 give ||R||<18ε². After separating −ε²VV*/2 and multiplying on the correct side by A, they yield

    U=F^(−1/2)A=I+(ε/2)(V−V*)+E, ||E||<20ε².

All order-sensitive terms are present. Indeed direct multiplication gives

    E=−(ε²/2)VV*−(ε²/2)(V+V*)V−(ε³/2)VV*V+R(I+εV).

Using V*V=I and VV*V=V confirms the bound. This is the left polar factor of the invertible A; it is unitary since UU*=I and U is invertible.

An independent sharper estimate uses |c_n|≤3/8 for n≥2 (the central-binomial ratios decrease). It gives

    ||E||≤(3/2)ε²+ε³/2+(3/8)(1+ε)q²/(1−q)
          =24039499/78392000000 <(31/10)ε².

This estimate validates the stated constants without trusting the supplied acceptance audits. Neither the series nor its branch is a formal asymptotic substitution: it is an operator-norm convergent functional-calculus identity for this strictly positive F.

## 4. Translation defect and forced generator

Let T=T_1. Then Th=e_(0,1), VTh=e_(1,2)=TVh, V*Th=0 and V*h=e_(−1,0). Hence

    UTh−TUh=(ε/2)T e_(−1,0)+ETh−TEh.

The leading vector g=T e_(−1,0)=2^−1/2(1_[1,2)−1_[2,3)) has norm1. Therefore the original bound proves

    ||UTh−TUh||>ε/2−40ε²=1/1000.

The independent sharper bound proves the stronger strict inequality>219/50000. Since Ah=φ and ATh=Tφ, this is exactly

    ||F^(−1/2)Tφ−TF^(−1/2)φ||>1/1000.

A same-index generator would have to equal F^(−1/2)φ at(0,0), and would fail at(0,1). This proves the claimed full indexed negative.

The generator and all series coefficients are real. Polynomial limits preserve the real subspace, so the same proof works on real or complex L²(R). Complex perturbations are not needed. The example is not semi-orthogonal: <φ,Dφ>=ε≠0. V and V* commute with D, so the tightening has the expected dilation covariance; no global translation commutation of V is assumed. In particular T e_(−1,0) must not be mistaken for e_(−1,1), which is a physical translation by2.

## 5. Independent exact scalar diagnostic, without a compressed Hilbert space

Two reducing subspaces provide an additional check. H0=span{e_(j,0):j∈Z} carries V as a bilateral shift; H1=span{e_(n,2^n):n≥0} carries it as a unilateral shift. On H0, X=ε(z+z^−1)+ε² under e_(j,0)↔z^j. Every polynomial approximation U_N=Σ_(n=0)^N c_nX^n A maps Th into H1. The vector g=T e_(−1,0) is orthogonal to H1: its basis vectors are T e_(n,0), n≥0, and T is unitary. Also T^−1g=e_(−1,0). Thus

    <U_NTh−TU_Nh,g>=−coefficient_(−1,0)(U_Nh).

`independent_controls.py` evaluates these finite operator polynomials by exact rational sparse arithmetic, retaining every reachable basis vector. It does not replace V by a finite matrix with a false boundary. For N=12, the full-operator remainder satisfies

    ||U−U_N||≤|c_13|(1+ε)q^13/(1−q).

The scalar first term remains exactly zero even in the limit because H1 is closed and reducing. Hence only one copy of this tail is needed for the displayed scalar interval. `CONTROL_RESULTS.json` records exact rational endpoints around0.004999812496093579. This is a certified lower witness for the norm, not a claim that it equals the full defect norm.

The control also verifies99 basis cases, adjoint parity, dilation covariance, frame-versus-Gram operator order, ε=0, the original remainder and the sharper bound. Normal,-O,-OO agree. Three deliberate errors (wrong adjoint parity, all-positive binomial signs, and replacing VV* by I) are each rejected in all three modes. Finite diagnostic computation supplements the analytic proof; it does not establish Haar completeness or source intent.

## 6. Prior literature and the new public full-target match

The2011 paper [Bownik–Jasper–Speegle](https://doi.org/10.1090/S0002-9939-2011-10887-6) was read in full, with p3255 visually checked. Its introduction asserts properness of the admissible subclass. Section4 proves an equivalence between its orthonormal-dilation conclusion and the indexed local-commutant condition on an abstract BS(1,2) representation. It gives no classical counterexample or proof of that strictness. This is substantive prior negative-status evidence and exact terminology, but its conditional theorem alone is not a verified classical full-negative proof.

The2007 [Bownik–Lemvig paper](https://doi.org/10.1016/j.acha.2007.04.004), pp263–266, concerns canonical duals F^−1, confirms indexed same-generator terminology, and corrects a sign error in the later2002 argument. Its dual-only results do not alone prove F^−1/2 failure for the same generator. The optional complex universal dual-to-tight bridge in the PR has a valid separate mechanism: under universal tight preservation, generators x±itF^−1/2x have frame operators F+t²I; subtracting their tight identities and taking t→0 yields universal dual preservation. This is not a pointwise implication. The explicit real Haar proof does not depend on it.

The perturbation family and isometry mechanism are classical. The PR's credit to Lemarié via Daubechies1990, Daubechies–Bin Han2002 and Chui–Shi1993 should remain. This audit freshly corroborated the older dual history through2007 and the current public paper; fresh direct downloads of the1990 and2002 full sources timed out. Their exact equation/attribution details are therefore not newly certified from those original pages in this audit. No missing historical download affects the direct operator proof.

The important new full-target match is [Ferudun's public paper](https://eulersolve.org/papers/owr-720-011/), DOI10.5281/zenodo.23438995. I checked its Theorem1.1(a)–(c),§§2–4 and underlying chain/polar calculation. For every orthonormal dyadic wavelet and0<ε<1 it proves indexed canonical-tight failure for this same classical family. Its explicit lower bound includes ε=1/100 and the Haar wavelet. The registered DOI is thus a full indexed-negative answer, rather than a dependency DOI. Its additional unordered, altered-lattice and Shannon non-Bessel claims are not needed and are not certified here.

Independent DataCite metadata says created=registered=updated2026-10-17T16:01:32Z, issued2026-10-17, version1.0, state=findable,isActive=true, and matches the exact title/author. The live PDF is178311bytes, SHA256`4c94d59915ef1b90ab1d731e643a8cd6524c616d502fc96e4ed6cb2b12466558`. Direct Zenodo-record and DOI opens returned403; DataCite and the author-hosted PDF succeeded. This authenticates the available publication identity and mathematical coverage, not an independently archived historical checksum of the17October file. No claim of peer review is inferred.

The PR's14October internal manuscript date predates the17October public record. No public release of the PR manuscript was authenticated here. Consequently one may identify a currently available full literature answer, but may not infer discovery order, copying, dependence, firstness, or priority over private work. The bounded search does not rule out still earlier literature. The current reader should no longer leave its historical no-verified-full-resolution sentence without a dated qualification.

## 7. Proposed literal row, not written

The present mathematical negative remains valid. For a queue that records current publicly available full answers, the following literal row is justified, with the publication DOI separated from private-manuscript chronology:

| 1781 | 30000043 / OWR-720-011 | Wavelet Structure of Canonical Tight Frames | 0.0545 | 5.0 | 3 | 2004 | already_solved | 1/5 |  | Public full indexed negative verified: Alper Ferudun,17October2026, Theorem1.1(c)/Corollary1.4, DOI10.5281/zenodo.23438995 (unrefereed). Independently checked real Haar phi=h+0.01Dh proof in this draft remains valid; internal14Octoberdate does not establish public or discovery priority. Classical family credited; no novelty, arbitrary-reindexing or altered-lattice claim for this draft. [Reviewed reader](attempts/30000043/README.md). | [10.5281/zenodo.23438995](https://doi.org/10.5281/zenodo.23438995) |

The1/5 field is preserved from the pinned row, not a newly authenticated lifetime attempt count. A project policy preferring claimed_solved until integration may retain that workflow status while adding the same current literature finding; the mathematical coverage and chronology qualifications should not be dropped.

## 8. Access, independence and closed evidence

Fresh current read-only GWS inspection preceded mathematics:191rows, one false substring match to unrelated30001345 arrangement invariants, zero exact/semantic wavelet matches. This is a tracker duplicate check, not a worldwide priority certificate.

Source identities, selected PDF pages and actual read/visual scope are in `SOURCE_INDEX.md`, `SOURCE_DOWNLOADS.json` and `PUBLIC_NEGATIVE_RETRIEVAL.json`. The current proof, contract, scope adjudication, optional bridge and mathematical audits were completely read; other packaging members were bound, not all replayed. No author verifier was used to establish correctness. `PINNED_MEMBER_HASHES.json` distinguishes these read scopes for all27actual paths.

An actual disk-full write occurred during source recovery. Only this current unsealed audit's three already-viewed PNG renders were removed; compressed selected PDFs were retained. Earlier sealed PR1327/1330/1332 folders were untouched. New storage stays below6MiB. The read-only verifier checks closed membership, content hashes, all27blobs, external input identities, main branch, cap and exact control replay. No outside person or other agent was contacted; only parent reporting occurred.
