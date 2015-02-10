# encoding: utf-8

import subprocess

from sphinxthat import conf
from sphinxthat.configurator import create_config_file


def _call(args, fail_silently=False):
    create_config_file()

    args = list(args or []) + ['--config', conf.config_filename]

    p = subprocess.Popen(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()

    out = p.stdout.read()
    if p.returncode != 0 and not fail_silently:
        raise Exception(out)
    return out


def reindex():
    return _call(['indexer', '--all', '--rotate'])


def start(silent_fail=False):
    return _call(['searchd'], silent_fail)


def stop(silent_fail=False):
    return _call(['searchd', '--stopwait'], silent_fail)


def restart():
    stop(silent_fail=True)
    start()
