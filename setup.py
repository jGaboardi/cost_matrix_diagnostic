from setuptools import setup

setup(name='cost_matrix_diagnostic',
      version='0.2',
      description='Run diagnostics on cost matrices created with TransCAD',
      url='https://github.com/jGaboardi/cost_matrix_diagnostic',
      author='James D. Gaboardi',
      author_email='jgaboardi@fsu.edu',
      license='3-Clause BSD',
      packages=['cost_matrix_diagnostic'],
      install_requires=['pandas', 'numpy'],
      zip_safe=False)