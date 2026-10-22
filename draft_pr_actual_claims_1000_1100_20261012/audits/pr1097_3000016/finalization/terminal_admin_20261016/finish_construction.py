#!/usr/bin/env python3
"""Complete archive/binding/diff tail after the recorded ENOSPC attempt."""
import sys
sys.dont_write_bytecode = True
import textwrap
import prepare_terminal as p
def main():
    p.write(p.K/'MANIFEST.json',dict(p.load(p.K/'MANIFEST.json'),entries=[{'path':q.relative_to(p.K).as_posix(),**p.pin(q)} for q in sorted(q for q in p.K.rglob('*') if q.is_file() and q!=p.K/'MANIFEST.json')]))
    namespace=vars(p).copy()
    namespace.update(utc=p.datetime.datetime.now(p.datetime.timezone.utc).isoformat(),
        freeze=p.load(p.F/'INPUT_FREEZE.json')['entries'],
        before={r['path']:r for r in p.load(p.F/'BEFORE_BYTES.json')['entries']},
        source_copies=p.load(p.T/'COPIES.json')['entries'],
        rows=p.load(p.T/'STAGE_RESOLUTION.json')['entries'],
        files=sorted(q for q in p.K.rglob('*') if q.is_file() and q!=p.K/'MANIFEST.json'))
    source=(p.F/'prepare_terminal.py').read_text()
    tail=source[source.index('    stream=io.BytesIO()'):source.index("if __name__=='__main__':main()")]
    exec(compile(textwrap.dedent(tail),str(p.F/'prepare_terminal.py')+'[tail]','exec'),namespace)
if __name__=='__main__':main()
