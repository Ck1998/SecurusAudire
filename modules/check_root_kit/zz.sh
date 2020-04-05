#!/bin/sh

#########################################################################
#
#    * DO NOT REMOVE *
#-----------------------------------------------------
# PLUGIN_AUTHOR=
# PLUGIN_CATEGORY=Debian
# PLUGIN_DESC=Debian tests
# PLUGIN_NAME=debian
# PLUGIN_VERSION=1.0.0
# PLUGIN_REQUIRED_TESTS=
#-----------------------------------------------------
#
#########################################################################
#


#########################################################################
#
# Add custom section to screen output
InsertSection "Debian Tests"
#
#################################################################################
# Constants

# Declare reduced BINPATHS for Debian Tests
DEBIAN_BINPATHS="bin sbin usr/bin usr/sbin usr/local/bin usr/local/sbin"

#################################################################################
# Start by scanning for any tools that will be required for later custom tests.
#
# This is basically a copy of the test from the file
# /usr/share/lynis/include/binaries with a shorter list of files to look for.
#
# Some of the files we search for here may be repeated checks from the default
# tests, but we look for them again due to local function dependencies.  It's a
# tiny redundancy that doesn't slow the tests up significantly.

# Test        : CUST-0001
# Description : Check for system binaries
# Notes       : Always perform this test, other tests depend on it.
Register --test-no CUST-0001 --weight L --network NO --description "Check for system binaries required by Debian Tests"
SCANNEDPATHS=""; N=0
Display --indent 2 --text "- Checking for system binaries that are required by Debian Tests..."
logtext "Status: Starting binary scan..."
for SCANDIR in ${DEBIAN_BINPATHS}; do
    logtext "Test: Checking binaries in directory ${SCANDIR}"
    if [ -d ${SCANDIR} ]; then
        Display --indent 4 --text "- Checking ${SCANDIR}... " --result FOUND --color GREEN
        SCANNEDPATHS="${SCANNEDPATHS}, ${SCANDIR}"
        logtext "Directory ${SCANDIR} exists. Starting directory scanning..."
        FIND=`ls ${SCANDIR}`
        for I in ${FIND}; do
            N=`expr ${N} + 1`
            BINARY="${SCANDIR}/${I}"
            logtext "Binary: ${BINARY}"
            # Optimized, much quicker (limited file access needed)
            case ${I} in
                apt-listbugs)           APTLISTBUGSBINARY=${BINARY};                              logtext "  Found known binary: apt-listbugs (System tool) - ${BINARY}"                 ;;
                apt-listchanges)        APTLISTCHANGESBINARY=${BINARY};                           logtext "  Found known binary: apt-listchanges (System tool) - ${BINARY}"              ;;
                checkrestart)           CHECKRESTARTBINARY="${BINARY}";                           logtext "  Found known binary: checkrestart (System tool) - ${BINARY}"                 ;;
		needrestart)            NEEDRESTARTBINARY="${BINARY}";                            logtext "  Found known binary: needrestart (System tool) - ${BINARY}"                  ;;
                cryptmount)             CRYPTMOUNTFOUND=1;      CRYPTMOUNTBINARY="${BINARY}";     logtext "  Found known binary: cryptmount (Encryption tool) - ${BINARY}"               ;;
                cryptsetup)             CRYPTSETUPFOUND=1;      CRYPTSETUPBINARY="${BINARY}";     logtext "  Found known binary: cryptsetup (Encryption tool) - ${BINARY}"               ;;
                debsecan)               DEBSECANBINARY="${BINARY}";                               logtext "  Found known binary: debsecan (System tool) - ${BINARY}"                     ;;
                debsums)                DEBSUMSBINARY="${BINARY}";                                logtext "  Found known binary: debsums (System tool) - ${BINARY}"                      ;;
                ecryptfsd)              ECRYPTFSDFOUND=1;       ECRYPTFSDBINARY="${BINARY}";      logtext "  Found known binary: ecryptfsd (Layered Encryption) - ${BINARY}"             ;;
                ecryptfs-migrate-home)  ECRYPTFSMIGRATEFOUND=1; ECRYPTFSMIGRATEBINARY=${BINARY};  logtext "  Found known binary: ecryptfs-migrate-home (Layered Encryption) - ${BINARY}" ;;
                fail2ban-server)        FAIL2BANBINARY=${BINARY};                                 logtext "  Found known binary: fail2ban-server (Security tool) - ${BINARY}"            ;;
                lvdisplay)              LVDISPLAYBINARY="${BINARY}";                              logtext "  Found known binary: lvdisplay (LVM tool) - ${BINARY}"                       ;;
                mount)                  MOUNTBINARY="${BINARY}";                                  logtext "  Fount known binary: mount (File system tool) - ${BINARY}"                   ;;
            esac
        done
      else
        Display --indent 4 --text "- Checking ${SCANDIR}... " --result "NOT FOUND" --color WHITE
        logtext "Directory ${SCANDIR} does NOT exist."
    fi
    logtextbreak
