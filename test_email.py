from email.message import EmailMessage
msg = EmailMessage()
msg.set_content('text')
msg.add_alternative('<html/>', subtype='html')
try:
    msg.get_payload()[1].add_related(b'123', maintype='image', subtype='png', cid='<logo>')
    print('SUCCESS')
except Exception as e:
    print('ERROR:', e)
