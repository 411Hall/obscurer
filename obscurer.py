#!/usr/bin/python

import random
import crypt
import string
import re
from random import randint
import time
from optparse import OptionParser
import sys
import pexpect

def rand_hex():
    return '{0}{1}'.format(random.choice('0123456789ABCDEF'), random.choice('0123456789ABCDEF'))


def random_int(len):
    return random.randint()


usernames = ['admin', 'support', 'guest', 'user', 'service', 'tech', 'administrator']
passwords = ['system', 'enable', 'password', 'shell', 'root', 'support']
services = ['syslog', 'mongodb', 'statd', 'pulse']
os = ['Ubuntu 14.04.5 LTS', 'Ubuntu 16.04 LTS', 'Debian GNU/Linux 6']
hostnames = ['web', 'db', 'nas']
hostname = random.choice(hostnames)
nix_versions = {
    'Linux version 2.6.32-042stab116.2 (root@kbuild-rh6-x64.eng.sw.ru) (gcc version 4.4.6 20120305 (Red Hat 4.4.6-4) (GCC) ) #1 SMP Fri Jun 24 15:33:57 MSK 2016':
        'Linux {0} 2.6.32-042stab116.2 #1 SMP Fri Jun 24 15:33:57 MSK 2016 x86_64 x86_64 x86_64 GNU/Linux'.format(
            hostname),
    'Linux version 4.4.0-62-generic (buildd@lcy01-33) (gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3) ) #83~14.04.1-Ubuntu SMP Wed Jan 18 18:10:30 UTC 2017':
        'Linux {0} 4.4.0-62-generic #83~14.04.1-Ubuntu SMP Wed Jan 18 18:10:30 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux'.format(
            hostname),
    'Linux version 4.4.0-36-generic (buildd@lgw01-20) (gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3) ) #55~14.04.1-Ubuntu SMP Fri Aug 12 11:49:30 UTC 2016':
        'Linux {0} 4.4.0-36-generic #55~14.04.1-Ubuntu SMP Fri Aug 12 11:49:30 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux'.format(
            hostname),
    'Linux version 4.4.0-59-generic (buildd@lcy01-32) (gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3) ) #80~14.04.1-Ubuntu SMP Fri Jan 6 18:02:02 UTC 2017':
        'Linux {0} 4.4.0-59-generic #80~14.04.1-Ubuntu SMP Fri Jan 6 18:02:02 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux'.format(
            hostname),
    'Linux version 4.6.0-nix-amd64 (devel@kgw92.org) (gcc version 5.4.0 20160609 (Debian 5.4.0-6) ) #1 SMP Debian 4.6.4-1nix1 (2016-07-21)':
        'Linux {0} 4.6.0-nix1-amd64 #1 SMP Debian 4.6.4-1nix1 (2016-07-21) x86_64 GNU/Linux'.format(hostname),
    'Linux version 3.13.0-108-generic (buildd@lgw01-60) (gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3) ) #155-Ubuntu SMP Wed Jan 11 16:58:52 UTC 2017':
        'Linux {0} 3.13.0-108-generic #155-Ubuntu SMP Wed Jan 11 16:58:52 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux'.format(
            hostname)}
processors = ['Intel(R) Core(TM) i7-2960XM CPU @ 2.70GHz', 'Intel(R) Core(TM) i5-4590S CPU @ 3.00GHz',
              'Intel(R) Core(TM) i3-4005U CPU @ 1.70GHz']
cpu_flags = ['rdtscp', 'arch_perfmon', 'nopl', 'xtopology', 'nonstop_tsc', 'aperfmperf', 'eagerfpu', 'pclmulqdq',
             'dtes64', 'pdcm', 'pcid',
             'sse4_2', 'x2apic', 'popcnt', 'tsc_deadline_timer', 'xsave', 'avx', 'epb', 'tpr_shadow', 'vnmi',
             'flexpriority', 'vpid', 'xsaveopt', 'dtherm', 'ida', 'arat', 'pln', 'pts']
