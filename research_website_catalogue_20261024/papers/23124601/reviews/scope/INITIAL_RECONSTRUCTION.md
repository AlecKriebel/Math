# Independent initial reconstruction — row106 /23124601

Created after reading the entire actual6-page deposited PDF and the complete20847-byte controlling TeX. Critical actualPDF4–5were rendered and viewed. No source checker, archived/current review or foreign primary body has been read. The original target's own abstract/metadata, manuscript and bibliography are the only scientific text consulted so far. This is a substantive early scope/proof ledger, not a theorem acceptance.

## Literal claim and conventions

Let B6 have fixed positive Artin generators a1,...,a5. Set c=(a1 a2 a3 a4)^5 (length20), h=a5 a4 a3 a2 a1 a1 a2 a3 a4 a5 (length10), z=(a1 a2 a3 a4 a5)^6 (length30), and G=B6/normal(ch^{-1}). This is a quotient by the normal closure of one relation c=h, not a quotient by a central element or by c=h=1. The braid identity z=ch=hc gives c²=h²=z inG, with z central inherited fromB6.

Inputs are literal words in the five fixed standard positive generators whose product inG is c². They are not arbitrary ordered conjugates of generators and not arbitrary positive nonseparating mapping-class factorizations. Strict Hurwitz replaces(x,y) by(x y x^{-1},x), or its inverse(y,y^{-1}xy); intermediate factors may be conjugates and need not remain standard. Simultaneous conjugation by any element ofG is a separate, explicitly broader equivalence. Both preserve tuple length. The theorem says exactly one strictclass atlength20 (representedh²), one atlength30(z), two atlength40(c² and(a2a3a4a5)^10). With simultaneous conjugation these become threeclasses. Every admittedlength20input word is literally one of10distinctcyclic rotations ofh². No zero/negative letters, arbitrarygenerators, variablebraidrank, or classificationofarbitraryconjugatefactorinputs is claimed.

Success requires the full upper boundm≤40 and necessarylinking pattern, an exhaustive validG-action rejection at20, an actualfaithfulB6 equality certificate at30, a faithful four-chain restriction at40, positive-monoid embedding and explicit localHurwitz moves, plus distinctionofstrictclasses. Noneofthose may be replacedby word/actionhash comparisons or by assumingsufficiencyoflinking data.

## 1. Geometric input and length cap

The proposed mapB6→Mod(Σ2,1) comes from a five-curve chain onΣ2,2 followedby cappingoneboundary. The odd chainrelation gives image(z)=tδ, and the four-chain evenrelation gives image(c²)=tδ, providedthe four-chain neighborhood aftercapping is the wholeΣ2,1 up to a boundarycollar. Then z=ch implies image(c)=image(h), so the homomorphism factors throughG. Every generator maps to a nonseparating positive twist. A maximum-length theorem for tδ must apply with genus2, oneboundary, noextra hypothesesonallowedpositivefactors. It givesm≤40 without requiringfaithfulnessofG→Mod. Exact theoremA and the chain/capping conventions remain to be checked in actual primary bodies.

AbelianizingB6 makesallgeneratorsequal. The addedrelation has exponentdifference20−10=10, soGab=Z/10: quotientpresentation gives atmostthat cyclicgroup and thesend-each-ai-to1mod10 map givesatleastit. Sincec² hasexponent40=0mod10, m belongs to{0,10,20,30,40}. Emptywordm0 remains to be excluded; centralityalone does not excludeit.

## 2. Normal-closure and integer linking argument

c andh are pure, hence so is the relatorr=ch^{-1}; its normalclosure is pure and the permutation mapS6 descends toG. Thus an admittedpositivewordw is pure already inB6. OnP6 use half signedcrossingcountsℓij, integral additivehomomorphisms; braidconjugation permuteslabels. Positivity givesℓij≥0 and m=2sumℓij. c² hasvectorβ with2onpairsamong1,...,5 and0on6-incidentpairs. c has1onthatclique andh has1on thestar at6, so relatorconjugateshavevectors rk=1−2·1[k in{i,j}] for k=1,...,6. A normalclosureexpression therefore gives integers ti of arbitrarysign with

ℓij(w)=βij+T−2(ti+tj), T=sumti=m/10−4.

The last equality follows independently by summingpaircoordinates: eachrk hassum10−5=5, so m/2−20=5T. This is onlynecessary; no integralpattern is assumed sufficientforquotientequality.

Write s=t1+...+t5 andt6=T−s. Internalpairboundsare ti+tj≤floor((T+2)/2); remainingboundsare ti+t6≤floor(T/2). ForT=−4,−3, summingtheteninternalbounds gives4s≤−10 ands≤−3. Summingthefiveotherbounds gives s≥−2 and−1respectively, impossible. ForT=−2 thoseboundsgive−1≤s≤0. Ifs=−1, t6=−1 and eachfirstti≤0; exactlyone is−1. Ifs0, t6−2; apositivefirstmaximumM forcesothers≤−M ands≤−3M<0, impossible, henceallfirstti0. Substitution gives doubledstars, includingstarat6 andatanyotherlabel.

