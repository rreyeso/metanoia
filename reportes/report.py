# from GoogleNews import GoogleNews
# from newspaper import Article
# import pandas as pd

# googlenews=GoogleNews(start='01/01/2022',end='01/05/2022')
# googlenews.search('carne de cerdo')
# result=googlenews.result()
# df=pd.DataFrame(result)
# print(df.head())

from datetime import date, timedelta
from pathlib import Path

from gnews import GNews
from newspaper import Article, Config

from data import indicators

html_template = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="report.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.8.3.min.js"></script>
    <title>Document</title>
</head>
<body>

    <img src="metanoia_logo.png" alt="Metanoia">
    
    <h3>Monitoreo semanal de cobertura en medios</h1>
    <p>Semana del {start_date} al {end_date}</p>
    
    <h4>Panorama Económico y Político</h2>
    
    <div>
        {business_summary}
    </div>

    <h4>Indicadores Económicos</h2>
    
    <div>
        {indicators}
    </div>
    
    <p class="souces">Fuente: <a href="https://www.inegi.org.mx/app/reloj/semaforo.html">INEGI - Semáforo de componentes cíclicos</a></p>

    <h4>Actualidad de las industrias restaurantera y porcina</h2>

    <div> 
        {specialized_articles}
    </div>
</body>
</html>
"""

def parse_specialized_articles(article):
    try:
        article_obj = Article(article["url"], language="es")
        article_obj.download()
        article_obj.parse()
        article_obj.nlp()
        html = f"""
            <li><b>{article["title"]}</b>. {article_obj.summary}
            <i><a href="{article["url"]}">{article["publisher"]["title"]}</a>; {article["published date"]}</i></p>
            </li>
        """
        return html
    except Exception as e:
        print(e)
        return ""

def parse_summary_articles(article):
    try:
        article_obj = Article(article["url"], language="es")
        article_obj.download()
        article_obj.parse()
        article_obj.nlp()
        html = f"""
            <li><b>{article["title"]}</b>. {article_obj.summary}
            <i><a href="{article["url"]}">{article["publisher"]["title"]}</a>; {article["published date"]}</i></p>
            </li>
        """
        return html    
    except Exception as e:
        print(e)
        return ""
    
google_news = GNews(language='es', country='MX', period='8d', max_results=3)

specialized_articles = google_news.get_news('"lupes bbq"') \
    + google_news.get_news('(industria restaurantera en mexico) OR (restaurantes AND guadalajara)') \
    + google_news.get_news('(industria porcina) OR (carne de cerdo)') \
    + google_news.get_news('(uber eats) OR (didi food)')
specialized_articles = ''.join([parse_specialized_articles(article) for article in specialized_articles])

google_news = GNews(language='es', country='MX', period='8d', max_results=5)

summary_articles = google_news.get_news('economía OR política')
summary_articles = ''.join([parse_summary_articles(article) for article in summary_articles])

with open(Path(__file__).parent / "report.html", "w", encoding="UTF-8") as f:
    f.write(html_template.format(
        start_date=date.today() - timedelta(days=8),
        end_date=date.today(),
        business_summary=summary_articles, 
        indicators=indicators(),
        specialized_articles=specialized_articles),
    )