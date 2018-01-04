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

Reading
-------

* `The Difference Between LEGO MINDSTORMS EV3 Home Edition (#31313) and LEGO MINDSTORMS Education EV3 (#45544)`_
* `LEGO Answers question`_ (Bricks, a StackExchange site)


.. _The Difference Between LEGO MINDSTORMS EV3 Home Edition (#31313) and LEGO MINDSTORMS Education EV3 (#45544):
    http://robotsquare.com/2013/11/25/difference-between-ev3-home-edition-and-education-ev3/
.. _Laurens Valk: http://robotsquare.com/about/
.. _LEGO Answers question:
    http://bricks.stackexchange.com/questions/1819/what-is-different-between-the-ev3-home-and-educational-sets/

Usage
-----

#. ``Lego-Mindstorms-Editions-Comparison.ods``, a LibreOffice Calc spread sheet, lists
   the pieces of all sets combined.  Columns ``H`` and ``K`` tell you which pieces to
   buy if you have either Home Edition + Expansion Set or Education Edition + Expansion
   Set.  You can filter the columns using the "Auto Filter" in the first row.

   The spread sheet document specifically targets the two sections
   *"‘Upgrading’ Elements from Education Edition to Home Edition"* and
   *"‘Upgrading’ Elements from Home Edition to Education Edition"* in Lauren's article.
   Specifically, the document will make the latter section less vague with regards to
   the *"you’ll need to purchase [...] certain Technic building elements"* statement.

   .. note::

      If you can't or don't want to install `LibreOffice`_ here are some free services
      that display or convert the spread sheet: `convert-doc`_ (view), `Zamzar`_ (convert),
      `convertfiles`_ (convert).  Some let you specify the `raw document url`_ directly.
      `Google Docs`_ and `Zoho Docs`_ also import the spread sheet.


#. ``lego-mindstorms-pieces.py`` is a Python3 script to help with calculating and
   ordering required LEGO Mindstorms EV3 spare parts.  It has three commands:

   ``parse``
      Generate the combined list of LEGO pieces from the 3 separate inventory
      lists (the combined list is what the above mentioned spread sheet is made of).
      It takes three file names as an argument.  Output is sent to ``stdout``.
      You can redirect it to a text file using the ``>`` operator on the command
      line.

   ``missing``
      Generate a list of LEGO parts missing in the combination of the Edu Expansion
      set + Home or Edu Core, that only the other (omitted) set would have.
      The output has the format ``part:quantity,...`` and is sent to ``stdout``.
      You can use the result as a shopping list in the ``order`` command.

   ``order``
      Add a list of LEGO parts and their quantity to the 'Shopping Bag' of LEGO's
      customer service platform.  A browser window will be opened, you'll be able
      to watch the browser do what you would normally do by hand, and execution
      will stop after all pieces have been added, so you can review and finalize
      your order.  (This is just to help you save time on entering 60+ pieces
      manually.  Nothing is ordered on your behalf!)

   For full instructions run: ``python3 lego-mindstorms-pieces.py {command} --help``

.. _LibreOffice: http://www.libreoffice.org/download/
.. _convert-doc: http://www.convert-doc.com/viewer/ods.html
.. _Zamzar: http://www.zamzar.com/convert/ods-to-xlsx/
.. _convertfiles: http://www.convertfiles.com/convert/document/ODS-to-XLS.html
.. _raw document url:
    https://github.com/bittner/lego-mindstorms-ev3-comparison/raw/master/Lego-Mindstorms-Editions-Comparison.ods
.. _Google Docs: https://docs.google.com/
.. _Zoho Docs: https://docs.zoho.com/sheet/

Requirements
~~~~~~~~~~~~

To run ``lego-mindstorms-pieces.py`` you need:

* Python Selenium (see ``requirements.txt``)
* `geckodriver`_
* `chromedriver`_

.. _geckodriver: https://github.com/mozilla/geckodriver/releases
.. _chromedriver: https://sites.google.com/a/chromium.org/chromedriver/

Documentation, Examples, Hints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See the `docs folder`_ for sample output of the ``order`` command, and screenshots
of prepared orders at LEGO's customer service platform.

The order process at LEGO is highly automated.  This usually means that orders
with items out of stock, or orders that are too large will not be processed.
LEGO notifies you with an automatic email in such a case.


.. _docs folder: https://github.com/bittner/lego-mindstorms-ev3-comparison/tree/master/docs

Data Sources
~~~~~~~~~~~~

* LEGO Mindstorms, `31313 EV3 Home Edition`_, User Guide (look for "User Guide" button)
* LEGO Mindstorms Education, `45544 EV3 Core Set`_, Element Overview
* LEGO Mindstorms Education, `45560 EV3 Expansion Set`_, Element Overview
* Brickset inventory lists: 31313-1_, 45544-1_, 45560-1_


.. _31313 EV3 Home Edition: http://www.lego.com/en-us/mindstorms/downloads
.. _45544 EV3 Core Set: https://education.lego.com/en-us/lego-education-product-database/mindstorms-ev3/45544-lego-mindstorms-education-ev3-core-set
.. _45560 EV3 Expansion Set: https://education.lego.com/en-us/lego-education-product-database/mindstorms-ev3/45560-lego-mindstorms-education-ev3-expansion-set
.. _31313-1: http://brickset.com/inventories/31313-1
.. _45544-1: http://brickset.com/inventories/45544-1
.. _45560-1: http://brickset.com/inventories/45560-1

Where To Go From Here?
----------------------

LEGO Parts Research, Shopping And Other Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `LEGO Pick a Brick`_ (official parts shop)
* `LEGO Bricks & Pieces`_ (official customer service) [#note]_
* Rebrickable:

  * compare `Mindstorms vs. Edu Core`_
  * compare `Mindstorms vs. Edu Expansion`_
  * compare `Edu Core vs. Edu Expansion`_
  * search `sets`_, search `parts`_

* Brickset:

  * `Mindstorms EV3`_
  * `Edu EV3 Core`_
  * `Edu EV3 Expansion`_

* `BrickLink > Catalog Search`_ (parts, shops, marketplace)
* `Brick Owl`_ (parts and store search)
* `LEGO parts drawing program`_ (LDraw.org)


.. [#note] Spare parts you want to buy in addition are usually available here.
   Use the 5-digit number of the set you did *not* buy (31313 or 45544) when
   the shop asks you for a set number.

.. _LEGO Pick a Brick: http://shop.lego.com/en-DE/Pick-A-Brick-ByTheme
.. _LEGO Bricks & Pieces: https://wwwsecure.us.lego.com/en-gb/service/replacementparts/order
.. _Mindstorms vs. Edu Core: http://rebrickable.com/compare/31313-1/45544-1
.. _Mindstorms vs. Edu Expansion: http://rebrickable.com/compare/31313-1/45560-1
.. _Edu Core vs. Edu Expansion: http://rebrickable.com/compare/45544-1/45560-1
.. _sets: http://rebrickable.com/pick_set
.. _parts: http://rebrickable.com/search?po=1
.. _Mindstorms EV3: http://brickset.com/sets/31313-1/Mindstorms-EV3
.. _Edu EV3 Core: http://brickset.com/sets/45544-1/Education-EV3-Core-Set
.. _Edu EV3 Expansion: http://brickset.com/sets/45560-1/Education-EV3-Expansion-Set
.. _BrickLink > Catalog Search: http://www.bricklink.com/catalogSearch.asp
.. _Brick Owl: http://www.brickowl.com/
.. _LEGO parts drawing program: http://www.ldraw.org/

Inspiration for LEGO EV3 Robots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LEGO robot programs can be written with the `LEGO MINDSTORMS EV3 Software`_
(on Windows and Mac) or with any programming language supported by the
`ev3dev firmware`_ (platform-independent).

`Open Roberta Lab`_ is available as a visual editor for ev3dev (`setup
instructions`_), featuring Python under the hood.  Also, if you use `Scratch`_
you may be interested in `Scratch extensions`_ (for Windows and Mac).

+---------------------------+--------------------------+----------------------------------------------+
| LEGO firmware             | ev3dev (Python)          | Description                                  |
+===========================+==========================+==============================================+
| **>** `Home Edition robots`_ **(build instructions for 5 official and many more robots)**           |
+---------------------------+--------------------------+----------------------------------------------+
|`Track3r (LEGO)`_          | `Track3r (ev3dev)`_      | Crawler-mounted, all-terrain robot           |
+---------------------------+--------------------------+----------------------------------------------+
| `Spik3r (LEGO)`_          | *n/a*                    | Remote-controlled scorpion robot             |
+---------------------------+--------------------------+----------------------------------------------+
| `R3ptar (LEGO)`_          | `R3ptar (ev3dev)`_       | Scary cobra snake robot                      |
+---------------------------+--------------------------+----------------------------------------------+
| `Gripp3r (LEGO)`_         | `Gripp3r (ev3dev)`_      | Heavy-duty lifting robot                     |
+---------------------------+--------------------------+----------------------------------------------+
| `Ev3rstorm (LEGO)`_       | `Ev3rstorm (ev3dev)`_    | Walking robot firing bullets                 |
+---------------------------+--------------------------+----------------------------------------------+
| **>** `Education Edition Core Set robots`_ **(build instructions for 5 robots)**                    |
+---------------------------+--------------------------+----------------------------------------------+
| `Educator Vehicle`_       | `Educator`_              | Multi-purpose robot for teaching robotics    |
+---------------------------+--------------------------+----------------------------------------------+
| `Sorter`_                 | *n/a*                    | Sorts LEGO bricks by size and color          |
+---------------------------+--------------------------+----------------------------------------------+
| `Gyro Boy`_               | `Balanc3r`_              | Self-balancing robots                        |
+---------------------------+--------------------------+----------------------------------------------+
| `Puppy`_                  | *n/a*                    | Looks and `behaves like a dog`_              |
+---------------------------+--------------------------+----------------------------------------------+
| `Robot Arm H25`_          | *n/a*                    | Robot arm used for assembly in factories     |
+---------------------------+--------------------------+----------------------------------------------+
| **>** `Education Edition Expansion Set robots`_ **(build instructions for 6 robots)**               |
+---------------------------+--------------------------+----------------------------------------------+
| `Znap`_                   | *n/a*                    | Crawler-mounted bat-like animal              |
+---------------------------+--------------------------+----------------------------------------------+
| `Remote Control`_         | *n/a*                    | A remote control for your hand               |
+---------------------------+--------------------------+----------------------------------------------+
| `Stair Climber`_          | *n/a*                    | Wheel and crawler-mounted vehicle            |
+---------------------------+--------------------------+----------------------------------------------+
| `Tank Bot`_               | *n/a*                    | Crawler-mounted military vehicle             |
+---------------------------+--------------------------+----------------------------------------------+
| `Elephant`_               | *n/a*                    | Walking and roaring elephant                 |
+---------------------------+--------------------------+----------------------------------------------+
| `Spinner Factory`_        | *n/a*                    | Complex assembly line machine                |
+---------------------------+--------------------------+----------------------------------------------+
| **> Popular (awesome) robots by other authors**                                                     |
+---------------------------+--------------------------+----------------------------------------------+
| *n/a*                     | `Explor3r`_              | Self-driving exploring robot                 |
+---------------------------+--------------------------+----------------------------------------------+
| *n/a*                     | `EV3D4`_                 | Remote-controlled Star Wars R2-D2 clone      |
+---------------------------+--------------------------+----------------------------------------------+
| `MindCub3r`_              | `MindCub3r (ev3dev)`_    | Solves the Rubik's cube                      |
+---------------------------+--------------------------+----------------------------------------------+
| *n/a*                     | `EV3 Tracked Explor3r`_  | Autonomous crawler-mounted tank vehicle      |
+---------------------------+--------------------------+----------------------------------------------+
| `EV3 Dancing robot`_      | *n/a*                    | The sweetest LEGO disco dancer ever!         |
+---------------------------+--------------------------+----------------------------------------------+
| `Wall-EV3`_ (non-free)    | *n/a*                    | Disney's cute `WALL-E robot`_ built with EV3 |
+---------------------------+--------------------------+----------------------------------------------+
| `Chip & Dale`_ (non-free) | *n/a*                    | Two mecha twin robots that walk and turn     |
+---------------------------+--------------------------+----------------------------------------------+
| `NXTurtle`_ (non-free)    | *n/a*                    | An awesome turtle (see also: `EV3 Turtle`_)  |
+---------------------------+--------------------------+----------------------------------------------+
| `EV3 Desk Guardian`_      | (easy to write yourself) | A bodyguard shooting robot for your desk     |
+---------------------------+--------------------------+----------------------------------------------+
| `Clev3r Car`_             | *n/a*                    | RC or autonomous car that avoids obstacles   |
+---------------------------+--------------------------+----------------------------------------------+
| `Cleaning Robot`_         | *n/a*                    | Clean your room with this Roomba clone!      |
+---------------------------+--------------------------+----------------------------------------------+
| *n/a*                     | `Sound & LEDs`_          | Demos to produce sound and activate LEDs     |
+---------------------------+--------------------------+----------------------------------------------+
| **> Other resources**                                                                               |
+---------------------------+--------------------------+----------------------------------------------+
| `Walking robots`_                                    | just videos of maker creations               |
+---------------------------+--------------------------+----------------------------------------------+
| More `EV3 Maker and Coding Activities`_              | official LEGO downloads                      |
+---------------------------+--------------------------+----------------------------------------------+

.. _LEGO MINDSTORMS EV3 Software: https://www.lego.com/en-us/mindstorms/downloads/download-software
.. _ev3dev firmware: http://www.ev3dev.org
.. _Open Roberta Lab: https://lab.open-roberta.org/
.. _setup instructions: https://github.com/OpenRoberta/robertalab-ev3dev#intro
.. _Scratch: https://scratch.mit.edu/
.. _Scratch extensions: http://kaspesla.github.io/ev3_scratch/
.. _Home Edition robots: http://www.lego.com/en-us/mindstorms/build-a-robot
.. _Track3r (LEGO): https://www.lego.com/en-us/mindstorms/build-a-robot/track3r
.. _Track3r (ev3dev): https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/TRACK3R
.. _Spik3r (LEGO): https://www.lego.com/en-us/mindstorms/build-a-robot/spik3r
.. _R3ptar (LEGO): https://www.lego.com/en-us/mindstorms/build-a-robot/r3ptar
.. _R3ptar (ev3dev): https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/R3PTAR
.. _Gripp3r (LEGO): https://www.lego.com/en-us/mindstorms/build-a-robot/gripp3r
.. _Gripp3r (ev3dev): https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/GRIPP3R
.. _Ev3rstorm (LEGO): https://www.lego.com/en-us/mindstorms/build-a-robot/ev3rstorm
.. _Ev3rstorm (ev3dev): https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/EV3RSTORM
.. _Education Edition Core Set robots: http://robotsquare.com/2013/10/01/education-ev3-45544-instruction/
.. _Educator Vehicle: http://robotsquare.com/wp-content/uploads/2013/10/45544_educator.pdf
.. _Educator: https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/EDUCATOR
.. _Sorter: http://robotsquare.com/2014/08/22/brick-sorter-sort-lego-bricks-by-color-and-size/
.. _Gyro Boy: http://robotsquare.com/2014/07/01/tutorial-ev3-self-balancing-robot/
.. _Balanc3r: https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/BALANC3R
.. _Puppy: http://robotsquare.com/wp-content/uploads/2013/10/45544_puppy.pdf
.. _behaves like a dog: https://www.youtube.com/watch?v=HJ3XLFsd4zI
.. _Robot Arm H25: http://robotsquare.com/wp-content/uploads/2013/10/45544_robotarmh25.pdf
.. _Education Edition Expansion Set robots: http://robotsquare.com/2013/10/01/lego-mindstorms-ev3-education-expansion-set-45560-instructions/
.. _Znap: http://robotsquare.com/wp-content/uploads/2013/10/45544_45560_znap.pdf
.. _Remote Control: http://robotsquare.com/wp-content/uploads/2013/10/45544_45560_remotecontrol.pdf
.. _Stair Climber: http://robotsquare.com/wp-content/uploads/2013/10/45544_45560_stairclimber.pdf
.. _Tank Bot: http://robotsquare.com/wp-content/uploads/2013/10/45544_45560_tankbot.pdf
.. _Elephant: http://robotsquare.com/wp-content/uploads/2013/10/45544_45560_elephant.pdf
.. _Spinner Factory: http://robotsquare.com/wp-content/uploads/2013/10/2x45544_45560_spinnerfactory_part_3.pdf
.. _Explor3r: https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/EXPLOR3R
.. _EV3D4: https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/EV3D4
.. _MindCub3r: http://mindcuber.com/mindcub3r/mindcub3r.html
.. _MindCub3r (ev3dev): https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/MINDCUB3R
.. _EV3 Tracked Explor3r: https://www.smallrobots.it/latest-pictures-of-ev3-tracked-explor3r/
.. _EV3 Dancing robot: http://teachkidsengineering.com/lego-mindstorms-dancing-robot/
.. _Wall-EV3: http://robotics.benedettelli.com/lego-wall-e/
.. _WALL-E robot: https://ideas.lego.com/projects/52042/updates
.. _Chip & Dale: http://robotics.benedettelli.com/ev3-mecha-page/
.. _NXTurtle: http://robotics.benedettelli.com/nxt-turtle-2-0/
.. _EV3 Turtle: https://www.youtube.com/watch?v=73jwQ8W_6bM
.. _EV3 Desk Guardian: http://robotics.benedettelli.com/ev3-desk-guardian/
.. _Clev3r Car: http://buildinst.cz/en/catalog/detail/31
.. _Cleaning Robot: https://www.youtube.com/watch?v=Np37j8akW4A
.. _Sound & LEDs: https://github.com/ev3dev/ev3dev-lang-python-demo/tree/master/robots/misc
.. _Walking robots: http://www.legoengineering.com/walking-robots/
.. _EV3 Maker and Coding Activities: https://education.lego.com/en-us/downloads/mindstorms-ev3

Your Contribution
-----------------

If you find a typo, an error, a critical mistake or feel there's some enhancement
needed please feel free to `open an issue`_, or even better clone the repository,
apply your changes, and `place a pull request`_.  Your contribution is welcome!

Please run ``flake8`` over the Python code to make sure it follows PEP8.
A line length of 100 is okay (``flake8 --max-line-length=100``).

Step by Step
~~~~~~~~~~~~

If you make changes to the raw data, e.g. ``raw-data/Brickset-inventory-*.csv``,
in a pull request please also regenerate the combined list and update the Calc
spread sheet as follows::

   $ cd raw-data/
   $ python3 ../lego-mindstorms-pieces.py parse Brickset-* > "Lego Mindstorms EV3 combined list.csv"

Then open ``Lego-Mindstorms-Editions-Comparison.ods`` and copy the contents of
the regenerated ``Lego Mindstorms EV3 combined list.csv`` from a text editor
into the spread sheet as follows:

#. Highlight the first 7 columns and press the ``Del`` key to clear the cells.
#. Place the cursor onto the first left upper cell and press ``Ctrl`` + ``v``.
#. The "Text Import" dialog pops up.  Choose "Unicode" and "Tab" separation.


.. _open an issue: https://github.com/bittner/lego-mindstorms-ev3-comparison/issues
.. _place a pull request: https://github.com/bittner/lego-mindstorms-ev3-comparison/pulls
