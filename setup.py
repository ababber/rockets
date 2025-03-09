from setuptools import setup, find_packages

MAIN_REQUIREMENTS = [
    "airbyte-cdk>=0.2.0,<0.3.0",
    "requests"
]

TEST_REQUIREMENTS = [
    "pytest~=6.1",
]

setup(
    name="source_nba_stats",
    description="Airbyte source connector for SportRadar NBA",
    author="Ankit",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,
    extras_require={"tests": TEST_REQUIREMENTS},
    package_data={"": ["*.json", "*.yaml", "*.yml"]},
)
