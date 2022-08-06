import os
import json
import uuid
from typing import Tuple, Callable, Any
from wsgiref.simple_server import make_server

directories = {"data": ["foo"]}

# This is a rather naive function for figuring out the
# repository and objectID from the URL.
def url_match(url: str) -> Tuple[str, str]:
    fragments = url.split("/", -1)
    directory = fragments[1]
    repository = fragments[2]
    object_id = ""

    if len(fragments) > 3:
        object_id = fragments[3]
    return directory, repository, object_id


class DataStorageServer:
    def __init__(self) -> None:
        self.storage = {}

    def __call__(
        self, environ: dict[str, any], start_response: Callable[..., Any]
    ) -> bytes:
        """
        The environ parameter is a dictionary containing some useful
        HTTP request information such as: REQUEST_METHOD, CONTENT_LENGTH,
        PATH_INFO, CONTENT_TYPE, etc.
        For the full list of attributes refer to wsgi definitions:
        https://wsgi.readthedocs.io/en/latest/definitions.html
        """
        # Extract relevant url and object data
        directory, repository, object_id = url_match(environ.get("PATH_INFO", ""))

        # Check if the url is true & validate database; otherwise yield 400
        true_url = False
        if directory in directories:
            if repository in directories.get(directory):
                true_url = True

                # Validate database format
                if directory not in self.storage:
                    self.storage[directory] = {repository: {}}
                if repository not in self.storage[directory]:
                    self.storage[directory] = {repository: {}}

        if true_url:

            # This method will GET (download) an object if the object exists
            if environ["REQUEST_METHOD"] == "GET":
                resp = self.storage.get(directory).get(repository).get(object_id)
                if resp:
                    body = bytes(resp["content"], "utf-8")
                    size = resp["size"]
                    status = "200 OK"
                    response_headers = [("Content-Type", "text/plain")]
                else:
                    body = b""
                    status = "404 NOT FOUND"
                    response_headers = [("Content-Type", "text/plain")]

            # This method will PUT (upload) an object to the designated repo
            elif environ["REQUEST_METHOD"] == "PUT":
                # Collect contents and assign object-id (oid)
                csize = environ["CONTENT_LENGTH"]
                ctype = environ["CONTENT_TYPE"]
                byte_content = environ["wsgi.input"].read()
                str_content = byte_content.decode("utf-8")

                content_exists = False
                # Check if content exists in repository
                # use metadata to search first and limit large content comparisons
                for key, value in self.storage.get(directory).get(repository).items():
                    if csize and ctype:
                        if value["size"] == csize and value["type"] == ctype:
                            if value.content == str_content:
                                content_exists = True
                                oid = key
                    else:
                        if value.content == str_content:
                            content_exists = True
                            oid = key

                # Write to Storage
                if not content_exists:
                    oid = str(uuid.uuid4())
                    self.storage[directory][repository][oid] = {
                        "content": str_content,
                        "size": csize,
                        "type": ctype,
                    }
                    status = "201 CREATED"
                else:
                    status = "202 ACCEPTED"

                message = {"oid": oid, "size": int(csize)}
                body = bytes(json.dumps(message), "utf-8")
                response_headers = [("Content-Type", "text/plain")]

            # This method will DELETE an existing objects from the designated repo
            elif environ["REQUEST_METHOD"] == "DELETE":
                try:
                    self.storage.get(directory).get(repository).pop(object_id)
                    status = "200 OK"
                except KeyError:
                    status = "404 NOT FOUND"
                body = b""
                response_headers = [("Content-Type", "text/plain")]

            # Return 404 if the Request does not meet requirements
            else:
                body = b""
                status = "404 BAD REQUEST"
                response_headers = [("Content-Type", "text/plain")]

        start_response(status, response_headers)
        yield body


if __name__ == "__main__":
    app = DataStorageServer()
    port = os.environ.get("PORT", 8282)
    with make_server("", port, app) as httpd:
        print(f"Listening on port {port}...")
        httpd.serve_forever()
