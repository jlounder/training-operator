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
