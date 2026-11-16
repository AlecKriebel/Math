# Row141 paper-first independent scope reconstruction

This reconstruction follows personal complete reading of the actual3PDF pages, all229 actual controlling TeX lines, and3fresh own individual rasters. It precedes supplied scientific code/results/archived scientific opinions/current peer or root findings/new foreign bodies. General background includes elementary word combinatorics, Euclidean gcd and prior unrelated review work; no record141 scientific opinion has been read. The target is a hypothesis and the manuscript's bounded literature-audit assertions are not treated as evidence.

## Exact target, assumptions and success criteria

A is an arbitrary alphabet, A* the finite-word free monoid, theta an antimorphic involution (theta(xy)=theta(y)theta(x),theta^2=id). A positive integer p is an *alternating* theta-period of w if w is a prefix of (u theta(u))^omega for some length-p word u. The same applies to q; no minimality is required. Put L=|w| and d=gcd(p,q). The theorem claims that L>=p+q-d forces w to be a prefix of (v theta(v))^omega for its own length-d prefix v. It also claims that the formula cannot uniformly be reduced by one, with a specific reversal/two-letter p2,q3,L3 witness. The original scope includes fixed letters, equal periods, divisibility, arbitrary alphabets and terminal incomplete blocks. It does not assert pair-by-pair optimality, fixed-point-free optimality, a theorem for morphic involutions or arbitrary mixed u/theta(u) block sequences, minimal periods, or global novelty.

Success requires an actual universal deduction at that full scope, correct common finite extension and central phase, a genuine counterexample to the uniformly lower formula, and exact actual primary definition/question/credit interfaces. A finite search cannot prove universality; old automated reviews cannot substitute for an independent proof. Any substantive defect must be documented rather than silently replacing the statement by a weaker one.

## Family1: involution on the free monoid must act letterwise in reverse order

Theta(epsilon)=theta(epsilon)^2 forces the image of the empty word to be empty by finite length. Bijectivity follows from theta^2=id; a nonempty word cannot map to epsilon. If a letter's image factored into two nonempty words, applying theta would factor that letter into two nonempty images, impossible in a free monoid. Hence theta permutes letters involutively and reverses their order. This proof works without finite-alphabet assumptions. Falsifier: erasing or letter-to-long-word transformations would break the coordinate model, but are excluded by involutivity and the free-monoid structure. No external theorem is needed for this lemma.

## Family2: distinguish exact alternating hypotheses from ordinary/generalized periods

The alternation fixes the phase at the beginning: u,theta(u),u,theta(u),... . It is stronger than permitting any concatenation of u and theta(u). For reversal and u=ab, the word abab belongs to u*u* but is not a prefix of abbaabba... . Therefore any source-conjecture identification must check the actual alternating definition, not infer it from the phrase theta-period. Ordinary period2p follows from an alternating p-period; the reverse implication alone does not hold without reflection symmetry. Falsifier: an arbitrary 2d-periodic word can fail the desired d-alternating phase.

## Family3: the length arithmetic fixes all prefixes used in the argument

Since d<=min(p,q), p+q-d>=max(p,q)>=d>0. Under the theorem's hypothesis both p- and q-blocks are fully determined by the observed word; v of lengthd exists. No invisible letters or choices are necessary to identify those roots. Empty words and periods longer than L can satisfy vacuous short-prefix definitions, but never the positive threshold here. Equality p=q gives d=p and thresholdp; divisibility gives d equal the smaller already-assumed period. Those are legitimate theorem cases and need no strict inequalities.

## Family4: a common finite reflected extension, not equality of unseen completions

Index w on[0,L-1] and define W on[-L,L-1] by W_i=w_i for i>=0 and W_i=sigma(w_(-1-i)) for i<0. This is exactly theta(w)w and depends only on w. For a p-alternating prefix, its formal residue labelling on Z/(2p) has label u_r for r<p and sigma(u_(2p-1-r)) for r>=p. This labelling satisfies s_(-1-i)=sigma(s_i), hence restricts to W and gives ordinary period2p on that same finite interval. Repeat independently for q to obtain period2q on the same W. Falsifier: reflecting only separate base blocks or asserting the two infinite completions agree beyond the observed interval would not establish the claim. This proof needs neither of those assumptions.

## Family5: ordinary gcd propagation and an independent self-contained route

The doubled word has length2L and periods2p,2q, while 2L>=2p+2q-2d and gcd(2p,2q)=2d. The standard finite-word Fine–Wilf interface is therefore applicable if its precise hypotheses are as stated. Independently, a Euclidean induction can prove the needed ordinary period lemma: for 0<h<k and length N>=h+k-gcd(h,k), the prefix of length N-h inherits periods h and k-h because for i<N-k, x_i=x_(i+k)=x_(i+k-h). Its length meets the reduced threshold. Induct on h+k, then use h being a multiple of d to extend the last h letters. The nontrivial boundary is N>=2h when k>h; this follows from k-h>=d. I will complete this induction explicitly in separate actual own-result work before any code/foreign exposure. Falsifier: using k-h on the full word without discarding h terminal letters would generally be invalid.

## Family6: recover the alternating *phase*, not merely ordinary period2d

