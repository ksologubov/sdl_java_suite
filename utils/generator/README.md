JavaScript ES6 Transformation rules
Overview

This documents contains the general transformation rules for RPC classes of SDL JavaScript Suite Library. The description of base classes, already included in the library, is not provided here, for details please view the source code.

The JSDoc is used for inline documentation of generated code. All non-XML values should follow Architecture & Contribution Guidelines (GUIDELINES.md)

These rules based on the current develop branch state (commit:c5b3b448e008dadc9a5b66addde17633ac957700) of smartdevicelink/sdl_javascript_suite repository.
The License Header

All files should start from the comment with the license information.

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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

<enum>

All Enum classes should be stored in the folder with name enums and the name of the script is the value from the "name" attribute of <enum> following by the extension .js.

Example:

enums/ImageType.js

The script should import the base Enum class and the produced class should extend it. The name of the class is the value from the "name" attribute of <enum>. The constructor has no params and should call super().

The class should have the next JSDoc comment:

/**
 * [decription]
 * @typedef {Enum} [enum_name]
 * @property {Object} _MAP
 */

Where [description] is <description> of the current <enum>, if exists, and [enum_name] is the value of the "name" attribute. The constructor should have the next JSDoc comment:

/**
 * @constructor
 */

Example:

import { Enum } from '_path_to_base_classes_/Enum.js';

/**
 * Contains information about the type of image.
 * @typedef {Enum} ImageType
 * @property {Object} _MAP
 */
class ImageType extends Enum {

    /**
     * @constructor
     */
    constructor() {
        super();
    }
}

The set of <element> should be mapped to the frozen object and put into the private static property _MAP.

Here are some general rules for keys and values of this object:

    The "name" attribute is the base value for both the key and the value of the mapped object.
    In case if the "internal_name" attribute exists, this should be used for the key instead of the "name" attribute.
    In case if the "value" attribute exists, this attribute should be used for the value instead of the "name" attribute.
    In case if the "hexvalue" attribute exists, this attribute should be used for the value instead of the "value" and "name" attributes.

According to ES6 standard, static (class-side) data properties and prototype data properties must be defined outside of the ClassBody declaration.

Example:

ImageType._MAP = Object.freeze({
    'STATIC': 'STATIC',
    'DYNAMIC': 'DYNAMIC',
});

For each <element> the static getter method should be defined in the class. The name of the getter is the "internal_name" or "name" attribute value, the same as _MAP keys. The returned value is the value from the frozen object described above taken by the corresponding key.

The getter should have the next JSDoc comment:

/**
 * [decription]
 * @return {[enum_type]}
 */

Where [description] is <description> of the current <element>, if exists, and [enum_type] is the one of String or Number.

Example:

/**
 * @return {String}
 */
static get STATIC() {
    return ImageType._MAP.STATIC;
}

/**
 * @return {String}
 */
static get DYNAMIC() {
    return ImageType._MAP.DYNAMIC;
}

The base Enum class requires children to have the own implementation of the valueForString method with one parameter named "value". This implementation should return the result of valueForStringInternal method where the first parameter is the parameter of the valueForString method and the second is the frozen object described above. This method should have the next JSDoc comment:

/**
 * Confirms whether the value passed in exists in the Enums of this class
 * @param {String} value
 * @return {null|[enum_type]} - Returns null if the enum value doesn't exist
 */

Where [enum_type] is the one of String or Number.

Example:

/**
 * Confirms whether the value passed in exists in the Enums of this class
 * @param {String} value
 * @return {null|String} - Returns null if the enum value doesn't exist
 */
static valueForString(value) {
    return ImageType.valueForStringInternal(value, ImageType.MAP);
}

After the _MAP definition, the script should export the produced class.

Example:

export { ImageType };

Below are examples of <enum> with different <element> attributes
Example with only "name" attribute:

XML:

<enum name="ImageType" since="2.0">
    <description>Contains information about the type of image.</description>
    <element name="STATIC" />
    <element name="DYNAMIC" />
</enum>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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

import { Enum } from '_path_to_base_classes_/Enum.js';

/**
 * Contains information about the type of image.
 * @typedef {Enum} ImageType
 * @property {Object} _MAP
 */
class ImageType extends Enum {

    /**
     * @constructor
     */
    constructor() {
        super();
    }

    /**
     * @return {String}
     */
    static get STATIC() {
        return ImageType._MAP.STATIC;
    }

    /**
     * @return {String}
     */
    static get DYNAMIC() {
        return ImageType._MAP.DYNAMIC;
    }

    /**
     * Confirms whether the value passed in exists in the Enums of this class
     * @param {String} value
     * @return {null|String} - Returns null if the enum value doesn't exist
     */
    static valueForString(value) {
        return ImageType.valueForStringInternal(value, ImageType._MAP);
    }
}

ImageType._MAP = Object.freeze({
    'STATIC': 'STATIC',
    'DYNAMIC': 'DYNAMIC',
});

export { ImageType };

Example with "internal_name" and "name" attribute:

XML:

<enum name="VrCapabilities" since="1.0">
    <description>Contains information about the VR capabilities.</description>
    <element name="TEXT" internal_name="VR_TEXT"/>
</enum>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
import { Enum } from '_path_to_base_classes_/Enum.js';

/**
 * Contains information about the VR capabilities.
 * @typedef {Enum} VrCapabilities
 * @property {Object} _MAP
 */
class VrCapabilities extends Enum {

    /**
     * @constructor
     */
    constructor() {
        super();
    }

    /**
     * @return {String}
     */
    static get VR_TEXT() {
        return VrCapabilities._MAP.VR_TEXT;
    }

    /**
     * Confirms whether the value passed in exists in the Enums of this class
     * @param {String} value
     * @return {null|String} - Returns null if the enum value doesn't exist
     */
    static valueForString(value) {
        return VrCapabilities.valueForStringInternal(value, VrCapabilities._MAP);
    }
}

VrCapabilities._MAP = Object.freeze({
    'VR_TEXT': 'TEXT',
});

export { VrCapabilities };

Example with "value" attribute:

XML:

<enum name="PredefinedWindows" since="6.0">
    <element name="DEFAULT_WINDOW" value="0">
        <description>The default window is a main window pre-created on behalf of the app.</description>
    </element>
    <element name="PRIMARY_WIDGET" value="1">
        <description>The primary widget of the app.</description>
    </element>
</enum>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
import { Enum } from '_path_to_base_classes_/Enum.js';

/**
 * @typedef {Enum} PredefinedWindows
 * @property {Object} _MAP
 */
class PredefinedWindows extends Enum {

    /**
     * @constructor
     */
    constructor() {
        super();
    }

    /**
     * The default window is a main window pre-created on behalf of the app.
     * @return {Number}
     */
    static get DEFAULT_WINDOW() {
        return PredefinedWindows._MAP.DEFAULT_WINDOW;
    }

    /**
     * The primary widget of the app.
     * @return {Number}
     */
    static get PRIMARY_WIDGET() {
        return PredefinedWindows._MAP.PRIMARY_WIDGET;
    }

    /**
     * Confirms whether the value passed in exists in the Enums of this class
     * @param {String} value
     * @return {null|Number} - Returns null if the enum value doesn't exist
     */
    static valueForString(value) {
        return PredefinedWindows.valueForStringInternal(value, PredefinedWindows._MAP);
    }
}

PredefinedWindows._MAP = Object.freeze({
    'DEFAULT_WINDOW': 0,
    'PRIMARY_WIDGET': 1,
});

export { PredefinedWindows };

Example with "hexvalue" attribute:

XML:

<enum name="FunctionID" internal_scope="base" since="1.0">
    <description>Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes enumeration starts at value 0.</description>
    <element name="RESERVED" value="0" since="1.0" />
    <element name="RegisterAppInterfaceID" value="1" hexvalue="1" since="1.0" />
    <element name="SliderID" value="26" hexvalue="1A" since="2.0" />
</enum>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS"
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
import { Enum } from '_path_to_base_classes_/Enum.js';

/**
 * Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes enumeration starts at value 0.
 * @typedef {Enum} FunctionID
 * @property {Object} _MAP
 */
class FunctionID extends Enum {

    /**
     * @constructor
     */
    constructor() {
        super();
    }

    /**
     * @return {Number}
     */
    static get RESERVED() {
        return FunctionID._MAP.RESERVED;
    }

    /**
     * @return {Number}
     */
    static get RegisterAppInterfaceID() {
        return FunctionID._MAP.RegisterAppInterfaceID;
    }

