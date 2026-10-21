# PR156 priority audit: current primary literature

UTC completion: 2026-10-12 (final seal supplies exact time). Original submission head: aec31742f3f26c5b1e533404da57539d17dc94a1; problem30005432; original queue claimed_solved, budget2/5. This is a private research audit, not a paper or a publication clearance.

## Finding and limits

The accepted counterexample is mathematically valid. The reviewed pre-September30 primary texts do not explicitly present its Z×Z4 operation or explicitly state the negative answer to unrestricted property-(s) ideal closure. That bounded non-discovery does **not** establish novelty. The example is a short specialization of an old four-element brace, a standard semidirect construction, and a prior finite-conjugacy characterization. Moreover, the September14 primary paper of Mondal, Shumyatsky, Trombetti and Yadav contains a different finite construction whose infinite-dimensional extension gives a negative answer to the same unrestricted closure question by a short calculation. This materially limits a broad discovery claim, even though that consequence is not stated in their paper and the extension is not isomorphic to our left brace.

Two material access gaps remain: the complete publisher version of Cascella–Properzi–Van Antwerpen (CPVA), and the complete publisher version/article-history online date of Mondal–Yadav (MY). Complete public CPVA postprint and MY preprint were read. Parent ROOT independently reports a later exact EulerSolve overlap and audits that work's history; this family does not certify mutual independence or global priority from citation silence. No new-paper clearance is given.

## Independence, evidence and coverage

The first assessment was sealed at 2026-10-12T05:57:02.303976Z before retrieving papers or consulting sibling priority leads. Its only inputs were the parent instructions, ROOT_MATHEMATICAL_GATE.json, and the preserved original COUNTEREXAMPLE.md. The original draft itself named CFT and CPVA; that dependency was disclosed. The first assessment and its byte hashes are preserved without retrospective editing. ROOT supplied the MY lead and its later-overlap report at the checkpoint recorded at06:03:01Z; subsequent parent journal/chronology information is explicitly labeled below. A later broad search also surfaced the EulerSolve abstract; it did not inform the sealed initial assessment. No historical original-review files or sibling priority reports were read.

Full textual readings: all23 pages of published CFT; all30 pages of CPVA arXivv2; all19 pages of MY arXivv1; all42 pages of MSTY arXivv1. Historical CFTv1/v2 and CPVAv1 were retrieved, and their relevant definitions, questions, examples, propositions, inventories and version differences were inspected; they were not each reread in full. Bachiller's original Proposition2.4 and its proof on arXivpp3–5 were read. Twelve decisive pages were rendered and inspected against text extraction. Unrelated finite probability theorems in MSTY were read for scope and potential implications, not independently recertified.

PRIVATE_SOURCE_MANIFEST.json preserves retrieval URLs, UTC times, response status, exact byte sizes and SHA256 hashes. PDFs, extracted text, metadata, diffs and renderings stay in private_sources. Current primary version metadata establishes submission/publication dates; these retrieved bytes are not an independently archived September30 snapshot. INPUT_OUTPUT_SEAL.json covers all inputs and all local outputs except the self-referential seal/digest files. The final digest file authenticates the seal. No external communication, Git/index/ref/MAIN, PR, Zenodo, or GWS mutation was performed.

## Exact property and translation

For z in a skew brace, the source property(s) requires both fixed indices

H_z=Fix^r(z)∩C_(B,+)(z), K_z=Fix^l(z)∩C_(B,circle)(z),

with H_z measured in the additive group and K_z in the multiplicative group. Here Fix^r(z)={g:z*g=0}, Fix^l(z)={g:g*z=0}. Equivalently each of z*B, B*z, additive conjugates and multiplicative conjugates must be finite. The first family holds the acting element z fixed while g varies. A finite lambda orbit of z only controls the opposite family B*z.

For our B, lambda_(n,c)(m,d)=(epsilon(c)m,(-1)^c d), with epsilon=(1,1,-1,-1). The lambda image has four elements, addition is abelian, and therefore every element is theta_f in CPVA's notation. Nevertheless z=(0,2) has z*B={(-2m,0):m∈Z}, an infinite family. Thus neither finite lambda orbits nor theta_f can substitute for exact(s). CPVA does not literally introduce a condition called property(F); its precise named conditions are lambda_f and theta_f. Any shorthand F must be defined explicitly and compared direction by direction.

