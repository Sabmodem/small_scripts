import httpx
import aiofiles
from gen import gen_name as gen
from base64 import b64decode
import uuid
import asyncio
import os
from.logger import logging, loggerInit

searx_url = os.environ.get('SEARX_URL')

async def find_images_no_empty():
  images = []
  query = None
  while not images:
    query = gen()
    async with httpx.AsyncClient() as client:
      images = await find_images(query, client)
  logging.info(f'Поиск по запросу: "{query}"')
  return images

async def find_images(q, client):
  res = await client.post(searx_url, data={
    'category_images': 1,
    'q': q,
    'pageno': 1,
    'time_range': None,
    'language': 'en-US',
    'format': 'json',
  })
  return res.json()['results']

async def download_image(data, index, count, results):
  logging.info(f'Попытка скачивания №{index}. Всего попыток: {count}')
  filename = f'./img/{uuid.uuid4()}.jpg'
  try:
    async with httpx.AsyncClient() as client:
      p = await client.get(data['img_src'])
    async with aiofiles.open(filename,'wb') as outfile:
      await outfile.write(p.content)
      results.append(True)
      logging.info(f'Попытка скачивания №{index} успешна.')
  except httpx.InvalidURL:
    await outfile.write(b64decode(data['img_src'][22:]))
  except Exception as e:
    logging.error(f'Попытка скачивания №{index} не удалась по причине: {e.__repr__()}, Файл: {filename}')
    results.append(False)

async def main():
  loggerInit('parser.log')
  if not os.path.exists('./img'):
    os.mkdir('./img')
  results = []
  images = await find_images_no_empty()
  logging.info('Найдено результатов:', len(images))
  await asyncio.gather(*[download_image(img, i, len(images), results) for i, img in enumerate(images)])
  logging.info(f'Всего попыток: {len(results)}. Успешно: {results.count(True)}. Завершено с ошибкой: {results.count(False)}')

if __name__ == '__main__':
  asyncio.run(main())
