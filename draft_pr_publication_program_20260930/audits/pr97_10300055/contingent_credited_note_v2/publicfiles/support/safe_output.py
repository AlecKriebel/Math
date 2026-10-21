"""Local disposable-output contract; no defence against concurrent hostile replacement."""
import contextlib
import json
import os
from pathlib import Path
import tempfile


def fresh_output(raw, package):
    """Reject aliases into inputs and any existing output; create once, exclusively."""
    requested = Path(raw).expanduser()
    output = requested.resolve(strict=False)
    package = package.resolve()
    if output == package or package in output.parents:
        raise ValueError('Choose an output directory outside the closed package')
    # lexists also detects a dangling final symlink. mkdir itself is exclusive.
    if os.path.lexists(requested) or os.path.lexists(output):
        raise ValueError('Output directory must be fresh and non-existing')
    if not output.parent.is_dir():
        raise ValueError('Output parent must already be an existing directory')
    os.mkdir(output, 0o700)
    return output


@contextlib.contextmanager
def exclusive_binary(path):
    """First creation fails for every existing leaf, including hardlinks."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        yield stream


def write_new(path, data):
    with exclusive_binary(path) as stream:
        stream.write(data)


def copy_new(source, destination):
    write_new(destination, source.read_bytes())


def json_bytes(value):
    return (json.dumps(value, indent=2) + '\n').encode('utf-8')


class Journal:
    """Exclusive initial publication; later updates replace the directory entry."""
    def __init__(self, path):
        self.path = Path(path)
        self.created = False

    def save(self, value):
        descriptor, name = tempfile.mkstemp(prefix='.journal-', dir=self.path.parent)
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(json_bytes(value))
            if self.created:
                # replace never writes through a destination symlink or hardlink.
                os.replace(temporary, self.path)
            else:
                # link publishes the complete file, failing if the leaf exists.
                os.link(temporary, self.path, follow_symlinks=False)
                self.created = True
        finally:
            if temporary.exists():
                temporary.unlink()
