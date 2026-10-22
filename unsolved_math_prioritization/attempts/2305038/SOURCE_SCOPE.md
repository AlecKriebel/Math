# Problem 5.38: source and scope checkpoint

Target: upstream 2305038 / AMR-022-5038, queue rank 316. The task is a simpler proof of two known sharp comparison inequalities, not discovery of the inequalities.

## Original source

Hayman and Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (21 September 2018), printed pp.98–99, PDF pp.99–100. The displayed question and its update were read together, and PDF p.100 was visually checked. The set D is the open complex unit disk. S consists of holomorphic injective functions F:D→C with F(0)=0 and F'(0)=1. Subordination means g=F∘φ for a holomorphic disk self-map φ with φ(0)=0; g itself need not be injective or locally injective. The two closed comparison disks have radii R=(3−sqrt(5))/2 and rho=3−sqrt(8).

The text says that a=g'(0)/F'(0) is real. This is insufficient: with F(z)=z/(1−z)^2 and φ(z)=−z, at z=−r, every 0<r<1 gives |g(z)|/|F(z)|=((1+r)/(1−r))^2>1 and |g'(z)|/|F'(z)|=((1+r)/(1−r))^4>1. This is a missing sign hypothesis in the source itself, not an extraction change.

The intended classical normalization is 0≤a≤1. The upper bound follows from Schwarz's lemma. Campbell's 1973 paper, p.425 Theorem 3, explicitly assumes g'(0)≥0. A rotation of the subordinate map alone does not preserve pointwise comparison with the same F at the same z, so the sign cannot be dismissed without changing the problem.

The printed update cites Campbell's enlargement of S to the universal linear-invariant family U_2. Enlargement is not itself a proof simplification. Campbell p.425 describes the forthcoming derivative proof as long and tedious. Barnard–Pearce (2008 author manuscript, published 2009) extends the derivative theorem to all orders α≥1, but its introduction pp.2–5 reviews the multiregion Campbell argument, and its later proof uses substantial exact algebra. We do not classify that extension as the requested simple proof.

## Working target and success test

Find checkable substantially simpler proofs of BOTH classical sharp radii, under the explicitly corrected 0≤a≤1 normalization. The missing-sign diagnostic does not complete this intended target. A proof only for a=0, only one inequality, a smaller radius, or injective φ leaves a gap. The objective comparison 'simpler' must be explained by proof structure and dependencies, not asserted as a theorem of novelty.

## Literature status at 2026-10-01

Read the full source entry and context; Campbell 1973 paper (all six pages, with p.425 directly relevant); Barnard–Pearce author manuscript introduction pp.1–5. The latter is published in *Complex Variables and Elliptic Equations* 54(2) (2009), 103–117, DOI 10.1080/17476930802669686. Its 16-page author manuscript is dated 3 November 2008; no byte comparison with final publisher PDF is claimed. The exact derivative normalization appears in the paragraph after Theorem B, rather than its abbreviated theorem sentence. Neither its unrelated α<1.65 extension nor its computational proof is being recertified here.

A 2025 primary chapter by A. Wiśniowska-Wajnryb, in *Advances in Functional and Complex Analysis*, pp.87–103, concerns majorization→derivative majorization for Ma–Minda convex subclasses. Its introduction and stated scope were checked; it does not supply this subordination→majorization simplification. Narrow searches found no later exact simplification, which is not proof of absence. Shah's original 1957 papers and Campbell 1972/1974 full papers have not yet been retrieved; AMS PDF requests returned HTTP 403. Do not claim a full historical proof comparison until those inputs are available or the limitation is explicit.
