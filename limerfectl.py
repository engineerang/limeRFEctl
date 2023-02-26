# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

import click
import os
import app.webserver
import gunicorn.app.base


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

@click.group()
def cli():
    # No windows support
    if os.name == 'nt':
        raise SystemExit('Windows not supported.')

@cli.command()
@click.option('-p', '--port', type=str, help='Network port to bind to', default='8000')
@click.option('-a', '--addr', type=str, help='Network address to bind to', default='127.0.0.1')
def run(port, addr):
    '''
    Launches the limerfectl webserver 
    '''
    options = {
        'bind': '%s:%s' % (addr, port),
        'workers': 1,
    }
    StandaloneApplication(app.webserver.app_limerfe, options).run()

