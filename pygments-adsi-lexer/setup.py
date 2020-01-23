from setuptools import setup, find_packages

setup (
    name='adsilexer',

    version='0.0.1',
    description='Pygments ADSI custom lexer.',
    keywords='pygments adsi lexer',
    license='MIT',

    author='tigerxp',
    author_email='vpupkin@gmail.com',

    packages=find_packages(),
    install_requires=['pygments>=2.0.2'],

    entry_points =
    """
    [pygments.lexers]
    adsilexer = adsilexer:AdsiLexer
    """,
)
