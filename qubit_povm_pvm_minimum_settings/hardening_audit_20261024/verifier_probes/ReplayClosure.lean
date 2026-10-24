/- Standalone verifier experiment. Does not add a project theorem or axiom.
   Rechecks a complete serialized proof dependency closure in an empty kernel environment. -/
import Lean.Replay
import Lean.Util.Path
open Lean

deriving instance BEq for InductiveVal, QuotKind, QuotVal, ConstantInfo

def collect (env trusted : Environment) (todo : List Name) : IO (Std.HashMap Name ConstantInfo) := do
  let mut pending := todo
  let mut found : Std.HashMap Name ConstantInfo := {}
  while !pending.isEmpty do
    let name := pending.head!
    pending := pending.tail!
    unless found.contains name do
      let some ci := env.find? name | throw <| IO.userError s!"Missing dependency {name}"
      if ci.isUnsafe || ci.isPartial then
        throw <| IO.userError s!"Unsafe/partial proof dependency {name}"
      if let .axiomInfo _ := ci then
        unless name == ``propext || name == ``Classical.choice || name == ``Quot.sound do
          throw <| IO.userError s!"Unexpected axiom {name}"
        let some expected := trusted.find? name | throw <| IO.userError s!"Missing trusted axiom {name}"
        unless ci.type == expected.type && ci.levelParams == expected.levelParams do
          throw <| IO.userError s!"Standard axiom signature mismatch: {name}"
      if let some expected := trusted.find? name then
        unless ci == expected do
          throw <| IO.userError s!"Trusted Init declaration differs: {name}"
      let mut dependencies := ci.getUsedConstantsAsSet.toList
      if let .inductInfo info := ci then
        dependencies := info.all ++ info.ctors ++ dependencies
      if let .ctorInfo info := ci then
        dependencies := info.induct :: dependencies
      pending := dependencies ++ pending
      found := found.insert name ci
  return found

def replayEndpoints (env trusted : Environment) (endpoints : List Name) (inventory : Option System.FilePath := none) (doReplay : Bool := true) : IO Nat := do
  for endpoint in endpoints do
    unless (env.find? endpoint).any (fun ci => match ci with | .thmInfo _ => true | _ => false) do
      throw <| IO.userError s!"Required theorem absent: {endpoint}"
  let closure ← collect env trusted endpoints
  IO.println s!"CLOSURE constants={closure.size}"
  (← IO.getStdout).flush
  if let some path := inventory then
    let mut modules : NameSet := {}
    for (name, _) in closure.toList do
      if let some idx := env.getModuleIdxFor? name then
        modules := modules.insert env.header.moduleNames[idx]!
    let paths ← modules.toList.mapM fun name => do
      pure <| Json.mkObj [("module", toJson name.toString), ("olean", toJson (← findOLean name).toString)]
    IO.FS.writeFile path (Json.mkObj [
      ("constants", toJson (closure.toList.map fun (name, _) => name.toString)),
      ("modules", toJson paths)] |>.pretty)
  for (name, ci) in closure.toList do
    if let .axiomInfo _ := ci then IO.println s!"AXIOM {name}"
  if !doReplay then return closure.size
  -- Imported module indices are dependency ordered. Reset only frontend async
  -- bookkeeping between modules: private user-name suffixes may repeat across
  -- modules, while all original fully qualified kernel names remain intact.
  let mut groups : Array (Std.HashMap Name ConstantInfo) :=
    Array.replicate (env.header.moduleNames.size + 1) {}
  for (name, ci) in closure.toList do
    let idx := (env.getModuleIdxFor? name).map ModuleIdx.toNat |>.getD env.header.moduleNames.size
    groups := groups.modify idx (fun group => group.insert name ci)
  let mut checked ← mkEmptyEnvironment 0
  let mut moduleCount := 0
  for group in groups do
    unless group.isEmpty do
      for (name, ci) in group.toList do
        for dependency in ci.getUsedConstantsAsSet do
          unless group.contains dependency || (checked.find? dependency).isSome do
            throw <| IO.userError s!"Dependency not yet replayed: {name} -> {dependency}"
        if let .inductInfo info := ci then
          for companion in info.all ++ info.ctors do
            unless group.contains companion do
              throw <| IO.userError s!"Inductive block crosses replay groups: {name} -> {companion}"
      checked ← checked.replay group
      checked := Environment.ofKernelEnv checked.toKernelEnv
      moduleCount := moduleCount + 1
      if moduleCount % 100 == 0 then
        IO.println s!"MODULES_REPLAYED {moduleCount}"
        (← IO.getStdout).flush
  IO.println s!"REPLAY_MODULES {moduleCount}"
  for (name, expected) in closure.toList do
    let some actual := checked.find? name | throw <| IO.userError s!"Replay omitted dependency {name}"
    unless actual == expected do
      throw <| IO.userError s!"Replayed dependency differs: {name}"
  for endpoint in endpoints do
    let some expected := env.find? endpoint | throw <| IO.userError s!"Missing input endpoint {endpoint}"
    let some actual := checked.find? endpoint | throw <| IO.userError s!"Replay omitted endpoint {endpoint}"
    unless actual == expected do
      throw <| IO.userError s!"Replayed endpoint differs: {endpoint}"
    IO.println s!"REPLAYED {endpoint}"
  return closure.size

