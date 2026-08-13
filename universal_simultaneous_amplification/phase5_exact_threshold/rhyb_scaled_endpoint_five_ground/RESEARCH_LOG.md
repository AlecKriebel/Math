# Research log: scaled endpoint five-ground reduction

## 2026-08-13 — corrected endpoint reduction and route obstruction

- Corrected the first-orbit input to `X=(r-1)q`, which is baseline matched
  at every fitness.  Derived the exact resolvent

  ```text
  h-h1 = r h h1 R(X-s),       h1=(1+rRX)^(-1).
  ```

- Added the scaled fifth ground `w=aX`; its potential is unchanged by the
  scalar factor and equals `V_w=Rq/q`.  The exact target density is

  ```text
  e=a(h-h1)=a r h h1 (X V_w-s V_v),   V_v=1/(rh).
  ```

- Generalized the complete ten-pair cut-Picone/Farkas reduction to arbitrary
  `r` with this corrected scaling.  The unresolved theorem is a target-sign
  consequence of all ten simultaneous linked ground orders, not a new fixed
  point or kernel search.

- The ten total-order equations cannot finish by uniqueness: for `n>=12`
  their matrix has nullity at least two and contains the physical measure.
  Whenever its proper cut inequalities are strict, small nonphysical
  nullspace perturbations preserve every order.  This does not give the
  negative target average needed to refute the full cone.

- Proved an exact obstruction to a potential-only use of the `(w,v)` order.
  On the exact local potential surface `V_w=V_v=1/[r(1-s)]`, every `(w,v)`
  correction vanishes, while for `0<X<s<1`,

  ```text
  e/a=(1-s)(X-s)/(1-s+X)<0.
  ```

  Thus no unconditional one-order pointwise Picone multiplier can close the
  endpoint inequality from only these local data.  This does not claim that
  the one-node specialization is a full physical kernel, and does not refute
  the full ten-order cone or the physical inequality.

- No graph or kernel search was performed.  The exact replay checks every
  displayed algebraic identity and a rational-in-fitness obstruction member.

- Best-guess completion: **100% for the assigned exact five-ground/Farkas
  reduction and single-order audit; roughly 55% for the diffuse-support
  branch** after the separate upper-sandwich theorem.  The remaining lower
  endpoint inequality is still the substantive gap.
