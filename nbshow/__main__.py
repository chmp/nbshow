import os
import itertools as it

import click
import nbconvert
import nbformat

from flask import Flask, redirect, render_template, Markup


@click.command(name='nbshow')
@click.argument('path', default='.')
def main(path):
    app = create_app(path)

    app.run()


def create_app(root):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect('/tree')

    @app.route('/tree')
    @app.route('/tree/')
    @app.route('/tree/<path:p>')
    def tree(p=''):
        full_path = os.path.join(root, p)
        if not is_subpath(root, full_path):
            raise RuntimeError('file not found')

        children = [
            {
                'name': c,
                'path': os.path.join(p, c),
                'full_path': c_full_path,
                'isdir': os.path.isdir(c_full_path),
                'isnb': os.path.isfile(c_full_path) and c_full_path.endswith('.ipynb'),
            }
            for c in os.listdir(full_path)
            for c_full_path in [os.path.join(full_path, c)]
            if not c.startswith('.')
        ]

        return render_template(
            'tree.html',
            path=p,
            children=children,
            breadcrumbs=get_breadcrumbs(p),
        )

    @app.route('/resource/<p>')
    def resource(p):
        paths = {
            'ipython.min.css': 'static/style/ipython.min.css',
            'style.min.css': 'static/style/style.min.css',
        }

        import notebook
        p = os.path.join(os.path.dirname(notebook.__file__), paths[p])
        with open(p, 'r') as fobj:
            return fobj.read()

    @app.route('/show/<path:p>')
    def show(p):
        return render_template(
            'show.html',
            path=p.strip(),
            breadcrumbs=get_breadcrumbs(p),
        )

    @app.route('/render/<path:p>')
    def render(p):
        full_path = os.path.join(root, p)
        if not is_subpath(root, full_path):
            raise RuntimeError('file not found')

        with open(full_path, 'r') as fobj:
            nb = nbformat.read(fobj, as_version=4)

        html_exporter = nbconvert.HTMLExporter()
        html_exporter.template_file = 'basic'
        body, _ = html_exporter.from_notebook_node(nb)

        return body

    return app


def is_subpath(parent, child):
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)

    if child == parent:
        return True

    if not parent.endswith(os.path.sep):
        parent = parent + os.path.sep

    return child.startswith(parent)


def get_breadcrumbs(p):
    path_parts = _full_split(p)

    breadcrumbs = [{'label': Markup('&#8962;'), 'url': '/tree'}]
    breadcrumbs.extend(
        {
            'label': label,
            'url': ('/tree/' + path) if not path.endswith('.ipynb') else ('/show/' + path),
        }
        for label, path in zip(
            path_parts,
            list(it.accumulate(path_parts, os.path.join))
        )
    )

    return breadcrumbs


def _full_split(p):
    result = []
    head = p

    while head:
        if os.path.sep not in head:
            return [head] + result

        head, tail = os.path.split(head)
        result = [tail] + result

    return result

if __name__ == "__main__":
    main()
