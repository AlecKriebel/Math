import SymmetricSector.Margins

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector

theorem exact_margin_40 : 1 - beta 40 - epsilon 40 =
    (639304267467075678841 / 115369588296792467144716 : ℚ) := by
  decide +kernel

end SymmetricSector
