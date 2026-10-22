# PR1114 independent priority falsification

Verdict: **the claimed complete oriented-surface conclusion follows from earlier published work by a standard, checkable branched-cover deduction. Do not publish it as a novel resolution.** This does not assert that the PR's direct formula is copied, that every exposition is identical, or that the first discovery of this deduction has been located.

Scope: PR1114, head `e1a11feef98ed0fde22375c983e30b72b268d265`, base `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`, catalogue30003952 / OWR-16415-015. All eight actual changed files are retained with immutable Git blob identities. There is no QUEUE change. This is an independent priority audit, not a complete re-audit of the PR's separate direct proof.

## Exact target and prior inputs

A'Campo's Problem9, OWR40/2018, printed2527 / PDF53, asks whether two prescribed right-twist classes about essential curves intersecting once on a negative-Euler-characteristic surface have actual representatives satisfying the three-term braid identity, in topological, C1 and Cr regularity. The original page was freshly fetched and visually read. The usual oriented-surface interpretation is retained; no convention-free nonorientable statement is inferred. A compact support/collar conclusion is stronger than that question.

Mann–Tshishiku, *Realization problems for diffeomorphism groups*, Theorem4.1, provides a smooth section for the three-marked disk. Its full proof, freshly read in arXivv1 and the different author-hosted PDF, constructs generators that act by rigid translations on small disks about the marked points and are identity near the outer boundary. Thus every word has the same local translation property. The arXivv1 is dated1February2018; the author publication page records Proc.Sympos.PureMath.102(2019),131–156. These inputs predate the present2026 work. The following elementary deduction supplies the precise surface conclusion.

Honda–Kazez–Matić, *Right-veering diffeomorphisms of compact surfaces with boundary II*, Geometry&Topology12(2008),2057–2094, printed2058 / PDF2, explicitly identifies the double cover of a three-marked disk with a one-holed torus and the induced braid mapping classes with its mapping class group. Positive half twists correspond to positive Dehn twists. This fresh publisher body and page were read and visually inspected. This is a mapping-class statement; the next argument independently handles actual smooth maps.

## Checkable deduction, including branch smoothness

Let D be an oriented smooth disk with three interior points P, and let H be a subgroup of its orientation-preserving diffeomorphisms. Assume every element fixes a common outer collar and, in common oriented Euclidean charts about the points of P, is a translation from one marked disk to another. These hypotheses hold for the image of the cited section, as just specified.

Construct the connected double cover of D minus P whose monodromy sends each meridian to1 in Z/2, and fill in the three branch points using the local charts

`pi_i(w)=p_i+w^2`.

Call the filled surface N. Its Euler characteristic is `2 chi(D)-3=-1`. The boundary monodromy is the sum of three meridians, hence1; the preimage of the boundary is connected. Therefore `2-2g-1=-1`, so N is a compact genus-one surface with one boundary component.

Every f in H permutes meridians up to conjugacy and preserves this monodromy homomorphism. Hence it lifts on the unbranched complement. Choose the unique lift fixing a chosen point over the outer boundary. Because f is identity on the collar, that lift is identity on the whole lifted collar: there the two possibilities are the identity and the nontrivial deck transformation, and only the former fixes that point. If `f(p_i)=p_j`, then locally `f(p_i+z)=p_j+z`. Consequently a lift satisfies `g(w)^2=w^2` near the corresponding branch point. On the punctured local disk the sign is constant, so `g(w)=w` or `g(w)=-w`; either extends smoothly and invertibly over0. Away from the branch points smoothness follows from ordinary covering charts. The inverse satisfies the same argument. Thus the lift is a C-infinity diffeomorphism with C-infinity inverse.

The product of the chosen lifts of f and h is a lift of fh fixing the same boundary point. Uniqueness therefore gives `L(fh)=L(f)L(h)` exactly. In particular, if sigma1,sigma2 are the standard positive half-twist generators and rho is the earlier section, then

`A=L(rho(sigma1)), B=L(rho(sigma2))`

satisfy `ABA=BAB` as maps, not just in a mapping-class quotient.

The induced mapping-class lift is the standard geometric lift. Indeed a base isotopy relative to the boundary and marked set lifts uniquely once its boundary lift is fixed; it extends continuously over branch points. The half-twist-to-Dehn-twist correspondence then gives `[A]=t_alpha0` and `[B]=t_beta0`, for the preimages of the two standard adjacent arcs. These simple closed curves intersect once. There is **no free boundary-twist offset**: we use the particular geometric lift of the prescribed half-twist mapping class, with its boundary lift fixed, not merely its action after capping or on homology. The cited correspondence is stated for the one-boundary surface, before capping, and preserves positive handedness. With the opposite consistent sign convention, invert both generators; the braid identity survives simultaneous inversion.

