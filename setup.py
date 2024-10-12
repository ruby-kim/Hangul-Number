from setuptools import setup, find_packages
import hangul_number

setup(name=hangul_number.__name__,
      description=hangul_number.__description__,
      version=hangul_number.__version__,
      author=hangul_number.__author__,
      author_email=hangul_number.__author_email__,
      url=hangul_number.__url__,
      download_url=hangul_number.__download_url__,
      install_requires=hangul_number.__install_requires__,
      license=hangul_number.__license__,
      long_description=open('./README.md', 'r', encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      packages=find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: Korean",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS",
            "Operating System :: POSIX",
      ]
      )
