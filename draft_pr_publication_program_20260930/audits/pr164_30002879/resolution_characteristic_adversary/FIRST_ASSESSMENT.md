# Independent first assessment: resolution / characteristic-map family

This assessment was made before reading original `independent_review/*`, `verification.json`, original research/README logs, original author code, other families' work, or a root verdict. The assessment concerns the immutable submission identified by original HEAD `7c8acab3ff84c6c8caadec8998296936a156e0bd`; the declared literal original progress is `2/5`. Input identities are in `INPUT_PINS.json`; sealing UTC and assessment SHA-256 are in `FIRST_ASSESSMENT_SEAL.json`.

## Exact hypothesis and falsifiers

For every field K of characteristic two, set A=K[x,y]/(x²,y²), M=A/(y), and B the upper triangular algebra with corners A, M, K. The candidate claims that the original coefficient-quotient map gamma: HH*(B) -> HH*(A) is injective in every degree and identifies the cohomology ring and bracket with

    L = K·1 + (y,u) K[x,y,u,v]/(x²,y²),  |u|=|v|=1,

where u and v are precisely the derivations d/dx and d/dy. The ambient bracket has pairings [u,x]=[v,y]=1 and all other generator pairings zero. A counterexample to exactness, to the pure-y comparison, to the characteristic normalization, to injectivity, to degree-zero image, to identification with the coefficient map, or to restriction of insertions would defeat this route. Finite-degree dimensions alone are insufficient evidence.

## Direct universal deductions

**Periodic bimodule resolution.** Write D=K[t]/(t²). In D^e=K[l,r]/(l²,r²), multiplication by s=l+r sends 1 to l+r, l and r to lr, and lr to zero. Thus image and kernel both equal span{s,lr}. The augmentation sends l,r to t and lr to zero, so its kernel is the same span. Also s²=0. This proves exactness of the constant-differential periodic resolution in every degree, using characteristic two. Tensor the x and y resolutions over the field K. Their homology tensor formula leaves only A in degree zero, hence the displayed P is an A-bimodule resolution. All terms are free over A^e. No assumption that K is finite, perfect, or algebraically closed appears.

**Coordinate normalization.** The normalized bar map sends e_(i,j) to the sum of all x/y words with i x entries and j y entries, each with coefficient 1. A bar differential internal term xx or yy vanishes. Every term arising from an adjacent unlike pair has exactly one partner obtained by swapping that pair; both give the identical xy-entry word, so cancel. Left and right boundary words give exactly the four terms in d e_(i,j). The map lifts the augmentation. The ordered cup cochain (d/dx)^cup i cup (d/dy)^cup j is 1 on the single word x^i y^j and zero on the other shuffle words and on every other e_(k,l) of that degree. Consequently there is no factorial, binomial, or divided-power factor. Hom_(A^e)(P,A) has zero differential; these cup classes are a basis over A in each degree. This establishes the polynomial presentation in the candidate's coordinates, rather than merely an abstract graded-vector-space identification.

**Module Ext and characteristic map.** The A-projective resolution Q_n=A with d_n multiplication by y is exact because ker(y)=yA. Its augmentation is A -> M. Hom_A(Q,M) has zero differential. Multiplication by any representative a in A on every term is a lift of the coefficient class a mod y; identity degree shifts lift the extension generator eta. Their compositions give Ext_A*(M,M)=M[eta]. For P tensor_A M, freeness as a left A-module follows from A^e tensor_A M = A tensor_K M. Its exactness follows from right-A splitting of the augmented P resolution: A is projective over itself, and each successive kernel is projective after splitting, by induction. The chain map Q -> P tensor_A M given by 1 -> e_(0,n) tensor 1 commutes with the differential since y annihilates M. It lifts identity_M. A coefficient cochain on e_(i,j), tensor identity_M, therefore pulls back to zero for i>0 and to multiplication by a mod y on Q_j for i=0. Thus in every degree

    chi(a u^i v^j) = 0  (i>0),
    chi(a v^j) = (a mod y) eta^j.

In particular chi is onto in every degree and ker(chi)=(y,u)R. The argument works without checking finitely many degrees and without using an author's checker.

