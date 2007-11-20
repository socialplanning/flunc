"""setuptool command for flunc"""
from setuptools import Command
import pkg_resources
from pkg_resources import resource_filename, Requirement
from flunc import get_optparser, main as run_flunc
import sys

def convert_to_useroptions(optparser):
    """adapted from nose"""
    user_opts = []
    for opt in optparser.option_list:
        long_opt = opt._long_opts[0][2:]
        if opt.action != 'store_true':
            long_opt = long_opt + "="
        short_opt = None
        if opt._short_opts:
            short_opt =  opt._short_opts[0][1:]
        user_opts.append((long_opt, short_opt, opt.help or ""))
    return user_opts


class ftest_runner(Command):
    """subclassable command to run flunc tests for a package where
    ftests"""
    description = "run flunc tests"

    resource_name = 'ftests'
    flunc_opts, description = get_optparser()
    user_options = convert_to_useroptions(flunc_opts)
    user_options.append(('suite', 't', 'name of test suite to run'))

    _defaults = flunc_opts.defaults
    
    @property
    def test_dir(self):
        return resource_filename(Requirement.parse(self.distribution.get_name()), self.resource_name)

    def initialize_options(self):
        """create the member variables, but change hyphens to underscores"""
        self.option_to_cmds = {}
        self._defaults['path'] = self.test_dir
        for opt in self.flunc_opts.option_list:
            cmd_name = opt._long_opts[0][2:]
            option_name = cmd_name.replace('-', '_')
            self.option_to_cmds[option_name] = cmd_name
            default = self._defaults.get(cmd_name)
            setattr(self, option_name, default)
        self.suite = 'all'
        self.attr  = None

    def finalize_options(self):
        pass

    def run(self):
        if self.distribution.ftest_require:
            self.distribution.fetch_build_eggs(self.distribution.ftest_require)

        # add stuff for niceties, like checking if port is open for
        # test etc

        argv = []
        for (option_name, cmd_name) in self.option_to_cmds.items():
            if option_name == 'suite':
                continue
            value = getattr(self, option_name)
            if value is not None:
                option_name = option_name.replace('_', '-')
                argv.extend(serialize_opt(option_name, value))
                
        argv.insert(0, self.suite)
        argv.insert(0, 'setup.py')
        run_flunc(argv=argv)

# adapted from nose

def serialize_opt(optname, value):
    argv = []
    if flag(value):
        if bool_(value):
            argv.append('--' + optname)
    else:
        argv.append('--' + optname)
        argv.append(value)
    return argv

def flag(val):
    """Does the value look like an on/off flag?"""
    if not isinstance(val, basestring):
        val = str(val)
    if len(val) > 5:
        return False
    return val.upper() in ('1', '0', 'F', 'T', 'TRUE', 'FALSE', 'ON', 'OFF')

def bool_(val):
    if not isinstance(val, basestring):
        val = str(val)
    return val.upper() in ('1', 'T', 'TRUE', 'ON')

