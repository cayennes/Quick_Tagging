# Quick Tagging is an anki2 addon for adding tags while reviewing by
# hitting a keyboard shortcut ('t' by default.)
# Copyright 2012 Cayenne Boyer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# CONFIGURATION OPTIONS

# Change this to change what keybinding opens the add tags dialog

tag_shortcut = 't'

# END CONFIGURATION OPTIONS

from aqt import mw
from aqt.utils import getTag
from aqt.reviewer import Reviewer

# function that allows tag adding

def promptAndAddTags():
    # prompt for new tags
    prompt = _("Enter tags to add:")
    (tagString, r) = getTag(mw, mw.col, prompt)
    # don't do anything if we didn't get anything
    if not r:
        return
    # otherwise, continue:
    # enable undo
    mw.checkpoint(_("Add Tags"))
    # add tags to card
    tagList = mw.col.tags.split(tagString)
    for tag in tagList:
        mw.reviewer.card.note().addTag(tag)
    mw.reviewer.card.note().flush()

# replace _keyHandler in reviewer.py to add a keybinding

def newKeyHandler(self, evt):
    key = unicode(evt.text())
    if key == tag_shortcut:
        promptAndAddTags()
    else:
        origKeyHandler(self, evt)

origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler

