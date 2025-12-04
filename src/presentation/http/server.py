import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(__file__).rsplit("/src", 1)[0])

from src.bootstrap import (
    create_dependency_container,
    get_database_connection,
    initialize_database,
)

db_connection = None

reservation_controller = None
office_repository = None


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/":
            self.send_json_response(
                200, {"status": "ok", "message": "Office Reservation API", "swagger": "/docs"}
            )
        elif path in {"/docs", "/docs/"}:
            self.serve_swagger_ui()
        elif path == "/openapi.json":
            self.serve_openapi_spec()
        elif path == "/api/offices":
            self.handle_list_offices()
        else:
            self.send_json_response(404, {"error": "Not found"})

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json_response(400, {"error": "Invalid JSON"})
            return

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/api/offices/availability":
            self.handle_check_availability(data)
        elif path == "/api/reservations":
            self.handle_create_reservation(data)
        elif path == "/api/offices/info":
            self.handle_get_office_info(data)
        else:
            self.send_json_response(404, {"error": "Not found"})

    def handle_list_offices(self) -> None:
        try:
            offices = office_repository.find_all()  # type: ignore
            response = {
                "success": True,
                "offices": [
                    {
                        "office_id": office.office_id,
                        "name": office.name,
                        "capacity": office.capacity,
                        "description": office.description,
                    }
                    for office in offices
                ],
            }
            self.send_json_response(200, response)
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})

    def handle_check_availability(self, data: dict[str, Any]) -> None:
        required_fields = ["office_id", "date", "start_time", "end_time"]
        if not all(field in data for field in required_fields):
            self.send_json_response(400, {"error": "Missing required fields"})
            return

        result = reservation_controller.check_office_availability(  # type: ignore
            office_id=data["office_id"],
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

        status_code = 200 if result.get("success") else 404
        self.send_json_response(status_code, result)

    def handle_create_reservation(self, data: dict[str, Any]) -> None:
        required_fields = ["office_id", "name", "email", "phone", "date", "start_time", "end_time"]
        if not all(field in data for field in required_fields):
            self.send_json_response(400, {"error": "Missing required fields"})
            return

        result = reservation_controller.book_office(  # type: ignore
            office_id=data["office_id"],
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )

        if result.get("success"):
            self.send_json_response(201, result)
        else:
            error_msg = result.get("error", "")
            if "not found" in error_msg.lower():
                status_code = 404
            elif "conflict" in error_msg.lower():
                status_code = 409
            else:
                status_code = 400
            self.send_json_response(status_code, result)

    def handle_get_office_info(self, data: dict[str, Any]) -> None:
        required_fields = ["office_id", "date", "start_time", "end_time"]
        if not all(field in data for field in required_fields):
            self.send_json_response(400, {"error": "Missing required fields"})
            return

        result = reservation_controller.get_office_info(  # type: ignore
            office_id=data["office_id"],
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

        status_code = 200 if result.get("success") else 404
        self.send_json_response(status_code, result)

    def serve_swagger_ui(self) -> None:
        html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Office Reservation API - Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "StandaloneLayout"
            });
        };
    </script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_openapi_spec(self) -> None:

        
        spec_path = Path(__file__).parent / "openapi.json"
        with spec_path.open(encoding="utf-8") as f:
            spec = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(spec.encode("utf-8"))

    def send_json_response(self, status_code: int, data: Any) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, _fmt: str, *_args: Any) -> None:
        return


def run_server(port: int = 8000) -> None:
    global db_connection, reservation_controller, office_repository  # noqa: PLW0603

    db_connection = get_database_connection()
    initialize_database(db_connection)
    reservation_controller, office_repository = create_dependency_container(db_connection)

    server_address = ("", port)
    httpd = HTTPServer(server_address, APIHandler)

    print("Database initialized")
    print("Office Reservation API started")
    print(f"Server running on http://localhost:{port}")
    print(f"Swagger documentation: http://localhost:{port}/docs")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
