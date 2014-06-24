Crane
=====

[![Build Status](https://travis-ci.org/victorlin/crane.svg?branch=master)](https://travis-ci.org/victorlin/crane)

Crane is a simple tool for building Dockerfiles. It can render templates for you. 

Demo
====

```bash
git git@github.com:victorlin/crane.git
cd crane
pip install -e .
crane examples.hello_baby
docker run -i -t hello_baby
```

Get started
===========
To create a simple building project, here you create a Python package like this

 - hello_baby
    - \__init__.py
    - templates
        - Dockerfile.jinja
        - hello_baby.sh.jinja

The `__init__.py`:

```python
from __future__ import unicode_literals

from crane import BuilderBase


class Builder(BuilderBase):

    image_name = 'hello_baby'
    image_version = '0.0.0'
    image_tag = 'latest'

```

The content of `Dockerfile.jinja` could be something like this:

```
FROM phusion/baseimage:0.9.10
MAINTAINER Victor Lin <bornstub@gmail.com>

# Set correct environment variables.
ENV HOME /root

ADD hello_baby.sh /tmp/hello_baby_v{{ builder.image_version }}.sh
RUN chmod +x /tmp/hello_baby_v{{ builder.image_version }}.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init", "--", "bash", "-c", "/tmp/hello_baby_v{{ builder.image_version }}.sh"]


```

It's a [jinja2](http://jinja.pocoo.org/docs/) template file, you can use the variable `builder` to generate something like your software version into the building process. Besides `Dockerfile.jinja`, all files suffixed with `.jinja` in `templates` folder under that Python package will be rendered to build folder before building the image. Another file we have in this example is `hello_baby.sh.jinja`:

```bash
#!/bin/bash
export VERSION='{{ builder.image_version }}'
echo "Current version $VERSION"

```

And likewiese, you can access `builder` variable in the template. The example can be found [here](https://github.com/victorlin/crane/tree/master/examples/hello_baby).
