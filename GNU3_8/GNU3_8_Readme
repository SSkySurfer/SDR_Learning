#Readme for GNUradio 3.8 version

## This will work with Pluto and GNU radio3.8 distros
* Most of the work was done on Ubuntu 20.04
* PlutoSDR was the main transceiver board

## Configure Virtual Machine with instant-GNUradio
* Was run through a virtual machine with instant GNUradio: https://github.com/bastibl/instant-gnuradio
* instant GNU radio was not adapted for PlutoSDR, so the proper iio-toolbox was installed

## Instructions for using Virtual Machine with VMware
* For use with Virtual Box, no networking changes are requried, but for VM ware, /etc/netstart/xxxxxxx-config.yaml was modified.
  - To modify, delete ens030XX and replace with the network id from "ip link show" command in the VM terminal. It will be something like ens33. edit the yaml file in sudo with the command "sudo gedit xxxxxxx-config.yaml", replace the network name, then save and close the file.
  - For sound, in the VMware settings "Edit virtual machine settings", add an interface with the "+" sign. Add the sound card from the host machine and save the configuration.
