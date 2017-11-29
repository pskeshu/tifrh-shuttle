from setuptools import setup

setup(name='tifrh-shuttle',
      version='0.1',
      description='TIFR-Hyderabad shuttle services',
      url='http://github.com/pskeshu/tifrh-shuttle',
      author='Kesavan Subburam',
      author_email='pskesavan@tifrh.res.in',
      license='MIT',
      packages=['fai'],
      install_requires=['Flask>=0.12.2',
                        'gunicorn==19.7.1'],
      zip_safe=False)