The multiplicative conjugacy formula, for g=(m,d), is

g circle(n,c) circleg^-1=(epsilon(d)n+(1-epsilon(c))m,c).

For c=0,1 there are at most two conjugates; for c=2,3 the arbitrary integer m gives infinitely many. CPVA Proposition5.17 now yields exactly S=FC(B,circle)=Z×{0,1}, agreeing with the root's fixed-index computation. This prior characterization does not assert additive closure of the FC-centre in an arbitrary brace. It is consistent with our result. Our x=(0,1) has both indices2; additive2x=(0,2) has both infinite; lambda_x(x)=(0,3) also exits S. Multiplicatively, S is normal.

## CFT published paper and historical versions

I. Colazzo, M. Ferrara and M. Trombetti, *On derived-indecomposable solutions of the Yang–Baxter equation*, Publ. Mat.69(1)(2025),171–193, DOI10.5565/PUBLMAT6912508. Primary complete published PDF: https://mat.uab.es/pubmat/fitxers/download/FileType%3Apdf/FolderName%3Av69%281%29/FileName%3A6912508.pdf . ArXiv2210.08598v1:16October2022 17:51:56UTC; v2:14November2023 10:13:39UTC; current v2 record identifies acceptance by Publ.Mat. The publisher PDF records received15June2023 and accepted14November2023. These dates and the2025 journal year should not be replaced by PDF creation or retrieval timestamps.

Publishedp175 explains Fix^r, Fix^l and their different ambient group indices. Definition3.7 onp176 gives the exact property above. Examples3.4–3.6 onp176 show pathologies of a single brace centralizer/annihilator in finite braces; they do not show a nonideal set of(s)-elements, because every element of a finite brace is(s).

Example3.8 onp177 is exactly the old finite brace C=(Z4,+,diamond), c diamond d=c+d+2cd, with Ann(C)={0,2}. CFT credits Bachiller Proposition2.4. Bachiller's arXiv1407.5224v1,19July2014 22:08:51UTC, Proposition2.4(iii),p4, explicitly gives the general c+d+pcd operation on Z/p² and the p=2 multiplicative V4 group; its2015 journal citation is J.PureAppl.Algebra219(8),3568–3603, DOI10.1016/j.jpaa.2014.12.013. The finite ingredient is not new.

CFT Proposition3.10,p177, proves S is an ideal for a **two-sided brace**; the argument uses both distributive laws for star families. The immediately following sentence reports the general skew-brace case unresolved. This same open-status passage and old C4 example occur in CFTv1p7 and v2pp7–8. This is affirmative source evidence of the problem's historical status, not proof that no later work before September30 settled it.

Later CFT results study globally(S) braces and bounded variants. Our B is not globally(S), so their use of FC-groups, annihilator index, derived objects and finite solution decompositions does not apply globally. The order-six semidirect product mentioned after Theorem3.31 is finite and cannot itself display S nonclosure. The unrestricted product of finite braces discussed earlier can fail global(S), but its finite-support-mod-annihilator behavior does not provide the current counterexample. No contradiction of a source finite-quotient theorem is claimed. In particular, the independently recorded failure of a displayed f-map is not promoted here to a contrary theorem conclusion.

## CPVA full public postprint and current journal status

R. Cascella, S. Properzi and A. Van Antwerpen, *Finiteness conditions on skew braces and solutions of the Yang–Baxter equation*, arXiv2603.06177. Primary v1:6March2026 11:35:16UTC; v2:14September2026 12:04:32UTC, comment “Postprint version”. The PDF's front date is15September2026; the submission timestamp is14September. Both precede the original PR.

The actual publication is *Mediterranean Journal of Mathematics*23,article187(2026), DOI10.1007/s00009-026-03182-4; the publisher records publication26August2026, received11March, revised5August, accepted10August. Primary publisher: https://link.springer.com/article/10.1007/s00009-026-03182-4 . Crossref agrees on the date and article metadata; the institutional VUB record lists34pages. It should be cited as a published article with the public postprint version identified, not merely as a September preprint.

