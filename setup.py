#!/usr/bin/python

from distutils.core import setup

setup(
    name='eerie-gator',
    version='0.1',
    description='OpenSprinkler Pi controller',
    author='Austyn Bontrager',
    author_email='austyn@gmail.com',
    packages=['eerie_gator'],
    scripts=['eerie-gate', 'eerie-gateway'],
    data_files=[
        ('/etc', ['eerie_gator/eerie_gator.conf']),
        ],
    requires=["RPi", "pytz", "flask", "icalendar", "dateutil"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
