# ChrisPark_ShirleyLi

## Title: Faculty Match

## Purpose: 
The primary target audience are professors looking for collaborators or students looking for faculty advisors.
The objectives of the application is for the users to look up professors and information about their research activity such as their publication and citation history, as well as what venues they publish at. Users can also make notes about professors they might be interested in.

## Demo:

Installation: Make sure you have Python 3 and pip installed, we used Python 3.9.12. Also have an instance of academicworld database in Neo4j, MongoDB, and MySQL running. Download the application on this Github page. If necessary, modify the MySQLClient, MyNeo4jClient, and MyMongoClient params in app.py to match the host and port of your DBs.

To run:
```
1. pip install -r ./requirements.txt
2. python3 app.py
3. Visit http://127.0.0.1:8050/ on your browser to see the dashboard! 
```

## Usage: 
Select a name of a faculty from the dropdown menu to see information about their publication record, top publications, and top venues at which they published. After reviewing the faculty's information, users can make additional notes about each faculty as you browse. If there's a faculty the users like, the users have the option to save the faculty as a favorite and note down why. Users can select the faculty by using the dropdown. The left text field is a place to write your notes about the faculty member selected above. And, the right text field is a place to write why the selected faculty member is your favorite. The notes and favorites chart allows users to add, update, or delete the charts by clicking on the buttons. The buttons for updating notes are on the left. The buttons for updating favorites are on the right. The notes chart is on the left. The favorites chart is on the right.

## Design: 
We made a Dash app with two drop down menus and 6 widgets. Selection in the drop down menus triggers callbacks to various functions that will update the tables and graphs in the widgets. We also implemented 3 client classes for each database (MongoDB, MySQL, and Neo4j) that have methods to retrieve entries that are used to populate and update the dropdowns and figures. 
The dropdowns for searching professor names are implmeneted in MySQL
The first widget displays a scatterplot of the author’s publications, with year on the x axis, and num citations on y. You can hover for more info like the title. It is implemented in Neo4j.
The second widget is a bar chart of the publication count trend over the years so that you can visualize the professor’s research output/productivity. It is implemented in MySQL.
The third is a table of the professor’s top 5 publications, and  you can see the number of citations. It is implemented in Neo4j.
The fourth is a funnel chart of the top venues at which the professor has published/presented his works. It is implemented in MySQL.
The fifth and the last widgets are tables that users can modify by using buttons to add, update, or delete entries to the table. They are updating widget in MongoDB that can perform updates of the backend databases.


## Implementation: 
The application *app.py* contains our Dash implementation of widgets, and callback functions dictated by buttons and dropdowns. *mysql_own.py, neo4j_own.py, and mongodb.py* contain our implementation of client connection classes and query/update methods for MySQL, Neo4j, and MongoDB respectively. The data visualization includes scatter plot, tables, bar graph, and funnel chart.

## Database Techniques: 
We used database indexing, stored procedures, and views in the MySQLClient class under mysql_own.py. Indexes for the faculty and publication tables were created using the MySQL client to allow efficient lookup on faculty and publication names. A stored procedure was used to query for top venues of individual professors, which was also created by the MySQLClient class into the MySQL database, and the procedure was called in the get_top_venue_list function which retrieves the top venues at which a professor published by citation numbers. A view called faculty_names was created to retrieve all faculty names, and a select is done on this view in the find_all_faculty_names function.

## Extra-Credit Capabilities:

## Contributions:
#### Shirley : 
* Contributed to the ideation of the overall dashboard ~2hr 
* The implementation for 4 widgets, including layout using Dash, plotly graphs/tables, and callback methods ~6hr 
* The query methods for Neo4j and MySQL, ~4hr
* The implementation of database techniques ~4hr
* The structuring and base methods for each database client class. ~2hr
#### Chris : 
* Implemented 2 updating widgets in MongoDB by allowing users to add texts in text fields and buttons - took 8 hours
* Implement the front end / user interface using css file, background, logo, and app layout - took 8 hours
* Made the app prototype with 3 widgets using jupyter notebook - took 2 hours
* Edit the video demo and upload it - took 30 minutes
#### Both : 
* Held weekly meetings to discuss and implement our changes together through discord, zoom, and github - took 8 hour each
* Video demo recording and script - took 1 hour each

<img width="1286" alt="image" src="https://user-images.githubusercontent.com/24705872/171320138-89ed6154-0cba-444e-ab43-c113d49b14de.png">
<img width="1258" alt="image" src="https://user-images.githubusercontent.com/24705872/171320264-c4774097-aa40-41ad-a1c7-328822039395.png">
<img width="1272" alt="image" src="https://user-images.githubusercontent.com/24705872/171320319-de8e0cae-a4fd-4a5d-b980-4827a6839d23.png">


