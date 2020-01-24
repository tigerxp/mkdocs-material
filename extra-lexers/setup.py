from setuptools import setup, find_packages

setup (
    name='pygments_extra_lexers',

    version='0.0.2',
    description='Pygments extra lexers (currently only ADSI).',
    keywords='pygments lexers adsi',
    license='MIT',

    author='tigerxp',
    author_email='vpupkin@gmail.com',

    packages=find_packages(),
    install_requires=['pygments>=2.0.2'],

    entry_points =
    """
    [pygments.lexers]
    extra_lexers = pygments_extra_lexers:AdsiLexer
    """,
)
