import string

import nltk
from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    s = s.translate(translator)
    tokens = nltk.word_tokenize(s)
    return tokens


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    idd = request.query.id
    lane = s.query(News).filter(News.id == idd).one()
    lane.label = label
    s.add(lane)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=5)
    for post in news_list:
        if (
            s.query(News)
            .filter(News.title == post["title"] and News.author == post["author"])
            .first()
            is None
        ):
            new_news = News(
                title=post["title"],
                author=post["author"],
                url=post["url"],
                comments=post["comments"],
                points=post["points"],
                label=None,
            )
            s.add(new_news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    table = NaiveBayesClassifier(1)
    label_list = s.query(News).filter(News.label is not None).all()
    nolabel_list = s.query(News).filter(News.label is None).all()
    X, y, z = (
        [i.title for i in label_list],
        [j.label for j in label_list],
        [clean(k.title) for k in nolabel_list],
    )
    X_fit, y_fit = x[: round(len(label_list) * 0.7)], y[: round(len(label_list) * 0.7)]
    table.fit(X_fit, y_fit)
    pred_lbl = table.predict(z)
    res_lst = []
    for i in pred_lbl:
        res_lst.append(label_type(i))
    result = (nolabel_list, res_lst)
    return template("news_template", rows=sorted(result))


if __name__ == "__main__":
    run(host="localhost", port=8080)
