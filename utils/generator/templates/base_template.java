/*
 * Copyright (c) 2017 - 2019, SmartDeviceLink Consortium, Inc.
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
 * Neither the name of the SmartDeviceLink Consortium, Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
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
package {{package_name}};
{% for i in imports %}
{%- if i != '' %}
import {{i}};{{ '\n' if loop.last }}
    {%- else %}
{{''}}
    {%- endif %}
    {%- endfor %}
    {%- if description is defined or since is defined or see is defined %}
/**
 {%- if description is defined %}
 {%- for d in description %}
 * {{d}}
 {%- endfor %}{%- endif %}
 *
 {%- if params is defined %}
 * <p><b>Parameter List</b></p>
 *
 * <table border="1" rules="all">
 *  <tr>
 *      <th>Param Name</th>
 *      <th>Type</th>
 *      <th>Description</th>
 *      <th>Req.</th>
 *      <th>Notes</th>
 *      <th>Version Available</th>
 *  </tr>
 {%- for param in params %}
 *  <tr>
 *      <td>{{param.origin}}</td>
 *      <td>{{param.return_type}}</td>
 *      <td>{%- for d in param.description %}{{d}}{%- endfor %}</td>
 *      <td>{{param.mandatory}}</td>
 *      <td></td>
 *      <td></td>
 *  </tr>
 {%- endfor %}
 *
 * </table>
 {%- endif %}
 {%- if description is defined and (see is defined or since is defined) %}
 *
 {%- endif %}
 {%- if see is defined %}
 * @see {{see}}
{%- endif %}
{%- if since is defined %}
 * @since SmartDeviceLink {{since}}
{%- endif %}
 */
    {%- endif %}
    {%- block body %}
    {% endblock -%}