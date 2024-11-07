import requests


class MealieAPI:
    def __init__(self, url, key):
        self.MEALIE_URL = url  # Basis-URL für Mealie
        self.API_KEY = key  # Dein API-Schlüssel
        self.HEADERS = {
            "Authorization": f"Bearer {self.API_KEY}",
        }
        self.get_user_self()  # Test if connection to Mealie is valid

    def get_user_self(self) -> bool:
        # Check connection and authentication data
        print(f"\nChecking connection and validating auth data...")

        # Send a GET request to get data
        response = requests.get(f"{self.MEALIE_URL}/api/users/self", headers=self.HEADERS)

        # Print information about the response
        if response.status_code == 200:
            print(f"\nConnection established! Auth data validated! - Status Code: {response.status_code}")
            return True
        else:
            print(
                f"\nError while connecting to your Mealie API! - Status Code: {response.status_code}, Response: {response.text}")
            return False

    def __get_recipe(self, recipe_id) -> dict:
        response = requests.get(f"{self.MEALIE_URL}/api/recipes/{recipe_id}", headers=self.HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error while getting Recipe from API! - Status Code: {response.status_code} - Response: {response.text}")

    def __put_recipe(self, recipe_id, data) -> str:
        response = requests.put(f"{self.MEALIE_URL}/api/recipes/{recipe_id}", headers=self.HEADERS, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error while getting Recipe from API! - Status Code: {response.status_code} - Response: {response.text}")

    def create_recipe_from_html(self, html_content) -> str:
        recipe_data = {
            "includeTags": True,
            "data": html_content
        }

        response = requests.post(
            f"{self.MEALIE_URL}/api/recipes/create/html-or-json",
            json=recipe_data,
            headers=self.HEADERS,
            timeout=300
        )

        if response.status_code == 201:
            recipe = response.json()
            print(f"Rezept erstellt mit ID")
        else:
            raise Exception(
                f"Error while getting Recipe from API! - Status Code: {response.status_code} - Response: {response.text}")

        return recipe

    def update_recipe_orig_url(self, recipe_id, orig_url) -> str:
        recipe = self.__get_recipe(recipe_id)
        recipe.update({"orgURL": orig_url})
        return self.__put_recipe(recipe_id, recipe)

    def upload_recipe_image(self, recipe_slug, image_url) -> str:
        files = {
            'image': open(image_url, 'rb')
        }
        data = {
            'extension': image_url.split('.')[-1]
        }
        response = requests.put(f"{self.MEALIE_URL}/api/recipes/{recipe_slug}/image", files=files, data=data,
                                headers=self.HEADERS)

        if response.status_code == 200:
            print(f"Cover Bild Rezept hinzugefügt")
            return response.json()
        else:
            raise Exception(
                f"Error while uploading Image to API! - Status Code: {response.status_code} - Response: {response.text}")

    def upload_recipe_asset(self, recipe_slug, recipe_asset) -> str:
        files = {
            'file': open(recipe_asset, 'rb')
        }
        data = {
            'extension': recipe_asset.split('.')[-1],
            'icon': "mdi-file-image",
            'name': recipe_slug + "_video"
        }
        response = requests.post(f"{self.MEALIE_URL}/api/recipes/{recipe_slug}/assets", files=files, data=data,
                                 headers=self.HEADERS)

        if response.status_code == 200:
            print(f"Video Asset hinzugefügt")
            return response.json()
        else:
            raise Exception(
                f"Error while uploading Video Asset to API! - Status Code: {response.status_code} - Response: {response.text}")