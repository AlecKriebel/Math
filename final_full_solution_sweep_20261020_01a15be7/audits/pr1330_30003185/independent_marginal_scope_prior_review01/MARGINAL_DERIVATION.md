# Independent marginal and source derivation

This review is tied to PR1330 head cd07418b0517f90e2928918b91c120ec08ff5b0c. It does not adjudicate the192-class generation theorem or the subdirect-product bridge. Only the bridge's Section3 square-spinor refinement is reviewed. No successful pair of marginals is promoted to a simultaneous event or to generation.

The independently checked proposition is: for every odd prime powerq, every actual strong matrix involutiont in the indicated natural group, and either separately specified t-eigenspace, uniform actual-group sampling gives a strong restriction of inv(t t^g) with probability greater than1/(40000 logn) in Sp atn>=49152 and greater than1/(5000000 logn) in O/SO/Omega atn>=98304. The orthogonal counted event can additionally require both restrictions in Omega, retaining exactly half its mass and giving1/(10000000 logn). The GL/GU published laws transfer exactly to SL/SU by an elementary orbit argument. These are marginal/scope conclusions, not acceptance of the full new generation claim.

## Original quantifiers

The actual OWR37/2016 contribution printed2160–2161 (PDF38–39) fixes an arbitrary given strongt, chooses independent uniformg in the group actually under consideration, and defines strength using the closed natural-dimension interval[n/3,2n/3]. The sufficient displayed Problem is for each fixed sign, not simultaneous signs. Its modified target is C_G(t)'', rather than the whole centralizer. Its description of that subgroup as quasisimple is informally inaccurate for a product; the specified derived-subgroup target remains unambiguous.

The main question is explicitly asymptotic random-selection complexity. OWR does not spell out a confidence number, threshold or exhaustive family list. Its named LGO2009 reference Sections1.1–1.2 explicitly defines natural SL,SU,Sp,SO andOmega, with both even orthogonal types and odd dimension. The unitary dimension is overF_(q²). LGOSection2.1 defines big-O on sufficiently large integers and gives the sample size ceiling(-logepsilon)k for failure below a separately prescribed epsilon when the proportion is>=1/k. This is primary support for the consolidated sufficiently-large-n/fixed-confidence interpretation. It is an interpretation of the cited context, not extra words printed in OWR.

The literal all-dimensions sufficient marginal Problem is false. In Sp4 over any oddq, choose negative and positive symplectic planes. An output centralizes t and squares to1. Its restriction to a plane has determinant1 and is diagonalizable, so is I or-I; neither is strong. The actual marginal probability is0. This does not falsify the asymptotic sampling theorem. Conversely an absolute lower proportionc/logn only gives fixed confidence withK_delta logn calls; it does not by itself imply1-o(1) failure for fixedK. A Bernoulli lawp=c/logn has limiting all-failure probability exp(-Kc). LGO's convention supports prescribed fixed confidence; no primary text inspected here demands the stronger limit at fixed multiplier.

Natural groups are not silently enlarged to projective groups, order-four lifts, similitudes or arbitrary intermediates. Odd characteristic is essential. The hypothesis is t actually inG, incorporating determinant/spinor and symplectic parity constraints. There is no promise of an involution of every arbitrary proposed dimension/type. Counting random selections is not a theorem about exact order computation, sampler implementation, certification or total running time.

## Symplectic chart and absolute measure

Write t negative onA and positive onB with dimensions2a<=2b. Negatingt is harmless inSp and leavest t^g unchanged. Strongness givesa<=b<=2a. LetF:A->B, letF* be the alternating adjoint andK=F*F. IfK andI+K are invertible, F is an embedding, its image nondegenerate, and graphW has form beta_A(I+K). All nondegenerate alternating forms of dimension2a are isometric, so s_W is conjugate tot. Each graph determinesF uniquely.

