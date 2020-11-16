#!/usr/bin/env python3
# Copyright 2020 Jeremy Lounder
# See LICENSE file for licensing details.

import logging
import textwrap

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class TrainingCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(
            self.on["grafana-dashboard"].relation_joined, self._on_dashboard_joined
        )
        self.framework.observe(
            self.on["grafana-dashboard"].relation_changed, self._on_dashboard_changed
        )
        self.framework.observe(
            self.on["grafana-dashboard"].relation_broken, self._on_dashboard_broken
        )
        self._stored.set_default(dashboards=dict())

    def _on_config_changed(self, _=None):
        pod_spec = self._build_pod_spec()
        self.model.pod.set_spec(pod_spec)
        self.unit.status = ActiveStatus("Grafana pod ready.")

    def _build_pod_spec(self):
        port = self.model.config["grafana_port"]
        config_content = self._build_grafana_ini()
        spec = {
            "containers": [
                {
                    "name": self.app.name,
                    "imageDetails": {"imagePath": "grafana/grafana:7.2.1-ubuntu"},
                    "ports": [{"containerPort": port, "protocol": "TCP"}],
                    "readinessProbe": {
                        "httpGet": {"path": "/api/health", "port": port},
                        "initialDelaySeconds": 10,
                        "timeoutSeconds": 30,
                    },
                    "files": [
                        {
                            "name": "grafana-config-ini",
                            "mountPath": "/etc/grafana",
                            "files": {"grafana.ini": config_content},
                        }
                    ],
                    "config": {},  # used to store hashes of config file text
                }
            ]
        }

        return spec

    def _build_grafana_ini(self):
        config_text = textwrap.dedent(
            """
            [server]
            http_port = {0}

            [security]
            admin_user = {1}
            admin_password = {2}
            """.format(
                self.model.config["grafana_port"],
                self.model.config["admin_username"],
                self.model.config["admin_password"],
            )
        )
        return config_text

    def _on_dashboard_joined(self, event):
        ingress_ip = self.model.get_binding(event.relation).network.ingress_address
        ingress_port = self.model.config["grafana_port"]
        grafana_host = "{}:{}".format(ingress_ip, ingress_port)
        event.relation.data[self.app].update({"host": grafana_host})

        private_ip = str(self.model.get_binding(event.relation).network.bind_address)
        event.relation.data[self.unit].update({"private_address": private_ip})

    def _on_dashboard_changed(self, event):
        if event.unit is None:
            return

        dashboard = event.relation.data[event.app].get("dashboard")
        if dashboard is None:
            return

        self._stored.dashboards.update({event.relation.id: dashboard})
        self._on_config_changed()

    def _on_dashboard_broken(self, event):
        self._stored.dashboards.pop(event.relation.id, None)
        self._on_config_changed()


if __name__ == "__main__":
    main(TrainingCharm)
