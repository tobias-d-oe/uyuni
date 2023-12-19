#
# Licensed under the GNU General Public License Version 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (c) 2023 B1 Systems GmbH

import getpass
import gettext
import logging
from spacecmd.utils import *

translation = gettext.translation('spacecmd', fallback=True)
try:
    _ = translation.ugettext
except AttributeError:
    _ = translation.gettext


#################################################

def help_clm_projectlist(self):
    print(_('clm_projectlist: shows a list of clm projects'))
    print(_('usage: clm_projectlist'))

def do_clm_projectlist(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    clm_projects = self.client.contentmanagement.listProjects(self.session)
    for project in clm_projects:
        print(project['label'])


#################################################

def help_clm_projectlistenv(self):
    print(_('clm_projectlistenv: shows a list of environments configured in given project'))
    print(_('usage: clm_projectlistenv <PROJECT>'))

def complete_clm_projectlistenv(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectlistenv(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectlistenv()
        return 1

    proj = args.pop(0)

    clm_projects = self.client.contentmanagement.listProjectEnvironments(self.session, proj)
    for project in clm_projects:
        print(project['label'])


#################################################

def help_clm_projectlistsrc(self):
    print(_('clm_projectlistsrc: shows the sources used by given project'))
    print(_('usage: clm_projectlistsrc <PROJECT>'))

def complete_clm_projectlistsrc(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectlistsrc(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectlistsrc()
        return 1

    proj = args.pop(0)

    clm_projects = self.client.contentmanagement.listProjectSources(self.session, proj)
    for project in clm_projects:
        print(project['channelLabel'])


#################################################

def help_clm_projectlistfilter(self):
    print(_('clm_projectlistfilter: shows filters used by given project'))
    print(_('usage: clm_projectlistfilter <PROJECT>'))

def complete_clm_projectlistfilter(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectlistfilter(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectlistfilter()
        return 1

    proj = args.pop(0)

    clm_projects = self.client.contentmanagement.listProjectFilters(self.session, proj)
    
    for project in clm_projects:
        print(project['filter']['name'])


#################################################

def help_clm_filterlistcriterias(self):
    print(_('clm_filterlistcriterias: shows filtercriterias'))
    print(_('usage: clm_flterlistcriterias'))

def complete_clm_filterlistcriterias(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_filterlistcriterias(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    types = []
    clm_filter_crits = self.client.contentmanagement.listFilterCriteria(self.session)
    for crit in clm_filter_crits:
        if not crit['type'] in types:
            types.append(crit['type'])

    for type in types:
        print()
        print(_('Type %s:') % type)
        print('-------------')
        print('  {:30s}{:30s}'.format("[matcher]","[field]"))
        for crit in clm_filter_crits:
            if crit['type'] == type:
                print('  {:30s}{:30s}'.format(crit['matcher'],crit['field']))


#################################################

def help_clm_projectdetails(self):
    print(_('clm_projectdetails: details overview of a project'))
    print(_('usage: clm_projectdetails <PROJECT>'))

def complete_clm_projectdetails(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectdetails(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectdetails()
        return 1

    proj = args.pop(0)

    clm_project = self.client.contentmanagement.lookupProject(self.session, proj)
    print(_('Project details:'))
    print('----------------')
    print(_('Name:          %s') % clm_project['name'])
    print(_('Label:         %s') % clm_project['label'])
    print(_('Description:   %s') % clm_project['description'])
    print(_('First Env:     %s') % clm_project['firstEnvironment'])
    print(_('Last Build:    %s') % clm_project['lastBuildDate'])

    print()
    print(_('Sources:'))
    print('---------')
    clm_projects = self.client.contentmanagement.listProjectSources(self.session, proj)
    basechannels = self.list_base_channels()
    for project in clm_projects:
        if not project['channelLabel'] in basechannels:
            print('  |-- %s' % project['channelLabel'])
        else:
            print(project['channelLabel'])

    print()
    print(_('Filters:'))
    print('---------')
    clm_filters = self.client.contentmanagement.listProjectFilters(self.session, proj)
    for filter in clm_filters:
        print('- %s' % filter['filter']['name'])

    print()
    print(_('Environments:'))
    print('--------------')
    clm_projects = self.client.contentmanagement.listProjectEnvironments(self.session, proj)
    for project in clm_projects:
        print('- %s' % project['label'])


#################################################

def help_clm_projectbuild(self):
    print(_('clm_projectbuild: builds given project'))
    print(_('usage: clm_projectbuild <PROJECT>'))

def complete_clm_projectbuild(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectbuild(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectbuild()
        return 1

    proj = args.pop(0)
 
    print(_('Building project %s') % proj)
    clm_projectbuild = self.client.contentmanagement.buildProject(self.session, proj)


#################################################

def help_clm_projectpromote(self):
    print(_('clm_projectpromote: promotes a stage'))
    print(_('usage: clm_projectpromote <PROJECT> <ENVIRONMENT>'))

def complete_clm_projectpromote(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_env(parts[1],text)
    return None

def do_clm_projectpromote(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not args or len(args) != 2:
        self.help_clm_projectpromote()
        return 1

    proj = args.pop(0)
    env  = args.pop(0) 
 
    print(_('Promoting project %s environment %s') % (proj, env))
    clm_projectpromote = self.client.contentmanagement.promoteProject(self.session, proj, env)


#################################################

def help_clm_projectcreate(self):
    print(_('clm_projectcreate: create a new project'))
    print(_('usage: clm_project_create [options] <LABEL> <NAME> <DESCRIPTION>'))

def complete_clm_projectcreate(self, text, line, beg, end):
    return None

def do_clm_projectcreate(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if len(args) < 3:
        self.help_clm_projectcreate()
        return 1

    label = args[0]
    name = args[1]
    try:
        desc = args[2]
    except:
        desc = ""

    print(_('Creating project: %s') % (label))
    clm_projectpromote = self.client.contentmanagement.createProject(self.session, label, name, desc)


#################################################

def help_clm_projectattachesource(self):
    print(_('clm_projectattachesource: attaching softwarechannel to a given project'))
    print(_('usage: clm_projectattachesource [options] <PROJECT> <SOURCE> [<TYPE>="software"]'))


def complete_clm_projectattachesource(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    return None

def do_clm_projectattachesource(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if len(args) < 2:
        self.help_clm_projectattachesource()
        return 1

    proj = args[0]
    src = args[1]
    try:
        stype = args[2]
    except:
        stype = "software"

    print(_('Attaching source(s) to project %s:') % (proj))
    if src.split(','):
        for s in src.split(','):
            print("- %s" % s)
            clm_projectattachesrc = self.client.contentmanagement.attachSource(self.session, proj, stype, s)
    else:
        clm_projectattachesrc = self.client.contentmanagement.attachSource(self.session, proj, stype, src)
        print("- %s" % src)


#################################################

def help_clm_projectdetachesource(self):
    print(_('clm_projectdetachesource: detache softwarechannel from a new project'))
    print(_('usage: clm_projectdetachesource <PROJECT> <SOURCE> [<TYPE>="software"]'))

def complete_clm_projectdetachesource(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_src(parts[1],text)
    return None

def do_clm_projectdetachesource(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if len(args) < 2:
        self.help_clm_projectdetachesource()
        return 1

    proj = args[0]
    src = args[1]
    try:
        stype = args[2]
    except:
        stype = "software"

    print(_('Detaching source(s) from project %s:') % (proj))
    if src.split(','):
        for s in src.split(','):
            print("- %s" % s)
            clm_projectattachesrc = self.client.contentmanagement.detachSource(self.session, proj, stype, s)
    else:
        clm_projectattachesrc = self.client.contentmanagement.detachSource(self.session, proj, stype, src)
        print("- %s" % src)


#################################################

def help_clm_projectaddenv(self):
    print(_('clm_projectaddenv: create an new environment in a project'))
    print(_('usage: clm_projectaddenv [options] <PROJECT> <LABEL> <NAME> <DESRIPTION>'))

def complete_clm_projectaddenv(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    return None

def do_clm_projectaddenv(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not len(args) == 4:
        self.help_clm_projectaddenv()
        return 1

    proj = args[0]
    name = args[1]
    label = args[2]
    desc = args[3]

    clm_projects = self.client.contentmanagement.listProjectEnvironments(self.session, proj)
   
    try:
        last = clm_projects[len(clm_projects)-1]['label']
    except:
        last=''

    print(_('Creating Environment %s in project %s:') % (label, proj))
    clm_project = self.client.contentmanagement.createEnvironment(self.session, proj, last, label, name, desc)


#################################################

def help_clm_projectdelenv(self):
    print(_('clm_projectdelenv: remove an environment from a project'))
    print(_('usage: clm_projectdelenv <PROJECT> <ENVIRONMENT>'))

def complete_clm_projectdelenv(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_env(parts[1],text)
    return None

def do_clm_projectdelenv(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not len(args) == 2:
        self.help_clm_project_delenv()
        return 1
    proj = args[0]
    env = args[1]
    print(_('Remove Environment %s from project %s:') % (env, proj))
    clm_project = self.client.contentmanagement.removeEnvironment(self.session, proj, env)


#################################################

def help_clm_projectstagingfull(self):
    print(_('clm_projectstagingfull: move all stages further'))
    print(_('''usage: clm_projectstagingfull [options] <PROJECT>

options:
  -r (reverse mode)'''))


def complete_clm_projectstagingfull(self, text, line, beg, end):
    return self.tab_complete_clm_projects(text)

def do_clm_projectstagingfull(self, args):
    arg_parser = get_argument_parser()
    arg_parser.add_argument('-r', '--reverse', action='store_true', default=False)
    args, options = parse_command_arguments(args, arg_parser)

    if not args:
        self.help_clm_projectstagingfull()
        return 1

    proj = args[0]

    clm_envs = self.client.contentmanagement.listProjectEnvironments(self.session, proj)
    clm_envs.pop()

    if not options.reverse:
        print (_('Forward Staging'))
        build_done = False
        while not build_done:
            try:
                clm_projectbuild = self.client.contentmanagement.buildProject(self.session, proj)
                print (_('- bulding'))
                build_done = True
            except:
                time.sleep(5)

        for env in clm_envs:
            build_done = False
            while not build_done:
                try:
                    clm_projectpromote = self.client.contentmanagement.promoteProject(self.session, proj, env['label'])
                    print(_('- promoting %s ') % env['label'])
                    build_done = True
                except:
                    time.sleep(5)
    else: 
        clm_envs_rev = clm_envs[::-1]
        print (_('Reverse Staging'))
        for env in clm_envs_rev: 

            build_done = False
            while not build_done:
                try:
                    clm_projectpromote = self.client.contentmanagement.promoteProject(self.session, proj, env['label'])
                    print(_('- promoting %s') % env['label'])
                    build_done = True
                except:
                    time.sleep(5)

        build_done = False
        while not build_done:
            try:
                clm_projectbuild = self.client.contentmanagement.buildProject(self.session, proj)
                print (_('- bulding'))
                build_done = True
            except:
                time.sleep(5)


#################################################

def help_clm_filterlist(self):
    print(_('clm_filterlist: shows a list of configured filters'))
    print(_('usage: clm_filterlist'))

def complete_clm_filterlist(self, text, line, beg, end):
    return None

def do_clm_filterlist(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    clm_filters = self.client.contentmanagement.listFilters(self.session)
    print(_('Filterlist:'))
    print('-----------')
    if not clm_filters:
        print(_('No filters configured'))
    else:
        print('  {:30s}{:15s}{:10s}{:30s}{:30s}{:30s}'.format('[name]',
                                                              '[type]',
                                                              '[rule]',
                                                              '[field]',
                                                              '[matcher]',
                                                              '[value]'))
        for filter in clm_filters:
            print('  {:30s}{:15s}{:10s}{:30s}{:30s}{:30s}'.format(filter['name'],
                                                                  filter['entityType'],
                                                                  filter['rule'],
                                                                  filter['criteria']['field'],
                                                                  filter['criteria']['matcher'],
                                                                  filter['criteria']['value']))


#################################################

def help_clm_filtercreate(self):
    print(_('clm_filtercreate: create a new filter'))
    print(_('usage: clm_filtercreate <NAME> <RULE> <TYPE> <FIELD> <MATCHER> <VALUE>'))

def complete_clm_filtercreate(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 3:
        return self.tab_complete_filter_rule(text)
    elif len(parts) == 4:
        return self.tab_complete_filter_type(text)
    elif len(parts) == 6:
        return self.tab_complete_filter_matcher(parts[3],text)
    return None

def do_clm_filtercreate(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not len(args) == 6:
        self.help_clm_filtercreate()
        return 1

    name = args[0]
    rule = args[1]
    entityType = args[2]

    criteria = {'matcher': args[4], 'field': args[3], 'value': args[5]}

    clm_filtercreate = self.client.contentmanagement.createFilter(self.session, name, rule, entityType, criteria)


#################################################

def help_clm_projectattachefilter(self):
    print(_('clm_projectattachefilter: attache a filter to a project'))
    print(_('usage: clm_projectattachefilter <PROJECT> <FILTER>'))

def complete_clm_projectattachefilter(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_filters(text)
    return None

def do_clm_projectattachefilter(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    projectLabel = args[0]
    filterName = args[1]

    filterId = -1
    clm_filters = self.client.contentmanagement.listFilters(self.session)
    for filter in clm_filters:
        if filter['name'] == filterName:
            filterId = filter['id']
            break

    if filterId != -1:
        print(_('Attache filter %s(%i) to project %s') % (filterName,filterId,projectLabel))
        clm_filterattache = self.client.contentmanagement.attachFilter(self.session, projectLabel, filterId)


#################################################

def help_clm_projectdetachefilter(self):
    print(_('clm_projectdetachefilter: detache a filter from a project'))
    print(_('usage: clm_projectdetachefilter <PROJECT> <FILTER>'))

def complete_clm_projectdetachefilter(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_projectfilters(parts[1],text)
    return None

def do_clm_projectdetachefilter(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    projectLabel = args[0]
    filterName = args[1]


    clm_filters = self.client.contentmanagement.listProjectFilters(self.session, projectLabel)

    filterId = -1
    for filter in clm_filters:
        if filter['filter']['name'] == filterName:
            filterId = filter['filter']['id']
            break

    if filterId != -1:
        print(_('Dettache filter %s(%i) from project %s') % (filterName,filterId,projectLabel))
        clm_filterattache = self.client.contentmanagement.detachFilter(self.session, projectLabel, filterId)


#################################################

def help_clm_filtercreateappstream(self):
    print(_('clm_filtercreateappstream: create a new appstream filter'))
    print(_('usage: clm_filtercreateappstream <PROJECT> <CHANNEL> <PREFIX>'))

def complete_clm_filtercreateappstream(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_src(parts[1],text)
    return None

def do_clm_filtercreateappstream(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not len(args) == 3:
        self.help_clm_filtercreateappstream()
        return 1

    projectLabel = args[0]
    channelLabel = args[1]
    prefix = args[2]
    clm_filtercreate = self.client.contentmanagement.createAppStreamFilters(self.session, prefix, channelLabel, projectLabel)


#################################################

def help_clm_projectstatus(self):
    print(_('clm_projectstatus: shows build state of a project'))
    print(_('usage: clm_projectstatus <PROJECT>'))

def complete_clm_projectstatus(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    return None

def do_clm_projectstatus(self, args):
    arg_parser = get_argument_parser()
    args, options = parse_command_arguments(args, arg_parser)

    if not len(args) == 1:
        self.help_clm_projectstatus()
        return 1

    projectLabel = args[0]
    clm_envs = self.client.contentmanagement.listProjectEnvironments(self.session, projectLabel)
    if not self.options.quiet:
        print('{:30s}{:15s}{:9s} {:19s} '.format("[label]","[status]","[version]","[buildtime]"))
        print('-'*74)
    for env in clm_envs:
        lastbuild = env['lastBuildDate']
        dt = datetime.strptime(str(lastbuild), '%Y%m%dT%H:%M:%S')
        if not self.options.quiet:
            print('{:30s}{:15s}{:9d} {:19s} '.format(env['label'],env['status'],env['version'],str(dt)))
        else:
            print('{},{},{},{} '.format(env['label'],env['status'],str(env['version']),str(dt)))


#################################################

def help_clm_envdiff(self):
    print(_('clm_envdiff: shows differences between project environments'))
    print(_('usage: clm_envdiff <PROJECT> <ENV1> <ENV2>'))

def complete_clm_envdiff(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return self.tab_complete_clm_projects(text)
    elif len(parts) == 3:
        return self.tab_complete_clm_env(parts[1],text)
    elif len(parts) == 4:
        return self.tab_complete_clm_env(parts[1],text)

    return None


def do_clm_envdiff(self, args):
    arg_parser = get_argument_parser()

    (args, _options) = parse_command_arguments(args, arg_parser)

    if len(args) != 2 and len(args) != 3:
        self.help_clm_envdiff()
        return None

    proj = args[0]
    if not proj in self.tab_complete_clm_projects(""):
        self.help_clm_envdiff()
        return None

    env1 = args[1]
    env2 = args[2]
   
    package_diff = []

    clm_projects = self.client.contentmanagement.listProjectSources(self.session, proj)
    for project in clm_projects:
        src_chan = proj + '-' + env1 + '-' +project['channelLabel']
        dst_chan = proj + '-' + env2 + '-' + project['channelLabel']
        print(_('Analyzing differences : '+src_chan+' -> '+dst_chan))

        if not self.check_softwarechannel(src_chan) or not self.check_softwarechannel(dst_chan):
            self.help_clm_envdiff()
            return None

        source_data = self.dump_softwarechannel(src_chan, None)
        target_data = self.dump_softwarechannel(dst_chan, None)
        for line in diff(source_data, target_data, src_chan, dst_chan):
            if line.startswith('-') and not line.startswith('---') or line.startswith('+') and not line.startswith('+++'):
                package_diff.append(line)
    print()
    if not len(package_diff) == 0:
        print(_('Differences found:'))
        for p in package_diff:
            print(p)
    else:
        print(_('No differences found'))
