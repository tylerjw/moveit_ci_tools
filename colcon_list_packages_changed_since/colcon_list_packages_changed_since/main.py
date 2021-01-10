#!/usr/bin/env python3

# Copyright 2021 PickNik LLC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the PickNik LLC nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import argparse
import os
import subprocess
import sys


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='List packages that have changed files since point in git history.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'path',
        help='<path> is the root of a git repo containing ros packages')
    parser.add_argument(
        'point',
        help='<point> is a git branch, tag, or commit')

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--names-only', '-n',
        action='store_true',
        default=False,
        help='Output only the name of each package but not the path')
    group.add_argument(
        '--paths-only', '-p',
        action='store_true',
        default=False,
        help='Output only the path of each package but not the name')
    args = parser.parse_args(argv)

    if not os.path.isdir(os.path.join(args.path, '.git')):
        print("'%s' is not the base of a git repo" % args.path, file=sys.stderr)
        return 1

    packages = get_packages_changed_since(args.path, args.point)

    lines = []
    for package in packages:
        if args.names_only:
            lines.append(package['name'])
        elif args.paths_only:
            lines.append(package['path'])
        else:
            lines.append('%s\t%s\t%s' % (package['name'], package['path'], package['type']))

    lines.sort()
    for line in lines:
        print(line)

    return 0


def find_executable(file_names):
    paths = os.getenv('PATH').split(os.path.pathsep)
    for file_name in file_names:
        for path in paths:
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                return file_path
    return None


def get_packages_in_repo(repo_path):
    bin_names = [
        'colcon',
    ]
    colcon_bin = find_executable(bin_names)
    if not colcon_bin:
        print('Could not find %s executable' %
              ' / '.join(["'%s'" % n for n in bin_names]), file=sys.stderr)
        return 1

    cmd = [colcon_bin, 'list', '--base-paths', repo_path]
    output = []
    try:
        output = subprocess.check_output(cmd).strip().decode().split()
    except subprocess.CalledProcessError as e:
        print('The invocation of "%s" failed with error code %d: %s' %
              (os.path.basename(colcon_bin), e.returncode, e),
              file=sys.stderr)

    return [
        {
            'name': output[x],
            'path': output[x+1],
            'type': output[x+2]
        }
        for x in range(0, len(output), 3)
    ]


def get_packages_changed_since(repo_path, point):
    packages = get_packages_in_repo(repo_path)

    bin_names = [
        'git',
    ]
    git_bin = find_executable(bin_names)
    if not git_bin:
        print('Could not find %s executable' %
              ' / '.join(["'%s'" % n for n in bin_names]), file=sys.stderr)
        return 1

    def modified_files_test(package):
        cmd = [
            'git', 'diff', '--name-only', '--diff-filter=MA',
            point + '..HEAD', os.path.relpath(package['path'], repo_path)
        ]
        modified_files = []
        try:
            modified_files = subprocess.check_output(cmd, cwd=repo_path).strip().decode().split()
        except subprocess.CalledProcessError as e:
            print('The invocation of "%s" failed with error code %d: %s' %
                  (os.path.basename(git_bin), e.returncode, ' '.join(cmd)),
                  file=sys.stderr)
            return False
        return (len(modified_files) > 0)

    filtered_packages = list(filter(modified_files_test, packages))
    return filtered_packages


if __name__ == '__main__':
    sys.exit(main())
