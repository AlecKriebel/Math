# A checked elementary variation of the July construction

This is this audit's deduction from previously published ingredients. It is **not** a claim that Di Matteo–Ferrara printed this counterexample, made this parameter change, or answered Colazzo's ideal-closure question explicitly. It is evidence about how much of the September result remains beyond the July paper.

## 1. General finite-factor calculation

Let Q be a finite left brace and let χ:(Q,∘)→C2 be a multiplicative group character. Put e(q)=(-1)^χ(q). On E=Z×Q use

(n,q)+(m,r)=(n+m,q+r),

(n,q)∘(m,r)=(n+e(q)m,q∘r).

These operations define the standard semidirect product of the trivial brace Z by Q. The circle operation is a group operation because e is a character; its integer coordinate associates by the exact coefficient identity e(q∘r)=e(q)e(r). Its lambda map is

λ_(n,q)(m,r)=(e(q)m,λ_q(r)),

an additive automorphism. Thus E is a left brace, and

(n,q)*(m,r)=((e(q)-1)m,q*r).

We claim that S(E)=Z×kerχ.

If χ(q)=1, the first integer coordinate of (n,q)*(m,0) is -2m. These star values are pairwise distinct as m ranges over Z. Equivalently Fix^r(n,q) is contained in {0}×Q, and the additive cosets represented by (m,0) are distinct. This is an infinite-index proof, independent of finite computation.

If χ(q)=0, the right star orbit is contained in {0}×Q and is finite. For any fixed (n,q), regardless of χ(q), the left star orbit lies in {0,-2n}×Q, hence is finite. Additive conjugacy is trivial because Q is a left brace of abelian type. For χ(q)=0, multiplicative conjugation is also finite: conjugation by (m,r) changes the integer coordinate of (n,q) to e(r)n and the finite coordinate to r∘q∘r^-1. Indeed the general conjugation formula is

(m,r)∘(n,q)∘(m,r)^-1=((1-e(q))m+e(r)n,r∘q∘r^-1).

Thus all four families are finite exactly when χ(q)=0. The orbit-index equivalence in the original property-(s) definition gives the claim; the specific fixed-subgroup indices below are also checked directly.

Consequently E's property-(s) set fails additive closure or lambda invariance whenever the multiplicative kernel kerχ does so in Q. It is a normal multiplicative subgroup, as the kernel of the induced multiplicative character E→C2.

This observation applies to **any** finite Q; the parameter change that introduces the infinite module is essential. With a finite trivial module, the entire resulting finite brace has property (s), so this conclusion cannot be read directly from a finite example without the new infinite extension and its orbit calculation.

## 2. The explicit July finite factor

Di Matteo–Ferrara, arXiv:2607.20222v1, Section 4.1, Lemmas 4.1–4.2 and displayed equations(1)–(4), give a left brace F on F2^4. Write q=(a,b,c,d), r=(u,v,w,z), all coordinates modulo 2, and define

p(q)=b+c+d+cd, q0(q)=c+bd, r0(q)=b+c+cd,

λ_q(r)=(u+zp(q),v+dw+zq0(q),w+zr0(q),z),

q∘r=q+λ_q(r), χ(q)=p(q).

The finite labels are a+2b+4c+8d. The displayed multiplicative kernel is

K={0,1,6,7,10,11,14,15}.

Addition is XOR on these labels, not integer addition. Thus 6 + 10=12∉K, and the printed calculation λ_8(6)=4∉K also shows failure of lambda invariance.

The source later uses the same character to act by inversion on a **finite C3** module over a restricted direct sum of F's. In this audit's variation, use one F and the **infinite trivial Z** module. Section 1 then proves S(E)=Z×K. For x=(0,6) and y=(0,10), the exact original-definition indices are

|E:Fix^r(x)|_+=2, |E:Fix^l(x)∩C_x^∘|_∘=2,

|E:Fix^r(y)|_+=4, |E:Fix^l(y)∩C_y^∘|_∘=8.

But x+y=(0,12) has e(12)=-1, so its right fixed subgroup has infinite additive index. Moreover λ_(0,8)(x)=(0,4)∉S(E). This is an equivalent negative answer to the source question, using a larger finite factor than PR156.

The verifier reconstructs F and χ independently; it checks all finite triples, the exact integer associativity coefficients, subgroup closures and the reported index calculations. There are25,632 checks in each of normal and optimized execution, using raised errors rather than assertions. The universal integer-coset proof above is the certificate for infinity.

## 3. What this does and does not establish about priority

The negative answer is obtainable by a short, independently checked variation of explicit July data. This demonstrates a close derivative relation and defeats any assessment that ignores Section 4 merely because Section 5 discusses a differently worded question. It does **not** authenticate a pre-September document asserting this negative answer, supplying Z×F, or claiming the variant as a result. The infinite-module selection and S(E) computation are deductions made here.

PR156's Z×Z4 brace is not isomorphic to E: its additive torsion subgroup has order 4, whereas E's additive torsion subgroup has order 16. The July paper therefore does not contain the exact same brace in a disguised coordinate system through this route. PR156 uses the older four-element brace from Colazzo–Ferrara–Trombetti Example 3.8 and a nonadditive multiplicative sign character; that choice and its direct index proof may be a distinct explicit example/observation, but no new semidirect construction or finite-conjugacy characterization should be credited to it.

The correct finding is a substantial **originality/credit concern with a checkable derivative construction**, not proof of an already-published explicit solution. Historical priority and the significance of the new observation remain separate judgments.
