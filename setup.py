from pathlib import Path
import setuptools

project_dir = Path(__file__).parent

requires = [
    "prompt-toolkit==3.0.14",
    "Pygments==2.7.4",
    "pydantic==1.8.2",
    "tabulate==0.8.9"
]

def setup_package():
    metadata = dict(
        name="yeetdb",
        version="0.1.0",
        description="A Throwaway Database written in Python",
        long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
        long_description_content_type="text/markdown",
        license = 'UNLICENSE',
        classifiers=[
            "Environment :: Console",
            "Programming Language :: Python",
            "Intended Audience :: Developers",
        ],
        url="https://github.com/sangarshanan/yeetdb",
        author="sangarshanan",
        packages=setuptools.find_packages("src"),
        package_dir={"": "src"},
        install_requires=requires,
        python_requires=">=3.6",
        include_package_data=True,
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
