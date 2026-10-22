# Fresh reconstruction of all mathematical claims

Review 02, 17 October 2026 UTC. These deductions were reconstructed from the displayed operations, not from a prior PASS judgment. The operative note and frozen original full proof were both read in full. Supplemental historical acceptance language is not a premise.

## Exact target and primary definition

The official OWR51/2019 PDF was freshly retrieved and physical page 22 (printed 3228) rendered and visually read. Problem 9 asks about a **finite, nontrivial, simple left brace**, with **metabelian multiplicative group and abelian Sylow subgroups**, and specifically a presentation by **two trivial** left braces. All these conditions are retained; no classification, minimum order or historical-first assertion is needed.

The full admissible asymmetric-product law was independently compared with arXiv:2001.08905v1, Theorem 2.2 and arXiv:1705.08493v1, Theorem 3.1. The original definition permits a normalized symmetric 2-cocycle. The note's reduction does not quietly assume bilinearity.

## Ingredients and all-input brace law

In the commutative ring ideal R=xF5[x]/(x5), products of five positive-degree terms vanish. The coefficients of log(1+r) through degree four reduce modulo five because their denominators, and those of exp through degree four, are units. Formal inverse and product identities may be substituted into this ideal: a discarded total-degree-five monomial in the formal variables becomes zero. Hence L and E are inverse on R and L(r+u+ru)=L(r)+L(u). This does not use a characteristic-zero infinite series or a coefficient 1/5.

Reflection sigma(x)=-x commutes with L. Its x4 coefficient eta is therefore invariant, and eta is a circle homomorphism. Expansion gives eta=a4-a1*a3-3*a2^2+a1^2*a2-4*a1^4 modulo five, independently rechecked for all 625 coefficient tuples in the fresh checker.

The binary space V has dimension four. For even-weight vectors, dividing the integer weight identity by two yields Q(v+w)=Q(v)+Q(w)+beta(v,w). If v is orthogonal to every e_i+e_j, all its coordinates agree. The all-one vector has odd weight, so the restricted form has zero radical. Cyclic rotation preserves weight and dot products. Its fixed vectors are constant, and its fixed space inside V is zero; thus M-id is bijective. There is a nonfixed vector, so M has exact order five.

For arbitrary a=(r,v,z), b=(u,w,Z), let L(r)=(k1,k2,k3,s), e=z+Q(v), and use corresponding h,t,f for b. The proposed output has log-coordinate k+tau^e h and final coefficient s+t. Polarization and rotation invariance give e(a circle b)=e+f. Its V coordinate is v+M^s w. Thus the stated bijection Psi sends **every** proposed product to the direct product of ordinary semidirect-product laws. Its inverse uses E and z=e+Q(v). This proves associativity, identity and inverses universally, rather than inferring them from checks on generators.

Subtracting a componentwise gives lambda_a(u,w,Z)=((1+r)sigma^e u, M^s w, Z+beta(v,M^s w)). The first block is linear over F5 and invertible because 1+r is a unit. The binary block is linear over F2; invert M^s and recover Z from its triangular last coordinate. These are additive automorphisms. Together with the already proved group law, this proves the left-brace identity on all triples. The fact Q and eta need not be additive as functions of the parameter a is harmless: linearity is in the input acted upon.

The additive group is C5^4 x C2^5. The order is 5^4*2^5=20,000. On the additive 5-part, star is exactly ring multiplication, so the brace is nontrivial and (x*x)*x=x3 is nonzero.

## All group hypotheses and all ideals

For K=F5^3, the image of tau-id is the span of coordinates one and three, of order 25. For V the image of M-id is all 16 vectors. In the displayed direct product group, the derived subgroup is therefore C5^2 x C2^4, order 400, abelian. Both actions are nonidentity. This is a nonabelian metabelian group, not a nilpotent group. The exhibited Sylow 5 and 2 subgroups have orders 625 and 32 and are abelian; every other Sylow subgroup is conjugate to one of them. No claim of normal Sylow subgroups is used.

If I is an ideal and i is known in I, then lambda_g(i)-i is in I by lambda invariance. The inference i*g in I also holds: multiplicative normality and the additive/lambda conditions give a quotient brace, where i=0 and lambda_0=id. This second inference is not available for an arbitrary left ideal. It is exactly the stronger inference needed in the proof.

For any nonzero mixed seed with r nonzero, sixfold addition gives (r,0,0). (The original full proof instead uses (2r,0,0), also valid because 2 is invertible modulo five.) If c*x^j is the lowest nonzero term, multiplication by x^(4-j) via a lambda difference gives c*x4 when j<4; higher terms vanish and j=4 needs no difference. Additive scaling gives a=x4. For a nonzero binary seed, either it is the scalar b=(0,0,1), or nondegeneracy supplies a shear with beta(w,v)=1 that yields b.

The ideal-normality inference gives b*x=3x and a*(0,w,0)=(0,(M-id)w,0). Thus a or b yields both, every pure V vector, and x. Subsequent lambda_x differences yield x2,x3,x4. These four ring vectors, four V basis vectors and b additively generate all B. Every possible nonzero ideal is covered; no assumption that ideals are coordinate subspaces or vector subspaces is made.

## Full universal obstruction and boundary cases

For general normalized symmetric cocycle b, the inverse/subtraction identity is (t,s)-(u,v)=(t-u,s-v-b(t-u,u)). It follows directly that lambda_(t,s)(u,v)=(alpha_s u,v-b(alpha_s u,t)). Since (t,0) circle (u,0)=(t+u,0), evaluate lambda composition on (w,0): b(w,t+u)=b(w,t)+b(w,u). Symmetry yields additivity in the first argument too. This deduction only assumes that the operations form a brace.