Full postprint arguments inspected: Definition2.11,p7, is the standard semidirect construction with trivial A and any homomorphism (C,circle)→Aut(A,+). It explicitly calls the construction recalled and cites the more general Facchini–Pompili work, *Semidirect products of digroups and skew braces*, Bull.Belg.Math.Soc.SimonStevin31(1)(2024),40–53. Definitions4.1 and5.4 introduce lambda_f and theta_f. Proposition5.8,p17, identifies theta_f=lambda_f∩FC(B,+), a strong left ideal. Proposition5.9 gives its ideal status under two-sided hypotheses. Definition5.14,p19, recovers all four exact(s) families; Lemma5.16 and Proposition5.17,pp19–20, prove exactS=FC(B,circle) under globaltheta_f. These results and the examples below already occur in v1.

Example2.12,p7, and Example5.10,pp17–18, use B=Z3×Q×Z with

(a,x,k)circle(b,y,l)=(a+(-1)^k b,x+2^k y,k+l).

Its theta_f=lambda_f=Z3×{0}×Z is not multiplicatively normal, but its exact S is Z3×{0}×{0}, an ideal. Indeed k≠0 gives an infinite fixed right-star image through (2^k−1)Q; k=0,x≠0 gives an infinite lambda orbit {2^l x}; x=k=0 leaves only the finite sign orbit in Z3, with finite multiplicative conjugacy. Thus this earlier theta_f counterexample cannot be treated as an exact(s) nonideal example.

Example2.13/5.18 is CD_infinity, additiveZ with n circle m=n+(-1)^n m. It has finite lambda image and exact S=2Z, an ideal. Its additive group has no C4 torsion and multiplicative group is D_infinity, whereas ours has additiveZ×C4 and multiplicativeD_infinity×C2. It is not isomorphic to ours. Example5.33,pp24–25, uses A=direct sum over primes of Z_p and a trivialZ action whose p-component generator has orderp−1. Its exact S=A×{0}: for k≠0, phi^k−id is nonzero in infinitely many p-components since p−1 divides k for only finitely many primes, producing an infinite fixed right-star image; k=0 elements have finite-support, hence finite action and conjugacy orbit. This S is an ideal.

Question5.21,p21, concerns an element with finite lambda orbit and both conjugacy classes; it is distinct from ideal closure. Theorem5.22 and Corollary5.23 show Soc(B)∩theta_f(B) is an ideal consisting of(s)-elements; in ours Soc(B)=Z×{0}, strictly smaller than S. Section6 solution decompositions and its examples do not explicitly contain the Z×C4 operation or its negative ideal conclusion.

Publisher PDF requests returned preview/cookie-error HTML; author SharedIt returned an empty challenge. No bypass was attempted. The exact remaining CPVA VOR gap is full comparison of its34-page statement body to the30-page public postprint, especially Definitions2.11/5.14, Propositions5.8/5.17 and Examples2.12/2.13/5.10/5.33, plus any added example or remark answering ideal closure. An author-labeled postprint is strong relevant evidence, but not a byte-identical VOR certification.

## What follows directly from the older ingredients

(C,circle) is V4, with three nontrivial sign characters. Their kernels are {0,2}, {0,1} and {0,3}; only the first is additively closed in C4. Taking the trivial braceZ and a sign action gives exactly the standard semidirect brace of Definition2.11. Its lambda image is finite, so Proposition5.17 reduces S to multiplicative finite conjugacy. The conjugacy formula above shows S=Z×ker(character). The two nonadditive choices are isomorphic via c↦−c, which is a brace automorphism of C. No mathematical sophistication beyond selecting one of these characters and making the elementary orbit calculation is needed.

Therefore our counterexample is a direct **application/specialization** of prior structural machinery. The explicit nonadditive character and its ideal-closure consequence were not stated in the core papers read here. This distinction matters: an unstated easy consequence does not establish that authors publicly disclosed the exact answer, but it also does not support inventing the brace or calling its ingredients new.

## Mondal–Yadav: full preprint, journal metadata, body gap

