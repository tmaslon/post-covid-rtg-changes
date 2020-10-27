from setuptools import setup

setup(
   name='covidotron',
   version='1.0',
   description='A module for post-COVID-19 changes identification from X-rays',
   license="MIT",
   author='',  #tbd
   author_email='',  #tbd
   packages=['covidotron'],  # same as name
   install_requires=['opencv-python']  # external packages as dependencies
)