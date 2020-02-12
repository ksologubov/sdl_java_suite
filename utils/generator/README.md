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
* `@since` should be present, if the `"since"` attribute exists, and `[since_version]` is the `Major.Minor.Patch` formatted value of this attribute.
* `@see` shows the custom reference in `[see_reference]`, if it's defined in the custom mapping.

The set of `<element>` should be mapped to the set of Enum constants. Based on the `<element>` attributes, constants could be with or without fields.

The following list are general rules for constant names and its fields:
1. The `"name"` attribute of `<element>` is the default name of the constant.
1. Uses of the "sync" prefix shall be replaced with "sdl" (where it would not break functionality). E.g. `SyncMsgVersion -> SdlMsgVersion`. This applies to member variables and their accessors. The key used when creating the RPC message JSON should match that of the RPC Spec.

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
* `@since` should be present, if the `"since"` attribute exists, and `[since_version]` is the `Major.Minor.Patch` formatted value of this attribute.
* `@see` shows the custom reference in `[see_reference]`, if it's defined in the custom mapping.

The constant definition should have the `@Deprecated` decorator if the `"deprecated"` attribute exists and has the value.

### Constants without fields:

This type of enums doesn't require constructor and requires additional method `valueForString` to be defined. It should return the Enum constant based on its string name, or `null` if the constant is not found.
```java
    /**
     * Convert String to [enum_name]
     *
     * @param value String
     * @return [enum_name]
     */
    public static [enum_name] valueForString(String value) {
        try {
            return valueOf(value);
        } catch (Exception e) {
            return null;
        }
    }
```
Where `[enum_name]` is the `"name"` attribute of `<enum>`

Example:

XML:
```xml
    <enum name="AppHMIType" since="2.0">
        <description>Enumeration listing possible app types.</description>
        <element name="DEFAULT" />
        <element name="COMMUNICATION" />
        <element name="MEDIA" />
        <element name="MESSAGING" />
        <element name="NAVIGATION" />
        <element name="INFORMATION" />
        <element name="SOCIAL" />
        <element name="BACKGROUND_PROCESS" />
        <element name="TESTING" />
        <element name="SYSTEM" />
        <element name="PROJECTION" since="4.5" />
        <element name="REMOTE_CONTROL" since="4.5" />
    </enum>
```

Output:
```java
/*
 * Copyright (c) 2017 - 2020, SmartDeviceLink Consortium, Inc.
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
package com.smartdevicelink.proxy.rpc.enums;
 
/**
 * Enumeration listing possible app types.
 *
 *
 * @since SmartDeviceLink 2.0.0
 */
public enum AppHMIType {
    /**
     * The App will have default rights.
     */
    DEFAULT,
    /**
     * Communication type of App
     */
    COMMUNICATION,
    /**
     * App dealing with Media
     */
    MEDIA,
    /**
     * Messaging App
     */
    MESSAGING,
    /**
     * Navigation App
     */
    NAVIGATION,
    /**
     * Information App
     */
    INFORMATION,
    /**
     * App dealing with social media
     */
    SOCIAL,
    BACKGROUND_PROCESS,
    /**
     * App only for Testing purposes
     */
    TESTING,
    /**
     * System App
     */
    SYSTEM,
    /**
     * Custom App Interfaces
     *
     * @since SmartDeviceLink 4.5.0
     */
    PROJECTION,
    /**
     * @since SmartDeviceLink 4.5.0
     */
    REMOTE_CONTROL;

    /**
     * Convert String to AppHMIType
     *
     * @param value String
     * @return AppHMIType
     */
    public static AppHMIType valueForString(String value) {
        try {
            return valueOf(value);
        } catch (Exception e) {
            return null;
        }
    }
}
```
### Constants with fields

This type of enums is divided into 3 additional types:
* field based on `"internal_name"` and `"name"` attributes of `<element>`
* field based on `"value"` attribute of `<element>`
* Special `FunctionID` Enum class

#### Constants with field based on `"internal_name"` and `"name"` attributes

In case if the `"internal_name"` attribute exists, this should be used for the constant name and the `"name"` attribute should be passed as a `String` field into Enum constant.

