from setuptools import setup, find_packages

setup(
    name='ce-mlflow-extension',
    version='0.1.0',
    author='CloudExplain Team',
    author_email='tobias@cloudexplain.eu',
    description='MLflow integration library for generating interactive HTML reports with SHAP analysis using Svelte and Chart.js',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'mlflow>=2.0.0',
        'shap>=0.40.0',
        'numpy>=1.20.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'jinja2>=3.0.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.12.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
        ]
    },
    include_package_data=True,
    package_data={
        'ce_mlflow_extension': [
            'templates/*.html',
            'templates/assets/*',
            'templates/components/*',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    keywords='mlflow, machine learning, explainability, shap, visualization, html, reports',
    project_urls={
        'Documentation': 'https://github.com/cloudexplain/ce-mlflow-extension',
        'Source': 'https://github.com/cloudexplain/ce-mlflow-extension',
        'Tracker': 'https://github.com/cloudexplain/ce-mlflow-extension/issues',
    },
)