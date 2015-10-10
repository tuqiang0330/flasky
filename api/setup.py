from setuptools import setup

setup(
    name = 'flasky-api',
    version = '1.0',
    long_description = __doc__,
    packages = [
        'flasky.api'
    ],
    package_dir = {
        'flasky.api': 'src'
    },
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'flasky-lib>=1.0',
        'flasky-model>=1.0',
        'Flask-Bcrypt>=0.7',
    ]
)
