"""Run a command and preserve exact argv, UTC timing, streams and content hashes."""
import datetime, hashlib, json, pathlib, subprocess, sys

base = pathlib.Path(__file__).resolve().parent
label = sys.argv[1]
argv = sys.argv[2:]
evidence = base / 'private' / 'runs'
evidence.mkdir(parents=True, exist_ok=True)
start = datetime.datetime.now(datetime.UTC).isoformat()
result = subprocess.run(argv, capture_output=True)
end = datetime.datetime.now(datetime.UTC).isoformat()
record = dict(label=label, argv=argv, cwd=str(pathlib.Path.cwd()), start_utc=start,
              end_utc=end, returncode=result.returncode)
for name, stream in [('stdout', result.stdout), ('stderr', result.stderr)]:
    p = evidence / (label+'.'+name)
    p.write_bytes(stream)
    record[name+'_sha256'] = hashlib.sha256(stream).hexdigest()
    record[name+'_bytes'] = len(stream)
for arg in argv:
    p = pathlib.Path(arg)
    if p.is_file():
        record.setdefault('input_file_sha256', {})[str(p.resolve())] = hashlib.sha256(p.read_bytes()).hexdigest()
(evidence/(label+'.json')).write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
