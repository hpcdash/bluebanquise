# -*- coding: utf-8 -*-
#
# Make coding more python3-ish
# Original idea from Bruno Travouillon, @btravouillon

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native

# ClusterShell is only needed when the filter runs. Imported at load time, a
# controller without it would warn on every run that loads the filters of
# this collection, whatever filters the run uses.
try:
    from ClusterShell.NodeSet import NodeSet
    HAS_CLUSTERSHELL = True
except ImportError:
    HAS_CLUSTERSHELL = False


def nodeset(nodes_list):
    '''Convert a list of nodes to ClusterShell's NodeSet'''

    if not HAS_CLUSTERSHELL:
        raise AnsibleError('The nodeset filter needs the ClusterShell python module on the controller')

    try:
        nodeset = NodeSet(",".join(nodes_list))
    except Exception as e:
        raise AnsibleError('Error joining nodeset, original exception: %s' % to_native(e))

    return nodeset


class FilterModule(object):
    ''' NodeSet Jinja2 filter. '''

    def filters(self):
        return {
            'nodeset': nodeset,
        }