For squarefree monicf of degreea avoiding0,-1, a semisimple self-adjointK with minimal polynomialf and characteristic polynomialf² has one symplectic conjugacy class. The primary extension fieldL_i acts self-adjointly; nondegeneracy of the trace pairing makes beta_A the trace of an alternating L_i-form. Alternation of the lifted form follows by testing beta_A(xu,u)=0 for allx inL_i; self-adjointness and odd characteristic give that equality. The primary space has L_i-dimension2, whose nondegenerate alternating form has unique isometry type. The centralizer is product Sp2(q^d_i). This yields |Sp(A)|/product|Sp2(q^d_i)| actualK, not a uniform-K assumption.

For fixedK the form beta_A K is alternating and nondegenerate. Isometric embeddings intoB form a transitive Sp(B)-orbit with pointwise stabilizer Sp(2(b-a),q); its cardinality is |Sp(B)|/|Sp(2(b-a))|, includingb=a. Divide the resulting number of graph conjugates by the FULL t-class cardinality |Sp(V)|/(|Sp(A)||Sp(B)|). For eachf the unconditional mass is

 P_f=|Sp(2a)|²|Sp(2b)|² /
     (|Sp(2(a+b))||Sp(2(b-a))| product_i|Sp2(q^d_i)|).

With |Sp(2r)|=q^(2r²+r)psi_r, psi_r=product_(j<=r)(1-q^(-2j)), the exponent is2a-3sumd_i=-a. The normalized expression is

 q^(-a) psi_a²psi_b²/(psi_(a+b)psi_(b-a)) product_i(1-q^(-2d_i))^(-1).

Forq>=3, psi_r>=1-sum_(j>=1)q^(-2j)>=7/8. The mass is at least(7/8)^4 q^(-a)>q^(-a)/2. No graph-chart probability was discarded. When a=b there is no factor2 class-centralizer correction: a centralizer must preserve the labeled +/- spaces, not exchange them.

## Common spectral mechanism

Relative toA+F(A), direct projection onto the graph gives the block operator

 [(I-K)(I+K)^(-1),  2K(I+K)^(-1);
  -2(I+K)^(-1),    (I-K)(I+K)^(-1)],

and it is identity on the perpendicular complement ofF(A) inB. For a primary rootkappa, lambda+lambda^(-1)=2(1-kappa)/(1+kappa), equivalently kappa=-(lambda-1)²/(lambda+1)². Avoiding0,-1 gives distinct reciprocal eigenvalues different from+/-1. All Frobenius conjugates and inverses have the same order two-part. The squarefree/minimal-polynomial hypotheses make the displayed operator semisimple. If one factor has uniquely maximal two-part>1, raising to half the global order is negative exactly on that factor's block and positive on every other block and the complement. Negative dimensions inA,B are2k,2k forSp andk,k forO. The complement inB counts toward the positive dimension.

Take d=2^h>=4 and k=d times odd. Half ofF_(q^k)^* has maximal order two-part(q^k-1)_2. The overcounted union of proper subfields has size below(3/2)q^(k/2). Forq>=3,k>=4, (q^k-1)/2-(3/2)q^(k/2)>=q^k/4 (writeu=q^(k/2)>=9 and checku²-6u-2>=0). For full-degree lambda, kappa has degree eitherk ork/2. The latter would imply lambda^(q^(k/2)+1)=1, whose two-part is2 becausek/2 is even, whereas the selected two-part is>=8. Thus kappa has full degree. The rational Cayley map has exactly two preimages, lambda andlambda^-1; Frobenius orbits then yield>=q^k/(8k) irreducible factors.

For e=v2(q²-1), the maximal possible eigenvalue two-part at a degreej factor is2^(e-1) forj odd and2^(e+v2(j)-1) forj even, by the elementary2-adic identities forq^j+/-1. A distinguished degree d timesodd has2^(e+h-1). Forbid remainder degrees divisible byd; every remaining factor then has smaller two-part. This is the credited Dixon–Praeger–Seress mechanism; the new chart masses are a separate calculation.

## Remainders and the two separate targets

