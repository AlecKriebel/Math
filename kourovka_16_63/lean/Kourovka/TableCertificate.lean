/- Exact comparison of the original transvectant formula with the exported integer
   table. Finite comparisons are split by their first index to bound kernel
   reduction memory. Every comparison uses ordinary kernel reduction. -/
import Kourovka.RawCoefficients
import Kourovka.ExportedData

namespace Kourovka
namespace TableCertificate

def row (i : Nat) : List (Nat × Nat × Nat × Int) :=
  (List.range 31).flatMap fun j =>
    if i < j then
      (List.range 31).flatMap fun k =>
        let c := Raw.coefficient i j k
        if c = 0 then [] else [(i, j, k, c)]
    else []

set_option Elab.async false
set_option maxRecDepth 20000
set_option maxHeartbeats 8000000

theorem row_0 : row 0 = [(0, 1, 1, 2), (0, 2, 2, -2), (0, 3, 3, 6), (0, 4, 4, 4), (0, 5, 5, 2), (0, 7, 7, -2), (0, 8, 8, -4), (0, 9, 9, -6), (0, 10, 10, 4), (0, 11, 11, 2), (0, 13, 13, -2), (0, 14, 14, -4), (0, 15, 15, 6), (0, 16, 16, 4), (0, 17, 17, 2), (0, 19, 19, -2), (0, 20, 20, -4), (0, 21, 21, -6), (0, 22, 22, 2), (0, 24, 24, -2), (0, 25, 25, 4), (0, 26, 26, 2), (0, 28, 28, -2), (0, 29, 29, -4)] := by
  decide +kernel

theorem row_1 : row 1 = [(1, 2, 0, 1), (1, 4, 3, 1), (1, 5, 4, 2), (1, 6, 5, 3), (1, 7, 6, 4), (1, 8, 7, 5), (1, 9, 8, 6), (1, 11, 10, 1), (1, 12, 11, 2), (1, 13, 12, 3), (1, 14, 13, 4), (1, 16, 15, 1), (1, 17, 16, 2), (1, 18, 17, 3), (1, 19, 18, 4), (1, 20, 19, 5), (1, 21, 20, 6), (1, 23, 22, 1), (1, 24, 23, 2), (1, 26, 25, 1), (1, 27, 26, 2), (1, 28, 27, 3), (1, 29, 28, 4)] := by
  decide +kernel

theorem row_2 : row 2 = [(2, 3, 4, 6), (2, 4, 5, 5), (2, 5, 6, 4), (2, 6, 7, 3), (2, 7, 8, 2), (2, 8, 9, 1), (2, 10, 11, 4), (2, 11, 12, 3), (2, 12, 13, 2), (2, 13, 14, 1), (2, 15, 16, 6), (2, 16, 17, 5), (2, 17, 18, 4), (2, 18, 19, 3), (2, 19, 20, 2), (2, 20, 21, 1), (2, 22, 23, 2), (2, 23, 24, 1), (2, 25, 26, 4), (2, 26, 27, 3), (2, 27, 28, 2), (2, 28, 29, 1)] := by
  decide +kernel

theorem row_3 : row 3 = [(3, 6, 15, 720), (3, 7, 16, 2880), (3, 8, 17, 7200), (3, 9, 18, 14400), (3, 14, 22, 8640), (3, 20, 22, 86400), (3, 21, 23, 518400), (3, 29, 22, 8640)] := by
  decide +kernel

theorem row_4 : row 4 = [(4, 5, 15, -480), (4, 6, 16, -720), (4, 8, 18, 2400), (4, 9, 19, 7200), (4, 13, 22, -1440), (4, 14, 23, 2880), (4, 19, 22, -28800), (4, 20, 23, -57600), (4, 21, 24, 86400), (4, 28, 22, -1440), (4, 29, 23, 2880)] := by
  decide +kernel

theorem row_5 : row 5 = [(5, 6, 17, -720), (5, 7, 18, -960), (5, 9, 20, 2880), (5, 12, 22, 576), (5, 13, 23, -1152), (5, 14, 24, 576), (5, 18, 22, 17280), (5, 19, 23, 11520), (5, 20, 24, -28800), (5, 27, 22, 576), (5, 28, 23, -1152), (5, 29, 24, 576)] := by
  decide +kernel