For any prescribed essential intersecting-once pair in an oriented surface S, a compact regular neighborhood is an oriented one-holed torus. An orientation-preserving diffeomorphism of this neighborhood with the labeled model carries alpha0,beta0 to the prescribed pair up to isotopy. Conjugate A,B by it and extend by identity outside the neighborhood. The common identity collar makes both maps and inverses globally smooth, and the map identity and prescribed twist classes are preserved. The neighborhood can be arbitrarily small and avoid any boundary, marked points or punctures. This proves precisely the asserted stronger conclusion in every allowed negative-Euler-characteristic case.

This deduction does not assert a section of the image after additional ambient relations are imposed, nor a realization of a full higher-genus mapping class group. Those are different statements and do not follow.

## Deliberate failure checks

* A bare arbitrary smooth disk action is insufficient for smooth branched lifting. For example `f(x,y)=(2x,y)` at a branch point need not have a differentiable lift through `z=w^2`. If a derivative existed and were the real-linear map `a w+b conjugate(w)`, comparing its square would force `a^2=3/2`, `b^2=1/2`, and `2ab=0`, which is impossible. This shows why the actual translation germs, rather than only Theorem4.1's headline, are used.
* Odd branch count, connected boundary and selection of the boundary-fixed lift are essential to the stated one-holed-torus model and canonical group homomorphism. We do not choose lifts independently up to deck transformation.
* Theorem4.2 is printed for **even** branch count `2g+2`, with two boundary components. It is not cited as an already-stated odd-three-branch theorem. The odd case above is proved separately using the controlled germs in the proof of Theorem4.1.
* The finite/cyclic PSL2 presentation generators in the prior construction are not confused with the adjacent half-twist generators. The section is evaluated on sigma1,sigma2; words preserve the translation property.
* The original question's 2018 open-problem label cannot override the explicit earlier theorem and the deduction. No assertion is made about what the questioner or other individuals knew.

## Evidence and boundaries

Fresh HTTPS200 source bytes are retained privately: originalOWR562604bytes SHA256 `0bd596abb171c94b1ff9352fba8f2a2cf91e12dd29180590ce2425054ea17de7`; MTarXivv1540597bytes `734ec498c4372338e955584beb965c74c4962c700efdf7890d9ae33ea988f340`; MTauthor435040bytes `61d33edd64e46acdb343bcfd0282e10112fd2ce268f56a19614a5bad8b40fd69`; HKMpublisher365317bytes `c7722a8c4f15b10db47bd5129a4768693a1062e0277fb919d75ae47ac8e94c5e`. Text extractions and the four visually inspected page images are retained with hashes. The university-hosted Farb–Margalit Version5 draft was also fetched, but its scattered branched-cover discussion is not needed for the decisive conclusion. No publisher-final version of MT or FM was independently verified. An initial web-tool DOI open returned an internal access error; direct fresh OWR publisher retrieval subsequently succeeded. That failed tool observation is not represented as an HTTP response with retained bytes.

Twenty query strings covering the exact original question, alternate A'Campo spelling, actual representatives, smooth braid realization, one-holed torus and half-twist lifts were searched. The query log records their limits: raw search-result response bodies were not retained and search nonresults are not an absence certificate. Only primary bodies support the conclusion. First discovery, authorship of the elementary deduction, exhaustive literature coverage and current worldwide open status remain unestablished. They are unnecessary for rejecting publication as a new full resolution, since the full conclusion already follows from explicit earlier primary inputs.

The parent's fresh180-row GWS check at22:27:59 found no exact problem/alias/Dehn-twist/smooth-braid publication match. Its retained narrow leads and ledger snapshot were copied as context, not independently refreshed here. This report does not certify all repository/Zenodo duplication checks or authorize a spreadsheet row.

No outside individual or unrelated agent was contacted. No original proof program was executed, no publication/PR/ledger mutation occurred, and no shared Git index/ref was changed. The report is AI-assisted and unrefereed; the artifact verifier certifies frozen byte integrity and simple exact controls, not formal proof correctness or human peer review.

## Primary references

1. [Original workshop report, Problem9 printed2527](https://ems.press/content/serial-article-files/46762?nt=1).
2. [Mann–Tshishiku arXivv1, Theorem4.1 and full proof pp18–19](https://arxiv.org/pdf/1802.00490v1).
3. [Mann–Tshishiku author-hosted PDF](https://pi.math.cornell.edu/~mann/papers/RealizationProblems.pdf) and [author publication record](https://bena-tshishiku.github.io/publication/nielsen-survey).
4. [Honda–Kazez–Matić publisher PDF, printed2058](https://msp.org/gt/2008/12-4/gt-v12-n4-p06-p.pdf).
