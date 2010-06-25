import os
import sys
import urllib
import gettext
import xml.dom.minidom
import pysvn

import locale
__lang__ = locale.getdefaultlocale()[0]
del locale

if sys.platform == 'win32':
    os.environ['LANGUAGE'] = __lang__

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

gettext.bindtextdomain('svnexport', 'locale')
gettext.bind_textdomain_codeset('svnexport', __encoding__)
gettext.textdomain('svnexport')
_ = gettext.gettext

class SVNExportException(Exception):
    def __init__(self, url, *args):
        Exception.__init__(self, *args)
        self.url = url
        self.msg = _('URL "%s" is not available').decode(__encoding__) %self.url
        
    def __str__(self):
        return self.msg.encode(__encoding__)

class ConfigParser():
    '''Reads the .svnexport.xml file

Following structure have to be present i.e.:
<svnexport>
  <api>
    <config>
      <pattern>%(name)s-%(rev)i%(ext)s</pattern>
    </config>
  </api>
</svnexport>'''
    
    def __init__(self):
        self.pattern = None
        
        self.__read_config__()
        
    def __read_config__(self):
        self.config_file = os.path.join(os.path.expanduser('~'), '.svnexport.xml')

        if os.path.isfile(self.config_file):
            try:
                self.config_dom = xml.dom.minidom.parse(self.config_file)

                root = self.config_dom.documentElement

                config = root.getElementsByTagName('api')[0].getElementsByTagName('config')[0]
                
                for cfg in config.childNodes:
                    if cfg.nodeName == 'pattern':
                        p = ''
                        for t in cfg.childNodes:
                             p += t.data

                        self.pattern = p.strip()
            except:
                self.pattern = '%(name)s-%(rev)i%(ext)s'
        else:
            self.pattern = '%(name)s-%(rev)i%(ext)s'


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

def export_entry(rurl, epath, entry, pattern='%(name)s-%(rev)i%(ext)s'):
    log = ''
    uname = entry[0].decode('utf-8')
    rev = entry[2]
    
    if entry[1] == 'dir':
        log = _('Created directory "%s"...') %uname
        os.mkdir(os.path.join(epath, uname))
    elif entry[1] == 'file':
        try:
            log = _('Exported "%s": r%i...') %(uname, rev)

            root, ext = os.path.splitext(uname)
            fname = pattern %{'name': root,
                              'rev': rev,
                              'ext': ext}
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
            t = _('Dir')
        elif e[1] == 'file':
            t = _('File')

        if not t == None:
            text += '%s\t: %s: r%i\n' %(t, e[0].decode('utf-8'), e[2])

    return text

def export(rurl, epath, list_only=False, entry_rev=False):
    cfg = ConfigParser()
    entries = get_entries(rurl, entry_rev)
    
    if not list_only:
        for e in entries:
            print export_entry(rurl, epath, e, cfg.pattern).encode(__encoding__)
    else:
        print list_entries(entries).encode(__encoding__)
        

if __name__ == '__main__':
    from optparse import OptionParser
    
    usage = '''usage: %prog [-e] -r URL [-o PATH]]
       %prog [-e] -l'''
    
    parser = OptionParser(usage=usage)
    parser.add_option('-r', '--repos', dest='repos',
                      help=_('The repository URL'), metavar='URL')
    parser.add_option('-o', '--output', dest='output',
                      help=_('Export to path'), metavar='PATH')
    parser.add_option('-e', '--entry-rev', dest='entry_rev',
                      action='store_true', default=False,
                      help=_('Use the revison of the entry instead of repository'))
    parser.add_option('-l', '--list', dest='list',
                      action='store_true', default=False,
                      help=_('List info only. Do not export somthing'))
    parser.add_option('-v', '--version', dest='version',
                      action='store_true', default=False,
                      help=_('Show version and exit'))

    (options, args) = parser.parse_args()

    if options.version:
        print 'Version: ', __version__
        sys.exit(0)

    epath = None 
    if not options.repos:
        print _('Repository must be specified\nTry "%s --help" for more information') %sys.argv[0]
        sys.exit(1)
    else:
        if options.output == None:
            rname = os.path.basename(str(options.repos).strip().strip('/'))
            epath = os.path.join(os.getcwd(), rname)
        else:
            epath = os.path.join(str(options.output))
        
    if not options.list:
        if os.path.exists(epath):
            print _('Path "%s" already exists') %epath
            sys.exit(1)
        else:
            os.mkdir(epath)

    try:
        export(options.repos, epath, options.list, options.entry_rev)
    except Exception, e:
        print e
        
