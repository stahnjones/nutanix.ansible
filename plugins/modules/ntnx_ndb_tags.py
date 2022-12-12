#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.tags import Tag  # noqa: E402
from ..module_utils.utils import strip_extra_attrs  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        entity_type=dict(type="str", choices=["DATABASE", "CLONE", "TIME_MACHINE", "DATABASE_SERVER"], required=False),
        tag_value_required=dict(type="bool", required=False),
        status=dict(type="str", choices=["ENABLED", "DEPRECATED"], required=False) # deprecate will disallow tags addition
    )
    return module_args

def create_tags(module, result):
    tags = Tag(module)

    spec, err = tags.get_spec()
    if err:
        result["error"] = err
        return module.fail_json(msg="Failed generating tag create spec", **result)
    
    resp = tags.create(data=spec)
    result["response"] = resp
    result["changed"] = True
    result["uuid"] = resp.get("id")

def update_tags(module, result):
    tags = Tag(module)
    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="'uuid' is required field for update", **result)

    tag = tags.read(uuid=uuid)
    if not tag:
        module.fail_json(msg="Failed fetching tag info", **result)

    default_spec = tags.get_default_update_spec()
    tag = strip_extra_attrs(tag, default_spec)
    spec, err = tags.get_spec(old_spec=tag)
    if err:
        result["error"] = err
        return module.fail_json("Failed generating tag update spec", **result)
    
    resp = tags.update(uuid=uuid, data=spec)
    result["response"] = resp
    result["changed"] = True
    result["uuid"] = uuid

def delete_tags(module, result):
    tags = Tag(module)
    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="'uuid' is required field for delete", **result)
    
    resp = tags.delete(uuid=uuid)
    result["response"] = resp
    result["changed"] = True

def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "uuid"), True)],
        required_by={
            'status': 'uuid',
        },
        mutually_exclusive=[("uuid", "entity_type")]
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("state", "present") == "present":
        if module.params.get("uuid"):
            update_tags(module, result)
        else:
            update_tags(module, result)
    else:
        delete_tags(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()