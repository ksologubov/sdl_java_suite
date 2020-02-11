# Proxy Library RPC Generator

## Overview

This script provides the possibility to auto-generate Java code based on a given SDL MOBILE_API XML specification.

## Requirements

The script requires Python 3.5 pre-installed in the system. This is the minimal Python 3 version that has not reached the end-of-life (https://devguide.python.org/devcycle/#end-of-life-branches).

Some required libraries are described in `requirements.txt` and should be pre-installed by the command:
```shell script
pip install -r requirements.txt
```
Please also make sure before usage the 'utils/generator/rpc_spec' Git submodule is successfully initialized, because the script uses the XML parser provided there.

## Usage
```shell script
usage: generator.py [-h] [-v] [-xml SOURCE_XML] [-xsd SOURCE_XSD]
                    [-d OUTPUT_DIRECTORY] [-t [TEMPLATES_DIRECTORY]]
                    [-r REGEX_PATTERN] [--verbose] [-e] [-s] [-m] [-y] [-n]

Proxy Library RPC Generator

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the version and exit
  -xml SOURCE_XML, --source-xml SOURCE_XML, --input-file SOURCE_XML
                        should point to MOBILE_API.xml
  -xsd SOURCE_XSD, --source-xsd SOURCE_XSD
  -d OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        define the place where the generated output should be
                        placed
  -t [TEMPLATES_DIRECTORY], --templates-directory [TEMPLATES_DIRECTORY]
                        path to directory with templates
  -r REGEX_PATTERN, --regex-pattern REGEX_PATTERN
                        only elements matched with defined regex pattern will
                        be parsed and generated
  --verbose             display additional details like logs etc
  -e, --enums           only specified elements will be generated, if present
  -s, --structs         only specified elements will be generated, if present
  -m, -f, --functions   only specified elements will be generated, if present
  -y, --overwrite       force overwriting of existing files in output
                        directory, ignore confirmation message
  -n, --skip            skip overwriting of existing files in output
                        directory, ignore confirmation message
```

# Java Transformation rules

## Overview
These are the general transformation rules for RPC classes of SDL Java Suite Library. The description of base classes, already included in the library, is not provided here, for details please view the source code. 

The JavaDoc is used for inline documentation of generated code. All non-XML values should follow Contributing to SDL Projects [CONTRIBUTING.md](ttps://github.com/smartdevicelink/sdl_android/blob/master/.github/CONTRIBUTING.md)

These rules based on the current `develop` branch state (commit:`7e6a16c027bcdd0fb523a9993dc59b0171167aea`) of [`smartdevicelink/sdl_java_suite`](https://github.com/smartdevicelink/sdl_java_suite) repository.

## Output Directory Structure and Package definitions

The generator script creates corresponding RPC classes for `<enum>`, `<struct>` and `<function>` elements of `MOBILE_API.xml`.
According to existing structure of Java Suite the output directory will contain following folders and files:

* com
    * smartdevicelink
        * protocol
            * enums
                * FunctionID.java
    * proxy
        * rpc
            * enums
                * `[- all <enum> classes except FunctionID and MessageType -]`
            * `[- all <struct> classes -]`
            * `[- all <function> classes -]`

Each Enum class should be stored as a single script file in the folder named `com/smartdevicelink/rpc/enums` and the name of the script file should be equal to the value from the `"name"` attribute of `<enum>` followed by the extension `.java`.

Example:
```shell script
# <enum name="ImageType" />
com/smartdevicelink/proxy/rpc/enums/ImageType.java
```

Each Enum class should include the package definition:
```java
package com.smartdevicelink.proxy.rpc.enums;
``` 

The only exception is the `<enum>` named `FunctionID`. This class should be stored in `com/smartdevicelink/protocol/enums` folder, as defined in the directory structure above.

The package definition for `FunctionID` class also is different:
```java
package com.smartdevicelink.protocol.enums;
``` 

Each Struct or Function class should be stored as a single script file in the folder named `com/smartdevicelink/proxy/rpc` and the name of the script file should be equal to the value from the `"name"` attribute of `<struct>` or `<function>` (followed by additional suffix `Response` if the `"messagetype"` attribute is set to `response`) followed by the extension `.java`.

Example:
```shell script
# <struct name="VehicleDataResult" />
com/smartdevicelink/proxy/rpc/VehicleDataResult.java

# <function name="AddCommand" messagetype="request" />
com/smartdevicelink/proxy/rpc/AddCommand.java
# <function name="AddCommand" messagetype="response" />
com/smartdevicelink/proxy/rpc/AddCommandResponse.java
# <function name="OnLanguageChange" messagetype="notification" />
com/smartdevicelink/proxy/rpc/OnLanguageChange.java
```

The package definition for Struct or Function classes is:
```java
package com.smartdevicelink.proxy.rpc;
``` 

## The License Header
All files should start from the comment with the license information.

```java
/*
 * Copyright (c) 2017 - [year], SmartDeviceLink Consortium, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following
 * disclaimer in the documentation and/or other materials provided with the
 * distribution.
 *
 * Neither the name of the SmartDeviceLink Consortium Inc. nor the names of
 * its contributors may be used to endorse or promote products derived
 * from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
```
Where `[year]` in the copyright line is the current year.

## `<enum>`
The name of the class is the value from the `"name"` attribute of `<enum>`.

The class should have the next JavaDoc comment:
```java
/**
 * [description]
 *
 * @deprecated
 * @since SmartDeviceLink [since_version]
 * @see [see_reference]
 */
```
Where:
* `[description]` is `<description>` of the current `<enum>`, if exists.
* `@deprecated` indicates the deprecation state if the `"deprecated"` attribute exists and has the value.
* `@since` should be present, if the `"since"` attribute exists, and `[since_version]` is the value of this attribute.
* `@see` shows the custom reference in `[see_reference]`, if it's defined in the custom mapping.

The set of `<element>` should be mapped to the set of Enum constants. Based on the `<element>` attributes, constants could be with or without fields.

The following list are general rules for constant names and its fields:
1. The `"name"` attribute of `<element>` is the default name of the constant.
2. In case if the `"internal_name"` attribute exists, this should be used for the constant name and the `"name"` attribute should be passed as a field into Enum constant.
3. The `"internal_name"` attribute should be normalized by following rules:
    * If it starts with the same prefix as `<enum>` name, this prefix should be removed.
    * After the prefix removal, if the value starts with `_` (underscore) separator and the next character is a letter of alphabet, the leading `_` (underscore) character should be removed.
4. In case if the `"value"` attribute exists, this attribute should be passed as the constant field.
5. Uses of the "sync" prefix shall be replaced with "sdl" (where it would not break functionality). E.g. `SyncMsgVersion -> SdlMsgVersion`. This applies to member variables and their accessors. The key used when creating the RPC message JSON should match that of the RPC Spec.

The exception is the `<enum>` named `FunctionID`. Additionally to rules above:
  1. Uses of the `"name"` attribute shall be normalized by the removal of the ID suffix, e.g. `RegisterAppInterfaceID -> RegisterAppInterface`. 
  2. The constant name should be `SCREAMING_SNIKE_CASE` formatted and has 2 fields, the first is the `"value"` attribute and the second is the normalized `"name"` attribute.

The constant definition could have the next JavaDoc comment:
```java
/**
 * [description]
 *
 * @since SmartDeviceLink [since_version]
 * @see [see_reference]
 */
```
Where:
* `[description]` is `<description>` of the current `<element>`, if exists.
* `@since` should be present, if the `"since"` attribute exists, and `[since_version]` is the value of this attribute.
* `@see` shows the custom reference in `[see_reference]`, if it's defined in the custom mapping.

The constant definition should have the `@deprecated` decorator if the `"deprecated"` attribute exists and has the value.

Constants with fields require private constructor to be defined in the Enum class.

### Examples:
#### Constants without fields:
```java
    /**
     * The button name for the physical Play/Pause toggle that can be used by media apps.
     *
     * @since SmartDeviceLink 5.0.0
     */
    PLAY_PAUSE,
    SEEKLEFT,
    SEEKRIGHT,
    TUNEUP;
```

#### Constants with field based on internal_name and name:
```java
    /**
     * Audio sample is 8 bits wide, unsigned.
     */
    _8_BIT("8_BIT"),
    /**
     * Audio sample is 16 bits wide, signed, and in little endian.
     */
    _16_BIT("16_BIT");

    private final String INTERNAL_NAME;

    private BitsPerSample(String internalName) {
        this.INTERNAL_NAME = internalName;
    }
```

#### Constants with field based on value:
```java
    /**
     * The default window is a main window pre-created on behalf of the app.
     */
    DEFAULT_WINDOW(0),
    /**
     * The primary widget of the app.
     */
    PRIMARY_WIDGET(1);

    final int VALUE;

    private PredefinedWindows (int value) {
        this.VALUE = value;
    }
```

#### FunctionID constants with 2 fields:
```java
    /**
     * @since SmartDeviceLink 1.0.0
     */
    REGISTER_APP_INTERFACE(1, "RegisterAppInterface");

    private final int                       ID;
    private final String                    JSON_NAME;

    private FunctionID(int id, String jsonName) {
        this.ID = id;
        this.JSON_NAME = jsonName;
    }
```


## `<struct>`

## `<function>`
