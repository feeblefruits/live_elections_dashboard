Elections 2019 solution by R3N13R & J4CQU3S
Copyright 2019 The Mail & Guardian - All rights reserved - dev@mg.co.za
Map Endpoint: https://playground.mg.co.za/maps/2019elections.html


ABOUT THE MAPBOX STUDIO DASHBOARD
Mapbox works with three templates: Datasets, Tilesets and Styles
Every map has a Dataset exported to a Tileset that can be Styled
Data can be manually updated here: https://studio.mapbox.com/datasets/mgdev/cjszui2th0x392ws5gx6s3uac/edit/
Styles can be updated here: https://studio.mapbox.com/styles/mgdev/cjsyl4zxb01o61fp5mvu80911/edit/ 
We have 3 layers in Styles so far: municipal-boundaries, data-features and leading-party
Our map is called Municipal-Results and we use property expressions to style features across a data range
Login to finetune these layers: https://account.mapbox.com/auth/signin/?route-to=https://studio.mapbox.com/

DEPENDANCIES
Install the mapbox SDK using pip or homebrew
https://mapbox-mapbox.readthedocs-hosted.com/en/latest/
https://github.com/mapbox/mapbox-sdk-py
pip install mapbox


RUN THE CODE
python mapengine.py
The code below can create and maintain GeoJson features on the map Using the Mapbox and IEC API's
The code can easily be extended 
Simply add more GeoJson features (Perhaps we can have links to News Stories, Videos or Eection day Photos also)


To run this script as a daemon:
Set the global var ENGINE to True and then run the code in a screen for the duration of an election    
https://linuxize.com/post/how-to-use-linux-screen/


CACHING CAVEATS
Tiles are served using a tile caching server - all servers incl ours honor the caching policy set in http headers
Then there is also intermediate caching by cloudflare and our CDN network
plus the mobile network if the user connect over GSM. Finally there is the caching policy on the client's browser
So how does caching affect rendering maps with real time data?
The data we serve may be real time as far as we are concerned
But what the visitor see in his browser depends very much on caching policies between us and the visitor
A first time visitor wil always see fresh data - if that same user hits the map 20 minutes later he may
well see a cached version of the map and most tiles will be (20 minutes old)
There are ways and little tricks to mitigate this - but we will have to do a lot of testing
What is the middle ground here? - I can spend a week solving this but at a cost of much more important priorities


OTHER CAVEATS
At this point I have not yet figured out how to trigger the Dataset export to our Tileset through the API
I have contacted Mapbox support for info on this, I suspect we wil have to use the upload API or the JS API
For now we trigger the export to the Tileset manually from the Mapbox Studio dashboard after an itteration
Here is how to do it:
After running the engine - login and go to https://studio.mapbox.com/datasets/
In the Mapbox Studio dashboard - click on the menu next to the dataset name [Municipal-Data]
Choose [Export to Tileset] - then - [Update a connected stylesheet] (ignore the time warning)
You will have to hard refresh your browser to see the latest data 


IDEAS
This map engine can be replicated to auto populate many types of maps for the M&G
If a service has an API then we can pull data and populate a map - for example - our own weather map

See: https://docs.mapbox.com/studio-manual/examples/ 
