a lot of university students accross BC and even the world enjoy following the facebook page ubc confessions. I was curious if I could find a way to predict how many reactions a post would get even before being on the page.

This program tries to predict quite poorly (around 48% accurate according to evaluations) whether or not a pending post will perform better or worst than the "average" post this year (2019). Average being the average number of reactions per post (which is around 220)

I wanted to complete this project relatively quickly, and couldn't figure out a way to get post data easily from a facebook page via web scraping/crawling frameworks or APIs. After cambridge analytica, facebook's graph API does not give away as much information as it once did, and also the website itself isn't really friendly towards scraping tools. so I scrolled for about an hour, copy and pasted on screen text into a .txt file, and used regular expressions to extract posts, dates, and reaction data.

many improvements can still be made



