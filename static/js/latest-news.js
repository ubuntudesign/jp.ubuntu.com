function formatDate(date) {
  const parsedDate = new Date(date);
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ];

  const day = parsedDate.getDate();
  const monthIndex = parsedDate.getMonth();
  const year = parsedDate.getFullYear();

  return day + " " + monthNames[monthIndex] + " " + year;
}

function htmlForLatestArticles(articles) {
  const articlesTree = document.createDocumentFragment();
  for (let i = 0; i < articles.length; i++) {
    const article = articles[i];
    const div = document.createElement("div");
    div.classList.add("col-3");
    const header = document.createElement("h4");

    const link = document.createElement("a");
    link.href = article.link;
    link.innerHTML = article.title.rendered;

    const date = document.createElement("p");
    date.classList.add("u-no-padding--top");
    const em = document.createElement("em");
    const time = document.createElement("time");
    time.setAttribute("pubdate", true);
    time.datetime = article.date;
    time.innerHTML = formatDate(article.date);

    date.appendChild(time);
    date.appendChild(em);
    header.appendChild(link);

    div.appendChild(header);
    div.appendChild(date);

    articlesTree.appendChild(div);
  }
  return articlesTree;
}

function htmlForLatestPinnedArticle(article) {
  const articlesTree = document.createDocumentFragment();

  const heading3 = document.createElement("h3");
  heading3.innerHTML = "Spotlight";
  const innerDiv = document.createElement("div");
  const heading4 = document.createElement("h4");
  const link = document.createElement("a");
  link.href = article.title;
  link.innerHTML = article.title.rendered;

  const paragraph = document.createElement("p");
  paragraph.classList.add("u-no-padding--top");
  const em = document.createElement("em");
  const time = document.createElement("time");
  time.setAttribute("pubdate", true);
  time.datetime = article.date;
  time.innerHTML = formatDate(article.date);

  em.appendChild(time);
  paragraph.appendChild(em);
  heading4.appendChild(link);

  innerDiv.appendChild(heading4);
  innerDiv.appendChild(paragraph);

  articlesTree.appendChild(heading3);
  articlesTree.appendChild(innerDiv);

  return articlesTree;
}

function reqListener() {
  const data = JSON.parse(this.responseText);
  const latest = data.latest_articles[0];
  const latestPinned = latest[0];

  const containerForLatestArticles = document.getElementById("latest-articles");
  const html = htmlForLatestArticles(latest);
  containerForLatestArticles.appendChild(html);

  if (latestPinned) {
    const containerForLatestNews = document.getElementById(
      "latest-news-container"
    );
    containerForLatestNews.classList.add("p-divider");

    const containerForSpotlight = document.getElementById("spotlight");
    containerForSpotlight.classList.add("col-3 p-divider__block");

    const htmlSpotLight = htmlForLatestPinnedArticle(latestPinned);
    containerForSpotlight.appendChild(htmlSpotLight);
  }
}

const oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", "blog/latest-news");
oReq.send();
