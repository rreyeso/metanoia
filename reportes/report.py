# from GoogleNews import GoogleNews
# from newspaper import Article
# import pandas as pd

# googlenews=GoogleNews(start='01/01/2022',end='01/05/2022')
# googlenews.search('carne de cerdo')
# result=googlenews.result()
# df=pd.DataFrame(result)
# print(df.head())

from pathlib import Path

from gnews import GNews
from newspaper import Article

google_news = GNews(language='es', country='MX', period='7d', max_results=5)

html_template = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="report.css" rel="stylesheet">
    <title>Document</title>
</head>
<body>

    <img src="metanoia_logo.png" alt="Metanoia">
    
    <h1>Monitoreo semanal de cobertura en medios</h1>
    
    <h2>Resumen ejecutivo</h2>
    
    <ul>
        {business_summary}
    </ul>

    <h2>Indicadores macroeconómicos</h2>
    
    <iframe src="https://public.tableau.com/views/se0_pibe/se0_pib?:embed=y&amp;:display_count=no&amp;:showVizHome=no&amp;:showShareOptions=false&amp;:toolbar=no" width="100%" height="1000" frameborder="0" scrolling="no">
    </iframe>
    
    <iframe src="https://public.tableau.com/views/se0_inpc/INPCdeJalisco?:embed=y&amp;:display_count=no&amp;:showVizHome=no&amp;:showShareOptions=false&amp;:toolbar=no" width="100%" height="600" frameborder="0" scrolling="no">
    </iframe>
    
    <!--
    <iframe src="https://public.tableau.com/shared/W6FNPMB98?:embed=y&amp;:display_count=no&amp;:showVizHome=no&amp;:showShareOptions=false&amp;:toolbar=no" width="1120" height="800" frameborder="0" scrolling="no">
    </iframe>
    
    <iframe src="https://public.tableau.com/views/Patrones_16057339254850/patrones?:embed=y&amp;:display_count=no&amp;:showVizHome=no&amp;:showShareOptions=false&amp;:toolbar=no" width="1120" height="800" frameborder="0" scrolling="no">
    </iframe>

    <iframe src="https://public.tableau.com/views/ICCJ_t/Dashboard1?:embed=y&amp;:display_count=no&amp;:showVizHome=no&amp;:showShareOptions=false&amp;:toolbar=no" width="1120" height="900" frameborder="0" scrolling="no">
    </iframe>
    -->
    
    <p class="souces">Fuente: <a href="https://iieg.gob.mx/ns/?page_id=11884">IIEG (Instituto de Información Estadística y Geográfica de Jalisco)</a></p>

    <h2>Actualidad de las industrias restaurantera y porcina</h2>

    <div> 
        {specialized_articles}
    <div>
</body>
</html>
"""

def parse_specialized_articles(article):
    article_obj = Article(article["url"], language="es")
    article_obj.download()
    article_obj.parse()
    article_obj.nlp()
    html = f"""
    <section>
        <h4>{article["title"]}</h4>
        <p>{article["publisher"]["title"]}, <i>{article["published date"]}</i><p>
        <p>{article_obj.summary}</p>
        <p><a href="{article["url"]}">Leer artículo completo.</a></p>
    </section>
    """
    return html

def parse_summary_articles(article):
    article_obj = Article(article["url"], language="es")
    article_obj.download()
    article_obj.parse()
    article_obj.nlp()
    html = f"""
    <li>{article["title"]}. {article_obj.summary}. <i><a href="{article["url"]}">{article["publisher"]["title"]}</a>; {article["published date"]}</i></p>
    </li>
    """
    return html

specialized_articles = google_news.get_news('(industria restaurantera) OR (restaurantes AND guadalajara)') \
    + google_news.get_news('(industria porcina) OR (carne de cerdo)')
specialized_articles = ''.join([parse_specialized_articles(article) for article in specialized_articles])

summary_articles = google_news.get_news('negocios OR politica')
summary_articles = ''.join([parse_summary_articles(article) for article in summary_articles])

with open(Path(__file__).parent / "report.html", "w", encoding="UTF-8") as f:
    f.write(html_template.format(business_summary=summary_articles, specialized_articles=specialized_articles))