done
SCANNEDPATHS=`echo ${SCANNEDPATHS} | sed 's/^, //g'`
logtext "Discovered directories: ${SCANNEDPATHS}"

logtext "CUST-0001 Result: found ${N} binaries"
# report "binaries_count=${N}"

#################################################################################
# Authentication modules (Tests:  CUST-02xx)

Display --indent 2 --text "- Authentication:"
logtext "Status: Starting Authentication checks..."

Display --indent 4 --text "- PAM (Pluggable Authentication Modules):"

# Test        : CUST-0280
# Description : Checking if libpam-tmpdir is installed and enabled.
logtext "Status: Checking if libpam-tmpdir is installed and enabled..."
Register --test-no CUST-0280 --weight L --network NO --description "Checking if libpam-tmpdir is installed and enabled."
if [ ${SKIPTEST} -eq 0 ]; then
    FIND=`find /lib -name pam_tmpdir.so`
    if [ ! "${FIND}" = "" ]; then
        logtext " - libpam-tmpdir is installed."
        AddHP 1 1
        FIND2=`grep pam_tmpdir.so /etc/pam.d/common-session`
        if [ ! "${FIND2}" = "" ]; then
            Display --indent 6 --text "- libpam-tmpdir" --result "Installed and Enabled" --color GREEN
            logtext " - libpam-tmpdir is enabled in common-session."
            AddHP 1 1
        else
            Display --indent 6 --text "- libpam-tmpdir" --result "Installed but not Enabled" --color YELLOW
            logtext " - libpam-tmpdir is not enabled in common-session."
            AddHP 0 1
        fi
    else
        Display --indent 6 --text "- libpam-tmpdir" --result "Not Installed" --color RED
        logtext " - libpam-tmpdir is not installed."
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install libpam-tmpdir to set \$TMP and \$TMPDIR for PAM sessions"
    fi
fi

