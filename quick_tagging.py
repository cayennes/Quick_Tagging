# Quick Tagging is an anki2 addon for quickly adding tags while reviewing
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

quick_tags = {

# Add lines here to create shortcuts that add specified tags

# Examples (remove the leading #):

# Keybinding to add a named tag:
#'j': {'tags': 'hard'},

# Add multiple tags by seperating them with spaces:
#'k': {'tags': 'hard marked'},

} # end quick_tags

# END CONFIGURATION OPTIONS

from aqt import mw
from aqt.utils import getTag
from aqt.reviewer import Reviewer

# add space separated tags to the current card

def addTags(tagString):
    # enable undo
    mw.checkpoint(_("Add Tags"))
    # add tags to card
    tagList = mw.col.tags.split(tagString)
    for tag in tagList:
        mw.reviewer.card.note().addTag(tag)
    mw.reviewer.card.note().flush()

# prompt for tags and add the results

def promptAndAddTags():
    # prompt for new tags
    prompt = _("Enter tags to add:")
    (tagString, r) = getTag(mw, mw.col, prompt)
    # don't do anything if we didn't get anything
    if not r:
        return
    # otherwise, add the given tags:
    addTags(tagsString)

# replace _keyHandler in reviewer.py to add a keybinding

def newKeyHandler(self, evt):
    key = unicode(evt.text())
    if key == tag_shortcut:
        promptAndAddTags()
    elif key in quick_tags:
        addTags(quick_tags[key]['tags'])
    else:
        origKeyHandler(self, evt)

origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler

