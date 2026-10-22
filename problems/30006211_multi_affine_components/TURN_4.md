# Turn 4 — A uniform bound for every pair of bilinear forms

AI-assisted mathematical proof candidate; independent review pending. Original unresolved4/5. This completes the bilinear subclass, including singular and rectangular matrix pencils, while leaving arbitrary multi-affine pairs unresolved.

## 1. Theorem

For arbitrary real m×n matrices A,B and a,b∈R, the set

X={ (x,y)∈R^m×R^n : xᵀAy=a, xᵀBy=b }

has at most four connected components. Every component in the proof is path connected. The bound is sharp already for m=n=2. If a=b=0, X is a cone and is connected. Empty matrix blocks and unused variables are allowed.

## 2. The classical real pencil decomposition

We use the classical Kronecker decomposition under strict equivalence over R. A real pencil sA+B can be brought, by constant real invertible matrices U,V, to a direct sum of a square regular pencil and rectangular right/left singular blocks

L_ε(s)=s[I_ε 0]+[0 I_ε],    ε≥0,

and their transposes. All square finite/infinite elementary blocks can be included in the regular part. The zero-size L_0 is a free unused column variable, and L_0ᵀ a free unused row variable.

This exact arbitrary-field statement is Theorem2.1 in Iwata–Takamatsu, SIAM J.Control Optim.55(2017),2134–2150, printed2136–2137, https://www.opt.mist.i.u-tokyo.ac.jp/~iwata/papers/KCF.pdf. Their Section2 explicitly distinguishes the arbitrary-field decomposition from a further complex Jordan form. We take F=R; complex coordinate changes are not used. The decomposition is a credited standard theorem, not a result proved by the finite checker.

Strict equivalence is legitimate for the common real level set: if A′=UAV and B′=UBV, the changes x=Uᵀξ,y=Vη give ξᵀA′η=xᵀAy and the analogous equality for B. Block diagonal pencils therefore give sums of block contributions on disjoint variable sets.

## 3. A positive singular block controls the topology

Suppose some right singular block has ε≥1. Write z∈R^ε for its short variable and w∈R^(ε+1) for its long variable, and let u collect all other variables. Up to exchanging the two equations, the block contributes

Σ_(i=1)^ε z_i w_i,    Σ_(i=1)^ε z_i w_(i+1).

For z≠0 the two coefficient rows (z,0) and(0,z) are linearly independent. In a putative relation α(z,0)+β(0,z)=0, inspecting the first nonzero entry of z forces α=0 and then β=0. Hence for every u and every pair of residual right-hand sides there is an affine w-fiber of dimension ε−1, with a continuous global section obtained from the2×2 Gram inverse.

The open part z≠0 is therefore an affine bundle over (R^ε\{0})×R^(dim u). More directly, contract its fibers linearly to the Gram section and use paths in the base. It has one path component if ε≥2 and two if ε=1, and it is nonempty for every(a,b).

At z=0, solutions exist precisely when the remaining blocks alone give(a,b); w is then completely free. Any such point first moves w to0 while keeping z=0 and u fixed. It then moves z from0 to any small nonzero vector while retaining w=0 and the same u. The block contribution stays zero, so this attaches the entire zero stratum to the open part. For ε=1, a zero-stratum point joins both signs of z, making X connected. If there is no zero-stratum point, the open part is all of X and has two components. In all cases a positive singular block gives b₀(X)≤2, and an index at least2 gives b₀(X)=1.

A left singular block has the same argument after interchanging its two variable sets. No connected-fiber/projection shortcut is used: the attaching paths are explicit, including the rank-drop stratum.

## 4. No positive singular blocks

If every rectangular block has index0, those blocks contribute only free variables. Removing them leaves a square regular pencil. If its size is positive, it has an invertible real combination because its determinant is a nonzero real polynomial; turn3 applies and gives at most four components. Taking a product with the unused Euclidean variables does not change this count.

If the regular part has size0, both forms are zero. The level set is empty when(a,b)≠(0,0) and all of the ambient Euclidean space when(a,b)=(0,0). Thus it has at most one component. These cases complete the proof.

The four-component example from turn3, x1y1+x2y2=1 and x1y1−x2y2=0, proves sharpness. Positive singular blocks do not furnish larger examples.

## 5. What this means for the original multi-affine question

Every bilinear form in two disjoint variable sets is multi-affine, so this is a degree-two subclass of the source's question with a dimension-independent bound. It covers all real coefficients and arbitrary rectangular shapes; it is not just simultaneous diagonalization or a generic-pencil statement.

A general multi-affine quadratic polynomial need not be bilinear across any partition, and affine linear terms need not be removable simultaneously. Higher-degree overlapping monomials are also absent here. Consequently the theorem does not establish the degree-two case for all multi-affine pairs, let alone the full arbitrary-degree question.

## 6. Exact controls and credit

`python turn4/check_singular_blocks.py` checks358 nonzero short-block vectors, exact full-row-rank solution sections for several residual values, zero-stratum attachments and real strict-equivalence identities. All4,421 assertions pass; stdout is frozen in turn4/verification.json. These are algebraic controls, not a numerical computation of general Kronecker forms or topology.

The matrix-pencil decomposition is explicitly credited to classical Kronecker theory, with the precise real-field statement verified in Iwata–Takamatsu above. Van Dooren's primary1979 paper, https://perso.uclouvain.be/paul.vandooren/publications/VDooren79.pdf, was also retrieved as historical/algorithmic context; no new canonical-form algorithm is claimed. Basu–Perrucci's existing component results remain credited in SOURCE_GATE.md. No novelty certification. Original unresolved4/5, informal completion estimate45%.
