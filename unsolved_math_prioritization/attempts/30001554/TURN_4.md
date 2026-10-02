# Turn 4: saturation at twice the least alternating period

Original conjecture unresolved. This turn proves a second all-alphabet theorem, independent of the finite enumeration:

> If p is the least alternating theta-period of a nonempty word w and |w|>=2p−1, then tau_theta(w)=p.

It also gives an explicit unbordered-factor witness and sharp structural restrictions on any remaining counterexample. The argument is a theta adaptation of the classical least-rotation method mentioned for ordinary words in the original report. No priority claim is made.

## 1. A primitive least rotation is ordinary unbordered

Let R be the lexicographically least cyclic rotation of a primitive word, using any total order on its finite alphabet. All nontrivial rotations are distinct, so R is strictly less than each. Suppose R had a nonempty proper border v. Write R=v s=t v; the words s,t have the same length. The two rotations s v and v t are nontrivial, so

    v s = R < v t  implies s<t,
    t v = R < s v  implies t<s.

This contradiction proves R ordinary unbordered. No compatibility of the alphabet order with theta is needed.

## 2. The periodic completion has only two possibilities

Put u=w[0:p] and complete it to the two-sided periodic word W=(u theta(u))^infinity. The componentwise negative-p relation ensures that w is a prefix of W. W has negative period p. It cannot have a smaller positive negative period, because that would restrict to the same smaller alternating period on w.

If every letter of u is fixed by theta, u is ordinary primitive: a shorter power root would give a smaller negative period of W and w. Here u is the primitive ordinary period block, of length p.

Otherwise, U=u theta(u) is ordinary primitive, of length2p. Indeed, if it had a shorter power root of length d dividing2p, then d<=p. Reduce the negative shift p modulo d. If the residue r is positive, W has negative period r<d<=p, a contradiction. If r=0, shifting p acts as the identity on letters of W, while it also acts as theta; then every letter is fixed, contrary to this case. Thus U is primitive.

The reduction modulo d is valid on the two-sided periodic completion: positions congruent modulo d carry equal letters, so W[i+r]=W[i+p]=theta(W[i]) for every integer i. The fixed-letter case also covers involutions with fixed points outside the support without assumptions about them.

## 3. Construct an unbordered p-letter factor

In the fixed-support case, take the least cyclic rotation R of u. It is ordinary unbordered by Section1, hence theta-unbordered. Its start lies at some phase0<=j<p.

In the nonfixed case, take the least rotation R of U. It is ordinary unbordered and, because W has negative period p, has form

    R=v theta(v),  |v|=p.

If v had a theta-border a of length k>0, its suffix would be theta(a). Then theta(v) would have suffix a, while v has prefix a. Hence R would have the nonempty proper ordinary border a, contradicting its unborderedness. So v is theta-unbordered.

The start phase i of R is between0 and2p−1. If i>=p, replace it by j=i−p; the corresponding p-letter factor is theta(v), which is also theta-unbordered. Otherwise set j=i. Thus in either case a theta-unbordered p-letter factor starts at some0<=j<p in W.

The hypothesis |w|>=2p−1 ensures j+p<=2p−1<=|w|, so this factor lies inside the actual finite word w. Therefore tau_theta(w)>=p. Turn1's opposite inequality tau_theta(w)<=p gives equality.

This is constructive: form the block u or u theta(u), choose its least rotation, reduce its phase modulo p, and extract the p-letter factor. A naive quadratic comparison of rotations suffices; no linear-time implementation claim is needed.

## 4. Consequences for the remaining source conjecture

If tau=t<p, the theorem's contrapositive yields

    n <= 2p−2,  so p >= ceil((n+2)/2).                (4.1)

The word itself cannot be theta-unbordered, for that would give t=n=p. Its longest theta-border has length n−p, by the exact period/border equivalence. Formula(4.1) shows that every theta-border has length at most(n−2)/2. Thus **all theta-borders of any genuine gap word are strictly nonoverlapping**, with at least two middle positions left over.

In particular, any counterexample to the original n>=3t implication must satisfy

    p >= ceil((3t+2)/2),

in addition to t>=8 by Turn2. Turn1's orbit-period reduction and Turn2's first-orbit restriction still apply. These simultaneous restrictions do not yet force p=t.

The finite-window gluing result has a useful minimal-counterexample consequence. If any original counterexample exists, choose one with the least possible tau=t. If it is longer than3t and every3t-letter factor had negative period<=t, gluing would give that period bound globally, a contradiction. Hence some3t-letter factor has period>t and tau<=t. If its tau were smaller than t, it would itself be a source counterexample, violating minimality. Therefore a least-tau counterexample may be chosen with exactly

    n=3t, tau=t, ceil((3t+2)/2)<=p<=3t−1.

The last upper bound uses the fact that this word is theta-bordered. This is a reduction of a hypothetical minimal counterexample, not a proof that none exists.

## 5. Controls and limits

verify_turn4.py exhausts the same four explicit alphabet ranges as Turn1. On every applicable instance it checks the completion's claimed primitivity, the least rotation's ordinary unborderedness, the actual finite-word witness, and the saturation equality. Every gap word is checked against(4.1) and the nonoverlapping-border consequence. There are12,266 assertions.

The theorem and minimal-counterexample reduction are valid for arbitrary finite alphabets and morphic involutions. The proof does not apply to antimorphic involutions or arbitrary block-choice theta-periods. It does not replace the required relationship between n and tau with a relationship only involving the unknown least period p. The original conjecture remains unresolved.
