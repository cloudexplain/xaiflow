from setuptools import setup, find_packages

setup(
    name='ce-mlflow-extension',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python library for generating HTML reports using SHAP values and metadata with Svelte and Chart.js.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'shap',
        'numpy',
        'pandas',
        'flask',  # or any other web framework you might use
        # Add other dependencies as needed
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)