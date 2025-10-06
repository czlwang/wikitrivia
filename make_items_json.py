import os
import json
from PIL import Image, ExifTags
from datetime import datetime
from glob import glob as glob
from pillow_heif import register_heif_opener

image_paths = glob("/home/czw/Documents/2025/wikitrivia_images/*")
items = []

register_heif_opener()

from PIL import Image
import pillow_heif


pillow_heif.register_heif_opener()

#img = Image.open('/home/czw/Documents/2025/wikitrivia_images/IMG_8738.HEIC')
#exif_data = img.getexif()
#img.save('/home/czw/Documents/2025/wikitrivia/test_image.png', format('jpeg'), exif_data=exif_data)
#
#exit()

for i,filename in enumerate(image_paths):
    try:
        image_exif = Image.open(filename)._getexif()
    except:
        continue

    #{"date_prop_id":"P571","description":"Country in western Europe","id":"Q31","image":"Flag_of_Belgium.svg","instance_of":["sovereign state"],"label":"Belgium","occupations":null,"page_views":234155,"wikipedia_title":"Belgium","year":1830}
    if image_exif:
        # Make a map with tag names
        exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
        #print(exif)
        # Grab the date
        if 'DateTimeOriginal' not in exif:
            print("no date")
            continue
        try:
            date_obj = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        except:
            print("giving up")
            continue
        date_str = date_obj.strftime("%Y-%m-%d")
        #print(date_str)
        #print(date_obj)
        print(exif['DateTimeOriginal'])
        #print(str(exif['DateTimeOriginal']))
        img_file = os.path.basename(filename)
        d = {"date_prop_id":"P404","description":"Country in western Europe","id":f"{i}","image":f"{img_file}","instance_of":["sovereign state"],"label":f"{i}","occupations":None,"page_views":234155,"wikipedia_title":"Belgium","year":date_str}
        items.append(json.dumps(d)+"\n")
    else:
        print('Unable to get date from exif for %s' % filename)

print(items)
with open("public/items.json", "w") as f:
    f.writelines(items)

