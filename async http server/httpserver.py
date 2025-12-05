import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] Connected: {addr}")

    try:
        while True:
            header_bytes = await reader.readuntil(b'\r\n\r\n')
            headers = header_bytes.decode()

            lines = headers.split("\r\n")
            request_line = lines[0]
            headers_dict = {}
            for line in lines[1:]:
                if line:
                    key, value = line.split(":", 1)
                    headers_dict[key.strip()] = value.strip()

            content_length = int(headers_dict.get("Content-Length", 0))
            body = b""
            if content_length > 0:
                body = await reader.readexactly(content_length)
                        
            response_body = "Hello from async http setver"
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
                f"{response_body}"
            )

            writer.write(response.encode())
            await writer.drain()

            if headers_dict.get("Connection", "").lower() != "keep-alive":
                break

    except asyncio.IncompleteReadError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 5000)
    print("[*] Async HTTP server running on port 5000")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())




            
