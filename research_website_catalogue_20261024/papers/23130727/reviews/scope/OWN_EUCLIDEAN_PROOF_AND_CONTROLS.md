# Independent universal proof and actual hand-worked controls

This body is written after INITIALfdc72cc3 and before supplied scientific support/code/results, archived scientific opinion, current peer/root findings, or new foreign scientific bodies. No scientific programme is run. The mechanism is a self-contained Euclidean overlap induction followed by an equivariant finite quotient at the central reflection. It does not enumerate native signed constraints or borrow another review's output.

## 1. Ordinary period lemma proved here, with its terminal boundary

Claim: for positive integers h,k, d=gcd(h,k), if a finite word x has ordinary periods h,k and length N>=h+k-d, it has ordinary period d. An ordinary period t means x_i=x_(i+t) whenever 0<=i<i+t<N; t need not be minimal.

Induct on h+k. Reorder so h<=k. If h=k, d=h and the conclusion is already a hypothesis. Otherwise k>h, and k-h is a positive multiple of d, hence k-h>=d. In particular N>=h+k-d>=2h. Let y be the prefix of length N-h. It inherits ordinary period h. For each index i such that i+(k-h)<N-h, equivalently i<N-k, both steps below occur in x:

    x_i = x_(i+k) = x_(i+k-h).

The first equality uses period k; the second uses period h in reverse. Therefore y has period k-h. Its length N-h>=k-d=h+(k-h)-d and gcd(h,k-h)=d. The sum of its two period parameters is k<h+k, so induction gives d as a period of y.

This is not yet enough unless the discarded suffix is recovered. Every j with N-h<=j<N has j-h in[0,N-h-1], because N>=2h. Period h gives x_j=y_(j-h). As h is a multiple of d, j and j-h have the same residue mod d. The prefix has length at least h>=d, and its d-periodicity makes all letters in each residue class agree by a finite chain. Hence every suffix letter has the same residue-class label as the prefix, and x has period d. No step assumes that k-h is a period of the full word. This completes a universal induction for all finite words, including noncoprime/equal/dividing periods and arbitrary alphabets.

Thus the exact ordinary Fine–Wilf interface needed below is independently proved here. Actual classical primary reading remains required for attribution and the manuscript's historical comparisons, not to fill an unsupported mathematical step in this derivation.

## 2. Direct finite reflection labels

An antimorphic involution theta necessarily is reverse followed by an involutive letter permutation sigma, by the free-monoid argument in INITIAL Family1. Let w have length L and alternating period p, with L>=p. Its length-p root u is the observed prefix. Define f_p on residues r mod2p by

    f_p(r)=u_r                          if 0<=r<p,
    f_p(r)=sigma(u_(2p-1-r))            if p<=r<2p.

Two facts are immediate and can be checked separately in the two residue ranges:

    f_p(-1-i)=sigma(f_p(i)),
    w_i=f_p(i)                         for 0<=i<L.

Define a finite word W on[-L,L-1] by W_i=w_i for nonnegative i, and W_i=sigma(w_(-1-i)) for negative i. For negative i, the displayed involution identity identifies W_i with f_p(i); for positive i this is the alternating hypothesis. Thus W is a restriction of a single residue labelling mod2p and has ordinary period2p. This argument constructs no equality between the p- and q-labellings beyond the finite interval. For q it gives the same actual W=theta(w)w, hence W has ordinary periods2p and2q.

## 3. Uniform gcd reduction and central equivariance

Let p,q>0,d=gcd(p,q), and assume L>=p+q-d. This ensures L>=max(p,q)>=d. The word W has length2L>=2p+2q-2d. Applying the *proved* ordinary lemma with h=2p,k=2q gives ordinary period2d on W. Consequently W has a well-defined label on each residue class mod2d represented in its interval: successive shifts by2d remain inside that interval and preserve the label.

Let v=w_0...w_(d-1). Its positive representatives0,...,d-1 give labels v_r. The negative representatives-d,...,-1 give labels sigma(v_(-1-j)). For the residue r with d<=r<2d, take j=r-2d; its label is sigma(v_(2d-1-r)). Therefore for every observed i>=0, r=i mod2d gives exactly

    w_i = v_r                           for r<d,
    w_i = sigma(v_(2d-1-r))             for r>=d.

That is the prefix of (v theta(v))^omega, at the original phase. No symmetry/palindrome is imposed on v and no letter is forced to be sigma-fixed. The reflection is across the gap between-1 and0; shifting that centre would be an incorrect proof. This proves the full original sufficient theorem independently of any native finite outputs or external classification.

## 4. Twelve actual hand-worked controls

