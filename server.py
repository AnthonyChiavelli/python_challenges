from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import os
import pickle
from time import strftime
import urlparse
import cgi


class RequestHandler(BaseHTTPRequestHandler):
    """
    A request handler for a simple server designed to compute the
    product and sum reductions of the provided list parameter. Uses
    a flat file and pickle module to maintain a "database" of requests
    so that history can be queried
    """

    def do_GET(self):
        """
        Handle GET requests
        """

        # Extract URL parameters
        params = urlparse.parse_qs(str(self.path).lstrip("/?"))

        # If this is calculation endpoint
        if "numbers" in params:

            # Convert params to list of numbers
            numbers = params['numbers'][0].split(",")

            # Perform calculations and reply with JSON result
            self._reply_with_calculation(numbers)

        # History endpoint
        elif "history" in params:

            # Load history if present
            request_history = []
            if os.path.isfile("server_db"):
                request_history = pickle.load(open("server_db"))

            # Convert param to number n
            history_cutoff = min(max(int(params['history'][0]), len(request_history)),
                                 len(request_history))

            # Get last n entries in history
            last_n_entries = request_history[len(request_history) - history_cutoff::][::-1]

            # Reply with history
            self._reply_with_history(last_n_entries)

    def do_POST(self):
        """
        Handle POST requests
        """

        # Extract data from request body
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST',
                                         'CONTENT_TYPE': self.headers['Content-Type'], })
        num_string = ",".join([form[key].value for key in form.keys()])

        # Perform calculations and return results
        self._reply_with_calculation(num_string.split(","))

    def _reply_with_calculation(self, numbers):
        """
        Perform the math and return the results as a JSON object
        """

        # Perform math
        response_dict = {"sum": reduce(lambda x, y: int(x) + int(y), numbers),
                         "product": reduce(lambda x, y: int(x) * int(y), numbers)}

        # Convert to JSON and send back
        json_response = json.dumps(response_dict)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Store this query in our history
        if os.path.isfile("server_db"):
            request_history = pickle.load(open("server_db"))
        else:
            request_history = []

        request_history.append({"ip": self.client_address[0],
                                "timestamp": strftime("%Y-%m-%d %H:%M:%S"),
                                "values": numbers,
                                "sum": response_dict["sum"],
                                "product": response_dict["product"]})
        pickle.dump(request_history, open("server_db", "w+"))

        self.wfile.write(json_response)

    def _reply_with_history(self, last_n_entries):
        """
        Reply with history, constrained by range specified in request
        """
        # Convert to JSON and send back
        response = json.dumps(list(last_n_entries))
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response)

if __name__ == "__main__":
    try:
        # Run the server
        server = HTTPServer(('', 8282), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        # Ensure that socket is closed when server terminates.
        server.socket.close()