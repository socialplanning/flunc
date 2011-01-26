__version__ = '0.8dev'

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

f = open('README.txt')
changes = open('CHANGES.txt')
readme = "\\\n" + "".join(f.readlines() + changes.readlines())
f.close()
changes.close()

setup(name="flunc",
      version=__version__,
      description="Functional test suite runner",
      long_description=readme,
      classifiers=[
        "Topic :: Software Development :: Testing",
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        ],
      keywords='',
      author="Luke Tucker, Rob Marianski and contributors",
      author_email="flunc-dev@lists.coactivate.org",
      maintainer="Ethan Jucovy",
      url="http://www.coactivate.org/projects/flunc",
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


