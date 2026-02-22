from run import app
import requests

with app.app_context():
    print('Testing connection...')
    with open('backend/static/profile_pics/default.jpg', 'rb') as f:
        img_bytes = f.read()
        
    url = f"{app.config['SUPABASE_URL']}/storage/v1/object/profile_pics/test_upload_raw.jpg"
    headers = {
        "Authorization": f"Bearer {app.config['SUPABASE_KEY']}",
        "Content-Type": "image/jpeg"
    }
    
    try:
        response = requests.post(url, headers=headers, data=img_bytes, verify=False)
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
    except Exception as e:
        print("EXCEPTION:", e)