**Original coefficient sequence, directly.** Put f=1-e and E=Kf+Ke. E^e is a product of fields, so the normalized E-relative bar resolution is a projective B-bimodule resolution; the usual augmented bar contraction supplies exactness. Modulo E, the only nonzero corners are f(B/E)f=bar(A) and f(B/E)e=M. A composable tensor word is either entirely in bar(A), or ends with exactly one M, preceded by bar(A) entries. Consequently C_E^0(B,B)=A direct-sum K and, for n>=1,

    C_E^n(B,B)=C^n(A,A) direct-sum T^(n-1),
    T^r=Hom_K(bar(A)^tensor r tensor M,M).

T is the cochain complex of the normalized A-module bar resolution of M. Let I=BeB. Then C_E^0(B,I)=K and C_E^n(B,I)=T^(n-1) for n>=1. The initial differential K -> T^0 sends c to c identity_M; later differentials are the module bar differential. With coefficients B/I=A, E-linearity kills all mixed and e-corner outputs; thus C_E*(B,A)=C*(A,A) exactly. The coefficient map B->A is projection onto the all-A component, including in degree zero.

The connecting map sends an A-cochain F in degree n to (a_1,...,a_n,m) -> F(a_1,...,a_n)m, which is the tensor-bar representative of the characteristic map. In degree zero its target is End_A(M)/K, so it sends a to its action on M modulo scalar actions. Therefore H^0(C_E(B,I))=0, H^1=M/K, and H^(n+1)=Ext_A^n(M,M) for n>=1. Surjectivity of chi_n kills every incoming connecting image in HH^n(B), n>=1, and gives image ker chi_n. In degree zero the quotient action has kernel K+yA and projection is injective. This verifies the original gamma itself without transferring the central difficulty to an unspecified alternative exact sequence.

**Structural compatibility.** On all-A input words, E-bimodule linearity forces intermediate outputs of relative insertions into the A corner. Projection then agrees with the same insertion in the normalized A cochains. A degree-zero diagonal output contributes only its A component; its e component is excluded by the endpoints. Normalization modulo E in B becomes normalization modulo Kf in A. The same argument applies to cup products. Hence this actual coefficient restriction preserves the Gerstenhaber bracket, including degree-zero insertions. With the polynomial coordinate normalization and generator brackets, the candidate's formula follows in all degrees.

## Source checks completed before sealing

- The official [OWR report](https://ems.press/content/serial-article-files/46571?nt=1), printed p.1363 / PDF p.47, visually confirms Question 5, its lower-right idempotent, the coefficient sequence, and Lemma 4. The source display itself does not spell out the M action.
- [Hermann v2](https://arxiv.org/pdf/1411.0836v2), Proposition 6.12 / PDF p.31, confirms the one-point-extension sequence and compatibility; Lemma 6.9 identifies its component map as tensoring by M. Section 9.6 and Lemma 9.7 / PDF p.45 tie the displayed algebra to the two-arrow example and give the relations determining its nontrivial permutation module.
- [Xu v2](https://arxiv.org/pdf/0805.3295v2), Section 3.1 / PDF p.15, visually confirms that g swaps the two arrows and h fixes both. The module is therefore the regular quotient for g and trivial for h, giving M=A/(y) after x=g-1,y=h-1. With the usual category composition this can be a right module; opposite passage gives the candidate's left-module algebra. All reversal signs disappear in characteristic two. The downloaded v2 body matches the original source-manifest SHA. An initially fetched v1 is also retained privately and separately identified; it gives the same action.

Full third-party source bodies, extraction files, response headers and rendered pages remain private. This public assessment contains original derivations and source locators.

## Initial verdict and exact remaining work

**No mathematical counterexample or blocking gap found in this approach family.** The strongest independently verified claim at this checkpoint is the all-degree, all-characteristic-two-field characteristic map, injectivity/image of the actual gamma, and its restriction compatibility. The degree-zero exception is real and is correctly handled by K+yA, rather than by ker chi_0=yA.

This is a first assessment, not an exhaustive novelty verdict. Xu's prior ring computation and Hermann's structural machinery are credited. Remaining work in this family: preserve a more explicit universal derivation as a checkable final artifact; implement independent diagnostics with active error checks in ordinary and optimized execution; show that deliberately wrong module/action, higher-degree normalization and corner/characteristic variants are rejected; then create final review, science result, and complete identity/publication manifests. These diagnostics will not replace the universal argument. No original author-code or prior-verdict input has yet been used.
