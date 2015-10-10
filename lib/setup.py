from setuptools import setup

setup(
    name = 'flasky-lib',
    version = '1.0',
    long_description = __doc__,
    packages = [
        'flasky.lib',
        'flasky.lib.http',
        'flasky.lib.log',
    ],
    package_dir = {
        'flasky.lib': 'src',
        'flasky.lib.http': 'src/http',
        'flasky.lib.log': 'src/log',
    },
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Flask>=0.10',
        'pylibmc>=1.5.0',
    ]
)