# Test        : CUST-0285
# Description : Checking if libpam-usb is installed and enabled.
logtext "Status: Checking if libpam-usb is installed and enabled..."
Register --test-no CUST-0285 --weight L --network NO --description "Checking if libpam-usb is installed and enabled."
if [ ${SKIPTEST} -eq 0 ]; then
    FIND=`find /lib -name pam_usb.so`
    if [ ! "${FIND}" = "" ]; then
        logtext " - libpam-usb is installed."
        AddHP 1 1
        FIND2=`grep "^auth\s\+\(required\|sufficient\)\s\+pam_usb.so" /etc/pam.d/common-auth`
        COUNT=`find /etc/pam.d/ -type f ! -name "common-*" ! -name "*.dpkg-old" | wc -l`
        if [ ! "${FIND2}" = "" ]; then
            GREP=`echo ${FIND2} | grep "required"`
            if [ ! "${GREP}" = "" ]; then
                Display --indent 6 --text "- libpam-usb" --result "Installed and 'required' in common-auth" --color GREEN
                logtext " - pam_usb.so is 'required' in common-auth."
                AddHP 1 1
                # Add Harden Points for ever other profile in /etc/pam.d that will
                # benefit from the inclusion in common-auth.  These points are
                # only awarded for "required" because it will require the usb
                # thumbdrive and a password to gain access.  For "sufficient",
                # the presence of the usb thumbdrive would act as a single
                # factor of authentication in place of the password.  No points
                # for single factor authentication of either type.
                AddHP ${COUNT} ${COUNT}
            else
                Display --indent 6 --text "- libpam-usb" --result "Installed and 'sufficient' in common-auth" --color YELLOW
                logtext " - pam_usb.so is 'sufficient' in common-auth."
                AddHP 0 1
                ReportSuggestion ${TEST_NO} "Change /etc/pam.d/common-auth to make pam_usb.so be 'required' instead of 'sufficient'."
            fi
                AddHP 0 ${COUNT}
        else
            # If pam_usb.so is not 'required' or 'sufficient' in
            # /etc/pam.d/common-auth then it may be enabled selectively in each
            # profile.  This can be handy for systems that desire to require two
            # factor authentication via usb for local sessions but use ssh-keys
            # for more intense authentication for remote sessions than just
            # using a password allows.

            # COUNT2 is the number of profiles with a "required" statement for
            # pam_usb.so
            COUNT2=`find /etc/pam.d/ -type f ! -name "common-*" ! -name "*.dpkg-old" -exec grep "^auth\s\+required\s\+pam_usb.so" "{}" + | wc -l`

            # COUNT3 is the number of profiles with a "sufficient" statement for
            # pam_usb.so
            COUNT3=`find /etc/pam.d/ -type f ! -name "common-*" ! -name "*.dpkg-old" -exec grep "^auth\s\+sufficient\s\+pam_usb.so" "{}" +  | wc -l`

            if [ ${COUNT2} -gt 0 ]; then
                Display --indent 6 --text "- libpam-usb" --result "Installed and 'required' by ${COUNT2} of ${COUNT} profiles" --color GREEN
                logtext " - pam_usb.so is 'required' for ${COUNT2}  of ${COUNT} profiles."
                AddHP ${COUNT2} ${COUNT}
            fi

            if [ ${COUNT2} = 0 -a ${COUNT3} = 0  ]; then
                Display --indent 6 --text "- libpam-usb" --result "Installed and but not 'required' or 'sufficient' for any profiles." --color RED
                AddHP 0 ${COUNT}
            else
                logtext " - pam_usb.so is 'sufficient' for ${COUNT3} of ${COUNT} profiles."
            fi
        fi
        # Next test Users for configured to use pamusb
        Display --indent 8 --text "- Users configured in /etc/pamusb.conf:"
        # Start with root, as there is one example with root included in the
        # default file, this string needs to be found more than once to get a
        # hardening point.
        ROOT_COUNT=`grep "<user\sid=\"root\">" /etc/pamusb.conf | wc -l`
        if [ ${ROOT_COUNT} -gt 1 ]; then
            Display --indent 10 --text "- root" --result "Yes" --color GREEN
            logtext " - pamusb.conf includes configuration for root."
            AddHP 1 1
        else
            Display --indent 10 --text "- root" --result "No" --color RED
            logtext " - pamusb.conf does not include configuration for root."
            AddHP 0 1
        fi
        USERLIST=`awk -F: '($3 > 500) && ($3 != 65534) { print $1 }' /etc/passwd`
        for U in ${USERLIST}; do
            USER_COUNT=`grep "<user\sid=\"${U}\">" /etc/pamusb.conf | wc -l`
            if [ ${USER_COUNT} -gt 0 ]; then
                Display --indent 10 --text "- ${U}" --result "Yes" --color GREEN
                logtext " - pamusb.conf includes configuration for ${U}."
                AddHP 1 1
            else
                Display --indent 10 --text "- ${U}" --result "No" --color RED
                logtext " - pamusb.conf does not include configuration for ${U}."
                AddHP 0 1
            fi
        done
    else
        Display --indent 6 --text "- libpam-usb" --result "Not Installed" --color RED
        logtext " - libpam-usb is not installed."
        # 10 missed hardening points is somewhat arbitrary but seems to be about
        # half of the points available for each profile that are commonly
        # installed in /etc/pam.d on my test systems.
        AddHP 0 10
        ReportSuggestion ${TEST_NO} "Install libpam-usb to enable multi-factor authentication for PAM sessions"
    fi
