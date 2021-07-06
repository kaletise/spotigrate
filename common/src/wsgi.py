import getopt
import sys


def usage():
    print(
        'Usage: wsgi.py [-d] -h <host> -p <port>\n'
        '-d: debug mode\n'
        '-h: webserver host (default: 127.0.0.1)\n'
        '-p: webserver port (default: 5000)'
    )


if __name__ == '__main__':
    run_args = {'debug': False, 'host': '127.0.0.1', 'port': 5000}
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'dh:p:', ['debug', 'host=', 'port=']
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-d', '--debug'):
            run_args['debug'] = True
        elif opt in ('-h', '--host'):
            run_args['host'] = arg
        elif opt in ('-p', '--port'):
            run_args['port'] = arg
        else:
            usage()
            sys.exit(2)
    from main import application
    if application:
        application.master.logger.warning(
            'This application is about to be served in development mode. '
            'Please make sure to deploy it properly in production'
        )
        application.run(**run_args)
else:
    from main import application
