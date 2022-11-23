import aiohttp
import asyncio
import time
import pandas as pd

start_time = time.time()

ERROR_PAGES = list()

async def get_recipes(session, url, page_num):
    headers = {'x-requested-with': 'XMLHttpRequest'}
    params = {'content': 'recipe', 'xhr': 'true','page': f"{page_num}"}
    async with session.get(url, params=params, headers=headers) as resp:
        try:
            recipes = await resp.json()

        except aiohttp.client_exceptions.ContentTypeError:
            ERROR_PAGES.append(page_num)
            return []

        return recipes["items"]



async def main(pages_to_scrape=range(1, 2000+1)):

    async with aiohttp.ClientSession() as session:

        all_recipes = []
        for page_num in pages_to_scrape:

            print("Scraping page", page_num)

            epicurious_url = 'https://www.epicurious.com/search'

            all_recipes.append(asyncio.ensure_future(get_recipes(session, epicurious_url, page_num)))

        original_recipes = await asyncio.gather(*all_recipes)
        # print(list(map(len, original_recipes)))
    

    original_recipes_flattened = list()

    for recipes in original_recipes:
        original_recipes_flattened.extend(recipes)
    # print(len(original_recipes_flattened))

    return original_recipes_flattened

        
if __name__ == "__main__":
    all_recipes_final = asyncio.run(main())

    if ERROR_PAGES:
        all_recipes_final.extend(asyncio.run(main(ERROR_PAGES)))

    print()
    print("-" * 40)

    print("Number of pages scraped:", 2000 - len(ERROR_PAGES))
    print("Number of Recipes:", len(all_recipes_final))
    print()
    
    print("Number of error pages:", len(ERROR_PAGES))
    print("Error pages:", ERROR_PAGES)
    print()

    print("Total Number of Recipes:", len(all_recipes_final))
    print()

    all_recipes_df = pd.DataFrame(all_recipes_final)
    print("Recipes DataFrame shape:", all_recipes_df.shape)
    print()

    print("--- Total Execution Time ---")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("-" * 40)
