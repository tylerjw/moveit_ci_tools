colcon_list_packages_changed_since
==================

List packages that have changed files since point in git history.


How to run the check from the command line?
-------------------------------------------

*Prerequisites*: ``colcon`` and ``git`` should already be installed.

.. code:: sh

    colcon_list_packages_changed_since <path> <point>

``path`` must be the root directory of a git repo containing ros packages.

``point`` must be a git branch, tag, or commit
