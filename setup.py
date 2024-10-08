import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'gevent >= 1.5a3',
    'gunicorn',
    'gevent-websocket >= 0.10.1',
    'plaster_pastedeploy',
    'premailer',
    'pyramid >= 1.10.4',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'pyramid-mako',
    'pyramid-zcml',
    'pyramid_retry',
    'pyramid_tm',
    'pyramid_zodbconn',
    'supervisor',
    'transaction',
    'ZODB3',
    'RelStorage',
    'zc.zlibstorage',
    'zope.component',
    'zope.interface',
    'zope.schema',
    'zope.container',
    'zope.cachedescriptors',
    'zope.processlifetime',
    'zope.generations',

    # indexing
    'zope.keyreference',
    'zope.intid',
    'zc.intid',
    'zope.catalog',
    'zope.site',
    
    'redis',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
    'httpie',
]

setup(
    name='testme',
    version='0.0',
    description='testme',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = testme:main',
        ],
        'console_scripts': [
            "inuo=testme.gunicorn:main",
        ],
    },
)
