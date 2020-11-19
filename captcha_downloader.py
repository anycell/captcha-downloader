# encoding=utf-8

import sys
import os
import time
import requests

def content_type_to_img_suffix(content_type):
    img_suffix = '.jpg'
    content_type = r.headers.get('Content-Type', '').lower()
    if content_type.find('image/jpeg') >= 0:
        img_suffix = '.jpg'
    elif content_type.find('image/gif') >= 0:
        img_suffix = '.gif'
    elif content_type.find('image/bmp') >= 0:
        img_suffix = '.bmp'
    elif content_type.find('image/tiff') >= 0:
        img_suffix = '.tif'
    elif content_type.find('image/x-icon') >= 0:
        img_suffix = '.ico'
    else:
        print('unrecognized content type: {0}, use default suffix: {1}'.format(content_type, img_suffix))

    return img_suffix


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        count = int(sys.argv[2])
        save_dir = sys.argv[3]
    except Exception as e:
        print("Usage: \r\npython download_captcha.py {url} {download-count} {save_dir}")
        os._exit(-1)

    if not os.path.exists(save_dir):
        print("save dir does not exist: {0}".format(save_dir))
        os._exit(-1)


    print("Download task start, count: {0}".format(count))

    fname_idx = 1
    idx = 0
    while idx < count:

        # if (idx % 10 == 0) or (idx + 1 == count):
        print("Downloading: {0}/{1}".format(idx+1, count))

        try:
            r = requests.get(url)
        except Exception as e:
            print("Download error: {0}, try again...".format(str(e)))
            time.sleep(1)
            continue

        idx += 1

        content_type = r.headers.get('Content-Type', '').lower()
        img_suffix = content_type_to_img_suffix(content_type)

        img_path = os.path.join(save_dir, '{0}{1}'.format(fname_idx, img_suffix))
        while os.path.exists(img_path):
            fname_idx += 1
            img_path = os.path.join(save_dir, '{0}{1}'.format(fname_idx, img_suffix))

        with open(img_path, 'wb') as f:
            f.write(r.content)

    print('Download task done!')
