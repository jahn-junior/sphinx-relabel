# This file is part of sphinx-relabel.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 3, as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY
# QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from sphinx.application import Sphinx
from docutils.nodes import document


def relabel(app: Sphinx, doctree: document) -> None:
    if not app.config.label_redirects:
        return

    label_mapping: dict[str, str] = {}
    if isinstance(app.config.label_redirects, str):
        # open file and read as dict
        label_mapping = {}
    elif not all(
        isinstance(k, str) and isinstance(v, str)
        for k, v in app.config.label_redirects.items()
    ):
        # error out
        print("why i oughtta")
    else:
        label_mapping = app.config.label_redirects

    for old_label in list(label_mapping.keys()):
        target_doc, anchor, link_text = app.env.domaindata["std"]["labels"][
            label_mapping[old_label]
        ]

        app.env.domaindata["std"]["labels"][old_label] = (
            target_doc,
            anchor,
            link_text,
        )
