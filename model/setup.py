from setuptools import setup

setup(
    name = 'flasky-model',
    version = '1.0',
    long_description = __doc__,
    packages = [
        'flasky.model'
    ],
    package_dir = {
        'flasky.model': 'src'
    },
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Flask>=0.10',
        'Flask-SQLAlchemy>=2.0',
    ]
)
