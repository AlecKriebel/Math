# Independent audit: counterexample to refined fixed-projection positivity

Date: 2026-10-20 UTC.

Audited `ATTEMPT_3.md`, SHA-256 `2ea79c46b06db0735052c6e946534b381d51828ab4cb57e6375925b0c01c1436`.

## Verdict

**PASS: the explicit polynomial is a counterexample to the precise assertion (P2) in Albert–Bousquet-Mélou, Section 6.3.1.** I independently checked the primary-source statement and independently enumerated the 54,810 relevant words, without using the attempt's formulas or its verification program to generate my counts.

The result does **not** disprove the unrefined (a+1)-positivity conjecture, does **not** disprove the quadrant-loop radius conjecture, and does **not** certify bibliographic novelty. The attempt states these limitations correctly.

## 1. Exact source interpretation

I inspected Section 6.3.1 (P2) in the locally available Albert–Bousquet-Mélou v3 primary-source extraction, together with its surrounding paragraph and the separate fixed-shuffle-class nonpositivity example in Section 6.3.2 (N2).

P2 fixes a vertical Dyck word v and asserts (a+1)-positivity of the length- and corner-count generating function of all quadrant loops whose vertical projection is v. It does not require summing over all vertical Dyck words of that length. It does sum over all possible horizontal Dyck projections at each length. Thus a negative coefficient in a+1 at any one fixed total length, after including all horizontal projections at that length, contradicts P2.

For v=N^13 S^13 and total length 30, horizontal length is exactly four. The complete list of nonnegative, returning horizontal projections is EEWW and EWEW. No other horizontal word is missing. Since both coordinate projections are Dyck paths, every shuffle of either projection with v stays in the nonnegative quadrant, and conversely every loop in this slice has exactly one of these horizontal projections.

Whether the source marks full length or half-length is immaterial here: the same polynomial occurs at full length 30 or half-length 15. The statistic is the original linear, ordered NW/ES count, with no cyclic seam.

Public source: Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, European Journal of Combinatorics 43 (2015), 131–164, Section 6.3.1 (P2). https://arxiv.org/abs/1312.4487v3 ; https://doi.org/10.1016/j.ejc.2014.08.024 .

## 2. Independent exhaustive integer enumeration

For each of H=EWEW and H=EEWW, I selected every four-element subset of the 30 positions, placed H in those positions and N^13 S^13 in the rest, and directly counted adjacent NW and ES pairs. I also checked the two projections, every quadrant prefix, final return, and distinctness of all resulting words.

Each projection produces exactly binom(30,4)=27,405 distinct words. My resulting histograms, indexed by corner counts zero, one, and two, are

    H=EWEW: [2744, 13650, 11011]
    H=EEWW: [11025, 13650, 2730]
    combined: [13769, 27300, 13741].

These are integer counts obtained directly from words, not by interpolation or floating-point computation. They give

    G(a)=13769+27300a+13741a^2.

Writing b=a+1 gives

    G(b-1)=210-182b+13741b^2.

The coefficient -182 is therefore a direct contradiction to P2. Checks at a=1 give 54,810 words, and at a=-1 give 210. Each individual shuffle class has value 105 at a=-1, consistent with the parity theorem. After completing this independent enumeration, I also ran `verify_attempt_3.py`; all of its reported tests passed.

## 3. Audit of the symbolic family

The two general formulas in Lemma 1 are correct. I checked the cited signed-count distribution directly against Kuszmaul, Theorem 2.16: it counts D=#NW-#ES, rather than C=#NW+#ES. Its use in the attempt respects that distinction.

For horizontal EEWW and vertical N^n S^n, both corner types cannot occur: NW followed chronologically by ES would force a W before a later E, while ES followed by NW would force an S before a later N. Thus C=|D| in that class.

For E1 W1 E2 W2, a word with both types must have the unique NW at W1 and the unique ES at E2. A second corner of either type is excluded by the N-before-S and horizontal projection orders. If these marked corners use N_j and S_k, respectively, E1 has exactly j possible preceding slots and W2 has exactly n-k+1 following slots. The interval between the corners is forced. Summing gives [n(n+1)/2]^2 mixed words. Replacing their absolute-signed weight 1 by their true weight a^2 proves the claimed correction term.

I checked the expanded coefficients and their transformation to b=a+1 algebraically. In particular the linear coefficient of the full fixed-vertical slice is

    -n(n+1)(n^2-11n-20)/6,

which is negative for every integer n>=13. The leading-degree formulas for fixed a are also correct. They prove negative entire fixed-shuffle classes for all -1<a<0 and negative fixed-vertical slices for -1<a<-3/5 once n is large enough. The examples -42 and -6919/100 agree with exact arithmetic.

## 4. Audit of the marked-corner convolution

The signed shuffle kernel follows from the signed-count distribution by setting the two binomial indices to u-k and d+k. Their sum is u+d, producing exactly the coefficient extraction stated in the attempt. For balanced loop projections it reduces to the positive binomial coefficient; for unbalanced interval projections it may be negative.

The chain formula is valid. Every marked NW or ES block consumes one horizontal and one vertical index, and marked blocks cannot overlap, so their selected indices form a strictly increasing chain in both coordinates. Conversely any admissible such chain, with independently chosen shuffles of the intervening intervals, reconstructs one marked word. No unmarked NW/ES corner can cross a marked block boundary: the block begins with an outward letter N/E and ends with an inward letter W/S. Hence the signs of the intervening shuffle intervals multiply without missing boundary factors.

The derivative identity is the k=1 specialization. It correctly identifies why the balanced a=-1 parity theorem does not yield nonnegative derivative contributions: the interval projections are generally unbalanced.

## 5. Scope controls

- This is stronger than the already known failure of positivity inside an individual shuffle class because both horizontal Dyck projections at the selected length are included.
- It remains weaker than a counterexample to unrefined positivity because the vertical projection is still fixed. Other vertical words can compensate its negative coefficient.
- Counts in this family grow polynomially with n when horizontal half-length is fixed at two. The counterexample alone provides no exponential-growth or radius contradiction.
- P2 is a subsidiary assertion in Section 6.3.1, not Conjecture 10 or Conjecture 11. Any publication or queue summary must keep that label and scope explicit.
- The source's reported finite verification ranges do not include this example; there is no claim that those reported checks were wrong.

No required correction was identified. 
