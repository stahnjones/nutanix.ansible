# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy


__metaclass__ = type


from .nutanix_database import NutanixDatabase
from .time_machines import TimeMachine


class Snapshot(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/snapshots"
        super(Snapshot, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "expiry": self._build_spec_expiry,
        }

    def create_snapshot(self, time_machine_uuid, data):
        endpoint = "{0}/{1}".format(time_machine_uuid, "snapshots")
        time_machine = TimeMachine(self.module)
        return time_machine.create(data=data, endpoint=endpoint)

    def get_snapshot(self, time_machine_uuid, name):
        snapshot_uuid, err = self.get_snapshot_uuid(time_machine_uuid, name)
        if err:
            return None, err
        return self.read(snapshot_uuid), None

    def get_snapshot_uuid(self, time_machine_uuid, name):
        endpoint = "snapshots"
        time_machine = TimeMachine(self.module)
        resp = time_machine.read(uuid=time_machine_uuid, endpoint=endpoint)

        snapshots_per_clusters = resp.get("snapshotsPerNxCluster", {})
        for _, snapshots_by_types in snapshots_per_clusters.items():
            for snapshots in snapshots_by_types:
                if snapshots.get("type") == "MANUAL":
                    for snapshot in snapshots.get("snapshots"):
                        if snapshot.get("name") == name:
                            return snapshot["id"], None
                    break

        return None, "Snapshot with name {0} not found".format(name)

    def _get_default_spec(self):
        return deepcopy({"name": ""})

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_expiry(self, payload, expiry):
        if not self.module.params.get("timezone"):
            return None, "timezone is required field for snapshot removal schedule"
        payload["lcmConfig"] = {
            "snapshotLCMConfig": {
                "expiryDetails": {
                    "expiryDateTimezone": self.module.params.get("timezone"),
                    "expireInDays": int(expiry),
                }
            }
        }
        return payload, None