# Reading the exact examples

[EXACT_EXAMPLES.json](EXACT_EXAMPLES.json) contains three small complete authored examples. Rational coordinates are strings, such as "8/9"; they are exact fractions rather than decimal approximations. All convex objects are closed and filled. Each object is the convex hull of its listed points, and planar polygons are listed counterclockwise. Edge and vertex labels are distinct.

## The three-edge standard example

The entry standard_3 records edges e0={v1,v2}, e1={v0,v2}, e2={v0,v1}, the three complete incidence orders, all three normalized edge witnesses, and all three representing segments. The third normalized coordinate is retained in edge_points, while objects uses the first two coordinates. Dropping the third coordinate is an affine bijection on the coordinate-sum-one hyperplane.

Its seven nonempty subfamilies have exactly six nonempty intersections. Every pair meets, while the triple does not. The three possible minimum-lift root certificates have lower bounds 4425/1024, 4233/1024, and 4425/1024 against upper bound 3/2. The certificates are recomputed from the complete orders and exponential vectors, rather than trusted as stored numerical verdicts.

## The four-leaf star

The entry star_4 gives five vertices, four edges, three complete orders, all four edge witnesses, and every hull. Its central object has four extreme points. All 31 nonempty subfamilies are tested, with exactly nine faces; its six minimal nonfaces are missing pairs of leaves. Their twelve root certificates are all supplied.

This example shows a limitation of the particular coordinate hull construction. It does not obstruct another triangle or segment representation of the same hypergraph. The existing exposed-star arguments and the complete coordinate proof explain that distinction.

## A two-level attachment to the nonplanar core

The entry nonplanar_two_level_attachment starts with the five-vertex, six-edge example credited to the triangle-representation chapter and adds edges g={1,6}, h={6,7}. It supplies all eight edges, all fifteen poset elements in each of three orders, and exact coordinates of all seven nondegenerate triangles. The first five objects use the displayed inflation formula with eta=1/1000. The remaining two triangles are the explicit rational graft described in the core proof.

All 127 nonempty subfamilies are checked against the complete downward closure, yielding 21 faces and precisely eight maximal edges. All 210 ordered distinct pairs verify the incidence realizer. The induced S3 on vertex labels 1,2,3 and edge labels a,b,e proves dimension at least three. The original incidence graph is retained as a subgraph, so its K3,3 subdivision from the preserved second edition proves nonplanarity.

Vertex 1 has degree four, while the core's vertex degrees are 3,3,3,3,2. Object 7 misses object 1; a grandparent incidence is not silently introduced. The core example lies inside the sufficient theorem, whose bound is on degrees remaining inside the 2-core rather than on the original vertex degrees.

## What is and is not established by these checks

The edition's exact checker recomputes all 312 ordered incidence-poset pairs and all 165 nonempty geometric subfamilies across these three examples, every stored coordinate and minimum-lift certificate, the four extreme central witnesses, inflation coordinates, nondegeneracy, and the core identity. Duplicate JSON keys, malformed scalar types, nonfinite values, unknown fields, and changed mathematical data are rejected explicitly. The general full-nerve theorem and all-parameter core theorem rest on the complete written proofs, not on these finite tests.
