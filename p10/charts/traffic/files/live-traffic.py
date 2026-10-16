import http.cookiejar
import json
import os
from pathlib import Path
import secrets
import threading
import time
import urllib.request

BASE = os.getenv("API_BASE_URL", "http://api-gateway:8080")
shared = {"post": None}
lock = threading.Lock()


def log(level, message, **attributes):
    print(
        json.dumps({"level": level, "service": "p10-traffic", "message": message, **attributes}), flush=True
    )


class Client:
    def __init__(self):
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )
        self.last_login = 0

    def call(self, path, body=None, method="POST", trace_id=None):
        headers = {"content-type": "application/json"}
        if trace_id:
            headers["traceparent"] = f"00-{trace_id}-{secrets.token_hex(8)}-01"
        request = urllib.request.Request(
            BASE + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers=headers,
            method=method,
        )
        with self.opener.open(request, timeout=8) as response:
            data = json.load(response)
        if data.get("errors"):
            raise RuntimeError("El servicio devolvió un error al procesar la solicitud.")
        return data

    def login(self):
        if time.monotonic() - self.last_login > 600:
            self.call(
                "/api/auth/login",
                {"email": os.environ["ADMIN_EMAIL"], "password": os.environ["ADMIN_PASSWORD"]},
            )
            self.last_login = time.monotonic()


def reader():
    client = Client()
    while True:
        trace_id = secrets.token_hex(16)
        try:
            client.login()
            with lock:
                post = shared["post"]
            if post:
                client.call("/api/posts/graphql", {"query": "{posts{id}}"}, trace_id=trace_id)
                client.call(
                    "/api/comments/graphql",
                    {"query": "query($id:ID!){comments(postId:$id){id}}", "variables": {"id": post}},
                    trace_id=trace_id,
                )
                client.call(f"/api/likes/{post}", method="GET", trace_id=trace_id)
        except Exception as error:
            log(
                "ERROR",
                "No se pudieron consultar los datos de prueba.",
                trace_id=trace_id,
                error_type=type(error).__name__,
            )
        time.sleep(0.5)


for _ in range(3):
    threading.Thread(target=reader, daemon=True).start()
writer = Client()
last_post, last_comment = 0, 0
while True:
    try:
        writer.login()
        now = time.monotonic()
        if now - last_post > 1200:
            data = writer.call(
                "/api/posts/graphql",
                {
                    "query": "mutation($input:CreatePostInput!){createPost(input:$input){id}}",
                    "variables": {
                        "input": {
                            "title": "P10 tráfico de revisión",
                            "content": "Publicación de prueba creada mediante la API autenticada.",
                        }
                    },
                },
            )
            with lock:
                shared["post"] = data["data"]["createPost"]["id"]
            last_post = now
            time.sleep(3)
            Path("/tmp/ready").touch()
        if now - last_comment > 60:
            with lock:
                post = shared["post"]
            writer.call(
                "/api/comments/graphql",
                {
                    "query": "mutation($input:AddCommentInput!){addComment(input:$input){id}}",
                    "variables": {"input": {"postId": post, "content": "Comentario de prueba P10"}},
                },
            )
            writer.call(f"/api/likes/{post}", method="PUT")
            last_comment = now
            log("INFO", "Se probaron la creación de comentarios y el cambio de Me gusta.")
        Path("/tmp/alive").touch()
    except Exception as error:
        log("ERROR", "No se pudieron guardar los datos de prueba.", error_type=type(error).__name__)
    time.sleep(5)
