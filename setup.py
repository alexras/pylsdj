from setuptools import setup

setup(name='pylsdj',
      version='1.2.0',
      description='A utility belt for dealing with LSDJ-related files',
      url='http://github.com/alexras/pylsdj',
      author='Alex Rasmussen',
      author_email='alexras@acm.org',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      license='MIT',
      packages=['pylsdj'],
      requires=['bread'],
      zip_safe=False)
