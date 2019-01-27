#!/usr/bin/env python

from setuptools import setup

setup(name='haste_cloud_gateway',
      version='0.10',
      packages=[
                'haste.cloud-gateway'],
      description='Cloud Gateway for the HASTE platform: http://http://haste.research.it.uu.se',
      author='Ben Blamey',
      author_email='ben.blamey@it.uu.se',
      install_requires=[
          'aiohttp'

      ],
      test_requires=[
          'pytest'
      ]
      )