1. Equal periods: theta=reverse, p=q=2,w=abba,L4,d2. Both source blocks ab/ba give the same hypothesis, and the theorem returns the same root ab. It does not assert a smaller or minimal period. Even L2 with w=ab meets the equal-period threshold2 and is valid as a short prefix.

2. Divisibility/noncoprime parameters: theta=reverse,p2,q4,w=abbaabba,L8,d2. For p2 the repeated block is abba; for q4 the root abba is its own reverse and gives the same infinite word. Threshold2+4-2=4 is met and output root ab is correct. Noncoprimeness is neither excluded nor replaced by an n=1 case.

3. Exact uniform failure one below the threshold: theta=reverse,p2,q3,w=abb. Root ab gives prefix abb of abba..., root abb is the entire q-prefix. L3=2+3-1-1. A d1 root would be a and produce aaa..., failing at position1. On the doubled word W=bbaabb, period4 holds (the only two comparisons are b=b,b=b); period6 is vacuous; period2 fails at positions0 and2. Its length6 is below the ordinary4+6-2=8 threshold. This independently checks both the claimed obstruction and why the doubled ordinary lemma cannot be applied prematurely.

4. Equality at the p2,q3 threshold under reversal: w=aaaa,L4. It is a prefix of (aa aa)^omega and (aaa aaa)^omega, and the gcd1 conclusion repeats a. This is a positive threshold case, not evidence that only this finite case proves the theorem.

5. Nontrivial swapped involution: on{0,1}, sigma(0)=1,sigma(1)=0 and theta=reverse-complement. Take w=0101,p2,q3,L4. For p2, u=01 and theta(u)=01; for q3,u=010 and theta(u)=101. Both yield the prefix0101 and d1 root0 yields (01)^omega. The conclusion is alternating01, not a constant word. This rejects a proof that silently assumes fixed letters.

6. Central phase control: theta=reverse,w=abba,d2. W=abbaabba indexed[-4,3]. Its central interval[-2,1] spells baab=theta(ab)ab, while its positive prefix from0 is abba=ab theta(ab). Repeating baab from0 would be wrong. The signed residue representative r-2d recovers the correct phase.

7. Incomplete terminal block: theta=reverse,p2,q4,w=abbaabb,L7,d2. The same two source completions as case2 give the prefix, which ends inside the final block. The gcd completion is abbaabba..., whose first7 letters are exactly w. No divisibility of L by any period was used.

8. Fixed-letter/one-letter alphabet: A={a},theta=reverse. Every word a^L has every positive alternating period, and the theorem is valid whenever the threshold is met. The uniform two-letter obstruction does not claim sharpness on this singleton alphabet.

9. Arbitrary block mixing is genuinely different: theta=reverse,w=abab,p2. The word is a prefix of a concatenation ab|ab, but its first four letters differ from the only phase-fixed p2 completion ab|ba. It fails the alternating p2 premise; it must not be counted as a target counterexample or accepted by a definition checker.

10. Ordinary doubled period alone is insufficient: theta=reverse,w=abab has ordinary period2, but it has no alternating period1, since its first-letter root a would force aaaa. Here theta(w)w=babaabab fails ordinary period2 across the centre, at positions2 and4. The missing common centred extension is exactly what prevents a false implication.

11. Euclidean induction with a nontrivial gcd: x=abababab,N8,h4,k6,d2. The prefix length N-h=4 is abab with periods4 and2 and meets4+2-2=4. The last4 letters shift back by h4 and retain their mod2 labels. This checks the reduced-word length and suffix-recovery arithmetic at equality.

12. Euclidean boundary with minimal h: x=aaaaa,N5,h1,k5,d1. The prefix has length4, periods1 and4, and threshold1+4-1=4; the final a shifts back by1. Separately h=k=5,N5 can have arbitrary root abcde and already has period5; the induction must terminate rather than claim a smaller ordinary period.

These are actual symbolic/hand-worked controls, not a recorded computational run. They deliberately include positive, negative, definitional and off-by-one boundary evidence across different mechanisms. They corroborate the universal derivation, which carries the unbounded quantifiers.

## 5. Frozen evidence limit

At this freeze the full sufficient theorem and the globally unreducible-by-one assertion are established by the self-contained proof and explicit example. No foreign primary body, scientific programme, supplied finite output, archived opinion, or current peer/root finding has been read. Actual original conjecture wording, historical comparison hypotheses, edition/licensing differences and bounded native static inspection remain to be checked; no global novelty/firstness is certified. Those are still independent gates, so this is not a final disposition. Followup remains null, publication authority false, root141 CLOSED.
