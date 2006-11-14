__version__ = '0.1'

from setuptools import setup, find_packages

setup(name="topp_ftester",
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
        'twill'
      ],
      include_package_data=True,
      entry_points="""
      [console_scripts]
      ftest = topp.ftest.ftest:main
      """,
      )


