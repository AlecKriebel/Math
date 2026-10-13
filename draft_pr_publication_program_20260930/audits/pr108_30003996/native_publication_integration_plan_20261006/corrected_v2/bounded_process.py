"""Bounded subprocess custody. Only caller-selected argv; no shell or services here."""
import datetime, hashlib, os, selectors, signal, subprocess, time
from pathlib import Path
from v2_guards import require, canonical

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def validate_policy(p):
    require(set(p) == {'max_process_count', 'retain_bytes_per_stream', 'max_stdout_bytes',
        'max_stderr_bytes', 'deadline_seconds', 'terminate_grace_seconds'}, 'Process policy fields')
    require(all(type(p[x]) is int for x in p), 'Integer process limits required')
    require(1 <= p['max_process_count'] <= 64 and 1 <= p['retain_bytes_per_stream'] <= 4096 and
        1 <= p['max_stdout_bytes'] <= 32*1024*1024 and 1 <= p['max_stderr_bytes'] <= 65536 and
        1 <= p['deadline_seconds'] <= 30 and 1 <= p['terminate_grace_seconds'] <= 2, 'Process limits out of bounds')

class BoundedRunner:
    def __init__(self, output, cwd, policy):
        validate_policy(policy)
        self.output, self.cwd, self.policy = Path(output), Path(cwd), policy
        self.records = []

    def run(self, argv, stdout_cap=None, deadline=None, watchdog=None, fixture=False, allow_failure=False):
        require(len(self.records) < self.policy['max_process_count'], 'Subprocess count cap')
        require(isinstance(argv, list) and argv and all(isinstance(x, str) for x in argv), 'Explicit argv required')
        cap = stdout_cap or self.policy['max_stdout_bytes']
        duration = deadline or self.policy['deadline_seconds']
        require(1 <= cap <= self.policy['max_stdout_bytes'] and 1 <= duration <= 120, 'Call bounds')
        started, begin = now(), time.monotonic()
        process = subprocess.Popen(argv, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            start_new_session=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1',
                'GIT_OPTIONAL_LOCKS':'0','LC_ALL':'C'})
        selector = selectors.DefaultSelector()
        for name, stream in [('stdout',process.stdout),('stderr',process.stderr)]:
            os.set_blocking(stream.fileno(), False); selector.register(stream, selectors.EVENT_READ, name)
        data = {'stdout':bytearray(), 'stderr':bytearray()}
        counts = {'stdout':0, 'stderr':0}; digests = {s:hashlib.sha256() for s in data}
        retained = {s:bytearray() for s in data}; reason = None; term_at = None; killed = False
        def stop(why):
            nonlocal reason, term_at
            if reason is None:
                reason, term_at = why, time.monotonic()
                try: os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError: pass
        try:
            while selector.get_map() or process.poll() is None:
                elapsed = time.monotonic() - begin
                if elapsed >= duration: stop('deadline_exceeded')
                if watchdog is not None and reason is None:
                    try: watchdog()
                    except Exception as error: stop('resource_watchdog:' + str(error)[:240])
                if term_at is not None and time.monotonic()-term_at >= self.policy['terminate_grace_seconds'] and not killed:
                    try: os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                    killed = True
                if elapsed >= duration + self.policy['terminate_grace_seconds'] + 3:
                    stop('custody_drain_deadline'); break
                for key, _ in selector.select(0.1):
                    stream, name = key.fileobj, key.data
                    block = os.read(stream.fileno(), 65536)
                    if not block:
                        selector.unregister(stream); stream.close(); continue
                    counts[name] += len(block); digests[name].update(block)
                    remaining = self.policy['retain_bytes_per_stream'] - len(retained[name])
                    retained[name].extend(block[:max(0,remaining)])
                    limit = cap if name == 'stdout' else self.policy['max_stderr_bytes']
                    if counts[name] > limit: stop(name + '_read_cap_exceeded')
                    if len(data[name]) < limit: data[name].extend(block[:limit-len(data[name])])
        finally:
            selector.close()
            if process.poll() is None:
                killed = True
                try: os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError: pass
            try: process.wait(timeout=3)
            except subprocess.TimeoutExpired: reason = 'unreaped_after_SIGKILL_operator_intervention_required'
            for stream in [process.stdout,process.stderr]:
                if not stream.closed: stream.close()
        record = {'actual_process_record':True, 'fixture':fixture, 'argv':argv, 'cwd':str(self.cwd),
            'PID':process.pid, 'UTC_start':started, 'UTC_end':now(), 'exit_code':process.returncode,
            'deadline_seconds':duration, 'termination_reason':reason, 'SIGKILL_attempted':killed,
            'child_reaped':process.returncode is not None,
            'controlled_environment':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','GIT_OPTIONAL_LOCKS':'0','LC_ALL':'C'},
            'output_complete':reason is None, 'stream_read_caps':{'stdout':cap,'stderr':self.policy['max_stderr_bytes']}}
        index = len(self.records); receipts = self.output / 'process_receipts'; receipts.mkdir(exist_ok=True)
        for stream in data:
            path = 'process_receipts/' + str(index) + '.' + stream + '.bin'
            (self.output/path).write_bytes(retained[stream])
            record[stream] = {'bytes_observed':counts[stream], 'sha256_observed':digests[stream].hexdigest(),
                'retained_path':path, 'retained_bytes':len(retained[stream]),
                'retained_sha256':hashlib.sha256(retained[stream]).hexdigest()}
        self.records.append(record)
        journal = canonical({'actual_operator_PID':os.getpid(),'records':self.records})
        require(len(journal)<=128*1024,'Process journal cap')
        (self.output/'PROCESS_JOURNAL.json').write_bytes(journal)
        require(allow_failure or (process.returncode == 0 and reason is None), 'Subprocess failed: ' + str(reason or process.returncode))
        return bytes(data['stdout']), bytes(data['stderr']), record
