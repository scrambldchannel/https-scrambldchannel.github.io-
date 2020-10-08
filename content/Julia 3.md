Title: Julia day #3
Date: 2020-10-08 08:17
Category: julia
Tags: julia, jupyter, hacktober
slug: a-paradigm-shift-with-julia
Authors: Alexander
status: draft
Summary: So about these custom types? 

I really need to look at typing in Julia.... A lot of the pre-compile stuff seems to hang on the back of implicitly chosen overloaded functions. Not sure if that's the right way to say it, probably not.

Also, I finally found a sensible developer workflow with help from Slack. And then I messed it up again 

Not sure Jupyter works for, I found myself typing a Python one liner at one point and the REPL and the in built package manager are starting to make sense.

Have made a connection but how to handle authentication? I ripped this off from GitHub.jl, I don't know what half of it does but have vendored an API that seems to work for simple stuff. I'm only using basic auth so a lot of work needs to be done there but I wanted to concentrate on making something happen before getting too bogged down in that. 

I really need to look into macros, they seem to behave a bit like decorators in Python but I'm plugging and playing a few things I don't understand and it's fun!

I'm also getting some sort of failing github action that I didn't even really know I enabled as part of this template...