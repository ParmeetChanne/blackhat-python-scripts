import win32con
import win32api
import win32security

import wmi
import sys
import os


def get_process_privileges(pid):
    try:
        # obtain a handle to the target process
        hproc = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION, False, pid)

        # open the main access token
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)

        # retreive the list of privileges enabled
        privs = win32security.GetTokenInformation(
            htok, win32security.TokenPrivileges)

        # iterate over privileges and outut the ones that are enabled
        prov_list = ""
        for i in privs:
            # check if the prvilieges is enabled
            if i[1] == 3:
                priv_list += "%s|" % win32security.LookupPrivilegeName(
                    None, i[0])

    except:
        priv_list = "N/A"

    return priv_list


def log_to_file(message):
    fd = open("process_monitor_log.csv", "ab")
    fd.write("%s\r\n" % message)
    fd.close()
    return


# create a log file header
log_to_file("Time, User, Executable, CommandLine, Parent PID, PID, Privileges")

# instantiate the WMI interface
c = wmi.WMI()

# create our process monitor
process_watcher = c.Win32_Process.watch_for("creation")

while True:
    try:
        new_process = process_watcher()

        proc_owner = new_process.GetOwner()
        proc_owner = "%s\\%s" % (proc_owner[0], proc_owner[2])
        create_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessId
        parent_pid = new_process.ParentProcessId
        privileges = get_process_privileges(pid)

        process_log_message = "%s,%s,%s,%s,%s,%s,%s\r\n" % (
            create_date, proc_owner, executable, cmdline, pid, parent_pid, privileges)

        print(process_log_message)

        log_to_file(process_log_message)

    except:
        pass
