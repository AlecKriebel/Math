# Source-first priority baseline: PR356 / problem30001552 / OWR-4425-007

This baseline was derived exclusively from the original Oberwolfach report before candidate or previous priority material was inspected. The complete contribution by Dirk Nowotka, joint work with Bastian Bischoff, printed pages 2219–2222 (PDF pages 25–28), including its references, was read. The official EMS PDF was also opened independently online. The report is No.37/2010, DOI 10.4171/OWR/2010/37, Mini-Workshop: Combinatorics on Words, meeting August 22–28, 2010. The contribution characterizes the material as work in progress.

## Exact mathematical target, reconstructed from the source

Let A be an alphabet, A* its free monoid, theta:A*→A* an involution (theta(theta(w))=w). A morphic involution satisfies theta(uv)=theta(u)theta(v); an antimorphic involution satisfies theta(uv)=theta(v)theta(u).

An ordinary period p of w means that w is a prefix of u^omega for some u of length p. A theta-period p means that w is a prefix of an infinite concatenation of blocks in {u,theta(u)}, with |u|=p; the choice of either block at each step is unrestricted. An alternating theta-period p means that w is a prefix of (u theta(u))^omega for some u with |u|=p; its first block is u. Write Pi_theta^alt(w) for these alternating periods.

The unnumbered conjecture immediately following Theorem23, printed page2220, is the following sufficient-bound claim:

For every antimorphic involution theta and finite word w, if p,q are positive integers in Pi_theta^alt(w) and |w|≥p+q−gcd(p,q), then gcd(p,q) belongs to Pi_theta^alt(w).

Theorem23 in that source already states the identical conclusion under the stronger hypothesis |w|≥p+q. Thus the proposed improvement is the reduction of the sufficient overlap threshold by gcd(p,q). Its threshold is the same expression as the ordinary Fine–Wilf theorem. The source does not provide a proof of Theorem23 or of the conjecture in this contribution.

## Adjacent claims and exclusions

* Theorem20 cites Fine–Wilf (1965) for ordinary periods: n≥p+q−gcd(p,q) implies an ordinary gcd-period.
* Theorem21 cites Czeizler–Kari–Seki (2010) for general, non-alternating antimorphic theta-periods, with p>q and n≥2p+q−gcd(p,q), concluding a common theta-primitive root of the prefixes of lengths p and q. This is not the alternating target and not the same threshold/conclusion.
* Theorem22 gives the Fine–Wilf threshold for non-alternating morphic theta-periods, and n≥p+q for alternating morphic theta-periods. Morphic and antimorphic cases must not be merged.
* The weak-theta-period substitution statement (Theorem19) concerns letterwise choices and ordinary periods after substitution; it is not the blockwise alternating target.
* Conjecture27 on page2222 is a distinct, numbered assertion about morphic involutions, theta-unbordered factors, and n≥3 tau_theta(w). It is not this unnumbered conjecture.
* The local theta-period discussion, CFT, and theta-unbordered example are surrounding research context, not assumptions of the target.

## Success criteria and boundary cases

Priority audit success means independently checking whether earlier public primary sources prove this exact alternating-antimorphic sufficient bound, a stronger statement implying it, or the exact proof mechanism under equivalent definitions. Search hits, titles, and abstracts are leads, not inspected proofs. Classical inputs must receive credit; proving an old sufficient implication anew does not itself establish novelty. Preserve chronology/version uncertainty and accessible-full-text gaps.

The source's discussion of bounds being tight and the new bound being the actual bound creates a separate sharpness question. A proof of the displayed implication settles its sufficient-bound component; it does not prove universal or parameterwise optimality. Fixed-letter involutions/reversal must not be silently excluded; fixed-point-free Watson–Crick complements are only a special case. Test equality n=p+q−gcd(p,q), p=q (then n≥p and the conclusion is immediate), divisibility, unequal periods, and the distinction between a period length and the block word. The threshold ensures n≥max(p,q), so both period witnesses are actual full prefixes. No additional p>q or coprimality restriction occurs in the target.

The exact remaining gap at this gate is the entire candidate comparison and bounded priority search. Neither correctness nor novelty is assumed.
