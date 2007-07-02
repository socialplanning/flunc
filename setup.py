__version__ = '0.1'

from setuptools import setup, find_packages

setup(name="flunc",
      version=__version__,
      description="",
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
      ],
      dependency_links=[
        # Latest twill is broken, defaulting to cheeseshop
        # (http://lists.idyll.org/pipermail/twill/2007-July/000715.html)

        # 'http://darcs.idyll.org/~t/projects/',
      ],
      include_package_data=True,
      entry_points="""
      [console_scripts]
      flunc = flunc.flunc:main
      """,
      )


