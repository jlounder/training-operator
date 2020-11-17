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

    $ sudo snap install microk8s --classic
    $ sudo usermod -a -G microk8s $USER
    $ sudo su - $USER
    $ microk8s status --wait-ready
    $ microk8s.enable dns storage
    $ sudo snap install juju --classic
    $ juju bootstrap microk8s micro
    $ juju add-model training

### Install Charmcraft

[Charmcraft](https://github.com/canonical/charmcraft) is our build and publish
tool for Operators.

    $ sudo snap install charmcraft --beta

## Usage

This project is intended as a training aid, to learn how to quick start an
Operator with the Python Operator Framework.

For each step in this project, you'll find numbered directories inside the stages
directory, which contains a complete version of the training operator. Example:
[stages/01podspec/src/charm.py](stages/01podspec/src/charm.py) - which contains
an updated version of the TrainingCharm class for Section 01.

After reviewing each step of the tutorial, you can build and deploy the charm
from within the stages directory:

    $ cd stages/01podspec
    $ charmcraft build
    Done, charm left in 'training.charm'
    $ juju deploy ./training.charm
    Deploying charm "local:kubernetes/training-0".
    $

### 00 - Initialize a new charm

    $ charmcraft init --project-dir training-charm --name training

This command will scaffold a charm into the training-charm directory, and the
contents should be identical to the staged [00init](stages/00init/) directory.

### 01 - Setting up a Kubernetes workload
To view the changes for [src/charm.py](stages/00init/src/charm.py)

    $ diff stages/00init/src/charm.py stages/01podspec/src/charm.py

Build and deploy.

### 02 - Using configs
View the changes for [config.yaml](stages/00init/config.yaml)

    $ diff stages/01podspec/config.yaml stages/02newconfigs/config.yaml

View the changes for [src/charm.py](stages/00init/src/charm.py)

    $ diff stages/01podspec/src/charm.py stages/02newconfigs/src/charm.py

Build and deploy. At this stage, you can use upgrade-charm instead of deploy.

    $ juju upgrade-charm training --path=./training.charm
    Added charm "local:kubernetes/training-1" to the model.

### 03 - Persistent storage (Kubernetes StatefulSets)
View the changes for [metadata.yaml](stages/00init/metadata.yaml)

    $ diff stages/02newconfigs/metadata.yaml stages/03storage/metadata.yaml

Build and redeploy. If you attempt to deploy after this change, you will see an
error message, because you cannot convert a traditional workload to a StatefulSet
in Kubernetes. You'll need to remove and redeploy the training application.

    $ juju remove-application training
    removing application training

### 04 - Add a relation
View the changes for [metadata.yaml](stages/00init/metadata.yaml)

    $ diff stages/03storage/metadata.yaml stages/04relation/metadata.yaml

View the changes for [src/charm.py](stages/00init/src/charm.py)

    $ diff stages/03storage/src/charm.py stages/04relation/src/charm.py

### 05 - Clusters and leadership
View the changes for [metadata.yaml](stages/00init/metadata.yaml)

    $ diff stages/04relation/metadata.yaml stages/05cluster/metadata.yaml

View the changes for [src/charm.py](stages/00init/src/charm.py)

    $ diff stages/04relation/src/charm.py stages/05cluster/src/charm.py

### 06 - Adding a unit test with harness
View the changes for [tests/test_charm.py](stages/00init/tests/test_charm.py)

    $ diff stages/05cluster/tests/test_charm.py stages/06harness/tests/test_charm.py

## Running Unit Tests

Create and activate a virtualenv, and install the development requirements, run
the testing helper script.

    $ cd stages/06harness
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements-dev.txt
    $ ./run_tests
