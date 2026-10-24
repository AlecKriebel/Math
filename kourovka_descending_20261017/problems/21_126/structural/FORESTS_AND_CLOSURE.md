# Forest ambient graphs and closure of excluded classes

Prepared October 24, 2026 UTC. These are deductions from established structural theorems plus elementary group arguments, not a complete solution of 21.126 or a claim of first priority.

## Forest RAAGs

**Proposition1.** Every finitely generated subgroup H of a finite forest RAAG is finitely presented and has a quadratic Dehn upper bound.

For a finite tree with at least three vertices, Tran, *Geometric embedding properties of Bestvina–Brady subgroups*, Algebraic & Geometric Topology17(2017),2499–2510, Theorem6.3, constructs the RAAG as the group of a compact orientable graph manifold. Trees with one or two vertices give Z and Z², realized by a solid torus and T²×I. A forest gives the free product of these groups, hence is the group of their orientable connected sum. The empty graph gives the trivial group. Thus every forest RAAG is a compact orientable3-manifold group.

Pass to the interior, whose inclusion in the compact manifold induces an isomorphism on π1, and take the covering corresponding to H. This is an orientable3-manifold with finitely generated fundamental group H. Scott's compact-core theorem supplies a compact orientable submanifold C with π1(C)≅H. Hence H is finitely presented. Applying the theorem to the interior avoids any distinction about Scott's original boundary convention.

No prime factor of C can have Nil or Sol geometry. Indeed its group would inject in H as a free factor, and would contain a finite-index subgroup which is respectively a nonabelian nilpotent group or a nonabelian solvable torus-bundle group. Both are solvable and nonabelian. Baudisch's two-generator theorem for RAAGs states that two noncommuting elements generate a nonabelian free group. Therefore every solvable subgroup of a RAAG is abelian: a noncommuting pair in such a subgroup would generate a nonsolvable subgroup F2. This contradiction excludes both exceptional geometries, including their finite quotients.

Aschenbrenner–Friedl–Wilton, *Decision problems for3-manifolds*, Geometry & Topology Monographs19(2015),201–236, Corollary4.7 (printed p219), states that the group of a compact orientable3-manifold with no Nil or Sol prime factor satisfies a quadratic isoperimetric inequality. Apply it to C. □

Dependencies: Scott, *Compact Submanifolds of3-Manifolds*, JLMS(2)7(1973),246–250, DOI10.1112/jlms/s2-7.2.246; Baudisch, *Subgroups of semifree groups*, Acta Math. Acad. Sci. Hungar.38(1981),19–28, DOI10.1007/BF01917515. Original PDFs for these two older results were not obtained (publisher403/non-PDF response). Their bibliographic records and stated standard theorem scopes were checked; this is an explicit access limit, not a claim of an independently reproduced proof of the external theorems. The Tran and3-manifold filling papers were downloaded and their actual theorem statements inspected.

In particular **A(P4) admits neither requested kind of subgroup**. This is an intrinsic filling deduction via compact cores, not an inheritance of ambient CAT(0) filling bounds.

## A closure lemma for ambient exclusions

For a fixed integer d≥2, let P_d(G) mean that every finitely presented subgroup H≤G has δ_H≼n^d.

**Proposition2.** The property P_d is preserved by finite free products and by taking direct product with Z.

For G=G_1*⋯*G_k, Kurosh's subgroup theorem expresses any finitely generated H≤G as a free product of a finitely generated free group and finitely many conjugates of subgroups H_j≤G_{i(j)}. Finite generation gives finiteness of the nontrivial factors and finite generation of them; finite presentation of H gives finite presentation of each factor because each is a retract. Thus each factor has δ≼n^d. In a null word of length n in this finite free-product presentation, reduction decomposes the filling into factor words with total length at most n; ∑n_i^d≤n^d. The free factor costs no relator cells. Adjusting finitely many presentation constants proves P_d(G).

For G×Z and H≤G×Z finitely presented, write K for its projection in G. If H∩(1×Z)=1, projection identifies H with K, so P_d(G) applies. Otherwise H∩(1×Z)=1×mZ for some m≥1. For k∈K choose (k,z)∈H; z mod m is well-defined and gives a homomorphism θ:K→Z/m. Hence

H={(k,z)∈K×Z: z mod m=θ(k)},

so H has finite index m in K×Z. It follows that K×Z is finitely presented, and K, being a retract, is finitely presented. Thus δ_K≼n^d. Sorting letters in a product presentation gives δ_{K×Z}≼δ_K+n²≼n^d; finite-index invariance gives δ_H≼n^d. □

## An explicit recursive class of ambient graphs

Let C be the least graph class containing (a) all finite forests and (b) all complete multipartite graphs with at most three nonempty parts, and closed under disjoint unions and adding universal vertices. Then every finitely presented subgroup of A(Γ), Γ∈C, has δ≼n^9.

For forests use Proposition1. For complete multipartite graphs with at most three parts, A(Γ) is a direct product of at most three finite-rank free groups. Ascari–Bertolotti–Italiano–Llosa Isenrich–Migliorini, [arXiv2406.19860v2](https://arxiv.org/abs/2406.19860v2), TheoremA, gives the degree-nine bound; fewer factors can be padded by trivial coordinates in three nonabelian free factors. Disjoint union corresponds to free product and a universal vertex to a direct Z factor, so Proposition2 proves the recursive assertion.

All defining graphs with at most four vertices lie in C (the executable census supplies a finite independent combinatorial check). This is only a sufficient exclusion criterion. Graphs outside C are not certified viable, and the degree9 bound is not claimed optimal. The full problem still includes arbitrary defining graphs and arbitrary finitely presented subgroups.
