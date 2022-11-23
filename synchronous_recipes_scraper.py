import requests
import pandas as pd
import time

start_time = time.time()

NUM_OF_PAGES_TO_SCRAPE = 2000

# A function to send GET request to the recipes endpoint and extract the recipe data
def get_recipes(page_num):
  headers = {
      'x-requested-with': 'XMLHttpRequest',
  }

  params = {
      'content': 'recipe',
      'xhr': 'true',
      'page': f"{page_num}",
  }

  response = requests.get('https://www.epicurious.com/search', params=params, headers=headers)

  if response.status_code == 200:
    return response.json().get("items")

  else:
    return []


if __name__ == "__main__":
  all_recipes = list()

  for page_num in range(1, NUM_OF_PAGES_TO_SCRAPE+1):
    print(f"Scraping page {page_num}")
    all_recipes.extend(get_recipes(page_num))

  print()
  print("-" * 40)
  print("Number of pages scraped:", NUM_OF_PAGES_TO_SCRAPE)
  print("Total Number of Recipes:", len(all_recipes))
  print()

  all_recipes_df = pd.DataFrame(all_recipes)
  print("Recipes DataFrame shape:", all_recipes_df.shape)
  print()

  print("--- Total Execution Time ---")
  print("--- %s seconds ---" % (time.time() - start_time))
  print("-" * 40)
