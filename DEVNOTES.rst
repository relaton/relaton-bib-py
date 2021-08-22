====================
Implementation notes
====================

Analyze before conversion
-------------------------

https://github.com/emad-elsaid/rubrowser - awesome tool

Approaches for automated ruby to python translation
---------------------------------------------------

1. https://github.com/cyndis/infl - outdated doesn't work because https://github.com/rubinius/rubinius/issues/3840
2. https://github.com/molhanec/rb2py - create unwanted base class layer
3. https://github.com/valo/rubypython - outdated
4. manual - choosen

How to do XML serialization?
----------------------------

* xml_dataclasses - https://github.com/tobywf/xml_dataclasses - not enough flexibility
* xsdata - https://xsdata.readthedocs.io/en/v21.8/xml.html - not enough flexibility
* Idea for own xml/asciib introspection based serializer was failed because too many custom cases
* own `to_xml` implementation with `xml.etree.ElementTree` - to much monkey work but looks like the only option right now

How to deal with variables which turned into python's keyword?
--------------------------------------------------------------

* append _ at the end (from -> from_) - https://stackoverflow.com/questions/6503920/is-it-possible-to-escape-a-reserved-word-in-python/6504209


reStructuredText vs Markdown
----------------------------

`cookiecutter` by default generated all documentation with `rst`. So I decided to try it

* https://www.zverovich.net/2016/06/16/rst-vs-markdown.html
* https://docutils.sourceforge.io/docs/user/rst/quickref.html

Test framework
--------------

https://www.pythonpool.com/python-unittest-vs-pytest/

No need for the coding comment anymore
--------------------------------------

https://stackoverflow.com/questions/14083111/should-i-use-encoding-declaration-in-python-3

Circular dependency between types
---------------------------------

https://stackoverflow.com/questions/52676647/how-to-define-circularly-dependent-data-classes-in-python-3-7

Wheel package vs EGG package for publishing
-------------------------------------------

https://packaging.python.org/discussions/wheel-vs-egg/

[????] Open question how to simplify imports