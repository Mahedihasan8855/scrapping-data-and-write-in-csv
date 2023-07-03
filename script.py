import requests, os
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://amazfitwatchfaces.com/mi-band-6/fresh/p/2'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

watch_faces = soup.find_all('div', class_='col-md-3 col-sm-4 col-xs-6')

data = {
    'Title': [],
    'Description': [],
    'Image': [],
    'Tags': [],
    'Download Link': []
}

for watch_face in watch_faces:
    user_element = watch_face.find(class_='wf-user')
    if user_element is not None:
        user_name = user_element.find('a').text
        data['Title'].append(user_name)

    description_element = watch_face.find(class_='panel-body').find_next_sibling(class_='text-center wf-info')
    if description_element is not None:
        description = description_element.find_previous_sibling('div').text
        data['Description'].append(description)

    image_element = watch_face.find('img')
    if image_element is not None:
        image_src = image_element['src']
        data['Image'].append(image_src)

    tags_element = watch_face.find(class_='wf-comp')
    if tags_element is not None:
        tags = tags_element.text
        data['Tags'].append(tags)

    download_link_element = watch_face.find('a', class_='wf-act')
    if download_link_element is not None:
        download_link = download_link_element['href']
        data['Download Link'].append(download_link)
    

print(data)

max_length = max(len(values) for values in data.values())

data_with_defaults = {key: values + [values[-1] if len(values) > 0 else ''] * (max_length - len(values))
                     for key, values in data.items()}

df = pd.DataFrame(data_with_defaults)
output_folder = 'output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = os.path.join(output_folder, 'watch_faces_information.csv')
df.to_csv(output_path, index=False)