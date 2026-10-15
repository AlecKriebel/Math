# Source-first seal: independent exact reproduction family

UTC: 2026-10-15 04:22Z. This note was written before inspecting the candidate, author scripts, or old reviewer code/verdicts. Discovery completion estimate: 15%; audit completion estimate: 20%.

Source: Dmitry Fuchs (2021), DOI 10.1007/s40598-020-00170-8, local PDF SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d. Read directly: prose pp. 501–505 and 510–512, Definition 2.1, Figure 8 (visually), Figure 9 (visually), both image tables pp.504–505 (visually), Conjecture 2.6 and tables p.511 (visually), and the source's n=6 argument. Text extraction also read introductory scope and p.506 remarks. Source derivatives are private and excluded from publication.

## Independent model

Use angular units pi/n, M=n−2. At the initial vertex, a=n alpha/pi lies in [0,M]. At the terminal vertex the actual interior angle shown in Figure 8 is pi−beta, so b=n beta/pi lies in [2,n]. Beta is not the interior angle itself. Let N be the number of straight segments of the folded trajectory and r=N−1 the number of reflections. Source prose fixes b−a to be an even integer for N even, and b+a to be an even integer for N odd. Set s=+1 for N even and s=−1 for N odd, then d=(b−s a)/2 is integral. Definition 2.1 reduces, on the physically correct parity branch, to

    k = s(d−1) mod M.

The piecewise inequalities enforce the physically possible b interval and the representative of k. They are not substitutes for preserving the trajectory's branch/parity at special angles.

Direct-chord check: with source clockwise vertices X0,...,Xn−1 and horizontal X0Xn−1, the unreflected chord X0Xj has a=n−j−1, b=n−j+1. Its N=1 branch is s=−1, so d=n−j and k=j−1 mod M, exactly Figure 9. Both boundary edges j=1,n−1 give k=0. This check works for n=3,4,5,6 and all n≥3. Reversing physical orientation changes which reference side is used and must be tracked.

A source ambiguity is visible before any submitted material is read: at rational directions both b−a and b+a may be even integers. For example n=5, X0X2 has a=2,b=4: the literal first printed row gives A0 while the physically correct N=1/sum branch and Figure 9 give A1. A faithful implementation must retain N parity or an equivalent unfolding orientation; reading the four printed equalities as an unordered union is ambiguous. The odd printed first-row bound k≤m+1 is also suspicious but its extra cases have nonpositive a bound and do not affect positive-angle generic data.

Conjecture 2.6 concerns an existing parallel short trajectory with unwrapped real slope a'=ell+epsilon a in the actual initial sector [0,M], and predicts k'=epsilon k−ell mod M. For even n, ell must be even. Modulo pi direction equivalence alone must not silently admit an impossible vertex ray or forbidden odd ell. For generic a, there are M physical directions for even n, 2M for odd n; stabilizers can reduce counts at boundary/symmetric angles.

## First assessment and falsifiable checks

The local arithmetic reduction above classifies one trajectory; it does not prove a relation between distinct parallel trajectories. Any argument using only transformed endpoint labels must prove that the new labels refer to the actual first vertex hit under real side reflections. A large cone/cyclic germ construction may make this plausible but can conceal that central existence/identification step.

Independent checks will retain the physical terminal supplement, segment parity and actual reflections; compare diagonal types and n=3,4,6 anchors; and reject wrong epsilon, wrong ell shift, forbidden odd ell for even n, and degenerate/edge assumptions. All finite experiments, however large, remain finite evidence for the unbounded conjecture.