fi



#################################################################################
# File system (Tests: Deb-05xx)

Display --indent 2 --text "- File System Checks:"
logtext "Status: Starting file system checks..."

# Test        : CUST-0510
# Description : Checking if LVM Groups or file systems are stored on encrypted partitions (dm-crypt, cryptsetup & cryptmount)

Display --indent 4 --text "- DM-Crypt, Cryptsetup & Cryptmount:"
logtext "Status: Starting file system checks for dm-crypt, cryptsetup & cryptmount..."

if [ ! "${MOUNTBINARY}" = ""  -a ! "${LVDISPLAYBINARY}" = "" -a ! "${CRYPTSETUPBINARY}" = "" ]; then PREQS_MET="YES"; else PREQS_MET="NO"; fi
Register --test-no CUST-0510 --preqs-met ${PREQS_MET} --weight L --network NO --description "Checking if LVM volume groups or file systems are stored on encrypted partitions"
if [ ${SKIPTEST} -eq 0 ]; then
    logtext "Test: Checking file system mount points"
    FIND=`${MOUNTBINARY} 2> /dev/null | grep -v "^[binfmt_misc|devpts|fusectl|hugetlbfs|none|proc|sysfs|systemd|tmpfs|udev]" | grep -v ecryptfs | awk '{ print $1 ":" $3 }'`
    TESTED_LIST=""
    if [ ! "${FIND}" = "" ]; then
        logtext "Result: found one or more file system mount points"
        for I in ${FIND}; do
            # physical device
            PDEV=${I%:*}
            # Mount Point
            MOUNTPOINT=${I#*:}
            # Test if we've already checked this physical device.  If we are
            # using bind mounts to mitigate issues with read-only file
            # systems or to expand the size of one partition by bind
            # mounting a directory to space on another drive then the bind
            # mounts can cause a physical device to appear multiple times in
            # the output of 'mount'.  This test makes sure we only test
            # whether or not it is encrypted one time.
            #
            # As far as I know there is no way to have the bind mounts not
            # listed in /etc/mtab, /proc/mounts, or the output of mount
            # because the kernel does not distinguish between bind and
            # other mounts.  To the kernel, it's just another mounted
            # file system.
            #
            # Normal file systems are listed by 'mount' generally before
            # those bind mounted on my systems, so forgoing a '| sort' on
            # the FIND command appears to make sure that the mount points we
            # care about are listed first and the bind second (which can
            # and will be ignored in this test).
            echo ${TESTED_LIST} | grep ${PDEV} > /dev/null
            exitstatus=$?
            if [ ${exitstatus} -eq 0 ]; then
                # already tested this physical device, breaking out of the
                # loop to the next item on the list.
                logtext "- For ${MOUNTPOINT}: Already tested ${PDEV}, assuming bind mount and skipping."
                continue
            fi
            logtext "Testing file system mount point: ${PDEV}"
            case "${PDEV}" in
                /dev/mapper/*)
                    TEST_DEVICE=`${LVDISPLAYBINARY} -m ${PDEV} 2>/dev/null`
                    exitstatus=$?
                    if [ ${exitstatus} -ne 0 ]; then
                        # If lvdisplay has a failing exit status, assign
                        # PDEV as DEVICE.  Some partitions will be mounted
                        # through /dev/mapper mappings but not be part of
                        # LVM groups.
                        DEVICE=${PDEV}
                    else
                        # If lvdisplay does not have a failing exit status,
                        # then get the DEVICE from its output
                        DEVICE=`echo ${TEST_DEVICE} | sed -e 's/.*Physical volume \(.*\) Physical.*/\1/'`
                    fi
                    ;;
                * )
                    DEVICE=${PDEV}
                    ;;
            esac
            CRYPT=`${CRYPTSETUPBINARY} status ${DEVICE} 2>/dev/null`
            exitstatus=$?
            # It is possible that multiple partitions may be included within
            # the same group (for LVM) and that group container may or may
            # not be encrypted.  If that is so, you will gain or
            # lose hardening points for each partition in the group.  Just
            # as you would if they were individual partitions on the hard
            # drive.
            #
            # Tests only apply to those partitions that are mounted when
            # Lynis is run.  You will not gain or lose points for any
            # partitions that are not mounted.
            if [ ${exitstatus} -eq 0 ]; then
                TYPE=`echo ${CRYPT} | grep "type:" | sed -e 's/.*type: \(.*\) cipher.*/\1/'`
                if [ "a${TYPE}a" = "an/aa" ]; then
                    # Partitions mounted via cryptmount will pass cryptsetup
                    # with a valid exit status and will show as "active" but
                    # will not show a type.
                    if [ ! "${CRYPTMOUNTBINARY}" = "" ]; then
                        # if cryptsetup exits with a valid exit status and
                        # cryptmount is installed, then that may explain why
                        # we are unable to determine the type from
                        # cryptsetup's output.
                        CIPHER=`echo ${CRYPT} | grep "cipher:" | sed -e 's/.*cipher: \(.*\) keysize.*/\1/'`
                        Display --indent 6 --text "- Checking ${MOUNTPOINT} on ${DEVICE}" --result "Cryptmount? [Cipher: ${CIPHER}]" --color GREEN
                        # We add a hardening point because we have verified that
                        # the drive is encrypted even if we cannot determine the
                        # 'type' with these tools.
                        AddHP 1 1
                    else
                        # if cryptsetup exits with a valid exit status but
                        # cryptmount is not installed then Display informs
                        # the user that the test is uncertain of the
                        # encryption status of the partition or drive.  It
                        # will be up to the user to determine its status.
                        Display --indent 6 --text "- Checking ${MOUNTPOINT} on ${DEVICE}" --result "Unknown Encryption Status" --color YELLOW
                        #
                        # We do not add a hardening point because it is possible
                        # that the partition is encrypted but its status cannot
                        # be verified by these tools.
                        AddHP 0 1
                    fi
                else
                    # cryptsetup exited with a valid exit status (0) and we
                    # were able to determine the type of encryption used
                    # from its output.
                    AddHP 1 1
                    Display --indent 6 --text "- Checking ${MOUNTPOINT} on ${DEVICE}" --result "ENCRYPTED (Type: ${TYPE})" --color GREEN
                fi
            else
                # if cryptsetup exits with a non-zero exit status, then the
                # drive or partition has not been encrypted in a manner that
                # cryptsetup can  detect.  For the purposes of this test, it
                # is considered to be not encrypted.
                if [ ! "${MOUNTPOINT}" = "/boot" ]; then
                    AddHP 0 1
                    Display --indent 6 --text "- Checking ${MOUNTPOINT} on ${DEVICE}" --result "NOT ENCRYPTED" --color WHITE
                else
                    # /boot is generally not be encrypted.  We should test to see
                    # that it is on its own partition.  Also might test if
                    # it is mounted read-only?
                    logtext " - ${DEVICE} is mounted on ${MOUNTPOINT}, cannot be encrypted with DM-Crypt."
                    Display --indent 6 --text "- Checking /boot on ${DEVICE}" --result "NOT ENCRYPTED" --color WHITE
                fi
            fi
            # add physical device to the tested list.
            TESTED_LIST="${TESTED_LIST},${PDEV}"
        done
      else
        Display --indent 6 --text "- No file system mount points found" --result ERROR --color RED
    fi