physical_hd = ['sda', 'sdb', ]
mount_names = ['share', 'db', 'media', 'mount', 'storage']
mount_options = ['noexec', 'nodev', 'nosuid', 'relatime']
mount_additional = [
    'vmware-vmblock /run/vmblock-fuse fuse.vmware-vmblock rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other 0 0',
    'gvfsd-fuse /run/user/1001/gvfs fuse.gvfsd-fuse rw,nosuid,nodev,relatime,user_id=1001,group_id=1001 0 0',
    'rpc_pipefs /run/rpc_pipefs rpc_pipefs rw,relatime 0 0']
mac_addresses = ['00:0F:3D:{0}:{1}:{2}'.format(rand_hex(), rand_hex(), rand_hex()),
                 'C4:A8:1D:{0}:{1}:{2}'.format(rand_hex(), rand_hex(), rand_hex()),
                 'F8:E9:03:{0}:{1}:{2}'.format(rand_hex(), rand_hex(), rand_hex()),
                 'BC:F6:85:{0}:{1}:{2}'.format(rand_hex(), rand_hex(), rand_hex())]
ps_aux_sys = ['[acpi_thermal_pm]', '[ata_sff]', '[devfreq_wq]', '[ecryptfs-kthrea]', '[ext4-rsv-conver]',
              '[firewire_ohci]', '[fsnotify_mark]', '[hci0]', '[kdevtmpfs]', '[khugepaged]', '[khungtaskd]',
              '[kintegrityd]',
              '[ksoftirqd/0]', '[ksoftirqd/1]', '[ksoftirqd/2]', '[ksoftirqd/3]', '[ksoftirqd/4]', '[kvm-irqfd-clean]',
              '[kworker/0:0]', '[kworker/0:0H]', '[kworker/0:1H]', '[kworker/0:3]', '[kworker/1:0]',
              '[kworker/1:0H]', '[kworker/1:1H]', '[kworker/1:2]', '[kworker/2:0]', '[kworker/2:0H]', '[kworker/2:1]',
              '[migration/0]', '[migration/1]', '[migration/2]', '[migration/3]', '[migration/4]', '[migration/5]',
              '[netns]', '[nfsiod]', '[perf]', '[rcu_bh]', '[rcu_sched]', '[rpciod]', '[scsi_eh_0]', '[scsi_eh_1]',
              '[watchdog/0]', '[watchdog/1]', '[watchdog/2]', '[watchdog/3]', '[watchdog/4]', '[xfsalloc]',
              '[xfs_mru_cache]']
ps_aux_usr = ['/sbin/dhclient', '/sbin/getty', '/usr/lib/gvfs/gvfs-afc-volume-monitor', '/usr/lib/gvfs/gvfsd',
              '/usr/lib/gvfs/gvfsd-burn', '/usr/lib/gvfs/gvfsd-fuse', '/usr/lib/gvfs/gvfsd-http',
              '/usr/lib/gvfs/gvfsd-metadata', '/usr/lib/ibus/ibus-dconf', '/usr/lib/ibus/ibus-engine-simple',
              '/usr/lib/ibus/ibus-ui-gtk3', '/usr/lib/ibus/ibus-x11', '/usr/lib/rtkit/rtkit-daemon',
              '/usr/lib/telepathy/mission-control-5',
              '/usr/lib/xorg/Xorg', '/usr/sbin/cups-browsed', '/usr/sbin/cupsd', '/usr/sbin/dnsmasq',
              '/usr/sbin/irqbalance', '/usr/sbin/kerneloops', '/usr/sbin/ModemManager', '/usr/sbin/pcscd',
              '/usr/sbin/pptpd']
ssh_ver = ['SSH-2.0-OpenSSH_5.1p1 Debian-5', 'SSH-1.99-OpenSSH_4.3', 'SSH-1.99-OpenSSH_4.7',
           'SSH-2.0-OpenSSH_5.1p1 Debian-5', 'SSH-2.0-OpenSSH_5.1p1 FreeBSD-20080901',
           'SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu5',
           'SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu6', 'SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7',
           'SSH-2.0-OpenSSH_5.5p1 Debian-6+squeeze2', 'SSH-2.0-OpenSSH_5.9p1 Debian-5ubuntu1',
           ' SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u1']