The `"internal_name"` attribute should be normalized by following rules:
* If it starts with the same prefix as `<enum>` name, this prefix should be removed.
* After the prefix removal:
    * if the value starts from digit, the leading `_` (underscore) separator should be added.
    * if the value starts with `_` (underscore) separator and the next character is a letter of alphabet, the leading `_` (underscore) character should be removed.

Constant definition:
```java
    [internal_name]("[name]")
```
Where `[internal_name]` is the normalized `"internal_name"` attribute of `<element>`, `[name]` is the `"name"` attribute.

Private field:
```java
    private final String INTERNAL_NAME;
```

The private constructor should be defined to accept the value from the constant and and set the private field.
```java
    private [enum_name](String internalName) {
        this.INTERNAL_NAME = internalName;
    }
```
Where `[enum_name]` is the `"name"` attribute of `<enum>`.

The `toString` 1method should be overridden to return the private field instead of the constant name.
```java
    @Override
    public String toString() {
        return INTERNAL_NAME;
    }
```

The additional `valueForString` should be defined. It should return the Enum constant based on the private field above, or `null` if the constant is not found.
```java
    public static [enum_name] valueForString(String value) {
        if (value == null) {
            return null;
        }

        for ([enum_name] anEnum : EnumSet.allOf([enum_name].class)) {
            if (anEnum.toString().equals(value)) {
                return anEnum;
            }
        }
        return null;
    }
```
Where `[enum_name]` is the `"name"` attribute of `<enum>`.

The `valueForString` method requires the import of `EnumSet` collection:
```java
import java.util.EnumSet;
```

Full example:

XML:
```xml
    <enum name="Dimension" since="2.0">
        <description>The supported dimensions of the GPS</description>
        <element name="NO_FIX" internal_name="Dimension_NO_FIX">
            <description>No GPS at all</description>
        </element>
        <element name="2D" internal_name="Dimension_2D">
            <description>Longitude and latitude</description>
        </element>
        <element name="3D" internal_name="Dimension_3D">
            <description>Longitude and latitude and altitude</description>
        </element>
    </enum>
```

Output:
```java
/*
 * Copyright (c) 2017 - 2020, SmartDeviceLink Consortium, Inc.
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
package com.smartdevicelink.proxy.rpc.enums;

import java.util.EnumSet;

/**
 * The supported dimensions of the GPS
 *
 *
 * @since SmartDeviceLink 2.0.0
 */
public enum Dimension {
    /**
     * Longitude and latitude
     */
    _2D("2D"),
    /**
     * Longitude and latitude and altitude
     */
    _3D("3D"),
    /**
     * No GPS at all
     */
    NO_FIX("NO_FIX");

    private final String INTERNAL_NAME;

    private Dimension(String internalName) {
        this.INTERNAL_NAME = internalName;
    }

    public static Dimension valueForString(String value) {
        if (value == null) {
            return null;
        }

        for (Dimension anEnum : EnumSet.allOf(Dimension.class)) {
            if (anEnum.toString().equals(value)) {
                return anEnum;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        return INTERNAL_NAME;
    }
}
```

#### Constants with field based on `"value"` attribute

In case if the `"value"` attribute exists, this attribute should be passed as the `int` constant field.

Constant definition:
```java
    [name]([value])
```
Where `[name]` is the `"name"` attribute of `<element>`, `[value]` is the `"value"` attribute.

Private field:
```java
    final int VALUE;
```

The private constructor should be defined to accept the value from the constant and and set the private field.
```java
    private [enum_name](int value) {
        this.VALUE = value;
    }
```
Where `[enum_name]` is the `"name"` attribute of `<enum>`.

The `getValue` 1method should be defined to return the private field value.
```java
    public int getValue(){
        return VALUE;
    }
```

The additional `valueForInt` should be defined. It should return the Enum constant based on the private field above, or `null` if the constant is not found.
```java
    public static [enum_name] valueForString(int value) {
        for ([enum_name] anEnum : EnumSet.allOf([enum_name].class)) {
            if (anEnum.toString().equals(value)) {
                return anEnum;
            }
        }
        return null;
    }
```
Where `[enum_name]` is the `"name"` attribute of `<enum>`.

