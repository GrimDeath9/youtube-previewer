import asyncio
import aiohttp

async def __request(session, url):
    async with session.get(url) as r:
        return await r.text()

async def __multiscrape(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(__request(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results
         
async def __main(urls):
    async with aiohttp.ClientSession() as session:
        output = await __multiscrape(session, urls)
        return output
    
def scrape(urls):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(__main(urls))