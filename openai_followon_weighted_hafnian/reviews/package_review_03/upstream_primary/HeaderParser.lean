import Lean

open Lean

def main (args : List String) : IO Unit := do
  let mut count := 0
  let mut failures := 0
  for path in args do
    let text ← IO.FS.readFile path
    let (_, _, messages) ← Parser.parseHeader (Parser.mkInputContext text path)
    count := count + 1
    if messages.hasErrors then
      failures := failures + 1
      IO.println s!"FAIL {path}"
      for message in messages.toList do
        IO.println (← message.toString)
  IO.println s!"headers={count}; failures={failures}"
