#!/usr/bin/env python3
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:

10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0
(Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
from urllib import request
import argparse
from collections import OrderedDict


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    url_dict = {}
    with open(filename, 'r') as f:
        text = f.readlines()
        for line in text:
            match = re.search(r'(?:\s)(/.*?/puzzle/.*?(.{5}jpg))', line)
            if match:
                url = "https://code.google.com" + match.group(1)
                url_sort_key = match.group(2)
                url_dict[url_sort_key] = url
        filtered_list = url_dict
        filtered_list = OrderedDict(sorted(url_dict.items()))
        print(filtered_list.items())
        return filtered_list.values()


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    print("fetching images")
    try:
        os.mkdir(dest_dir)
    except OSError:
        print("there is already a directory with that name")
        sys.exit()
    else:
        os.chdir(dest_dir)

    completion = 1
    img_list = []  # list for creating html index

    for url in img_urls:
        print("fetching images " +
              str((completion / len(img_urls))*100) + "% complete")
        request.urlretrieve(url, 'img' + str(completion))
        img_list.append('img' + str(completion))
        completion += 1

    with open('index.html', 'w') as f:
        f.write('<html><body>')
        for img in img_list:
            f.write("<img src='{}'>".format(img))
        f.write('</body></html>')


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
