from setuptools import setup

setup(
    name="idecdash_data_updater",
    version = "1.0.0",
    description = "IDECDash Data Updater component",
    author = "IDEClab",
    author_email = "example@udec.cl",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License : MIT License",
    ],
    packages=[
        "Dashboard", 
        "Dashboard.Helpers", 
        "Dashboard.DatabaseManager", 
        "Dashboard.DownloadManager", 
        "Dashboard.LoaderManager", 
        "Dashboard.QueueManager", 
    ]
)
