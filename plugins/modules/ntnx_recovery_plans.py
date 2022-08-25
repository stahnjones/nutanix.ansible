#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_recovery_plans
short_description: module which supports recovery_plans CRUD operations
version_added: 1.5.0
description: 'Create, Update, Delete Recovery Plan'
options:
  plan_uuid:
    description: recovery_plan uuid
    type: str
    required: false
  name:
    description: Recovery Plan name
    type: str
    required: false
  desc:
    description: A description for the Recovery Plan.
    type: str
    required: false
  stages:
    type: list
    elements: dict
    description:
      - >-
        Input for the stages of the Recovery Plan. Each stage will perform a
        predefined type of task. For example, a stage can perform the recovery
        of the entities specified in a stage.
      - During update it given stages will override all existing stages
    required: false
    suboptions:
      vms:
        type: list
        elements: dict
        description: vms to be recovered in current stage
        required: false
        suboptions:
          uuid:
            description:
              - uuid of vm
              - mutually exclusive with C(name)
            type: str
            required: false
          name:
            description:
              - name of vm
              - mutually exclusive with C(uuid)
            type: str
            required: false
          enable_script_exec:
            description:
              - this will enable scripts execution post recovery for vm
              - >-
                Nutanix Guest Tools must be installed on the VMs to enable
                scripts.
            type: bool
            required: false
      categories:
        type: list
        elements: dict
        description: Categories for filtering entities.
        required: false
        suboptions:
          key:
            description: category key
            type: str
            required: false
          value:
            description: category value
            type: str
            required: false
          enable_script_exec:
            description:
              - this will enable scripts execution post recovery for vm
              - >-
                Nutanix Guest Tools must be installed on the VMs to enable
                scripts.
            type: bool
            required: false
      delay:
        description: >-
          Amount of time in seconds to delay the execution of next stage after
          execution of current stage.
        type: int
        required: false
  primary_location:
    description: primary site
    type: dict
    required: false
    suboptions:
      url:
        description: availability zone url
        type: str
        required: true
      cluster:
        description: specific cluster uuid
        type: str
        required: false
  recovery_location:
    description: recovery site
    type: dict
    required: false
    suboptions:
      url:
        description: availability zone url
        type: str
        required: true
      cluster:
        description: specific cluster uuid
        type: str
        required: false
  network_mappings:
    type: list
    elements: dict
    description:
      - list of network mappings
      - during update given list will override all existing network mappings
    required: false
    suboptions:
      primary:
        description: primary site networks for particular mapping
        type: dict
        required: true
        suboptions:
          test:
            description: Test network
            type: dict
            required: false
            suboptions:
              name:
                description: name of subnet
                type: str
                required: true
              gateway_ip:
                description: gateway ip of subnet incase of IPAM
                type: str
                required: false
              prefix:
                description: network prefix for subnet
                type: int
                required: false
              external_connectivity_state:
                description: if external connectivity is enabled
                type: bool
                required: false
              custom_ip_conifg:
                description: configure custom ip assignment for vm after recovery
                type: list
                elements: dict
                required: false
                suboptions:
                  vm:
                    description: vm spec
                    type: dict
                    required: true
                    suboptions:
                      uuid:
                        description:
                          - uuid of vm
                          - mutually exclusive with C(name)
                        type: str
                        required: false
                      name:
                        description:
                          - name of vm
                          - mutually exclusive with C(uuid)
                        type: str
                        required: false
                  ip:
                    description: ip address to be assigned to vm
                    type: str
                    required: true
          prod:
            description: production network
            type: dict
            required: false
            suboptions:
              name:
                description: name of subnet
                type: str
                required: true
              gateway_ip:
                description: gateway ip of subnet incase of IPAM
                type: str
                required: false
              prefix:
                description: network prefix for subnet
                type: int
                required: false
              external_connectivity_state:
                description: if external connectivity is enabled
                type: bool
                required: false
              custom_ip_conifg:
                description: configure custom ip assignment for vm after recovery
                type: list
                elements: dict
                required: false
                suboptions:
                  vm:
                    description: vm spec
                    type: dict
                    required: true
                    suboptions:
                      uuid:
                        description:
                          - uuid of vm
                          - mutually exclusive with C(name)
                        type: str
                        required: false
                      name:
                        description:
                          - name of vm
                          - mutually exclusive with C(uuid)
                        type: str
                        required: false
                  ip:
                    description: ip address to be assigned to vm
                    type: str
                    required: true
      recovery:
        description:
          - >-
            Network configuration to be used for performing network mapping and
            IP preservation/mapping on Recovery Plan execution.
          - primary site networks for particular mapping
        type: dict
        required: true
        suboptions:
          test:
            description: Test network
            type: dict
            required: false
            suboptions:
              name:
                description: name of subnet
                type: str
                required: true
              gateway_ip:
                description: gateway ip of subnet incase of IPAM
                type: str
                required: false
              prefix:
                description: network prefix for subnet
                type: int
                required: false
              external_connectivity_state:
                description: if external connectivity is enabled
                type: bool
                required: false
          prod:
            description: production network
            type: dict
            required: false
            suboptions:
              name:
                description: name of subnet
                type: str
                required: true
              gateway_ip:
                description: gateway ip of subnet incase of IPAM
                type: str
                required: false
              prefix:
                description: network prefix for subnet
                type: int
                required: false
              external_connectivity_state:
                description: if external connectivity is enabled
                type: bool
                required: false
              custom_ip_conifg:
                description: configure custom ip assignment for vm after recovery
                type: list
                elements: dict
                required: false
                suboptions:
                  vm:
                    description: vm spec
                    type: dict
                    required: true
                    suboptions:
                      uuid:
                        description:
                          - uuid of vm
                          - mutually exclusive with C(name)
                        type: str
                        required: false
                      name:
                        description:
                          - name of vm
                          - mutually exclusive with C(uuid)
                        type: str
                        required: false
                  ip:
                    description: ip address to be assigned to vm
                    type: str
                    required: true
  network_type:
    description: network type
    type: str
    required: false
    choices:
      - STRETCH
      - NON_STRETCH
  floating_ip_assignments:
    type: list
    elements: dict
    description: >-
      Floating IP assignment for VMs upon recovery in an Availability Zone. This
      is applicable only for the public cloud Availability Zones.
    required: false
    suboptions:
      availability_zone_url:
        description: URL of the Availability Zone.
        type: str
        required: true
      vm_ip_assignments:
        description: >-
          IP assignment for VMs upon recovery in the specified Availability
          Zone.
        type: list
        elements: dict
        required: true
        suboptions:
          vm:
            description: The reference to a vm
            type: dict
            required: true
            suboptions:
              name:
                description:
                  - VM name
                  - mutually exclusive with C(uuid)
                type: str
                required: false
              uuid:
                description:
                  - VM UUID
                  - mutually exclusive with C(name)
                type: str
                required: false
          vm_nic_info:
            description: Information about vnic to which floating IP has to be assigned.
            type: dict
            required: true
            suboptions:
              ip:
                description: >-
                  IP address associated with vnic for which floating IP has to
                  be assigned on failover.
                type: str
                required: false
              uuid:
                description: >-
                  Uuid of the vnic of the VM to which floating IP has to be
                  assigned.
                type: str
                required: true
          test_ip_config:
            description: >-
              Configuration for assigning floating IP to a VM on the execution
              of the Recovery Plan.
            type: dict
            required: false
            suboptions:
              ip:
                description: 'IP to be assigned to VM, in case of failover.'
                type: str
                required: true
              allocate_dynamically:
                description: Whether to allocate the floating IPs for the VMs dynamically.
                type: bool
                required: false
          prod_ip_config:
            description: >-
              Configuration for assigning floating IP to a VM on the execution
              of the Recovery Plan.
            type: dict
            required: false
            suboptions:
              ip:
                description: 'IP to be assigned to VM, in case of failover.'
                type: str
                required: true
              allocate_dynamically:
                description: Whether to allocate the floating IPs for the VMs dynamically.
                type: bool
                required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create recovery plan
  ntnx_recovery_plans:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    state: "present"
    name: test-integration-rp-updated
    desc: test-integration-rp-desc-updated
    stages:
      - vms:
          - name: "{{dr_vm_name}}"
            enable_script_exec: true
        categories:
          - key: Environment
            value: Production
            enable_script_exec: true
        delay: 2
      - categories:
          - key: Environment
            value: Dev
    primary_location:
      url: "{{primary_az_url}}"
    recovery_location:
      url: "{{recovery_az_url}}"
    network_type: NON_STRETCH
    network_mappings:
      - primary:
          test:
            name: "{{static.name}}"
            gateway_ip: "{{static.gateway_ip}}"
            prefix: "{{static.network_prefix}}"
          prod:
            name: "{{static.name}}"
            gateway_ip: "{{static.gateway_ip}}"
            prefix: "{{static.network_prefix}}"
        recovery:
          test:
            name: "{{dr.recovery_site_network}}"
          prod:
            name: "{{dr.recovery_site_network}}"

- name: Update stage categories
  check_mode: yes
  ntnx_recovery_plans:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    plan_uuid: "{{plan_uuid}}"
    state: "present"
    name: test-integration-rp-updated
    desc: test-integration-rp-desc-updated
    stages:
      - vms:
          - name: "{{dr_vm_name}}"
            enable_script_exec: true
        categories:
          - key: Environment
            value: Staging
            enable_script_exec: true
        delay: 2
      - categories:
          - key: Environment
            value: Testing

- name: Delete created recovery plans
  ntnx_recovery_plans:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    wait: True
    plan_uuid: "{{ recovery_plan2.plan_uuid }}"
  register: result

"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.recovery_plans import RecoveryPlan  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


# TO-DO: Test floating IP assignments
def get_module_spec():

    vm_spec = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        enable_script_exec=dict(type="bool", required=False),
    )
    entity_by_spec = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
    )
    category = dict(
        key=dict(type="str", required=False, no_log=True),
        value=dict(type="str", required=False),
        enable_script_exec=dict(type="bool", required=False),
    )
    stage = dict(
        vms=dict(
            type="list",
            elements="dict",
            options=vm_spec,
            mutually_exclusive=[("name", "uuid")],
            required=False,
        ),
        categories=dict(type="list", elements="dict", options=category, required=False),
        delay=dict(type="int", required=False),
    )
    availability_zone = dict(
        url=dict(type="str", required=True), cluster=dict(type="str", required=False)
    )
    custom_ip_config = dict(
        vm=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=[("name", "uuid")],
            required=True,
        ),
        ip=dict(type="str", required=True),
    )
    network = dict(
        name=dict(type="str", required=True),
        gateway_ip=dict(type="str", required=False),
        prefix=dict(type="int", required=False),
        external_connectivity_state=dict(type="bool", required=False),
        custom_ip_conifg=dict(
            type="list", elements="dict", options=custom_ip_config, required=False
        ),
    )
    site_network = dict(
        test=dict(type="dict", option=network, required=False),
        prod=dict(type="dict", option=network, required=False),
    )
    network_mapping = dict(
        primary=dict(type="dict", options=site_network, required=True),
        recovery=dict(type="dict", options=site_network, required=True),
    )
    floating_ip_config = dict(
        ip=dict(type="str", required=True),
        allocate_dynamically=dict(type="bool", required=False),
    )
    vm_nic_info = dict(
        uuid=dict(type="str", required=True), ip=dict(type="str", required=False)
    )
    vm_ip_assignment_config = dict(
        vm=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=[("name", "uuid")],
            required=True,
        ),
        vm_nic_info=dict(type="dict", options=vm_nic_info, required=True),
        test_ip_config=dict(type="dict", options=floating_ip_config, required=False),
        prod_ip_config=dict(type="dict", options=floating_ip_config, required=False),
    )
    floating_ip_assignment = dict(
        availability_zone_url=dict(type="str", required=True),
        vm_ip_assignments=dict(
            type="list", elements="dict", options=vm_ip_assignment_config, required=True
        ),
    )
    module_args = dict(
        plan_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        stages=dict(type="list", elements="dict", options=stage, required=False),
        primary_location=dict(type="dict", options=availability_zone, required=False),
        recovery_location=dict(type="dict", options=availability_zone, required=False),
        network_mappings=dict(
            type="list", elements="dict", options=network_mapping, required=False
        ),
        network_type=dict(
            type="str", choices=["STRETCH", "NON_STRETCH"], required=False
        ),
        floating_ip_assignments=dict(
            type="list", elements="dict", options=floating_ip_assignment, required=False
        ),
    )
    return module_args


def create_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    name = module.params["name"]
    if recovery_plan.get_uuid(name):
        module.fail_json(msg="Recovery Plan with given name already exists", **result)

    spec, error = recovery_plan.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create recovery plan spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = recovery_plan.create(spec)
    uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["plan_uuid"] = uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = recovery_plan.read(uuid)

    result["response"] = resp


def check_recovery_plan_idempotency(old_spec, update_spec):

    if old_spec["spec"]["name"] != update_spec["spec"]["name"]:
        return False

    if old_spec["spec"]["description"] != update_spec["spec"]["description"]:
        return False

    # each element of network_mappings have to checked as order of mappings is not significant in this case
    old_ntw_mappings = old_spec["spec"]["resources"]["parameters"][
        "network_mapping_list"
    ]
    update_ntw_mappings = update_spec["spec"]["resources"]["parameters"][
        "network_mapping_list"
    ]

    if len(old_ntw_mappings) != len(update_ntw_mappings):
        return False
    for mapping in update_ntw_mappings:
        if mapping not in old_ntw_mappings:
            return False

    # comparing floating IP assignments
    old_ip_assignments = old_spec["spec"]["resources"]["parameters"].get(
        "floating_ip_assignment_list", []
    )
    update_ip_assignments = update_spec["spec"]["resources"]["parameters"].get(
        "floating_ip_assignment_list", []
    )

    if len(old_ip_assignments) != len(update_ip_assignments):
        return False
    for config in update_ip_assignments:
        if config not in old_ip_assignments:
            return False

    # comparing availibility zones
    if (
        old_spec["spec"]["resources"]["parameters"]["availability_zone_list"]
        != update_spec["spec"]["resources"]["parameters"]["availability_zone_list"]
    ):
        return False

    # comparing stage list
    if (
        old_spec["spec"]["resources"]["stage_list"]
        != update_spec["spec"]["resources"]["stage_list"]
    ):
        return False

    return True


def update_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    plan_uuid = module.params.get("plan_uuid")
    result["plan_uuid"] = plan_uuid

    resp = recovery_plan.read(uuid=plan_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")
    # remove stage_uuid of all stages
    for stage in resp["spec"]["resources"]["stage_list"]:
        stage.pop("stage_uuid")

    update_spec, error = recovery_plan.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan update spec", **result)

    # check for idempotency
    if check_recovery_plan_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = recovery_plan.update(data=update_spec, uuid=plan_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = recovery_plan.read(uuid=plan_uuid)

    result["response"] = resp


def delete_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    plan_uuid = module.params["plan_uuid"]
    resp = recovery_plan.delete(uuid=plan_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        resp = tasks.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():

    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "plan_uuid"), True),
            ("state", "present", ("stages", "plan_uuid"), True),
            ("state", "present", ("primary_location", "plan_uuid"), True),
            ("state", "present", ("recovery_location", "plan_uuid"), True),
            ("state", "present", ("network_mappings", "plan_uuid"), True),
            ("state", "present", ("network_type", "plan_uuid"), True),
            ("state", "absent", ("plan_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "plan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("plan_uuid"):
            update_recovery_plan(module, result)
        else:
            create_recovery_plan(module, result)
    else:
        delete_recovery_plan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
