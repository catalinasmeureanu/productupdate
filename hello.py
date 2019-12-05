#!/usr/bin/env python3
import requests
import json
import semver
import pyjq
import logging
import argparse
import sys

URL = "https://releases.hashicorp.com/{0}/index.json"


logger = logging.getLogger('ldw')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger.setLevel(logging.DEBUG)

def get_max_version (versions):
    max = '0.0.0'
    for v in versions:
        max=semver.max_ver(max,v)
    return max

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--product', help='Please indicate the product')
    parser.add_argument('-a', '--arch', help='Please indicate the arch')
    parser.add_argument('-os', '--os', help='Please indicate the os')
    parser.add_argument('-v', action='store_true', help='Increase verbosity')
    parser.add_argument('--no-download', action='store_true')

    args = parser.parse_args()
    prod = args.product
    os = args.os
    arch = args.arch
    if args.v :
        logging.info("Setting verbosity on")
        logger.setLevel(logging.DEBUG)
        
    else:
        logger.setLevel(logging.INFO)


    logger.debug(" Input parameters are product={0} os={1} arch={2}".format(prod, os,arch))
    response=requests.get(URL.format(prod))
    try:
        response.raise_for_status()
    except:
        logger.error("Could not find the indicated product:'{0}'".format(prod))
        sys.exit(2)

    data=response.json()
    vers = pyjq.all('.versions[].version', data)
    if len(vers) ==0 :
        logger.error("Could not find the indicated product:'{0}'".format(prod))
        sys.exit(2)

    max_ver=get_max_version(vers)
    logger.info("Latest version of {0} is : {1}".format(prod, max_ver))
    
    fis = pyjq.all('.versions["{0}"].builds[] | select(.os == "{1}" and .arch == "{2}") | .url'.format(max_ver,os,arch), data)
    if len(fis) == 0:
        logger.error("Could not find the indicated release for product:'{0}' arch: '{1}' os: '{2}'".format(prod,arch,os))
        sys.exit(1)

    logger.info("File identified is {0}".format(fis[0]))
    download_file(fis[0])
    
    
if __name__ == '__main__':
    main()

