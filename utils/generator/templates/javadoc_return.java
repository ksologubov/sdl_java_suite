     {%- if p.param_doc is not defined %}
     {%- if p.description is defined %}
     {%- for d in p.description %}
     {%- if loop.index == 1 -%}
     * @return {{p.return_type}} {{d}}
     {%- else -%}
     * {{d}}
     {%- endif -%}{%- endfor -%}
     {%- else %}
     * @return {{p.return_type}}
     {%- endif -%}
     {%- else -%}
     {%- set l = p.return_type|length + 8 -%}
     * {% for v in p.param_doc -%}
     {%- if loop.index == 1 -%}
     @return {{p.return_type}} {{v}}
     {%- else -%}
     * {{v|indent(l,True)}}
     {%- endif -%}{% endfor -%}
     {%- endif -%}
     {%- if p.since is defined %}
     * @since SmartDeviceLink {{p.since}}
     {%- endif %}