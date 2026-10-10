# Planar IKEA problem: credited prior resolution

**Problem:** 1900002 / AMR-018-0002, ranked entry 1016.  
**Status:** SOLVED-IN-LITERATURE, for planar convex lattice polygons.  
**Proof turns:** 0. The prior-result stopping condition applies.

## Exact question and attribution

Karpenkov's 2017 problem list, §1.3, Problem 2, seeks a characterization of ordered collections of integer-angle LLS data that can occur around a planar lattice polygon.

Source: [Open problems in geometry of continued fractions](https://arxiv.org/abs/1712.01450), p. 3. The same section's Problem 1, concerning an integer cosine rule, is a separate question.

James Dolan and Oleg Karpenkov give the planar convex classification in **Theorem 3.3** of [Lattice angles of lattice polygons](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/), *Journal de théorie des nombres de Bordeaux* 37(3) (2025), 873–896, DOI 10.5802/jtnb.1345. Its proof is §5.1, p. 893. The publisher records online publication on 27 November 2025; [arXiv:2310.01091](https://arxiv.org/abs/2310.01091) was submitted on 2 October 2023.

This resolves the convex planar interpretation adopted by the primary authors. It does not settle arbitrary nonconvex polygons, the integer cosine rule, or higher-dimensional IKEA. The journal article separately identifies higher-dimensional IKEA as open in §6. Its angle data classify realizability, not a unique affine-congruence class of polygon.

## Arithmetic form of the classification

Write the ordered LLS blocks as A_1,...,A_n, each a nonempty positive integer sequence of odd length, with n >= 3. Concatenation is denoted by a comma. For integers c_1,...,c_n define

U_j = (A_1,c_1,A_2,...,c_(j-1),A_j),

V = (A_2,c_2,A_3,...,c_(n-1),A_n).

The continuant convention is K(())=1, K((a))=a and

K(x_1,...,x_m)=x_m K(x_1,...,x_(m-1))+K(x_1,...,x_(m-2)).

The prescribed angle-curvature data are realizable by a convex lattice n-gon exactly when:

1. K(U_n)=0;
2. c_n = -floor(K(V,1)/K(V));
3. the list K(U_1),...,K(U_n), after deleting zero entries, has exactly n-3 sign changes.

For the angles-only question, quantify existentially over c_1,...,c_(n-1) and set c_n by condition 2. The denominator is automatically nonzero if condition 1 holds, as proved in AUDIT.md. This is an exact classification by integer witnesses. The packet does not claim a finite bound on those witnesses or a terminating rejection algorithm obtained by bounded enumeration.

## What was checked

The exact primary statement, published theorem, defining conventions and proof were inspected. The executable audit independently derives angle blocks and chord curvatures from 203 concrete convex lattice polygons; checks cyclic starts and integral affine shears; and compares 19,531 signed continuant words with independent matrix products. Incorrect closing curvature and a closed wrong-winding example are rejected. These finite checks support transcription and convention accuracy; they are not the proof of the theorem.

The public packet contains authored explanations, code and verification metadata only. The source PDFs, extracted text, dataset contents and private gate records are excluded. The cited published theorem supplies the mathematical resolution; no novelty or formal-verification claim is made.
