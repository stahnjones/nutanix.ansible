#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_slas_info
short_description: sla  info module
version_added: 1.8.0-beta.1
description: 'Get sla info'
options:
      name:
        description:
            - sla name
        type: str
      uuid:
        description:
            - sla id
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.slas import SLA  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_sla(module, result):
    sla = SLA(module)
    resp, err = sla.get_sla(
        uuid=module.params.get("uuid"), name=module.params.get("name")
    )

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching sla info", **result)
    result["response"] = resp


def get_slas(module, result):
    sla = SLA(module)

    resp = sla.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_sla(module, result)
    else:
        get_slas(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