    /**
     * @return {Number}
     */
    static get SliderID() {
        return FunctionID._MAP.SliderID;
    }

    /**
     * Confirms whether the value passed in exists in the Enums of this class
     * @param {String} value
     * @return {null|Number} - Returns null if the enum value doesn't exist
     */
    static valueForString(value) {
        return FunctionID.valueForStringInternal(value, FunctionID._MAP);
    }
}

FunctionID._MAP = Object.freeze({
    'RESERVED': 0x0,
    'RegisterAppInterfaceID': 0x1,
    'SliderID': 0x1A,
});

export { FunctionID };

<struct>

All Struct classes should be stored in the folder with name structs and the name of the script is the value from the "name" attribute of <struct> following by the extension .js.

Example:

structs/Image.js

The first of all the script should import the base RpcStruct class and the produced class should extend it. The name of the class is the value from the "name" attribute of <struct>. Then the script should import all Enum and Struct classes, if such are using in the represented structure. The constructor has one parameter named parameters to pass the JavaScript object with initial values of the represented structure and should call super(parameters) to pass this object into the parent class.

Example:

import { RpcStruct } from '_path_to_base_classes_/RpcStruct.js';
import { ImageType } from '../enums/ImageType.js';
class Image extends RpcStruct {
    constructor(parameters) {
        super(parameters);
    }
}

For each <param> the getter and setter methods should be defined in the class:

    The name of the getter is the camelCase formatted value of the "name" attribute with the get prefix, for the setter the prefix should be set.
    If the <param> has the "type" attribute value as one of Boolean, Float, Integer, String, the getter should return the result of the this.getParameter method by the key from the rule 1; The setter should return the result of the this.setParameter method, where the first parameter of this method is the key from the rule 1, the second is the value passed into setter.
    If the <param> has the "type" attribute value as the one of <enum> or <struct> name, the getter should return the result of the this.getObject method, where the first parameter of this method is the corresponding Struct or Enum class, the second is the key from the rule 1; The setter should return the result of the this.setParameter method, where the first parameter of this method is the key from the rule 1, the second is the value passed into setter; The passed in the setter value previously should be validated by calling the this.validateType method, where the fist parameter is the Struct or Enum class corresponding to the "type" attribute value of <param>, the second is the value itself. Example:

setValue(value) {
    return this.setParameter(KEY_VALUE, value);
}

getValue() {
    return this.getParameter(KEY_VALUE);
}

setImageType(type) {
    this.validateType(ImageType, type);

    return this.setParameter(KEY_IMAGE_TYPE, type);
}

getImageType() {
    return this.getObject(Image, KEY_IMAGE_TYPE);
}

Then the <struct>'s set of <param> should be mapped to the static properties of the new class by following rules:

    The name of the property is the SCREAMING_SNAKE_CASE formatted value of the "name" attribute of <param> with the KEY_ prefix.
    The value of the property is the value of the "name" attribute of <param>

Example:

Image.KEY_VALUE = 'value';
Image.KEY_IMAGE_TYPE = 'imageType';
Image.KEY_IS_TEMPLATE = 'isTemplate';

Finally, the script should export the produced class.

Example:

export default { Image };

Below is the full example of the Struct class with simple and Enum parameters inside:

XML:

<struct name="Image" since="2.0">
    <param name="value" minlength="0" maxlength="65535" type="String" mandatory="true">
        <description>Either the static hex icon value or the binary image file name identifier (sent by PutFile).</description>
    </param>
    <param name="imageType" type="ImageType" mandatory="true">
        <description>Describes, whether it is a static or dynamic image.</description>
    </param>
    <param name="isTemplate" type="Boolean" mandatory="false" since="5.0">
        <description>If true, the image is a template image and can be recolored by the HMI</description>
    </param>
</struct>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS"
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
import { RpcStruct } from '_path_to_base_classes_/RpcStruct.js';
import { ImageType } from '../enums/ImageType.js';

class Image extends RpcStruct {

    constructor(parameters) {
        super(parameters);
    }

    setValue(value) {
        return this.setParameter(KEY_VALUE, value);
    }

    getValue() {
        return this.getParameter(KEY_VALUE);
    }

    setImageType(type) {
        this.validateType(ImageType, type);

        return this.setParameter(KEY_IMAGE_TYPE, type);
    }

    getImageType() {
        return this.getObject(Image, KEY_IMAGE_TYPE);
    }

