# Copyright 2014
# Cisco, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cloudpulseclient.openstack.common import cliutils as utils


def _print_list_field(field):
    return lambda obj: ', '.join(getattr(obj, field))


def do_result(cs, args):
    healtchecks = cs.healthcheck.list()
    columns = ('uuid', 'id', 'name', 'testtype', 'state')
    utils.print_list(healtchecks, columns,
                     {'versions': _print_list_field('versions')})


@utils.arg('--name',
           metavar='<name>',
           required=True,
           help='Name of the healthcheck to create.')
@utils.arg('--state',
           required=True,
           metavar='<state>',
           help='state of the healthcheck')
@utils.arg('--id',
           required=True,
           metavar='<id>',
           help='id of the healthcheck')
def do_run(cs, args):
    opts = {}
    opts['name'] = args.name
    opts['id'] = args.id
    opts['state'] = args.state
    healtcheck = cs.healthcheck.create(**opts)
    utils.print_dict(healtcheck._info)


@utils.arg('cpulse',
           metavar='<cpulse>',
           nargs='+',
           help='ID or name of the (cpulse)s to delete.')
def do_show(cs, args):
    for id in args.cpulse:
        healthcheck = cs.healthcheck.get(id)
        utils.print_dict(healthcheck._info)


@utils.arg('cpulse',
           metavar='<cpulse>',
           nargs='+',
           help='ID or name of the (cpulse)s to delete.')
def do_delete(cs, args):
    for id in args.cpulse:
        try:
            cs.healthcheck.delete(id)
        except Exception as e:
            print("Delete for cpulse %(cpulse)s failed: %(e)s" %
                  {'cpulse': id, 'e': e})