ForT=−1, internalbounds gives≤0 andremainingbounds gives≥0, so s0,t6−1 andallfirstti0, givingℓij1for allpairs. ForT0, s≥0; iffirstmaximumM≥1 theotherfour≤1−M, sos≤4−3M≤1; otherwise s≤0. Ifs0, remainingindividualboundsti≤0 forceallzero. Ifs1,t6−1, allfirstti≤1, atmostonepositivebecausepairbounds≤1; sum1thenforces one1andfour0. These are preciselysixdoubledcliques with anisolatedlabel. This checks the all-integer proof without any finitecoordinate-box assumption. A finite integersearch could be a diagnostic only.

## 3. Length40 and the two strict classes

A positivewordwith anisolatedlinkingstrand has no crossings withthatstrand. It stays in itsinitialslotk. If2≤k≤5, otherstrands onoppositesidescannotcross eachotherwithout crossingthatstrand, contradictingthefullfive-labelclique. Hencek1or6. In thek6case, w contains onlya1,...,a4. FaithfulnessofB5's four-chain map toModΣ2,1 thenpromotesgeometric equalityofw,c² to equalityinB5. This is the oneplace a chainembedding, ratherthanjust aG→Modhomomorphism, is essential. The precisePerron–Vannier A4scope andeffectofboundarycappingmust bechecked in theprimarysource; a statementabout a differentambient surface or fillingquotientwouldnot suffice.

Positivebraidmonoidembedding makesgroup-equalpositivewordsconnected by positiveArtin/commutationrelations. A commutingadjacentpair isstrictHurwitzswappable. Ifxyx=yxy, twoinverseHurwitzmoves on(x,y,x) give(y,y^{-1}xy,x) then(y,x,x^{-1}y^{-1}xyx)=(y,x,y), so apositivebraidrelation is realized withoutimposingstandardintermediatefactors. Thusallk6inputs haveclassc². Thek1case is the shiftedwordw0.

The braid d=a1...a5 satisfies d ai d^{-1}=a(i+1) fori≤4, so conjugatesc²tow0. Sincec²=z inG andzcentral, bothproductsarez. StrictHurwitzpreservestheactualsubgroupgeneratedbythetuple, becauseeachnewfactor is in theoldsubgroup andviceversa. ItsS6image isS5fixing6for c² andS5fixing1forw0; these are distinct subgroups, not merelyabstractlyisomorphicones. The descendedS6map therefore proves strictinequivalence even ifG's faithfulgeometrywereunknown. Simultaneousconjugationbyd merges them. No extra central-product argument can silentlymerge these strictclasses.

## 4. Length20: complete universe and sound rejection

The doubledstar means thedistinguishedlabel crosses eachotherlabel4times and otherlabelsnevercross. Theirrelativeorder is fixed. Itsposition is a nearest-neighborwalk on1,...,6 returningtostart; movingacrossedgei recordsai. Because theother5labelsstay inorder, eachfixededgecorrespondstooneofthose labels. Fourcrossingspereachlabel means eachof5edgesused4times. Conversely suchawalkhas thepositivepure doubledstarvector. Complete enumeration canonlyprune whenanedge'scountwouldexceed4; atdepth20allcounts thenequal4. Needactual independentcounts81,162,162,162,162,81 anddistinctness810, not merelya supporthash.

The manuscript'sF4table has
A1=(1,12,13,14), A2=(1,-2,1;1;3;4), A3=(1;2,-3,2;2;4), A4=(1;2;3,-4,3;3), A5=(1;2;3;3,-2,1,4), with theprinted inverses. Signedwords mustbe fullfreereducedwords. Right-action wordcompositionapplies thenextgenerator substitution to thealreadyobtainedimages. Bothinversecompositions, all4adjacentbraidrelations, all6distantcommutations andAc=Ah must hold exactly. This is21fullautomorphism-equalitychecks whenbothinverseordersarecountedseparately. If theyhold, unequalF4actionsreject a candidateinG evenwithoutfaithfulness. Equalactions alone neveraccept quotient equality.

Acceptance is instead certifiedby theexplicit survivors beingexactly the10cyclicrotations ofh². Centralityh²=z makes thoseproducts equalz; inverseHurwitzmovesmove thefirstfactor tolast with finalconjugate z^{-1}g1z=g1. So theyformone strictclass. The exact10survivors andstarts1,2,2,2,2,1 remain finiteobligations, not assumptions. Boundarynegativecontrols shouldincludeusingonereducedgeneratorimageonly, omittinganypresentationrelation, erroneousleft/rightcomposition, and equatingactionhashesratherthanfulltuples.

## 5. Length30: finite lift consistency, not linkingsufficiency

Allℓij1 means eachlabelledpaircrossestwice. The proposed state is15ternarypaircounts qij≤2 plus currentlabelorder. Forreachableq, pairparitydeterminesrelativeorderofeverylabelpair, henceuniquelythepermutation; a paritypatternneednotalwaysbetransitive, butunreachablepatternsarenotmergedinto thereachableuniverse. Astate determineslegalnextadjacentpairs andcostupdates, so mergingonlybyreachableq preservescontinuations. Totalcountstrictlyincreases upto30; noquotientcycleorunboundedwordsearchoccurs.

