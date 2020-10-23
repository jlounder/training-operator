# training-operator

## Description

This codebase is an example charm - based on the Canonical training for the
[Python Operator Framework](https://github.com/canonical/operator). The code in
its current form is a scaffolded charm, with no customization.

## Prerequisites

Follow these instructions to configure your environment:

### Setup MicroK8s and Juju

Most up to date instruction can be found at <https://juju.is/docs/microk8s-cloud>

But a quick summary can be found here:

    > sudo snap install microk8s --classic
    > sudo usermod -a -G microk8s $USER
    > sudo su - $USER
    > microk8s status --wait-ready
    > microk8s.enable dns storage
    > sudo snap install juju --classic
    > juju bootstrap microk8s micro
    > juju add-model training

### Install Charmcraft

[Charmcraft](https://github.com/canonical/charmcraft) is our build and publish
tool for Operators.

    > sudo snap install charmcraft --beta

## Usage

This project is intended as a training aid, to learn how to quick start an
Operator with the Python Operator Framework.

For each step in this project, you'll find numbered files inside the staged
directory. Example: [stages/src-charm-py/01podspec.py](stages/src-charm-py/01podspec.py)
- which contains an updated version of [src/charm.py](src/charm.py) for step 01
of the training.

After reviewing each step of the tutorial, you should make the changes from the
appropriate files in stages. Example, for Step 01, you should run the following
commands:

    > cp stages/src-charm-py/01podspec src/charm.py
    > charmcraft build
    Done, charm left in 'training.charm'
    > juju deploy ./training.charm
    Deploying charm "local:kubernetes/training-0".
    >

### 00 - Initialize a new charm

    > charmcraft init --project-dir training-charm --name training

This command will scaffold a charm into the training-charm directory, and should
look identical to this repository (except for the stages directory). Inside the
stages directory, you will find a 00 prefix for each file, which reflects this
initial stage.

### 01 - Setting up a Kubernetes workload
To view the changes for [src/charm.py](src/charm.py)

    > diff stages/src-charm-py/00init.py stages/src-charm-py/01podspec.py

Build and deploy.

### 02 - Using configs
View the changes for [conig.yaml](conig.yaml)

    > diff stages/config-yaml/00init.yaml stages/config-yaml/02newconfigs.yaml

View the changes for [src/charm.py](src/charm.py)

    > diff stages/src-charm-py/01podspec.py stages/src-charm-py/02newconfigs.py

Build and deploy. At this stage, you can use upgrade-charm instead of deploy.

    > juju upgrade-charm training --path=./training.charm
    Added charm "local:kubernetes/training-1" to the model.

### 03 - Persistent storage (Kubernetes StatefulSets)
View the changes for [metadata.yaml](metadata.yaml)

    > diff stages/metadata-yaml/00init.yaml stages/metadata-yaml/03storage.yaml

Build and redeploy. If you attempt to deploy after this change, you will see an
error message, because you cannot convert a traditional workload to a StatefulSet
in Kubernetes. You'll need to remove and redeploy the training application.

    > juju remove-application training
    removing application training

### 04 - Adding a relation
View the changes for [metadata.yaml](metadata.yaml)

    > diff stages/metadata-yaml/03storage.yaml stages/metadata-yaml/04relation.yaml

View the changes for [src/charm.py](src/charm.py)

    > diff stages/src-charm-py/02newconfigs.py stages/src-charm-py/04relation.py

### 05 - Adding a unit test with harness
View the changes for [tests/test_charm.py](tests/test_charm.py)

    > diff stages/tests-test_charm-py/00init.py stages/tests-test_charm-py/04harness.py

## Running Unit Tests

Create and activate a virtualenv, and install the development requirements, run
the testing helper script.

    > virtualenv -p python3 venv
    > source venv/bin/activate
    > pip install -r requirements-dev.txt
    > ./run_tests
