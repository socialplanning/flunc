__version__ = '0.2'

from setuptools import setup, find_packages

setup(name="flunc",
      version=__version__,
      description="Functional test suite runner",
      long_description="""\
""",
      classifiers=[
        # dev status, license, HTTP categories
        ],
      keywords='',
      author="The Open Planning Project",
      author_email="",
      url="",
      license="GPL",
      packages=find_packages(exclude=[]),
      zip_safe=False,
      install_requires=[
        'twill',
        'lxml',
      ],
      dependency_links=[
        'http://darcs.idyll.org/~t/projects/',
      ],
      include_package_data=True,
      entry_points="""
      [console_scripts]
      flunc = flunc.flunc:main
      [distutils.setup_keywords]
      ftest_require=setuptools.dist:check_requirements
      [distutils.commands]
      flunc = flunc.command:ftest_runner
      """,
      )


