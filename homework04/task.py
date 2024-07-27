from multiprocessing import Process
from threading import Thread
import asyncio
import aiohttp
import requests
import time
import argparse


def download(url):
    time_start = time.time()
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open('./downloads/'+filename, 'wb') as file:
        file.write(response.content)
    print(f'File {filename} downloaded in {time.time() - time_start:.2f} sec.')


async def download_async(url):
    time_start = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            filename = url.split('/')[-1]
            with open('./downloads/'+filename, 'wb') as file:
                async for chunk in response.content.iter_chunked(10):
                    file.write(chunk)
            print(f'File {filename} downloaded in {time.time() - time_start:.2f} sec.')


async def async_download(url_list):
    time_start = time.time()
    tasks = []
    for url in url_list:
        task = asyncio.ensure_future(download_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f'Download complete ({time.time() - time_start:.2f} sec.)')


def threading_download(url_list):
    time_start = time.time()
    threads = []
    for url in url_list:
        thread = Thread(target=download, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f'Download complete ({time.time() - time_start:.2f} sec.)')


def processing_download(url_list):
    time_start = time.time()
    processes = []
    for url in url_list:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print(f'Download complete ({time.time() - time_start:.2f} sec.)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('method', choices=['threading', 'processing', 'async'])
    parser.add_argument('url_list', nargs='+')
    args = parser.parse_args()

    if args.method == 'threading':
        threading_download(args.url_list)
    elif args.method == 'processing':
        processing_download(args.url_list)
    elif args.method == 'async':
        asyncio.run(async_download(args.url_list))
