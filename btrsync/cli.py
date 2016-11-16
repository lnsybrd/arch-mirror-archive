#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
btrsync.cli
--------------

Main `btrsync.cli` CLI.
"""
import click
import contextlib
import logging
import os

from datetime import datetime

log = logging.getLogger('btrsync')


@contextlib.contextmanager
def cd(path):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)

def make_snapshot(data_dir, version):
    """
    Make a snapshot of the previous version to sync against.
    """
    log.debug('Finding last sync')
    versions = [
        path for path in os.listdir(data_dir) if (
            os.path.isdir(os.path.join(data_dir, path)) and
            not os.path.islink(os.path.join(data_dir, path)) and
            not version == path
        )
    ]

    versions.sort()
    if len(versions):
        latest = os.path.join(data_dir, versions[-1])

    log.debug('latest: {0}'.format(latest))

    new_version = os.path.join(data_dir, version)

    if not os.path.exists(new_version):
        cmd = "btrfs subvol snapshot {} {}".format(latest, new_version)
        log.debug(cmd)
        os.system(cmd)
    else:
        log.info('Version {} already exists: {}'.format(version, new_version))

def repo_sync(sync_url, data_dir, version, excludes, delete):
    log.info(
        'repo_sync(pkg_sync_url: {}, data_dir: {}, version: {}, excludes: {}, delete: {})'.format(
            sync_url, data_dir, version, excludes, delete
        )
    )

    target = '{}/'.format(
        os.path.join(data_dir, version)
    )
    log.debug('target: {}'.format(target))

    if not os.path.exists(target):
        raise RuntimeError('Target directory {} does not exist'.format(target))

    cmd = (
        "rsync -rltvH "
        "{delete} "
        "{excludes} "
        "{url} "
        "{target} ".format(
            delete='--delete' if delete else '',
            excludes=''.join([" --exclude '{}' ".format(exclude) for exclude in excludes]),
            url=sync_url,
            target=target
        )
    )

    log.debug(cmd)
    os.system(cmd)

def make_current(data_dir, version):
    """
    Link the new version as the current
    """
    current = os.path.join(data_dir, 'current')
    if os.path.exists(current) and os.path.islink(current):
        os.remove(current)

    os.symlink(os.path.join(data_dir, version), current)

@click.command()
@click.option('--sync-url', required=True)
@click.option('--data-dir', required=True)
@click.option('--version', default=datetime.now().strftime('%Y.%m.%d'), show_default=True)
@click.option('--exclude', multiple=True)
@click.option('--delete/--no-delete', default=True, show_default=True)
@click.option('--debug', is_flag=True, show_default=True)
def sync(sync_url, data_dir, version, exclude, delete, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    make_snapshot(data_dir, version)
    repo_sync(sync_url, data_dir, version, exclude, delete)
    make_current(data_dir, version)