The `valueForInt` method requires the import of `EnumSet` collection:
```java
import java.util.EnumSet;
```

Full example:

XML:
```xml
    <enum name="PredefinedWindows" since="6.0">
        <element name="DEFAULT_WINDOW" value="0">
            <description>The default window is a main window pre-created on behalf of the app.</description>
        </element>
        <element name="PRIMARY_WIDGET" value="1">
            <description>The primary widget of the app.</description>
        </element>
    </enum>
```

Output:
```java
/*
 * Copyright (c) 2017 - 2020, SmartDeviceLink Consortium, Inc.
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
package com.smartdevicelink.proxy.rpc.enums;

import java.util.EnumSet;

/**
 *
 * @since SmartDeviceLink 6.0.0
 */
public enum PredefinedWindows {
    /**
     * The default window is a main window pre-created on behalf of the app.
     */
    DEFAULT_WINDOW(0),
    /**
     * The primary widget of the app.
     */
    PRIMARY_WIDGET(1);

    final int VALUE;
    /**
     * Private constructor
     */
    PredefinedWindows (int value) {
        this.VALUE = value;
    }

    public static PredefinedWindows valueForInt(int value) {
        for (PredefinedWindows anEnum : EnumSet.allOf(PredefinedWindows.class)) {
            if (anEnum.getValue() == value) {
                return anEnum;
            }
        }
        return null;
    }

    public int getValue(){
        return VALUE;
    }
}
```

### `FunctionID` Enum class

Additionally to general rules for constant names and its fields there are some rules for the `FunctionID` Enum class:
  1. Uses of the `"name"` attribute shall be normalized by the removal of the ID suffix, e.g. `RegisterAppInterfaceID -> RegisterAppInterface`. 
  1. The constant name should be `SCREAMING_SNIKE_CASE` formatted;
  1. The constant has 2 fields, the first is the `int` value of the `"value"` attribute and the second is the `String` value of normalized `"name"` attribute.

Constant definition:
```java
    [constant_name]([value], "[name]")
```
Where `[constant_name]` is the normalized and `SCREAMING_SNIKE_CASE` formatted `"name"` attribute of `<element>`, `[name]` is the just normalized `"name"` attribute, `[value]` is the `"value"` attribute.

Private fields:
```java
    private final int ID;
    private final String JSON_NAME;
```

The private constructor should be defined to accept the value and name from the constant and and set the private fields.
```java
    private FunctionID(int id, String jsonName) {
        this.ID = id;
        this.JSON_NAME = jsonName;
    }
```

The next custom imports, fields and methods are required for `FunctionID` Enum class:

Imports:
```java
import java.util.EnumSet;
import java.util.Map.Entry;
import java.util.Iterator;
import java.util.HashMap;
```

Fields:
```java
    // MOCKED FUNCTIONS (NOT SENT FROM HEAD-UNIT)
    ON_LOCK_SCREEN_STATUS(-1, "OnLockScreenStatus"),
    ON_SDL_CHOICE_CHOSEN(-1, "OnSdlChoiceChosen"),
    ON_STREAM_RPC(-1, "OnStreamRPC"),
    STREAM_RPC(-1, "StreamRPC");

    public static final int INVALID_ID = -1;
```

Methods:
```java
    public int getId(){
        return this.ID;
    }

    @Override
    public String toString() {
        return this.JSON_NAME;
    }

    private static void initFunctionMap() {
        functionMap = new HashMap<String, Integer>(values().length);

        for(FunctionID value : EnumSet.allOf(FunctionID.class)) {
            functionMap.put(value.toString(), value.getId());
        }
    }

    public static String getFunctionName(int i) {
        if(functionMap == null) {
            initFunctionMap();
        }

        Iterator<Entry<String, Integer>> iterator = functionMap.entrySet().iterator();
        while(iterator.hasNext()) {
            Entry<String, Integer> thisEntry = iterator.next();
            if(Integer.valueOf(i).equals(thisEntry.getValue())) {
                return thisEntry.getKey();
            }
        }

        return null;
    }

    public static int getFunctionId(String functionName) {
        if(functionMap == null) {
            initFunctionMap();
        }

        Integer result = functionMap.get(functionName);
        return ( result == null ) ? INVALID_ID : result;
    }

    /**
     * This method gives the corresponding FunctionID enum value for a string RPC
     *
     * @param name String value represents the name of the RPC
     * @return FunctionID represents the equivalent enum value for the provided string
     */
    public static FunctionID getEnumForString(String name) {
        for(FunctionID value : EnumSet.allOf(FunctionID.class)) {
            if(value.JSON_NAME.equals(name)){
                return value;
            }
        }
        return null;
    }
```



