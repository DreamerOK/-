from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    url = "https://hi-news.ru/computers"
    
    limit = 1000
    
    chromeOptions = Options()
    chromeOptions.add_experimental_option(\
        "prefs",\
        {'profile.managed_default_content_settings.javascript': 2})
    driver = webdriver.Chrome('chromedriver', chrome_options=chromeOptions)
    driver.implicitly_wait(10)
    
    driver.get(url)
    articles = []
    while len(articles) < limit:
        articleElems = driver.find_elements_by_class_name("type-post")

        for articleElem in articleElems:
            articles.append(articleElem.find_element_by_tag_name("a")\
                            .get_attribute("href"))
            if len(articles) >= limit:
                break

        nextElems = driver.find_elements_by_class_name("search-arrow")
        for nextElem in nextElems:
            if nextElem.text == "Следующие":
                driver.get(nextElem.find_element_by_tag_name("a")\
                           .get_attribute("href"))
                break

    index = 0
    while index < len(articles):
        driver.get(articles[index])
        index = index + 1

        centerElem = driver.find_element_by_class_name("main-section")
        newsTitle = centerElem.find_element_by_class_name("single-title").text
        newsText = centerElem.find_element_by_id("post")\
                   .find_element_by_class_name("text").text
        try:
            newsKeywords = centerElem.find_element_by_class_name("tags")\
                           .find_elements_by_tag_name("a")
        except NoSuchElementException:
            newsKeywords = []
    
        xmlData = etree.Element("doc")

        sourceXmlData = etree.SubElement(xmlData, "source")
        sourceXmlData.text = etree.CDATA(driver.current_url)

        categoryXmlData = etree.SubElement(xmlData, "category")
        categoryXmlData.text = etree.CDATA("Компьютеры")
        categoryXmlData.attrib['verify'] = "true"
        categoryXmlData.attrib['type'] = "str"
        categoryXmlData.attrib['auto'] = "true"
    
        titleXmlData = etree.SubElement(xmlData, "title")
        titleXmlData.text = etree.CDATA(newsTitle)
        titleXmlData.attrib['verify'] = "true"
        titleXmlData.attrib['type'] = "str"
        titleXmlData.attrib['auto'] = "true"

        keywordsXmlData = etree.SubElement(xmlData, "keywords")
        keywordsXmlData.attrib['verify'] = "true"
        keywordsXmlData.attrib['type'] = "list"
        keywordsXmlData.attrib['auto'] = "true"
        for newsKeyword in newsKeywords:
            keywordXmlData = etree.SubElement(keywordsXmlData, "item")
            keywordXmlData.text = etree.CDATA(newsKeyword\
                                              .get_attribute('textContent'))
            keywordXmlData.attrib['type'] = "str"

        textXmlData = etree.SubElement(xmlData, "text")
        textXmlData.text = etree.CDATA(newsText)
        textXmlData.attrib['verify'] = "true"
        textXmlData.attrib['type'] = "str"
        textXmlData.attrib['auto'] = "true"
    
        xmlTree = etree.ElementTree(xmlData)
        xmlTree.write("Articles\\Article " + str(index) + ".xml",\
                      encoding="utf-8", xml_declaration=True,\
                      pretty_print=True)
        
    driver.close()

