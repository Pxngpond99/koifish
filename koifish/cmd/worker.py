from koifish.api.worker import create_server


def main():
    server = create_server()
    server.run()
