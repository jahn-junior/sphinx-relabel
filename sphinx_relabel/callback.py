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

"""Contains the core callback function of reLabel."""

import json
from pathlib import Path
from typing import cast

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import ConfigError
from sphinx.util.nodes import make_refnode


def relabel(app: Sphinx, doctree: nodes.document) -> None:  # noqa: ARG001
    """Process and create redirects after the doctree is read."""
    if not app.config.label_redirects:
        return

    if isinstance(app.config.label_redirects, str):
        # open file and read as dict
        with Path.open(app.confdir / app.config.label_redirects) as redirects_file:
            app.config.label_redirects = json.load(redirects_file)
    elif not all(  # if there are non-string entries
        isinstance(k, str) and isinstance(v, str)
        for k, v in app.config.label_redirects.items()
    ):
        raise TypeError("All source and destination labels must be strings.")

    for old_label in app.config.label_redirects:
        if (
            app.config.label_redirects[old_label]
            not in app.env.domaindata["std"]["labels"]
        ):
            raise ConfigError(
                f"Label '{app.config.label_redirects[old_label]}' not found in the standard domain."
            )

        target_doc, anchor, link_text = app.env.domaindata["std"]["labels"][
            app.config.label_redirects[old_label]
        ]

        app.env.domaindata["std"]["labels"][old_label] = (
            target_doc,
            anchor,
            link_text,
        )


def handle_redirected_labels(
    app: Sphinx, env: BuildEnvironment, node: nodes.reference, contnode: nodes.Node
) -> nodes.reference | None:
    """Process `pending_xref` nodes that point to redirected labels in local docs."""
    redirects = getattr(app.config, "label_redirects", {})

    old_target = cast(str, node.get("reftarget"))
    if old_target in redirects:
        node["reftarget"] = redirects[old_target]
        return make_refnode(
            app.builder,
            env.docname,
            redirects[old_target],
            contnode.astext(),
            contnode,
            redirects[old_target],
        )

    return None
