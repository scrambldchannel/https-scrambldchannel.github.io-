Title: Creating a TI process from a .pro file using TM1py
Date: 2020-10-04 11:01
Category: tm1
Tags: tm1, cognos, ibm, ti
slug: hot-promotion-of-tm1-pro-file
Authors: Alexander
featured_image: images/pro_file.jpg
Summary: Ever wondered what's going on in your .pro files? I did so I tried to take one apart with Python and re-create it with TM1py...

An [issue](https://github.com/cubewise-code/tm1py/issues/383) raised over at the TM1py project asked for a feature to add hot promotion of TM1 processes saved as pro files. The API allows creation of TI processes and TM1py provides some useful wrapper functions that can achieve this. However, the fiddly part was parsing a pro file to get the relevant information out to allow us to create an instance of the TM1py Process object.

### Exploring the pro file format

Pro files are saved as text so are human readable. As well as containing the code defined in the different tabs (prolog, metadata, data and epilog) the file contains metadata providing additional details about the file. For this example, I'm taking apart the [process to refresh feeders](https://github.com/cubewise-code/bedrock/blob/master/main/%7Dbedrock.cube.rule.processfeeders.pro) from the [Bedrock project](https://github.com/cubewise-code/bedrock).

The process is pretty straightforward, it takes a cube, or list of cubes, and a few other general parameters and does what it says on the tin - i.e. each specified cube will have its feeders refreshed. This is what it looks like on file:

```text
601,100
602,"}bedrock.cube.rule.processfeeders"
```

These first couple of lines specify the version and the name of the process. How do I know this? Wim pointed me in the direction of the codes in the TM1 docs, notably the file at ```tm1_64/TM1JavaApiDocs/constant-values.html``` which contains a list of constants in the docs for the old Java API. It turns out that these correspond to the codes that start each line in the pro file. I've scraped the codes and saved them [here](https://gist.github.com/scrambldchannel/9955cb731f80616c706f2d5a81b82c2a).

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

### Multiline codes

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

### Multiline codes with key value pairs

We then see the default values and the hint the TI process editor provides. Note it gets a bit fiddly. Instead of just the value, the lines are prefixed by name of the parameter. So these lines need to be handled a bit differently when being parsed. The default values and prompts for a process are optional. The Bedrock processes are pretty thorough hence I think both prompts and default values are set for each process. I wasn't sure this would always be the case so I created a fresh process, with all the different permutations of parameter settings. I turned out there's always the full list of parameters and they're always in the same order. So the first field seems a bit redundant.

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

### The actual TI code

Now we get into the TI code itself. It is defined like any other multiline option. This section defines the prolog. Most of it is just Bedrock boilerplate so I'm not showing the whole thing. You'll have to trust me when I tell you it's 133 lines in total.

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

```text
573,3

#****Begin: Generated Statements***
#****End: Generated Statements****
574,5

#****Begin: Generated Statements***
#****End: Generated Statements****
```

While the epilog is again mostly boilerplate.

```text
575,24

#****Begin: Generated Statements***
#****End: Generated Statements****

...

### End Epilog ###
```

### Wait, there's more

There's still a bit at the end to cut through, but at least that's an overview of how it all works. Option ```576``` a bit more complicated but everything else seems pretty straightforward. Looking through the names of the codes, there are lots I think represent things that can't be created through the endpoint that allows a process to be created. For example, ```900``` to ```927``` all seem to pertain to settings for the SAP connector. 

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

### Parsing it in Python

I had a go at parsing a pro file. This is rough and a bit buggy but I got a PoC working. I tinkered around with this code and managed to identify all the multiline codes in all the Bedrock processes but there may be some more lurking, particularly in the codes that cover connection configurations which aren't covered in Bedrock.

This first part reads the file and creates a dictionary of the codes and values:

```python
# location of pro file to load

file = "}bedrock.cube.rule.processfeeders.pro"

# codes to treat differently
multiline_codes = ['560', '561', '572', '573', '574', '575', '577', '578', '579', '580', '581', '582', '566']
multiline_codes_with_key = ['590','637']

with open(file, encoding='utf-8-sig') as f:

    process_dict = {}
    in_multiline = False
    in_multiline_with_key = False
    code = ''

    for line in f:
        if in_multiline:
            process_dict[code].append(line.replace('"', '').rstrip())
            lines = lines - 1
            if lines == 0:
                in_multiline = False
        elif in_multiline_with_key:
            fields = line.split(',')
            process_dict[code].append(fields[1].replace('"', '').rstrip())
            lines = lines - 1
            if lines == 0:
                in_multiline_with_key = False
        else:
            fields = line.split(',')
            code = fields[0]
            if code in multiline_codes:
                lines = int(fields[1])
                if lines > 0:
                    in_multiline = True
                process_dict[code] = []
            elif code in multiline_codes_with_key:
                lines = int(fields[1])
                if lines > 0:
                    in_multiline_with_key = True
                process_dict[code] = []
            else:
                process_dict[code] = ''.join(fields[1:]).replace('"', '').rstrip()
```

### Create an instance of the Process class

From there, it's possible to create an instance of a TM1py ```Process``` object from the information grabbed for each process. I found it easier to use the built-in methods to create the parameters and variables. 

```python
import TM1py

my_new_process = TM1py.Objects.Process(
    name=process_dict['602'],
    has_security_access=(True if process_dict['1217'] == 'True' else False),
    ui_data=process_dict['576'],
    prolog_procedure="\n".join(process_dict['572']),
    metadata_procedure="\n".join(process_dict['573']),
    data_procedure="\n".join(process_dict['574']),
    epilog_procedure="\n".join(process_dict['575']),
    datasource_type='None',
    datasource_ascii_decimal_separator=process_dict['588'],
    datasource_ascii_delimiter_char=process_dict['567'],
    datasource_ascii_delimiter_type='Character', # doesn't seem to have a corresponding code
    datasource_ascii_header_records=process_dict['569'],
    datasource_ascii_quote_character=process_dict['568'],
    datasource_ascii_thousand_separator=process_dict['589'],
    datasource_data_source_name_for_client=process_dict['585'],
    datasource_data_source_name_for_server=process_dict['586'],
    datasource_password=process_dict['565'],
    datasource_user_name=process_dict['564'],
    datasource_query=process_dict['566'],
    datasource_uses_unicode=process_dict['559'],
    datasource_view=process_dict['570'],
    datasource_subset=process_dict['571']
)

# now add parameters and variables

for index, item in enumerate(process_dict['560']):

    if process_dict['561'][index] == "2":
        parameter_type = "String"
        value = process_dict['590'][index]
    else:
        parameter_type = "Numeric"
        if process_dict['590'][index] == "":
            value = 0
        else:
            value = float(process_dict['590'][index])

    my_new_process.add_parameter(
        name=item,
        prompt=process_dict['637'][index],
        value=value,
        parameter_type=parameter_type
    )

for index, item in enumerate(process_dict['577']):

    variable_type = "String" if process_dict['578'][index] == "2" else "Numeric"        

    my_new_process.add_variable(
        name=item,
        variable_type=variable_type
    )    
```

### Add to server

With a valid process object we should be able to create the process on the server:

```python
import pathlib
import configparser

# establish connection / how you 
config = configparser.ConfigParser()
config.read('config.ini')

with TM1py.Services.TM1Service(**config['tm1srv01']) as tm1:

    if tm1.processes.exists(my_new_process.name):
        tm1.processes.delete(my_new_process.name)

    response = tm1.processes.create(my_new_process)

    # check status of response
    print(response.status_code)
```

This works smoothly and the process can now be found on the server:

<img style="padding-top: 10px; padding-bottom: 10px;" src="/images/process_now_appears_on_server.png">

The parameters are intact and seem to have the right types and defaults:

<img style="padding-top: 10px; padding-bottom: 10px;" src="/images/process_seems_intact.png">

### Testing and known issues

I did notice a couple of issues once I'd done a diff of the source file and the pro file created afterwards. A few differences were down to whitespace being stripped in the new version of the file. There were a couple of bugs though... 

Multiline parameters containing commas get truncated:

<img style="padding-top: 10px; padding-bottom: 10px;" src="/images/pro_diff_comma_issue.png">

More seriously, in this code block, my pretty naive parsing hasn't handled nested quotes. A robust solution would probably require using regular expressions for parsing:

<img style="padding-top: 10px; padding-bottom: 10px;" src="/images/pro_diff_quote_issue.png">

Note, the process ran successfully for a single cube but does fail when trying to use wildcards with the following showing up in the logs indicating the MDX isn't parsing (which makes sense):

```text
7292   [2]   ERROR   2020-10-04 16:05:58.936   TM1.Mdx.Interface   Syntax error at or near: ')}', character position 50
```

So far, as a PoC, it shows that it can be done but needs some tweaking. Not every detail in the file is used to construct the new process so it's very likely that some legacy processes can't be created this way such as those created with the wizard or using the SAP connector. There are probably better solutions though, such as using TM1py to grab a process on a development server and push it to production. 

I was able to import all the latest Bedrock pro files and create them on the server but haven't actually tested them in depth. I also haven't tested it on with processes with ODBC data sources and think they might be problematic as I'm assuming there might be some more multiline options I haven't handled properly. So I wouldn't necessrily recommend it, but it's possible.