user_count = random.randint(1, 3)
users = []
password = []
service = []
i = 0
while i < user_count:
    rand_user = random.choice(usernames)
    users.append(rand_user)
    usernames.remove(rand_user)
    service.append(random.choice(services))
    password.append(random.choice(passwords))
    i = i + 1

## Generate Host Profile ##
ram_size = 512 * random.choice(range(2, 16, 2))
hd_size = 61440 * random.choice(range(2, 16, 2))
processor = random.choice(processors)
ip_ranges = ['10.{0}.{1}.{2}'.format(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)),
             '172.{0}.{1}.{2}'.format(random.randint(16, 31), random.randint(1, 255), random.randint(1, 255)),
             '192.168.{0}.{1}'.format(random.randint(1, 255), random.randint(1, 255))]
ip_address = random.choice(ip_ranges)
ipv6_number = list(map(int, ip_address.split('.')))


def base_py(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/cowrie/commands/base.py"), "r+") as base_file:
        user = random.choice(users)
        base = base_file.read()
        base_file.seek(0)
        to_replace = re.findall('(?<=output = \(\n)(.*)(?=for i in range)', base, re.DOTALL)
        new_base = "\t\t\t('USER      ', ' PID', ' %CPU', ' %MEM', '    VSZ', '   RSS', ' TTY      ', 'STAT ', 'START', '   TIME ', 'COMMAND',),\n"
        new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
            'root', '1', '0.0', '0.0', randint(10000, 25000), randint(500, 2500), '?', 'Ss', time.strftime('%b%d'),
            '0:00', '/sbin/init')
        new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
            'root', '2', '0.0', '0.0', '0', '0', '?', 'S', time.strftime('%b%d'), '0:00', '[kthreadd]')
        r = randint(15, 30)
        sys_pid = 3
        while r > 0:
            sys_pid = sys_pid + randint(1, 3)
            new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
                'root', sys_pid, '0.0', '0.0', '0', '0', '?', random.choice(['S', 'S<']), time.strftime('%b%d'), '0:00',
                random.choice(ps_aux_sys))
            r -= 1
        t = randint(4, 10)
        usr_pid = 1000
        while t > 0:
            usr_pid = usr_pid + randint(20, 70)
            minute = time.strftime('%m')
            hour = time.strftime('%')
            new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
                random.choice(['root', user]), usr_pid, '{0}.{1}'.format(randint(0, 4), randint(0, 9)),
                '{0}.{1}'.format(randint(0, 4), randint(0, 9)), randint(10000, 25000), randint(500, 2500),
                '?', random.choice(['S', 'S<', 'S+', 'Sl']), time.strftime('%H:%m'), '0:00', random.choice(ps_aux_usr))
            t -= 1
        new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
            'root', usr_pid + randint(20, 100), '0.{0}'.format(randint(0, 9)), '0.{0}'.format(randint(0, 9)),
            randint(1000, 6000), randint(500, 2500), '?', random.choice(['S', 'S<', 'S+', 'Sl']),
            time.strftime('%H:%m'), '0:{0}{1}'.format(0, randint(0, 3)), '/usr/sbin/sshd: %s@pts/0\' % user')
        new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
            '\'%s\'.ljust(8) % user', usr_pid + randint(20, 100), '0.{0}'.format(randint(0, 9)),
            '0.{0}'.format(randint(0, 9)), randint(1000, 6000), randint(500, 2500), 'pts/{0}'.format(randint(0, 5)),
            random.choice(['S', 'S<', 'S+', 'Sl']), time.strftime('%H:%m'),
            '0:{0}{1}'.format(0, randint(0, 3)), '-bash')
        new_base += "\t\t\t('{0:<10}', '{1:>4}', '{2:>5}', '{3:>5}', '{4:>7}', '{5:>6}', '{6:<10}', '{7:<5}', '{8:>5}', '{9:>8}', '{10}',),\n".format(
            '\'%s\'.ljust(8) % user', usr_pid + randint(20, 100), '0.{0}'.format(randint(0, 9)),
            '0.{0}'.format(randint(0, 9)), randint(1000, 6000), randint(500, 2500), 'pts/{0}'.format(randint(0, 5)),
            random.choice(['S', 'S<', 'S+', 'Sl']),
            time.strftime('%H:%m'), '0:{0}{1}'.format(0, randint(0, 3)), '\'ps %s\' % \' \'.join(self.args)')
        new_base += "\t\t\t)\n\t\t"
        base_replacements = {to_replace[0]: new_base}
        substrs = sorted(base_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        base_update = regexp.sub(lambda match: base_replacements[match.group(0)], base)
        base_file.write(base_update)
        base_file.truncate()
        base_file.close()
        print "base.py file changed!\n"


def free_py(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/cowrie/commands/free.py"), "r+") as free_file:
        free = free_file.read()
        free_file.seek(0)
        total = int(ram_size - ((3 * ram_size) / 100.0))
        used_ram = int((randint(50, 75) * ram_size) / 100.0)
        free_ram = total - used_ram
        shared_ram = ram_size / 48
        buffers = ram_size / 36
        cached = used_ram - shared_ram - buffers
        buffers_cachev1 = used_ram - (buffers + cached)
        buffers_cachev2 = used_ram + (buffers + cached)
        free_replacements = {
            "Mem:          7880       7690        189          0        400       5171": "Mem:          {0}       {1}        {2}          {3}        {4}       {5}".format(
                total, used_ram, free_ram, shared_ram, buffers, cached),
            "-/+ buffers/cache:       2118       5761": "-/+ buffers/cache:       {0}       {1}".format(buffers_cachev1,
                                                                                                        buffers_cachev2),
            "Swap:         3675        129       3546": "Swap:         0        0       0",
            "Mem:       8069256    7872920     196336          0     410340    5295748": "Mem:       {0}    {1}     {2}          {3}     {4}    {5}".format(
                total * 1000, used_ram * 1000, free_ram * 1000, shared_ram * 1000, buffers * 1000, cached * 1000),
            "-/+ buffers/cache:    2166832    5902424": "-/+ buffers/cache:    {0}    {1}".format(
                buffers_cachev1 * 1000, buffers_cachev2 * 1000),
            "Swap:      3764220     133080    3631140": "Swap:      0     0    0".format(),
            "Mem:          7.7G       7.5G       189M         0B       400M       5.1G": "Mem:          {0}G       {1}G       {2}M         {3}B       {4}M       {5}G".format(
                total / 1000, round(used_ram / 1000.0, 1), free_ram / 1000, shared_ram, buffers, cached / 1000),
            "-/+ buffers/cache:       2.1G       5.6G": "-/+ buffers/cache:       {0}M       {1}G".format(
                round(buffers_cachev1 / 1000.0, 1), round(buffers_cachev2 / 1000.0, 1)),
            "Swap:         3.6G       129M       3.5G": "Swap:         0B       0B       0B"}
        substrs = sorted(free_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        free_update = regexp.sub(lambda match: free_replacements[match.group(0)], free)
        free_file.write(free_update)
        free_file.truncate()
        free_file.close()
        print "free.py file changed!\n"


def ifconfig_py(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/cowrie/commands/ifconfig.py"), "r+") as ifconfig_file:
        ifconfig = ifconfig_file.read()
        ifconfig_file.seek(0)
        eth_rx = randint(10000000000, 500000000000)
        eth_tx = randint(10000000000, 500000000000)
        lo_rxtx = randint(10000, 99999)
        ifconfig_replacements = {'04:01:16:df:2d:01': '{0}'.format(random.choice(mac_addresses)),
                                 '139435762': str(randint(1000, 100000000)), '116082382': str(randint(1000, 100000000)),
                                 '102191499830': str(eth_rx), '102.1': '{0}'.format(str(eth_rx / 1000000000)),
                                 '68687923025': str(eth_tx), '68.6': '{0}'.format(str(eth_tx / 1000000000)),
                                 '19932': str(lo_rxtx), '19.9': '{0}'.format(str(lo_rxtx / 1000)),
                                 '110': '{0}'.format(randint(50, 250)),
                                 'fe80::601:16ff:fedf:2d01/64': '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*ipv6_number)}
        substrs = sorted(ifconfig_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        ifconfig_update = regexp.sub(lambda match: ifconfig_replacements[match.group(0)], ifconfig)
        ifconfig_file.write(ifconfig_update)
        ifconfig_file.truncate()
        ifconfig_file.close()
        print "ifconfig file changed!\n"


def arp_py(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/proc/net/arp"), "r+") as arp_file:
        arp = arp_file.read()
        arp_file.seek(0)
        base_ip = '.'.join(ip_address.split('.')[0:3])
        arp_replacements = {'192.168.1.27': '{0}.{1}'.format(base_ip, random.randint(1, 255)),
                            '192.168.1.1': '{0}.{1}'.format(base_ip, '1'),
                            '52:5e:0a:40:43:c8': '{0}'.format(random.choice(mac_addresses)),
                            '00:00:5f:00:0b:12': '{0}'.format(random.choice(mac_addresses))}
        substrs = sorted(arp_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        arp_update = regexp.sub(lambda match: arp_replacements[match.group(0)], arp)
        arp_file.write(arp_update.strip("\n"))
        arp_file.truncate()
        arp_file.close()
        print "Arp file changed!\n"


def version_uname(cowrie_install_dir):
    version, uname = random.choice(list(nix_versions.items()))
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/proc/version"), "w")  as version_file:
        version_file.write(version)
        version_file.close()
    with open("{0}{1}".format(cowrie_install_dir, "/cowrie/commands/uname.py"), "r+")  as uname_file:
        uname_py = uname_file.read()
        uname_file.seek(0)
        refunc = "(?<=version ).*?(?= \()"
        uname_kernel = re.findall(refunc, version)
        replacements = {"Linux %s 3.2.0-4-amd64 #1 SMP Debian 3.2.68-1+deb7u1 x86_64 GNU/Linux": version,
                        "3.2.0-4-amd64": '{0}'.format(uname_kernel[0]), 'amd64': 'x86_64'}
        substrs = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        uname_update = regexp.sub(lambda match: replacements[match.group(0)], uname_py)
        uname_file.write(uname_update.strip("\n"))
        uname_file.truncate()
        uname_file.close()
    print "Version & Uname file changed!\n"


def meminfo_py(cowrie_install_dir):
    kb_ram = ram_size * 1000
    meminfo = \
        'MemTotal:        {0} kB\nMemFree:         {1} kB\nMemAvailable:    {2} kB\nCached:          {3} kB\nSwapCached:            0 kB\n' \
        'Active:          {4} kB\nInactive:        {5} kB\nActive(anon):     {6} kB\nInactive(anon):   {7} kB\nActive(file):    {8} kB\n' \
        'Inactive(file):  {9} kB\nUnevictable:          64 kB\nMlocked:              64 kB\nSwapTotal:             0 kB\nSwapFree:              0 kB\n' \
        'Dirty:              {10} kB\nWriteback:             0 kB\nAnonPages:        {11} kB\nMapped:            {12} kB\nShmem:             {13} kB\n' \
        'Slab:              {14} kB\nSReclaimable:      {15} kB\nSUnreclaim:        {16} kB\nKernelStack:       {17} kB\nPageTables:        {18} kB\n' \
        'NFS_Unstable:          0 kB\nBounce:                0 kB\nWritebackTmp:          0 kB\nCommitLimit:     {19} kB\nCommitted_AS:    {20} kB\n' \
        'VmallocTotal:   {21} kB\nVmallocUsed:           0 kB\nVmallocChunk:          0 kB\nHardwareCorrupted:     0 kB\nAnonHugePages:    {22} kB\n' \
        'HugePages_Total:       0\nHugePages_Free:        0\nHugePages_Rsvd:        0\nHugePages_Surp:        0\nHugepagesize:       2048 kB\n' \
        'DirectMap4k:      {23} kB\nDirectMap2M:      {24} kB'.format(kb_ram, '{0}'.format(kb_ram / 2), '{0}'.format(
            kb_ram - random.randint(100000, 400000)),
                                                                      '{0}'.format(
                                                                          kb_ram - random.randint(100000, 200000)),
                                                                      '{0}'.format(kb_ram / 2),
                                                                      '{0}'.format(kb_ram / 3),
                                                                      '{0}'.format(kb_ram / 24),
                                                                      '{0}'.format(kb_ram / 48),
                                                                      '{0}'.format(int(kb_ram / 2.75)),
                                                                      '{0}'.format(int(kb_ram / 3.1)),
                                                                      '{0}'.format(random.randint(1000, 4000)),
                                                                      '{0}'.format(int(kb_ram / 10.45)),
                                                                      '{0}'.format(int(kb_ram / 133)),
                                                                      '{0}'.format(int(kb_ram / 180)),
                                                                      '{0}'.format(int(kb_ram / 90)),
                                                                      '{0}'.format(int(kb_ram / 75)),
                                                                      '{0}'.format(int(kb_ram / 170)),
                                                                      '{0}'.format(int(kb_ram / 210)),
                                                                      '{0}'.format(int(kb_ram / 172)),
                                                                      '{0}'.format(int(kb_ram / 1.8)),
                                                                      '{0}'.format(int(kb_ram / 2.5)),
                                                                      '{0}'.format(int(kb_ram * 10.3)),
                                                                      '{0}'.format(int(kb_ram / 17)),
                                                                      '{0}'.format(int(kb_ram / 25)),
                                                                      '{0}'.format(int(kb_ram / 20)))
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/proc/meminfo"), "w")  as new_meminfo:
        new_meminfo.write(meminfo)
        new_meminfo.close()
        print "Meminfo Info file changed!\n"


def mounts(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/proc/mounts"), "r+") as mounts_file:
        mounts = mounts_file.read()
        mounts_file.seek(0)
        mounts_replacements = {'rootfs / rootfs rw 0 0': '', '10240': '{0}'.format(random.randint(10000, 25000)),
                               '997843': '{0}'.format(random.randint(950000, 1000000)),
                               '1613336': '{0}'.format(random.randint(1500000, 2500000)),
                               '/dev/dm-0 / ext3': '/dev/{0}1 / ext4'.format(random.choice(physical_hd)),
                               '/dev/sda1 /boot ext2 rw,relatime 0 0': '/dev/{0}2 /{1} ext4 rw,nosuid,relatime 0 0'.format(
                                   random.choice(physical_hd), random.choice(mount_names)),
                               'mapper': '{0}'.format(random.choice(usernames))}
        substrs = sorted(mounts_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        mounts_update = regexp.sub(lambda match: mounts_replacements[match.group(0)], mounts)
        mounts_update += random.choice(mount_additional)
        mounts_file.write(mounts_update.strip("\n"))
        mounts_file.truncate()
        mounts_file.close()
        print "Mounts Info file changed!\n"


def cpuinfo(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/proc/cpuinfo"), "r+") as cpuinfo_file:
        cpuinfo = cpuinfo_file.read()
        cpuinfo_file.seek(0)
        cpu_mhz = "{0}{1}".format(processor.split("@ ")[1][:-3].replace(".", ""), "0.00")
        no_processors = processor.split("TM) i")[1].split("-")[0]
        cpu_replacements = {"Intel(R) Core(TM)2 Duo CPU     E8200  @ 2.66GHz": processor,
                            ": 23": ": {0}".format(random.randint(60, 69)), ": 2133.305": ": {0}".format(cpu_mhz),
                            ": 10": ": {0}".format(random.randint(10, 25)),
                            ": 4270.03": ": {0}".format(random.randint(4000.00, 7000.00)),
                            ": 6144 KB": ": {0} KB".format(1024 * random.choice(range(2, 16, 2))),
                            "lahf_lm": " ".join(random.sample(cpu_flags, random.randint(6, 14))),
                            "siblings	: 2": "{0}{1}".format("siblings	: ", no_processors)}
        substrs = sorted(cpu_replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        cpuinfo_update = regexp.sub(lambda match: cpu_replacements[match.group(0)], cpuinfo)
        cpuinfo_file.write(cpuinfo_update)
        cpuinfo_file.truncate()
        cpuinfo_file.close()
        print "CPU Info file changed!\n"


def group(cowrie_install_dir):
    y = 0
    num = 1001
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/group"), "r+") as group_file:
        group = group_file.read()
        group_file.seek(0)
        while y < len(users):
            if y == 0:
                new_user = "{0}:x:{1}:{2}:{3},,,:/home/{4}:/bin/bash".format(users[y], str(num), str(num), users[y],
                                                                             users[y])
                replacements = {"richard": users[y], "sudo:x:27:": "{0}{1}".format("sudo:x:27:", users[y])}
                substrs = sorted(replacements, key=len, reverse=True)
                regexp = re.compile('|'.join(map(re.escape, substrs)))
                group_update = regexp.sub(lambda match: replacements[match.group(0)], group)
            elif y == 1:
                group_update += "{0}:x:{1}:".format(users[y], str(num))
                num = num + 1
            elif y > 1:
                group_update += "\n{0}:x:{1}:".format(users[y], str(num))
                num = num + 1
            y = y + 1
        group_file.write(group_update)
        group_file.truncate()
        group_file.close()
        print "Group file changed!\n"


def passwd(cowrie_install_dir):
    y = 0
    num = 1000
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/passwd"), "r+") as passwd_file:
        passwd = passwd_file.read()
        passwd_file.seek(0)
        while y < len(users):
            if y == 1:
                new_user = "{0}:x:{1}:{2}:{3},,,:/home/{4}:/bin/bash".format(users[y], str(num), str(num), users[y],
                                                                             users[y])
                replacements = {"richard:x:1000:1000:Richard Texas,,,:/home/richard:/bin/bash": new_user}
                substrs = sorted(replacements, key=len, reverse=True)
                regexp = re.compile('|'.join(map(re.escape, substrs)))
                passwd_update = regexp.sub(lambda match: replacements[match.group(0)], passwd)
            elif y > 1:
                passwd_update += "{0}:x:{1}:{2}:{3},,,:/home/{4}:/bin/bash".format(users[y], str(num), str(num),
                                                                                   users[y], users[y])
            y = y + 1
            num = num + 1
        passwd_file.write(passwd_update)
        passwd_file.truncate()
        passwd_file.close()
        print "Passwd file changed!\n"


def shadow(cowrie_install_dir):
    x = 0
    shadow_update = ""
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/shadow"), "r+") as shadow_file:
        shadow = shadow_file.read()
        shadow_file.seek(0)
        days_since = random.randint(16000, 17200)
        salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        while x < len(users):
            if x <= 1:
                gen_pass = crypt.crypt(password[x], "$6$" + salt)
                salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                new_user = "{0}:{1}:{2}:0:99999:7:::".format(users[x], gen_pass, random.randint(16000, 17200))
                new_root_pass = crypt.crypt("password", "$6$" + salt)
                replacements = {"15800": str(days_since),
                                "richard:$6$ErqInBoz$FibX212AFnHMvyZdWW87bq5Cm3214CoffqFuUyzz.ZKmZ725zKqSPRRlQ1fGGP02V/WawQWQrDda6YiKERNR61:15800:0:99999:7:::\n": new_user,
                                "$6$4aOmWdpJ$/kyPOik9rR0kSLyABIYNXgg/UqlWX3c1eIaovOLWphShTGXmuUAMq6iu9DrcQqlVUw3Pirizns4u27w3Ugvb6": new_root_pass}
                substrs = sorted(replacements, key=len, reverse=True)
                regexp = re.compile('|'.join(map(re.escape, substrs)))
                shadow_update = regexp.sub(lambda match: replacements[match.group(0)], shadow)
            elif x > 1:
                gen_pass = crypt.crypt(password[x], "$6$" + salt)
                shadow_update += "\n{0}:{1}:{2}:0:99999:7:::".format(users[x], gen_pass, random.randint(16000, 17200))
            x = x + 1
        shadow_file.write(shadow_update)
        shadow_file.truncate()
        shadow_file.close()
        print "Shadow file changed!\n"


def cowrie_cfg(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/cowrie.cfg"), "r+") as cowrie_cfg:
        cowrie_config = cowrie_cfg.read()
        cowrie_cfg.seek(0)
        replacements = {"svr04": hostname, "#fake_addr = 192.168.66.254": "fake_addr = {0}".format(ip_address),
                        "ssh_version_string = SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2": "ssh_version_string = {0}".format(
                            random.choice(ssh_ver))}
        substrs = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        config_update = regexp.sub(lambda match: replacements[match.group(0)], cowrie_config)
        cowrie_cfg.write(config_update)
        cowrie_cfg.truncate()
        cowrie_cfg.close()
        print "Hostname config changed!\n"


def hosts(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/hosts"), "r+") as host_file:
        hosts = host_file.read()
        host_file.seek(0)
        host_file.write(hosts.replace("nas3", hostname))
        host_file.truncate()
        host_file.close()
        print "Hosts file changed!\n"


def hostname_py(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/hostname"), "r+") as hostname_file:
        hostname_contents = hostname_file.read()
        hostname_file.seek(0)
        hostname_file.write(hostname_contents.replace("svr04", hostname))
        hostname_file.truncate()
        hostname_file.close()
        print "Hostname file changed!\n"


def issue(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/honeyfs/etc/issue"), "r+") as issue_file:
        issue = issue_file.read()
        issue_file.seek(0)
        issue_file.write(issue.replace("Debian GNU/Linux 7", random.choice(os)))
        issue_file.truncate()
        issue_file.close()
        print "Issue file changed!\n"


def userdb(cowrie_install_dir):
    with open("{0}{1}".format(cowrie_install_dir, "/data/userdb.txt"), "r+") as userdb_file:
        userdb = userdb_file.read()
        userdb_file.seek(0)
        replacements = {"richard:x:*": "", "richard:x:fout": ""}
        substrs = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))
        userdb_update = regexp.sub(lambda match: replacements[match.group(0)], userdb)
        userdb_file.write(userdb_update.strip("\n"))
        for user in users:
            userdb_file.write("\n{0}:x:*".format(user))
        userdb_file.truncate()
        userdb_file.close()
        print "UserDB file changed!\n"


def fs_pickle(cowrie_install_dir):
    launch = "python {0}/bin/fsctl {1}/data/fs.pickle".format(cowrie_install_dir, cowrie_install_dir)
    p = pexpect.spawn(launch)
    p.expect(".*.\r\n\r\nfs.pickle:.*")
    p.sendline("rm -r /home/richard")
    p.expect(".*fs.pickle.*")
    for user in users:
        p.sendline("mkdir /home/{0}".format(user))
        p.expect(".*fs.pickle.*")
    p.sendline("exit")


def allthethings(cowrie_install_dir):
    try:
        base_py(cowrie_install_dir)
        free_py(cowrie_install_dir)
        ifconfig_py(cowrie_install_dir)
        arp_py(cowrie_install_dir)
        version_uname(cowrie_install_dir)
        meminfo_py(cowrie_install_dir)
        mounts(cowrie_install_dir)
        cpuinfo(cowrie_install_dir)
        group(cowrie_install_dir)
        passwd(cowrie_install_dir)
        shadow(cowrie_install_dir)
        cowrie_cfg(cowrie_install_dir)
        hosts(cowrie_install_dir)
        hostname_py(cowrie_install_dir)
        issue(cowrie_install_dir)
        userdb(cowrie_install_dir)
        fs_pickle(cowrie_install_dir)
    except:
        e = sys.exc_info()[1]
        print "\nError: {0}\nCheck file path and try again.".format(e)
        pass

if __name__ == "__main__":
    parser = OptionParser(usage='usage: %prog cowrie/install/dir [options]')
    parser.add_option("-a", "--allthethings", action='store_true', default='False', help="Change all the things")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print "[!] Not enough Arguments, Need at least file path"
        parser.print_help()
        sys.exit()

    elif options.allthethings is True:
        allthethings(args[0])
        sys.exit()
