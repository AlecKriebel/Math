import CyclicBell.D4
-- INTENTIONALLY FALSE. A doubled state amplitude cannot remain normalized.
example : CyclicBell.ip (fun i => 2 * CyclicBell.D4.phi i)
    (fun i => 2 * CyclicBell.D4.phi i) = 1 := by
  norm_num [CyclicBell.ip, CyclicBell.D4.phi, Fintype.sum_prod_type, Fin.sum_univ_succ]
