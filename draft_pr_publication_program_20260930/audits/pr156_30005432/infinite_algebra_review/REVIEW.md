# Independent adversarial review of the infinite algebra

**Mathematical gate: PASS for the supplied property-(s) definition.** No blocking defect was found in the counterexample or its optional mathematical calculations. A reproducible, nonblocking defect was found in the submitted computational verification: its assertions disappear under Python optimization. Independent replacement controls address that defect. Literature priority, novelty, and the fidelity of surrounding source quotations are not cleared by this review.

Candidate: PR 156, `AlecKriebel/Math`, immutable submission HEAD `aec31742f3f26c5b1e533404da57539d17dc94a1`, attempt `30005432`. Review completed 2026-10-12 05:51:19 UTC. Best-guess completion of the assigned mathematical audit: 100%; this is not a percentage of novelty or publication readiness.

## Scope, independence, and falsifiable claim

The exact claim reviewed is that in an arbitrary skew left brace the set of elements satisfying the two supplied finite-index conditions need not be an ideal. The supplied definitions are

\[
a*b=-a+a\circ b-b,\quad
\operatorname{Fix}^r(x)=\{b:x*b=0\},\quad
\operatorname{Fix}^l(x)=\{b:b*x=0\},
\]

with indices in the **additive** group for the right fixed/centralizer intersection and in the **multiplicative** group for the left fixed/centralizer intersection. The construction must be valid over all integers; its fixed-set denominators must be subgroups; the witness must have finite indices; its additive double must have a provably infinite index. Failure of additive closure then suffices to disprove every standard ideal claim that requires an additive subgroup.

The original `COUNTEREXAMPLE.md` and `source_record.json` were read first. An independent derivation was recorded and byte-hashed in `INITIAL_ASSESSMENT.md` before the original verifier and source reconciliation were read. No original/historical review or sibling mathematical findings were read. This is independent validation of a supplied construction, not independent discovery of that construction. No external communication, Git mutation, PR action, release, or publication action was performed.

## Universal construction and brace proof

Let \(C=\mathbb Z/4\mathbb Z\), \(D(c,d)=c+d+2cd\pmod4\), and \(e(0)=e(1)=1\), \(e(2)=e(3)=-1\). Use canonical representatives only when evaluating the sign; the definition is periodic modulo four.

Write \(c=u+2v\), \(d=r+2s\) for bits \(u,v,r,s\). Since \(u+r=(u\mathbin\oplus r)+2ur\),

\[
D(c,d)=(u\mathbin\oplus r)+2(v\mathbin\oplus s)\pmod4.
\]

Thus \((C,D)\cong C_2\times C_2\), with identity 0, every element self-inverse, and \(D\) commutative. Both \(e(c)=(-1)^v\) and \(h(c)=(-1)^u=1+2c\pmod4\) are multiplicative characters for **D**, not for the additive \(C_4\) operation.

On \(B=\mathbb Z\times C\) define coordinatewise addition and

\[
(n,c)\circ(m,d)=(n+e(c)m,D(c,d)).
\]

The two associations of a triple have integer coordinate
\(n+e(c)m+e(c)e(d)k\), because \(e(D(c,d))=e(c)e(d)\), and their component coordinates agree by associativity of \(D\). This proves associativity universally in \(n,m,k\in\mathbb Z\). The identity is \((0,0)\), and the inverse is \((-e(c)n,c)\): both products with that inverse have integer coordinate zero and component \(D(c,c)=0\). The additive structure is plainly an abelian group.

Direct calculation, using the additive inverse, gives

\[
\lambda_{(n,c)}(m,d)=- (n,c)+(n,c)\circ(m,d)
=(e(c)m,(1+2c)d)=(e(c)m,(-1)^c d),
\]

where the second coordinate is modulo four. It is an additive automorphism, since both factors are signs. Consequently \(a\circ(b+t)=a+\lambda_a(b+t)=(a\circ b)-a+(a\circ t)\). This is the left brace law for all inputs. The character calculations also directly establish \(\lambda_{a\circ b}=\lambda_a\lambda_b\). No finite-quotient inference is used here.

The star formula is therefore exactly

