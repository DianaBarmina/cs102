import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    tbl_list = parser.findAll("table")
    body = tbl_list[2]
    # title_list = [title.text for title in body.findAll("a", {"class": "titlelink"})]

    body_title = body.findAll("a", {"class": "titlelink"})
    title_list, urls_list = [], []
    for i in body_title:
        title_list.append(i.text)
        urls_list.append(i["href"])

    urls_list = ["https://news.ycombinator.com/" + i if i[:4] == "item" else i for i in urls_list]

    body_auth = body.findAll("a", {"class": "hnuser"})
    auth_list = []
    for i in body_auth:
        auth_list.append(i.text)

    body_points = body.findAll("span", {"class": "score"})
    point_list = []
    for i in body_points:
        point_list.append(i.text.split()[0])

    body_idd = body.findAll("tr", {"class": "athing"})
    idd_list = []
    for i in body_idd:
        idd_list.append(i["id"])

    disc_list = []
    for i in idd_list:
        res = body.findAll("span", {"id": f"unv_{i}"})[0].findNext("a", {"href": f"item?id={i}"})
        disc_list.append(res.text)

    comm_list = []
    for i in disc_list:
        if i.isalpha():
            comm_list.append(0)
        else:
            ii = i.split()
            comm_list.append(ii[0])

    news_list = []
    for i, _ in enumerate(title_list):
        news_list.append(
            {
                "author": auth_list[i],
                "comments": comm_list[i],
                "points": point_list[i],
                "title": title_list[i],
                "url": urls_list[i],
            }
        )

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    body = parser.findAll("table")[2]
    resp = body.findAll("a", {"class": "morelink"})[0]["href"]
    return resp


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    print(get_news("https://news.ycombinator.com/newest", n_pages=2)[:4])
