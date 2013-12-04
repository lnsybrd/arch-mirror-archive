#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
archarchive.cli
---------------

Main `archarchive.cli` CLI.
"""
import click
import contextlib
import logging
import os

from datetime import datetime

log = logging.getLogger('archarchive')


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
    Make a new btrfs snapshot from the last version
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

def repo_sync(sync_url, data_dir, version):
    log.info('repo_sync(pkg_sync_url: {}, data_dir: {}, version: {})'.format(sync_url, data_dir, version))

    target = '{0}/'.format(os.path.join(data_dir, version))
    log.debug('target: {0}'.format(target))

    if not os.path.exists(target):
        raise RuntimeError('Target directory {} does not exist'.format(target))

    cmd = "rsync -rltvH " + \
          "--delete "\
          "--exclude '*/.*' --exclude '*/os/i686' " + \
          "--exclude 'pool/*/*-i686.pkg.*' {0} {1}".format(sync_url, target)

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
@click.option('--sync-url', default="rsync://mirror.pkgbuild.com/packages/", show_default=True)
@click.option('--run-dir', default="/var/run/", show_default=True)
@click.option('--data-dir', default='/srv/data/mirror/archlinux', show_default=True)
@click.option('--version', default=datetime.now().strftime('%Y.%m.%d'), show_default=True)
@click.option('--debug', is_flag=True, show_default=True)
def sync(sync_url, run_dir, data_dir, version, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    make_snapshot(data_dir, version)
    repo_sync(sync_url, data_dir, version)
    make_current(data_dir, version)
