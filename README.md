<img src="assets/logo.png" alt="reLabel logo" style="height: 256px; display: block">

reLabel is a tool for redirecting labels in your Sphinx documentation.

In documentation, we go to great lengths to redirect pages as they're moved, but we
don't show the same care with Sphinx labels. If external documentation links to your
project with Intersphinx, then removing labels will break references to them.

With reLabel, you can redirect removed labels to any existing label in your docs,
preventing any surprise Intersphinx breakages.

## Usage

Map removed labels to existing labels with the `label_redirects` option in your
`conf.py` file:

```python
label_redirects = {
    "old-label": "new-label"
}
```

Alternatively, list the label redirects in a separate file, formatted as valid JSON:

```python
label_redirects = "labels.json"
```

## Project setup

reLabel is published on PyPI and can be installed with:

```bash
pip install sphinx-relabel
```

After adding reLabel to your Python project, update your Sphinx's conf.py file to
include reLabel as one of its extensions:

```python
extensions = [
    "sphinx_relabel"
]
```

## Community and support

You can report any issues or bugs on the project's [GitHub
repository](https://github.com/jahn-junior/sphinx-relabel).

If you're interested in contributing to reLabel, start with the [contribution
guide](CONTRIBUTING.md).

## License and copyright

reLabel is released under the [GPL-3.0 license](LICENSE).
