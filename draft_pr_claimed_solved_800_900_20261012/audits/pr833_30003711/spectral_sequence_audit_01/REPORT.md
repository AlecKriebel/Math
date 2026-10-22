# PR833 spectral-sequence dependency audit

**Decision:** Chen-Wan arXiv:2306.17303v2 Proposition 4.2(1) is false for its stated constant-F3 characteristic map. The entire map in degree seven is zero. The asserted edge-kernel equality with the Chern ideal fails: in degree seven the actual kernel has dimension six, while the Chern ideal has dimension five. The proposed residual class C=y x x'^2 is killed by an additional differential. This invalidates that inspected proof of the lower-bound input used by the submitted equality claim.

This is a version-specific verification result. It does not prove that the genus is less than eight, and it does not assert that the inaccessible published article, DOI [10.1090/proc/17184](https://doi.org/10.1090/proc/17184), has the same proof or defect. The author supplied a separate upper-bound construction. Nothing here overturns that construction; its independent validation is outside this subaudit.

The initial independent reconstruction was saved before reading any other audit or root challenge. It is retained as `INDEPENDENT_RECONSTRUCTION.md`. This report supplies the completed spectral-sequence analysis and a checkable alternate-fibration calculation.

## 1. Frozen claim, sources, and criteria

The frozen candidate is `../source/author/PROOF.md`, SHA256 c42d7adb46caa0fd5fbaa4ad6006baf711a2a6674a69375671fa9cd86141b965, at PR833 head 0e6e23213494ecb4a7208f920d25d7b49502a5cb. Its equality claim is ordinary, unnormalized, section-based Schwarz genus exactly eight for the nine-flex cover over the smooth cubic coefficient space. It cites Chen-Wan Theorems 1.2/4.1 for genus at least eight. The complete 4,344-byte curated queue record was read; its literature assessment is a dated assertion to verify, not an axiom.

The exact inspected Chen-Wan version is [arXiv:2306.17303v2](https://arxiv.org/pdf/2306.17303v2), 173,395 bytes, SHA256 be48f13fbffd76508dff6b37f8becc853c9a3f1c80e4068b2ee5652c36c1bbc8. Its pages 5-7 state and prove Proposition 4.2. All three pages were extracted, rendered, and visually inspected.

The independent primary comparisons are Ian J. Leary's [mod-p paper, arXiv:0711.4831v1](https://arxiv.org/pdf/0711.4831v1), Theorem 2 and proof on pages 2-3 and Theorem 7 and proof on pages 11-13; and his [integral paper, arXiv:0711.4826v1](https://arxiv.org/pdf/0711.4826v1), Theorem 2 and proof, especially pages 6-7. Relevant equation pages were rendered and visually inspected. Exact hashes and reading receipts are in `SOURCE_LEDGER.json`. These are public author-uploaded primary copies; no restricted access was bypassed.

Success would require a nonzero class for the actual map cl*:H^7(BK;F3)->H^7(PU(3)/K;F3), or a correct checkable replacement lower-bound proof. Failure of the displayed class alone would not refute the whole proposition; the duality argument below refutes the entire claimed nonzero map. The coefficients, actual embeddings, manifold hypotheses, all differentials that can enter degree-seven row zero, and extension issues are checked explicitly.

## 2. Actual groups and classifying maps

Write w=exp(2 pi i/3), and use the exact determinant-one matrices

A = [[0,0,1],[1,0,0],[0,1,0]],   B=diag(1,w,w^2).

Their projective images generate K=C3^2 in PU(3). Put H=<A,B,wI> in SU(3), and Ptilde=<A,B,U(1)I> in U(3). These are different groups: H is discrete of order 27; Ptilde has nine circle components. Direct multiplication gives BA=w AB. Every element of H has a unique normal form w^t A^a B^b. In F3 coordinates its multiplication is

(a,b,t)(d,e,s)=(a+d,b+e,t+s+bd).                         (1)

Distinctness follows by comparing the monomial matrix positions and entries. The center and derived subgroup both equal <wI>, and H_ab=K. The full inverse image of K under SU(3)->PU(3) is H. Therefore

M=PU(3)/K=SU(3)/H=U(3)/Ptilde.

SU(3) is simply connected, for example by the homotopy sequence of SU(2)->SU(3)->S5 and SU(2)=S3. Thus pi_1(M)=H, up to the harmless opposite-group convention for right deck transformations.

Let u:M->BH classify the universal cover, q:H->K the quotient, j:M->BPtilde the principal-Ptilde characteristic map, and p:Ptilde->K the quotient. The map in the preprint is cl=Bq o u=Bp o j up to homotopy. In particular its induced map on H1 is an isomorphism, because H_ab=K. The exact finite replay checks all 729 actual matrix products, all 19,683 associativity triples, the central-coordinate coboundary, and the rank of the one-cochain differential.

## 3. Independent structural falsification

Define y(a,b,t)=a, y'(a,b,t)=b, and the central-coordinate one-cochain t(a,b,t)=t. Equation (1) gives

(delta t)(g,h)=-b d=-(y' cup y)(g,h).

Hence y'y=0 and yy'=0 in H2(BH;F3), and also in H2(M;F3). This does not assume a ring presentation from either paper. A directly ordered certificate is f(a,b,t)=t-ab, for which delta f(g,h)=a e=(y cup y')(g,h). The replay verifies the first version on all 729 pairs. At the odd prime three, y^2=y'^2=0 by graded commutativity.

M is a closed connected smooth real eight-manifold. It is oriented: a Lie-group orientation on SU(3) descends, since each finite right translation is isotopic to the identity through right translations in the connected group. Poincare duality over F3 gives a perfect pairing

H7(M;F3) x H1(M;F3) -> H8(M;F3)=F3.                  (2)

Now H*(BK;F3)=Lambda(y,y') tensor F3[x,x'], with degrees 1,1,2,2. Every degree-seven class is yP3(x,x')+y'Q3(x,x'), and multiplying it by any degree-one class produces a multiple of yy'. Its pullback therefore annihilates both generators of H1(M;F3). They span all H1(M), since cl* is an isomorphism on H1. By (2), every pulled-back degree-seven class is zero:

cl*:H7(BK;F3)->H7(M;F3) is zero.                     (3)

The target is not zero: its dimension is two by (2). Neither normalized versus unnormalized genus, a cup-product sign, nor a right-action convention changes (3).

## 4. The correct Leary ring and the actual Chern classes

Put R=H*(BPtilde;F3), and write c for Leary's degree-four class and z for his degree-six class. It is graded commutative, generated by y,y',x,x',c,z of degrees 1,1,2,2,4,6. The relevant complete homogeneous relations are

xy'=x'y,  x^3 y'=x'^3 y,  x^3 x'=x'^3 x,
cy=-x^2 y,  cy'=-x'^2 y',
cx=-x^3,  cx'=-x'^3,
c^2=x^4+x'^4-x^2 x'^2.

The exterior squares of y,y' vanish. Leary identifies the nonzero degree-two product y'y with the mod-three reduction of his integral chi_1. It annihilates x,x',y,y',c. It is not zero on BPtilde; it becomes zero on BH and M.

These are genuinely the Chern classes of the actual inclusion Ptilde->U(3), up to the harmless sign choice for y,y'. The representation is induced from the index-three subgroup <B,U(1)> and its character lambda B^b -> lambda. It is the irreducible three-dimensional representation whose center acts by scalar multiplication. Leary's integral Theorem 2 proof shows that its lower Chern classes are the corresponding chi_i with the binomial coefficient (1/3) binom(3,i)=1 for i=1,2, and defines z as its top Chern class. Thus C2=c and C3=z; C1 is a nonzero multiple of yy'. This can also be checked for C2 on the four rank-one projective subgroups by the three weights t,t+w,t-w, which give C2=-w^2.

Leary's commutator presentation can differ by inverting one chosen A-generator. This changes y and x by a common sign and leaves C=y x x'^2 unchanged. The central representation and C2 are unchanged. All statements below are therefore consistent with the actual matrices rather than only the abstract group name.

Chen-Wan's displayed Theorem 4.3 has cy'=-x^2 y' where Leary has cy'=-x'^2 y'. Their later equation (4.9) uses the latter. They also omit the degree-eight polynomial relation. If their erroneous displayed relation is read literally, associativity of c y'x' already identifies C with y'x'^3, putting C in the Chern ideal. The exact replay checks this. Correcting that transcription is necessary, but the corrected ring still has the extra differential below.

A basis of R7 is

A0=yx^3,
B0=yx^2x'=yx'^3=y'x^3,
C=yxx'^2=y'x^2x',
D0=y'x'^3,
zy, zy'.                                               (4)

Independence follows from Leary's stated monomial basis, or exact homogeneous ideal reduction. R3 has basis yx,yx'=y'x,y'x'. The degree-seven Chern ideal I=(C1,C2,C3) has basis A0,B0,D0,zy,zy': C1 R5=0, cR3 spans A0,B0,D0, and zR1 spans zy,zy'. Consequently

dim R7=6,  dim I7=5,  (R/I)7=F3{C}.                   (5)

Thus the preprint did locate a class outside the Chern ideal when the ring is corrected. The error is concluding that this ideal is the complete edge kernel.

## 5. Explicit killer in the SU(3) fibration

Leary Theorem 7 describes the finite lift H=P(3). In addition to y,y',x,x', it has Massey classes

Y=<y,y,y'>,   Y'=<y',y',y>,   deg Y=deg Y'=2.

The relations needed here, all on the rendered page 12, are

yy'=0, xy'=x'y,
yY=y'Y'=xy', yY'=y'Y,
YY'=xx', Y^2=xY', Y'^2=x'Y.

Let L=y'Y=yY', a degree-three class. These relations imply

xL=(y'Y')Y=y'xx'=yx'^2,
x'L=y'Y'^2=(y'Y')Y'=x^2y'.                            (6)

Leary gives the restriction of the actual second Chern class as

c|BH=-(xY'+x'Y+x^2+x'^2).                             (7)

Each term in (7), multiplied by L, equals C:

(xY')L=x y'Y'Y=x^2x'y'=C,
(x'Y)L=x'y'Y^2=xx'y'Y'=C,
x^2 L=x(yx'^2)=C,
x'^2 L=x'(x^2y')=C.

Over F3 this proves the exact identity

(c|BH) L=-4C=-C.                                     (8)

The script verifies (8) from the stated relations by exact homogeneous ideal reduction, without assuming any total-space cohomology.

Consider SU(3)->M->BH. Its fibre has exterior generators a3,a5, and d4(a3)=c|BH. Consequently

d4(L a3)=+/-C.

If L supported an earlier differential, the same target class would already have vanished; in fact no earlier outgoing differential from this degree-zero coefficient class is possible, and a3 is transgressive. Thus (8) explicitly proves that C maps to zero on M. The annihilating degree-three class L is absent from the image of R3. It is created on passing through the S1-fibration BH->BPtilde, whose Euler class is C1. This explains concretely why computing c times only R3 misses the killer.

Equation (8) is an independent check of the particular class in (3), using primary group-cohomology calculations and Chern transgression rather than manifold duality.

## 6. All differentials relevant to the original degree-seven edge

In the original fibration U(3)->M->BPtilde, the action on fibre cohomology is trivial: all right translations in connected U(3) are homotopic to the identity. Thus

E2^{p,q}=R^p tensor Lambda(a1,a3,a5)^q.

The universal transgressions pull back to d2(a1)=C1, d4(a3)=c, d6(a5)=z. The nonzero fibre rows are q=0,1,3,4,5,6,8,9. Write v=yy', a nonzero scalar multiple of C1. After d2, row zero is R/(v), row one is Ann(v) a1, and the corresponding rows obtained by multiplication by a3,a5 have the same coefficients. The new annihilator row is the crucial feature.

Here is the complete list of possible incoming differentials to bidegree (7,0):

| r | Source (7-r,r-1) | Effect |
|---|---|---|
| 2 | (5,1) | vR5=0 |
| 3 | (4,2) | row absent |
| 4 | (3,3) | cR3 spans A0,B0,D0 |
| 5 | (2,4) | nonzero extra differential, discussed below |
| 6 | (1,5) | zR1 spans zy,zy' |
| 7 | (0,6) | zero: Ann(v)^0=0 |
| >=8 | negative first coordinate | absent |

No d3 modifies these source calculations: row-four classes are row-one classes times a3, and row-six classes are row-one classes times a5; d3 vanishes on those transgressive fibre generators and has no possible target from row one. At the pages stated, the low-p source positions have no unlisted incoming boundaries.

At E4^{2,4}, the coefficient space Ann(v)^2 is spanned by x,x',v. Multiplication by c sends these respectively to -x^3,-x'^3,0 in row one. The first two outputs are independent, so

E5^{2,4}=F3{[v a1a3]}.                               (9)

The exact replay verifies this rank computation. Meanwhile E5^{7,0} has basis C,zy,zy'. The classes y a5,y'a5 in (1,5) survive to their d6, and that differential has image zy,zy', since the actual C3 is z. There is no r=7 source. Therefore the independently proven vanishing of C, either by (3) or (8), forces d5([v a1a3]) to have a nonzero C component.

Its other two components are zero by a concrete symmetry. The unitary matrix J fixing e1 and swapping e2,e3 normalizes Ptilde and sends A to A^-1 and B to B^-1. Its conjugation action fixes the central scalar group. Conjugation on U(3) is isotopic to the identity, so it fixes a1,a3,a5 and the Chern classes. On y,y',x,x' it acts by -1. Consequently [v a1a3] and C are fixed, whereas zy and zy' are negated. Naturality of d5 implies

d5([v a1a3])=lambda C,   lambda in F3^x.               (10)

Equivalently it is +/-C after fixing the transgression signs. This identifies the missing differential up to the unavoidable nonzero-unit normalization. It is a forced page calculation using the independently established total-space vanishing and explicit equivariance, not a claim to have constructed an explicit cochain representative for the d5 itself.

After (10), d6 kills zy and zy'. Thus E_infinity^{7,0}=0. The degree-seven edge map R7->H7(M;F3) is zero, consistently with (3). In particular

ker(j*:R7->H7(M;F3))=R7,
I7 is a strict subspace of that kernel.

There is no additive or multiplicative extension ambiguity capable of restoring C as an edge class. For total degree seven the edge lands in filtration seven, and E_infinity^{7,0}=F7H7/F8H7 with F8H7=0 in the first-quadrant sequence. A killed row-zero class therefore pulls back to zero. The two nonzero classes of H7(M) occur in lower filtration. This report does not need or claim a computation of every cohomology degree or the whole global edge-kernel ideal.

## 7. Adversarial repair and disposition assessment

The conclusion was tested against the actual lift, the characteristic-map factorization, signs, odd-prime exterior squares, compactness, orientability, the dimensions of H1 and H7, Chern labels, the misprinted ring relation, later differentials, and filtered extensions. Two materially different mechanisms agree: an explicit central-coordinate coboundary plus Poincare duality annihilates the entire degree-seven map; the Leary-Massey identity (8) explicitly kills the displayed class and explains the missing d5.

The completed independent lower-bound audit and root REPAIR_ASSESSMENT were read only after the first derivation was saved. They agree with (3) and (5). The root's source-access assessment states that normal publisher routes did not retrieve the final article body, and no inspected primary replacement was found. Those are bounded retrieval results, not mathematical evidence about the unavailable proof. This subaudit made no access bypass or outreach attempt and did not prepare outreach.

A convention correction or a different constant-F3 degree-seven class for this same map cannot repair this route: the entire map is zero. A proof with nonconstant coefficients or a different mechanism could still prove genus at least eight, but no such proof is supplied by this calculation. Assuming its existence would transfer the remaining lower-bound problem to an unsupported claim.

The proposed disposition is justified within independent-verification standards: withhold the submitted equality and any solved-result preprint/merge, preserve the independently cleared upper bound at most eight as a partial finding, and close this particular claimed-solved PR if no checkable lower-bound repair is recovered. The precise reason is that the inspected lower-bound proof fails and the required replacement is unverified. The reason must not be stated as genus below eight or as falsification of the published theorem. Bibliographic publication alone does not settle the explicit version-specific contradiction found in the inspected dependency.

The proposed public `../CLOSURE_COMMENT.md` and `../CLOSURE_PR_BODY.md` were also checked. Their mathematical account, qualification about the final journal proof, and planned distinction between verified upper bound and uncertified equality are consistent with this report. Minor editorial advice was to say the stronger OWR invariant is not resolved by this PR, rather than making a broader literature-status assertion, and to repair two missing spaces. Their deliberate EVIDENCE_COMMIT placeholders must be replaced by the pushed evidence commit before any posting. This subaudit reviewed text only and performed no PR action.

**Strongest verified result of this subaudit:** equations (3), (5), (8), and (10), including the strict degree-seven edge-kernel/Chern-ideal inclusion.

**Exact remaining gap for the candidate equality:** a correct independently checkable proof of the required genus lower bound, from the actual final article or another source/mechanism. No new central proof attempt was initiated. The parent effort budget remains 1/5.

## 8. Reproduction and artifact scope

Run `python3 exact_replay.py` in this folder. Its default result path is beside the script, independently of the caller directory. To replay from the parent audit folder without changing canonical output, use `python3 spectral_sequence_audit_01/exact_replay.py --output replay/spectral_sequence_exact.json` (the destination directory must exist). It uses only Python's standard library, exact integers, and arithmetic in F3. `EXACT_RESULTS.json` records the matrix/cochain counts, H1 dimension, correct and literal-misprint Chern-ideal checks, the E5 source dimension, and the identity (8). Normal and optimized interpreter runs agree byte-for-byte; `REPLAY_RECEIPTS.json` records their commands and hashes. The mathematical deductions in Sections 3 and 6 remain explicit proofs, not formal proof-assistant certificates.

Private primary PDFs, extracted full texts, and page images are excluded by this folder's `.gitignore`; their hashes are recorded in the source ledger. `PUBLIC_MANIFEST.json` identifies the public report, initial reconstruction, exact replay, decision, receipts, and log, excluding itself and every private source/render. No Git, queue, PR, release, or external service state was mutated by this subaudit.
