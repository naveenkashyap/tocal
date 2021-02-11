from setuptools import setup  # type: ignore

setup(
    name="tocal",
    version="0.0.1",
    packages=["tocal"],
    entry_points={"console_scripts": ["tocal=tocal.__main__:main"]},
)