For finite abelian factor groups, a mixed-primary b-value is killed by relatively prime powers and is zero. Values on T_p x T_p are killed by a p-power and lie in S_p. Thus P=T_p x S_p is an additive subgroup of order equal to the full p-part. It need not have split additive law: the valid T=S=C2, b(t,u)=tu example has addition C4. The set also forms a multiplicative p-subgroup of the same order since alpha preserves primary groups, hence is a multiplicative Sylow subgroup.

If that Sylow subgroup is abelian, commuting (t,0) and (0,s) forces alpha_s(t)=t for t in T_p and s in S_p. Subtraction now gives a*b0=(0,-b(u,t)). Such an element acts trivially by lambda on P, so (a*b0)*c=0 for all a,b0,c in P. There is no odd-prime or split-exponent assumption here. Zero factors and primes absent from one factor cause no exception. The lemma does not require simplicity or metabelianity.

Brace isomorphisms preserve additive element orders and both star operations. Thus a primary triple witness obstructs **every** isomorphic asymmetric presentation with two trivial factors, even with different factor groups and coordinates. This proves the claimed full negative answer.

The abelian-Sylow hypothesis is essential: the supplied order-eight control is a genuine brace from two trivial factors, with a nonabelian multiplicative 2-group and nonzero triples. Nonzero star squares alone do not suffice: the order-25 control has nonzero squares and zero triples. A nonbilinear symmetric coboundary can satisfy the cocycle identity while failing lambda composition; that is a valid negative control, not an excluded admissible presentation. The four unchanged programs actually exercise these boundaries.

## Redundant claims of the original full proof

Global lambda-fixedness of (u,w,Z) first gives r*u=0 for every r, so u is a multiple of x4. The a=x4 action forces w fixed by M, hence w=0. Conversely these (c*x4,0,Z) are globally fixed: reflection preserves x4 and multiplication by r kills it. Hence |Fix|=10.

The full lambda kernel is zero. Binary action forces s=0 and v=0 by M's order and beta's radical. If z=1 the diagonal coefficient of x is -1 instead of +1, so the ring block cannot be the identity. If z=0 then r annihilates R, giving r=c*x4; eta(r)=c=0 now forces r=0. Addition is abelian, so Soc(B)=0.

The center of K semidirect C2 consists of the fixed middle K coordinate; the V semidirect C5 factor has trivial center. Thus Z(G)={(E(c*x2),0,0)} has order five, including E(x2)=x2+3*x4. The fresh checker verifies this witness commutes with every one of the 20,000 elements, independently of Psi.

For a simple nontrivial two-trivial-factor product, rad(b) x {0} is a proper ideal, so rad(b)=0. With H generated by alpha_s(t)-t, the set H x S is an ideal (equivalently the kernel of the multiplicative and additive projection to T/H), hence H=T. The derived subgroup is therefore T x {0}, while Fix={0} x S. They are multiplicative complements, so |Fix| equals the abelianization order. Here the latter order is 20,000/400=50, different from ten. Also {0} x ker(alpha) is a proper ideal, so alpha is faithful. A central (t,s) must have alpha_s=id, hence s=0, and t fixed by all alpha. Invariance of b then yields b(t,alpha_u(v)-v)=0. These differences generate T, so t is in rad(b) and is zero. Thus that simple two-trivial-factor class is centerless; B is not. This is not a claim that all simple braces are centerless.

Finally reflection by k=(0,0,1) sends E(2x) to E(-2x). Under the stated commutator convention [k,h]=k circle h circle k^-1 circle h^-1, h=E(2x) gives d=E(-4x)=E(x)=x+3x2+x3+4x4. Then d*x=x2+3x3+x4 and x*(d*x)=x3+3x4, nonzero. Thus the original derived-star fixedness witness and its orientation are correct. For any two-trivial-factor product with rad(b)=0 and H=T, a derived element (t,0) has star image (0,-b(u,t)), in Fix; the advertised redundant condition follows.

## Software evidence and exact limit

The mathematical arguments above are all-input arguments. Matching finite output is not a replacement for them. The source programs were read, including the factored ring/binary checks, ideal transcript generator and consumer, explicit guard calls, mutation controls, generic cocycle tests and symbolic quotient-ring arithmetic. None uses removable Python assert statements. Their imported modules are standard-library facilities; no operative network access or imported historical mathematical module is required.

The fresh checker `check_seed_certificates.py` uses its own unital coefficient convolution, bit-coordinate rotation and explicitly expanded eta. It regenerates all 19,999 deterministic transcript commitments, checks every row and route in order, independently consumes all 259,858 inference records, checks all five complete sample transcripts and requires all nine generators. It imports no published checker code. Tampering with arithmetic, references, seed identity or a necessary endpoint is rejected. It separately rechecks the nonzero triple, central witness and two associativity-breaking mutations. Its initial final-line-deletion control removed an already-known x4 and was valid; strengthening it to remove the missing x3 generator gives the intended negative test. This is honestly recorded as a test-design correction in the research log.

Strongest verified mathematical result: the full negative answer with every stated group and brace hypothesis, together with the redundant invariants. Remaining mathematical gap found in these proofs: none. Finite tests do not constitute proof-assistant certification, an exhaustive 20,000-cubed evaluation, or a theorem about all cocycles without the written argument.
