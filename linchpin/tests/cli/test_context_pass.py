import os

from nose.tools import *

import logging
from unittest import TestCase

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.cli.context import LinchpinCliContext
from linchpin.tests.mockdata.contextdata import ContextData


def test_context_create():

    lpc = LinchpinCliContext()
    assert_equal(isinstance(lpc, LinchpinCliContext), True)


def setup_context_data():

    """
    Perform setup of ContextData() object, and run get_temp_filename()
    """

    global config_path
    global config_data
    global evars_data
    global logfile

    cd = ContextData()
    cd.load_config_data()
    cd.parse_config()
    evars_data = cd.evars
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data

    logfile = cd.logfile
    cd.write_config_file(config_path)


@with_setup(setup_context_data)
def test_load_config():

    lpc = LinchpinCliContext()
    lpc.load_config(lpconfig=config_path)

#    assert_dict_equal.__self__.maxDiff = None
    assert_dict_equal(config_data, lpc.cfgs)


@with_setup(setup_context_data)
def test_get_cfg():

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    cfg_value = lpc.get_cfg('hookstates', 'up')

    assert_equal(cfg_value, config_data['hookstates']['up'])


@with_setup(setup_context_data)
def test_set_cfg():

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.set_cfg('test', 'key', 'value')

    assert_equal(lpc.get_cfg('test', 'key'), lpc.cfgs['test']['key'])


@with_setup(setup_context_data)
def test_load_global_evars():

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.load_global_evars()

    assert_dict_equal(evars_data, lpc.evars)


@with_setup(setup_context_data)
def test_get_evar():

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.load_global_evars()
    evar_value = lpc.get_evar('_async')

    assert_equal(evar_value, evars_data['_async'])


@with_setup(setup_context_data)
def test_set_evar():

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.load_global_evars()
    lpc.set_evar('test', 'me')

    assert_equal('me', lpc.evars['test'])


@with_setup(setup_context_data)
def test_logging_setup():


    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.setup_logging()

    assert os.path.isfile(logfile)


@with_setup(setup_context_data)
def test_log_msg():

    # This test assumes the default message format found around line 139
    # of linchpin/cli/context.py

    lvl=logging.DEBUG
    msg = 'Test Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.setup_logging()
    lpc.log(msg, level=lvl)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_context_data)
def test_log_state():

    lvl=logging.DEBUG
    msg = '{0}: State Msg'.format(logging.getLevelName(lvl))
    regex = '^{0}.*STATE - {1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.setup_logging()
    lpc.log_state(msg)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_context_data)
def test_log_info():

    lvl=logging.INFO
    msg = 'Info Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.setup_logging()
    lpc.log_info(msg)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_context_data)
def test_log_debug():

    lvl=logging.DEBUG
    msg = 'Debug Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(config_path)
    lpc.setup_logging()
    lpc.log_debug(msg)


    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)


def main():

    tlc = TestLinchpinCliContext()
    tlc.setup_load_config()
    tlc.test_load_config()

if __name__ == '__main__':
    sys.exit(main())
