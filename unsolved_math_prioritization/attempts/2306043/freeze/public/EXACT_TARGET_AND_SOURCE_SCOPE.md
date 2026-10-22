# Exact target and source scope

## Analytic class and quantifiers

D={z in C: |z|<1}; S consists of holomorphic injective maps f:D->C with f(0)=0 and f'(0)=1. Thus f(z)/z has a removable value 1 at zero and is nonzero throughout D. There is a unique analytic logarithm L with L(0)=0. Define gamma_n by L(z)=2 sum gamma_n z^n. Write b_n=n gamma_n, H(z)=sum b_n z^n=(zf'(z)/f(z)-1)/2, A(r)=sum |b_n|r^n, and S_N=sum_{n<=N}|b_n|. All these series converge at 0<=r<1.

Primary target: for each fixed f in S, there are finite C_f and r_f<1 such that A(r)<=C_f/(1-r) for r_f<r<1. Since A is continuous on compact radial intervals, the cutoff can be removed by changing C_f. A uniform C over all f is a stronger claim not assumed here. To disprove the stated interpretation requires a single f in S and a sequence r_j->1 with (1-r_j)A(r_j)->infinity along a subsequence. A family of different finite-degree extremizers is insufficient.

## Governing primary source

W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, 21 September 2018, https://arxiv.org/pdf/1809.07200v2 . The document publicly identifies itself as a draft. Printed pages 133–134 contain Problem 6.42's normalization, Problem 6.43, and its complete update. Page 114 supplies S; Update 6.1 on page 115 records the de Branges resolution of the Milin inequalities. The target and update were checked in extracted text and rendered page images, including placement of absolute values, powers n^2 and r^n, and the distinction between O and non-o.

The update attributes to W. K. Hayman a function in S whose quadratic sum Q(r)=sum n^2|gamma_n|^2 r^n is not o((1-r)^(-1)log(1/(1-r))). It leaves the absolute-linear-sum problem open. That assertion is not itself a negative answer to 6.43: these are different norms. The cited paper is *The logarithmic derivative of multivalent functions*, Michigan Mathematical Journal 27(2) (1980), 149–179, DOI https://doi.org/10.1307/mmj/1029002355 . Direct article/PDF retrieval was attempted, but the downloaded response was an HTML access/bot page rather than a PDF. Its original construction and proof were not inspected. The historical example is therefore an attributed input from the inspected primary problem update, not an independently verified construction.

The requested starting page https://www.unsolvedmath.com/problems/2306043 was attempted first. Web retrieval failed and the direct HTTP response said Forbidden. No rendered live-site statement or status was inferred. The primary mathematical source governs the attempt.

## Other theorem source and inspection limit

P. L. Duren and M. M. Schiffer, *Grunsky inequalities for univalent functions with prescribed Hayman index*, Pacific Journal of Mathematics 131(1) (1988), 105–117, https://msp.org/pjm/1988/131-1/pjm-v131-n1-p06-p.pdf . Printed pages 106–107 were inspected as text and page images. They define the positive Hayman index and maximal-growth direction, state Bazilevich's weighted-square inequality, and derive it from their strengthened Grunsky theorem. The displayed constant 1/2 and the square on the modulus were verified visually. The later variational proof of that strengthened theorem was not independently audited in this investigation. TURN_4 treats Bazilevich's inequality as a published theorem and proves the subsequent majorant consequences completely.

The de Branges–Milin inequalities and the starlike criterion are established external theorem inputs, not re-proved here. TURN_1's generating-function deduction, TURN_3's coefficient estimate from positive real part, and all elementary sequence arguments are supplied in full. No claim that the source proofs have all been independently reconstructed is made.

## Current-literature check

Searches on 5 October 2026 included the exact problem number, Aharonov with logarithmic coefficients/absolute sums, the cited Hayman title/DOI, and logarithmic coefficients with Hayman index. They did not produce a verified full resolution of this exact problem. Searches returned several modern papers about different coefficient, inverse-coefficient, or subclass questions; those do not resolve this target. This is a bounded search result, not proof that no newer resolution exists. Public primary-paper leads consulted include https://arxiv.org/abs/1701.05413 and https://arxiv.org/abs/2001.11098 ; neither abstract states the full-class absolute-sum assertion here. No proof in those papers is used.

## Queue and duplicate check

At inspection, main was 28128d274d780c814005596ee293141f80e3f2c2. The live main-branch queue row listed rank 683, ID 2306043 / AMR-022-6043, queued, 0/5. The queue file Git blob was dce961ea85917a765b29405f55dec6347d326660. The public catalog selected record agreed on identity/rank/status. Its mathematical desk route proposed dyadic Cauchy–Schwarz and logarithmic energy; that is investigated and limited in TURN_1, TURN_2, and TURN_5.

Read-only repository checks found:
- no 2306043 entry in the 60-directory main attempts listing;
- no selected-ID entry in the main state ledger;
- no PR matches for 2306043, the exact string 6.43, or logarithmic coefficients;
- no branch matches for 2306043, aharonov, or logarithmic;
- the Aharonov PR search matched other, different minimum-area targets, not this problem;
- no selected-ID membership in the public related-target groups.

These checks establish no prior attempt found in the inspected repository surfaces, not omniscience about unindexed/private or deleted work. No historical shared raw corpus was presumed available. The public selected catalog and initial review were checked, but the unavailable full original imported AI report was not reconstructed or treated as evidence. The complete primary statement and update replace no missing mathematical hypothesis.

Public inspection links:
- https://github.com/AlecKriebel/Math/blob/28128d274d780c814005596ee293141f80e3f2c2/unsolved_math_prioritization/QUEUE.md
- https://github.com/AlecKriebel/Math/tree/28128d274d780c814005596ee293141f80e3f2c2/unsolved_math_prioritization/attempts
- https://github.com/AlecKriebel/Math/blob/28128d274d780c814005596ee293141f80e3f2c2/unsolved_math_prioritization/review_v2/related_target_groups.json

Publication scope is only this authored packet and a later independently audited queue-row update. No source PDF/text, catalog contents, source corpus, or private coordination belongs in the published packet.
