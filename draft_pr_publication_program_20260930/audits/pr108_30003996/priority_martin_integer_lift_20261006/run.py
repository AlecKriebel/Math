"""Audit subprocess receipt wrapper; writes only in this dedicated folder."""
import datetime, hashlib, json, pathlib, subprocess, sys
BASE = pathlib.Path(__file__).resolve().parent
argv = sys.argv[1:]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
record = dict(utc=started, completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), pid=p.pid, argv=argv, exit=p.returncode)
with (BASE / 'private/COMMANDS_RAW.jsonl').open('a') as f:
    f.write(json.dumps(record) + '\n')
public_record = dict(record)
public_record['argv'] = [a if len(a) < 1000 else '[long argument sha256=' + hashlib.sha256(a.encode()).hexdigest() + ']' for a in argv]
with (BASE / 'COMMANDS.jsonl').open('a') as f:
    f.write(json.dumps(public_record) + '\n')
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
print(json.dumps(public_record), file=sys.stderr)
sys.exit(p.returncode)
