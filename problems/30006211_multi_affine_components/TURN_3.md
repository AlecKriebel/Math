# Turn 3 — Four-component bound for regular square bilinear pencils

AI-assisted mathematical proof candidate; independent review pending. Original unresolved3/5. Consider two equations xᵀAy=a and xᵀBy=b in x,y∈R^m, with a real matrix pencil containing an invertible member. Each defining polynomial is multi-affine, but this is a restricted bilinear class.

## 1. Reduction and statement

The common zero set has at most four connected components. If m≥3, it has at most two. These bounds include degenerate and nondiagonalizable matrices.

If a=b=0, the solution set is a cone containing0 and is path connected. Otherwise choose a linear combination M of A,B that is invertible and whose corresponding right-hand side is nonzero. Such a choice exists because the invertible combinations form a nonempty open subset of R² and cannot be contained in the line annihilating(a,b). Make an invertible change of the two equations, normalize the first constant, and change y by an invertible matrix. The problem becomes

X_C={ (x,y): x·y=1, xᵀCy=0 }

for some real m×m matrix C. All these changes are homeomorphisms or equivalent equations, and preserve bilinearity. The exact classification below proves the bound.

## 2. Rank at least two, nonscalar C

Fix x. Put v=Cᵀx. The y-fiber is nonempty iff x≠0 and either x,v are independent, or v=0. Thus the base of the projection to x is

B=R^m \ ({0} ∪ ⋃_(λ∈R\{0}) ker(Cᵀ−λI)).

Only real eigenvalues contribute. On D=B\ker Cᵀ, the two rows xᵀ,vᵀ are independent. The fibers are affine spaces of dimension m−2, with a continuous global section given by solving the full-row-rank2 matrix by its Gram inverse. Linear contraction of each fiber onto that section shows that each path component of D lifts to a path-connected subset of X_C.

We must handle compatible rank-one fibers rather than assume connected fibers suffice. Let x0∈ker Cᵀ\{0}. Since rank C≥2, choose δ with v=Cᵀδ not parallel to x0. The two equations

(x0+tδ)·y=1,  v·y=0

have a continuous local solution y(t) near t=0 because their rows are independent there. For t≠0 this is a solution over x0+tδ in D. The original fiber over x0 is the connected affine hyperplane x0·y=1, so every one of its points can first move within that fiber to y(0), then along this attaching path into the rank-two part. Thus no new component is created at such fibers.

The components of D and B are precisely the chambers determined by the codimension-one nonzero real eigenspaces. All other removed eigenspaces, ker Cᵀ and{0} have codimension at least two and cannot disconnect a chamber. To justify this elementary fact, in an open convex chamber connect two points by two line segments through a generic intermediate point: for each removed codimension-two linear subspace, the forbidden intermediate points lie in a proper affine subspace obtained by spanning it with an endpoint. Avoid finitely many such sets. Projection to B prevents different chambers from being joined in X_C, and the preceding attachment argument shows every point over a chamber is in its one lifted component.

For m≥3, at most one real eigenspace can be a hyperplane, since eigenspaces for distinct eigenvalues have direct sum and2(m−1)>m. For m=2, there are at most two such lines. Hence in this rank≥2 nonscalar case the component count is2^h, with h the number of nonzero real eigenvalue hyperplanes: h≤1 when m≥3 and h≤2 when m=2.

## 3. Scalar and rank-one exceptions

If C=λI with λ≠0, there are no solutions. If C=0, the set is B_m={x·y=1}. The linear change u=(x+y)/√2,v=(x−y)/√2 identifies B_m with S^(m−1)×R^m by setting the radius of u to√(2+||v||²). It has two components for m=1 and one for m≥2.

Now let rank C=1 and C≠0. Write C=u vᵀ and λ=vᵀu=trace C.
- If λ≠0, a real similarity takes C to diag(λ,0,…,0). A simultaneous dual change of x and y preserves x·y. The equations become x1y1=0 and Σ_(j≥2)x_jy_j=1. The first-pair zero-product fiber is connected, so the count is that of B_(m−1): two for m=2, one for m≥3, and empty for m=1.
- If λ=0, C is a nonzero rank-one nilpotent. A real similarity makes its only nonzero entry a single off-diagonal1. Relabelling gives x2y1=0 along with x·y=1. The solution set is the union of the branches x2=0 and y1=0. Each is B_(m−1) times a free line. Their intersection imposes x2=y1=0 and Σ_(j≥3)x_jy_j=1. For m=2 the intersection is empty and each branch has two components, giving four. For m≥3 each branch is connected and their intersection is nonempty, giving one.

The rank-one normal forms follow directly by choosing a basis beginning with u and, in the nilpotent case, a vector w satisfying vᵀw=1; no diagonalizability assumption is used. This exhausts all cases.

The nilpotent m=2 example is an important counter-control: its projection base is connected with connected nonempty fibers, yet the total space has four components. The explicit attachment analysis and exceptional cases are necessary.

## 4. Sharpness and limits

For m=2, x1y1+x2y2=1 and x1y1−x2y2=0 give x1y1=x2y2=1/2, with four components. For m≥3, taking C=diag(1,…,1,0) gives two components, distinguished by the sign of the last x-coordinate; the other bilinear zero-level factor is a cone and connected. Thus both bounds are sharp.

The current theorem assumes a square pencil with an invertible real combination. It does not yet cover a singular/rectangular pencil, affine linear terms that cannot be removed by a common translation, or higher-degree overlapping multi-affine polynomials. The next turn addresses singular bilinear blocks; the original question remains broader.

## 5. Controls and credit

`python turn3/check_regular_pencils.py` checks186 small exact matrix models, including scalar, real/nonreal, Jordan and rank-one cases,765 explicit rank-drop attachment samples and the exceptional branch identities. Its1,879 assertions supplement the path-component proof. Imported turn2 controls run silently and are not counted again. An initially incorrect second-branch test parametrization was corrected before this file was frozen; the mathematical branch statement above and final receipt use y1=0 correctly.

The argument uses standard rank/eigenspace and elementary topology facts, with no novelty certification. The source problem remains Basu's OWR9/2025 question, https://ems.press/content/serial-article-files/51353, and the previously established one-polynomial context is credited to Basu–Perrucci, https://arxiv.org/abs/2204.01595. Original unresolved3/5; informal completion estimate35%.