fi

# Test        : CUST-0520
# Description : Check if user home directories are encrypted with ecryptfs
# Notes       : Ecryptfs is useful on multi-user systems.  Can be configured
#               so that files in the users home directories are only
#               decrypted while the user is logged in.
#
#               This function adds hardening points according to the
#               following criteria:
#                  +1 Ecryptfs Installed
#                  +1 for each user account that can be configured to use it.
if [ ! "${ECRYPTFSDBINARY}" = "" ]; then PREQS_MET="YES"; else PREQS_MET="NO"; fi
Register --test-no "CUST-0520" --os Linux --preqs-met ${PREQS_MET} --weight L --network NO --description "Checking for Ecryptfs"
if [ ${SKIPTEST} -eq 0 -a ! "${ECRYPTFSDBINARY}" = "" ]; then
    Display --indent 4 --text "- Ecryptfs" --result INSTALLED --color GREEN
    logtext "Ecryptfs installed."
    AddHP 1 1
    logtext "Test: If user home directories are configured to use Ecryptfs"
    USERLIST=`awk -F: '($3 > 500) && ($3 != 65534) { print $1","$6 }' /etc/passwd`
    for U in ${USERLIST}; do
    ECRYPTFSHOME=1
    USER=`echo ${U} | sed -e 's/,.*//'`
    HOMEDIR=`echo ${U} | sed -e 's/^[^,]*,//'`
    logtext "USER: ${USER}"
    logtext "HOME DIR: ${HOMEDIR}"
    if [ -d /home/.ecryptfs/${USER} -a -f /home/.ecryptfs/${USER}/.ecryptfs/auto-mount -a -f /home/.ecryptfs/${USER}/.ecryptfs/Private.mnt ]; then
        PRIVDIR=`cat /home/.ecryptfs/${USER}/.ecryptfs/Private.mnt`
        logtext "PRIVATE DIR: ${PRIVDIR}"
        if [ "${HOMEDIR}" = ${PRIVDIR} ]; then
        # Ecryptfs installed and configured to encrypt users
        # entire ${HOME} directory.
        logtext "Result: Home directory for ${USER} configured to use Ecryptfs"
        Display --indent 6 --text "- Home for ${USER}" --result YES --color GREEN
        AddHP 1 1
        ECRYPTFSHOME=0
        fi
    fi
    if [ ${ECRYPTFSHOME} -eq 1 ]; then
        # Ecryptfs Private directory configured but not for
        # users ${HOME} directory -OR- Ecryptfs has not been setup
        # for user.
        logtext "Result: Ecryptfs installed but not configured for ${USER}'s home directory"
        Display --indent 6 --text "- Home for ${USER}" --result NO --color RED
        AddHP 0 1
        # Unsure if ecryptfs-migrate-home is part of all Ecryptfs installations
        # on all Linux distributions.
        if [ ! "${ECRYPTFSMIGRATEBINARY}" = "" ]; then
        ReportSuggestion ${TEST_NO} "As root run 'ecryptfs-migrate-home --user ${USER}' to configure Ecryptfs for user's home directory"
        else
        ReportSuggestion ${TEST_NO} "Configure Ecryptfs for ${USER}'s home directory"
        fi
    fi
    done
