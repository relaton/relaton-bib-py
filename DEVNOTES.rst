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

Key differences
---------------

1. cyclic dependency possible in python
2. keyword different, append _
3. not allow to have method and pproperty with the same name in the same class
4. brackets on functions mandatory


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

TypeError: non-default argument 'name' follows default argument
---------------------------------------------------------------

 - https://bugs.python.org/issue39300
 - https://bugs.python.org/issue36077
 - https://stackoverflow.com/questions/51575931/class-inheritance-in-python-3-7-dataclasses/53085935#53085935

List vs list
------------

 - https://stackoverflow.com/questions/52629265/static-typing-in-python3-list-vs-list

iso639-lang vs iso-639
----------------------

https://pypi.org/project/iso639-lang/ vs https://pypi.org/project/iso-639/

iso-639 - has less size



Open questions
--------------

[?] How to simplify imports?
[?] Acsiidoc does order matters?
[?] Some test framework which can generage random dataclass?