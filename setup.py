from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='clchoropleth',
      version='1.0.3',
      description='Creates SVG choropleths of Chilean regions',
      url='http://github.com/slarrain/clchoropleth',
      author='Santiago Larrain',
      author_email='santiagolarrain@gmail.com',
      license='MIT',
      packages=['clchoropleth'],
      install_requires=[
          'clcomuna',
          'bs4',
          'pandas'
      ],
      include_package_data=True,
      zip_safe=False)