fi

#################################################################################
# Software

Display --indent 2 --text "- Software:"
logtext "Status: Starting Software checks..."

# Test        : CUST-0810
# Description : Checking if apt-listbugs is installed and enabled.
Register --test-no "CUST-0810" --weight L --network NO --description "Checking for apt-listbugs"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${APTLISTBUGSBINARY}" = "" ]; then
        logtext " - apt-listbugs is installed."
        AddHP 1 1
        FIND=`find /etc/apt/apt.conf.d -name *listbugs`
        if [ ! ${FIND} = "" ]; then
            logtext " - Apt configured to use apt-listbugs"
            Display --indent 4 --text "- apt-listbugs" --result "Installed and enabled for apt" --color GREEN
            AddHP 1 1
        else
            logtext " - Apt is not configured to use apt-listbugs"
            Display --indent 4 --text "- apt-listbugs" --result "Installed but not enabled for apt" --color YELLOW
            AddHP 0 1
            ReportSuggestion ${TEST_NO} "Reinstall apt-listbugs to enabled default task in /etc/apt/apt.comf.d"
        fi
    else
        logtext " - apt-listbugs is not installed."
        Display --indent 4 --text "- apt-listbugs" --result "Not Installed" --color RED
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install apt-listbugs to display a list of critical bugs prior to each APT installation."
    fi
