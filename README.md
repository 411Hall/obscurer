# Obscurer

## Cowrie Honeypot Obscurer

A Python script designed to remove (nearly) all default values from a Cowrie Honey Pot installtion. 

A random host profile with new users, hostname, groups, file shares, harddrive(s) sizes, mounts, cpu, ram, OS version, IP address, MAC addresses and SSH version is created. In theory this makes it much harder to easily detect default cowrie honeypot installations.

Be aware this will wipe out any custome configuration you have made to the cowrie.cfg.

## Requirements 

Fresh Cowrie Install
python 2.7
pip install pexpect

## Usage

```
python obscurer.py [options] path/to/cowrie/directory

Options:
  -h, --help    Show this help message and exit
  -a, --allthethings  Change all of the default values
  
Example:
python obscurer.py -a /opt/cowrie 
```

Once the script has completed restart the Cowrie service and SSH to the host to confirm changes have been made.
