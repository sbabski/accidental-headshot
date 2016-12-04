import requests
import re
from bs4 import BeautifulSoup
import pprint

def sitemapper(page):
  print('mapping ' + page)
  soup = to_soup(page)
  section = soup.find('div', class_='page-content').contents[1].contents[1]
  columns = section.find_all('div', class_='index-list')
  result = []
  for c in columns:
    result += c.find_all('li')
  return result

def parse_page(title, type):
  print('extracting ' + title)
  soup = to_soup(format_url(title, type))
  section = soup.find_all('div', class_='page-content')
  #print(section)
  rel_data = re.findall('</h2>.*', str(section))
  if not rel_data:
    rel_data = re.findall('</h1>.*', str(section))
    print('no h2')
  #if not rel_data:
    #rel_data = re.findall('</h2>.*', str(section))
    #print('cannot find hr')
    #print(to_soup_encoded(format_url(title, type)))
  result = find_folders(BeautifulSoup(rel_data[0], 'html.parser'), title.replace(' ', ''))
  if not len(result):
    result = find_folders(section[0], title.replace(' ', ''))
  return result

def parse_subpage(url):
  soup = to_soup(url)
  return find_folders(soup)

def find_folders(data, title=''):
  #print('found relevant')
  folders = data.find_all('div', class_='folder')
  result = []
  if folders:
    print('extracting folders')
    for folder in folders:
      result += e(folder, extract_trope)
  else:
    print('no folders')
    def cb(uls):
      return test_sub(uls, title.replace(' ', ''))
    result = e(data, cb)
  return list(set(result))

def e(text, cb):
  #print('extracting section')
  uls = text.find_all('ul', recursive = False)
  if(not uls):
    print('no links after hr')
    return []
  return cb(uls)

def extract_trope(uls):
  #remove ymmv?
  #print('extract tropes')
  holder = []
  for ul in uls:
    for entry in ul:
      #only first layer
      trope = entry.find('a')
      if trope:
        href = str(trope['href']).lower()
        if 'main' in href:
          holder.append(href)
        else:
          print(href)
  print(len(holder))
  return holder

def test_sub(uls, title):
  #print('test for subpages')
  first_link = str(uls[0].find('a')['href']).lower()
  if title not in first_link:
    return extract_trope(uls)
  else:
    #print('extracting subpages')
    result = []
    for ul in uls:
      for entry in ul:
        trope = entry.find('a')
        if trope:
          href = str(trope['href']).lower()
          result += parse_subpage(href)
    return result

def format_url(title, type):
  type = type.replace(' ', '')
  title = title.replace(' ', '')
  return 'http://tvtropes.org/pmwiki/pmwiki.php/' + type + '/' + title

def to_soup(url):
  r = requests.get(url)
  return BeautifulSoup(r.content, 'html.parser')

def to_soup_encoded(url):
  r = requests.get(url)
  return BeautifulSoup(r.content, 'html5lib')

#for trope pages:

def parse_page_trope(title):
  print('extracting ' + title)
  soup = to_soup(format_url(title, 'main'))
  section = soup.find_all('div', class_='page-content')
  rel_data = re.findall(re.compile('</h2>.*', re.DOTALL), str(section))
  if rel_data:
    data = BeautifulSoup(rel_data[0], 'html.parser')
    labels = data.find_all('div', class_='folderlabel')
    if labels:
      print('folders')
      folders = data.find_all('div', class_='folder')
      del labels[0]
      def cb(i):
        return folders[i].find('ul', recursive=False)
      return extract_lists(labels, cb)
    else:
      new_data = BeautifulSoup(re.findall(re.compile('<span .*', re.DOTALL), rel_data[0])[0], 'html.parser')
      labels = new_data.find_all('span', class_='asscaps')
      if labels:
        print('spans')
        uls = new_data.find('body').find_all('ul', recursive=False)
        if(len(uls) == len(labels)):
          def cb(i):
            return uls[i]
          return extract_lists(labels, cb)
        else:
          print('error')
          return 0
      else:
        print('pages or nothing')
        return 0
  else:
    print('no h2')
    return 0

def extract_lists(labels, cb):
  result = []
  bad_types = ['Fan Works', 'Webcomics', 'Web Original', 'Toys', 'Real Life', 'Public Service Announcement', 'Web Video']
  for i in range(len(labels)):
    if not any(type in labels[i].get_text() for type in bad_types):
      result += get_media_hrefs(cb(i))
  return list(set(result))

def get_media_hrefs(ul):
  result = []
  for li in ul:
    for a in li.find_all('a', class_='twikilink'):
      link = a['href'].lower()
      bad_links = ['main', 'creator', 'usefulnotes']
      if 'tvtropes' in link and not any(type in link for type in bad_links):
        result.append(a['href'].lower())
  return result

#may be in folders DONE
#may be under headings class "asscaps" DONE
#may be in under new pages - whole page is list

#so far always under example h2, with or without colon DONE

#if not, add to a file for debugging
#may just be that there are none listed

#should discriminate by type of media: no advertisements, web comics, web originals, fan works, tabletop DONE

#each media should not be main, creator, usefulnotes DONE
#add to file for debugging if it is not these
#go into page, check other labels as next step

#if being directed from a media, make sure the media is added to the trope list

#see if has already been simply added, then add accordingly
