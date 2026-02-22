import os
import secrets
import io
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from backend import mail, supabase

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    img_byte_arr = io.BytesIO()
    
    format_mapping = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG', '.gif': 'GIF'}
    img_format = format_mapping.get(f_ext.lower(), 'PNG')
    if i.mode in ("RGBA", "P") and img_format == 'JPEG':
        i = i.convert("RGB")
        
    i.save(img_byte_arr, format=img_format)
    img_bytes = img_byte_arr.getvalue()
    
    content_type = 'image/jpeg' if img_format == 'JPEG' else f'image/{img_format.lower()}'
    
    import requests
    
    url = f"{current_app.config['SUPABASE_URL']}/storage/v1/object/profile_pics/{picture_fn}"
    headers = {
        "Authorization": f"Bearer {current_app.config['SUPABASE_KEY']}",
        "Content-Type": content_type
    }
    
    response = requests.post(url, headers=headers, data=img_bytes)
    
    if not response.ok:
        print(f"Supabase upload failed: {response.text}")
        return 'default.jpg'

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )

    msg.body = f'''To reset your password visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not request this, ignore this email.
'''

    mail.send(msg)
