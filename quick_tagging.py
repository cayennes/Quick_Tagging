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

# Bury by adding a True bury element:
#'l': {'tags': 'needs_elaboration', bury: True},

} # end quick_tags

# END CONFIGURATION OPTIONS

from aqt import mw
from aqt.utils import getTag, tooltip
from aqt.reviewer import Reviewer

# add space separated tags to a note

def addTags(note, tagString):
    # add tags to card
    tagList = mw.col.tags.split(tagString)
    for tag in tagList:
        note.addTag(tag)
    note.flush()

# prompt for tags and add the results to a note

def promptAndAddTags(note):
    # prompt for new tags
    prompt = _("Enter tags to add:")
    (tagString, r) = getTag(mw, mw.col, prompt)
    # don't do anything if we didn't get anything
    if not r:
        return
    # otherwise, add the given tags:
    addTags(note, tagString)
    tooltip('Added tag(s) "%s"' % tagString)

# replace _keyHandler in reviewer.py to add a keybinding

def newKeyHandler(self, evt):
    key = unicode(evt.text())
    note = mw.reviewer.card.note()
    if key == tag_shortcut:
        mw.checkpoint(_("Add Tags"))
        promptAndAddTags(note)
    elif key in quick_tags:
        if 'bury' in quick_tags[key] and quick_tags[key]['bury']:
            mw.checkpoint("Add Tags and Bury")
            addTags(note, quick_tags[key]['tags'])
            mw.col.sched.buryNote(note.id)
            mw.reset()
            tooltip('Added tag(s) "%s" and buried note' 
                    % quick_tags[key]['tags'])
        else:
            mw.checkpoint(_("Add Tags"))
            addTags(note, quick_tags[key]['tags'])
            tooltip('Added tag(s) "%s"' % quick_tags[key]['tags'])
    else:
        origKeyHandler(self, evt)

origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler

