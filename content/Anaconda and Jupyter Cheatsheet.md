Title: Anaconda and Jupyter Cheatsheet
Date: 2019-08-26 11:59
Category: docs
Tags: anaconda, jupyter, python, ubuntu, linux
slug: jupyter-cheatsheet
Authors: Alexander
Summary: Trying to document a semi sensible workflow for Conda environments and kernels for Jupyter Notebook projects

> **WARNING**: This is a work in progress

# Introduction

A bit annoyed at finding myself having to re-learn a good workflow for setting up dev environments for Jupyter projects, I thought I'd try to list my workflow as is and update as I improve so I can refer back after a hiatus. This is a work in progress!

## Which Conda? Or no Conda at all?

Honestly, I fell into using Anaconda via a group project I joined a while back. I've used it sporadically since for stuff I want to do in Jupyter Notebooks mostly. I've never really looked at alternatives (ie other Condas, or using pipenv). For now, it's been nice to have a GUI but increasingly I'm trying to do things from the command line. That said, it's mostly meant I haven't had to think too much about 

### Installing Anaconda

Just pull the latest installer from [their website](https://www.google.com "Download page for Anaconda"). Download the appropriate bundle for your OS and architecture and follow the installation instructions. I am exclusively using the 3.7 distribution and don't have any legacy code I depend on for my projects.

Eg using Linux, wherever you've downloaded the installer(obviously full filename to match whatever you've downloaded):

```shell
$ source ./Anaconda3-2019.07-Linux-x86_64.sh
```

I generall y install it in the default location, i.e. an anaconda directory in ~/

### Managing Environments

You can use the GUI (ie anaconda-navigator) but can do most things from the command line. I find the gui a bit clunky to be honest but it's nice to be able to fall back on it.

#### List environments

This will give you a list of environments this conda knows about.

```shell
$ conda env list
# conda environments:
#
base                  *  /home/alex/anaconda3
[...]
$
```

#### Create

You probably want to create a new environment for a new project and install any releveant libraries within it.

```shell
$ conda create -n testenv python=3.7 anaconda
```

#### Activate

Once you've created an environment, activate it install packages of interest. 

```shell
$ conda activate testenv
(testenv) $
```

### Installing libraries

Libraries can be installed with either onda or pip. As a basic process, I search for them on conda first and install if available and install them via pip if not. 

#### Is it in the conda repos?

Eg. this looks for a package and tells you it's available.

```shell
(testenv) $ conda search plotly
Loading channels: ...working... done
# Name                       Version           Build  Channel             
plotly                        2.0.15  py27h139127e_0  pkgs/main           
plotly                        2.0.15  py35h43bf465_0  pkgs/main           
plotly                        2.0.15  py36hd032def_0  pkgs/main
[...]
(testenv) $
```

#### Great, install it from conda

We don't need to look any further, just install it.

```shell
(testenv) $ conda install plotly
```

##### It might not exist in the conda repo though

If you get a response like this, it's not available in the conda distribution you have. 

```shell
(testenv) $ conda search geoplotlib
Loading channels: done
No match found for: geoplotlib. Search: *geoplotlib*
[...]
(testenv) $
```

##### Try installing via pip instead

If it's a library that's available on PyPi, you should be able to install it by doing the following.

```shell
(testenv) $ pip install geoplotlib
Collecting geoplotlib
[...]
Successfully installed geoplotlib-0.3.2
(testenv) $
```
#### Deactivate

Once you are done fiddling with a given environment, you can deactivate it so that anything you do won't impact it.

```shell
(testenv) $ conda deactivate
$
```

## Managing Jupyter kernels and conda environments

I find it useful to create a single conda environment to launch jupyter notebooks from and leverage the ability to let them run kernels from other environments offered by installing ipykernel.

### Install ipykernel in our new env

This makes a kernel based on this environment available for environments running nb_conda_kernels.

```shell
(testenv) $ conda install ipykernel
```

### Create the notebook env

To launch our notebook server, we want to create a seperate env.

```shell
$ conda create -n notebook python=3.7 anaconda
```

#### Activate the notebook env and install nb_conda_kernels

Activate the new notebook env

```shell
$ conda activate notebook
(notebook) $ 
```

Install nb_conda_kernels

```shell
$ conda install nb_conda_kernels
```

### Launch a notebook server 

```shell
(notebook) $ jupyter notebook
```

#### Open the notebook base url in your browser

Eg navigate to [http://localhost:8888](http://localhost:8888 "your (probable) local server url")

You should now be able to create a new notebook using a kernel from your new environment. From there you should be able to import all the libraries you've installed into the current environment from the running kernel.

## Using Notebooks

A few notes on use of notebooks themselves.

### Where to save them

I created a new empty repo on Github and cloned that locally and work there on notebook projects, committing completed projects back to Github and potentially moving bigger projects into their own repo or publishing certain notebooks to this blog.

### Useful key bindings

|Action|Binding|
|------------|------------|
| Shift + Enter| Run Active Cell|