    setIsTemplate(isTemplate) {
        return this.setParameter(KEY_IS_TEMPLATE, isTemplate);
    }

    getIsTemplate() {
        return this.getParameter(KEY_IS_TEMPLATE);
    }

}

Image.KEY_VALUE = 'value';
Image.KEY_IMAGE_TYPE = 'imageType';
Image.KEY_IS_TEMPLATE = 'isTemplate';

export default { Image };

<function>

All Function classes should be stored in the folder with the name messages and the name of the script is the value from the "name" attribute of <function> (following by additional suffix Response for the response value of "messagetype" attribute) following by the extension .js.

Example:

messages/AddCommand.js
messages/AddCommandResponse.js
messages/OnLanguageChange.js

There are some prerequisites for the Function class:

    The first of all, based on the value of the "messagetype" attribute of <function>, the script should import the base RpcRequest, RpcResponse or RpcNotification class and the produced class should extend it.
    The second required thing is the import of the enums/FunctionID.js. This required for getting the functionID hex value of the current RPC function. The key of the required <element> of FunctionID enum is the value from the "functionID" attribute of <function>.
    Then the script should import all Enum and Struct classes, if such are using in the function params.
    The name of the class is the value from the "name" attribute of <function> (following by additional suffix Response for the response value of "messagetype"), e.g. AddCommand, AddCommandResponse, OnLanguageChange.
    The constructor has one parameter named store to pass the JavaScript object with initial values of the function params and should call super(store) to pass this object into the parent class.
    The constructor should call this.setFunctionName method with the correspond FunctionID value described in the point 2, e.g. FunctionID.AddCommandID.

Example:

import { RpcRequest } from '_path_to_base_classes_/RpcRequest.js';
import { FunctionID } from '../enums/FunctionID.js';
import { Image } from '../enums/Image.js';
import { MenuParams } from '../enums/MenuParams.js';

class AddCommand extends RpcRequest {

    constructor(store) {
        super(store);
        this.setFunctionName(FunctionID.AddCommandID);
    }
}

Example:

import { RpcResponse } from '_path_to_base_classes_/RpcResponse.js';
import { FunctionID } from '../enums/FunctionID.js';


class AddCommandResponse extends RpcResponse {

    constructor(store) {
        super(store);
        this.setFunctionName(FunctionID.AddCommandID);
    }
}

Example:

import { RpcNotification } from '_path_to_base_classes_/RpcNotification.js';
import { FunctionID } from '../enums/FunctionID.js';
import { Language } from '../enums/Language.js';
import { MenuParams } from '../enums/MenuParams.js';

class OnLanguageChange extends RpcNotification {

    constructor(store) {
        super(store);
        this.setFunctionName(FunctionID.OnLanguageChangeID);
    }
}

For each <param> the getter and setter methods should be defined in the class:

    The name of the getter is the camelCase formatted value of the "name" attribute with the get prefix, for the setter the prefix should be set.
    If the <param> has the "type" attribute value as one of Boolean, Float, Integer, String, the getter should return the result of the this.getParameter method by the key from the rule 1; the setter should return the result of the this.setParameter method, where the first parameter of this method is the key from the rule 1, the second is the value passed into setter.
    If the <param> has the "type" attribute value as the one of <enum> or <struct> name, the getter should return the result of the this.getObject method, where the first parameter of this method is the corresponding Struct or Enum class, the second is the key from the rule 1; The setter should return the result of the this.setParameter method, where the first parameter of this method is the key from the rule 1, the second is the value passed into setter; The passed value in the setter previously should be validated by calling the this.validateType method, where the fist parameter is the Struct or Enum class corresponding to the "type" attribute value of <param>, the second is the value itself.
    The exclusion are <param> with name success, resultCode and info of <function> with the attribute messagetype="response", in this case they should be omitted.

Example:

setCmdID(id) {
    return this.setParameter(KEY_CMD_ID, id);
}

getCmdID() {
    return this.getParameter(KEY_CMD_ID);
}

setMenuParams(menuParams) {
    this.validateType(MenuParams, menuParams);

    return this.setParameter(KEY_MENU_PARAMS, menuParams);
}

getMenuParams() {
    return this.getObject(MenuParams, KEY_MENU_PARAMS);
}

