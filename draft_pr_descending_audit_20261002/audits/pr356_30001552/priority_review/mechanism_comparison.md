# Comparison lemmas and exact prior-theorem test

These are deductions made during the bounded priority audit after candidate release. They are neither attributed prior theorems nor novelty claims. They supply ways an equivalent earlier result could falsify the candidate's priority.

Let theta=sigma∘R, where R reverses words and sigma is an involutive permutation of letters. An antimorphic involution has this form (the candidate proves the structural fact).

## Parity untwisting

For a finite word w indexed from0 define T(w)_i=sigma^i(w_i). T is a length-preserving involution. For every p<=|w|, w is a prefix of (u theta(u))^omega, |u|=p, if and only if T(w) is a prefix of (v R(v))^omega, |v|=p.

Proof: extend the defining block repetition. Write r=i mod2p and v_j=sigma^j(u_j),0<=j<p. If r<p, sigma^i(u_r)=sigma^r(u_r)=v_r. If r>=p, the original letter is sigma(u_k), k=2p−1−r. The transformed letter is sigma^(i+1)(u_k). Since i+1−k is even, this equals sigma^k(u_k)=v_k, the corresponding letter of R(v). The converse follows by applying T again, since sigma²=identity. The same T acts on all p simultaneously.

Thus a prior exact ordinary-reversal alternating theorem at lengthp+q−g would imply the full antimorphic target at the same length. This argument introduces no alphabet restriction and includes fixed letters.

## Aligned two-letter encoding

For each fixed orbit {a}, use its own fresh symbolx and set phi(a)=xx. For each two-cycle {a,b}, use fresh symbolsx,y and set phi(a)=xy, phi(b)=yx. Different orbits use disjoint symbols. The uniform length2 code is injective and satisfies phi(theta(z))=R(phi(z)). Therefore alternating periodp of w is equivalent to alternating reversal period2p of phi(w). The reverse implication uses the aligned length2p prefix phi(w[0:p]) and code injectivity.

Consequently an exact reversal theorem would apply at encoded length2(p+q−g) and recover period2g, which decodes to g.

## Simpson3.4 substitution

The published Theorem3.4 on p.459 assumes length>=2h1+2h2−D, D=gcd(2(r2−r1),2h1,2h2), and concludes ordinary periodD. A reversal-alternating repetition has essential centers at−1/2+kp in zero-based coordinates (at1/2+kp in the paper's one-based coordinates); the shared phase permits common offsets modulo each half-period. Their difference is a multiple ofg, so D=2g, with h1=p,h2=q.

The paper also defines a palindromic periodicity only when the finite word contains at least a full doubled block (length>=2h), so at the conjectured short length the premise can already fail. Even when that premise holds, the theorem requires2p+2q−2g on T(w), whose length is still|w|. For phi(w), h1=2p,h2=2q and D=4g, so it requires4p+4q−4g while the conjecture supplies2|w|>=2p+2q−2g. Neither parameter match supplies the short theorem.

The candidate's whole-prefix reflection extension theta(w)w does supply length2|w| with periods2p,2q, allowing ordinary Fine–Wilf directly. Its proof obligation is precisely this shared extension and the recovery of alternatingg. Calling that an automatic application of the weaker original-word Simpson bound would conceal the extra deduction.

The separate, explicitly executed `comparison_check.py` checks both equivalences on every word of lengths 1–7 over a 3-letter alphabet with every involutive permutation, and checks the displayed numeric substitutions for p,q <= 50. Its complete saved stdout and pre-execution code/prose pins accompany the report. The default `verify_priority.py` checks that saved evidence and inventories without rerunning these loops. The finite controls supplement the algebra; they do not certify universal novelty or replace a proof.

