from setuptools import setup, find_packages

setup(name='buzz',
      version='0.1',
      description='RPi component of the Buzz doorbell application',
      url='https://github.com/mxtm/buzz-rpi',
      author='Max Tamer-Mahoney',
      author_email='max@mxtm.me',
      license='MIT',
      packages=find_packages(include=['buzz', 'buzz.*']),
      zip_safe=False)