S. Mondal and M.K.Yadav, *Commuting probability of skew left braces*, arXiv2603.16771v1,17March2026 16:48:18UTC,19pages; only v1 appears in the primary arXiv history. Full text: https://arxiv.org/pdf/2603.16771v1 . Primary metadata confirms *Journal of Algebra*712,491–519, cover date15February2027, DOI10.1016/j.jalgebra.2026.08.004. Publisher API https://api.elsevier.com/content/article/PII:S002186932600431X?httpAccept=text/xml and Crossref confirm the title/journal; MSTY's September14 bibliography already cites this VOR. Calling it solely an unaccepted preprint is inaccurate.

The exact available-online day is not verified by the primary material accessible here. Crossref has no published-online field; its created timestamp13August2026 15:01:46UTC is DOI registration, not publication. A secondary index says13August, but this is not used as certification. Publisher HTML requests failed403, view=FULL API failed401, ordinary XML API returned core metadata without originalText or article history. The publicly visible author publications page offers arXiv and stale submitted wording; that does not override publisher metadata.

MYp4 defines left/right brace centralizers with the exact fixed subgroups; their intersection is Cb_B(x). It defines FCI(B) by finite **multiplicative** index of Cb_B(x). MY explicitly states S⊆FCI and does not assert general equality in that version. Proposition2.3,p5, proves FCI is a multiplicative subgroup and a subbrace under two-sided, symmetric or lambda-homomorphic hypotheses. Proposition2.4 gives two-sided ideal status. These are conditional positive results, not an unrestricted negative ideal result.

In ours, FCI=S by direct formulas. For z=(n,c), Cb_B(z) consists of g=(m,d) satisfying (epsilon(c)−1)m=0, (epsilon(d)−1)n=0 and2cd=0mod4. For c=0,1 it containsZ×{0} and has finite multiplicative index; for c=2,3 it is finite because m=0, so has infinite index. The extra subbrace hypotheses fail: lambda_(x+x) differs from lambda_x² for x=(0,1), so it is not lambda-homomorphic; lambda_(x+x) also differs from lambda_(x circle x), violating the reversed lambda identity of symmetric braces. The root gate independently excludes two-sidedness.

The finite eight-element example onp4 shows a **single** centralizer fails additive closure; all its elements are(s). Example3.6,p8, repeats the old C4 brace for commuting probability3/4. The final infinite example,p18, is the direct product of the trivial braceR/Z and that C4 brace. Both operations are abelian there and lambda acts only on the finite C4 coordinate, so it is globally(S). Its compact-brace section proves Borel/finite-index facts about FCI, without an unrestricted negative S conclusion.

Required missing MY text: complete29-page VOR, in particular Section2 centralizer/FCI statements and proofs, every changed or added infinite example, and publisher article history giving actual online release date. Full preprint non-discovery does not certify absence from a longer published version.

## MSTY September14 full text: material implicit counterexample

S. Mondal, P. Shumyatsky, M. Trombetti and M.K.Yadav, *Relative commuting probability and BFC-type results for finite skew braces*, arXiv2609.16269v1,14September2026 19:31:58UTC,42pages, the sole primary version. All42pages read from https://arxiv.org/pdf/2609.16269v1 . Its pre-September30 status is primary-version evidence; it is an unrefereed preprint in the retrieved record.

Sections1–6 prove finite probability estimates and conditional results for classT (two-sided/symmetric/lambda-homomorphic). Theorem4.7,pp18–19, gives a finite counterexample family; Propositions5.9–5.12,pp28–31, give finite sharpness/obstruction families; Example6.12,p36, gives a finite derived-subgroup nonideal example. Finite braces have S=B, so these finite examples do not themselves answer exact(s) closure. The source's S(B) onp24 means {x:x*x=identity}, **not** property-(s) elements. Its C4 example onp33 again credits an old operation. General Proposition4.6,pp17–18, assumes finiteGamma2(B); general group Lemma5.2,p24, requires a uniform bound on both mutual conjugacy families. Neither implies S closure in our counterexample. Section7,pp37–40, studies potentially infinite structure braces through a finite socle quotient under classT hypotheses; it has no explicit unrestricted negative S statement. Its Example7.3 uses trivial solutions and free abelian structure braces.

However, Theorem4.7 supplies a **short prior route to the negative answer**. Keep n=1 and take U=direct sum over positive integers of F7 instead of its finite U_m=F7^m. Let V=F3², beta(v,w)=v1w2−v2w1, and z,t∈F3. Use exactly their formulas

