from collections import OrderedDict
from contextlib import contextmanager
import os
import subprocess as sp

from django.conf import settings

TX = settings.TRANSIFEX_TX_BIN
LANG = settings.PYDOC_LANG
GIT = settings.GIT_BIN
SPHINX_INTL = settings.SPHINX_INTL_BIN
SPHINX_BUILD = settings.SPHINX_BUILD_BIN


@contextmanager
def cd(newdir):
    """
    Context manager for changing working directory.

    Ref: http://stackoverflow.com/a/24176022
    """
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def run_command_under_doc_root(cmd, catched=True):
    with cd(newdir=settings.PYDOC_ROOT):
        if catched:
            process = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            process = sp.run(cmd)
        return process


def git_add_commit_push():
    git_processes = OrderedDict()
    commit_msg = 'Update translation (auto daily)'
    commands = OrderedDict([
        ('git_add', [GIT, 'add', 'locale/*']),
        ('git_commit', [GIT, 'commit', '-m', commit_msg]),
        ('git_push', [GIT, 'push']),
    ])
    for cmd_name, cmd in commands.items():
        git_processes[cmd_name] = run_command_under_doc_root(cmd)
    return git_processes


def tx_pull(page=None):
    cmd = [TX, 'pull', '-l', LANG]
    if page is not None:
        # update certain page
        tx_page_identifier = '{:s}.{:s}'.format(
            settings.TRANSIFEX_PROJ_NAME,
            page
        )
        cmd += ['-r', tx_page_identifier]
    return run_command_under_doc_root(cmd)


def sphinx_intl_build():
    return run_command_under_doc_root(
        [SPHINX_INTL, 'build']
    )


def sphinx_build_html(rebuild_all=False):
    cmd = [
        SPHINX_BUILD, '-b', 'html',
        '-d', 'build/doctrees',
        '-D', 'language=%s' % LANG,
        '-A', 'autobuildi18n=1',
    ]
    if rebuild_all:
        cmd += ['-a']
    cmd += [
        '.', 'build/html',
    ]
    return run_command_under_doc_root(cmd)


def update_one_page(page):
    processes = OrderedDict()
    processes['tx_pull'] = tx_pull(page)
    processes['sphinx_intl_build'] = sphinx_intl_build()
    processes['sphinx_build_html'] = sphinx_build_html()
    return processes


def full_update_and_commit():
    processes = OrderedDict()
    processes['tx_pull'] = tx_pull(page=None)
    # FIXME: set rebuild_all=False to shorten build time
    # rebuild_all will take too long time
    # causing the task times out and respawn for many times
    # additionally make update_one_page uncached (unpickled)
    processes['sphinx_build_html'] = sphinx_build_html(rebuild_all=False)
    processes.update(git_add_commit_push())
    return processes
