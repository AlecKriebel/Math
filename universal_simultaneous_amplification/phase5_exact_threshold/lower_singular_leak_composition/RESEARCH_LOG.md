# Research log: singular leak composition

## 2026-08-13 -- exact tensor law and serial saturation obstruction

- Started from the undirected-realizable three-type singular leak family
  whose normalized diffuse branching response is

  ```text
  (Bd gain, dB cost) proportional to (1, r-1).
  ```

- Derived the exact zero-temperature root formulas

  ```text
  b_i = r(Pb)_i/[t_i+r(Pb)_i],
  s_i = r(Rs)_i/[1+r(Rs)_i] <= r t_i/(1+r t_i).
  ```

  Hence every repeated singular root with `t_i/(Pb)_i -> 0` saturates to
  `(b_i,s_i)->(1,0)`, independently of the downstream response amplitude.
  A serial outer stage therefore resets to the same ray rather than
  multiplying its two coordinates.
- Strengthened the local statement: for every cold root `t_i->0`, one has
  `s_i->0`; if its Bd endpoint tends to any `b_i->b>p_0`, then

  ```text
  cost/gain - (r-1) = (r-1)(1-b)/(b-p_0) >= 0.
  ```

  Thus even a cold crossover with `t_i/(Pb)_i` of order one cannot improve
  the singular ray.  Equality requires full Bd saturation `b=1`.
- For the literal Kronecker/tensor composition, proved the exact singular
  polarization law.  If one factor has polarized mass `c`, depth `L` has

  ```text
  q_L=1-(1-c)^L,
  beta_L=(r-1)/r+q_L/r,
  sigma_L=(r-1)/r-(r-1)q_L/r.
  ```

  Thus the dB-cost/Bd-gain ratio is exactly `r-1` for every depth.  At the
  tangent scale, `q_L=Lc+O(L^2 c^2)`, so fixed-depth responses add rather
  than multiply.
- More generally, tensor composition of two singular polarized profiles
  has `q_12=q_1+q_2-q_1q_2`.  This is an idempotent union law on the
  polarized mass, not the hoped-for diagonal map `(G,D)->(G,(r-1)D)`.
- On `I_k=[1+1/k,2-1/k]`, the actual worst cost/gain remains `1-1/k` at
  every depth, whereas the conjectural powered ratio would be at most
  `(1-1/k)^L`.  Taking `L_k>>k` therefore does not help this composition.
- **PROVED FOR THE STATED COMPOSITIONS:** independent tensor products and
  serial/hierarchical cascades whose gain is carried by repeated cold roots
  cannot turn `(1,r-1)` into `(1,(r-1)^L)`.
- **NOT A UNIVERSAL LOWER OBSTRUCTION:** a gain-carrying layer with
  nonvanishing temperature, a same-scale compensating type, or non-diffuse
  collisions leaves the cold-root composition class.  Those are the exact
  remaining escape mechanisms.
- Best-guess completion of the full exact-threshold problem: **70%**.  This
  closes the most direct depth-amplification interpretation of the new ray
  but does not construct the missing lower diagonal.
