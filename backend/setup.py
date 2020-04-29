from setuptools import find_packages, setup

setup(
   name='BigInters',
   version='1.0',
   description='Bigithin Intersin',
   author='Kevin Li',
   author_email='li.kevin512@gmail.com',
   packages=['BigInters', 'BigInters.Analyzer', 'BigInters.Analyzer.RiotAPI'],  #same as name
   install_requires=['requests', 'flask'], #external packages as dependencies
)