def runChecks (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  let trusted ← importModules #[{ module := `Init }] {} 0 (loadExts := false)
  let mode := args.headD "controls"
  if mode == "main" || mode == "inventory" then
    let env ← importModules #[{ module := `Bell }] {} 0 (loadExts := false)
    let endpoints := [`Bell.two_input_convex_equality,
      `Bell.HilbertFiniteLabels.at_most_two_input_equality,
      `Bell.HilbertFiniteLabels.finite_source_projective_simulation]
    let count ← replayEndpoints env trusted endpoints (args[1]?.map System.FilePath.mk) (mode == "main")
    if mode == "main" then
      IO.println s!"PASS main-endpoint empty-environment replay; {count} declarations checked"
    else
      IO.println s!"PASS dependency inventory only; {count} declarations; no replay performed"
  else if mode == "controls" then
    let env ← importModules #[{ module := `Init }] {} 0 (loadExts := false)
    let positive : Declaration := .thmDecl {
      name := `ReplayFixture.valid, levelParams := [],
      type := mkConst ``True, value := mkConst ``True.intro }
    let valid ← match env.addDeclCore 0 positive none with
      | .ok e => pure e
      | .error e => throw <| IO.userError (← e.toMessageData {} |>.toString)
    let _ ← replayEndpoints valid trusted [`ReplayFixture.valid]
    IO.println "CONTROL valid accepted"
    let malformed : Declaration := .thmDecl {
      name := `ReplayFixture.invalid, levelParams := [],
      type := mkConst ``False, value := mkConst ``True.intro }
    let invalid ← match env.addDeclCore 0 malformed none (doCheck := false) with
      | .ok e => pure e
      | .error e => throw <| IO.userError (← e.toMessageData {} |>.toString)
    let rejected ← try
      let _ ← replayEndpoints invalid trusted [`ReplayFixture.invalid]
      pure false
    catch err =>
      let message := err.toString
      unless (message.splitOn "type mismatch").length > 1 do throw err
      IO.println s!"CONTROL malformed proof rejected: {message}"
      pure true
    unless rejected do throw <| IO.userError "INVALID PROOF ACCEPTED"
    let blank ← mkEmptyEnvironment 0
    let falseEnv ← blank.replay (← collect trusted trusted [``False])
    let retyped : Declaration := .axiomDecl {
      name := ``propext, levelParams := [], type := mkConst ``False, isUnsafe := false }
    let changed ← match falseEnv.addDeclCore 0 retyped none with
      | .ok e => pure e
      | .error e => throw <| IO.userError (← e.toMessageData {} |>.toString)
    let client : Declaration := .thmDecl {
      name := `ReplayFixture.retypedClient, levelParams := [],
      type := mkConst ``False, value := mkConst ``propext }
    let changed ← match changed.addDeclCore 0 client none with
      | .ok e => pure e
      | .error e => throw <| IO.userError (← e.toMessageData {} |>.toString)
    let retypedRejected ← try
      let _ ← replayEndpoints changed trusted [`ReplayFixture.retypedClient]
      pure false
    catch err =>
      unless (err.toString.splitOn "Standard axiom signature mismatch").length > 1 do throw err
      IO.println s!"CONTROL retyped standard axiom rejected: {err}"
      pure true
    unless retypedRejected do throw <| IO.userError "RETYPED STANDARD AXIOM ACCEPTED"
    let blank ← mkEmptyEnvironment 0
    let changedTrue : Declaration := .inductDecl [] 0 [
      { name := ``True, type := mkSort .zero, ctors := [] }] false
    let changedCore ← match blank.addDeclCore 0 changedTrue none with
      | .ok e => pure e
      | .error e => throw <| IO.userError (← e.toMessageData {} |>.toString)
    let coreRejected ← try
      let _ ← collect changedCore trusted [``True]
      pure false
    catch err =>
      unless (err.toString.splitOn "Trusted Init declaration differs").length > 1 do throw err
      IO.println s!"CONTROL changed core inductive rejected: {err}"
      pure true
    unless coreRejected do throw <| IO.userError "CHANGED CORE INDUCTIVE ACCEPTED"
    IO.println "PASS positive, malformed-proof, retyped-axiom, and changed-core controls"
  else
    throw <| IO.userError "Expected controls, inventory, or main"

-- --run otherwise executes on the OS main thread, whose stack is not enlarged
-- by Lean's -s option. A dedicated Lean worker uses the explicitly sized stack.
def main (args : List String) : IO Unit := do
  let task ← IO.asTask (runChecks args) Task.Priority.dedicated
  IO.ofExcept task.get
