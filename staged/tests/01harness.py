# Copyright 2020 Jeremy Lounder
# See LICENSE file for licensing details.

import unittest
# from unittest.mock import Mock

from ops.testing import Harness
from charm import TrainingCharm


class TestCharm(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = Harness(TrainingCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test__grafana_port_config_changed(self):
        self.harness.set_leader(True)
        self.harness.update_config({"grafana_port": 4000})
        pod_spec = self.harness.get_pod_spec()[0]
        self.assertEqual(pod_spec["containers"][0]["ports"][0]["containerPort"], 4000)
        self.assertEqual(pod_spec["containers"][0]["readinessProbe"]["httpGet"]["port"], 4000)
