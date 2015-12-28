LEGO Mindstorms EV3 Comparison
==============================

This project is meant to complement the comparison made in
`The Difference Between LEGO MINDSTORMS EV3 Home Edition (#31313) and LEGO MINDSTORMS Education EV3 (#45544)`_,
an article by `Laurens Valk`_.

There are two editions of LEGO Mindstorms, LEGO's Robotics Invention System (RIS),
the EV3 Home Edition and the Education Edition.  You may wonder what is the difference
and which one is right for you.  Reviews on Amazon will tell you that the Education
set is meant for schools, with a more robust plastic packaging and shorter, in-class
exercises to go through instead of full-blown projects to be exercised from start to
end that fulfill you as a robot newbie with the Home Edition.

If you one day want to upgrade your set you'll be wondering if you can combine the
two.  The data elaborated in this project may help you with your decision on what
pieces to buy.

Usage
-----

``Lego-Mindstorms-Editions-Comparison.ods``, a LibreOffice Calc spread sheet, lists
the pieces of all sets combined.  Columns ``F`` and ``I`` tell you which pieces to
buy if you have either Home Edition + Expansion Set or Education Edition + Expansion
Set.  You can filter the columns using the "Auto Filter" in the first row.

The spread sheet document specifically targets the two sections
*"‘Upgrading’ Elements from Education Edition to Home Edition"* and
*"‘Upgrading’ Elements from Home Edition to Education Edition"* in Lauren's article.
Specifically, the document will make the latter section less vague with regards to
the *"you’ll need to purchase [...] certain Technic building elements"* statement.

``lego-mindstorms-pieces.py`` is a Python3 script to generate the combined list of
LEGO pieces from the three separate inventory lists.  It takes three file names as
an argument.

Resources
---------

* LEGO Mindstorms, `31313 EV3 Home Edition`_, User Guide (look for "User Guide" button)
* LEGO Mindstorms Education, `45544 EV3 Core Set`_, Element Overview
* LEGO Mindstorms Education, `45560 EV3 Expansion Set`_, Element Overview
* Brickset inventory lists: 31313-1_, 45544-1_, 45560-1_
* `The Difference Between LEGO MINDSTORMS EV3 Home Edition (#31313) and LEGO MINDSTORMS Education EV3 (#45544)`_
* `LEGO Answers`_ question (Bricks, a StackExchange site)


.. _The Difference Between LEGO MINDSTORMS EV3 Home Edition (#31313) and LEGO MINDSTORMS Education EV3 (#45544):
    http://robotsquare.com/2013/11/25/difference-between-ev3-home-edition-and-education-ev3/
.. _Laurens Valk: http://robotsquare.com/about/
.. _31313 EV3 Home Edition: http://www.lego.com/en-us/mindstorms/downloads
.. _45544 EV3 Core Set: https://education.lego.com/en-us/lego-education-product-database/mindstorms-ev3/45544-lego-mindstorms-education-ev3-core-set
.. _45560 EV3 Expansion Set: https://education.lego.com/en-us/lego-education-product-database/mindstorms-ev3/45560-lego-mindstorms-education-ev3-expansion-set
.. _31313-1: http://brickset.com/inventories/31313-1
.. _45544-1: http://brickset.com/inventories/45544-1
.. _45560-1: http://brickset.com/inventories/45560-1
.. _LEGO Answers: http://bricks.stackexchange.com/questions/1819/what-is-different-between-the-ev3-home-and-educational-sets/

Your Contribution
-----------------

If you find a typo, an error, a critical mistake or feel there's some enhancement
needed please feel free to `open an issue`_, or even better clone the repository,
apply your changes, and `place a pull request`_.  Your contribution is welcome!


.. _open an issue: https://github.com/bittner/lego-mindstorms-ev3-comparison/issues
.. _place a pull request: https://github.com/bittner/lego-mindstorms-ev3-comparison/pulls