Full example:

XML:
```xml
<enum name="FunctionID" internal_scope="base" since="1.0">
    <description>Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes enumeration starts at value 0.</description>
    <element name="RESERVED" value="0" since="1.0" />
    <element name="RegisterAppInterfaceID" value="1" hexvalue="1" since="1.0" />
    <element name="SliderID" value="26" hexvalue="1A" since="2.0" />
</enum>
```

Output:
```java
/*
 * Copyright (c) 2017 - 2020, SmartDeviceLink Consortium, Inc.
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
package com.smartdevicelink.protocol.enums;

import java.util.EnumSet;
import java.util.Map.Entry;
import java.util.Iterator;
import java.util.HashMap;

/**
 * Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes enumeration starts at
 * value 0.
 *
 *
 * @since SmartDeviceLink 1.0.0
 */
public enum FunctionID {
    /**
     * @since SmartDeviceLink 1.0.0
     */
    RESERVED(0, "RESERVED"),
    /**
     * @since SmartDeviceLink 1.0.0
     */
    REGISTER_APP_INTERFACE(1, "RegisterAppInterface");
    /**
     * @since SmartDeviceLink 2.0.0
     */
    SLIDER(26, "Slider"),

    // MOCKED FUNCTIONS (NOT SENT FROM HEAD-UNIT)
    ON_LOCK_SCREEN_STATUS(-1, "OnLockScreenStatus"),
    ON_SDL_CHOICE_CHOSEN(-1, "OnSdlChoiceChosen"),
    ON_STREAM_RPC(-1, "OnStreamRPC"),
    STREAM_RPC(-1, "StreamRPC");

    public static final int                 INVALID_ID = -1;

    private static HashMap<String, Integer> functionMap;

    private final int                       ID;
    private final String                    JSON_NAME;

    private FunctionID(int id, String jsonName) {
        this.ID = id;
        this.JSON_NAME = jsonName;
    }

    public int getId(){
        return this.ID;
    }

    @Override
    public String toString() {
        return this.JSON_NAME;
    }

    private static void initFunctionMap() {
        functionMap = new HashMap<String, Integer>(values().length);

        for(FunctionID value : EnumSet.allOf(FunctionID.class)) {
            functionMap.put(value.toString(), value.getId());
        }
    }

    public static String getFunctionName(int i) {
        if(functionMap == null) {
            initFunctionMap();
        }

        Iterator<Entry<String, Integer>> iterator = functionMap.entrySet().iterator();
        while(iterator.hasNext()) {
            Entry<String, Integer> thisEntry = iterator.next();
            if(Integer.valueOf(i).equals(thisEntry.getValue())) {
                return thisEntry.getKey();
            }
        }

        return null;
    }

    public static int getFunctionId(String functionName) {
        if(functionMap == null) {
            initFunctionMap();
        }

        Integer result = functionMap.get(functionName);
        return ( result == null ) ? INVALID_ID : result;
    }

    /**
     * This method gives the corresponding FunctionID enum value for a string RPC
     *
     * @param name String value represents the name of the RPC
     * @return FunctionID represents the equivalent enum value for the provided string
     */
    public static FunctionID getEnumForString(String name) {
        for(FunctionID value : EnumSet.allOf(FunctionID.class)) {
            if(value.JSON_NAME.equals(name)){
                return value;
            }
        }
        return null;
    }
}
```


## `<struct>`

## `<function>`
