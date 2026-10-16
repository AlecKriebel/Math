# Independent mathematical derivation (before previous audit conclusions)

## Exact target and required inputs

For each fixed closed oriented topological surface S of genus g >= 2, with the half-log quasiconformal Teichmuller metric d_T, the target is one finite c_g >= 0 valid for all centers o, all finite R >= 0 and all x,y in the closed ball B(o,R), giving an actual continuous rectifiable path contained in that same ball with length <= d_T(x,y)+4c_g. This is a claim about ordinary metric length, not solely an infimum of allowable path lengths.

The substantive external hypothesis needed is the following uniform extremal-length statement: a finite K_g >= 1 independent of endpoints a,b, intermediate point z and essential simple closed curve gamma satisfies Ext_z(gamma) <= K_g max(Ext_a(gamma),Ext_b(gamma)) along every minimizing Teichmuller segment. The full scope and source statement still require independent primary-source verification. Another external input is existence of minimizing Teichmuller segments and Kerckhoff's formula with factor 1/2 and the indicated ratio direction.

## Derivation from those hypotheses

Every essential curve has positive extremal length at every point. Put f_w(gamma) = (1/2) log(Ext_w(gamma)/Ext_o(gamma)). Dividing the given inequality by Ext_o(gamma) and taking half logarithms yields f_z(gamma) <= (1/2)log K_g + max(f_a(gamma),f_b(gamma)). For every gamma, f_a(gamma) <= sup_eta f_a(eta) and similarly for b. Hence sup_gamma f_z(gamma) <= (1/2)log K_g + max(sup_gamma f_a(gamma),sup_gamma f_b(gamma)). Kerckhoff then gives d_T(o,z) <= max(d_T(o,a),d_T(o,b))+c_g, where c_g=(1/2)log K_g >= 0. This deduction uses no extremal curve or foliation attaining a supremum. If the original uniform K were below 1, replacing it by max(K,1) would retain the estimate.

Now work in any geodesic metric space with that radial segment estimate for some finite c >= 0; existence of one suitable minimizing segment for every endpoint pair suffices. Select radial minimizing segments from o to x and o to y for this fixed pair only. A point at radial arclength t on one of them has distance exactly t from o, by minimality of its subsegments. Thus a radial piece never exits the original ball.

If R < c, concatenate x-to-o and o-to-y. Its length d(o,x)+d(o,y) <= 2R < 2c <= d(x,y)+4c. This also covers a center endpoint and coincident endpoints (a constant path would additionally suffice).

If R >= c, define alpha=min(c,d(o,x)) and beta=min(c,d(o,y)). Let a and b be the respective points after traversing those inward distances. Then d(o,a)=max(d(o,x)-c,0) <= R-c; the nonnegative right side is essential here. The identical estimate holds for b. The suitable minimizing a-to-b segment has radial distance <= R-c+c=R everywhere. Both radial end pieces stay inside B(o,R). Triangle inequality along a-x-y-b gives d(a,b) <= alpha+d(x,y)+beta, so total concatenated length alpha+d(a,b)+beta <= d(x,y)+2alpha+2beta <= d(x,y)+4c.

Each nonconstant piece has an isometric arclength parametrization on a finite closed interval. Pasting those at their common endpoints defines a continuous map on [0,L]; zero-length pieces are omitted, or retained as constant intervals. If L=0 use the constant path on [0,1]. Finite concatenation has length equal to the sum of piece lengths: the upper bound follows by inserting joining times in any partition and the lower bound by combining near-maximizing partitions of each piece. Rescaling the parameter interval gives an actual continuous rectifiable path, without intrinsic-distance attainment or any compactness assumption.

At R=c all retreated points are o, so the middle is constant and total length <=2c. At c=0 radial retreat is zero and the given estimate puts the chosen original segment in the original ball. At R=0 endpoints are necessarily o and the path is constant; if c>0 this falls in R<c and if c=0 in R>=c. Cases a=b, x=y, either endpoint o, asymmetric short radial distances and nonunique selected radial/middle segments impose no additional assumption. No simultaneous or continuous selection over parameter families is required.

For fixed g, choosing c_g=(1/2)log K_g produces the target. If d_T(x,y)<=k for k>=0, the same path has length <= k+4c_g. Farb's k=2 formulation follows if his domain is exactly the original closed Teichmuller ball. For arbitrary k>0 this is the stronger quantified additive bound. This does not give a genus-independent estimate, a numerical value or an optimal Teichmuller constant.

## Adversarial checks and exact remaining gap at this checkpoint

The potentially central failures would be (i) K depending on gamma or endpoints, (ii) a thick-part restriction, (iii) reversed Kerckhoff quotient/normalization, (iv) no actual minimizing segments, (v) the target using another metric or enlarged ball. These are primary-source scope questions still outstanding. No gap remains in the conditional metric argument. The generic proof is an elementary deduction and supplies no evidence of historical priority or a new substantive Teichmuller theorem. Direct segment nonconvexity is compatible with this concatenated path. A dual-wall-space estimate cannot be numerically compared to original d_T using only a quasiisometry.
