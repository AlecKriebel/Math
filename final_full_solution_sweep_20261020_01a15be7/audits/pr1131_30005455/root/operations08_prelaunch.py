"""Root entry guard for the exact operations08 package; no authority is granted here."""
from pathlib import Path
import argparse,hashlib,json,stat,sys,types
SOURCE=Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations08/source")
MANIFEST_SHA="3d4d250e56a5ce25c5a7365b8e5afdacc81da3c521d72542d6393736965e37f1"
BOOTSTRAP_SHA="77b9800c55221810174cf0de9dc7b6dc345b999877c13d6f8971ed1b4ca2ad43"
def need(ok,message):
    if not ok:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    # These explicit checks run before parsing arguments or loading any project code.
    need(sys.flags.optimize == 0 and __debug__,"HOLD: optimized interpreter is outside the reviewed execution contract")
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,"HOLD: require Python -I -S -B")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--driver-sha256",required=True)
    parser.add_argument("--check-only",action="store_true")
    parser.add_argument("arguments",nargs=argparse.REMAINDER)
    args=parser.parse_args()
    here=Path(__file__).resolve()
    need(not Path(__file__).is_symlink() and stat.S_ISREG(here.stat().st_mode),"HOLD: nonregular entry guard")
    need(sha(here.read_bytes())==args.driver_sha256,"HOLD: entry guard changed")
    raw=(SOURCE/"SOURCE_MANIFEST.json").read_bytes()
    need(sha(raw)==MANIFEST_SHA,"HOLD: source manifest changed")
    boot=(SOURCE/"bootstrap08.py").read_bytes()
    need(sha(boot)==BOOTSTRAP_SHA,"HOLD: bootstrap changed")
    namespace={"__file__":str(SOURCE/"bootstrap08.py"),"__name__":"root_hash_checked_ops08_bootstrap"}
    exec(compile(boot,str(SOURCE/"bootstrap08.py"),"exec",dont_inherit=True,optimize=0),namespace)
    checked=namespace["source_bytes"](SOURCE,MANIFEST_SHA,BOOTSTRAP_SHA)
    if args.check_only:
        need(not args.arguments,"HOLD: check-only accepts no phase arguments")
        print(json.dumps({"status":"PRELAUNCH_SOURCE_CHECK_ONLY_PASS","optimize":sys.flags.optimize,"source_manifest_sha256":MANIFEST_SHA,"bootstrap_sha256":BOOTSTRAP_SHA,"source_members":len(checked),"provider_calls":0,"execution_authority_granted":False},sort_keys=True))
        return
    arguments=args.arguments
    if arguments and arguments[0]=="--":arguments=arguments[1:]
    need(bool(arguments),"HOLD: explicit reviewed phase arguments required")
    # The package's independent root-approval, intent, source and provider guards remain mandatory.
    module=namespace["load_verified"](SOURCE,MANIFEST_SHA,BOOTSTRAP_SHA)
    return module.main(arguments)
if __name__=="__main__":main()
