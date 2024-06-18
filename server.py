#!/usr/bin/env python3

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import json
import os
import datetime
import random

def print_in_color(text: str, color: str, end="\n"):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    if color == "green":
        text = OKGREEN + text + ENDC
    elif color == "cyan":
        text = OKCYAN + text + ENDC
    elif color == "blue":
        text = OKBLUE + text + ENDC
    elif color == "brown":
        text = WARNING + text + ENDC

    print(text, end=end)


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):

        print_in_color(f"{self.headers}", end="", color="green")
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        if self.headers["Content-Length"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode('utf-8')
        else:
            post_data = b""

        print_in_color(f"{self.headers}", color="green", end="")

        if "application/json" in self.headers["Content-Type"]:
            try:
                post_data = json.dumps(json.loads(post_data), indent=2)
            except Exception:
                pass

        print_in_color(f"{post_data}\n", color="cyan")

        current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        random_number = random.randint(1, 1000)
        file_name = f"requests/post_data_{current_date}_{random_number}.json"

        with open(file_name, "w") as file:
            file.write(post_data)
        

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

    def log_message(self, format, *args):
        print_in_color(
            "%s - - [%s] %s\n"
            % (self.address_string(), self.log_date_time_string(), format % args),
            color="brown",
        )


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print_in_color(f"Starting httpd {port}...\n", color="green")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping httpd...\n")


if __name__ == "__main__":
    from sys import argv

    if not os.path.exists("requests"):
        os.makedirs("requests")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
