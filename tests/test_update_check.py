import hashlib,io,unittest
from pathlib import Path
from unittest.mock import patch
import shutil
import update_check as u

PAYLOAD=b"MZ-test-installer"
TAG="v9.8.7"
NAME="QuickPhotoViewer-Setup-9.8.7.exe"
def release():
    return {"tag_name":TAG,"assets":[{"name":NAME,"size":len(PAYLOAD),
        "browser_download_url":u.RELEASES+"/download/"+TAG+"/"+NAME,
        "digest":"sha256:"+hashlib.sha256(PAYLOAD).hexdigest()}]}

class UpdateTests(unittest.TestCase):
    def test_update_and_current(self):
        self.assertEqual(u.parse_release(release(),"2.9.5")["name"],NAME)
        self.assertIsNone(u.parse_release(release(),"9.8.7"))
        self.assertIsNone(u.parse_release(dict(release(),prerelease=True),"2.9.5"))
        self.assertIsNone(u.parse_release(dict(release(),draft=True),"2.9.5"))
    def test_reject_asset(self):
        for key,value in [("browser_download_url","https://example.org/bad.exe"),("digest",""),("size",0)]:
            item=release();item["assets"][0][key]=value
            with self.assertRaises(ValueError):u.parse_release(item,"2.9.5")
    def test_verified_download(self):
        info=u.parse_release(release(),"2.9.5")
        with patch.object(u,"request",return_value=io.BytesIO(PAYLOAD)):
            p=u.download_installer(info)
            try:self.assertEqual(p.read_bytes(),PAYLOAD)
            finally:shutil.rmtree(p.parent)
        with patch.object(u,"request",return_value=io.BytesIO(b"x"*len(PAYLOAD))):
            with self.assertRaises(ValueError):u.download_installer(info)
    def test_cancel_and_oversize(self):
        info=u.parse_release(release(),"2.9.5")
        with patch.object(u,"request",return_value=io.BytesIO(PAYLOAD)):
            with self.assertRaises(InterruptedError):u.download_installer(info,cancel=lambda:True)
        with patch.object(u,"request",return_value=io.BytesIO(PAYLOAD+b"x")):
            with self.assertRaises(ValueError):u.download_installer(info)
    def test_source_guard(self):
        self.assertIsNone(u.installed_directory("2.9.5"))
if __name__=="__main__":unittest.main()
