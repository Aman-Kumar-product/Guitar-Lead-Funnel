try:
    from backend.main import app
except Exception as e:
    import traceback
    error_traceback = traceback.format_exc()
    
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'text/plain'),
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': f"Import Failed:\n\n{error_traceback}".encode('utf-8')
        })
