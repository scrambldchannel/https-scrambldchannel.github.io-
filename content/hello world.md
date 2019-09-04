Title: Blogging with Pelican, Github, and Travis CI
Date: 2019-07-26 12:24
Category: Misc
Tags: pelican, python
slug: hello-world
Authors: Alexander
Summary: Getting this show on the road

I've been meaning to set up a simple Github pages hosted blog for a while and wanted to play with a static site generator and a simple CI pipeline. Keen to use Python, I opted for Pelican and bootstrapped this page in a few minutes by following [this great guide from Will Barnes](https://wtbarnes.Github.io/2016/03/31/blogging-howto/ "Will's guide"). As ever, I tend to enjoy _playing_ with blogging frameworks more than I do actually blogging, so we'll see how this goes....

In a nutshell, [Pelican](https://Github.com/getpelican/pelican "Pelican on Github") is a static site generator written in Python. It works by rendering content written in either Markdown or Rst via Jinja templates to produce an easily deployed static html site. It reminds me of my first ever blog (now long lost) which used the venerable [Blosxom](http://blosxom.sourceforge.net/ "Blosxom on Sourceforge"). What I loved about it was that there was no need for a database, you just produced blog posts by editing text files. Tools like Pelican take it a step further though by generating the entire site and hosting that rather than having any server sided processing involved.

Another thing I wanted to play with was CI (continuous integration) services like Travis CI. Creating a Github hosted Pelican blog is a really nice intro to the concept and it can be quite cool to watch your site rebuild (in real time) after every push to Github, even if Travis does seem to be sending me emails suggesting my build is still failing even when it appears to be fine. I guess that's another little thing to enjoy investigating. 