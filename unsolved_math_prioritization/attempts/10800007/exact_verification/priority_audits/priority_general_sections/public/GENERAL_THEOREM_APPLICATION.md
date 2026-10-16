# Checked application of a classical general theorem

Saved 2026-10-13T05:16:34.686498+00:00. This is an audit derivation, not a priority attribution or paper. It was developed after the independent first seal.

## Published theorem actually read

Hatcher, *Algebraic Topology*, Theorem 2B.3, printed p. 172: every continuous injection from an open subset of R^n to R^n has open image. The full theorem and proof were read in a public academic mirror of the author's book PDF: https://people.dm.unipi.it/benedett/HATCHER.pdf, PDF page181, also visually verified. The mirror PDF metadata records creation2015-04-22; the exact edition/build is not certified as the2002 publisher PDF. The known published book is Cambridge University Press2002, but the mirror's exact build/version has not been authenticated as the publisher final. No original Brouwer1911/1912 body is claimed read.

## Target-specific hypothesis certificate

Let E={(p,x,y): x²−y²+a1x+a2y+a0=0, xy+b1x+b2y+b0=0}⊂R8. The map T:R6→E defined on q=(a1,a2,b1,b2,x,y) by

T(q)=((a1,a2,−x²+y²−a1x−a2y,b1,b2,−xy−b1x−b2y),x,y)

is a homeomorphism. It is continuous, maps into E by direct substitution, and its continuous inverse reads the four linear coefficients and two root coordinates. Thus E is a six-dimensional manifold with a global Euclidean chart.

In that chart the incidence projection is

Q(q)=(a1,a2,−x²+y²−a1x−a2y,b1,b2,−xy−b1x−b2y).

Q^-1(0)={0}: the four linear coefficients must vanish, then x²−y²=xy=0 forces x=y=0.

For each t>0, q_+(t)=(0,0,0,0,t,0) and q_−(t)=(0,0,0,0,−t,0) are distinct, converge to0, and have equal images (0,0,−t²,0,0,0). Hence Q is not injective on any neighborhood of0.

Suppose an open U⊂R6 containing0 has an exact continuous real-root selection. It induces a strict section σ:U→R6 of Q. Q∘σ=id_U makes σ injective, and uniqueness at0 gives σ(0)=0. By the published general theorem σ(U) is open inR6 and contains0. Therefore σ(U) contains q_+(t),q_−(t) for sufficiently small t>0. But Q is injective on σ(U), because Q(σ(p))=p and σ is a function. This contradicts Q(q_+(t))=Q(q_−(t)). Thus there is no local section at0, and every hypothetical open cover fails at a member containing0, whatever its cardinality.

This establishes a direct general-theorem route with no fibration assumption, no discriminant removal, and no approximate substitution. The algebraic chart, uniqueness, and arbitrarily close duplicate pair are **our target-specific deductions**. The cited theorem itself does not name the six-coefficient family or diagnose Vassiliev Problem 2A. Accordingly, its historical availability establishes prior general mathematical machinery, not a prior explicit full-target resolution.

## Equivalent elementary degree route

The slice i(w)=(0,0,−Re(w),0,0,−Im(w)/2) has exactly the roots z²=w. A local section restricts to a disk square root. On a circle w=r·u, h(u)=s(r·u)/√r maps S1→S1 and h(u)²=u. Hatcher Section 2.2 printed p. 134 gives multiplicativity of degree; Example 2.32 printed p. 137 gives degree2 for the squaring map. Therefore1=2deg(h), impossible. Full relevant printed p. 134 and137 were read textually and visually; this is a deduction from degree facts, not an assertion of a published target resolution.