At leastq^r/3 monic degree-r polynomials are squarefree and avoid0,-1. Forq>=5 use the union bound q^(r-1) nonsquarefree and two forbidden roots; handle r0,1 directly. Forq3 the exact normalized generating series is(1-u²/3)/[(1-u)(1+u/3)²], giving c_r=3/8+(-1)^r3^(-r)(10-8r)/16>=1/3. A union bound on irreducible degrees divisible byd removes at mostq^r(1+logr)/d, usingN(q,jd)<=q^(jd)/(jd). For d>=12(1+loga), at leastq^r/4 remain for0<=r<=a. No independence claim is needed.

ForSp choose the least power2 d>=12(1+loga); d<24(1+loga). At a>=8192 one hasa>=576(1+loga)>24d, because at8192 use log2<7/10 and thereafter a/(1+loga) increases. The targetA interval is[a/3,2a/3]. The targetB interval is[b/3,min(2b/3,5a/6)]. For everya<=b<=2a its width is at leasta/6 and its upper endpoint at most5a/6. The arithmetic progression d timesodd has spacing2d, so each interval contains at leasta/(12d)-1>=a/(24d) eligiblek. All remainders have degree>=a/6.

Each goodf has exactly one factor with degree divisible byd, so its distinguished factor, degree and remainder are uniquely recoverable. The counts do not overcount acrossk. The number of goodf is at leastq^a/(768d); each has unconditional mass>q^(-a)/2. This gives>1/(1536d)>1/[36864(1+loga)]>1/(40000 logn), since n=2(a+b)>=4a and log4>1. Both targets are covered separately. This derivation has no simultaneous-event step.

## Orthogonal orbit and geometry

Use symmetric beta withQ(v)=beta(v,v)/2 and discriminant detbeta modulo squares. Over an odd finite field, dimension and this class classify nondegenerate symmetric forms. Both odd-dimensional determinant classes must be retained even though their abstract groups can be isomorphic by scaling. In even dimension2r the split sign ischi((-1)^r detbeta).

Each strong t-eigenspace has dimension>=3. It contains a hyperbolic plane, which represents every nonzero field value. Reflections in that eigenspace, extended by identity, centralize t and realize(-1,square) and(-1,nonsquare) under determinant/spinor norm. These generate O/Omega, so O=Omega C_O(t). Thus the particular O-class of t is one Omega-class and one SO-class. Uniform actual O,SO,Omega conjugators give exactly the same t-conjugate measure. Negatingt can be done after this reduction, without assuming-I belongs to the initial group; target labels merely swap. The centralizer of t and-t is the same matrix subgroup.

Let dimA=a<=b=dimB and c=b-a. GraphW is isometric toA exactly whenchi(det(I+K))=+1. A_K has discriminant discA detK. Forc>0 its complement exists in either determinant class and has discC=discB/(discA detK); classification yields the required embedding. Forc=0 the necessary and sufficient condition ischi(detK)=chi(discB/discA). This cannot be dropped. For each admissibleK the embedding fiber is |O(B)|/|O(C)|. Fixing thedetK character fixes complement type. The proof choosesalpha=chi(discB/discA) forc0 andalpha=+1 forc>0; it is allowed to retain only that subset.

For squarefreef of degreea, primary spaces are mutually perpendicular because their projections are self-adjoint polynomials inK. Each is1-dimensional overL_i=F_(q^d_i) with balanced formTr(c_i uv). The nondegenerate trace pairing proves this description, and changes of extension-field basis identify exactly two square classes ofc_i. Each has isometry centralizer{+1,-1}. Norm maps preserve quadratic character, so toggling one trace-form class toggles its base-field discriminant. Exactly2^(s-1) of2^s choices have the prescribed total discA. Thus all actualO(A)-operator classes together contribute exactly|O(A)|/2, for EACHf. The determinant characters arechi((-1)^a f(0)) andchi((-1)^a f(-1)), depending only onf, not those trace choices.

