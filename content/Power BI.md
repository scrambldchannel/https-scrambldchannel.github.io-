Title: A quick dive into Power BI
Date: 2019-10-28 16:24
Category: bi
Tags: microsoft,power bi,bi,olap,analysis,visualisation
slug: power-bi-quick-dive
Authors: Alexander
Summary: Time to take a closer look at Microsoft's increasing pervasive BI platform

## Why?

Lots of jobs seemingly for it and tableau


## So what is it? 

You can install the desktop version for free (windows only)

MS offer a paid service offering that can be used to 

It's cheap! Seriously, from about 8 bucks a month per user. This compares pretty favourably to 

It connects to everything, or at least promises too. It makes a change from the old days of a ring fenced MS ecosystem. This includes all sorts of web services I haven't even heard of.

## Look and feel

Much like other office tools, with simalarities to access in particular


## Components

Data - getting data in 
Relationships - building a model
Reports - building reports / dashboards

## Resources

The power BI blog is OK
The youtube channel
Guy in a cube

## Using it

### Importing data

Use the query editor or data pane as it is on my version

There is a thing called mcode to edit queries

There's a nice preview

You can derive columns, split columns, modify columns, transpose data, grouping etc

There is a cool feature where you can step back through different transformation steps and see the effect in your preview pane. You can also rename steps to make it easier to follow the transform steps

A good best practice is to explicitly select the columns you want to keep when importing so that changes to table structure (well, at least new columns shouldn't break anything). You probably want to understand if tables are changing though

removing duplicates is nice too 

#### Text specific tools

Split, standardize the case, remove trailing whitespace or special characters

#### Numeric tools

Quite a lot out of the box, done in a simple way.

#### Date tools

Same for date tools, makes designing a time dimension really easy. Although in practice, I guess in most cases you would have a standard date / calendar dimension that you would just drop into all models

You have options for grouping and aggregating the data too but it makes me wonder whether it might be better to do those kind of operations at source anyway. Presumably the underlying database engines are often going to be a bit better at optimising those operations anyway and it would also reduce the amount of data being pulled

#### Merging/Appending columns

Like a pandas merge, essentially joining on a key.

Appending is just like a sql union I guess. Could presumably be used to add another month of data to an existing table for example There is an option where you can set a query to append all files within a directory whenever you refresh a query.

Not necessarily a good idea in most cases. I'd guess that in most cases you can either perform the necessary join in your query if you really need it in one table. In other cases you could use them in 

#### Data Source Settings

You can do things like change the file name or path for a data source

You can also set some queries not to refresh every time the model is refreshed. This is useful for when you have queries where the results never change (particularly if they are big). It might also prove useful if 


There are also data types you can use for region information. This really simplifies GIS visualisations for people

You can create hierarchies  using a set of columns which is again useful for geo vis. Time hierarchies are often created automatically too

You can also set a data source to actually be pulled from source at report time

### Creating the model

normalise
- Eliminate redundant data
- Minimise erros and anomalies
- Simplify queries

It allows you to create a simple star schema or snowflake model quickly and sets a lot of sensible defaults for you It actually does a pretty good job of guessing the cardinality and actually doesn't let you create many to many relationships etc

If you don't have relationships set, you end up with these funny repeating values which I find a little bit counterintuitive. It does let you set bi-directional filters though, not sure when this would be useful

You can hide fields from the report view though to prevent people doing something stupid. This can be useful to remove all keys leaving only the descriptive fields

There is a nice little feature to be able to show subsets of your tables on tabs of the viewer which can help with comprehending more complicated models


You can add calculated columns to your data sources but usually you just want a measure. Adding new columns is inefficient as you're instantiating them in the table data. Plus they don't understand row context

#### Measures

There are implicit and explicit measures. Implicit measures are created when you drag and drop this into a report but explicit measures are created in the model(?) section. 

Measures are defined in a language called DAX which is really just a syntax for creating calculations. 

Measures also obey the filter context so will automatically update once 

```dax
Batting Average = SUM(Batting[runs]) / (SUM(Batting[innings]) - SUM(Batting[not_outs]))
```

A lot of built in functions that do quite a lot of functionality

Unsurprisingly, a lot of functions will be familiar to users of Excel/Access etc which is a huge benefit for users coming from that background which is presumably a lot of them. 

Using measures in something like a calendar table (which I still want to call a dimension) might make sense but is there a performance difference?

Things get a little more interesting when using the RELATED keyword. You can reference columns from other tables provided a relationship is defined in your model 

The calculate function is pretty flexible and important, allows you to calculate something filter with filters applied

Eg - if you had a column of runs scored each ball, you could filter it for values of four and six give you a number of boundaries.

It allows you to over rule filter context for a certain row

FILTER is also important too and essentially allows you to filter the data by row to give you a subset of the data. It actually produces a new dataset. This can be performance hindering though so only use it when it can't be achieved any other way. Filter can be used to integrate measures into your filters which calculate can't do on itself

Iterator functions (ones with an X at the end mostly) let you calculate a measure at the leaf level and have it aggregated up. From a TM1 perspective, an iterator function is like calculating something at the N level and then just let it sum up while by default, measure calculations are applied at a C level.

Time intelligence functions allow you to calculate things like YTD, MTD easily. The can be used as a filter in the calculate function for a given measure to give you things like

DAX Best practice - use measures instead of new columns

Try to avoidimplicit measures

Break it into chunks

reference columns with the table name(even when not completely necessary)

Aim to redundant columns

Importing a column is generally better than calculating it. So if you can do it in SQL, you will get a better performance than creating it in a column

Minimise iterator functions

### Visualisation

Lots of different charts

Filters can be applied at different scope levels - chart - page - report

Slicers can give you a nice widget to manually select a date range. They can be synched across pages






