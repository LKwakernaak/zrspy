from setuptools import setup

setup(
      name='zrspy',
      version='0.1',
      py_modules=['zrs'],
      install_requires=[
              'click',
              'bs4',
              'pandas',
              'datetime',
              'requests',
              'sqlalchemy'
              ],
      entry_points='''
      [console_scripts]
      zrspy=zrs:main
      ''',
      )