\[
(n,c)*(m,d)=((e(c)-1)m,2cd\pmod4).
\tag{1}
\]

An optional transparent identification is \((B,\circ)\cong D_\infty\times C_2\): \((1,0)\) is the infinite translation, \((0,2)\) an involution reversing it, and \((0,1)\) a central involution. The proof above does not rely on that identification.

## Exact witness and infinite index

Put \(x=(0,1)\). Equation (1) gives \(x*(m,d)=(m,d)*x=(0,2d)\). Both fixed sets are \(H=\mathbb Z\times\{0,2\}\). Addition is abelian, so its additive centralizer is all of \(B\). Also \(x\circ(m,d)=(m,D(1,d))=(m,d)\circ x\), so its multiplicative centralizer is all of \(B\).

The additive parity map \((m,d)\mapsto d\pmod2\) is a surjective homomorphism with kernel \(H\). The same map is a surjective circle homomorphism, since \(D(c,d)\equiv c+d\pmod2\), and has the same kernel. Thus \(H\) is a subgroup in each relevant group, and the two indices for \(x\) are **exactly 2 and 2**.

Its **additive** double is \(y=x+x=(0,2)\), distinct from its circle square \(x\circ x=(0,0)\). Equation (1) gives \(y*(m,d)=(-2m,0)\). The torsion-free property of \(\mathbb Z\) implies that its right fixed subgroup is exactly \(\{0\}\times C\). Its additive index is infinite: for any integers \(j,k\),

\[
(j,0)-(k,0)\in\{0\}\times C\iff j=k.
\]

Hence the cosets represented by \((j,0)\), \(j\in\mathbb Z\), are pairwise distinct. In this additive abelian group the quotient is indeed a group isomorphic to \(\mathbb Z\). This explicit injection of \(\mathbb Z\) into the coset space, not a bounded count, is the infinite-index certificate. Therefore \(x\) has property (s) and \(x+x\) does not, and the claimed ideal closure is false.

## Complete intersections, legitimate indices, and optional claims

For \(z=(n,c)\), \(g=(m,d)\), addition is abelian and the multiplicative centralizer equation is

\[
g\circ z=z\circ g\iff(1-e(c))m=(1-e(d))n.
\]

The two denominators are exactly

\[
H_z=\{(m,d):(e(c)-1)m=0,\ 2cd=0\pmod4\},
\]
\[
K_z=\{(m,d):(e(c)-1)m=0,\ (e(d)-1)n=0,\ 2cd=0\pmod4\}.
\tag{2}
\]

For \(K_z\), start with \(\operatorname{Fix}^l(z)\), which supplies the last two conditions; the centralizer then supplies the first. Confusing the raw left fixed set with this intersection would be a substantive error, but the submitted finite-index calculations make the distinction correctly.

| c | n | H_z | K_z | additive index | circle index |
|---|---|---|---|---:|---:|
| 0 | 0 | B | B | 1 | 1 |
| 0 | nonzero | B | Z x {0,1} | 1 | 2 |
| 1 | 0 | Z x {0,2} | Z x {0,2} | 2 | 2 |
| 1 | nonzero | Z x {0,2} | Z x {0} | 2 | 4 |
| 2 | 0 | {0} x C | {0} x C | infinite | infinite |
| 2 | nonzero | {0} x C | {0} x {0,1} | infinite | infinite |
| 3 | 0 | {0} x {0,2} | {0} x {0,2} | infinite | infinite |
| 3 | nonzero | {0} x {0,2} | {(0,0)} | infinite | infinite |

All displayed H_z are additive subgroups. All K_z are circle subgroups: their component sets are Klein-group subgroups, and their integer coordinate is either unrestricted or zero; both conditions are stable under the group law and inverse. For unrestricted integer coordinates the subgroups are full preimages under the circle projection \(\pi:B\to(C,D)\), giving the exact finite component index. When the integer coordinate is forced to zero, the circle cosets represented by \((j,0)\) are distinct, since \((j,0)^{-1}_\circ\circ(k,0)=(k-j,0)\). The latter argument uses a coset space; it does not assert normality or a quotient **group** for those finite circle subgroups.

