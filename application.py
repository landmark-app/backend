import argparse

from src.run import application


if __name__ == "__main__":
    parser = argparse.ArgumentParser("""
    Creates a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """)
    msg = 'Hostname of Flask app [{}]'.format("0.0.0.0")
    parser.add_argument("-H", "--host",
                        help=msg,
                        default="0.0.0.0")
    msg = 'Port for Flask app [{}]'.format("80")
    parser.add_argument("-P", "--port",
                        help=msg,
                        default="80")
    parser.add_argument("-d", "--debug",
                        action="store_true", dest="debug")

    args = parser.parse_args()

    application.run(
        debug=args.debug,
        host=args.host,
        port=int(args.port)
    )
