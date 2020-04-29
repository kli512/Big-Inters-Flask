from setuptools import find_packages, setup

setup(
   name='BigIntersFrontend',
   version='1.0',
   description='Bigithin Intersin la Front',
   author='Kevin Li',
   author_email='li.kevin512@gmail.com',
   packages=['BigIntersFrontend'],  #same as name
   install_requires=['requests', 'flask'], #external packages as dependencies
)
