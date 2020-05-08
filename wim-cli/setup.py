from setuptools import setup

setup(
    name="wim-cli",
    version="1.0",
    packages=["wim", "wim.commands"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
    [console_scripts]
        wim=wim.cli:cli
    """,
)