(u,v,z)+(a,w,t)=(u+a,v+w,z+t+beta(v,w)),
(u,v,z)circle(a,w,t)=(u+2^z a,v+w,z+t).

The primary proof verifies associativity using bilinearity, the semidirect circle law, lambda_(u,v,z)(a,w,t)=(2^z a,w,t−beta(v,w)), and lambda_xlambda_y=lambda_(x circle y). Every identity remains valid for arbitrary F7-vector spaceU: multiplication by2 has order3; the additive finite factor is the Heisenberg group on V×F3. Thus the infinite extension is a skew brace, without assuming any probability limit or bound.

For x=(u,v,z) and g=(a,w,t), its four relevant families are explicit:

x*g=((2^z−1)a,0,−beta(v,w)),
g*x=((2^t−1)u,0,−beta(w,v)),
g+x−g=(u,v,z+2beta(w,v)),
g circlex circleg^-1=(2^t u+(1−2^z)a,v,z).

For z=0 all four families are finite: w,t range over finite sets, and the U-coordinate in the last family is one of u,2u,4u. For z=1,2, multiplication by2^z−1 is a nonzero scalar of F7, hence an automorphism of U. Distinct basis vectors a=e_j produce infinitely many distinct x*g, and infinitely many multiplicative conjugates. Therefore exact S=U×V×{0}.

Take x=(0,(1,0),0) and y=(0,(0,1),0). Both lie in S, but x+y=(0,(1,1),1) does not. More precisely, each of x and y has fixed indices3,3: both fixed intersections impose beta(v,w)=0 on w and leave U,z unrestricted. For their sum, both intersections impose a=0 as well, giving infinite index through the independent U basis vectors. Lambda_(0,(0,1),0)(x) has last coordinate1 and also leaves S. Thus additive closure and lambda-invariance fail, while S remains a multiplicatively normal subgroup.

This extension is not brace-isomorphic to ours: its additive group is nonabelian and locally finite of exponent21, while ours is abelianZ×C4 and contains infinite-order elements. It gives the same unrestricted negative conclusion, but does not establish the stronger abelian-additive version. MSTY does not state this extension or the property-(s) consequence. We must distinguish this independently checked, very direct implication of a prior primary construction from an explicit prior disclosure of the question's answer. A broad new-invention claim would omit a material prior mechanism.

MSTY references [21] Ferrara–Trombetti–Tsang, *A probabilistic approach to the Yang–Baxter equation and skew braces*, arXiv2608.20620. This further lead was recorded, not screened in this bounded family. It is not eliminated from a global priority search by its title or by search absence. ROOT's other families and final synthesis own that broader scope.

## Chronology and disposition

All CFT, CPVA, MY preprint, and MSTY versions discussed above precede September30. Parent ROOT supplied primary GitHub chronology: PR156 created2026-09-30T12:24:37Z, preserved head timestamp12:28:42Z; Zenodo v1 record23292254 created2026-10-11T05:15:40.640397Z. Those parent-supplied records were not independently fetched by this family. The original PR date and the later Zenodo record creation date should not be conflated. The October11 EulerSolve exact overlap and its public version history belong to ROOT's independently audited later-literature analysis. Lack of a citation to our PR cannot certify mutual independence.

Both normal and optimized diagnostic modes pass96,370 controls. They enumerate all V4 sign characters, verify the main conjugacy/right-star coefficients and the c↦−c isomorphism, and check all finite MSTY coefficient identities for the arbitrary-U extension. They also verify every finite coefficient combination in its conjugacy formula. Infinitude follows from the explicit all-integer formula or independent U basis vectors, not finite enumeration. These controls supplement the proofs above and do not recertify unrelated probability theorems.

Family result: **bounded priority audit complete; no novelty or publication clearance**. Strongest verified priority evidence: old ingredients and exact prior structural characterization; an alternative unrestricted negative counterexample follows directly from MSTY's pre-September30 finite construction. Exact explicit pre-September30 disclosure of our Z×C4 example was not found in the full primary texts read. Material VOR body/date gaps remain, and later exact overlap must be incorporated. Best-guess completion of this assigned bounded family audit100%; overall priority remains unresolved; no novelty probability is certified. No outside input was requested or prepared.
