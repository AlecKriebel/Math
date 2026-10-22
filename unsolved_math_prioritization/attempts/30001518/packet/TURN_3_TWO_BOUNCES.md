# Turn 3: rigidity of two-reflection branches

The third substantive approach tried to classify short retroreflecting itineraries and then rule out a body assembled from them. The classification below is local. The assembly and arbitrary-reflection-count problem remains unresolved.

## Proposition

In a planar billiard, suppose an open two-dimensional set of rays follows a regular itinerary with exactly two distinct, transverse collisions on C² mirror arcs. If every ray in this set exits with velocity opposite its incoming velocity, then, near each such trajectory, both struck mirror arcs are straight and perpendicular. The converse direction statement holds for any itinerary which actually strikes two perpendicular straight mirrors in sequence.

## Proof

Let R_i denote reflection in the tangent line at collision i. For incoming unit velocity v, outgoing velocity is R₂R₁v. The matrix R₂R₁ is a planar rotation. A planar rotation sends one nonzero vector to its negative if and only if the rotation is −Id. Thus retroreflection forces the two tangent lines to be perpendicular.

It remains to justify that the two collision points can vary independently. Parametrize the arcs regularly as q₁(s),q₂(t). The intermediate unit vector is

    u(s,t)=(q₂(t)−q₁(s))/|q₂(t)−q₁(s)|.

At the given trajectory its derivative in angular coordinate with respect to t is

    det(u,q₂′(t))/|q₂(t)−q₁(s)|,

which is nonzero by transversality of collision 2. Thus (s,t) are local coordinates for the position-and-angle data immediately after collision 1, and, by reflecting in its tangent, for incoming ray data as well. Regularity and strict clearance preserve the two-collision itinerary in a small product rectangle J₁×J₂ of endpoint parameters.

Writing the continuous tangent angles as θ₁(s),θ₂(t), one has

    θ₂(t)−θ₁(s)=π/2 mod π

throughout that product rectangle. Fixing t makes θ₁ constant; fixing s makes θ₂ constant. A regular C¹ arc with constant tangent line lies in a straight line. The lines are perpendicular. Conversely the product of reflections in perpendicular lines has linear part −Id, which reverses every direction of any valid two-bounce trajectory. ∎

## Almost-everywhere formulation

If a body were perfect in the source's almost-everywhere sense, the outgoing direction is continuous on any open regular two-reflection itinerary chart. A full-flux-measure identity on that chart therefore holds everywhere on it: a point of failure would have a neighborhood of failure and positive flux. The proposition applies to every such chart. This does not assert that all incidence data lie in two-reflection charts, or that positive measure alone produces an open chart for an arbitrary prescribed exceptional subset.

## Obstruction encountered

The direction algebra is not an impossibility proof: a pair of perpendicular mirrors really does reverse directions on an open set. Finite apertures leave other incidence data following different itineraries. The proposition does not eliminate three or more curved reflections, infinitely many combinatorial branches, or general singular accumulation. A classification of two bounces is consequently insufficient for the original existence question.
