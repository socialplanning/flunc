__version__ = '0.5'

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

f = open('README.txt')
readme = "\\\n" + "".join(f.readlines())
f.close()

setup(name="flunc",
      version=__version__,
      description="Functional test suite runner",
      long_description=readme,
      classifiers=[
        # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Software Development :: Testing",
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        ],
      keywords='',
      author="The Open Planning Project",
      author_email="flunc-dev@lists.openplans.org",
      url="http://www.openplans.org/projects/flunc",
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


