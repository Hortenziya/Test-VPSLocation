function downloadWithBenchmark(fileName){
    getDownloadInfo("/download_info/" + fileName, (info) => {
        downloadFile(info['download_url'], (duration) => {
            console.log("download info", duration)
            const now = new Date();
            const year = now.getUTCFullYear();
            const month = String(now.getUTCMonth() + 1).padStart(2, '0');
            const day = String(now.getUTCDate()).padStart(2, '0');
            const hours = String(now.getUTCHours()).padStart(2, '0');
            const minutes = String(now.getUTCMinutes()).padStart(2, '0');
            const seconds = String(now.getUTCSeconds()).padStart(2, '0');
            const milliseconds = String(now.getUTCMilliseconds()).padStart(3, '0');

            const utcTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
            downloadResultMessage = `${info['vps_name']}, ${info['vps_city']}, ${info['vps_ip']}`
            downloadResultMessage += `, ${duration} sec, ${utcTime}`

            document.getElementById("downloadTime").innerHTML = downloadResultMessage
        })
    })
}

function getDownloadInfo(url, callback) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      console.log("download info", response)
      callback(response);
    }
  };
  xhr.send();
}

function downloadFile(fileUrl, callback) {
  console.log("downloading", fileUrl)
  const startTime = performance.now();
  const fileName = fileUrl.substr(fileUrl.lastIndexOf('/') + 1)
  fetch(fileUrl)
  .then(response => response.blob())
  .then(blob => {
    // Зберігаємо у Викачане
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();

    // Фіксуємо час
    const endTime = performance.now();
    const downloadTime = (endTime - startTime) / 1000;

    // Викликаємо функцію, яку передали в callback з тривалістю, як аргумент
    callback(downloadTime.toFixed(0))
  });
}