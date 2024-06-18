import base64

from requests import post

from pkt_fpk.settings import ASM_ADDRESS, ASM_APIKEY


def read_file_and_base64(filepath):
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def get_bio_model(b64data, bio_model="bio_common"):
    data = {
        'apikey': ASM_APIKEY,
        'model': bio_model,
        'wavs': [b64data]
    }

    r = post("http://"+ASM_ADDRESS+"/bio", json=data)
    if r.status_code != 200:
        return {
            "error": 'Ошибка подтверждения модели (код ошибки {}):\n{}'.format(
                r.status_code, r.content)}
    return {"b64data": r.json()[0]['data']}
