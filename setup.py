from setuptools import find_packages, setup

setup(name='python_geometry',
      version='0.1',
      install_requires=[
          'natsort', 
          'cached-property', 
          'typeguard',
          'py-structs>=1.0.0',
          'taichi',
          'nptyping',

          # Testing related
          'pytest',
      ],
      packages=find_packages(),
      entry_points={}
)