fi

# Test        : CUST-0811
# Description : Checking if apt-listchanges is installed and enabled.
Register --test-no "CUST-0811" --weight L --network NO --description "Checking for apt-listchanges"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${APTLISTCHANGESBINARY}" = "" ]; then
        logtext " - apt-listchanges is installed."
        AddHP 1 1
        FIND=`find /etc/apt/apt.conf.d -name *listchanges`
        if [ ! ${FIND} = "" ]; then
            logtext " - Apt configured to use apt-listchanges"
            Display --indent 4 --text "- apt-listchanges" --result "Installed and enabled for apt" --color GREEN
            AddHP 1 1
        else
            logtext " - Apt is not configured to use apt-listchanges"
            Display --indent 4 --text "- apt-listchanges" --result "Installed but not enabled for apt" --color YELLOW
            AddHP 0 1
            ReportSuggestion ${TEST_NO} "Reinstall apt-listchanges to enabled default task in /etc/apt/apt.comf.d"
        fi
    else
        logtext " - apt-listchanges is not installed."
        Display --indent 4 --text "- apt-listchanges" --result "Not Installed" --color RED
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install apt-listchanges to display any significant changes prior to any upgrade via APT."
    fi
fi

# Test        : CUST-0830
# Description : Checking if checkrestart is installed.
Register --test-no CUST-0830 --weight L --network NO --description "Verifying that checkrestart is installed."
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${CHECKRESTARTBINARY}" = "" ]; then
        logtext " - checkrestart is installed."
        Display --indent 4 --text "- checkrestart" --result "Installed" --color GREEN
        AddHP 1 1
    else
        logtext " - checkrestart is not installed."
        Display --indent 4 --text "- checkrestart" --result "Not Installed" --color RED
        ReportSuggestion ${TEST_NO} "Install debian-goodies so that you can run checkrestart after upgrades to determine which services are using old versions of libraries and need restarting."
        AddHP 0 1
    fi
fi

# Test        : CUST-0831
# Description : Checking if needrestart is installed.
Register --test-no CUST-0831 --weight L --network NO --description "Verifying that needrestart is installed."
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${NEEDRESTARTBINARY}" = "" ]; then
        logtext " - needrestart is installed."
        Display --indent 4 --text "- needrestart" --result "Installed" --color GREEN
        AddHP 1 1
    else
        logtext " - needrestart is not installed."
        Display --indent 4 --text "- needrestart" --result "Not Installed" --color RED
        ReportSuggestion ${TEST_NO} "Install needrestart, alternatively to debian-goodies, so that you can run needrestart after upgrades to determine which daemons are using old versions of libraries and need restarting."
        AddHP 0 1
    fi
fi




