# -*- coding: iso-8859-1 -*-

"""
:Author: Martin Wendt, moogle(at)wwwendt.de 
:Copyright: Licensed under the MIT license, see LICENSE file in this package.

Small wrapper for different etree packages.

See DEVELOPERS.txt_ for more information about the WsgiDAV architecture.

.. _DEVELOPERS.txt: http://wiki.wsgidav-dev.googlecode.com/hg/DEVELOPERS.html  
"""

__docformat__ = "reStructuredText"


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# Import XML support
useLxml = False
try:
    from lxml import etree
    useLxml = True
except ImportError:
    try:    
        # Try xml module (Python 2.5 or later) 
        from xml.etree import ElementTree as etree
        print "WARNING: Could not import lxml: using xml instead (slower). Consider installing lxml from http://codespeak.net/lxml/."
    except ImportError:
        try:
            # Try elementtree (http://effbot.org/zone/element-index.htm) 
            from elementtree import ElementTree as etree
        except ImportError:
            print "ERROR: Could not import lxml, xml, nor elementtree. Consider installing lxml from http://codespeak.net/lxml/ or update to Python 2.5 or later."
            raise


#===============================================================================
# XML
#===============================================================================

def stringToXML(text):
    """Convert XML string into etree.Element."""
    try:
        return etree.XML(text)
    except:
        # TODO:
        # litmus fails, when xml is used instead of lxml
        # 18. propget............... FAIL (PROPFIND on `/temp/litmus/prop2': Could not read status line: connection was closed by server)
        # text = <ns0:high-unicode xmlns:ns0="http://example.com/neon/litmus/">&#55296;&#56320;</ns0:high-unicode>
        raise


def xmlToString(element, pretty_print=False):
    """Wrapper for etree.tostring, that takes care of unsupported pretty_print 
    option and prepends an encoding header."""
    if useLxml:
        xml = etree.tostring(element, 
                             encoding="UTF-8", 
                             xml_declaration=True, 
                             pretty_print=pretty_print)
    else:
        xml = etree.tostring(element, "UTF-8")
    assert xml.startswith("<?xml ") 
    return xml


def makeMultistatusEL():
    """Wrapper for etree.Element, that takes care of unsupported nsmap option."""
    if useLxml:
        return etree.Element("{DAV:}multistatus", nsmap={"D": "DAV:"})
    return etree.Element("{DAV:}multistatus")


def makePropEL():
    """Wrapper for etree.Element, that takes care of unsupported nsmap option."""
    if useLxml:
        return etree.Element("{DAV:}prop", nsmap={"D": "DAV:"})
    return etree.Element("{DAV:}prop")


def makeSubElement(parent, tag, nsmap=None):
    """Wrapper for etree.SubElement, that takes care of unsupported nsmap option."""
    if useLxml:
        return etree.SubElement(parent, tag, nsmap=nsmap)
    return etree.SubElement(parent, tag)


def elementContentAsString(element):
    """Serialize etree.Element.
    
    Note: element may contain more than one child or only text (i.e. no child 
          at all). Therefore the resulting string may raise an exception, when
          passed back to etree.XML(). 
    """
    if len(element) == 0:
        return element.text or ""  # Make sure, None is returned as '' 
    stream = StringIO()
    for childnode in element:
        print >>stream, xmlToString(childnode, pretty_print=False)
    s = stream.getvalue()
    stream.close()
    return s


#===============================================================================
# TEST
#===============================================================================
    
if __name__ == "__main__":
    pass