Letf=(2,...,2). Completewordsareexactlypaths0→f. To reverse apositivecompletion fromq tof, startatidentity(finalpermutationatf), execute thegenerators ofthatcompletion inreverseorder, retainingpositivecrossings. The sameadjacentlabelsmeet inreverseorder; thecountsaref−q. Conversely a reachingpath forf−q endsatthepermutationofq (sameparities), andthereversegeneratorsequencecompletesq. Countsneverovershootbecauseall incrementsnonnegativeandfinalvectorf. ThusS={qreachable:f−qreachable} is exactlythecoaccessiblegraph, not anassumedBooleanfilter. Independentbackwardexploration is a materialnegative/positivecheckofthis step.

ChooseoneparentpathanditsactualfaithfulArtinF6action U(q) for everystate inS. Everychosenancestor is inS becauseitstillhasacompletion. For everyallowededgeinsideS, fullsix-reducedword equality T_i(U(q))=U(q') proves theliftindependentofpathbyinduction. IfU(f) equalstheactionofz, faithfulnessgivesallcompletewordsw=z inB6, thenpositivemonoidembedding/Hurwitzrelationsgiveonestrictclass. Counts234368/711342and90921/261810 arechecksums, not theproof: everyliteral edge comparison andtheendpointcomparison mustbe recomputed. Complete streamhashaf2b8ec... canauthenticateoutputsbutcannotreplacecomparisons.

Equal linkingcounts donotdeterminethebraidglobally. The paper's a1²a2² versus a2²a1² arepositivepureprefixeswithsamecounts/permutationbutdifferentactions. The valid30-proof mustexcludethesestatesfromS andmustnevermergebraidactionsjustbecauseqagreeswithoutcheckingedges. Thecentralfinite theorem for sixstrands is claimed evenifthegeneralCassonassertion, reportedwithoutproof byElrifai–Morton, is unavailable.

## Primary and originality boundaries to check after this seal

1. Wajnryb'sactualSection3/page126: exactquotient, c/h/z conventions andwhether 'positiveword' reallyisfixed-generatorinput versusarbitraryconjugatepositivefactorization; exactHurwitzequivalencedefinition. Auroux'sseparateoperations mustnotbe conflated.
2. Baykur–Monden–VanHorn-Morris TheoremA: exactΣ2,1maximum40, positive nonseparating factors, boundarytwistandchain/cappingapplicability; noincorrectinjectivityassumptionforG.
3. Perron–Vannier A4faithfulness asactuallystatedbyWajnryb, and ideallyactualoriginalresult: correctsurface, chainmapandboundarycollar.
4. Gonzalez-Meneses actualSections1.6/4: faithfulArtin representation pluspositivemonoidembedding, withright-action convention translated explicitly. Groupbraidrelations mustnotbesilentlyreplacedwithmonoidrelationswithoutembedding.
5. Matsumoto'sactualTheorem1.3: doesitidentifythisexactG withModΣ2,1? It iscredit/backgroundforthecurrentgeometricbound except insofarasclaimsaboutthepriorpresentationare made.
6. SatoactualTheorem5.1/Table1/Remark5.1(1): exacthypotheses (sectionofselfintersection−1, relativelyminimal, genus2,no reduciblefibres), itspermittedlengths, whetherstatementoronlynecessity. This ispriorcredit, nottheprinted proof'smainlengthroute.
7. Elrifai–Mortonactualpage496: exacttwice-per-pair assertion andCassonattribution/proofstatus. No claimofnewgeneraltheoremorofnoveltyfrom a negativeliteraturesearch. Unknownprioritymayremain even ifcurrentproofchecks.

## Independent approach families and initial status

A. Exact source identity/fullnativeobjects/recursivegzipcustody: source-readysealed, alloriginalbytes preserved; authoredoldreviewsremainunread.
B. Quotient/input/equivalence semantics andall-integerlinking lattice: universalderivation above; nofinitesearchforsufficiency.
C. Geometricimportscope/boundarycapping/faithfulA4: highest externalapplicabilityrisk; actualprimarybodiespending.
D. F4presentationand20-worduniversesurvivor proof: ownindependent implementation plannedbeforeprovidedcodeuse; nofaithfulquotientrepresentationneeded.
E. F6finitegraph pathlift/reversal/coaccessibilityandwholeedgeequality: completenessproofabove; allfinitecomparisonsremainunverified. Avoidpromotingstatecounts/hashes.
F. Strictversussimultaneousclasses, positivebraidmonoidrelations and subgroupinvariant: mechanismcoherent; classicalembeddinginterfacepending.
G. Credit/firstness: explicitprimaryscopereviewrequired, defaultunknownpriorityandnoexternaloutreach.

No mathematical counterexample has been established atthisearlystage. The fulltheorem remainsUNVERIFIED pendingactualprimaryinterfaces andmeaningfulindependentfiniteproof reproduction. Source/supportPASS orhistoricalauditsarenotproof. A substantivegapwillberecordedpreciselyandreportedwithoutrepairorsilentnarrowing. Reviewcompletionestimate25%.
