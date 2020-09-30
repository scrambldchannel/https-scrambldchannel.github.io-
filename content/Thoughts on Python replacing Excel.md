Title: Will Python replace Excel? The answer is, er, complicated
Date: 2020-09-27 15:56
Category: tm1
Tags: excel, python
slug: python-replacing-excel
Authors: Alexander
Status: draft
Summary: Python has experienced huge growth for decades and is now finding its way into all sorts of areas but will it replace Excel as some people seem to thing? I confess that I'm skeptical

At a meetup I attended in Manchester earlier this year (shout out to the [North West Ruby User Group](https://www.meetup.com/North-West-Ruby-User-Group/)) I had an interesting conversation with a guy who was the founder of a startup. When I asked about his business model, he looked a little sheepish and explained that it was a SaaS offering that allowed clubs and schools to manage subscriptions and billing. Like many, when I hear "startup" I immediately think of companies that are going to disrupt the delivery of new contact lenses by autonomous drone _before_ you even know that you've run out by using ML models based on how many times you've eaten carrots or listened to Art Garfunkel. OK so I made that up but if you end up making money out of it, I will be asking for equity.

There was no need for this guy to feel embarrassed about his business model. We talked for a while and it seemed, after a tough start, he and his partners were doing well. Given the current climate, I worry a little about their cash flow but then no one really foresaw this. I hope they're doing OK. Pandemics aside, one thing he said really stuck with me which, to paraphrase, was something like:

> Behind every spreadsheet there's a potential business opportunity

I liked this way of looking at things, although I suspect it wasn't an original insight, it made sense to me as someone who has spent years working with a technology that has an unofficial slogon of "Escape Excel Hell". In fact a cursory web search found [this article](https://www.businesswire.com/news/home/20040511005458/en/Latest-Version-Applixs-TM1-Offers-Escape-Spreadsheet) suggesting that "Latest Version of Applix's TM1 Offers Escape from 'Spreadsheet Hell'". This is still a pretty prevalent selling point in the TM1 space, and not one I'm criticising, but it seems that in 2020, there's still quite a lot of "Spreadsheet Hell" going around.

In fact a few months ago, I listened to [this episode](https://talkpython.fm/episodes/show/200/escaping-excel-hell-with-python-and-pandas) of the excellent _Talk Python to me_ podcast. It was great, and I don't mean to criticise it or guest Chris Moffitt at all. Indeed, his blog [Practical Business Python](https://pbpython.com/) looks to be a great resource and I don't think he's suggesting Python will replace Excel either. I have read a number of articles recently that do seem to put that idea forward though. 

### Why? What's stopping them moving to Python? 

I can think of a few reasons actually which I've listed below. I should point out that I don't really have any skin in this game or a strong affinity for any particular tool, indeed I don't use Excel personally at all, but I do think spreadsheets have a place and happily use Google Sheets for a few things.

#### Inertia

This is the obvious one. I've read that Excel alone has over 750 million users. That's a lot and between them, they're managing spreadsheets that may (literally) date back decades. I've worked on numerous projects where the stated aim is to eradicate a collection of bloated, poorly understood spreadsheets. It's hard to unpick them, and that's from someone who is paid to do so. It's not feasible to expect that people can migrate away from these legacy tools and workflows without significant (i.e. expensive) outside support. Furthermore, people just don't like change. Quite frankly, the idea that many people have the appetite to change is a bit ridiculous.

#### It's not just a new tool, it's a new paradigm

When I read articles about this Python based revolution, most of them seem to focus on comparing Pandas to Excel for manipulating and analysing data. Leaving aside the difficulty in learning a new tool, this feels like comparing apples to oranges to me. A spreadsheet provides what is essentially a functional programming environment where is using Python is broadly imperative. In fact Excel is like a trojan horse that lets people write software without realising it. I assume that most of the proponents of this are thinking of people transitioning to notebook environments but that's still a completely different way of thinking than a spreadsheet. Some pundits seem to think that there is a whole new generation entering the workforce that have all learned Python at university. I think in some job roles, this might be true but I think this isn't representative of the overall Excel userbase.

#### Just because it makes sense for one use case, doesn't mean it will for all

Most of the posts I read also seem to follow the pattern of "I replaced my Excel spreadsheet with Python so everyone should". Obviously this doesn't transfer across domains. I still see a lot of people using spreadsheets to manage things like simple to do lists. Sure, you could argue there are better tools for this, I'd opt for a kanban board like Trello for example, but it sure isn't going to be solved by a Python script or a notebook.

#### The transition proposed is really to a different way of modelling, not a different tool

Some of the use cases I've seen labelled as "Python is better than Excel" aren't really talking about that at all. Instead, they are describing the process of transitioning to using a completely different way of modelling. I've heard people comparing the use of a rudimentary Excel roll forecasting model that uses a few assumptions to do a rolling forecast to a fully fledged scikit learn model trained with years of historical data. Of course Python is a better choice here but you're not really talking about the same thing.

#### Visualisation and Integration with the dreaded Powerpoint

Python has an amazing list of charting options which I go into here but these aren't a drop in replacement for charting in Excel. Indeed, one of the real advantages of the Microsoft stack in this space is how uniform the UX is across a number of tools like Excel, Access, Power BI and even SSAS. Many Excel users also need to ultimately get their visuals into Powerpoint which, as much as I loathe it, is still all pervasive in some organisations. Sure, there are ways to do this with Python but they're non-trivial. If anything, I'd say that Power BI is the real growth area in this space. 

#### The maintainability fallacy

I've come across a number of pundits suggesting that Python is somehow inherently easier to maintain than an Excel spreadsheet. I think this is a little naive as anyone who has tried to unpick bad code, in any language, should appreciate. You can write horrible Python and managing environments and re-producibility with Python is in some ways harder than Excel given the need to manage different Python environments and dependencies. Sure, raw Python is easier to check into git than a spreadsheet full of formulas but try explaining what git is to a junior accountant, I dare you. That's after you've explained how to install their project's dependencies with pip or conda. 


#### Lots of people still only have a hammer

> When all you have is a hammer, everything looks like a nail

Most people have come across this phrase, or something like it, also known as the [Law of the Instrument](https://en.wikipedia.org/wiki/Law_of_the_instrument). This is abundantly true with Excel too, I've seen all sorts of things implemented in Excel, some of it horrible, some of it admirable. However I don't think it's a given that the toolbox is going to expand any time soon. Python on Windows has improved out of sight but it's still not trivial for the average Excel user. Moreover, in many corporate environments, there are significant barriers in place. A common on ramp is a tool like Anaconda but in my experience this isn't always easily available, or supported, in big organisations. 

### So what is going to happen then? 

I'm not sure but I don't see a new dawn of Python domination in this space any time soon. I think we will see a shift from a dependence on locally run Excel stacks to cloud spreadsheet offerings. Google sheets raised the bar when it came it to concurrent use and may have stolen some ground from Microsoft but I suspect