getHmiDisplayLanguage() {
  return this.getObject(Language, KEY_HMI_DISPLAY_LANGUAGE);
}

setHmiDisplayLanguage(language) {
  this.validateType(Language, language);

  return this.setParameter(KEY_HMI_DISPLAY_LANGUAGE, language);
}

Then the <function>'s set of <param> should be mapped to the static properties of the new class by following rules:

    The name of the property is the SCREAMING_SNAKE_CASE formatted value of the "name" attribute of <param> with the KEY_ prefix.
    The value of the property is the value of the "name" attribute of
    The exclusion are <param> with name success, resultCode and info of <function> with the attribute messagetype="response", in this case they should be omitted.

Example:

AddCommand.KEY_CMD_ID = 'cmdID';
OnLanguageChange. KEY_LANGUAGE = 'language';
OnLanguageChange.KEY_HMI_DISPLAY_LANGUAGE = 'hmiDisplayLanguage';

Finally, the script should export the produced class.

Example:

export default { AddCommand };

Below are full examples for Request, Response and Notification.
Request Example:

XML:

<function name="AddCommand" functionID="AddCommandID" messagetype="request" since="1.0">
    <description>
        Adds a command to the in application menu.
        Either menuParams or vrCommands must be provided.
    </description>

    <param name="cmdID" type="Integer" minvalue="0" maxvalue="2000000000" mandatory="true">
        <description>unique ID of the command to add.</description>
    </param>

    <param name="menuParams" type="MenuParams" mandatory="false">
        <description>Optional sub value containing menu parameters</description>
    </param>

    <param name="vrCommands" type="String" minsize="1" maxsize="100" maxlength="99" array="true" mandatory="false">
        <description>
            An array of strings to be used as VR synonyms for this command.
            If this array is provided, it may not be empty.
        </description>
    </param>

    <param name="cmdIcon" type="Image" mandatory="false" since="2.0">
        <description>
            Image struct determining whether static or dynamic icon.
            If omitted on supported displays, no (or the default if applicable) icon shall be displayed.
        </description>
    </param>

</function>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS"
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

import { RpcRequest } from '_path_to_base_classes_/RpcRequest.js';
import { FunctionID } from '../enums/FunctionID.js';
import { MenuParams } from '../structs/MenuParams.js';
import { Image } from '../structs/Image.js';

class AddCommand extends RpcRequest {

    constructor(parameters) {
        super(parameters);
        this.setFunctionName(FunctionID.AddCommandID);
    }

    getCmdID() {
        return this.getParameter(KEY_CMD_ID);
    }

    setCmdID(cmdID) {
        return this.setParameter(KEY_CMD_ID, cmdID);
    }

    getMenuParams() {
        return this.getObject(MenuParams, KEY_MENU_PARAMS);
    }

    setMenuParams(params) {
        this.validateType(MenuParams, params);

        return this.setParameter(KEY_MENU_PARAMS, params);
    }

    getVrCommands() {
        return this.getParameter(KEY_VR_COMMANDS);
    }

    setVrCommands(vrCommands) {
        return this.setParameter(KEY_VR_COMMANDS, vrCommands);
    }

    getCmdIcon() {
        return this.getObject(Image, KEY_CMD_ICON);
    }

    setCmdIcon(icon) {
        this.validateType(Image, icon);

        return this.setParameter(KEY_CMD_ICON, icon);
    }

}

AddCommand.KEY_CMD_ID = "cmdID";
AddCommand.KEY_MENU_PARAMS = "menuParams";
AddCommand. KEY_VR_COMMANDS = "vrCommands";
AddCommand.KEY_CMD_ICON = "cmdIcon";

export default { AddCommand };

Response Example:

    Please pay attention that no other parameters for this example except "info", "success" and "resultCode", thus they were omitted and only the constructor and other parameters are present)

XML:

<function name="PerformInteraction" functionID="PerformInteractionID" messagetype="response" since="1.0">
    <param name="success" type="Boolean" platform="documentation" mandatory="true">
        <description> true if successful; false, if failed </description>
    </param>

    <param name="resultCode" type="Result" platform="documentation" mandatory="true">
        <description>See Result</description>
        <element name="SUCCESS"/>
        <element name="INVALID_DATA"/>
        <element name="OUT_OF_MEMORY"/>
        <element name="TOO_MANY_PENDING_REQUESTS"/>
        <element name="APPLICATION_NOT_REGISTERED"/>
        <element name="GENERIC_ERROR"/>
        <element name="REJECTED"/>
        <element name="INVALID_ID"/>
        <element name="DUPLICATE_NAME"/>
        <element name="TIMED_OUT"/>
        <element name="ABORTED"/>
        <element name="UNSUPPORTED_RESOURCE"/>
        <element name="WARNINGS"/>
    </param>

    <param name="info" type="String" maxlength="1000" mandatory="false" platform="documentation">
        <description>Provides additional human readable info regarding the result.</description>
    </param>

    <param name="choiceID" type="Integer" minvalue="0" maxvalue="2000000000" mandatory="false">
        <description>
            ID of the choice that was selected in response to PerformInteraction.
            Only is valid if general result is "success:true".
        </description>
    </param>

    <param name="manualTextEntry" type="String" maxlength="500" mandatory="false" since="3.0">
        <description>
            Manually entered text selection, e.g. through keyboard
            Can be returned in lieu of choiceID, depending on trigger source
        </description>
    </param>

    <param name="triggerSource" type="TriggerSource" mandatory="false">
        <description>
            See TriggerSource
            Only is valid if resultCode is SUCCESS.
        </description>
    </param>

</function>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS"
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

import { RpcResponse } from '_path_to_base_classes_/RpcResponse.js';
import { FunctionID } from '../enums/FunctionID.js';
import { TriggerSource } from '../enums/TriggerSource.js';

class PerformInteractionResponse extends RpcResponse {

    constructor(store) {
          super(store);
          this.setFunctionName(FunctionID.PerformInteractionID);
    }

    getChoiceID() {
        return this.getParameter(KEY_CHOICE_ID);
    }

    setChoiceID(choiceID) {
        return this.setParameter(KEY_CHOICE_ID, choiceID);
    }

    getManualTextEntry() {
        return this.getParameter(KEY_MANUAL_TEXT_ENTRY);
    }

    setManualTextEntry(manualTextEntry) {
        return this.setParameter(KEY_MANUAL_TEXT_ENTRY, manualTextEntry);
    }

    getTriggerSource() {
        return this.getObject(TriggerSource, KEY_TRIGGER_SOURCE);
    }

    setTriggerSource(triggerSource) {
        this.validateType(TriggerSource, triggerSource);

        return this.setParameter(KEY_TRIGGER_SOURCE, triggerSource);
    }
}

PerformInteractionResponse.KEY_CHOICE_ID = "choiceID";
PerformInteractionResponse.KEY_MANUAL_TEXT_ENTRY = "manualTextEntry";
PerformInteractionResponse.KEY_TRIGGER_SOURCE = "triggerSource";

export default { PerformInteractionResponse };

Notification Example:

XML:

<function name="OnLanguageChange" functionID="OnLanguageChangeID" messagetype="notification" since="2.0">
    <param name="language" type="Language" mandatory="true">
        <description>Current SDL voice engine (VR+TTS) language</description>
    </param>
    <param name="hmiDisplayLanguage" type="Language" mandatory="true">
        <description>Current display language</description>
    </param>
</function>

The Output:

/*
* Copyright (c) 2019, SmartDeviceLink Consortium, Inc.
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
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS"
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

import { RpcNotification } from '_path_to_base_classes_/RpcNotification.js';
import { FunctionID } from '../enums/FunctionID.js';
import { Language } from '../enums/Language.js';

class OnLanguageChange extends RpcNotification {

  constructor(store) {
      super(store);
      this.setFunctionName(FunctionID.OnLanguageChangeID);
  }

  getLanguage() {
    return this.getObject(Language, KEY_LANGUAGE);
  }

  setLanguage(language) {
    this.validateType(Language, language);

    return this.setParameter(KEY_LANGUAGE, language);
  }

  getHmiDisplayLanguage() {
    return this.getObject(Language, KEY_HMI_DISPLAY_LANGUAGE);
  }

  setHmiDisplayLanguage(language) {
    this.validateType(Language, language);

    return this.setParameter(KEY_HMI_DISPLAY_LANGUAGE, language);
  }

}

OnLanguageChange.KEY_LANGUAGE = "language";
OnLanguageChange.KEY_HMI_DISPLAY_LANGUAGE = "hmiDisplayLanguage";

export default { OnLanguageChange };