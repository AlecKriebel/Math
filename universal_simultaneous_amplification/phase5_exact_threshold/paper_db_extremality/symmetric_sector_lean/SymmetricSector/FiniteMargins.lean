import SymmetricSector.GeneratedMargins.All
import SymmetricSector.GeneratedMargins.Exact40
import Mathlib.Tactic.IntervalCases

namespace SymmetricSector
open GeneratedMargins

/-- All later finite orders have margin at least one hundredth. -/
theorem later_finite_phase_bound {N : ℕ} (hlo : 41 ≤ N) (hhi : N ≤ 287) :
    beta N + epsilon N ≤ 1 - (1 / 100 : ℚ) := by
  interval_cases N
  · exact bound41
  · exact bound42
  · exact bound43
  · exact bound44
  · exact bound45
  · exact bound46
  · exact bound47
  · exact bound48
  · exact bound49
  · exact bound50
  · exact bound51
  · exact bound52
  · exact bound53
  · exact bound54
  · exact bound55
  · exact bound56
  · exact bound57
  · exact bound58
  · exact bound59
  · exact bound60
  · exact bound61
  · exact bound62
  · exact bound63
  · exact bound64
  · exact bound65
  · exact bound66
  · exact bound67
  · exact bound68
  · exact bound69
  · exact bound70
  · exact bound71
  · exact bound72
  · exact bound73
  · exact bound74
  · exact bound75
  · exact bound76
  · exact bound77
  · exact bound78
  · exact bound79
  · exact bound80
  · exact bound81
  · exact bound82
  · exact bound83
  · exact bound84
  · exact bound85
  · exact bound86
  · exact bound87
  · exact bound88
  · exact bound89
  · exact bound90
  · exact bound91
  · exact bound92
  · exact bound93
  · exact bound94
  · exact bound95
  · exact bound96
  · exact bound97
  · exact bound98
  · exact bound99
  · exact bound100
  · exact bound101
  · exact bound102
  · exact bound103
  · exact bound104
  · exact bound105
  · exact bound106
  · exact bound107
  · exact bound108
  · exact bound109
  · exact bound110
  · exact bound111
  · exact bound112
  · exact bound113
  · exact bound114
  · exact bound115
  · exact bound116
  · exact bound117
  · exact bound118
  · exact bound119
  · exact bound120
  · exact bound121
  · exact bound122
  · exact bound123
  · exact bound124
  · exact bound125
  · exact bound126
  · exact bound127
  · exact bound128
  · exact bound129
  · exact bound130
  · exact bound131
  · exact bound132
  · exact bound133
  · exact bound134
  · exact bound135
  · exact bound136
  · exact bound137
  · exact bound138
  · exact bound139
  · exact bound140
  · exact bound141
  · exact bound142
  · exact bound143
  · exact bound144
  · exact bound145
  · exact bound146
  · exact bound147
  · exact bound148
  · exact bound149
  · exact bound150
  · exact bound151
  · exact bound152
  · exact bound153
  · exact bound154
  · exact bound155
  · exact bound156
  · exact bound157
  · exact bound158
  · exact bound159
  · exact bound160
  · exact bound161
  · exact bound162
  · exact bound163
  · exact bound164
  · exact bound165
  · exact bound166
  · exact bound167
  · exact bound168
  · exact bound169
  · exact bound170
  · exact bound171
  · exact bound172
  · exact bound173
  · exact bound174
  · exact bound175
  · exact bound176
  · exact bound177
  · exact bound178
  · exact bound179
  · exact bound180
  · exact bound181
  · exact bound182
  · exact bound183
  · exact bound184
  · exact bound185
  · exact bound186
  · exact bound187
  · exact bound188
  · exact bound189
  · exact bound190
  · exact bound191
  · exact bound192
  · exact bound193
  · exact bound194
  · exact bound195
  · exact bound196
  · exact bound197
  · exact bound198
  · exact bound199
  · exact bound200
  · exact bound201
  · exact bound202
  · exact bound203
  · exact bound204
  · exact bound205
  · exact bound206
  · exact bound207
  · exact bound208
  · exact bound209
  · exact bound210
  · exact bound211
  · exact bound212
  · exact bound213
  · exact bound214
  · exact bound215
  · exact bound216
  · exact bound217
  · exact bound218
  · exact bound219
  · exact bound220
  · exact bound221
  · exact bound222
  · exact bound223
  · exact bound224
  · exact bound225
  · exact bound226
  · exact bound227
  · exact bound228
  · exact bound229
  · exact bound230
  · exact bound231
  · exact bound232
  · exact bound233
  · exact bound234
  · exact bound235
  · exact bound236
  · exact bound237
  · exact bound238
  · exact bound239
  · exact bound240
  · exact bound241
  · exact bound242
  · exact bound243
  · exact bound244
  · exact bound245
  · exact bound246
  · exact bound247
  · exact bound248
  · exact bound249
  · exact bound250
  · exact bound251
  · exact bound252
  · exact bound253
  · exact bound254
  · exact bound255
  · exact bound256
  · exact bound257
  · exact bound258
  · exact bound259
  · exact bound260
  · exact bound261
  · exact bound262
  · exact bound263
  · exact bound264
  · exact bound265
  · exact bound266
  · exact bound267
  · exact bound268
  · exact bound269
  · exact bound270
  · exact bound271
  · exact bound272
  · exact bound273
  · exact bound274
  · exact bound275
  · exact bound276
  · exact bound277
  · exact bound278
  · exact bound279
  · exact bound280
  · exact bound281
  · exact bound282
  · exact bound283
  · exact bound284
  · exact bound285
  · exact bound286
  · exact bound287

/-- The full quantified second part of Appendix A's finite lemma. -/
theorem finite_phase_positive {N : ℕ} (hlo : 40 ≤ N) (hhi : N ≤ 287) :
    beta N + epsilon N < 1 := by
  by_cases h : N = 40
  · subst N
    have hb := bound40
    linarith
  · have hb := later_finite_phase_bound (by omega : 41 ≤ N) hhi
    linarith

/-- The printed exact N=40 margin is the minimum over all 248 finite orders. -/
theorem finite_minimum_margin {N : ℕ} (hlo : 40 ≤ N) (hhi : N ≤ 287) :
    (639304267467075678841 / 115369588296792467144716 : ℚ) ≤
      1 - beta N - epsilon N := by
  by_cases h : N = 40
  · subst N
    rw [exact_margin_40]
  · have hb := later_finite_phase_bound (by omega : 41 ≤ N) hhi
    linarith

/-- The minimum is attained only at the stated endpoint. -/
theorem finite_minimum_margin_strict {N : ℕ} (hlo : 41 ≤ N) (hhi : N ≤ 287) :
    (639304267467075678841 / 115369588296792467144716 : ℚ) <
      1 - beta N - epsilon N := by
  have hb := later_finite_phase_bound hlo hhi
  linarith

end SymmetricSector