theorem row_6 : row 6 = [(6, 7, 19, -720), (6, 8, 20, -720), (6, 9, 21, 720), (6, 11, 22, -432), (6, 12, 23, 864), (6, 13, 24, -432), (6, 17, 22, -17280), (6, 19, 24, 17280), (6, 26, 22, -432), (6, 27, 23, 864), (6, 28, 24, -432)] := by
  decide +kernel

theorem row_7 : row 7 = [(7, 8, 21, -480), (7, 10, 22, 576), (7, 11, 23, -1152), (7, 12, 24, 576), (7, 16, 22, 28800), (7, 17, 23, -11520), (7, 18, 24, -17280), (7, 25, 22, 576), (7, 26, 23, -1152), (7, 27, 24, 576)] := by
  decide +kernel

theorem row_8 : row 8 = [(8, 10, 23, 2880), (8, 11, 24, -1440), (8, 15, 22, -86400), (8, 16, 23, 57600), (8, 17, 24, 28800), (8, 25, 23, 2880), (8, 26, 24, -1440)] := by
  decide +kernel

theorem row_9 : row 9 = [(9, 10, 24, 8640), (9, 15, 23, -518400), (9, 16, 24, -86400), (9, 25, 24, 8640)] := by
  decide +kernel

theorem row_10 : row 10 = [(10, 13, 22, 144), (10, 14, 23, 576), (10, 29, 30, 576)] := by
  decide +kernel

theorem row_11 : row 11 = [(11, 12, 22, -72), (11, 13, 23, -72), (11, 14, 24, 144), (11, 28, 30, -144)] := by
  decide +kernel

theorem row_12 : row 12 = [(12, 13, 24, -72), (12, 27, 30, 96)] := by
  decide +kernel

theorem row_13 : row 13 = [(13, 26, 30, -144)] := by
  decide +kernel

theorem row_14 : row 14 = [(14, 25, 30, 576)] := by
  decide +kernel

theorem row_15 : row 15 = [] := by
  decide +kernel

theorem row_16 : row 16 = [] := by
  decide +kernel

theorem row_17 : row 17 = [] := by
  decide +kernel

theorem row_18 : row 18 = [] := by
  decide +kernel

theorem row_19 : row 19 = [] := by
  decide +kernel

theorem row_20 : row 20 = [] := by
  decide +kernel

theorem row_21 : row 21 = [] := by
  decide +kernel

theorem row_22 : row 22 = [] := by
  decide +kernel

theorem row_23 : row 23 = [] := by
  decide +kernel

theorem row_24 : row 24 = [] := by
  decide +kernel

theorem row_25 : row 25 = [(25, 28, 22, 144), (25, 29, 23, 576)] := by
  decide +kernel

theorem row_26 : row 26 = [(26, 27, 22, -72), (26, 28, 23, -72), (26, 29, 24, 144)] := by
  decide +kernel

theorem row_27 : row 27 = [(27, 28, 24, -72)] := by
  decide +kernel

theorem row_28 : row 28 = [] := by
  decide +kernel

theorem row_29 : row 29 = [] := by
  decide +kernel

theorem row_30 : row 30 = [] := by
  decide +kernel

end TableCertificate

theorem raw_table_matches_exported : Raw.reconstructedTerms = exportedTerms := by
  change (List.range 31).flatMap TableCertificate.row = exportedTerms
  rw [show List.range 31 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30] from by decide]
  simp only [List.flatMap_cons, List.flatMap_nil, TableCertificate.row_0, TableCertificate.row_1, TableCertificate.row_2, TableCertificate.row_3, TableCertificate.row_4, TableCertificate.row_5, TableCertificate.row_6, TableCertificate.row_7, TableCertificate.row_8, TableCertificate.row_9, TableCertificate.row_10, TableCertificate.row_11, TableCertificate.row_12, TableCertificate.row_13, TableCertificate.row_14, TableCertificate.row_15, TableCertificate.row_16, TableCertificate.row_17, TableCertificate.row_18, TableCertificate.row_19, TableCertificate.row_20, TableCertificate.row_21, TableCertificate.row_22, TableCertificate.row_23, TableCertificate.row_24, TableCertificate.row_25, TableCertificate.row_26, TableCertificate.row_27, TableCertificate.row_28, TableCertificate.row_29, TableCertificate.row_30]
  rfl

end Kourovka
