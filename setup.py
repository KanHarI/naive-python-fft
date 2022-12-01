from setuptools import setup, find_packages

setup(name='NaivePythonFFT',
      version='1.0',
      description='Simple FFT implementations',
      author='Itay Knaan Harpaz',
      author_email='knaan.harpaz@gmail.com',
      url='https://github.com/KanHarI/naive-python-fft',
      install_requires=['mypy', 'black', 'flake8', 'isort', 'pytest', 'ipython', 'flake8-black', 'seaborn', 'numpy', 'tqdm'],
      packages=find_packages(exclude=['test']),
      )
