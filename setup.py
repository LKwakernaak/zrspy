from setuptools import setup, find_packages

setup(
    name='zrspy',
    version='0.1',
    py_modules=['zrs'],
    packages=find_packages(),
    install_requires=[
            'click',
            'arrow',
            'ics',
            'bs4',
            'pandas',
            'httplib2',
            'datetime',
            'requests',
            'sqlalchemy',
            'oauth2client',
            'google-api-python-client',
    	  'lxml',
            ],
    entry_points='''
    [console_scripts]
    zrspy=zrs:main
    ''',
    author='l.kwakernaak',
    author_email='kwakernaak@physics.leidenuniv.nl'
)

