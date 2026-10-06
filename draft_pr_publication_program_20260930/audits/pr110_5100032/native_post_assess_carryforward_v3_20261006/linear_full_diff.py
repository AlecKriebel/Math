"""Complete linear-time review diff; one replacement hunk per UTF-8 file.

Common prefix/suffix lines are retained with three context lines. All central
old/new lines are emitted explicitly, even when some match. This is an exact
patch, not a shortest edit script. Native bodies and source bodies are never
modified. Binary additions retain their complete base64 bodies and full pins.
"""
import base64, hashlib, json, pathlib

N = 'unsolved_math_prioritization/'

def need(value, message):
    if not value:
        raise ValueError(message)

def pin(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

def lf_lines(body):
    """Split only on LF, retaining CRLF and every other byte exactly."""
    fields = body.split(b'\n')
    lines = [field + b'\n' for field in fields[:-1]]
    if fields[-1]:
        lines.append(fields[-1])
    return lines

def unified_range(start, count):
    # Unified format counts from one; an empty range names its preceding line.
    if count == 0:
        return str(start) + ',0'
    if count == 1:
        return str(start + 1)
    return str(start + 1) + ',' + str(count)

def full_diff(before, offers, prefix, cap=1024*1024):
    """Emit all offered paths in offer order, rejecting rather than truncating.

UTF-8 is classified on whole bodies. Diff lines are byte lines delimited only
by LF, so CRLF, lone CR, Unicode separators and a missing final LF survive.
An empty new file has headers and an explicit zero-count hunk, and its
existence is also recorded by the complete affected-path/body inventory.
"""
    need(type(cap) is int and cap >= 0, 'Exact nonnegative DIFF cap')
    need(type(prefix) is str and prefix.startswith(N+'attempts/') and prefix.endswith('/'),
         'Canonical target prefix')
    native = {N + name: body for name, body in before.items()}
    parts = []; size = 0
    def emit(body):
        nonlocal size
        size += len(body)
        need(size <= cap, 'Complete DIFF exceeds reviewed cap; no truncated result')
        parts.append(body)
    def emit_line(sign, line):
        emit(sign + line)
        if not line.endswith(b'\n'):
            emit(b'\n\\ No newline at end of file\n')
    for name, body in offers.items():
        rel = pathlib.PurePosixPath(name)
        need(type(name) is str and not rel.is_absolute() and str(rel) == name
             and '..' not in rel.parts and all(ord(c) >= 32 for c in name),
             'Canonical unambiguous offered path')
        need(name in native or name.startswith(prefix), 'Native or target-only DIFF path')
        need(type(body) is bytes, 'Full offered byte body')
        old = native.get(name)
        need(old is None or old != body, 'Unchanged derived output must not be offered')
        try:
            body.decode('utf8')
            if old is not None:
                old.decode('utf8')
        except UnicodeDecodeError:
            need(old is None, 'Native derived files must be UTF-8')
            emit(('Complete new binary addition '+name+' '+json.dumps(pin(body),sort_keys=True)+'\n').encode())
            emit(base64.b64encode(body)+b'\n')
            continue
        previous = [] if old is None else lf_lines(old)
        added = lf_lines(body)
        left = 0; small = min(len(previous), len(added))
        while left < small and previous[left] == added[left]:
            left += 1
        tail = 0
        while tail < small-left and previous[len(previous)-1-tail] == added[len(added)-1-tail]:
            tail += 1
        begin = max(0, left-3)
        old_end = len(previous)-tail + min(3,tail)
        new_end = len(added)-tail + min(3,tail)
        # Full byte reconstruction is checked independently of the emitted text.
        rebuilt = previous[:begin] + added[begin:new_end] + previous[old_end:]
        need(b''.join(rebuilt) == body, 'Full replacement hunk does not reconstruct exact offered bytes')
        emit(('--- '+('/dev/null' if old is None else 'a/'+name)+'\n+++ b/'+name+'\n').encode())
        emit(('@@ -'+unified_range(begin,old_end-begin)+' +'+unified_range(begin,new_end-begin)+' @@\n').encode())
        for line in previous[begin:left]:
            emit_line(b' ',line)
        for line in previous[left:len(previous)-tail]:
            emit_line(b'-',line)
        for line in added[left:len(added)-tail]:
            emit_line(b'+',line)
        for line in previous[len(previous)-tail:old_end]:
            emit_line(b' ',line)
    return b''.join(parts)