# Test        : CUST-0870
# Description : Checking if debsecan is installed and enabled.
Register --test-no "CUST-0870" --weight L --network NO --description "Checking for debsecan"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${DEBSECANBINARY}" = "" ]; then
        logtext " - debsecan is installed."
        AddHP 1 1
        FIND=`find /etc/cron* -name debsecan`
        if [ ! ${FIND} = "" ]; then
            logtext " - cron job is configured for debsecan"
            Display --indent 4 --text "- debsecan" --result "Installed and enabled for cron" --color GREEN
            AddHP 1 1
        else
            logtext " - cron job is not configured for debsecan"
            Display --indent 4 --text "- debsecan" --result "Installed but not enabled for cron" --color YELLOW
            AddHP 0 1
            ReportSuggestion ${TEST_NO} "Reinstall debsecan to enabled default task in /etc/cron.d/debsecan"
        fi
    else
        logtext " - debsecan is not installed."
        Display --indent 4 --text "- debsecan" --result "Not Installed" --color RED
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install debsecan to generate lists of vulnerabilities which affect this installation."
    fi
fi  

# Test        : CUST-0875
# Description : Checking if debsums is installed and enabled.
Register --test-no "CUST-0875" --weight L --network NO --description "Checking for debsums"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${DEBSUMSBINARY}" = "" ]; then
        logtext " - debsums is installed."
        AddHP 1 1
        COUNT=`find /etc/cron* -name debsums | wc -l`
        # Default installation of debsums includes scripts in /etc/cron.daily,
        # /etc/cron.weekly and /etc/cron.monthly.   As there are three, simply
        # checking if the find statement is not blank produced an error.
        # However, by testing if more than zero were found, we can be sure that
        # it is enabled for cron.
        if [ ${COUNT} -gt 0 ]; then
            logtext " - cron jobs are configured for debsums."
            Display --indent 4 --text "- debsums" --result "Installed and enabled for cron" --color GREEN
            AddHP 1 1
        else
            logtext " - cron jobs are not configured for debsums."
            Display --indent 4 --text "- debsums" --result "Installed but not enabled for cron" --color YELLOW
            AddHP 0 1
            ReportSuggestion ${TEST_NO} "Reinstall debsums to enabled default tasks for cron."
        fi
    else
        logtext " - debsums is not installed."
        Display --indent 4 --text "- debsums" --result "Not Installed" --color RED
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install debsums for the verification of installed package files against MD5 checksums."
    fi
fi

# Test        : DEB-0880
# Description : Checking if fail2ban-server is installed.
Register --test-no "DEB-0880" --weight L --network NO --description "Checking for fail2ban"
if [ ${SKIPTEST} -eq 0 ]; then
    if [ ! "${FAIL2BANBINARY}" = "" ]; then
        logtext " - fail2ban is installed."
        AddHP 1 1
        LOCAL=`find /etc/fail2ban/ -name jail.local | wc -l`
        # Default installation of fail2ban includes a default configuration in
        # /etc/fail2ban/jail.conf.  However this configuration can be
        # overwritten by any updates to the fail2ban package.  To prevent this,
        # the configuration file should be copied to /etc/fail2ban/jail.local.
        if [ ${LOCAL} -gt 0 ]; then
            logtext " - fail2ban local custom configuration enabled."
            Display --indent 4 --text "- fail2ban" --result "Installed with jail.local" --color GREEN
            AddHP 1 1
        else
            logtext " - fail2ban configuration has not been localized."
            Display --indent 4 --text "- fail2ban" --result "Installed with jail.conf" --color YELLOW
            AddHP 0 1
            ReportSuggestion ${TEST_NO} "Copy /etc/fail2ban/jail.conf to jail.local to prevent it being changed by updates."
        fi
    else
        logtext " - fail2ban is not installed."
        Display --indent 4 --text "- fail2ban" --result "Not Installed" --color RED
        AddHP 0 2
        ReportSuggestion ${TEST_NO} "Install fail2ban to automatically ban hosts that commit multiple authentication errors."
    fi
fi



logtextbreak

# Wait for keypress (unless --quick is being used)
wait_for_keypress

#EOF