W's central interval[-d,d-1] is theta(v)v. This is not itself the block to repeat starting at coordinate0: the positive first d letters are v, and the next d must be theta(v). For index i>=0, reduce modulo2d to r. Choose representative r if r<d and r-2d otherwise. Both are in W; chains of 2d steps remain within the interval. Consequently w_i=v_r for r<d and sigma(v_(2d-1-r)) for r>=d. This is exactly the desired phase. Falsifier: using a reflection centre at0 rather than the gap between-1 and0, or repeating theta(v)v from0, would reverse/shift the conclusion incorrectly.

## Family7: exact below-threshold obstruction and its limited strength

For theta=reversal, w=abb over distinct a,b, p2 uses u=ab and utheta(u)=abba; q3 uses u=abb. Thus both alternating periods hold at L3=2+3-1-1. A period1 alternating root under reversal repeats the first letter a forever, contradicting b. This proves only failure of the globally reduced formula. It neither establishes exact thresholds for every pair nor needs the input periods to be minimal. A defect in those details would invalidate the optimality wording even if the sufficient theorem survived.

## Family8: involution and alphabet boundaries

Fixed letters are allowed. For pure reversal, d1-alternation means a constant word; for a swapped pair under reverse-complement, it means ababab..., not a constant word. An argument forcing sigma(a)=a would improperly narrow the theorem. A one-letter alphabet has only fixed-letter behaviour. An empty alphabet has no positive-length root, so the positive-period hypotheses are impossible. For an infinite alphabet only finitely many letters occur in w; no finiteness of A is used. Non-involutive antimorphisms and morphic involutions lie outside the exact hypothesis.

## Family9: truncation, equal/dividing periods and rescaling boundaries

L can end anywhere inside either source block and need not be a multiple of p,q,2p,2q or2d. The reflected interval argument uses only observed coordinates and handles this directly. p=q is tautologically covered. If p divides q, d=p is already one of the given periods, so the formula is sufficient without claiming necessity. The minimal threshold formula always ensures L>=d, so selecting v is well-defined. Falsifier: adding a terminal-block-completeness assumption or silently requiring relatively prime p,q would change the theorem.

## Family10: precise external source interfaces still unverified

The original Fine–Wilf finite-word theorem must be checked at its ordinary-period length and gcd conventions. Nowotka's OWR37/2010 contribution, joint with Bischoff, must actually contain the unnumbered conjecture after Theorem23 on printed2220, with the alternating premise/conclusion used here, distinct from numbered Conjecture27; the workshop2010 versus publication2011 distinction must remain. Bischoff's institutional thesis Lemma3.9/Satz3.11 must have the claimed reflection/doubled-period mechanism and longer p+q bound, with its exact antimorphism assumptions. These are critical credit/target interfaces, not assumed true from the target bibliography.

## Family11: comparison/novelty statements are separate from validity

The claimed Czeizler–Kari–Seki theorems25/26/28 and corollary32 concern a different block-power/primitive-root interface; the exact 2010 journal version must be read separately from MFCS2008 numbering. Kari–Seki's claimed improved bound2p+q-d-floor(d/2) has range p>q>=2d and author/publisher access limits. Simpson's published theorem3.4 uses reflection offsets and D=gcd(2(r2-r1),2h1,2h2), length2h1+2h2-D, conclusion ordinary periodD. Exact source bodies and their full hypotheses are needed before accepting any comparison. Even correct comparisons and a historical record of53 searches do not certify first discovery or continuing openness. I will preserve that audit as history, not use its judgment as proof. A true theorem may be classical or an immediate application; novelty is not assumed.

## Family12: edition, rights, custody and exposure honesty

The source packet is immutable128 ordinary files/18dirs,125payloads plus3exact root terminals,69regular ZIP occurrences, nativeZIPthenPDF. Native version is present string1.0; native publication3Oct2026, created4OctUTC. Personal reading now finds printed3October2026 and no printed version line, but those new observations must never rewrite source-only historical null/unread/currentSheet-unobserved fields. The actual archive's rights/asset-specific license text has not yet been read; no broad code-license assumption is imported from other papers. Full source/native typed objects, headers/key/list order, null/absence/custom history and original assets will remain unchanged byreference. Core is qualified17 originals plus sole405b checkpoint helper bound to0f285e35 receipt, not18 original unchanged; generated caches have no immutable claim. No source/scientific helper or supplied programme is executed. The first actual metadata/Poppler preparation exited0 and exact streams were retained. No new foreign body, native support/code/result, archived scientific opinion or current peer/root findings have yet been read. Root141 stays CLOSED.

## Strongest paper-first status and next falsifiable gate

The manuscript's elementary construction and phase argument appear internally coherent at the exact full scope, and the uniform obstruction is checkable directly. This initial statement is not a final verdict: precise primary question/comparison interfaces, actual own completed Euclidean proof/control results, and bounded static support/licensing/custody inspection remain. Next I will finish and separately freeze the universal induction and actual hand-worked controls before native scientific support or new foreign exposure. Only afterward may minimal primary acquisition occur, preferring exact-edition existing raw bodies byreference. No follow-up direction or publication authority is claimed; default followup null.
