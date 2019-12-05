# Purpose
This repo can be used to find the latest version of a Hashicorp product. The build for the latest version is downloaded for a given operating system and architecture.

# How to use it

 Input parameters:
 * Hashicorp product
 * Architecture
 * Operating system

 To run the script:

`$ python3.7 hello.py -p=product -a=arch -os=operatingsystem`

Example:

`$ python3.7 hello.py -p=packer -a=amd64 -os=solaris`

The build will be downloaded in the current directory.

To enable verbose mode add parameter `-v`.
