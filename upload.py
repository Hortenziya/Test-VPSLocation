import os
from datetime import datetime

import time
import requests


class FileUpload:
    upload_dir: str

    def __init__(self, upload_dir):
        self.upload_dir = upload_dir

    # функція, яку викликаємо на кожному сервері (відмінність - тільки посилання)
    def upload_to_vps(self, link, server_url):
        start_time = time.perf_counter()
        #завантажити файл на сервер
        response = requests.get(link)
        file_content = response.content
        file_size = int(response.headers['content-length'])

        self.check_free_space(file_size)

        filename = link.split('/')[-1]
        filepath = os.path.join(self.upload_dir, filename)
        #зберегти файл на сервері
        with open(filepath, "wb") as f:
            f.write(file_content)

        end_time = time.perf_counter()
        time_taken = round(end_time - start_time)
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        download_url = f"{server_url}/{filename}"

        download_info = {
            'download_url': download_url,
            'upload_time': current_time,
            'upload_duration': time_taken
        }

        return download_info

    # перевірити чи достатньо місця на диску
    def check_free_space(self, file_size):
        free_space = os.statvfs(self.upload_dir)[0] * \
                 os.statvfs(self.upload_dir)[4]
        if file_size > free_space:
            raise Exception("Not enough disk space")
