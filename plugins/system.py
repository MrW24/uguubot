import os
import re
import time
import platform
from util import hook
from datetime import timedelta


def convert_kilobytes(kilobytes):
    if kilobytes >= 1024:
        megabytes = kilobytes / 1024
        size = '%.2f MB' % megabytes
    else:
        size = '%.2f KB' % kilobytes
    return size


@hook.command(autohelp=False, adminonly=True)
def system(inp):
    """system -- Retrieves information about the host system."""
    hostname = platform.node()
    os = platform.platform()
    python_imp = platform.python_implementation()
    python_ver = platform.python_version()
    architecture = '-'.join(platform.architecture())
    cpu = platform.machine()
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime = str(timedelta(seconds = uptime_seconds))

    return "Hostname: \x02{}\x02, Operating System: \x02{}\x02, Python " \
           "Version: \x02{} {}\x02, Architecture: \x02{}\x02, CPU: \x02{}" \
           "\x02, Uptime: \x02{}\x02".format(hostname, os, python_imp, python_ver, architecture, cpu, uptime)


@hook.command(autohelp=False, adminonly=True)
def memory(inp):
    """memory -- Displays the bot's current memory usage."""
    if os.name == "posix":
        # get process info
        status_file = open('/proc/self/status').read()
        s = dict(re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M))
        # get the data we need and process it
        data = s['VmRSS'], s['VmSize'], s['VmPeak'], s['VmStk'], s['VmData']
        data = [float(i.replace(' kB', '')) for i in data]
        strings = [convert_kilobytes(i) for i in data]
        # prepare the output
        out = "Threads: \x02{}\x02, Real Memory: \x02{}\x02, Allocated Memory: \x02{}\x02, Peak " \
              "Allocated Memory: \x02{}\x02, Stack Size: \x02{}\x02, Heap " \
              "Size: \x02{}\x02".format(s['Threads'], strings[0], strings[1], strings[2],
              strings[3], strings[4])
        # return output
        return out

    elif os.name == "nt":
        cmd = 'tasklist /FI "PID eq %s" /FO CSV /NH' % os.getpid()
        out = os.popen(cmd).read()
        memory = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            memory += float(amount.replace(',', ''))
        memory = convert_kilobytes(memory)
        return "Memory Usage: \x02{}\x02".format(memory)

    else:
        return "Sorry, this command is not supported on your OS."


@hook.command(autohelp=False)
def uptime(inp, bot=None):
    """uptime -- Shows the bot's uptime."""
    uptime_raw = round(time.time() - bot.start_time)
    uptime = timedelta(seconds=uptime_raw)
    with open('/proc/uptime', 'r') as f:
        sysuptime_seconds = float(f.readline().split()[0])
        sysuptime = str(timedelta(seconds = sysuptime_seconds))

    return "Uptime: \x02{}\x02, System Uptime: \x02{}\x02".format(uptime, sysuptime)


@hook.command(autohelp=False, adminonly=True)
def pid(inp):
    """pid -- Prints the bot's PID."""
    return "PID: \x02{}\x02".format(os.getpid())


@hook.command(autohelp=False)
def bots(inp):
    return "Reporting in! 2[Python] UguuBot run by W24 See 12%help for more information"
    
@hook.command(autohelp=False)
def help(inp):
    return "UguuBot run by W24 10• For a mostly accurate list of commands, see http://uguubot.com 10• For support and channel requests, join #W24Bot"

@hook.command(autohelp=False)
def source(inp):
    return "\x02wbot's Source\x02 - https://github.com/MrW24/wbot"
    
