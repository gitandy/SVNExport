import os
import sys
import urllib
import pysvn

import version
__version__ = version.VERSION
del version
__author_name__ = 'Andreas Schawo'
__author_email__ = 'andreas@schawo.de'
__copyright__ = 'Copyright (c) 2010, Andreas Schawo, All rights reserved'
__license__ = '''Copyright (c) 2010, Andreas Schawo <andreas@schawo.de>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
   3. Neither the name of the authors nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHORS 'AS IS' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.'''

__encoding__ = 'cp1252'
try:
    if sys.stdout.encoding:
        __encoding__ = sys.stdout.encoding
except:
    pass

class SVNExportException(Exception):
    def __init__(self, url, *args):
        Exception.__init__(self, *args)
        self.url = url
        self.msg = 'URL "%s" is not available' %self.url
        
    def __str__(self):
        return self.msg

def get_entries(rurl, entry_rev=False):
    try:
        client = pysvn.Client()
        info = client.info2(rurl, recurse=True)

        entries = []
        for i in info[1:]:
            name = i[0]
            kind = str(i[1]['kind'])
            rev = i[1]['rev'].number
            if entry_rev:
                rev = i[1]['last_changed_rev'].number

            entries.append((name, kind, rev))

        return tuple(entries)
    except pysvn.ClientError:
        raise SVNExportException(rurl)

def export_entry(rurl, epath, entry):
    log = ''
    uname = entry[0].decode('utf-8')
    rev = entry[2]
    
    if entry[1] == 'dir':
        log = 'Created directory "%s"...' %uname
        os.mkdir(os.path.join(epath, uname))
    elif entry[1] == 'file':
        try:
            log = 'Exported "%s": r%i...' %(uname, rev)

            root, ext = os.path.splitext(uname)
            fname = '%s-r%i%s' %(root, rev, ext)
            with open(os.path.join(epath, fname), 'wb') as f:
                client = pysvn.Client()
                f.write(client.cat(rurl + '/' + urllib.quote(entry[0])))
        except pysvn.ClientError:
            raise SVNExportException(rurl)

    return log

def list_entries(entries):
    text = ''

    for e in entries:
        t = None
        if e[1] == 'dir':
            t = 'D'
        elif e[1] == 'file':
            t = 'F'

        if not t == None:
            text += '%s: %s: r%i\n' %(t, e[0].decode('utf-8'), e[2])

    return text

def export(rurl, epath, list_only=False, entry_rev=False):
    entries = get_entries(rurl)
    
    if not list_only:
        for e in entries:
            print export_entry(rurl, epath, e).encode(__encoding__)
    else:
        print list_entries(entries).encode(__encoding__)
        

if __name__ == '__main__':
    from optparse import OptionParser
    
    usage = '''usage: %prog [-e] -r URL [-o PATH]]
       %prog [-e] -l'''
    
    parser = OptionParser(usage=usage)
    parser.add_option('-r', '--repos', dest='repos',
                      help='The repository URL', metavar='URL')
    parser.add_option('-o', '--output', dest='output',
                      help='Export to path', metavar='PATH')
    parser.add_option('-e', '--entry-rev', dest='entry_rev',
                      action='store_true', default=False,
                      help='Use the revison of the entry instead of repository')
    parser.add_option('-l', '--list', dest='list',
                      action='store_true', default=False,
                      help='List info only. Do not export somthing')
    parser.add_option('-v', '--version', dest='version',
                      action='store_true', default=False,
                      help='Show version and exit')

    (options, args) = parser.parse_args()

    if options.version:
        print 'Version: ', __version__
        sys.exit(0)

    epath = None 
    if not options.repos:
        print 'Repository must be specified\nTry "%s --help" for more information' %sys.argv[0]
        sys.exit(1)
    else:
        if options.output == None:
            rname = os.path.basename(str(options.repos).strip().strip('/'))
            epath = os.path.join(os.getcwd(), rname)
        else:
            epath = os.path.join(str(options.output))
        
    if not options.list:
        if os.path.exists(epath):
            print 'Path "%s" already exists' %epath
            sys.exit(1)
        else:
            os.mkdir(epath)

    export(options.repos, epath, options.list, options.entry_rev)
