Thanks a lot for taking the time to work on this challenge. 

To rank the search results better, we want to predict possible categories to boost for a given user search query.

For this purpose we collected `search` and `productview` events. As an applied scientist in the search team, we kindly ask you to develop a simple CLI to predict categories to boost for a given search term.

Please include the project with all the source code as a zip/tar.gz file.

You are free to use any library or programming language. We would like to run the project in our local machines easily.


`events.log` file is in JSONL format. Every row has an event serialized as json with the properties:
{
    "session": session id of the request,
    "name": name of the event,
    "query": (search event only) text the user searched,
    "title": (productview event only) title of the product,
    "product_id": (productview event only) id of the product,
    "category":(productview event only) category of the product,
}


We hope you will have fun while building the project.
