# Git Releases
Documentation regarding publishing/releases methods.

## Initial Setup
Before Pip publishing will work on a new project several steps need to be taken:
  - An account needs to be created at https://pypi.org/ and/or https://test.pypi.org/
  - A auth token needs to be created for each account
  - This token needs to be stored as a secret on the github project

Complete instructions and more informaction can be found [here](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries).


## Steps
These are the basic steps to follow in order to publish a new version of this code onto Pip:

 - Complete your changes to the code base
 - Increment _\_\_version\_\_.py_ with new version number
 - Run "make release". This runs
    - init-dev, check, test, docu, build functions in the make file,
    - reads the python code version from _\_\_version\_\_.py_,
    - creates a git tag based off the python version,
    - commits, tags, and pushes to the project repo (with rollbacks if fail)
 - Go to the "releases" page on github.com (https://github.com/(my_org)/(my_project)/releases) and create new release:
    - Select "Draft New Release" 
    - Select tag created in previous step, 
    - Leaving the Release Title blank will default to the tag name
    - Fill in release notes 
    - and hit "Publish Release"

Publishing the release will cause the _/.github/workflows/python-publish.yml_ action to start. This will run through the make init, check, docu, and build steps before publishing the new version to pip using the supplied pip secret.

This triggers init-dev, check, test, docu, build and publishes to pip
Readthedocs might detect the changes and update the webpage. Not sure about that

## What version number to choose?
A comprehensive description on a sensible versioning strucutre is described [here](https://semver.org/). 

## What other actions are running?
All yaml files stored in the ./.github/workflows/*.yml folder are github actions associated with the project. [Here](https://github.com/sdras/awesome-actions) is a curated list of possible actions that could be run.
