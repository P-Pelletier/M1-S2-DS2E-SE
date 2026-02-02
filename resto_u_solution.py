import requests
import time 
import random
import re


user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0'}


def get_all_links():
    urlpage = 'https://www.crous-strasbourg.fr/se-restaurer/ou-manger/'
    res = requests.get(urlpage, headers = user_agent)
    links = re.findall('href="(.*?)">',str(res.text))
    
    names_links = dict()
    for link in links:
        if '/restaurant/' in link:
            link = str(link)
            name = re.findall('restaurant/(.*)/',link)[0]
            name = re.sub('-',' ',name)
            name = re.sub(' 2','',name)
            name = name.title()
            names_links.update({name:link})

    return names_links


def get_page(urlpage):
    time.sleep(2 + random.uniform(0,8))
    res = requests.get(urlpage, headers = user_agent)
    return res.text


def get_date(menu):
  date = re.findall('<time class="menu_date_title">(.*?)</time>',menu)
  date = re.sub('Menu du ','',date[0])
  return date


def get_meal_type_and_poles(meal):
  meal_type = re.findall('<div class="meal_title">(.*)</div>',meal)[0]
  meal_by_poles = re.findall("<li>(.*?)</li></ul></li>",meal)
  return meal_type, meal_by_poles


def get_meal_infos(meal_by_pole):
  pole, meal_infos = meal_by_pole.split("<ul><li>")
  meal_infos = meal_infos.split('</li><li>')
  meal_infos = [meal for meal in meal_infos if meal != '-']
  return pole, meal_infos


def get_all_meals_from_resto_u(name, urlpage):
  page = get_page(urlpage)
  
  menus = re.findall(r'<div class="menu">.*?</ul>\s*</div>\s*</div>', page, re.DOTALL)
  
  resto_u_all_infos = dict()
  for menu in menus:
    date = get_date(menu)
    meals = re.findall(r'<div class="meal">(.*?)</ul>\s*</div>',menu, re.DOTALL)
    
    resto_u_all_infos.update({date:{name:dict()}})
    for meal in meals:
      meal_type, meal_by_poles = get_meal_type_and_poles(meal)
      
      resto_u_all_infos[date][name].update({meal_type:dict()})
      for meal_by_pole in meal_by_poles:
        pole, meal_infos = get_meal_infos(meal_by_pole)
        resto_u_all_infos[date][name][meal_type].update({pole:meal_infos})
  return resto_u_all_infos
    
    
def get_all_infos():
  links = get_all_links()
  all_resto_u_all_infos = dict()
  for name, link in links.items():
    print(name)
    resto_u_all_infos = get_all_meals_from_resto_u(name, link)
    if resto_u_all_infos:
      for date in resto_u_all_infos.keys():
        if date in all_resto_u_all_infos:
          all_resto_u_all_infos[date].update(resto_u_all_infos[date])
        else:
          all_resto_u_all_infos.update({date:resto_u_all_infos[date]})
  return all_resto_u_all_infos

def show_item(list_):
    i = 1
    for item in list_:
        print('%s : %s'%(str(i),item))
        i+=1


def main():
  all_resto_u_all_infos = get_all_infos()
  quit = 'N'
  change_rest = 'Y'
  while quit=='N':
      dates = list(all_resto_u_all_infos.keys())
      show_item(dates)
      date_choosed = int(input('Select the date (type the number aside)'))
      restaurants = list(all_resto_u_all_infos[dates[date_choosed-1]].keys())
      while change_rest == 'Y':
          print('---------------------------------------\n\n')
          show_item(restaurants)
          rest_choosed = int(input('Select the restaurant (type the number aside)'))
          meal_keys = list(all_resto_u_all_infos[dates[date_choosed-1]][restaurants[rest_choosed-1]].keys())
          show_item(meal_keys)
          meal_choosed = int(input('Select the meal (type the number aside)'))
          
          menu = all_resto_u_all_infos[dates[date_choosed-1]][restaurants[rest_choosed-1]][meal_keys[meal_choosed-1]]
          for meal in menu:
              print('''%s :
              %s
                '''%(meal,menu[meal]))
          change_rest = input('Do you want to select another restaurant ? (Y/N)')
      
      
      quit = input('Do you want to quit ? (Y/N)')
      if quit == 'N':
          change_rest = 'Y'

if __name__ == '__main__':
  main()
