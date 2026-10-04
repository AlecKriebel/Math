"""Run untouched candidate copies; preserve complete stdout/stderr receipts."""
from pathlib import Path
import contextlib, datetime, hashlib, io, json, os, runpy, subprocess, sys, time, gzip

P = Path(__file__).resolve().parent
D = P / 'private/replay'
S = P / 'reproduction_streams'
S.mkdir(exist_ok=True)
original = subprocess.check_output
receipts = []

def observed_check_output(*args, **kwargs):
    command = args[0] if args else kwargs['args']
    label = Path(command[1]).name.replace('.py', '')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tic = time.monotonic()
    result = subprocess.run(command, cwd=kwargs.get('cwd', D), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (S / (label + '.stdout')).write_bytes(result.stdout)
    (S / (label + '.stderr')).write_bytes(result.stderr)
    receipts.append(dict(command=list(command), started_utc=started, returncode=result.returncode,
                         seconds=time.monotonic()-tic, stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr),
                         stdout_sha256=hashlib.sha256(result.stdout).hexdigest()))
    result.check_returncode()
    return result.stdout

subprocess.check_output = observed_check_output
output = io.StringIO()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with contextlib.redirect_stdout(output):
        runpy.run_path(str(D / 'verify_publication.py'), run_name='__main__')
    (S / 'verify_publication.stdout').write_text(output.getvalue())
    (S / 'verify_publication.stderr').write_text('')
except Exception as error:
    receipts.append(dict(publication_error=repr(error)))
    raise
finally:
    subprocess.check_output = original
    (P / 'reproduction_receipts.json').write_text(json.dumps(dict(started_utc=started, receipts=receipts), indent=2)+'\n')

# Retain the full C++ stream privately, compressed, and verify it independently
# against the Python target digest; no candidate source is changed.
exe = P / 'private/check_turn4'
compile_result = subprocess.run(['g++','-O3','-std=c++17',str(D/'check_turn_4.cpp'),'-o',str(exe)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(S/'cpp_compile.stdout').write_bytes(compile_result.stdout)
(S/'cpp_compile.stderr').write_bytes(compile_result.stderr)
compile_result.check_returncode()
stream = subprocess.Popen([str(exe),'--stream'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
digest = hashlib.sha256()
whole = hashlib.sha256()
states = size = 0
terminal = None
with gzip.open(P/'private/full_cpp_stream.stdout.gz','wb',compresslevel=6) as destination:
    for line in stream.stdout:
        destination.write(line)
        whole.update(line)
        size += len(line)
        if line.startswith(b'S|'):
            digest.update(line)
            states += 1
        else:
            terminal = json.loads(line)
stderr = stream.stderr.read()
rc = stream.wait()
(S/'cpp_full_stream.stderr').write_bytes(stderr)
expected = json.loads((D/'TURN_4_CHECKS.json').read_text())
assert rc == 0 and states == expected['coaccessible_states']
assert digest.hexdigest() == expected['canonical_action_stream_sha256']
for key,value in terminal.items():
    assert expected[key] == value
full_receipt = dict(returncode=rc, state_records=states, complete_stdout_bytes=size,
                    complete_stdout_sha256=whole.hexdigest(), state_stream_sha256=digest.hexdigest(),
                    complete_stream_private_gzip='private/full_cpp_stream.stdout.gz', terminal=terminal,
                    compressed_bytes=(P/'private/full_cpp_stream.stdout.gz').stat().st_size)
(P/'full_cpp_stream_receipt.json').write_text(json.dumps(full_receipt,indent=2)+'\n')
print(output.getvalue(),end='')
print(json.dumps(full_receipt,indent=2))
