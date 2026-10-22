"""Capture own read-only integrity check and exact failed stdin inspection replay."""
import datetime,hashlib,json,pathlib,subprocess,sys
OWN=pathlib.Path(__file__).resolve().parent
which=sys.argv[1]
if which not in ("failed_inspection_replay","corrected_integrity"):raise SystemExit("bad capture mode")
source=OWN/("integrity_attempt01.py" if which=="failed_inspection_replay" else "verify_author_packet.py")
script=source.read_bytes();out=OWN/"runs"/which;out.mkdir(exist_ok=False)
(out/source.name).write_bytes(script)
def pin(raw):return {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
exe=pathlib.Path(sys.executable).resolve()
argv=[str(exe),"-"] if which=="failed_inspection_replay" else [str(exe),"-E","-S","-B","-P",str(source)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(argv,input=script if which=="failed_inspection_replay" else None,cwd=OWN,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20,check=False)
(out/"stdout.bin").write_bytes(r.stdout);(out/"stderr.bin").write_bytes(r.stderr)
binding={"schema":"pr206-owned-integrity-raw-run-v1","mode":which,"argv":argv,"cwd":str(OWN),"UTC_start":start,"UTC_end":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":pin(script),"stdin_script_exact_replay":which=="failed_inspection_replay","interpreter":{"path":str(exe),**pin(exe.read_bytes())},"exit_code":r.returncode,"stdout":pin(r.stdout),"stderr":pin(r.stderr),"expected_exit":1 if which=="failed_inspection_replay" else 0}
(out/"RUN_BINDING.json").write_text(json.dumps(binding,indent=2,sort_keys=True)+"\n")
print(json.dumps(binding,sort_keys=True))
if which=="corrected_integrity":print(r.stdout.decode());print(r.stderr.decode(),file=sys.stderr)
raise SystemExit(0 if r.returncode==binding["expected_exit"] else 1)
