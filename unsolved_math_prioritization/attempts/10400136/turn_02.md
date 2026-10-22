# Attempt 2: roots on parameter spaces and a canonical-cover test

## Mechanism

The original invariant is K_N = H_N^N. We tried to construct the desired refinement by choosing an Nth root continuously or algebraically as the flat bundle varies. This is a distinct analytic/topological route, requiring no tetrahedral move calculations.

## Exact root criterion

Let X be a connected, locally path-connected and semilocally simply connected space, and let K:X→C* be continuous. Fix x_0 in X and a number h_0 with h_0^N=K(x_0). A continuous function h:X→C* satisfying h^N=K and h(x_0)=h_0 exists exactly when

    wind(K∘γ) ∈ N Z

for every loop γ based at x_0. Here wind is the winding number about zero.

Proof: if h exists, the winding number of h^N around every loop is N times that of h. Conversely, lift K through the covering p:C*→C*, p(z)=z^N, starting at h_0. The path-lifting endpoint is independent of the chosen path precisely when every loop maps into p_*(π_1(C*))=N Z. This defines the desired continuous lift. On a complex manifold with holomorphic K, local holomorphic roots exist; their ratio with the continuous lift takes values in discrete μ_N and is locally constant, so the lift is holomorphic. The same argument applies componentwise to a suitable smooth locus.

In particular, there is no continuous universal root-selection map s:C*→C* with s(z)^N=z: the unit circle has winding number one. Passing to the d-fold cover z=t^d gives a root exactly when N divides d, because the generator now has winding d. For odd N>1, no cover in this one-loop example whose degree is a power of two cures a primitive μ_N monodromy. This does not rule out a spin or framing refinement of the actual QHI, whose transformation law is additional input; it only rules out curing arbitrary odd-order monodromy by parity information alone.

For a nonzero element K of a complex function field F, a rational root exists exactly when its class in F*/(F*)^N vanishes. Divisibility by N of every divisor order is necessary, but without further assumptions is not enough to assert a rational root. We use only the exact field criterion, not such an implication.

## What the tautological cover does and does not solve

For any nonvanishing K, the space

    E_K = {(x,t): t^N=K(x)}

is an N-sheeted cover of X and carries the tautological root t. That construction is automatic for every invariant K and contains no new phase information. It merely repackages the choice of the desired answer as extra data. The original problem seeks an explanation in terms of independently meaningful structures on the geometric triple; we have not identified E_K with such a space.

The cover must also be restricted to K≠0. If K=0, every state-sum representative has value zero, ratios cannot be used, and t^N=K is no longer an unramified N-sheeted cover at that point. No nonvanishing theorem for the original state sum is assumed.

## Outcome

This gives an exact, testable obstruction: compute the monodromy homomorphism of the actual K_N on an appropriate representation-parameter space, then identify a geometrically defined lift killing it. We have neither computed that homomorphism in the full closed-triple setting nor established its vanishing. The finite covers in the analytic-family literature do not supply that conclusion just by their degree; their stated invariants still have a μ_N ambiguity after the sign correction.

**Result:** a conditional root-lifting criterion and a proved failure of universal root selection; no claim that an obstructing loop has been realized by the original QHI.
