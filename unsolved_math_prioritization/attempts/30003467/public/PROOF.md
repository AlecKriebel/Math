# Exact deduction of the prior negative answer

## 1. Target and conventions

Let P be a finite set of distinct planar points, and let F be a family of pseudo-disks. The target asks for a map c:P→{1,2,3} such that, for every D∈F,

|P∩D|≥4 implies |c(P∩D)|≥2.

Thus the quantifiers are ∀F ∀P ∃c ∀D∈F. The coloring may depend on both P and F. “Proper” here means non-monochromatic hyperedges of the indicated size. It does not mean that all three colors occur or that every pair of points in a disk has different colors. The vertices being colored are points. Coloring the regions themselves is a different, dual question.

The original source is Pálvölgyi's report of joint work with Keszegh, OWR 19/2017, Conjecture 2, printed p.1173, [original report](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1). The supplied cleaned wording permits a misleading ∀P ∃c ∀F reading; that is not substituted for the source target.

Standard pseudo-disks are bounded closed Jordan regions whose distinct boundaries meet in at most two points. The related 2019 paper also uses the boundary-arc convention permitting shared arcs. Our witnesses can be chosen as distinct ordinary closed disks and satisfy both conventions, so this distinction does not affect the answer.

## 2. The imported theorem and credit

Damásdi–Pálvölgyi's Theorem 1 supplies, for each positive integer m, a finite planar point set whose every three-coloring has a monochromatic disk trace of exactly m points. The proof uses open disks. [Preprint, Theorem 1](https://arxiv.org/abs/2011.12187); [published article](https://doi.org/10.1007/s00493-021-4846-5).

This published existence theorem is the only non-elementary input to the deduction below. Its geometric construction is not claimed as a new construction here.

## 3. Finite-family reduction

Apply the theorem with m=4 to obtain P. There are precisely 3^|P| maps P→{1,2,3}. For each such map c choose one open disk U_c whose trace E_c=P∩U_c has exactly four points and is monochromatic under c. This is a finite collection of choices, hence produces a finite family U. Discard duplicate disks. For every c, at least one of its witnessing disks remains. Thus the same one finite family U defeats every three-coloring. The construction has not chosen a different family after the coloring is fixed: all witnesses were collected first.

Alternatively, one may take one representative disk for each trace E_c. There are at most binomial(|P|,4) such traces. Either bound proves finiteness; no bound independent of |P| is required by the target.

## 4. Closed disks with exactly the same incidences

Write U=B(o,r), with r>0, for one of these finitely many open disks, and set E=P∩U. Since E has four points,

a=max{||p-o||:p∈E}<r.

Choose any r' satisfying a<r'<r, and let D={x:||x-o||≤r'}. Every point of E is strictly inside D. Every p∈P\E has ||p-o||≥r>r', so is strictly outside D. Consequently P∩D=E and no point of P lies on ∂D. Do this independently for every U∈U. The resulting finite family F has exactly the same relevant traces. Duplicate closed disks may again be discarded without losing any trace.

This argument works even if an excluded point lay on an original open-disk boundary. It needs no generic-position assumption and no assertion that the open disks were uniformly separated in advance. In exact squared-distance form one can choose (r')²=(a²+r²)/2; this is the transfer formula exercised by the finite controls.

## 5. Why this is an admissible pseudo-disk family

Each member of F is a bounded closed disk of positive radius, hence a Jordan region. For two different disks with centers o₁,o₂ and radii r₁,r₂, their boundary equations are

||x-o₁||²=r₁² and ||x-o₂||²=r₂².

If o₁≠o₂, subtracting the equations gives a nonconstant affine equation. Common boundary points therefore lie on one line; a line meets a circle in at most two points. If o₁=o₂, distinct radii give disjoint boundaries. Equal radii would give a duplicate disk, already discarded. Thus any two distinct boundaries meet at most twice.

For the connected-boundary-arc convention, restrict the inequality ||x-o₁||²≤r₁² to x=o₂+r₂(cos t,sin t). After cancellation it has the form A cos t+B sin t≤C. Its solution on the circle is empty, the entire circle, a point, or one connected closed arc. The concentric case is empty or the entire circle. Hence this convention is satisfied too, with the usual inclusion of disjoint pairs.

## 6. Contradiction and scope

Suppose the target held for this P and F. It would supply a map c:P→{1,2,3}. Section 3 supplies its witness U_c. Section 4 supplies D_c∈F with P∩D_c=P∩U_c. That intersection has exactly four points of one color, violating the required implication. Therefore the actual threshold-four conjecture is false.

The same deduction works at each prescribed positive integer threshold m. In particular, replacing 4 by some larger universal threshold cannot rescue the unrestricted primal pseudo-disk statement. An open family versus a closed family, exact m versus at least m, or finite versus possibly infinite range families does not rescue it either.

This says nothing negative about fixed-radius disks, families with a common stabbing point, or a dual coloring theorem. The counterexample uses the unrestricted disk family, where radii may vary; deleting that freedom changes the problem. No new priority, exhaustive search, minimal witness size, explicit coordinate certificate, or independent proof of the imported geometric existence theorem is claimed.