Dividing graphs by the full t-class gives per admissiblef

 P_f=|O(A)|²|O(B)|²/[2|O(V)||O(C)|].

Theq-exponent isa(a-1)+b(b-1)-[(a+b)(a+b-1)+(b-a)(b-a-1)]/2=-a. The exact order products give7/6<=eta(U)<=8/3 for every positive dimension and type;eta(0)=1. Hence P_f>=q^(-a)2401/18432>q^(-a)/8, includingc0. This is an absolute full-class mass. Taylor's actual printed139–141 classification/order and163–165 spinor statements were independently inspected; no entire-book audit is claimed.

The Cayley distinguished factor hasdetK character+1 because evenk makes-1 a square inF_(q^k). Further1+kappa=4lambda/(lambda+1)² is nonsquare there, since maximal order two-part makes lambda nonsquare. Taking norms givesdet(I+K) character-1. Thus a remainder with signs(alpha,-1) gives the total(alpha,+1) chart sector.

## All four sectors, includingq3

For the three nonprincipal characters chi(f(0)),chi(f(-1)),chi(f(0)f(-1)), extended by0 on the forbidden-root polynomials, all monic degree-r sums vanish forr>=2: the two evaluations are independent linear coefficient constraints. Degree1 sums are-1,-chi(-1),-1; the last follows by counting(z²=c(c-1)) through the factorization(2c-1-2z)(2c-1+2z)=1. Thus each Dirichlet polynomial isL(u,xi)=1+su, s=+/-1. Its square is the principal character excluding BOTHlinear factors, whose series is(1-u)²/(1-qu). The squarefree Euler product is therefore

 S_xi(u)=(1+su)(1-qu²)/(1-u²)².

Itsdegree2j coefficient is1-(q-1)j, anddegree2j+1 is s[1-(q-1)j]. Forr>=1 the magnitude is<=qr/2. Fourier inversion over sign pairs and T_r>=q^r/3 gives each raw sector>=q^r/12-3qr/8>=q^r/16 forr>=8, using18r<=q^(r-1). Atq3,r8 the sufficient inequality holds; its ratio improves thereafter. Multiplying target signs bychi(-1)^r supplies the determinant sectors. This addresses all four signs without an asymptotic character estimate that could fail atq3.

For d>=32(1+loga), excluding factors with degrees divisible byd removes at mostq^r/32 globally, leaving>=q^r/32 in each sector. No independence of signs and degrees is used. Choose the least power2 satisfying this condition, so d<64(1+loga). At a>=32768 use log2<7/10 and monotonicity to get a>=1536(1+loga)>24d. The same two intervals give at leasta/(24d) eligiblek andr>=a/6>8. Counts yield>=q^a/(6144d) distinctf and probability>1/(49152d)>1/[3145728(1+loga)]. Finally1+loga<(4/3)logn forn>=2a,a>=32768, yielding>1/(4194304 logn)>1/(5000000 logn). No assumptionn>=4a was incorrectly imported from the symplectic notation.

## Exact half square-spinor refinement

The distinguished factor is one primary factor, and the positive-degree remainder has no factor of that degree type; thuss>=2. Impose square discriminant on its negative spaceU_* inA. One distinguished trace-form choice has this sign; among the other s-1choices exactly2^(s-2) have the complementary total discA. All operator class centralizers are2^s. The previously counted2^(s-1)classes have therefore lost exactly half their ACTUALweight. ThedetK anddet(I+K) signs and embedding fiber are unchanged, because they depend onf and the fixed total discA. This justifies probability mass, not merely an abstract sign count.

The corresponding negative spaceF(U_*) inB has the same discriminant class since det(K|U_*) is square. Its dimensionk is divisible by4. Both restrictions thus have determinant1. The spinor norm of-I on a k-dimensional negative space with orthogonal basis is2^(-k)disc(beta), by the product of reflectionQ-values; both factors are square whenk is even anddisc is square. Both restrictions lie inOmega. This proves the refined marginal>1/(10000000 logn), separately on either target, for actualO,SO,Omega sampling via the earlier orbit equality. It does not assert that all Bray outputs have square spinor norm on each component, or that two strong events happen simultaneously.

