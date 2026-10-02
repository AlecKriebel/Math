# Turn 2: finite-window gluing and an all-length bounded-tau theorem

Original conjecture remains unresolved. This turn proves, computer-assisted, the original implication for **all finite alphabets, all morphic involutions, all word lengths, whenever tau_theta(w)<=7**. Its restriction is tau, not word length. The proof consists of an all-parameter gluing reduction and a complete finite enumeration, both described below.

## 1. Signed Fine–Wilf lemma, with proof

If a word has negative periods p and q and length at least p+q, it has negative period g=gcd(p,q). This is the morphic alternating assertion of the original report's Theorem22; the following is a direct proof, so this turn does not depend on an unexamined proof of that assertion.

First take length S=p+q. On positions0,...,S−1, join each i to i+p modulo S. The join has difference p without wraparound and difference q with wraparound. The endpoint letters are therefore theta-images in either case. Each residue class modulo g forms a cycle of length s=S/g, because gcd(p/g,s)=1.

If s is odd, traversing this negative-edge cycle yields a=theta(a); all letters on that cycle are fixed and equal. Adjacent positions in this residue class, separated by g, are thus theta-images.

If s is even, p/g and q/g are both odd. Each cycle edge reverses parity of the scaled index (the index within its residue class). Transport along edges therefore assigns opposite theta-powers to positions whose scaled indices differ by1. Positions at distance g are theta-images again. This proves the desired shift on the S-letter word.

For a longer word, apply the S-letter statement to every contiguous S-letter window. Every pair at distance g is contained in one such window, so the conclusion is global. Fixed letters are allowed throughout. A word0011 under binary swap has negative periods2 and3 but not1; its length4=p+q−g shows why the usual smaller ordinary Fine–Wilf threshold cannot simply be substituted.

## 2. Period extension and gluing

**Extension lemma.** Suppose X has negative period p and a suffix Z of length at least p+g has negative period g. Then X has negative period g. To check any pair i,i+g in X, translate both positions forward by the same multiple jp of p until the first enters Z. If it was outside Z, its first entry lies within the first p positions of Z; hence both translated positions lie in Z. If it was already inside Z, use j=0. Iterating the negative-p relation multiplies both letters by theta^j. Since the translated pair satisfies the negative-g relation and theta commutes with its own powers, the original pair does too. The prefix version follows by translating backward.

**Gluing lemma.** Suppose X is a prefix and Y a suffix of their union word, they have negative periods p,q, and their overlap Z has length at least p+q. The signed Fine–Wilf lemma gives g=gcd(p,q) on Z. Since |Z|>=p+g and |Z|>=q+g, extension gives negative period g on both X and Y. Every distance-g pair in the union is contained in at least one of them, because their overlap has length at least g. Thus the union has negative period g.

This lemma needs no identity assumption and no bound on the alphabet.

## 3. Reduction to one finite window length

For a positive integer t, define B_t as follows:

    Every word x of length 3t with tau_theta(x)<=t has a negative period <=t.

If B_t holds, then **every** word w of length n>=3t with tau_theta(w)<=t has a negative period <=t. Start with its first3t letters. For each next letter, glue the existing prefix (negative period p<=t) to the last3t-letter window (negative period q<=t). The overlap has length3t−1>=2t>=p+q. The gluing lemma provides a new negative period gcd(p,q)<=t. Induction reaches the whole word.

Consequently, verifying B_t proves the original conjecture for every word with actual tau exactly t: the resulting period is <=t, while Turn1's universal inequality gives period>=tau=t. Verifying B_1,...,B_7 suffices for the all-length assertion claimed here. It does not verify B_t for larger t.

More generally, the same argument works with any tested window length L>=2t+1, but this turn uses L=3t, precisely matching the source threshold.

## 4. Finite alphabet reduction without an external dependency

Suppose a letter belongs to a theta-orbit that first appears at position j (zero-based). The prefix ending there is theta-unbordered: a nonempty theta-border of length k would require its prefix's last letter, at position k−1<j, to equal theta(w[j]), which lies in that previously absent orbit. This is impossible.

Therefore, in any word with tau<=t, every new theta-orbit first appears within the first t positions. There are at most t occurring orbits and at most2t letters in their theta-closed support. This strengthens the alphabet bound from Turn1 and does not use the ordinary Ehrenfeucht–Silberger theorem. It does not imply that the orbit word is periodic; that separate claim still has Turn1's credited dependency.

## 5. Complete canonical enumeration

The standard-library program finite_window.py generates one representative of every finite word with its appearing-orbit involution structure, modulo equivariant renaming and interchange of the two letters within each two-cycle.

A new orbit is numbered by order of first appearance. Its first symbol has code2j. At creation it is either fixed (theta(2j)=2j) or paired (theta(2j)=2j+1 and conversely). For each existing orbit the recursion allows its fixed symbol, or both paired symbols. A new orbit is allowed only before position t; the previous lemma proves that this restriction loses no accepted word. The unused odd code of a fixed orbit is never generated.

After appending one symbol, all newly completed suffixes longer than t are tested for a nonempty proper theta-border by literal symbol comparisons. If any such suffix is unbordered, the branch is discarded. Previously completed factors were already tested. Thus accepted prefixes are exactly the canonical words with tau<=t. At length3t the program exhaustively checks every p=1,...,3t and asserts that the least negative period is <=t.

This is an exhaustive, uncapped finite tree. No random sampling, timeout inference, external solver, or guessed state invariant is involved. The numbers of terminal representatives are:

    t:       1   2   3    4     5     6      7
    leaves:  2   8  37  199  1196  8026  59814

All tests pass. TURN_2_ENUMERATION.json gives exact counts at every depth, nonperiodic-prefix counts, and SHA256 of the complete canonical terminal stream. Each line in that hashed stream is compact JSON [orbit_type_boolean_list,word_integer_list], followed by newline, in the deterministic traversal order. The full stream need not be stored.

## 6. Replay, cross-controls, and limits

Run:

    python finite_window.py --max-t 7 > /tmp/windows.json
    cmp TURN_2_ENUMERATION.json /tmp/windows.json
    python verify_turn2.py

The separate checker verifies signed graph consequences for all1<=p,q<=30 at two lengths, literal gluing on short binary words, and Cartesian-product controls under specified explicit alphabets. Those controls are supplemental; the all-alphabet bounded-tau theorem uses the proved canonical completeness and the full finite-window replay.

The original conjecture for arbitrary tau is still open in this packet. No finite assertion count establishes the infinite family B_t. No new priority claim is made for the signed Fine–Wilf lemma, which is already stated in the original report.
