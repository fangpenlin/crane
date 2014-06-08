from __future__ import unicode_literals
import os
import logging
import subprocess
import importlib

from jinja2 import Environment
from jinja2 import FunctionLoader
from jinja2 import StrictUndefined

logger = logging.getLogger(__name__)


class BuilderBase(object):

    #: owner_name
    owner_name = None
    #: name of image
    image_name = None
    #: version of image
    image_version = None
    #: the tag of image
    image_tag = None
    #: target tag name
    target_name = None
    #: directory for building
    build_dir = None

    #: name of dependencies builder
    dependencies = None

    def __init__(self, folder=None):
        self.folder = folder
        if self.folder is None:
            module = importlib.import_module(self.__class__.__module__)
            self.folder = os.path.dirname(module.__file__)
        self.jinja_env = Environment(
            loader=FunctionLoader(self._load_template),
            undefined=StrictUndefined,
        )
        self.init_variables()

    def _load_template(self, filepath):
        """Load jinja tempalte from a given filepath and return the content

        """
        with open(filepath, 'rt') as tempate_file:
            return tempate_file.read()

    def init_variables(self):
        """Initialize variables

        """
        if self.image_tag is None:
            self.image_tag = 'v{}'.format(self.image_version)
        if self.target_name is None:
            self.target_name = self.image_name
            if self.owner_name is not None:
                self.target_name = '{}/{}'.format(
                    self.owner_name,
                    self.target_name,
                )
            if self.image_tag is not None:
                self.target_name = '{}:{}'.format(
                    self.target_name,
                    self.image_tag,
                )
        if self.build_dir is None:
            self.build_dir = os.path.join(self.folder, '.build')
            if not os.path.exists(self.build_dir):
                os.mkdir(self.build_dir)

    def render_templates(self):
        """Render tempaltes

        """
        templates_dir = os.path.join(self.folder, 'templates')
        if not os.path.exists(templates_dir):
            return
        for filename in os.listdir(templates_dir):
            if not filename.endswith('.jinja'):
                continue
            template_path = os.path.join(templates_dir, filename)
            target_path = os.path.join(self.build_dir, filename)
            target_path = target_path[:-len('.jinja')]
            template = self.jinja_env.get_template(template_path)
            logger.info('Rendering template %s', template_path)
            with open(target_path, 'wt') as rendered_file:
                rendered_file.write(template.render(builder=self))

    def copy_files(self):
        """Copy files into build dir

        """
        # TODO:
        pass

    def build(self):
        logger.info(
            'Building image %s @ %s',
            self.image_name,
            self.image_version,
        )
        logger.debug('Build in folder %s', self.build_dir)

        self.copy_files()
        self.render_templates()
        # build the image
        logger.info('Building %s to %s', self.build_dir, self.target_name)
        subprocess.check_call(' '.join([
            'docker',
            'build',
            '-t="{}"'.format(self.target_name),
            self.build_dir,
        ]), shell=True)

    def upload(self):
        pass
        # TODO:
