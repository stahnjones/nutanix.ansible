#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_scale
short_description: module for scaling database instance
version_added: 1.8.0
description: 
    - module for scaling database instance
    - currently, extension of database storage is only supported
options:
      pre_update_cmd:
        description:
            - complete OS command that you want to run before scaling
        type: str
      post_update_cmd:
        description:
            - complete OS command that you want to run post scaling
        type: str
      storage_gb:
        description:
            - storage to be added in GB
        type: int
        required: true
      db_uuid:
        description:
            - database instance uuid
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""
RETURN = r"""


"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        db_uuid=dict(type="str", required=True),
        storage_gb=dict(type="int", required=True),
        pre_update_cmd=dict(type="str", required=False),
        post_update_cmd=dict(type="str", required=False),
    )
    return module_args


def scale_db_instance(module, result):
    _databases = DatabaseInstance(module)
    uuid = module.params.get("db_uuid")
    if not uuid:
        module.fail_json(msg="db_uuid is required field for scaling", **result)

    resp = _databases.read(uuid)
    result["response"] = resp

    database_type = resp.get("type")
    if not database_type:
        module.fail_json(msg="failed fetching database type", **result)

    spec = _databases.get_scaling_spec(
        scale_config=module.params, database_type=database_type
    )

    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.scale(uuid=uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True
    result["db_uuid"] = uuid


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}

    scale_db_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
