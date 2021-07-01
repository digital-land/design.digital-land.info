# -*- coding: utf-8 -*-
"""
Manager command for installing GOV.UK assets
"""

import contextlib
import glob
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory
import urllib
import zipfile

from flask_script import Command, Option


@contextlib.contextmanager
def pushd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_cwd)


def move_dir(src, to):
    for f in glob.glob(src):

        if not os.path.isdir(to):
            os.makedirs(to)

        shutil.move(f, to)


def rmdir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


class ManageGovUkAssets(Command):
    """
    Download and compile GOV.UK template, frontend toolkit and elements
    """

    option_list = (
        Option('--app-dir', default='app', help="Relative path to app module"),
        Option('--clean', action='store_true', help="Remove installed files"),
    )

    def __init__(self):
        self.app_dir = None
        self.clean = False
        self.packages = {
            'frontend_toolkit': GovUkFrontendToolkit,
            'elements': GovUkElements,
            'template': GovUkTemplate
        }

    def run(self, app_dir, clean):
        """
        Download and install the govuk assets
        """

        self.app_dir = app_dir
        self.clean = clean

        for package_name, package_class in self.packages.items():
            self.install(package_name, package_class(app_dir))

    def install(self, package_name, package):
        """
        Download and extract package zip file into tempdir, then build
        """

        if self.clean:
            package.clean()

        with TemporaryDirectory() as download_dir:
            dest_zip = '{}/{}.zip'.format(download_dir, package_name)
            unzip_dir = '{}/unzipped'.format(download_dir)

            urllib.request.urlretrieve(package.url, dest_zip)

            with zipfile.ZipFile(dest_zip) as zf:
                zf.extractall(unzip_dir)

            package.build(unzip_dir)


class GovUkFrontendToolkit(object):

    url = (
        'https://github.com/alphagov/govuk_frontend_toolkit/archive/'
        'master.zip')

    def __init__(self, app_dir):
        self.dest_dir = '{}/static/govuk_frontend_toolkit'.format(app_dir)

    def clean(self):
        rmdir(self.dest_dir)

    def build(self, unzip_dir):
        for path in ['images', 'javascripts', 'stylesheets']:
            move_dir(
                '{}/govuk_frontend_toolkit-master/{}'.format(unzip_dir, path),
                to=self.dest_dir)


class GovUkElements(object):

    url = 'https://github.com/alphagov/govuk_elements/archive/master.zip'

    def __init__(self, app_dir):
        self.dest_dir = '{}/static/govuk_elements'.format(app_dir)

    def clean(self):
        rmdir(self.dest_dir)

    def build(self, unzip_dir):
        move_dir(
            '{}/govuk_elements-master/public'.format(unzip_dir),
            to=self.dest_dir)


class GovUkTemplate(object):

    url = 'https://github.com/alphagov/govuk_template_jinja/archive/master.zip'

    def __init__(self, app_dir):
        self.dest_views = '{}/templates/govuk_template'.format(app_dir)
        self.dest_assets = '{}/static/govuk_template'.format(app_dir)

    def clean(self):
        rmdir(self.dest_views)
        rmdir(self.dest_assets)

    def build(self, unzip_dir):
        master_dir = '{}/govuk_template_jinja-master'.format(unzip_dir)

        print( master_dir )

        move_dir(
            '{}/assets'.format(master_dir),
            to=self.dest_assets)

        move_dir(
            '{}/views'.format(master_dir),
            to=self.dest_views)