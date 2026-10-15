# Independent uniform separation derivation

This proof was derived from the claim alone, before reading any proposed author proof, author verifier, review, sibling finding or priority source. It establishes the mathematical claim, subject to ROOT's independent adjudication. It does not adjudicate the unread candidate or novelty.

Let F0=0,F1=F2=1 and F_(j+1)=F_j+F_(j-1). Fix n>=3, q=F_n and p=F_(n-1). The proposed points have latitude parameter t=k/q, radius2sqrt[t(1-t)], height1-2t and longitude2pi p k/q. Their squared norm is4t(1-t)+(1-2t)^2=1. Every coordinate is real for0<=k<q.

## 1. Fibonacci identities with signs

The consecutive denominator vectors u_j=(F_j,F_(j-1)) and u_(j+1)=(F_(j+1),F_j), for j>=2, have determinant

C_j=F_j^2-F_(j-1)F_(j+1)=(-1)^(j-1).

Indeed C2=-1, and the recurrence gives C_(j+1)=-C_j. They therefore form an integer unimodular basis of Z^2. Consecutive Fibonacci numbers are coprime by the Euclidean recurrence gcd(F_n,F_(n-1))=gcd(F_(n-1),F_(n-2)), terminating at gcd(1,1)=1.

For the fixed rational rotation, define E_j=pF_j-qF_(j-1). Then

E_j=(-1)^(j-1)F_(n-j), for2<=j<=n,

including E_n=0. To check the starting signs, E2=p-q=-F_(n-2), and E3=2p-q=F_(n-3). The sequence E_j satisfies the Fibonacci recurrence, and the signed backward Fibonacci expression does too through j=n, proving the identity inductively. Thus neighboring errors have opposite signs before the terminal zero; the final case must not be described as two strictly nonzero opposite errors.

The addition identity, for j>=2 and h>=0, is

F_(j+h)=F_j F_(h+1)+F_(j-1)F_h.

For fixed j the right side satisfies the Fibonacci recurrence in h and equals F_j,F_(j+1) at h0,1. Also F_(h+1)<=2F_h for h>=1 and F_(j-1)<=F_j for j>=2.

## 2. Uniform best-approximation bound by an integer basis

Take ANY integer1<=m<q and ANY integer a. Choose j uniquely with F_j<=m<F_(j+1), using j>=2 to avoid the duplicate denominator1. Because m<F_n, this j lies between2 and n-1. Let A=F_(n-j)>0 and B=F_(n-j-1)>=0. Unimodularity supplies integers S,T with

(m,a)=S(F_j,F_(j-1))+T(F_(j+1),F_j).

Its exact error is

p m-q a=(-1)^(j-1)(S A-T B).

We claim |S A-T B|>=A. The sign/range proof exhausts every case:

- If S=0, m=T F_(j+1), contradicting0<m<F_(j+1).
- If S,T are both positive, m>=F_(j+1); if both negative, m<0. The same exclusions apply to both nonnegative/nonpositive coefficients when the preceding S=0 case and T=0 case are treated separately.
- If T=0, then m=S F_j>0 forces S>=1, so the error magnitude is S A>=A.
- In the remaining case S and T have opposite signs, |S A-T B|=|S|A+|T|B>=A, since |S|>=1 and B>=0.

In particular B=0 at j=n-1 causes no gap: the bound still follows from |S|>=1. Therefore

|p m-q a|>=F_(n-j).

Using h=n-j>=1 in the addition identity gives

q=F_j F_(h+1)+F_(j-1)F_h<=3F_j F_h<=3m|p m-q a|.

This proves, uniformly for EVERY1<=m<q and EVERY integer a,

**m|p m-q a|>=q/3.**

No continued-fraction theorem, irrational approximation replacement, integer-form nonvanishing, restricted small-gap assumption or finite enumeration is a premise. It is the elementary integer-basis best-approximation mechanism. The constant1/3 is sharp for q3,p2,m1,a1; sharpness of this coarse arithmetic inequality is not required for the geometric result.

Choose a nearest integer to p m/q and let r=p m-aq. Then0<|r|<=q/2 by coprimality and m<q. If q is even, either sign at the half-residue tie is allowed; the angular cosine and absolute sine are identical. The bound above applies to either choice.

## 3. The exact all-pair geometric reduction

