# PR329 / problem20000450: bounded primary-source priority audit

The submitted computation gives an explicit answer for the regular pentagonal pencil in AIM Question17, interpreted through its smooth genus-one normalization and a chosen origin. Its universal Tate 5-torsion polynomial, radical parameter and full-torsion specialization criterion are established earlier mathematics. Fisher supplies the modular map, Verdure the full-torsion Kummer criterion, and Morton the identical degree-ten coefficient table and explicit complementary-point formulas. The appropriate contribution claim is the source-specific normalization, coordinate bridge, twist and resulting division-field computation. This audit found no earlier complete answer for that exact pencil in the inspected corpus. It does **not** certify first discovery, first application, or that the question remained open in2026.

This report concerns attribution and bounded historical comparison. The independent mathematical gate was reported PASS by the parent at2026-10-04T09:38:00.578674Z. The convention comparisons below are independently checkable; they are not a replacement for the geometry, arithmetic and division proofs. Final audit acceptance and publication authorization remain separate, external decisions. This held package is unsealed.

## Original question and precise target

The original is Question17, printed/physical51 of *Rational and integral points on higher-dimensional varieties*, the AIM workshop collection. The workshop ran11–20December2002; the retrieved PDF cover has a22November2004 version stamp. Both independent native access and the supplied original give the same502057-byte PDF, SHA2568b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6. The operative page and all four remarks were read in original pixels before candidate exposure. [Official original](https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf), [official HTML Question17](https://www.aimath.org/WWN/qptsurface2/articles/html/27a/).

The question takes the product of the five side-line equations of a regular pentagon and combines it with the square of the circumcircle equation to form a pencil of plane quintics. It asks for the 5-torsion of the genus-one curves. In a homogeneous model the degree-five term requires the additional projective coordinate factor multiplying the squared conic. One should compute on the normalization with an origin, rather than treat a singular plane quintic itself as a smooth elliptic curve.

The first source remark already states that the five points at infinity form a torsion subgroup. Thus exhibiting only that subgroup does not answer the full target: in characteristic zero the geometric kernel has25points, with20outside the marked cyclic subgroup. The other remarks discuss possible twists and conditional5-primary Tate–Shafarevich applications, a relation with a pencil discussed in workshop talks, and the role of regularity or a replacement of the circle by a star-pentagon expression. Those are context and further questions. They do not supply a proof of a nontrivial Tate–Shafarevich element, or ask this candidate to solve all nonregular or alternative pencils.

The original does not fix the coefficient field, scale of the line product, origin, exact parameter normalization or exceptional fibers. The candidate makes these choices explicitly. Their relation to the primary question, rather than equality of the symbol lambda under arbitrary rescaling, is the relevant equivalence. The current official HTML still displays the question and remarks. Such display is not a current-openness certificate; the collection includes later follow-up material and elsewhere discusses solved questions.

## Exact candidate assessed

Write r=sqrt(5), K=Q(r), phi=(1+r)/2, c=phi^5=(11+5r)/2 and d=5+2r. In the candidate normalization Q=X^2+Y^2-T^2 and

    P=2(X^5-10X^3Y^2+5XY^4)
      +5phi(X^2+Y^2)^2T-5phi^3(X^2+Y^2)T^3+phi^5T^5.

The pencil is P+lambda TQ^2=0. Its smooth normalization E_lambda has origin[0:1:0]. The submitted finite elliptic fibers exclude lambda=0,-5r,-c; the member at infinity is outside that elliptic family. The special plane fiber lambda=-(25+10r)/4 is cuspidal but its normalization remains elliptic and is included. Statements that require five ordinary nodes would unnecessarily omit it. The field assertions here concern the generic family over K(lambda), and finite lambda in K subject to these conditions, rather than arbitrary extensions or characteristic5.

The explicit birational reduction and quadratic twist lead to

    D_beta: y^2+(1-beta)xy-beta y=x^3-beta x^2,
    beta=(11-5r)lambda/[2(lambda+5r)].

The marked subgroup consists of the origin and(0,0),(0,beta),(beta,0),(beta,beta^2). The remainder of the 5-division polynomial has degree ten in x; both y-solutions give the remaining20points. For delta^2=d, a primitive fifth root zeta and theta^5=lambda+c, the asserted full coordinate field of E_lambda is

    K(E_lambda[5])=K(delta,zeta,theta),

with the analogous generic statement. Its degree over K is4 when lambda+c is a fifth power in K and20 otherwise; the larger Galois group is D_10 x C_2, with D_10 of order10. The asserted K-rational5-torsion is zero and the infinity subgroup becomes cyclic of order5 over K(delta). These field and twist conclusions are model-specific descent statements, in addition to applying the old Tate formulas. The previous generic universal F_20 example over Q discussed below cannot simply be substituted for this quadratic-base twist.

## Prior pentagonal progress that must be credited

The imported upstream report is explicitly partial progress. It already contains the pentagonal line polynomial, the known infinity subgroup and its quadratic character, the determinant/Weil-pairing quotient character, and a reflection/conic reduction with a first parameter. It expressly leaves the final lambda-to-Tate parameter, complementary20points, full coordinate field and complete exceptional set unfinished. It is therefore substantive prior work on this **same** pencil, while not an earlier complete answer to the full-kernel target in the inspected version.

The report describes itself as run27July2026. Upstream problem metadata carry later August2026 creation/update fields. Those are record fields, not independently established first publication times. The pinned HuggingFace dataset revision is37e53eabe540fb458758e198be61634bd02ee008. The independently retrieved full research_results.json and problems.json are byte-identical to the parent-provided dataset pins. The selected upstream report and the parent's current26309-byte report are semantically equal. A computed ASCII/indent2/newline serialization of that same upstream object exactly reproduces the author's historic26340-byte report hash56ce26a89b743cdf34807407c9e392dd1738b92c1982c661132ab159172eb93a. This is a reproducible semantic/serialization reconciliation, not a claim that today's file is byte-identical to a historically retrieved file. The separate historic6071-byte problem-wrapper serialization has not been reconstructed and remains a precise provenance limit. [Pinned dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008).

## Fisher: old Tate and full-level maps

Fisher's *Some examples of5and7descent for elliptic curves over Q* (JEMS3(2001),169–201) is the operative primary modular source. Lemma1.1 at172 gives the Tate family with a marked5-point; the discriminant is at173. Lemma3.4 and its proof at194–195 give the full-level parameter map. All33physical pages were independently read, and the relevant original pages were visually inspected. The paper records receipt6October2000, final form14November2000 and publication online15February2001; the current EMS page separately labels publication30June2001. These fields are preserved distinctly. [Published primary](https://ems.press/content/serial-article-files/31488).

For the candidate's beta, the old maps can be expressed using

    iota(v)=(cv+1)/(v-c),  eps(tau)=(phi tau+1)/(tau-phi),
    f(tau)=tau^4+3tau^3+4tau^2+2tau+1,
    g(tau)=tau^4-2tau^3+4tau^2-3tau+1.

The exact identity iota(eps(tau)^5)=tau f(tau)/g(tau), together with iota(beta)=-1/(lambda+c), is independently verified by the public checker. Thus the full-level cover and its Kummer mechanism are established inputs, not new modular theory. Applying them to the chosen pentagonal normalization requires the explicit beta(lambda) and twist bridge.

The retrieved author preprint *The Cassels–Tate pairing and the Platonic solids* is dated11October2001, with subsequent JNT98(2003),105–155 publication. Its universal Tate and isogeny/torsor formulas were read in scope. It concerns normal genus-one models in projective4-space and descent; a visual resemblance to a pentagon does not identify the singular plane quintic pencil. Fisher's invariants paper (2006arXiv,2008journal) and elliptic normal quintic paper (2011arXiv,2013journal) were also read in their operative introductory/theorem scopes. Their general Jacobian, Pfaffian and level5 theory does not by itself print the specific plane-to-Tate bridge assessed here. These scoped comparisons are not whole-paper negative certificates. [2001author preprint /2003article precursor](https://www.dpmms.cam.ac.uk/~taf1000/papers/ctp.pdf), [invariants primary](https://arxiv.org/pdf/math/0610318), [normal quintic primary](https://arxiv.org/pdf/1110.3520).

## Verdure: prior full-torsion and specialization criterion

Verdure's *Lagrange resolvents and torsion of elliptic curves*, IJPAM33(1)(2006),75–92, is a stronger direct attribution input. The author-hosted primary is a scanned18-page published article. All18original pages were visually read; its nearly empty text extraction was not mistaken for readable source text. [Original article](https://math.uit.no/ansatte/hugues/papers/IJPAM.pdf).

Theorem5 on84 concerns a nonsingular Tate curve in characteristic different from5. The displayed Tate curve on83 becomes exactly D_beta when Verdure's t=beta. With zeta+zeta^-1=(r-1)/2, the two discriminant roots appearing there are alpha_5=c and beta_5=-c^-1. His criterion is that all25points are rational over the field containing zeta exactly when

    (t-alpha_5)/(t-beta_5)

is a fifth power. Proposition3 and Corollary1 on80–81 give cyclic coordinate degree1or5 once the marked point and zeta are present. The proof on84–88 uses polynomial formulas over Z[1/5][T]; on88 it explicitly preserves specialization when the discriminant and necessary parameter differences remain nonzero. This is prior coverage of the nonsingular specialization mechanism, rather than only a generic-field computation.

In the candidate parameter the old value is exactly

    (beta-c)/(beta+c^-1)=c/iota(beta)=-c(lambda+c).

A fifth root is -phi theta. Since -1 and c=phi^5 are fifth powers, this is the candidate's Kummer extension. The old theorem supplies an upper inclusion by adjoining that root; the coordinate degree1or5 and criterion supply the exact fifth-root field when the value is not already a fifth power. Returning from D_beta over the twist-splitting field to the original E_lambda over K still requires its constant quadratic factor and descent. The candidate's excluded nonsingular Tate parameters are essential; the special cuspidal **plane** model is harmless once its Tate normalization is nonsingular. These distinctions prevent use of the old theorem outside its assumptions.

Verdure's original does not mention the AIM pencil, its circumcircle or the pentagonal normalization. That full-paper observation does not exclude an earlier application elsewhere, an oral workshop computation, or unpublished material. The article displays2006 and receipt9November2006; an exact online publication timestamp has not been established.

## Morton: identical old table and complementary coordinates

Morton's *Product formulas for the5-division points on the Tate normal form and the Rogers–Ramanujan continued fraction* gives old explicit product formulas for the complementary points. The exact relevant degree-ten table and radical are already present in the first public arXiv version,19December2016, not merely the expanded2018v4 or2019journal publication. Both full10-pagev1 and full19-pagev4 texts were read; original pixels atv1pages3–5 andv4pages5–7,18 were inspected. [V1primary](https://arxiv.org/pdf/1612.06268v1), [v4primary](https://arxiv.org/pdf/1612.06268v4), [JNT200(2019),380–396](https://doi.org/10.1016/j.jnt.2018.12.013).

Morton's curve

    E_5(b): Y^2+(1+b)XY+bY=X^3+bX^2

is exactly D_beta under b=-beta, with the same coordinates. Every one of the11coefficients of his D_5 table (v1p3/v4p5) equals the candidate's R_beta after this substitution. His epsilon=phi^-1 and epsilon_bar=-phi, and the old radical becomes

    u^5=(2b+11+5r)/(-2b-11+5r)=c(lambda+c),
    b=(epsilon^5 u^5+epsilon_bar^5)/(u^5+1).

Thus u=phi theta supplies the exact radical bridge. Theorem2.1 atv1p5/v4p7 provides both coordinates of the complementary points. V4p18 additionally identifies the generic coordinate field. That generic recovery statement is not used alone to justify all specializations: Verdure's prior theorem and specialization proof are the direct older input for those. Morton expressly credits Verdure's earlier Kummer element.

The19-page institution-deposited manuscript has different PDF bytes fromv4 but identical whole extracted text after whitespace normalization. It has not been identified as the journal's version-of-record PDF. The currently served arXivv4 PDF build date is2022; the displayed version and submission history remain11June2018. V1's earlier public date and actual operative formulas are independently documented. The universal coefficient table, radical solver and complementary-coordinate formulas should receive explicit prior credit wherever printed in the paper, supplement or metadata. They are not novel formulas attributable to this submission.

## Other leads and current-source follow-up

Consani–Scholten's quintic-threefold paper includes an old pentagonal line configuration and cites still earlier geometric work. Its relevant sections and examples concern a different polynomial family, including genus-six fibers, rather than the circumcircle-square genus-one pencil. This supports credit for older geometry and guards against confusing shared line configurations with an exact full-torsion answer. Original older Hirzebruch/vanGeemen–Werner works were not retrieved in this audit. [Primary](https://arxiv.org/pdf/math/0009134).

McCallum's1988 *On the Shafarevich–Tate group of the Jacobian of a quotient of the Fermat curve* was obtained as an original GDZ scan. The introduction and final page were read in pixels (printed637–640,666), not all30article pages. It concerns Fermat-quotient Jacobians, CM and pairing/5-primary questions. It does not supply an operative pentagonal normalization in the inspected scope; no broader negative claim is made. The EuDML index misspells its title as 'curvature'; the actual original title is 'curve'. Its relevance is source context, not a demonstrated Tate–Shafarevich application for every E_lambda. [Original scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0093/LOG_0032.pdf).

Cullinan–Kenney–Voight2022, *On a probabilistic local-global principle for torsion on elliptic curves*, gives a prior Kummer splitting-field statement for a universal5-isogenous family over Q (Lemma4.3.3,70–71). Its modular fractional linear parameter is related to iota. This independently supports the classical nature of the field machinery; its generic F_20 group is not the same base-field/twist statement as the candidate's D_10 x C_2. [Published primary](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1193.pdf).

The concrete newer AIM-citing lead *The elliptic sieve and Brauer groups* (2023) was checked against the published author-deposited primary. Pages1–5 and38 were read. Page5 expressly cites AIM Questions23and33 about sums of squares on elliptic curves, not Question17. Its complete extracted text has no pentagon/quintic/5-torsion occurrence. This closes that particular lead in its inspected scope; it is not a whole39-page reading claim. The official AIM Question17 HTML and Fisher's current author bibliography were also inspected. None of these current-source checks is evidence that an answer is still unknown to its original proposer. [2023primary](https://wrap.warwick.ac.uk/id/eprint/175726/2/Proceedings%20of%20London%20Math%20Soc%20-%202023%20-%20Bhakta%20-%20The%20elliptic%20sieve%20and%20Brauer%20groups.pdf).

## Actual candidate chronology and bounded archive checks

The retrieved PR metadata list two commits:0a77190f5ea7945a68ae6b5630f9730d876f3d16, author/committer2October2026 10:08:45Z, and96395a4f506af6a6045e3cd59afcba2db6b7e2e7,10:19:14Z. PR329 was created10:20:32Z and was open/unmerged at retrieval. All four original scientific files were retrieved independently at both exact commits, and all eight bodies are byte-identical to the frozen snapshot. The first tree lists12top-level files; the later tree adds review/publication/status material. The mathematical formulas did not change between these two public commit objects. Author/committer dates and a currently accessible commit do not establish the first push or the first time any unindexed version became publicly available. [PR329](https://github.com/AlecKriebel/Math/pull/329), [first commit](https://github.com/AlecKriebel/Math/commit/0a77190f5ea7945a68ae6b5630f9730d876f3d16), [second commit](https://github.com/AlecKriebel/Math/commit/96395a4f506af6a6045e3cd59afcba2db6b7e2e7).

All28returned GitHub release metadata names, bodies and asset names were scanned, with an empty second page. All19returned versions of the known repository Zenodo concept were inspected in metadata; the latest dates7September2026. None of those metadata identify this target. Their deposited archive contents were not inspected, so this is not a certificate that no older repository archive contains some relevant material. The exact numeric Zenodo query20000450 returns an unrelated record with that record ID, not the mathematical problem. A pentagonal/torsion query returns32records over two pages; their titles/metadata do not identify an exact earlier answer. Neither query is falsely recorded as a zero-hit search. [GitHub releases](https://github.com/AlecKriebel/Math/releases), [known repository concept](https://doi.org/10.5281/zenodo.21753404).

## Falsifiable comparison results and final scope

The prospective tests were fixed before candidate exposure. The full-kernel test identifies a completed computation beyond the old infinity subgroup. The equivalence test identifies the precise model and parameter changes, rather than equating every genus-one quintic. The stronger-prior-result test found **actual old direct coverage** of the universal polynomial, coordinate radical and nonsingular specialization criterion. The source-follow-up test found no complete exact pencil answer in the sources actually inspected, while preserving the oral/unpublished/current-status gap. The chronology test distinguishes record fields, source versions, commit objects and retrieval times.

The public standard-library checker performs25exact rational-polynomial comparisons over Q(sqrt(5)), covering all11coefficients and the Tate, Fisher, Verdure and Morton bridges. It uses no private PDF, raw imported report, network, symbolic-package installation or source-specific path. Its PASS establishes the stated formula comparisons, not independent firstness or a proof of the full candidate by itself. Native full stdout/stderr/exit receipts, source copies and early-exposure freezes remain private. The public package is a precise allowlist; the local whole-namespace verifier also checks their bodies/modes and the early freezes.

The scientifically appropriate publication framing is an explicit computation for the regular pentagonal pencil using established Tate/modular/division theory, with all prior source-specific progress and direct universal formulas credited. The bounded historical result is that no earlier complete exact-pencil answer was found in this audit's inspected corpus. There is no claim of a novel universal torsion object, first complete discovery or first application, continued openness in2026, or a proved Tate–Shafarevich/nonregular-pentagon extension. GAPS_AND_LIMITS.md and the source/search/reading/version ledgers identify every retained scope and version limit. These historical limits are not unresolved premises of the mathematical gate.
