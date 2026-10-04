# Turn1: reflection reduces the alternating antimorphic conjecture to Fine–Wilf

AI-assisted mathematical proof candidate; independent review pending. This proves the stronger alternating conclusion in the exact original source. Classical Fine–Wilf and the source definitions are credited; novelty is not certified.

## Theorem
Let theta be an antimorphic involution on A*. If a finite word w has alternating theta-periods p,q>0 and
|w|≥p+q−g, where g=gcd(p,q),
then g is an alternating theta-period of w. In particular it is a theta-period in the weaker imported sense.

## 1. Alphabet action and two-sided alternating extensions
An antimorphic involution is reversal composed with an involutive permutation sigma of the alphabet. To see this without assuming length preservation, theta is a bijective monoid antimorphism and fixes the empty word. Nonempty letters cannot map to the empty word. The image of a letter cannot be a product of two nonempty words: applying theta again would factor that letter into two nonempty words. Thus letters map to letters, sigma²=id, and antimorphism determines theta on every word.

For a seed u=u_0...u_(p−1), define a bi-infinite2p-periodic letter sequence s_u on the integers by the block u theta(u) at positions0,...,2p−1. It satisfies
s_u(−1−i)=sigma(s_u(i)) for every integer i.                 (1)
Proof: reduce i modulo2p. For0≤i<p, the reflected residue is2p−1−i, the corresponding letter of theta(u), namely sigma(u_i). For p≤i<2p the same assertion follows by applying sigma twice. This proves(1) for all residues and hence all integers.

If w is a prefix of (u theta(u))^omega and L=|w|, the segment of s_u indexed−L,...,L−1 is exactly
W=theta(w)w.                                                (2)
The right half is w; by(1) the left half in increasing order is sigma(w_(L−1))...sigma(w_0). Consequently W has ordinary period2p. This argument works even if L is not a multiple of p; no phase alignment at the left endpoint is assumed.

## 2. Apply classical Fine–Wilf to the doubled word
Apply(2) to both alternating representations of w. The SAME word W=theta(w)w has ordinary periods2p and2q. Its length is2L and
2L≥2p+2q−2g=2p+2q−gcd(2p,2q).
The classical finite-word Fine–Wilf theorem therefore gives ordinary period2g for W.

Index W by−L,...,L−1 as above. Its2g-periodicity means letters at any two positions in this interval congruent modulo2g agree: connect them by successive2g steps, all within the interval. The threshold ensures L≥max(p,q)≥g, so the complete central block indexed−g,...,g−1 is available.

## 3. Recover the alternating gcd representation
Let v=w_0...w_(g−1). For any right-half position0≤i<L, write r=i mod2g. If0≤r<g,2g-periodicity gives w_i=w_r=v_r. If g≤r<2g, compare i to the position r−2g in[−g,−1]. Equation(2) gives
w_i=W_(r−2g)=sigma(w_(2g−1−r)),
which is the letter at position r−g of theta(v). Thus every position of w agrees with the infinite repetition v theta(v)v theta(v)... . Hence g is an alternating theta-period, as asserted.

The case p=q is included (then L≥g and the conclusion is already a hypothesis); the indexing proof still works. The argument uses no surjectivity beyond the stated involution, no selected alphabet size, no letter fixed-point assumption, and no infinite limiting inference from a finite scan.

## 4. One sharpness witness and excluded generalizations
The bound cannot be uniformly lowered by one: take theta to be ordinary reversal, p=2,q=3, and w=abb of length3=p+q−gcd(p,q)−1. It is a prefix of (ab ba)^omega and of (abb bba)^omega, but does not have theta-period1 (all length1 blocks would be identical under reversal). This witnesses sharpness of the universal formula, not pointwise optimality for every numerical pair (divisibility cases are already trivial).

For a freely mixed theta-period, the reflected extension need not have ordinary period2p. For a morphic involution, its action does not reverse the prefix into the required left segment. These are why the proof is expressly limited to the original alternating ANTIMORPHIC setting. Related general pseudoperiodicity theorems retain their separate bounds.

## Status
Complete first-turn candidate, pending separate source/proof audit. The computational controls verify finite instances and the indexing identities; the theorem follows from the written reflection argument and classical Fine–Wilf, not from enumeration. No fifth-turn exhaustion, formal certification or research-priority claim.