For arbitrary indices0<=k<l<q set t=k/q,s=l/q,m=l-k,d=s-t=m/q and v=t+s-2ts. Let c=cos(2pi p m/q)=cos(2pi r/q). Expansion of the Euclidean squared chord gives

||z_l-z_k||^2/4 = t+s-2ts-2c sqrt[t(1-t)s(1-s)]

= **H=v-c sqrt(v^2-d^2)**,

since v^2-d^2=4t(1-t)s(1-s). Moreover v-d=2t(1-s)>=0, so v>=d>0 and w=sqrt(v^2-d^2) is real.

If c<=0, H>=v>=d=m/q>=1/q.

If c>0, note H=v-cw>=v-w>0. The identity

(v-cw)^2-d^2(1-c^2)=(w-cv)^2>=0

therefore yields H>=d sqrt(1-c^2)=d|sin(2pi r/q)|. Because r is nonzero and nearest, c>0 implies0<|r|<q/4. Concavity of sine on[0,pi/2] gives sin x>=2x/pi there, hence

|sin(2pi r/q)|>=4|r|/q.

The arithmetic lemma now gives

H>=4m|r|/q^2>=4/(3q)>1/q.

These two cases cover every pair, every Fibonacci index, and every angular sign. In particular no assertion that the fixed-gap latitude minimum is equatorial or polar is used. Such an assertion is generally false: for a continuous latitude gap d1/10 and c4/5, the allowable value v1/6 has w2/15 and H3/50, below both the pole value1/10 and central value109/1000. The present inequality is valid for all allowable v.

## 4. Attainment and full equality check

The point z0 is the north pole. Its squared chord to z1 is4/q by direct substitution (equivalently H=s=1/q), irrespective of longitude. Together with the uniform lower bound, the minimum chord is exactly2/sqrt(q).

The positive-cosine case is strict. In the other case equality H=1/q forces m=1 and v=d. Since0<=t<s<1, v-d=2t(1-s)=0 forces t=0, hence k0,l1. Thus the unordered pair(0,1) is the only equality pair, including the q2 boundary. This uniqueness is a consequence of the proof; the requested claim only needs attainment.

## 5. Quadratic-form hazard and finite controls

The identity p^2+pq-q^2=(-1)^n follows from the same Cassini recurrence. Consequently r^2-(-1)^n m^2 is divisible by q, but the quotient can vanish. Already n4,q3,p2,m1,r=-1 has quotient0; n6,q8,p5,m2,r2 does too. A blanket assertion that the form is nonzero would be false. Neither integrality nor nonvanishing is used in the proof above.

The independently written arithmetic_controls.py checks exact signed errors, determinant signs, addition, all nearest residues for n3..26, terminal zero neighbors, extra nonnearest a values and the product inequality. It also deliberately rejects reversed Cassini parity, an unsigned-nearest-residue misuse and the false nonvanishing premise.

The separately written interval_controls.py uses only rational arithmetic. Machin's identity pi=16atan(1/5)-4atan(1/239) is justified by tan(2atan(1/5))=5/12, tan(4atan(1/5))=120/119 and tan(4atan(1/5)-atan(1/239))=1 with the angle in(0,pi/2), hence pi/4. Alternating arctangent partial sums with the first omitted term give exact outward bounds; outward rounding preserves them. Cosine is bounded by its even Taylor polynomial through degree48 and the Lagrange remainder obtained from degree49, whose coefficient is zero: the error is at most x^50/50!, since all derivatives of cosine have absolute value at most1. Term-by-term interval evaluation and outward dyadic rounding remain conservative. Square-root endpoints are exact integer-square-root rounding with squared endpoints checked against the rational radicand. Interval products include all endpoint sign combinations.

Those intervals certify all16588 unordered pairs for q2,3,5,8,13,21,34,55,89,144, with exact pole equality and strictly positive lower margins at every other pair. They also certify a counterexample to a FALSE general-angle extension: q13,p1,k6,l7 has H<62850259439/10^12<1/13. That rotation is coprime but not the prescribed Fibonacci p8; it is not a counterexample to the target.

The finite controls are corroboration and meaningful negative tests. The uniform claim is proved by Sections1–4, not extrapolated from their ranges. No priority conclusion, author-candidate assessment, general packing optimality or shifted/irrational-angle assertion follows.
