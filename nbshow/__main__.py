from nbshow import create_app
import click


@click.command(name='nbshow')
@click.argument('path', default='.')
@click.option('--port', type=int)
@click.option('--host')
def main(path, host, port):
    app = create_app(path)
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