## Full-to-special laws and target scope

ForD=GL orGU andJ=SL orSU, respectively, let actualt belong toJ. The full centralizer isD(A)xD(B). Its determinant map is ontoD/J: scale one nonzero basis vector inGL, or one vector of an orthogonal Hermitian basis by an arbitrary norm-one scalar inGU. Hence D=J C_D(t). Thus t^D=t^J; uniform conjugation has equal-sized fibers in each group, giving identical class laws. A deterministic pushforward gives identical inv(t t^g) laws, and independent samples give identical whole sequences. A uniform special-group element is NOT pointwise nearly uniform in the larger group; no such false comparison is needed.

At the large dimensions at issue L=SL(A)xSL(B) orSU(A)xSU(B) is perfect, lies inC_J(t), and has abelian quotient there. Thus L=L'<=C_J(t)'<=L, givingC_J(t)''=L; the same full-group centralizer target follows. Published DPSTheorem1.1 gives GLn>=700,kappa.0002 uniform marginal. Published GPRDTheorem1 gives GUn>=250,kappa.0001 nearly-uniform marginal, which includes uniform;Theorem2 gives GL/GU factor-product generation for a fixed strongt and independent nearly-uniform samples. Their proofs are invoked as published results, not entirely reaudited here.

No statement about the new Sp/O centralizer GENERATION follows from this marginal review alone. The separate192-class theorem, class-selection/subdirect bridge and any full new publication must pass independent review. The primary sources and own exact controls are supporting reproducibility artifacts; they are not replacements for this general written argument or a global novelty certificate.


## Concrete rejected alternatives

The discarded codimension-zero constraint has an explicit witness: q3,A=B=diag(1,1), f=X²+2X+2. This polynomial is squarefree, avoids0,-1 and has det(I+K) character+1 butdetK character-1. Its four self-adjoint operators onA cannot embedA_K into the same-discriminantB. Dropping the condition would falsely multiply by|O(B)|=8 and count32maps; exhaustive81map enumeration gives0 in this fiber. The actual proof retains it. Dropping the graph-discriminant condition already fails forq3,one-dimensionalA=B andF=1: K=1 gives graph form2, not the original form1. Dropping the adjoint full-class denominator or conditioning on a chart likewise changes the actual finite masses; the positive/nonzero finite fibers verify the full formula directly.

The equal-negative-dimensions lemma can be proved without forms: for conjugate involutionst,s withy=ts, t exchanges generalizedlambda andlambda^-1 spaces, which are therefore balanced fort whenlambda is not+/-1. On the+1 primary space, the odd-order unipotenty has an odd square root and conjugatest tos, so their negative dimensions agree. On the-1 primary space writey=-u; tu is conjugatet by an odd square root ofu, while s=-tu. Global conjugacy oft,s forces this primary space to have equal t-positive andnegative dimensions. Raisingy to half its order selects complete reciprocal pairs, and the-1 space only when the global two-part is2; every selected part is balanced fort. Thus dim(E_-(z)intersectE_+(t))=dim(E_-(z)intersectE_-(t)), even without semisimplicity. ForSp with target dimensions2a and4a, simultaneous strength forces the common dimension4a/3. It is impossible when3 does not dividea. This is a genuine obstruction, including arbitrarily large admissible dimensions, not a missing independent-marginals estimate. The two separate target constructions are the correct scope.

The exactly-half refinement would fail with a single primary factor: fixing the total discriminant already fixes that factor's sign, so the extra square-discriminant requirement retains all or none. The proof explicitly ensures at least two factors through its positive-degree remainder. The four-sector bound is also restricted tor>=8; empty smallq3sectors must not be interpreted as contradicting the large-degree theorem. The exact controls include those empty sectors and the validr8boundary.
