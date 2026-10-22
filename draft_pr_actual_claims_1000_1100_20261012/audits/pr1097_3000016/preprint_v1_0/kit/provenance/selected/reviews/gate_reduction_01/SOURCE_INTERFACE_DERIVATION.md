# Independently checked source interfaces

## Source hardness

[Farrell–Levine v3](https://arxiv.org/pdf/1502.04690v3) defines HALTING on PDF page 2 with a nonnegative configuration and a strongly connected adjacency-matrix multigraph; loops are allowed. Page 10 uses logarithmic multiplicity size. Theorem 3.1, pages 11–13, constructs a strongly connected total Laplacian from a lattice basis in polynomial time; page 11 explicitly gives a Karp reduction and Corollary 3.2 states NP-completeness. I read these complete pages, plus the relevant introduction and least-action statement on pages 1–4; pages 2, 10 and 11 were also actually viewed as rendered images. This is a dependency on a published theorem, not a reproof of the Amini–Manjunath lattice hardness theorem it cites.

The p.11 lattice representative may be signed. Independently, adding k_v=max(0,-x_v) loops and the same k_v chips leaves the net update matrix unchanged, shifts every threshold and every reachable coordinate by the same fixed k_v, and preserves legality and stable endpoints for every word. This valid authored bridge removes any need to infer an unstated nonnegative representative. Its bit size is polynomial. Removing loops by relays next is essential before the gate construction.

## Target membership

[Hujter–Kiss–Tóthmérész v4](https://arxiv.org/pdf/1507.03209v4), pages 2–3, defines loopless multigraphs, binary adjacency multiplicities and nonnegative configurations. Its complete Theorem 12 proof on pages 8–9 supplies coNP membership. I read the full proof, Proposition 8 and the required preliminary period/deletion/bounded-game statements on pages 2–6; pages 2, 3, 4, 8 and 9 were actually viewed as rendered images. The certificate does not assume a supplied firing word or that its intermediate vector g is legal.

For the strongly connected subclass, one can check the polynomial-bit certificate boundary independently. Write L for the incoming, negative-diagonal Laplacian. A reduced nonnegative solution f to Lf=y-x has some coordinate f(w)<p(w), where p is the primitive positive kernel vector. Cofactor bounds give polynomial bit length for p. Fixing w, delete row/column w: L_w is nonsingular, and

f_{-w}=L_w^{-1}((y-x)_{-w}-f(w)L_{-w,w}).

Every numerator is bounded by determinant/cofactor bounds in the input dimension, maximum degree, and input coordinate bit lengths; the integer denominator has absolute value at least 1. Thus f has polynomial bit length, and 0<=g<=f does too. Reducedness is checkable from the primitive period vector, computed by cofactors and gcd. Integer linear equivalence is decidable by polynomial integer linear algebra; in a strongly connected graph a signed integer solution can be shifted by a positive kernel multiple to become nonnegative. This supplies an explicit size check for the source theorem's certificates.

The soundness comparison is especially useful: if a legal prefix has odometer h<=g and the next move v exhausts the matching coordinate h(v)=g(v)<f(v), all other coordinates of g-h contribute nonnegative incoming chips. Hence (x+Lg)(v)>=(x+Lh)(v)>=d_v, contradicting the claimed stuck condition. No uniqueness of arbitrary unreduced legal odometers is assumed.

## Earlier barrier

[Tóthmérész v2](https://arxiv.org/pdf/2102.11970v2), pages 4–7, was read completely. Page 5 was visually viewed. Theorem 2.3 reaches its polynomial-hierarchy consequence through recurrence and certificates for nonhalting. That proof interface differs from the present direct gate/marker many-one construction. This observation alone says nothing about priority against later publications.

## Original problem access

The current standalone Egres problem page failed direct retrieval and web opening; bounded alternates and their outcomes are recorded in SOURCE_ORIGINAL_ACCESS.json. The primary Egres chip-firing survey was returned in full by web search and read, including its signed configuration definition and its separate simple-graph and multigraph complexity rows. It supports directed multigraph coNP-hardness as the relevant branch. The repo catalog identifies AMR-029-0016 with the standalone page title. I do not claim to have retrieved or read the standalone problem body today. The parent should retain this access limitation until independently resolving that exact-page question, and should not infer current openness from historical labels. Mathematical validation here covers the expressly stated binary-multigraph language; it does not answer the separate simple-graph branch.
