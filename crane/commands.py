#!/usr/bin/env python
from __future__ import unicode_literals
import logging
import importlib

import click


def load_builder_module(name):
    """Load and return builder by given name

    """
    return importlib.import_module(name)


@click.command()
@click.argument(
    'name',
    type=str,
)
def build(name):
    """Build a Dockerfile project

    """
    # TODO: use a better way to config the logger
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)
    module = importlib.import_module(name)
    builder = module.Builder()

    if builder.dependencies:
        logger.info('Building dependencies ...')
        for dep_name in builder.dependencies:
            # TODO: what about depdant's dependencies?
            # handle that later
            dep_module = load_builder_module(dep_name)
            dep_builder = dep_module.Builder()
            dep_builder.build()

    builder.build()
    logger.info('Finish building %s', builder.image_name)

if __name__ == '__main__':
    build()