Consequently \(S=\mathbb Z\times\{0,1\}\) exactly. It is a normal circle subgroup, as the preimage of a subgroup of the abelian Klein quotient, but is not an additive subgroup. Moreover \(\lambda_x(x)=(0,3)\notin S\), so lambda invariance also fails. Right distributivity fails at \(u=v=x\), \(w=(1,0)\): \((u+v)\circ w=(-1,2)\), whereas \((u\circ w)-w+(v\circ w)=(1,2)\). Thus no two-sided-brace conclusion is contradicted by this example.

The source-reconciliation **formulas**, independently checked after the first assessment, are also correct. Namely \(\ker\lambda=\mathbb Z\times\{0\}\), and the global fixed set of all lambdas is \(\{0\}\times\{0,2\}\). Their intersection is zero, giving the stated annihilator under that convention (the additive centralizer condition adds nothing). The star-generated additive subgroup is \(B^{(2)}=2\mathbb Z\times\{0,2\}\): all products lie there, while \((0,2)*(1,0)=(-2,0)\) and \(x*x=(0,2)\) generate it. The additive generators \(r=(1,0),x\) generate the whole additive group, while their circle subgroup is only \(S\). Every \(b=(n,0)\) gives \(b*r=b*x=r*b=x*b=0\), although \(\lambda_{(0,2)}(b)=(-n,0)\). Thus values at these additive generators do not certify global lambda-fixedness or membership in the trivial annihilator. This review does not authenticate a published lemma's standing hypotheses or judge a broader published theorem; those require the separate source gate.

## Exact controls and falsification results

`independent_verify.py` uses explicit raised failures, with no reliance on Python assertions. Its coefficient vectors compute both sides of identities in three independent integer variables; each equality is universal over Z because the coordinate laws are affine linear. The finite component is exhausted. The written torsion-free and distinct-coset arguments supply the infinitude certificate. Numerical controls evaluate the actual infinite operations without clipping or reducing integers.

`python3 run_controls.py` produced `RUN_RECEIPT.json` and raw stdout/stderr records. The independent verifier passes **33,516 checks in each of normal and -O modes**, with identical category coverage. Supplemental triple controls use integer coordinates -2 through 2; pair controls include 0, signs, and integers as large as 10^100. All eight subgroup/index cases are checked. These numerical bounds are fully recorded and do not substitute for the universal proof.

Four independent defective variants are rejected with nonzero exit status in **each** mode:

1. Changing e(3) to +1 destroys the character: formal associativity fails at component triple (1,2,0), with opposite coefficients for the third integer variable.
2. Omitting the 2cd component term also destroys formal associativity, at (1,1,0).
3. Replacing the star integer argument m by n contradicts the universal star formula at (c,d)=(2,0).
4. Claiming right distributivity is rejected by the explicit (-1,2) versus (1,2) witness.

Finite quotients with integer moduli 2,3,4,5,7,8,11 give y's right index q/gcd(q,2); every element has property (s) in each finite quotient. At q=2 the sign multiplier -2 kills even m=1. This boundary control specifically shows why finite quotient enumeration cannot certify the infinite claim.

**Nonblocking issue: optimized original verifier.** The submitted `ck` is `assert b,g; C[g]+=1`. Its normal and optimized runs both print 33,512 reported checks, but -O eliminates every assertion. An in-memory replay changing e(3) to +1 is rejected normally, yet under -O it exits successfully and prints `PASS_EXACT_COUNTEREXAMPLE_CONTROLS` with 33,512 reported checks. This is captured in `original_noncharacter_epsilon_*` records. It means the original optimized receipt is not evidence of checking. It does not falsify the actual construction or the original normal run. Replace assertions with explicit exception checks if the submitted verifier is to certify optimized runs.

## Result and exact remaining boundary

The strongest verified result is the valid infinite left brace with x of indices (2,2), additive 2x of infinite additive index, and exact S=Z x {0,1}. No mathematical gap remains for that counterexample under the supplied definition. Optional mathematical formulas also pass. Novelty, priority, source interpretation, and publication readiness remain unassessed here. Byte-level input identity and all owned outputs are recorded in `IO_BYTEHASH_MANIFEST.json`; `SEAL.json` records its hash and the main document hashes. Regenerating controls changes timestamped receipts and requires resealing.
