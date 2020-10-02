Title: Dissecting a TM1 pro file
Date: 2020-09-24 11:01
Category: tm1
Tags: tm1, cognos, ibm, ti
slug: dissecting-a-tm1-pro-file
Authors: Alexander
Summary: Ever wondered what's going on in your .pro files? I did so I tried taking one apart
Status: draft

An [issue](https://github.com/cubewise-code/tm1py/issues/383) raised over at the TM1py project asked for a feature to add hot promotion of TM1 processes saved as pro files. The API allows creation of TI processes and TM1py provides some useful wrapper functions that can achieve this. However the fiddly part was parsing a pro file to get the relevant information out to allow us to create an instance of the TM1py Process object.

Pro files are saved as text so are human readable. As well as containing the code defined in the different tabs (prolog, metadata, data and epilog) the file contains metadata providing additional details about the file. For this example, I'm taking apart the [process to refresh feeders](https://github.com/cubewise-code/bedrock/blob/master/main/%7Dbedrock.cube.rule.processfeeders.pro) from the [Bedrock project](https://github.com/cubewise-code/bedrock).

The process is pretty straightforward, it takes a cube, or list of cubes, and a few other general parameters and does what it says on the tin - i.e. each specified cube will have its feeders refreshed. This is what it looks like on file:


```text
601,100
602,"}bedrock.cube.rule.processfeeders"
```

These first couple of lines specify the version and the name of the process. How do I know this? Wim pointed me in the direction of the codes in the TM1 docs, notably the file at ```tm1_64/TM1JavaApiDocs/constant-values.html``` which contains a list of constants in the docs for the old Java API. It turns out that these correspond to the codes that start each line in the pro file.

As it goes on, you can see, each line is simply a code and either a numeric value or a string. I'm not sure why ```C:\TM1Data\Bedrock3\Data\Excel.RUX``` is there, it doesn't seem relevant in the context of what this process is doing. Looking at the codes, those are the settings for the ```datasourcename``` and ```datasourcenameforserver```. So I reckon they can actually go. 

```text
562,"NULL"
586,"C:\TM1Data\Bedrock3\Data\Excel.RUX"
585,"C:\TM1Data\Bedrock3\Data\Excel.RUX"
```

A lot of these values are blank and a cursory read of the manual suggests they are used to specify the various different options for a processes datasource. ```565``` is the password, which again shouldn't be relevant for this process (but presumably doesn't stop the process from being loaded at startup). 

```text
564,
565,"iz13ydO3pyNWPxv;_ZDRUHNTdGmz=bnSCs8wD[SQouyR>TbW4@>Mfu>4nKmG>fk]idlFzBx3V]Jd`kG?5Ncaw\0<`W6CO0JtwGA==1;Q[LnvggL/{Csa9f`RMzyLg[8`MRam[xNgATuF]cYz2cH:=PM4Mhf6qml[K?DwW7kl;Z2VGJjZfVw?FA}ZEnoQRgO$KQzB9@9F"
559,1
928,0
593,
594,
595,
597,
598,
596,
800,
801,
566,0
567,","
588,"."
589,","
568,""""
570,
571,
569,0
592,0
599,1000
```

This is a bit different though. For those familiar with TI processes, it's simple enough to work out what's going on. These are the names of the parameters of the process. The ```4``` after ```560``` indicates that there are four parameters specified.

```text
560,4
pLogOutput
pStrictErrorHandling
pCube
pDelim
```

This is a bit more opaque but next come the parameter types. These define the type of the parameter, ```1``` indicates a number and ```2``` indicates a string. 

```text
561,4
1
1
2
2
```

To round it off, we see the default values and the hint the TI process editor provides:

```text
590,4
pLogOutput,0
pStrictErrorHandling,0
pCube,""
pDelim,"&"
637,4
pLogOutput,"OPTIONAL: Write parameters and action summary to server message log (Boolean True = 1)"
pStrictErrorHandling,"OPTIONAL: On encountering any error, exit with major error status by ProcessQuit after writing to the server message log (Boolean True = 1)"
pCube,"REQUIRED: Process feeders for this cube (Separated by Delimiter, Accepts Wild card)"
pDelim,"OPTIONAL: Delimiter (default value if blank = '&')"
```

Next we get a whole lot of codes I haven't yet looked up that obviously don't have a great influence on this process. I suspect they pertain to the variable definitions for data coming from the data source. Since this process doesn't use a source, it makes sense that it would be blank.

```text
577,0
578,0
579,0
580,0
581,0
582,0
603,0
```

Now we get into the TI code itself. This section defines the prolog. Most of it is just Bedrock boilerplate so I'm not showing the whole thing. You'll have to trust me when I tell you it's 133 lines in total.

```text
572,133
#Region CallThisProcess
# A snippet of code provided as an example how to call this process should the developer be working on a system without access to an editor with auto-complete.
If( 1 = 0 );
    ExecuteProcess( '}bedrock.cube.rule.processfeeders', 'pLogOutput', pLogOutput,
      'pStrictErrorHandling', pStrictErrorHandling,
	    'pCube', '', 'pDelim', '&'
    );
EndIf;
#EndRegion CallThisProcess

#****Begin: Generated Statements***
#****End: Generated Statements****

################################################################################################# ####################
##~~Join the bedrock TM1 community on GitHub https://github.com/cubewise-code/bedrock Ver 4.0~~##
################################################################################################# 

...
```

The metadata and data tabs are unsurprisingly empty, as again, there's no data source for this process.

```
573,3

#****Begin: Generated Statements***
#****End: Generated Statements****
574,5

#****Begin: Generated Statements***
#****End: Generated Statements****
```

While the epilog is again mostly boilerplate: 

```
575,24

#****Begin: Generated Statements***
#****End: Generated Statements****

...

### End Epilog ###
```

There's still a bit at the end to cut through, but at least that's an overview of how it all works.

```text
576,CubeAction=1511DataAction=1503CubeLogChanges=0
930,0
638,1
804,0
1217,1
900,
901,
902,
938,0
937,
936,
935,
934,
932,0
933,0
903,
906,
929,
907,
908,
904,0
905,0
909,0
911,
912,
913,
914,
915,
916,
917,0
918,1
919,0
920,50000
921,""
922,""
923,0
924,""
925,""
926,""
927,""
```

I'm going to check whether the list of codes is consistent across all pro files, using Bedrock as a test bed. Parsing the file shouldn't be that hard but analysing the codes could prove a bit annoying, let's see if I find time but it seems a nice little feature.