from setuptools import setup

setup(
	name='tnm-wim-cli',
	version='1.0',
	packages=['cli', 'cli.commands'],
	include_package_data=True,
	install_requires=[
		'click',
	],
	entry_points="""
		[console_scripts]
		tnm-wim=cli.cli:cli
	""",
)