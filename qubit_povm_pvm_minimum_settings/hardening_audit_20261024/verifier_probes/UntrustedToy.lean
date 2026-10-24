/- Adversarial verifier fixture only. Deliberately invalid serialized theorem.
   Never import this module into production mathematics. -/
import Lean
open Lean Elab Command
run_elab do
  let decl := Declaration.thmDecl {
    name := `AdversarialFixture.invalid
    levelParams := []
    type := mkConst ``False
    value := mkConst ``True.intro }
  match (← getEnv).addDeclCore 0 decl none (doCheck := false) with
  | .ok env => setEnv env
  | .error ex => throwError "fixture setup failed: {ex.toMessageData {}}"
