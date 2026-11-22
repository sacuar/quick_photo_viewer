from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent/'icons'
im=Image.open(p/'original-blue.png').convert('RGBA')
im.save(p/'quick_photo_viewer.ico',sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
im.save(p/'quick_photo_viewer.png')
banner=Image.new('RGB',(164,314));d=ImageDraw.Draw(banner)
for y in range(314):
    t=y/313;d.line((0,y,164,y),fill=(int(13+14*t),int(34+65*t),int(58+65*t)))
logo=im.resize((120,120),Image.Resampling.LANCZOS);banner.paste(logo,(22,78),logo);banner.save(p/'wizard.bmp')
small=Image.new('RGB',(55,55),'#eef6fa');logo=im.resize((49,49),Image.Resampling.LANCZOS);small.paste(logo,(3,3),logo);small.save(p/'wizard-small.bmp')
